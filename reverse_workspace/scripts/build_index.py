#!/usr/bin/env python3
"""Generate FILE_TREE.txt and FILES.csv for extracted/ directory."""
import csv
import hashlib
import os
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "reverse_workspace/extracted")
OUT_TREE = os.path.join(ROOT, "..", "indexes", "FILE_TREE.txt")
OUT_CSV = os.path.join(ROOT, "..", "indexes", "FILES.csv")
os.makedirs(os.path.dirname(OUT_TREE), exist_ok=True)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


PRIORITY_MAP = {
    ".js": "P0", ".mjs": "P0", ".cjs": "P0",
    ".json": "P1",
    ".html": "P1",
    ".map": "P0",
    ".css": "P2",
    ".node": "P1",
    ".dll": "P2",
    ".exe": "P1",
    ".apk": "P1",
    ".png": "P3", ".webp": "P3", ".svg": "P3", ".ico": "P3",
    ".ttf": "P3",
    ".pak": "P3", ".dat": "P3", ".bin": "P3",
}

rows = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    for fn in sorted(filenames):
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, ROOT).replace("\\", "/")
        size = os.path.getsize(full)
        ext = os.path.splitext(fn)[1].lower()
        h = sha256(full)
        prio = PRIORITY_MAP.get(ext, "P2")
        rows.append((rel, size, ext, h, prio))

rows.sort(key=lambda r: r[0])

with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["path", "size", "ext", "sha256", "priority"])
    for r in rows:
        w.writerow(r)

# FILE_TREE.txt: 目录树 (2 levels deep of dirs, all files)
lines = []
def tree(root, prefix="", depth=0):
    entries = sorted(os.listdir(root))
    dirs = [e for e in entries if os.path.isdir(os.path.join(root, e))]
    files = [e for e in entries if not os.path.isdir(os.path.join(root, e))]
    for d in dirs:
        if depth < 6:
            lines.append(f"{prefix}{d}/")
            tree(os.path.join(root, d), prefix + "  ", depth + 1)
    for fn in files:
        size = os.path.getsize(os.path.join(root, fn))
        lines.append(f"{prefix}{fn}  ({size})")

tree(ROOT)
with open(OUT_TREE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"FILES.csv: {len(rows)} files -> {OUT_CSV}")
print(f"FILE_TREE.txt -> {OUT_TREE}")
