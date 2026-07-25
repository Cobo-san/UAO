#!/usr/bin/env python3
"""
SATA HDD Offline Recovery & Diagnostics Engine
Inspects physical disk devices on Windows and Linux (WSL2), detects offline SATA drives,
and provides step-by-step raw disk mounting and data recovery execution pipelines.
"""

import os
import sys
import json
import subprocess
import platform

def get_current_os():
    return platform.system()

def inspect_windows_disks():
    print("=== [1/2] WINDOWS PHYSICAL DISK INSPECTION ===")
    ps_command = "Get-CimInstance Win32_DiskDrive | Select-Object DeviceID, Caption, Model, InterfaceType, Size, Status, Partitions, PNPDeviceID | ConvertTo-Json"
    try:
        res = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True, check=True)
        disks = json.loads(res.stdout)
        if isinstance(disks, dict):
            disks = [disks]
        
        print(f"[+] Found {len(disks)} Physical Disk Devices on Host:")
        for d in disks:
            print(f"  * DeviceID    : {d.get('DeviceID')}")
            print(f"    Caption     : {d.get('Caption') or 'Unknown (Offline / Uninitialized SATA Drive)'}")
            print(f"    Interface   : {d.get('InterfaceType')}")
            print(f"    Size (Bytes): {d.get('Size')}")
            print(f"    Partitions  : {d.get('Partitions')}")
            print(f"    PNP ID      : {d.get('PNPDeviceID')}")
            print("-" * 60)
        return disks
    except Exception as e:
        print(f"[-] Error querying Windows disks: {e}")
        return []

def inspect_linux_wsl_disks():
    print("\n=== [2/2] LINUX (WSL2) BLOCK DEVICE INSPECTION ===")
    cmd = ["wsl", "-d", "AlmaLinux-10", "-u", "root", "--", "lsblk", "-o", "NAME,SIZE,FSTYPE,TYPE,MOUNTPOINTS,MODEL"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(res.stdout)
    except Exception as e:
        print(f"[-] Error querying WSL Linux block devices: {e}")

def print_recovery_roadmap():
    print("\n==========================================================================")
    print(" RECOMMENDED SATA HDD DATA RECOVERY WORKFLOW (LINUX / WSL2 METHOD)")
    print("==========================================================================")
    print("Step 1: Open PowerShell as Administrator on Windows and mount raw disk:")
    print("        wsl --mount \\\\.\\PHYSICALDRIVE0 --bare\n")
    print("Step 2: Inside AlmaLinux-10 or Ubuntu (WSL2), locate the attached drive:")
    print("        sudo lsblk\n")
    print("Step 3: Attempt Read-Only Mount (Safest for existing partitions):")
    print("        sudo mkdir -p /mnt/sata_recovery")
    print("        sudo mount -o ro /dev/sde1 /mnt/sata_recovery\n")
    print("Step 4: If File System / Partition Table is damaged, use TestDisk or ddrescue:")
    print("        sudo testdisk /dev/sde           # Restores partitions & boot sectors")
    print("        sudo photorec /dev/sde           # Carves raw files (photos, docs, code)")
    print("        sudo ddrescue /dev/sde /var/ai_storage_primary/sata_backup.img /var/ai_storage_primary/sata.log\n")

def main():
    print("=== SATA HDD DATA RECOVERY & DIAGNOSTIC ENGINE ===")
    inspect_windows_disks()
    inspect_linux_wsl_disks()
    print_recovery_roadmap()

if __name__ == "__main__":
    main()
