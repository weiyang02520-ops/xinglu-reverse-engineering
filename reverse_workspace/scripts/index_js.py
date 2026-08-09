#!/usr/bin/env python3
"""Phase 8: automated indexing of JS bundles.

Produces (into reverse_workspace/indexes/):
  STRINGS.json        — Chinese UI strings (unique, from core bundles)
  URLS.json           — all http(s)/ws(s) URLs
  ENDPOINTS.json      — API path patterns (api/... paths, method hints)
  STORAGE_KEYS.json   — localStorage/sessionStorage keys
  ROUTES.json         — route-like string patterns
  IMPORTS.json        — static import() chunk references
  FUNCTION_HINTS.json — IPC channel / handler names
"""
import json
import os
import re
import sys
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(BASE, ".."))
FORMATTED = os.path.join(WS, "formatted")
INDEXES = os.path.join(WS, "indexes")
os.makedirs(INDEXES, exist_ok=True)

CORE_FILES = [
    "main.js",
    "preload.cjs",
    "index-CvAAoCbC.js",
    "rendererApp-D0lJ3WIN.js",
    "index-D-s4yRj5.js",
]

chinese = []
urls = []
endpoints = []
storage_keys = []
routes = []
imports = []
ipc_channels = []

CN_RE = re.compile(r"[一-鿿　-〿＀-￯]{2,}")
URL_RE = re.compile(r"(?:(?:https?|wss?|ftp)://[^\s\"'`<>()\\]+)")
PATH_RE = re.compile(r"[\"'`](/[a-zA-Z0-9_./{}:?=&-]{3,120}?)[\"'`]")
STORAGE_RE = re.compile(r"(?:localStorage|sessionStorage)\.(?:getItem|setItem|removeItem)\(\s*[\"']([^\"']+)[\"']")
ROUTE_RE = re.compile(r"(?:path|to|route|navigate|href)\s*[:=]\s*[\"'](/?[a-zA-Z0-9_./:-]{2,80}?)[\"']")
IMPORT_RE = re.compile(r"(?:import\(|from\s+[\"'])([a-zA-Z0-9_./@-]+\.(?:js|mjs|ts|jsx|tsx|cjs))(?:[\"']|\))")
IPC_RE = re.compile(r"novelforge:[\w-]+")

for fname in CORE_FILES:
    path = os.path.join(FORMATTED, fname)
    if not os.path.exists(path):
        continue
    data = open(path, encoding="utf-8", errors="replace").read()
    src = fname

    for m in CN_RE.finditer(data):
        s = m.group(0).strip()
        if len(s) >= 3:
            chinese.append({"text": s, "file": src})

    for u in URL_RE.findall(data):
        u = u.rstrip(".,;)]}")
        urls.append({"url": u, "file": src})

    for m in PATH_RE.finditer(data):
        p = m.group(1)
        if p.startswith("/api/") or "/api/" in p or p.startswith("/v1/"):
            endpoints.append({"path": p, "file": src})

    for k in STORAGE_RE.findall(data):
        storage_keys.append({"key": k, "file": src})

    for m in ROUTE_RE.finditer(data):
        routes.append({"route": m.group(1), "file": src})

    for m in IMPORT_RE.finditer(data):
        imports.append({"mod": m.group(1), "file": src})

    for c in IPC_RE.findall(data):
        ipc_channels.append({"channel": c, "file": src})

def uniq(items, keyfn):
    seen = set()
    out = []
    for it in items:
        k = keyfn(it)
        if k not in seen:
            seen.add(k)
            out.append(it)
    return out

# 去重并按出现次数(中文)或字母序输出
cn_counter = Counter(f"{x['text']}|{x['file']}" for x in chinese)
chinese = uniq(chinese, lambda x: x["text"])
urls = uniq(urls, lambda x: x["url"])
endpoints = uniq(endpoints, lambda x: x["path"])
storage_keys = uniq(storage_keys, lambda x: x["key"])
routes = uniq(routes, lambda x: x["route"])
imports = uniq(imports, lambda x: x["mod"])
ipc_channels = uniq(ipc_channels, lambda x: x["channel"])

with open(os.path.join(INDEXES, "STRINGS.json"), "w", encoding="utf-8") as f:
    json.dump(chinese, f, ensure_ascii=False, indent=1)
with open(os.path.join(INDEXES, "URLS.json"), "w", encoding="utf-8") as f:
    json.dump(urls, f, ensure_ascii=False, indent=1)
with open(os.path.join(INDEXES, "ENDPOINTS.json"), "w", encoding="utf-8") as f:
    json.dump(endpoints, f, ensure_ascii=False, indent=1)
with open(os.path.join(INDEXES, "STORAGE_KEYS.json"), "w", encoding="utf-8") as f:
    json.dump(storage_keys, f, ensure_ascii=False, indent=1)
with open(os.path.join(INDEXES, "ROUTES.json"), "w", encoding="utf-8") as f:
    json.dump(routes, f, ensure_ascii=False, indent=1)
with open(os.path.join(INDEXES, "IMPORTS.json"), "w", encoding="utf-8") as f:
    json.dump(imports, f, ensure_ascii=False, indent=1)
with open(os.path.join(INDEXES, "FUNCTION_HINTS.json"), "w", encoding="utf-8") as f:
    json.dump(ipc_channels, f, ensure_ascii=False, indent=1)

print(f"中文字符串: {len(chinese)}")
print(f"URL: {len(urls)}")
print(f"API 路径: {len(endpoints)}")
print(f"存储键: {len(storage_keys)}")
print(f"路由: {len(routes)}")
print(f"import 引用: {len(imports)}")
print(f"IPC 通道: {len(ipc_channels)}")
