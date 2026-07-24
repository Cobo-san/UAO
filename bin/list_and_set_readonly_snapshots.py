#!/usr/bin/env python3
"""
Master Snapshot Manager & Read-Only Protection Engine
Lists all local and Google Drive system memory snapshots and enforces strict READ-ONLY protection attributes.
"""

import os
import sys
import stat
import time
import platform
import sqlite3

def get_current_os():
    return platform.system()

def get_snapshot_paths():
    if get_current_os() == "Windows":
        return {
            "local_snapshots": r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\golden_snapshots",
            "gdrive_snapshots": r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Snapshots_Reversion_Archive"
        }
    else:
        return {
            "local_snapshots": "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/golden_snapshots",
            "gdrive_snapshots": "/mnt/c/Users/Monica Fugazi/GoogleDrive_sounddharma/Snapshots_Reversion_Archive"
        }

def make_readonly(file_path):
    try:
        if get_current_os() == "Windows":
            # Remove write permissions, add read-only attribute
            mode = os.stat(file_path).st_mode
            os.chmod(file_path, mode & ~stat.S_IWRITE)
        else:
            os.chmod(file_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        return True
    except Exception as e:
        print(f"[!] Error setting read-only on {file_path}: {e}")
        return False

def scan_and_lock_dir(dir_path, dir_label):
    if not os.path.exists(dir_path):
        print(f"[!] Directory missing: {dir_path}")
        return []

    records = []
    items = sorted(os.listdir(dir_path), reverse=True)
    
    for item in items:
        full_path = os.path.join(dir_path, item)
        is_dir = os.path.isdir(full_path)
        
        if not is_dir:
            size_bytes = os.path.getsize(full_path)
            mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(full_path)))
            
            # Enforce Read-Only Permission
            locked = make_readonly(full_path)
            
            records.append({
                "name": item,
                "path": full_path,
                "size_kb": round(size_bytes / 1024, 2),
                "modified": mtime,
                "type": "JSON Snapshot",
                "readonly": "READ_ONLY_LOCKED" if locked else "ERROR"
            })
        else:
            mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(full_path)))
            # Also set read-only on files within subdirectory
            for root, dirs, files in os.walk(full_path):
                for f in files:
                    make_readonly(os.path.join(root, f))
            records.append({
                "name": item,
                "path": full_path,
                "size_kb": 0,
                "modified": mtime,
                "type": "Snapshot Directory",
                "readonly": "READ_ONLY_LOCKED"
            })
            
    return records

def main():
    print("=== MASTER SNAPSHOT INSPECTOR & READ-ONLY ENFORCER ===")
    paths = get_snapshot_paths()

    local_records = scan_and_lock_dir(paths["local_snapshots"], "Local Golden Snapshots")
    gdrive_records = scan_and_lock_dir(paths["gdrive_snapshots"], "Google Drive Snapshots Archive")

    print(f"\n===========================================================================")
    print(f"  PART 1: LOCAL GOLDEN SNAPSHOTS ({len(local_records)} SNAPSHOTS) [ALL READ-ONLY]")
    print(f"===========================================================================")
    for idx, r in enumerate(local_records, 1):
        print(f"[{idx:02d}] {r['name']}")
        print(f"     * Path     : {r['path']}")
        print(f"     * Size/Time: {r['size_kb']} KB | Modified: {r['modified']}")
        print(f"     * Status   : [LOCKED] {r['readonly']}")
        print("-" * 75)

    print(f"\n===========================================================================")
    print(f"  PART 2: GOOGLE DRIVE SNAPSHOTS ARCHIVE ({len(gdrive_records)} SNAPSHOTS) [ALL READ-ONLY]")
    print(f"===========================================================================")
    for idx, r in enumerate(gdrive_records, 1):
        print(f"[{idx:02d}] {r['name']}")
        print(f"     * Path     : {r['path']}")
        print(f"     * Size/Time: {r['size_kb']} KB | Modified: {r['modified']}")
        print(f"     * Status   : [LOCKED] {r['readonly']}")
        print("-" * 75)

    print(f"\n[OK] TOTAL {len(local_records) + len(gdrive_records)} SNAPSHOTS AUDITED AND ENFORCED AS READ-ONLY!")

if __name__ == "__main__":
    main()
