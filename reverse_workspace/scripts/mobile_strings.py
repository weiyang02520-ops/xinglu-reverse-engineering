#!/usr/bin/env python3
"""Extract targeted strings from mobile bundle: bridge connection + UI."""
import re
import sys
from collections import Counter

BASE = r"c:\Users\peng\Desktop\逆向\reverse_workspace\formatted\pretty"
data = open(BASE + r"\mobile.pretty.js", encoding="utf-8").read()

print("=== 1. 明确的短字符串(bridge/连接相关) ===")
for m in sorted(set(re.findall(r'["\']([a-zA-Z0-9_./:{}?&=,-]{3,60})["\']', data))):
    if any(k in m.lower() for k in ["bridge", "connect", "pair", "mobile", "server", "http", "url", "key", "protocol", "events", "apk"]):
        print("  ", m)

print("\n=== 2. 中文 UI 字符串(2-30字) ===")
cn = re.findall(r'["\']([一-鿿][^"\'\n]{1,30})["\']', data)
cnt = Counter(cn)
for s, c in cnt.most_common(80):
    print(f"  [{c}] {s}")
