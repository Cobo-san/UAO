#!/usr/bin/env python3
"""
Clean SQLite Database Rebuilder
Re-creates universal_synaptic_matrix.sqlite cleanly without orphan index corruption.
"""

import os
import sys
import sqlite3
import platform

def get_current_os():
    return platform.system()

def rebuild_clean_db(db_path):
    print(f"[*] Rebuilding clean SQLite database: {db_path}")
    if os.path.exists(db_path):
        try:
            os.chmod(db_path, 0o666)
            os.remove(db_path)
            print(f"  [-] Removed corrupt DB file: {db_path}")
        except Exception as e:
            print(f"  [!] Notice removing file: {e}")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Enable WAL mode
    cursor.execute("PRAGMA journal_mode = WAL;")
    cursor.execute("PRAGMA synchronous = NORMAL;")

    conn.commit()
    conn.close()
    print(f"  [+] Created fresh clean WAL SQLite database at {db_path}")

def main():
    paths = [
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\universal_synaptic_matrix.sqlite",
        r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Parallel_Synaptic_Database_Matrix\universal_synaptic_matrix.sqlite"
    ]
    for p in paths:
        rebuild_clean_db(p)

if __name__ == "__main__":
    main()
