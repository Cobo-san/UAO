#!/usr/bin/env python3
"""
FreeBSD Sandbox VM Database & Optimization Registrar
Registers FreeBSD Sandbox VM configuration, ZFS ARC limits, VirtIO specs,
and GCP regional lock (us-east1-b) in universal_synaptic_matrix.sqlite.
"""

import os
import sys
import json
import sqlite3
import time
import platform

ACCOUNT_EMAIL = "sounddharma@gmail.com"
GCP_PROJECT_ID = "anaconda-google-project-sounddharma"

def get_current_os():
    return platform.system()

def get_db_path():
    if get_current_os() == "Windows":
        return r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\universal_synaptic_matrix.sqlite"
    else:
        return "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/synaptic_matrix/universal_synaptic_matrix.sqlite"

def main():
    print("=== REGISTERING FREEBSD SANDBOX VM IN SQLITE MATRIX ===")
    db_path = get_db_path()
    if not os.path.exists(db_path):
        print("[-] Database missing.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS freebsd_vm_sandbox_registry (
        vm_id TEXT PRIMARY KEY,
        vm_name TEXT,
        vcpus INTEGER,
        ram_gb REAL,
        zfs_arc_max TEXT,
        gcp_region_lock TEXT,
        cobo_san_build_status TEXT,
        timestamp_utc TEXT
    );
    """)

    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    cursor.execute("""
    INSERT OR REPLACE INTO freebsd_vm_sandbox_registry VALUES (
        'freebsd_sandbox_node_01',
        'FreeBSD-Sandbox-CoboSan',
        24,
        24.0,
        '8G (Optimized for 16GB LLM Inference)',
        'us-east1-b (South Carolina Zone B)',
        'UNIFIED_COBO_SAN_BUILD_UNPACKED',
        ?
    );
    """, (ts,))

    conn.commit()
    conn.close()

    print(f"[+] FreeBSD Sandbox VM Registered in SQLite Matrix: {db_path}")
    print("[OK] FREEBSD SANDBOX REGISTRATION COMPLETE WITH 100% SUCCESS!")

if __name__ == "__main__":
    main()
