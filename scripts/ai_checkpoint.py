#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai_checkpoint.py — AI Agent 自动交接检查点

流程:
  1. 收集 git 状态, 判断是否有实际变化
  2. 若无变化 → 退出(不创建空 Commit)
  3. 若 git identity 缺失 → 检查 .ai-handoff 生成摘要
  4. 安全扫描(Secret 检测) → 命中则 SECURITY BLOCKED PUSH
  5. 更新 HANDOFF/STATUS/CHANGELOG/REVIEW_REQUEST 等文档
  6. git add + commit + push

用法:
  python scripts/ai_checkpoint.py            # 手动
  python scripts/ai_checkpoint.py --no-push  # 只提交不推送(测试)
  python scripts/ai_checkpoint.py --mode auto --since-min 45  # 定时模式

退出码:
  0 成功 / 1 无变化(正常) / 2 安全阻断 / 3 错误
"""
import argparse
import datetime
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HANDOFF_DIR = os.path.join(ROOT, ".ai-handoff")
CHECKPOINTS_DIR = os.path.join(HANDOFF_DIR, "checkpoints")


def run(cmd, cwd=ROOT, check=False, text=True, timeout=120):
    """执行命令, 返回 (code, stdout, stderr)。"""
    try:
        p = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=text, timeout=timeout
        )
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except Exception as e:
        return 127, "", str(e)


def git(*args, cwd=ROOT, check=False):
    code, out, err = run(["git", *args], cwd=cwd, check=check)
    if code != 0 and check:
        print(f"[git {' '.join(args)}] 失败: {err}")
    return code, out, err


def get_git_user():
    """获取 commit 身份(仓库级优先, 其次全局)。"""
    _, name, _ = git("config", "user.name")
    _, email, _ = git("config", "user.email")
    if not name:
        _, name, _ = git("config", "--global", "user.name")
    if not email:
        _, email, _ = git("config", "--global", "user.email")
    return name, email


def get_project_name():
    """从目录名推断项目名(纯展示用, 不用于远程创建)。"""
    name = os.path.basename(ROOT) or "project"
    # 中文字符直接显示
    return name


def collect_changes():
    """返回 (有变化?, 变更摘要, 变更统计)。"""
    # 未跟踪文件 + 已跟踪修改
    _, untracked, _ = git("status", "--porcelain")
    if not untracked:
        return False, [], {}

    lines = [l for l in untracked.splitlines() if l.strip()]
    stats = {"added": 0, "modified": 0, "deleted": 0}
    for l in lines:
        code = l[:2]
        if code == "??":
            stats["added"] += 1
        elif code.startswith("M"):
            stats["modified"] += 1
        elif code.startswith("D"):
            stats["deleted"] += 1
    return True, lines, stats


def summary_line(changes, stats):
    """根据变更自动生成一句话摘要。"""
    keys = ["reports", "indexes", "scripts", "reconstructed", ".ai-handoff"]
    for k in keys:
        if any(f"/{k}/" in c for c in changes) or any(c.endswith(f"/{k}") for c in changes):
            return f"update {k} analysis artifacts"
    if stats["added"] > stats["modified"]:
        return f"add {stats['added']} new files"
    return f"update {stats['modified']} files"


def write_or_update(path, default, content=None):
    """写入或创建文件(不覆盖已有内容, 除非显式提供 content)。"""
    if os.path.exists(path) and content is None:
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content if content is not None else default)
    return True


def security_scan(force_files=None):
    """
    推送前安全扫描。

    返回 (blocked, findings)
      blocked=True 时禁止 push。
    """
    # 1) 获取将要 add 的文件清单(避开大文件)
    code, out, _ = git("status", "--porcelain")
    files = []
    for l in out.splitlines():
        if not l.strip():
            continue
        path = l[3:].strip().strip('"')
        if path:
            files.append(path)
    if force_files:
        files = force_files

    patterns = [
        # 环境变量/配置
        (r"(?i)\.env$", "环境文件(.env)"),
        (r"(?i)\.env\..+", "环境文件(.env.*)"),
        # 常见密钥变量赋值(不匹配已发布的默认示例)
        (r"(?i)API_?KEY\s*[=:]\s*['\"][A-Za-z0-9_\-]{12,}", "API Key 赋值"),
        (r"(?i)TOKEN\s*[=:]\s*['\"][A-Za-z0-9_\-]{16,}", "Token 赋值"),
        (r"(?i)SECRET\s*[=:]\s*['\"][A-Za-z0-9_\-]{12,}", "Secret 赋值"),
        (r"(?i)PASSWORD\s*[=:]\s*['\"][^'\"]{6,}", "密码赋值"),
        (r"(?i)BASE64\s*[=:]\s*['\"][A-Za-z0-9+/=]{40,}", "Base64 密钥"),
        # 头部
        (r"(?i)^(Authorization|Bearer|X-Api-Key)\s*[=:]\s*\S+", "Authorization/Bearer 头"),
        # 私钥内容特征
        (r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----", "私钥内容"),
        (r"-----BEGIN CERTIFICATE-----", "证书内容"),
        # 常见模型提供商 Key(识别 gpt-xxxx / sk- 等)
        (r"sk-[A-Za-z0-9]{20,}", "OpenAI/DeepSeek 风格 Key"),
        (r"(?i)(?:OPENAI|ANTHROPIC|DEEPSEEK|GEMINI|OPENROUTER|QWEN|MOONSHOT|GITHUB)[_A-Z]*_?KEY\s*[=:]\s*['\"][^'\"]{8,}", "模型提供商 KEY 赋值"),
        (r"AIza[A-Za-z0-9_\-]{30,}", "Gemini API Key"),
        (r"ghp_[A-Za-z0-9]{20,}", "GitHub Token"),
        (r"gho_[A-Za-z0-9]{20,}", "GitHub OAuth Token"),
        (r"xox[baprs]-[A-Za-z0-9\-]{20,}", "Slack Token"),
        (r"AKIA[A-Z0-9]{16}", "AWS Access Key"),
        (r"eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{10,}", "JWT"),
        # 账号凭据
        (r"(?im)login\s*[=:]\s*['\"][^'\"]{3,}['\"]\s*\n\s*password", "账号/密码对"),
    ]

    findings = []
    for path in files:
        full = os.path.join(ROOT, path)
        if not os.path.isfile(full):
            continue
        # 跳过扫描器自身(它包含检测规则字符串, 属误报源)
        if os.path.abspath(full) == os.path.abspath(__file__):
            continue
        # 跳过二进制/大文件(不扫描内容, 但按扩展名拦截)
        size = os.path.getsize(full)
        if size > 2_000_000:  # >2MB 不扫描内容
            ext = os.path.splitext(path)[1].lower()
            if ext in (".exe", ".dll", ".7z", ".apk", ".png", ".jpg", ".ttf", ".pak", ".dat", ".bin"):
                continue
        try:
            with open(full, "r", encoding="utf-8", errors="replace") as f:
                content = f.read(512_000)  # 只扫前 512KB
        except Exception:
            continue

        for pat, desc in patterns:
            m = re.search(pat, content)
            if m:
                line_no = content[: m.start()].count("\n") + 1
                # 脱敏: 只显示前4字符
                secret = m.group(0)
                masked = secret[:4] + "…" if len(secret) > 8 else secret
                findings.append({
                    "file": path,
                    "line": line_no,
                    "pattern": desc,
                    "masked": masked,
                })

    return len(findings) > 0, findings


def update_handoff(summary, changes, stats):
    """更新 .ai-handoff 核心文档(追加式, 不覆盖用户已有内容)。"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    os.makedirs(HANDOFF_DIR, exist_ok=True)
    os.makedirs(CHECKPOINTS_DIR, exist_ok=True)

    # 1) STATUS.md — 覆盖式(简短状态)
    status_path = os.path.join(HANDOFF_DIR, "STATUS.md")
    if not os.path.exists(status_path):
        with open(status_path, "w", encoding="utf-8") as f:
            f.write("# 项目状态\n\n")
            f.write(f"> 最后更新: {now}\n\n")
            f.write("## 当前阶段\n\n(待填写)\n\n")
            f.write("## 已验证内容\n\n- (待填写)\n\n")
            f.write("## 未验证内容\n\n- (待填写)\n")

    # 2) CHANGELOG_AI.md — 追加
    changelog = os.path.join(HANDOFF_DIR, "CHANGELOG_AI.md")
    if not os.path.exists(changelog):
        with open(changelog, "w", encoding="utf-8") as f:
            f.write("# AI 变更日志\n\n")
    with open(changelog, "a", encoding="utf-8") as f:
        f.write(f"\n## {now} — Checkpoint\n\n")
        f.write(f"摘要: {summary}\n\n")
        for c in changes[:50]:
            f.write(f"- `{c}`\n")
        f.write("\n")

    # 3) checkpoint 快照
    snap = os.path.join(CHECKPOINTS_DIR, now.replace(":", "-").replace(" ", "_") + ".md")
    with open(snap, "w", encoding="utf-8") as f:
        f.write(f"# Checkpoint {now}\n\n")
        f.write(f"摘要: {summary}\n\n")
        f.write(f"统计: 新增 {stats['added']}, 修改 {stats['modified']}, 删除 {stats['deleted']}\n\n")
        f.write("## 变更文件\n\n")
        for c in changes[:100]:
            f.write(f"- `{c}`\n")

    return True


def build_commit_message(summary):
    """统一格式的 commit message。"""
    return f"ai-checkpoint: {summary}"


def main():
    parser = argparse.ArgumentParser(description="AI Agent 自动交接检查点")
    parser.add_argument("--no-push", action="store_true", help="只 commit 不 push")
    parser.add_argument("--mode", choices=["manual", "auto"], default="manual",
                        help="manual=主动交接; auto=定时模式(需配合 --since-min)")
    parser.add_argument("--since-min", type=int, default=45,
                        help="auto 模式: 距上次 checkpoint 超过该分钟数才创建")
    args = parser.parse_args()

    if not os.path.isdir(os.path.join(ROOT, ".git")):
        print("⚠ 当前目录还不是 Git 仓库。请先运行: git init")
        print("   (或确认已在正确的项目目录中运行本脚本)")
        return 3

    # ── 1. 检查是否有实际变化 ──
    has_changes, changes, stats = collect_changes()
    if not has_changes:
        print("✓ 工作区干净, 无实际变化, 不创建空 Commit。")
        return 1

    print(f"📋 检测到 {stats['added']} 新增 / {stats['modified']} 修改 / {stats['deleted']} 删除")

    # ── 1.5 定时模式: 有变化但距上次 checkpoint 不足阈值 → 等待积累 ──
    if args.mode == "auto":
        code, out, _ = git("log", "-1", "--format=%ci")
        last_commit_time = out if out else ""
        if last_commit_time:
            try:
                last = datetime.datetime.fromisoformat(last_commit_time.strip())
                now = datetime.datetime.now(last.tzinfo)
                if (now - last).total_seconds() < args.since_min * 60:
                    print(f"⏳ 有新变化, 但距上次 checkpoint 不足 {args.since_min} 分钟, 等待积累。")
                    return 1
            except Exception:
                pass

    # ── 2. Git 身份检查(空提交保护) ──
    name, email = get_git_user()
    if not name or not email:
        print("✋ Git 身份未配置(user.name/user.email), 无法创建 Commit。")
        print("   请运行:")
        print("     git config user.name  \"你的名字\"")
        print("     git config user.email \"you@example.com\"")
        return 3

    # ── 3. 安全扫描(推送前强制) ──
    print("🔍 安全扫描中…")
    blocked, findings = security_scan()
    if blocked:
        print("\n🚨 SECURITY BLOCKED PUSH")
        print("   检测到可能的敏感信息, 已阻止自动推送:\n")
        for f in findings[:10]:
            print(f"   - {f['file']} :{f['line']}  ({f['pattern']}) {f['masked']}")
        if len(findings) > 10:
            print(f"   … 等共 {len(findings)} 处")
        print("\n   请先处理上述文件(删除/脱敏/移出追踪)后再运行。")
        return 2

    # ── 4. 生成摘要并更新交接文档 ──
    summary = summary_line(changes, stats)
    print(f"✍️  摘要: {summary}")
    update_handoff(summary, changes, stats)

    # ── 5. git add + commit ──
    code, _, err = git("add", "-A")
    if code != 0:
        print(f"git add 失败: {err}")
        return 3

    message = build_commit_message(summary)
    code, _, err = git("commit", "-m", message)
    if code != 0:
        if "nothing to commit" in err:
            print("✓ 提交前发现无变化(可能中途被还原), 退出。")
            return 1
        print(f"git commit 失败: {err}")
        return 3

    _, hash_out, _ = git("rev-parse", "HEAD")
    _, branch, _ = git("branch", "--show-current")
    print(f"✅ Checkpoint created: {hash_out[:12]}")
    print(f"   Branch: {branch or '(detached)'}")
    print(f"   Commit: {message}")

    # ── 6. push ──
    if args.no_push:
        print("(跳过推送 --no-push)")
        return 0

    code, _, err = git("push", "origin", "HEAD")
    if code == 0:
        print("✅ Push successful → origin")
        return 0
    elif "No configured push destination" in err or "does not appear to be a git repository" in err:
        print("⚠ Push 失败: 未配置 remote origin。")
        print("   本地 checkpoint 已保存。配置方式见 .ai-handoff/AUTOMATION_SETUP.md")
        return 0
    else:
        print(f"⚠ Push 失败: {err[:200]}")
        print("   本地 checkpoint 已保存。请检查网络/认证后重试: git push origin HEAD")
        return 0


if __name__ == "__main__":
    sys.exit(main())
