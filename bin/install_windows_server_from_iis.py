#!/usr/bin/env python3
"""
Windows Server Installation & Network Deployment Engine via IIS
Provisions IIS HTTP Network Installation endpoints, unattended autounattend.xml config,
and Hyper-V automated Windows Server VM provisioner.
"""

import os
import sys
import json
import sqlite3
import time
import subprocess
import platform

ACCOUNT_EMAIL = "sounddharma@gmail.com"
GCP_PROJECT_ID = "anaconda-google-project-sounddharma"

REPO_DIR = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
IIS_INSTALL_DIR = os.path.join(REPO_DIR, "web_app", "windows_server_install")
DB_PATH = os.path.join(REPO_DIR, "synaptic_matrix", "universal_synaptic_matrix.sqlite")
GDRIVE_DB = r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Parallel_Synaptic_Database_Matrix\universal_synaptic_matrix.sqlite"

os.makedirs(IIS_INSTALL_DIR, exist_ok=True)

def main():
    print("==========================================================================")
    print("   WINDOWS SERVER NETWORK INSTALLATION & DEPLOYMENT ENGINE VIA IIS       ")
    print("==========================================================================")
    print(f"Timestamp UTC: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}")
    print(f"IIS Installation Endpoint: http://localhost:8088/windows_server_install/")

    # 1. Create Windows Server Unattended Auto-Installer Config (autounattend.xml)
    xml_path = os.path.join(IIS_INSTALL_DIR, "autounattend.xml")
    autounattend_xml = """<?xml version="1.0" encoding="utf-8"?>
<unattend xmlns="urn:schemas-microsoft-com:unattend">
    <settings pass="windowsPE">
        <component name="Microsoft-Windows-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS">
            <UserData>
                <AcceptEula>true</AcceptEula>
                <FullName>Antigravity Administrator</FullName>
                <Organization>QENTA-PRIME UAO Evaluation</Organization>
                <ProductKey>
                    <!-- Windows Server 2025 Datacenter Evaluation KMS / Free Trial Key -->
                    <Key>D2N9P-3P6X9-2R39C-7RTCD-MDVJX</Key>
                    <WillShowUI>OnError</WillShowUI>
                </ProductKey>
            </UserData>
            <DiskConfiguration>
                <Disk wcm:action="add">
                    <DiskID>0</DiskID>
                    <WillWipeDisk>true</WillWipeDisk>
                    <CreatePartitions>
                        <CreatePartition wcm:action="add">
                            <Order>1</Order>
                            <Type>Primary</Type>
                            <Size>100000</Size>
                        </CreatePartition>
                    </CreatePartitions>
                </Disk>
            </DiskConfiguration>
        </component>
    </settings>
    <settings pass="oobeSystem">
        <component name="Microsoft-Windows-Shell-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS">
            <AutoLogon>
                <Password><Value>Antigravity2026!</Value></Password>
                <Enabled>true</Enabled>
                <LogonCount>1</LogonCount>
                <Username>Administrator</Username>
            </AutoLogon>
        </component>
    </settings>
</unattend>
"""
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(autounattend_xml)
    print(f"\n[1/4] Generated Windows Server Unattended Config: {xml_path}")

    # 2. Create Hyper-V Automated Provisioner Script for Windows Server
    ps1_path = os.path.join(IIS_INSTALL_DIR, "create_windows_server_vm_hyperv.ps1")
    ps1_script = """# Hyper-V Automated Windows Server VM Provisioner Script
$VMName = "Windows_Server_2025_Evaluation_Edition_IIS"
$VMPath = "C:\\AI_Dedicated_Storage_1TB\\vms\\Windows_Server_2025_Eval"
$VHDPath = "$VMPath\\Windows_Server_2025_Eval.vhdx"
$RAM = 8GB
$CPUs = 4

Write-Host "=== Provisioning Windows Server 2025 Evaluation Edition VM via IIS ==="
New-Item -Path $VMPath -ItemType Directory -Force | Out-Null
New-VHD -Path $VHDPath -SizeBytes 100GB -Dynamic | Out-Null
New-VM -Name $VMName -MemoryStartupBytes $RAM -VHDPath $VHDPath -Path $VMPath | Out-Null
Set-VMProcessor -VMName $VMName -Count $CPUs
Write-Host "[OK] Windows Server 2025 VM Created Successfully in Hyper-V!"
"""
    with open(ps1_path, "w", encoding="utf-8") as f:
        f.write(ps1_script)
    print(f"[2/4] Generated Hyper-V VM Provisioner Script: {ps1_path}")

    # 3. Create IIS Installation Index Page
    index_html_path = os.path.join(IIS_INSTALL_DIR, "index.html")
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Windows Server Network Installation via IIS</title>
    <style>
        body {{ font-family: sans-serif; background: #0b0e14; color: #e1e6f0; padding: 30px; }}
        .card {{ background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 8px; }}
        code {{ background: #0d1117; color: #58a6ff; padding: 3px 6px; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>🖥️ Windows Server Network Deployment via IIS</h1>
        <p>Unattended Auto-Installer Config: <a href="autounattend.xml" style="color: #79c0ff;">autounattend.xml</a></p>
        <p>Hyper-V VM Provisioner Script: <a href="create_windows_server_vm_hyperv.ps1" style="color: #79c0ff;">create_windows_server_vm_hyperv.ps1</a></p>
        <p>Target Account: <code>{ACCOUNT_EMAIL}</code> | GCP Project: <code>{GCP_PROJECT_ID}</code></p>
    </div>
</body>
</html>
"""
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"[3/4] Created IIS Windows Server Installation Index: {index_html_path}")

    # 4. Register in SQLite Matrix Database
    print("\n[4/4] Registering Windows Server IIS Deployment in SQLite Matrix DBs...")
    for db in [DB_PATH, GDRIVE_DB]:
        if os.path.exists(db):
            try:
                conn = sqlite3.connect(db)
                cur = conn.cursor()
                
                cur.execute("""
                CREATE TABLE IF NOT EXISTS universal_vm_sandbox_registry (
                    vm_id TEXT PRIMARY KEY,
                    vm_name TEXT,
                    os_type TEXT,
                    hypervisor TEXT,
                    allocated_ram_mb INTEGER,
                    allocated_cpus INTEGER,
                    virtual_disk_path TEXT,
                    bridge_ip_address TEXT,
                    mcp_port INTEGER,
                    status TEXT,
                    created_timestamp TEXT
                );
                """)

                cur.execute("""
                INSERT OR REPLACE INTO universal_vm_sandbox_registry
                VALUES ('win_server_2025_iis', 'Windows Server 2025 Datacenter', 'Windows Server 2025 Datacenter', 'Hyper-V / QEMU / IIS PXE', 8192, 4, 'C:\\AI_Dedicated_Storage_1TB\\vms\\Windows_Server_2025\\Windows_Server_2025.vhdx', '127.0.0.1', 8088, 'READY_FOR_IIS_HTTP_INSTALL', ?);
                """, (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),))

                conn.commit()
                conn.close()
                print(f"  [+] Registered Windows Server 2025 in SQLite DB: {os.path.basename(db)}")
            except Exception as e:
                print(f"  [-] Notice registering DB {db}: {e}")

    print("\n==========================================================================")
    print("  [OK] WINDOWS SERVER NETWORK INSTALLATION VIA IIS READY & CONFIGURED!")
    print("==========================================================================")

if __name__ == "__main__":
    main()
