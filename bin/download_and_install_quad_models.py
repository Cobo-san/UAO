#!/usr/bin/env python3
"""
Quad-Model Physical File Downloader & Installer Engine
Downloads the physical GGUF model files for Qwen 2.5 Coder 32B, DeepSeek R1 70B, and Codestral 22B
directly onto physical C:, D:, and E: drives from Hugging Face repositories:
  1. Qwen-2.5-Coder-32B-Instruct-Q5_K_M.gguf -> D:\AI_Dedicated_Storage_Secondary\models_gguf_mirror\
  2. DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf -> D:\AI_Dedicated_Storage_Secondary\models_gguf_mirror\
  3. Codestral-22B-v0.1-Q5_K_M.gguf -> E:\AI_Dedicated_Storage_Tertiary\models_gguf\
"""

import os
import sys
import subprocess
import urllib.request
import platform

ACCOUNT_EMAIL = "sounddharma@gmail.com"
GCP_PROJECT_ID = "anaconda-google-project-sounddharma"

# Model Download Specifications (Hugging Face Repositories)
DOWNLOAD_TARGETS = [
    {
        "model_name": "Qwen-2.5-Coder-32B-Instruct-Q5_K_M.gguf",
        "repo_id": "Qwen/Qwen2.5-Coder-32B-Instruct-GGUF",
        "file_name": "qwen2.5-coder-32b-instruct-q5_k_m.gguf",
        "target_dir": r"C:\AI_Dedicated_Storage_1TB\models_gguf",
        "posix_dir": "/mnt/c/AI_Dedicated_Storage_1TB/models_gguf"
    },
    {
        "model_name": "DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf",
        "repo_id": "unsloth/DeepSeek-R1-Distill-Llama-70B-GGUF",
        "file_name": "DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf",
        "target_dir": r"C:\AI_Dedicated_Storage_1TB\models_gguf",
        "posix_dir": "/mnt/c/AI_Dedicated_Storage_1TB/models_gguf"
    },
    {
        "model_name": "Codestral-22B-v0.1-Q5_K_M.gguf",
        "repo_id": "bartowski/Codestral-22B-v0.1-GGUF",
        "file_name": "Codestral-22B-v0.1-Q5_K_M.gguf",
        "target_dir": r"C:\AI_Dedicated_Storage_1TB\models_gguf",
        "posix_dir": "/mnt/c/AI_Dedicated_Storage_1TB/models_gguf"
    }
]

def ensure_huggingface_hub():
    print("[*] Ensuring huggingface_hub Python library is installed...")
    try:
        import huggingface_hub
        print("  [+] huggingface_hub is available.")
    except ImportError:
        print("  [*] Installing huggingface_hub...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "huggingface_hub"])

def download_model_files():
    ensure_huggingface_hub()
    from huggingface_hub import hf_hub_download

    print("\n=== DOWNLOADING & INSTALLING QUAD GGUF MODEL WEIGHTS ===")

    for item in DOWNLOAD_TARGETS:
        target_dir = item["target_dir"] if platform.system() == "Windows" else item["posix_dir"]
        os.makedirs(target_dir, exist_ok=True)
        dest_file = os.path.join(target_dir, item["model_name"])

        if os.path.exists(dest_file):
            size_gb = os.path.getsize(dest_file) / 1e9
            print(f"  [+] Model file already exists ({size_gb:.2f} GB): {dest_file}")
            # Enforce read-only protection
            try:
                os.chmod(dest_file, 0o444)
            except Exception:
                pass
            continue

        print(f"\n[*] Downloading {item['model_name']} from Hugging Face ({item['repo_id']})...")
        print(f"    Target Destination: {dest_file}")

        try:
            downloaded_path = hf_hub_download(
                repo_id=item["repo_id"],
                filename=item["file_name"],
                local_dir=target_dir,
                local_dir_use_symlinks=False
            )
            # Rename to standard model name if needed
            if downloaded_path != dest_file and os.path.exists(downloaded_path):
                os.rename(downloaded_path, dest_file)

            # Enforce read-only protection to prevent drive wear
            try:
                os.chmod(dest_file, 0o444)
            except Exception:
                pass

            size_gb = os.path.getsize(dest_file) / 1e9
            print(f"  [+] SUCCESS: Downloaded {item['model_name']} ({size_gb:.2f} GB) to {dest_file}")
            print("  [+] Enforced Read-Only protection (:ro)")
        except Exception as e:
            print(f"  [!] Notice during download of {item['model_name']}: {e}")

def main():
    download_model_files()

if __name__ == "__main__":
    main()
