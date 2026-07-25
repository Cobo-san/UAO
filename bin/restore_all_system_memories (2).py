#!/usr/bin/env python3
"""
Master Memory Restoration Engine
Restores all system memories, subagent states, MCP kernel routes, token caches,
and distro-to-region GCP locks from the latest golden snapshot into the universal synaptic matrix.
"""

import os
import sys
import json
import sqlite3
import time
import platform
from pathlib import Path

ACCOUNT_EMAIL = "sounddharma@gmail.com"

def get_current_os():
    return platform.system()

def get_paths():
    if get_current_os() == "Windows":
        return {
            "living_repo": r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository",
            "db_path": r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\universal_synaptic_matrix.sqlite",
            "golden_snapshots": r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\golden_snapshots"
        }
    else:
        return {
            "living_repo": "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository",
            "db_path": "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/synaptic_matrix/universal_synaptic_matrix.sqlite",
            "golden_snapshots": "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/golden_snapshots"
        }

def find_latest_snapshot(snapshots_dir):
    if not os.path.exists(snapshots_dir):
        return None
    files = [f for f in os.listdir(snapshots_dir) if f.startswith("snapshot_") and f.endswith(".json")]
    if not files:
        return None
    files.sort(reverse=True)
    return os.path.join(snapshots_dir, files[0])

def restore_memories_from_json(snapshot_json_path, db_path):
    if not os.path.exists(snapshot_json_path):
        print(f"[!] Snapshot file not found: {snapshot_json_path}")
        return False

    with open(snapshot_json_path, 'r', encoding='utf-8') as f:
        snapshot_data = json.load(f)

    tables_data = snapshot_data.get("tables_data", {})
    metadata = snapshot_data.get("export_metadata", {})

    print(f"[*] Restoring snapshot metadata: {metadata.get('timestamp_utc')} UTC ({metadata.get('total_tables')} tables)")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Enable WAL mode for high performance
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")

    restored_tables = 0
    total_records = 0

    for table_name, records in tables_data.items():
        if isinstance(records, str):  # error message string
            continue
        if not isinstance(records, list):
            continue

        if not records:
            restored_tables += 1
            continue

        # Get column names from the first record
        cols = list(records[0].keys())
        placeholders = ", ".join(["?"] * len(cols))
        col_names = ", ".join([f"`{c}`" for c in cols])

        # Delete existing data in table to ensure clean restore
        try:
            cursor.execute(f"DELETE FROM `{table_name}`;")
        except sqlite3.OperationalError:
            # Table might not exist, will create dynamically if needed
            pass

        insert_sql = f"INSERT OR REPLACE INTO `{table_name}` ({col_names}) VALUES ({placeholders});"

        table_count = 0
        for rec in records:
            vals = [rec[c] for c in cols]
            try:
                cursor.execute(insert_sql, vals)
                table_count += 1
            except Exception as e:
                print(f"[!] Error restoring record into {table_name}: {e}")

        conn.commit()
        restored_tables += 1
        total_records += table_count
        print(f"  [+] Table `{table_name}`: {table_count} records restored.")

    # Integrity Check
    cursor.execute("PRAGMA quick_check;")
    check_res = cursor.fetchone()
    conn.close()

    print(f"[OK] Restoration complete. Integrity check: {check_res[0]}")
    print(f"[OK] Restored {restored_tables} tables, total {total_records} records.")
    return True

def main():
    print("=== MASTER SYSTEM MEMORY RESTORATION ENGINE ===")
    paths = get_paths()
    
    snapshot_path = find_latest_snapshot(paths["golden_snapshots"])
    if not snapshot_path:
        print("[!] No golden snapshot found to restore.")
        sys.exit(1)

    print(f"[+] Target Snapshot: {os.path.basename(snapshot_path)}")
    print(f"[+] Target Database: {paths['db_path']}")

    success = restore_memories_from_json(snapshot_path, paths["db_path"])

    if success:
        print("[OK] MEMORIES RESTORED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
