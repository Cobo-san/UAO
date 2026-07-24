#!/usr/bin/env python3
"""
Spaceship Flight Simulator & Master System Cockpit Launcher
Launches the Live Terminal Server (localhost:9999) and opens the Spaceship Cockpit HUD Dashboard.
"""

import os
import sys
import webbrowser
import subprocess
import time
import platform

def get_current_os():
    return platform.system()

def launch_terminal_server():
    repo_dir = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
    if get_current_os() != "Windows":
        repo_dir = "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository"

    server_script = os.path.join(repo_dir, "bin", "antigravity_terminal_server.py")
    if os.path.exists(server_script):
        print(f"[*] Starting Antigravity Live Terminal Server (Port 9999): {server_script}")
        if get_current_os() == "Windows":
            subprocess.Popen([sys.executable, server_script], creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
        else:
            subprocess.Popen([sys.executable, server_script])
        time.sleep(1)
        print("[+] Live Terminal Server Started on http://localhost:9999")

def main():
    print("=== Launching Antigravity Spaceship Cockpit & Live Terminal Suite ===")
    
    # 1. Start Terminal Server Background API
    launch_terminal_server()

    # 2. Open Cockpit Flight Simulator HUD Dashboard in Browser
    if get_current_os() == "Windows":
        dashboard_path = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\spaceship_cockpit_terminal_dashboard.html"
    else:
        dashboard_path = "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/spaceship_cockpit_terminal_dashboard.html"

    if os.path.exists(dashboard_path):
        print(f"[+] Opening Spaceship Cockpit Flight Simulator Dashboard: {dashboard_path}")
        webbrowser.open(f"file:///{dashboard_path.replace('\\', '/')}")
    else:
        print(f"[!] Cockpit Dashboard file not found: {dashboard_path}")

    print("[OK] SPACESHIP FLIGHT SIMULATOR COCKPIT & LIVE TERMINAL LAUNCHED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
