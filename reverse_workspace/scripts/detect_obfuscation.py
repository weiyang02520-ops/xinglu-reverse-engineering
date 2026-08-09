#!/usr/bin/env python3
"""Obfuscation detection: distinguish minification from real obfuscation."""
import re
import sys

BASE = r"c:\Users\peng\Desktop\逆向\reverse_workspace\formatted"
FILES = ["main.js", "rendererApp-D0lJ3WIN.js", "index-D-s4yRj5.js", "preload.cjs"]

print("========== Obfuscation Detection ==========")
for fname in FILES:
    data = open(f"{BASE}\\{fname}", encoding="utf-8", errors="replace").read()
    print(f"\n--- {fname} ({len(data)} bytes) ---")
    n_eval = len(re.findall(r"\beval\s*\(", data))
    n_func = len(re.findall(r"new\s+Function", data))
    hexstr = len(re.findall(r"\\x[0-9a-fA-F]{2}", data))
    whiles = len(re.findall(r"\bwhile\s*\(", data))
    short_vars = len(re.findall(r"\b(?:var|let|const)\s+[a-zA-Z_$][a-zA-Z0-9_$]{0,2}\s*=", data))
    idents = re.findall(r"\b[a-zA-Z_$][a-zA-Z0-9_$]{1,60}\b", data)
    avg = sum(len(i) for i in idents) / max(1, len(idents))
    lines = data.count("\n")
    print(f"  eval(): {n_eval}")
    print(f"  new Function(): {n_func}")
    print(f"  hex escape strings: {hexstr}")
    print(f"  while loops: {whiles}")
    print(f"  short var decls (1-3 chars): {short_vars}")
    print(f"  avg identifier length: {avg:.1f}")
    print(f"  newlines: {lines}")
