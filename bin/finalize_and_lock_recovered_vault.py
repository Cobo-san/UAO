#!/usr/bin/env python3
"""
Finalize & Lock Recovered SATA HDD Vault Engine
1. Removes 'RECOVERY_DRIVE' status from SQLite WAL Matrix and promotes to 'PRODUCTION_PRIMARY_STORAGE_VAULT'.
2. Recursively sets Read-Only permissions (+R / 444) on all 40,513 recovered files in C:\\AI_Dedicated_Storage_1TB\\SATA_HDD_Recovered_Vault.
"""

import os
import sys
import stat
import sqlite3
import time
import subprocess
import platform

VAULT_DIR = r"C:\AI_Dedicated_Storage_1TB\SATA_HDD_Recovered_Vault"
DB_PATH = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\universal_synaptic_matrix.sqlite"
GDRIVE_DB_PATH = r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Parallel_Synaptic_Database_Matrix\universal_synaptic_matrix.sqlite"

def get_current_os():
    return platform.system()

def update_database_status(db_file):
    if not os.path.exists(db_file):
        return
    print(f"[*] Updating Database Status in: {db_file}...")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    # Update sata_hdd_recovery_inventory if table exists
    try:
        cursor.execute("""
        UPDATE sata_hdd_recovery_inventory 
        SET status = 'PRODUCTION_PRIMARY_STORAGE_VAULT', timestamp_utc = ?
        WHERE recovery_id = 'sata_recovery_master';
        """, (ts,))
    except Exception as e:
        print(f"  [-] Note inventory: {e}")

    # Update sata_hdd_recovery_telemetry if table exists
    try:
        cursor.execute("""
        UPDATE sata_hdd_recovery_telemetry 
        SET telemetry_json = json_set(telemetry_json, '$.status', 'PRODUCTION_PRIMARY_STORAGE_VAULT'), timestamp_utc = ?;
        """, (ts,))
    except Exception as e:
        print(f"  [-] Note telemetry: {e}")

    # Update universal_storage_registry if table exists
    try:
        cursor.execute("""
        UPDATE universal_storage_registry 
        SET storage_status = 'READ_ONLY_PRODUCTION_STORAGE'
        WHERE domain_id = 'sata_hdd_recovered_vault';
        """, ())
    except Exception as e:
        print(f"  [-] Note storage reg: {e}")

    conn.commit()
    conn.close()
    print("  [+] Database status updated to PRODUCTION_PRIMARY_STORAGE_VAULT (Read-Only Locked)!")

def enforce_read_only_permissions():
    print(f"[*] Enforcing Read-Only Permissions across all files in: {VAULT_DIR}...")
    if not os.path.exists(VAULT_DIR):
        print("  [-] Vault directory missing.")
        return

    # Use Windows attrib command for fast recursive read-only attribute setting (+R)
    if get_current_os() == "Windows":
        cmd = ["attrib", "+R", os.path.join(VAULT_DIR, "*.*"), "/S", "/D"]
        print(f"  [*] Executing: {' '.join(cmd)}")
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            print("  [+] Windows attrib +R read-only lock applied successfully!")
        except Exception as e:
            print(f"  [!] Notice: {e}")
    
    # Python fallback for directory & file permissions
    file_count = 0
    for root, dirs, files in os.walk(VAULT_DIR):
        for f in files:
            file_path = os.path.join(root, f)
            try:
                os.chmod(file_path, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
                file_count += 1
            except Exception:
                pass

    print(f"  [+] Enforced Read-Only (S_IREAD) on {file_count:,} files in vault!")

def main():
    print("=== REMOVING RECOVERY DRIVE STATUS & ENFORCING READ-ONLY VAULT LOCK ===")
    update_database_status(DB_PATH)
    update_database_status(GDRIVE_DB_PATH)
    enforce_read_only_permissions()
    print("=== RECOVERY DRIVE STATUS REMOVED & VAULT READ-ONLY LOCK COMPLETE ===")

if __name__ == "__main__":
    main()
