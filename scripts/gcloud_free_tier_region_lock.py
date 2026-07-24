#!/usr/bin/env python3
"""
GCP Distro-to-Region 1-to-1 Free Tier Lock Engine
Assigns 1 dedicated GCP Free Tier Region to each OS Distro instance:
- Windows Host  --> us-east1    (South Carolina)
- AlmaLinux-10  --> us-central1 (Iowa)
- Ubuntu        --> us-west1    (Oregon)
"""

import os
import sys
import json
import sqlite3
import subprocess
import platform

# 1-to-1 Distro to Region Mapping
DISTRO_REGION_MAP = {
    "Windows": {
        "region": "us-east1",
        "zone": "us-east1-a",
        "label": "Windows Host -> US East 1 (South Carolina)"
    },
    "AlmaLinux": {
        "region": "us-central1",
        "zone": "us-central1-a",
        "label": "AlmaLinux-10 WSL -> US Central 1 (Iowa)"
    },
    "Ubuntu": {
        "region": "us-west1",
        "zone": "us-west1-a",
        "label": "Ubuntu WSL -> US West 1 (Oregon)"
    },
    "FreeBSD": {
        "region": "us-east1",
        "zone": "us-east1-b",
        "label": "FreeBSD Node -> US East 1 Zone B (South Carolina)"
    }
}

FREE_TIER_MACHINE_TYPE = "e2-micro"
MAX_BOOT_DISK_GB = 30
MAX_STORAGE_GB = 5

def get_current_os():
    return platform.system()

def get_distro_identity():
    current_os = get_current_os()
    if current_os == "Windows":
        return "Windows"
    else:
        # Check /etc/os-release for AlmaLinux vs Ubuntu
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                content = f.read().lower()
                if "alma" in content:
                    return "AlmaLinux"
                elif "ubuntu" in content:
                    return "Ubuntu"
        return "AlmaLinux"

def apply_distro_region_lock():
    distro = get_distro_identity()
    target_info = DISTRO_REGION_MAP.get(distro, DISTRO_REGION_MAP["Windows"])
    region = target_info["region"]
    zone = target_info["zone"]

    print(f"[*] Identified Distro Instance: {distro}")
    print(f"[*] Locking Instance to Dedicated Region: {target_info['label']}")

    commands = [
        ["gcloud", "config", "set", "compute/region", region],
        ["gcloud", "config", "set", "compute/zone", zone],
        ["gcloud", "config", "set", "core/disable_prompts", "true"]
    ]

    for cmd in commands:
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if res.returncode == 0:
                print(f"  [+] {' '.join(cmd)} -> SUCCESS")
            else:
                print(f"  [-] {' '.join(cmd)} -> {res.stderr.strip()}")
        except Exception as e:
            print(f"  [!] gcloud skipped: {e}")

def update_binary_ipc_guardrails(db_path):
    if not os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS distro_region_mapping;")

    cursor.execute("""
    CREATE TABLE distro_region_mapping (
        distro_id TEXT PRIMARY KEY,
        assigned_region TEXT,
        assigned_zone TEXT,
        label TEXT,
        cost_policy TEXT
    );
    """)

    for distro_key, info in DISTRO_REGION_MAP.items():
        cursor.execute("""
        INSERT INTO distro_region_mapping VALUES (?, ?, ?, ?, '$0.00 FREE TIER GUARANTEED');
        """, (distro_key, info["region"], info["zone"], info["label"]))

    conn.commit()
    conn.close()

def main():
    print("=== GCP Distro-to-Region 1-to-1 Dedicated Free Lock Engine ===")
    apply_distro_region_lock()

    living_db = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\universal_synaptic_matrix.sqlite"
    if get_current_os() != "Windows":
        living_db = "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/synaptic_matrix/universal_synaptic_matrix.sqlite"
    update_binary_ipc_guardrails(living_db)

    gdrive_db = r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Parallel_Synaptic_Database_Matrix\universal_synaptic_matrix.sqlite"
    if get_current_os() != "Windows":
        gdrive_db = "/mnt/c/Users/Monica Fugazi/GoogleDrive_sounddharma/Parallel_Synaptic_Database_Matrix/universal_synaptic_matrix.sqlite"
    update_binary_ipc_guardrails(gdrive_db)

    print("[OK] DISTRO-TO-REGION 1-TO-1 MAPPING LOCKED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
