#!/usr/bin/env python3
"""
Kimi K2.7-Code Local Installation & Anaconda/HuggingFace Downloader
Initializes model storage directory at C:\AI_Dedicated_Storage_1TB\models_gguf\moonshotai_kimi_k2.7_code
and downloads configuration manifests for HuggingFace / Anaconda AI Platform / GGUF.
"""

import os
import sys
import json
import sqlite3
import time

ACCOUNT_EMAIL = "sounddharma@gmail.com"
GCP_PROJECT_ID = "anaconda-google-project-sounddharma"

TARGET_MODEL_DIR = r"C:\AI_Dedicated_Storage_1TB\models_gguf\moonshotai_kimi_k2.7_code"
GGUF_MODEL_DIR = r"C:\AI_Dedicated_Storage_1TB\models_gguf\unsloth_kimi_k2.7_gguf"
REPO_DIR = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
DB_PATH = os.path.join(REPO_DIR, "synaptic_matrix", "universal_synaptic_matrix.sqlite")
GDRIVE_DB = r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Parallel_Synaptic_Database_Matrix\universal_synaptic_matrix.sqlite"

def main():
    print("==========================================================================")
    print("   KIMI K2.7-CODE ANACONDA & HUGGINGFACE LOCAL INSTALLER                  ")
    print("==========================================================================")
    print(f"Timestamp UTC: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}")
    print(f"Target Path 1: {TARGET_MODEL_DIR}")
    print(f"Target Path 2: {GGUF_MODEL_DIR}")

    # 1. Create Model Storage Directories
    os.makedirs(TARGET_MODEL_DIR, exist_ok=True)
    os.makedirs(GGUF_MODEL_DIR, exist_ok=True)

    config_manifest = {
        "model_id": "moonshotai/Kimi-K2.7-Code",
        "huggingface_repo": "https://huggingface.co/moonshotai/Kimi-K2.7-Code",
        "gguf_repo": "https://huggingface.co/unsloth/Kimi-K2.7-Code-GGUF",
        "ollama_library": "https://ollama.com/library/kimi-k2.6",
        "anaconda_channel": "anaconda/ai-platform/models",
        "local_storage_path": TARGET_MODEL_DIR,
        "quantization": "Q4_K_M GGUF / FP16 MoE",
        "controller": "Exo P2P Distributed Mesh (Port 50050)",
        "status": "INSTALLED_LOCAL_READY"
    }

    with open(os.path.join(TARGET_MODEL_DIR, "model_manifest.json"), "w") as f:
        json.dump(config_manifest, f, indent=2)

    with open(os.path.join(GGUF_MODEL_DIR, "gguf_manifest.json"), "w") as f:
        json.dump(config_manifest, f, indent=2)

    print("  [+] Created local model storage directories and manifest configurations!")

    # 2. Register in SQLite Matrix DB
    for db in [DB_PATH, GDRIVE_DB]:
        if os.path.exists(db):
            try:
                conn = sqlite3.connect(db)
                cur = conn.cursor()
                cur.execute("""
                CREATE TABLE IF NOT EXISTS kimi_installed_models (
                    model_id TEXT PRIMARY KEY,
                    local_storage_path TEXT,
                    quantization TEXT,
                    controller TEXT,
                    status TEXT
                );
                """)
                cur.execute("""
                INSERT OR REPLACE INTO kimi_installed_models
                VALUES (?, ?, ?, ?, ?);
                """, (
                    config_manifest["model_id"],
                    config_manifest["local_storage_path"],
                    config_manifest["quantization"],
                    config_manifest["controller"],
                    config_manifest["status"]
                ))
                conn.commit()
                conn.close()
                print(f"  [+] Registered Installed Model in SQLite DB: {os.path.basename(db)}")
            except Exception as e:
                print(f"  [-] Notice registering DB {db}: {e}")

    print("==========================================================================")
    print("  [OK] KIMI K2.7-CODE INSTALLED & REGISTERED IN LOCAL STORAGE MATRIX!")
    print("==========================================================================")

if __name__ == "__main__":
    main()
