#!/usr/bin/env python3
"""
GitHub Repository Initialization & Push Helper Engine
Helper script to initialize Git, generate .gitignore (excluding large .gguf weights),
commit all Cobo-San Golden Build artifacts, and push to GitHub (sounddharma).
"""

import os
import sys
import subprocess
import platform

ACCOUNT_EMAIL = "sounddharma@gmail.com"
GITHUB_USERNAME = "sounddharma"
REPO_NAME = "cobo-san-master-build"

def get_current_os():
    return platform.system()

def generate_gitignore(repo_dir):
    gitignore_path = os.path.join(repo_dir, ".gitignore")
    content = """# Cobo-San Git Ignore File
*.gguf
*.iso
*.vhd
*.vhdx
*.qcow2
*.sqlite-wal
*.sqlite-shm
__pycache__/
*.pyc
.tmp.driveupload/
"""
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Generated .gitignore at {gitignore_path}")

def print_github_instructions():
    print("\n==========================================================================")
    print("  GITHUB REPOSITORY INTEGRATION INSTRUCTIONS")
    print("==========================================================================")
    print(f"Target Account : {ACCOUNT_EMAIL} ({GITHUB_USERNAME})")
    print(f"Target Repo Name: {REPO_NAME}")
    print("\nTo push this codebase to GitHub, run the following commands in Terminal/WSL2:")
    print("--------------------------------------------------------------------------")
    print("1. git init")
    print("2. git add .")
    print('3. git commit -m "Initial commit of Cobo-San Master Golden Build"')
    print(f"4. git remote add origin https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git")
    print("5. git branch -M main")
    print("6. git push -u origin main")
    print("--------------------------------------------------------------------------\n")

def main():
    print("=== GITHUB REPOSITORY CHECK & HELPER ENGINE ===")
    repo_dir = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
    if get_current_os() != "Windows":
        repo_dir = "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository"

    generate_gitignore(repo_dir)
    print_github_instructions()

if __name__ == "__main__":
    main()
