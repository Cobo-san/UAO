#!/usr/bin/env python3
"""
System-Wide Read-Only Lock Enforcement Engine
Applies strict Read-Only (:ro) permissions (chmod 444 / attrib +r) across all
models, databases, source scripts, manifests, snapshots, and repositories.
"""

import os
import sys
import platform
import subprocess

def enforce_readonly_lock():
    print("==========================================================================")
    print("      ENFORCING SYSTEM-WIDE READ-ONLY (:RO) LOCK UNTIL FURTHER NOTICE      ")
    print("==========================================================================")

    repo_dir = os.path.dirname(os.path.dirname(__file__))
    drives = ["C:", "D:", "E:"]

    # 1. Lock All GGUF Model Weight Files
    print("\n--- 1. Locking All Physical GGUF Model Files Across C:, D:, E: Drives ---")
    models = [
        "Llama-3.3-70B-Instruct-Q4_K_M.gguf",
        "Qwen-2.5-Coder-32B-Instruct-Q5_K_M.gguf",
        "DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf",
        "Codestral-22B-v0.1-Q5_K_M.gguf"
    ]
    for d in drives:
        base_dir = f"{d}\\AI_Dedicated_Storage_1TB\\models_gguf" if d == "C:" else (f"{d}\\AI_Dedicated_Storage_Secondary\\models_gguf_mirror" if d == "D:" else f"{d}\\AI_Dedicated_Storage_Tertiary\\models_gguf")
        if platform.system() != "Windows":
            base_dir = f"/mnt/{d[0].lower()}/AI_Dedicated_Storage_1TB/models_gguf" if d == "C:" else (f"/mnt/{d[0].lower()}/AI_Dedicated_Storage_Secondary/models_gguf_mirror" if d == "D:" else f"/mnt/{d[0].lower()}/AI_Dedicated_Storage_Tertiary/models_gguf")

        for m in models:
            p = os.path.join(base_dir, m)
            if os.path.exists(p):
                try:
                    os.chmod(p, 0o444)
                    print(f"  [LOCKED :RO] [{d}] {m} -> Read-Only (chmod 444)")
                except Exception as e:
                    print(f"  [!] Notice locking {p}: {e}")

    # 2. Lock All Golden Packages & Manifests
    print("\n--- 2. Locking Golden Master Packages & Manifests ---")
    cobo_dir = os.path.join(repo_dir, "cobo-san")
    if os.path.exists(cobo_dir):
        for root, dirs, files in os.walk(cobo_dir):
            for file in files:
                p = os.path.join(root, file)
                try:
                    os.chmod(p, 0o444)
                    print(f"  [LOCKED :RO] {file} -> Read-Only (chmod 444)")
                except Exception as e:
                    pass

    # 3. Lock All Golden Snapshots
    print("\n--- 3. Locking All Golden Memory Snapshots ---")
    snap_dir = os.path.join(repo_dir, "golden_snapshots")
    if os.path.exists(snap_dir):
        for root, dirs, files in os.walk(snap_dir):
            for file in files:
                p = os.path.join(root, file)
                try:
                    os.chmod(p, 0o444)
                except Exception as e:
                    pass
        print(f"  [LOCKED :RO] All memory snapshots in {snap_dir} locked in Read-Only mode!")

    # 4. Lock Primary SQLite Databases
    print("\n--- 4. Locking SQLite WAL Databases ---")
    db_paths = [
        os.path.join(repo_dir, "synaptic_matrix", "universal_synaptic_matrix.sqlite"),
        r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Parallel_Synaptic_Database_Matrix\universal_synaptic_matrix.sqlite"
    ]
    for db in db_paths:
        if os.path.exists(db):
            try:
                os.chmod(db, 0o444)
                print(f"  [LOCKED :RO] Database: {db} -> Read-Only (chmod 444)")
            except Exception as e:
                pass

    print("\n==========================================================================")
    print("  [OK] SYSTEM-WIDE READ-ONLY (:RO) LOCK ENFORCED UNTIL FURTHER NOTICE!   ")
    print("==========================================================================")

if __name__ == "__main__":
    enforce_readonly_lock()
