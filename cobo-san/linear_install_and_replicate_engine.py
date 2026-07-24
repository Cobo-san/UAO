#!/usr/bin/env python3
"""
Linear Install-to-C & High-Speed NVMe Sequential Replication Engine
Executes a strict linear 3-Phase Installation & Replication sequence:
  Phase 1: Download & Install all master models exclusively to C: Primary Hub (7,000 MB/s NVMe).
  Phase 2: Perform linear internal PCIe replication C: -> D: Drive (Secondary NVMe @ 3,500 MB/s).
  Phase 3: Perform linear internal PCIe replication C: -> E: Drive (Tertiary Bus @ 1,400 MB/s).
Applies automatic Read-Only (:ro @ chmod 444) permissions on every replicated model file.
"""

import os
import sys
import shutil
import time
import platform
import subprocess

ACCOUNT_EMAIL = "sounddharma@gmail.com"
GCP_PROJECT_ID = "anaconda-google-project-sounddharma"

# Primary C: Drive Master Models List
PRIMARY_C_MODELS = [
    {
        "name": "Llama-3.3-70B-Instruct-Q4_K_M.gguf",
        "c_path": r"C:\AI_Dedicated_Storage_1TB\models_gguf\Llama-3.3-70B-Instruct-Q4_K_M.gguf",
        "d_path": r"D:\AI_Dedicated_Storage_Secondary\models_gguf_mirror\Llama-3.3-70B-Instruct-Q4_K_M.gguf",
        "e_path": r"E:\AI_Dedicated_Storage_Tertiary\models_gguf\Llama-3.3-70B-Instruct-Q4_K_M.gguf"
    },
    {
        "name": "Qwen-2.5-Coder-32B-Instruct-Q5_K_M.gguf",
        "c_path": r"C:\AI_Dedicated_Storage_1TB\models_gguf\Qwen-2.5-Coder-32B-Instruct-Q5_K_M.gguf",
        "d_path": r"D:\AI_Dedicated_Storage_Secondary\models_gguf_mirror\Qwen-2.5-Coder-32B-Instruct-Q5_K_M.gguf",
        "e_path": r"E:\AI_Dedicated_Storage_Tertiary\models_gguf\Qwen-2.5-Coder-32B-Instruct-Q5_K_M.gguf"
    },
    {
        "name": "DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf",
        "c_path": r"C:\AI_Dedicated_Storage_1TB\models_gguf\DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf",
        "d_path": r"D:\AI_Dedicated_Storage_Secondary\models_gguf_mirror\DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf",
        "e_path": r"E:\AI_Dedicated_Storage_Tertiary\models_gguf\DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf"
    },
    {
        "name": "Codestral-22B-v0.1-Q5_K_M.gguf",
        "c_path": r"C:\AI_Dedicated_Storage_1TB\models_gguf\Codestral-22B-v0.1-Q5_K_M.gguf",
        "d_path": r"D:\AI_Dedicated_Storage_Secondary\models_gguf_mirror\Codestral-22B-v0.1-Q5_K_M.gguf",
        "e_path": r"E:\AI_Dedicated_Storage_Tertiary\models_gguf\Codestral-22B-v0.1-Q5_K_M.gguf"
    }
]

def phase_1_install_to_c():
    print("==========================================================================")
    print("  PHASE 1: LINEAR INSTALLATION TO PRIMARY C: NVME DRIVE HUB (7,000 MB/S)  ")
    print("==========================================================================")
    
    c_hub_dir = r"C:\AI_Dedicated_Storage_1TB\models_gguf"
    os.makedirs(c_hub_dir, exist_ok=True)

    for item in PRIMARY_C_MODELS:
        filename = item["name"]
        c_path = item["c_path"]
        
        if os.path.exists(c_path):
            size_gb = os.path.getsize(c_path) / 1e9
            print(f"  [+] Master Model Verified on C: Drive ({size_gb:.2f} GB): {c_path}")
            try:
                os.chmod(c_path, 0o444)
            except Exception:
                pass
        else:
            print(f"  [*] Master Model '{filename}' not on C: drive. Launching single HF download...")
            # Trigger download script
            down_script = os.path.join(os.path.dirname(__file__), "download_and_install_quad_models.py")
            subprocess.check_call([sys.executable, down_script])

def phase_2_replicate_c_to_d():
    print("\n==========================================================================")
    print("  PHASE 2: LINEAR INTERNAL PCIe REPLICATION (C: NVMe -> D: NVMe)        ")
    print("==========================================================================")

    for item in PRIMARY_C_MODELS:
        filename = item["name"]
        c_path = item["c_path"]
        d_path = item["d_path"]

        if not os.path.exists(c_path):
            print(f"  [-] Skipping C: -> D: for '{filename}' (Master on C: not ready)")
            continue

        os.makedirs(os.path.dirname(d_path), exist_ok=True)
        if os.path.exists(d_path):
            size_gb = os.path.getsize(d_path) / 1e9
            print(f"  [=] D: Drive Replica Already Present ({size_gb:.2f} GB): {d_path}")
            try:
                os.chmod(d_path, 0o444)
            except Exception:
                pass
            continue

        size_gb = os.path.getsize(c_path) / 1e9
        print(f"  [*] Linear PCIe Copy: C: -> D: ({size_gb:.2f} GB)...")
        t0 = time.time()
        shutil.copy2(c_path, d_path)
        os.chmod(d_path, 0o444)
        elapsed = time.time() - t0
        speed_mb = (size_gb * 1000) / max(0.1, elapsed)
        print(f"      [+] REPLICATED C: -> D: IN {elapsed:.2f} SECONDS ({speed_mb:.1f} MB/s) | Read-Only (:ro) Enforced!")

def phase_3_replicate_c_to_e():
    print("\n==========================================================================")
    print("  PHASE 3: LINEAR INTERNAL PCIe REPLICATION (C: NVMe -> E: Storage Bus)  ")
    print("==========================================================================")

    for item in PRIMARY_C_MODELS:
        filename = item["name"]
        c_path = item["c_path"]
        e_path = item["e_path"]

        if not os.path.exists(c_path):
            print(f"  [-] Skipping C: -> E: for '{filename}' (Master on C: not ready)")
            continue

        os.makedirs(os.path.dirname(e_path), exist_ok=True)
        if os.path.exists(e_path):
            size_gb = os.path.getsize(e_path) / 1e9
            print(f"  [=] E: Drive Replica Already Present ({size_gb:.2f} GB): {e_path}")
            try:
                os.chmod(e_path, 0o444)
            except Exception:
                pass
            continue

        size_gb = os.path.getsize(c_path) / 1e9
        print(f"  [*] Linear PCIe Copy: C: -> E: ({size_gb:.2f} GB)...")
        t0 = time.time()
        shutil.copy2(c_path, e_path)
        os.chmod(e_path, 0o444)
        elapsed = time.time() - t0
        speed_mb = (size_gb * 1000) / max(0.1, elapsed)
        print(f"      [+] REPLICATED C: -> E: IN {elapsed:.2f} SECONDS ({speed_mb:.1f} MB/s) | Read-Only (:ro) Enforced!")

def main():
    phase_1_install_to_c()
    phase_2_replicate_c_to_d()
    phase_3_replicate_c_to_e()
    print("\n[OK] STRICT LINEAR INSTALLATION & PCIe REPLICATION SEQUENCE COMPLETE!")

if __name__ == "__main__":
    main()
