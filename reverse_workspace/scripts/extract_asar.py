#!/usr/bin/env python3
"""Static ASAR extractor — pure Python, no execution of target code.

ASAR layout:
  [4 bytes pickle header magic][4 bytes LE header payload size][JSON header]
  [file data ...]  (file offsets in header are relative to end of header)
"""
import json
import os
import struct
import sys


def read_header(f):
    """Parse asar header with flexible layout detection.

    Layout:
      0x00: 04 00 00 00            pickle magic
      0x04: <u32>                  pickle payload size (includes nested length fields)
      0x08: <u32>                  string size
      0x0c: <u32>                  json size
      0x10: '{' ...                JSON payload
    data_base = 4 + 4 + pickle_size  (points right after the pickle container)
    """
    f.seek(0)
    magic = f.read(4)
    if len(magic) != 4:
        raise ValueError("too small to be asar")
    f.seek(4)
    pickle_size = struct.unpack("<I", f.read(4))[0]
    data_base = 4 + 4 + pickle_size
    f.seek(16)
    payload = f.read(pickle_size)
    header, _ = json.JSONDecoder().raw_decode(payload.decode("utf-8"))
    return header, data_base


def extract_node(node, out_path, f, data_base):
    """Recursively extract files/dirs from asar header tree."""
    for name, child in node.items():
        safe_name = name.lstrip("./")
        target = os.path.join(out_path, safe_name)
        if "files" in child:
            os.makedirs(target, exist_ok=True)
            extract_node(child["files"], target, f, data_base)
        elif "link" in child:
            # symlink-like entry pointing to another path inside the asar
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target + ".LINK", "w") as out:
                out.write(child["link"])
        elif child.get("unpacked"):
            # data lives outside the asar (resources/app.asar.unpacked)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            open(target + ".UNPACKED", "w").close()
        else:
            offset = int(child["offset"])
            size = child["size"]
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as out:
                f.seek(data_base + offset)
                remaining = size
                while remaining > 0:
                    chunk = f.read(min(1 << 20, remaining))
                    if not chunk:
                        raise ValueError("truncated file data")
                    out.write(chunk)
                    remaining -= len(chunk)


def main():
    src = sys.argv[1]
    dst = sys.argv[2]
    with open(src, "rb") as f:
        header, header_end = read_header(f)
        root = header["files"]
        if os.path.exists(dst):
            import shutil

            shutil.rmtree(dst)
        os.makedirs(dst, exist_ok=True)
        extract_node(root, dst, f, header_end)
        print(f"extracted to {dst}")

        # summary
        count = 0
        total = 0

        def walk(node, base=""):
            nonlocal count, total
            for name, child in node.items():
                if "files" in child:
                    walk(child["files"], os.path.join(base, name))
                else:
                    count += 1
                    total += child["size"]

        walk(root)
        print(f"files: {count}, total size: {total}")


if __name__ == "__main__":
    main()
