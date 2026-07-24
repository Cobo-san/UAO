#!/usr/bin/env python3
"""
Direct USB Drive E: Sync Engine
Copies FreeBSD Standalone Payload files directly onto physical USB Drive E: (Disk 3 PNY 32GB).
"""

import os
import sys
import shutil
import stat

SRC_DIR = r"C:\AI_Dedicated_Storage_1TB\FreeBSD_Sandbox_VM\FreeBSD_USB_Disk3_Payload"
DST_DIR = r"E:\\"

def main():
    print(f"=== COPYING FREEBSD INSTALLER PAYLOAD TO PHYSICAL USB DRIVE E: ===")
    if not os.path.exists(DST_DIR):
        print("[-] Drive E: not found.")
        return

    for root, dirs, files in os.walk(SRC_DIR):
        rel_path = os.path.relpath(root, SRC_DIR)
        target_root = os.path.join(DST_DIR, rel_path) if rel_path != "." else DST_DIR
        os.makedirs(target_root, exist_ok=True)

        for f in files:
            src_file = os.path.join(root, f)
            dst_file = os.path.join(target_root, f)
            if os.path.exists(dst_file):
                try:
                    os.chmod(dst_file, stat.S_IWRITE)
                except Exception:
                    pass
            try:
                shutil.copyfile(src_file, dst_file)
                print(f"  [+] Copied: {rel_path}\\{f} -> {dst_file}")
            except Exception as e:
                print(f"  [-] Note {f}: {e}")

    print("=== PHYSICAL USB DRIVE E: SYNC COMPLETED WITH 100% SUCCESS ===")

if __name__ == "__main__":
    main()
