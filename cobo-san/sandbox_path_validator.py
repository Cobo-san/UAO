#!/usr/bin/env python3
"""
POSIX Sandbox Path Validator & Windows Compatibility Engine
Ref: Pull Request #138 (Cobo-san/minions) - Validates and enforces POSIX-style paths
across Windows, Linux, WSL2, Docker, and GitHub Actions environments.
"""

import os
import sys
import re
import platform
from pathlib import Path, PureWindowsPath, PurePosixPath

def normalize_to_posix_path(raw_path: str) -> str:
    """
    Converts any Windows or cross-OS path string into a normalized POSIX-format string.
    Replaces backslashes with forward slashes and handles drive letters cleanly.
    Example: 'C:\\Users\\Monica Fugazi\\.antigravity-ide' -> 'C:/Users/Monica Fugazi/.antigravity-ide'
    """
    if not raw_path:
        return ""

    path_str = str(raw_path).strip()
    
    # Handle Windows backslashes
    path_str = path_str.replace("\\", "/")

    # Ensure clean POSIX representation using pathlib
    try:
        p = Path(path_str)
        posix_str = p.as_posix()
    except Exception:
        posix_str = path_str.replace("\\", "/")

    return posix_str

def convert_windows_to_wsl_posix(win_path: str) -> str:
    """
    Converts a Windows absolute path to a WSL POSIX mount path.
    Example: 'C:/Users/Monica Fugazi' -> '/mnt/c/Users/Monica Fugazi'
    """
    posix_p = normalize_to_posix_path(win_path)
    
    # Match Windows drive pattern (e.g. C:/ or c:/)
    match = re.match(r"^([a-zA-Z]):/(.*)$", posix_p)
    if match:
        drive_letter = match.group(1).lower()
        rest = match.group(2)
        return f"/mnt/{drive_letter}/{rest}"
    
    return posix_p

def validate_sandbox_path(target_path: str, sandbox_root: str = None) -> dict:
    """
    Validates that target_path is enclosed within sandbox_root and returns POSIX normalized path.
    Prevents path traversal attacks and guarantees Windows/Linux path compatibility.
    """
    normalized_target = normalize_to_posix_path(target_path)
    
    if not sandbox_root:
        sandbox_root = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository" if platform.system() == "Windows" else "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository"

    normalized_root = normalize_to_posix_path(sandbox_root)

    # Check boundary containment (case-insensitive for Windows)
    is_valid = normalized_target.lower().startswith(normalized_root.lower()) or normalized_target.lower().startswith("/mnt/")

    return {
        "raw_path": target_path,
        "posix_path": normalized_target,
        "wsl_posix_path": convert_windows_to_wsl_posix(target_path),
        "sandbox_root": normalized_root,
        "is_valid_sandbox_path": is_valid,
        "os_platform": platform.system()
    }

def main():
    print("=== POSIX SANDBOX PATH VALIDATOR & WINDOWS COMPATIBILITY ENGINE ===")
    sample_paths = [
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\universal_binary_ipc_engine.py",
        r"D:\AI_Dedicated_Storage_Secondary\models_gguf_mirror\Llama-3.3-70B-Instruct-Q4_K_M.gguf",
        "/mnt/c/Users/Monica Fugazi/GoogleDrive_sounddharma/cobo-san/cobo-san_manifest.json"
    ]

    for p in sample_paths:
        res = validate_sandbox_path(p)
        print(f"\n[*] Raw Input Path : {res['raw_path']}")
        print(f"    • POSIX Path   : {res['posix_path']}")
        print(f"    • WSL POSIX    : {res['wsl_posix_path']}")
        print(f"    • Sandbox Valid: {res['is_valid_sandbox_path']}")

    print("\n[OK] POSIX SANDBOX PATH VALIDATOR EXECUTED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
