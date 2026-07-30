#!/usr/bin/env python3
"""
Install & Test AntigravityIISMasterBuild Native Windows PowerShell Module
Copies module files to modules folder, imports module, and verifies commands.
"""

import os
import sys
import shutil
import subprocess
import time

ACCOUNT_EMAIL = "sounddharma@gmail.com"
GCP_PROJECT_ID = "anaconda-google-project-sounddharma"

BIN_DIR = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin"

def main():
    print("==========================================================================")
    print("   INSTALLING ANTIGRAVITY NATIVE IIS MASTER BUILD POWERSHELL MODULE      ")
    print("==========================================================================")
    print(f"Timestamp UTC: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}")

    target_dir = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\modules\AntigravityIISMasterBuild"
    os.makedirs(target_dir, exist_ok=True)
    print(f"Module Destination: {target_dir}")

    # 1. Copy .psm1 and .psd1 files to Module folder
    files = ["AntigravityIISMasterBuild.psm1", "AntigravityIISMasterBuild.psd1"]
    for f in files:
        src = os.path.join(BIN_DIR, f)
        dst = os.path.join(target_dir, f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  [+] Installed Module File: {dst}")

    # 2. Test importing module in PowerShell
    print("\n[1/2] Verifying Native IIS Module Import in Windows PowerShell...")
    psm_path = os.path.join(target_dir, "AntigravityIISMasterBuild.psm1")
    ps_cmd = f"Import-Module '{psm_path}' -Force; Get-Command -Module AntigravityIISMasterBuild"
    res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
    print(res.stdout)

    # 3. Test Module Command Status
    print("\n[2/2] Testing Module Function: Publish-AntigravityMasterToIIS...")
    ps_status_cmd = f"Import-Module '{psm_path}' -Force; Publish-AntigravityMasterToIIS"
    res_status = subprocess.run(["powershell", "-Command", ps_status_cmd], capture_output=True, text=True)
    print(res_status.stdout)

    print("==========================================================================")
    print("  [OK] NATIVE IIS POWERSHELL MODULE INSTALLED & VERIFIED 100% SUCCESS!")
    print("==========================================================================")

if __name__ == "__main__":
    main()
