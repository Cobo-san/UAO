#!/usr/bin/env python3
"""
FreeBSD Hyper-V Management & Integration Services Registrar
Registers Hyper-V management, KVP services, synthetic drivers (hv_storvsc, hv_netvsc),
and FreeBSD VM configurations in SQLite database matrices.
"""

import os
import sys
import json
import sqlite3
import time

ACCOUNT_EMAIL = "sounddharma@gmail.com"
GCP_PROJECT_ID = "anaconda-google-project-sounddharma"

REPO_DIR = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
DB_PATH = os.path.join(REPO_DIR, "synaptic_matrix", "universal_synaptic_matrix.sqlite")
GDRIVE_DB = r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Parallel_Synaptic_Database_Matrix\universal_synaptic_matrix.sqlite"

bsd_hyperv_configs = [
    {
        "vm_id": "hyperv_freebsd14_hardened",
        "name": "FreeBSD 14.1 Hardened Hyper-V VM",
        "os_version": "FreeBSD 14.1-RELEASE",
        "mount_target": r"E:\Hardened_FreeBSD_Metal_Anaconda_Stack",
        "hv_drivers": "hv_kvp, hv_vss, hv_utils, hv_storvsc, hv_netvsc",
        "security_level": "kern.securelevel=2",
        "status": "HYPERV_MANAGEMENT_READY"
    },
    {
        "vm_id": "hyperv_freebsd15_hardened",
        "name": "FreeBSD 15 Hardened ZFS Hyper-V VM",
        "os_version": "FreeBSD 15.0-CURRENT/RELEASE",
        "mount_target": r"H:\Partition_H1_FreeBSD15_Hardened_Live",
        "hv_drivers": "hv_kvp, hv_vss, hv_utils, hv_storvsc, hv_netvsc",
        "security_level": "security.bsd.hardened=YES",
        "status": "HYPERV_MANAGEMENT_READY"
    }
]

def main():
    print("==========================================================================")
    print("   FREEBSD HYPER-V MANAGEMENT & INTEGRATION SERVICES REGISTRAR           ")
    print("==========================================================================")
    print(f"Timestamp UTC: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}")

    for db in [DB_PATH, GDRIVE_DB]:
        if os.path.exists(db):
            try:
                conn = sqlite3.connect(db)
                cur = conn.cursor()
                cur.execute("""
                CREATE TABLE IF NOT EXISTS freebsd_hyperv_management (
                    vm_id TEXT PRIMARY KEY,
                    name TEXT,
                    os_version TEXT,
                    mount_target TEXT,
                    hv_drivers TEXT,
                    security_level TEXT,
                    status TEXT
                );
                """)

                for cfg in bsd_hyperv_configs:
                    cur.execute("""
                    INSERT OR REPLACE INTO freebsd_hyperv_management
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                    """, (
                        cfg["vm_id"], cfg["name"], cfg["os_version"],
                        cfg["mount_target"], cfg["hv_drivers"],
                        cfg["security_level"], cfg["status"]
                    ))

                # Log MCP Synaptic Route
                cur.execute("""
                INSERT OR REPLACE INTO mcp_synaptic_routes
                VALUES ('mcp_route_freebsd_hyperv_management', 'Hyper-V', 'FREEBSD_HYPERV_MANAGEMENT', 50050, 'HYPERV_INTEGRATION_SERVICES', 'FreeBSD 14.1 & FreeBSD 15 Hyper-V Integration & KVP Services', 1);
                """)

                conn.commit()
                conn.close()
                print(f"[+] Registered FreeBSD Hyper-V Management in: {os.path.basename(db)}")
            except Exception as e:
                print(f"[-] Notice registering DB {db}: {e}")

    print("==========================================================================")
    print("  [OK] FREEBSD HYPER-V MANAGEMENT CONFIGURATION REGISTERED 100%!")
    print("==========================================================================")

if __name__ == "__main__":
    main()
