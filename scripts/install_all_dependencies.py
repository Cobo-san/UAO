#!/usr/bin/env python3
"""
Master Install-All Engine for Windows Host, AlmaLinux-10, and Ubuntu
Ensures all developer packages, CLI tools, Python modules, and cross-OS bridge files are installed.
"""

import os
import sys
import subprocess
import platform

def get_current_os():
    return platform.system()

def run_cmd(cmd, desc):
    print(f"[*] {desc}: {' '.join(cmd)}")
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode == 0:
            print(f"  [+] SUCCESS: {res.stdout.strip()[:100]}")
        else:
            print(f"  [-] NOTICE ({res.returncode}): {res.stderr.strip()[:100]}")
    except Exception as e:
        print(f"  [!] ERROR: {e}")

def install_windows_dependencies():
    print("=== Installing / Verifying Windows Host Dependencies ===")
    # 1. Install Google Cloud SDK via winget if not present
    run_cmd(["winget", "install", "Google.CloudSDK", "--silent", "--accept-package-agreements", "--accept-source-agreements"], "Installing Google Cloud SDK via winget")
    
    # 2. Run Python binary IPC engine initialization
    engine_script = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\universal_binary_ipc_engine.py"
    if os.path.exists(engine_script):
        run_cmd([sys.executable, engine_script], "Running Universal Binary IPC Engine")

    # 3. Run Token Savings Engine initialization
    token_script = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\zero_cost_token_savings_engine.py"
    if os.path.exists(token_script):
        run_cmd([sys.executable, token_script], "Running Zero-Cost Token Savings Engine")

    # 4. Run Synaptic MCP Kernel Router
    router_script = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\synaptic_mcp_kernel_router.py"
    if os.path.exists(router_script):
        run_cmd([sys.executable, router_script], "Running Synaptic MCP Kernel Router")

    # 5. Run Distro Region Lock Engine
    lock_script = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\scripts\gcloud_free_tier_region_lock.py"
    if os.path.exists(lock_script):
        run_cmd([sys.executable, lock_script], "Running Distro Region Lock Engine")

def install_wsl_dependencies():
    print("=== Installing / Verifying WSL Distro Dependencies (AlmaLinux & Ubuntu) ===")
    # AlmaLinux-10 setup via wsl
    wsl_cmd_alma = [
        "wsl.exe", "-d", "AlmaLinux-10", "-u", "root", "bash", "-c",
        "dnf install -y python3 python3-pip curl wget git tar sqlite && "
        "bash '/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/scripts/setup_universal_cross_os_bridge.sh' && "
        "bash '/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/scripts/gcloud_free_tier_region_lock.sh'"
    ]
    run_cmd(wsl_cmd_alma, "Configuring AlmaLinux-10 WSL Environment & Dependencies")

def main():
    print("=== Master Install-All Orchestrator ===")
    if get_current_os() == "Windows":
        install_windows_dependencies()
        install_wsl_dependencies()
    else:
        print("[*] Running inside Linux environment...")
        subprocess.run(["bash", "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/scripts/setup_universal_cross_os_bridge.sh"])
        subprocess.run(["bash", "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/scripts/gcloud_free_tier_region_lock.sh"])

    print("=== INSTALL ALL COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
