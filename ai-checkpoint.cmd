@echo off
rem ============================================
rem  ai-checkpoint.cmd — 一键 AI 交接检查点
rem  用法: ai-checkpoint  或  ai-checkpoint.cmd
rem  (Windows 双击或命令行执行)
rem ============================================
cd /d "%~dp0"
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 python, 请先安装 Python 并加入 PATH。
    exit /b 3
)
python scripts\ai_checkpoint.py %*
exit /b %errorlevel%
