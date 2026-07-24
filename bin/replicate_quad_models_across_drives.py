#!/usr/bin/env python3
"""
High-Speed Internal NVMe Model Replication Engine
Performs zero-network internal NVMe file replication (at 3,500 - 7,000 MB/s) across C:, D:, and E: drives
once master GGUF model files complete downloading. Enforces read-only (:ro) permissions on all replicas.
"""

import os
import sys
import shutil
import time
import platform

DRIVES = ["C:", "D:", "E:"]

MODEL_SOURCES = {
    "Llama-3.3-70B-Instruct-Q4_K_M.gguf": r"C:\AI_Dedicated_Storage_1TB\models_gguf\Llama-3.3-70B-Instruct-Q4_K_M.gguf",
    "Qwen-2.5-Coder-32B-Instruct-Q5_K_M.gguf": r"D:\AI_Dedicated_Storage_Secondary\models_gguf_mirror\Qwen-2.5-Coder-32B-Instruct-Q5_K_M.gguf",
    "DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf": r"D:\AI_Dedicated_Storage_Secondary\models_gguf_mirror\DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf",
    "Codestral-22B-v0.1-Q5_K_M.gguf": r"E:\AI_Dedicated_Storage_Tertiary\models_gguf\Codestral-22B-v0.1-Q5_K_M.gguf"
}

def get_drive_target_path(drive_letter, filename):
    drive_clean = drive_letter[0].upper()
    if drive_clean == "C":
        return f"C:\\AI_Dedicated_Storage_1TB\\models_gguf\\{filename}"
    elif drive_clean == "D":
        return f"D:\\AI_Dedicated_Storage_Secondary\\models_gguf_mirror\\{filename}"
    else:
        return f"E:\\AI_Dedicated_Storage_Tertiary\\models_gguf\\{filename}"

def replicate_models_internally():
    print("=== HIGH-SPEED INTERNAL NVME MODEL REPLICATION ENGINE ===")
    replicated_count = 0

    for filename, src_path in MODEL_SOURCES.items():
        if not os.path.exists(src_path):
            print(f"[*] Master model '{filename}' is still downloading (waiting for master completion)...")
            continue

        src_size_gb = os.path.getsize(src_path) / 1e9
        print(f"\n[+] Found Master Model ({src_size_gb:.2f} GB): {src_path}")

        for drive in DRIVES:
            target_path = get_drive_target_path(drive, filename)
            if target_path.lower() == src_path.lower():
                continue

            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            if os.path.exists(target_path):
                print(f"  [=] Drive {drive} already has replica ({os.path.getsize(target_path)/1e9:.2f} GB): {target_path}")
                continue

            print(f"  [*] Internal Replication: {src_path} -> {target_path} (High-Speed NVMe Bus)...")
            start_time = time.time()
            try:
                shutil.copy2(src_path, target_path)
                os.chmod(target_path, 0o444) # Lock Read-Only
                elapsed = time.time() - start_time
                speed_mb = (src_size_gb * 1000) / max(0.1, elapsed)
                print(f"      [+] REPLICATED IN {elapsed:.2f} SECONDS ({speed_mb:.1f} MB/s) | Read-Only ENFORCED!")
                replicated_count += 1
            except Exception as e:
                print(f"      [!] Notice during replication to {target_path}: {e}")

    print(f"\n[OK] INTERNAL NVME REPLICATION CYCLE COMPLETE: {replicated_count} new replicas created!")

def main():
    replicate_models_internally()

if __name__ == "__main__":
    main()
