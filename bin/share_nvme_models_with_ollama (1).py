#!/usr/bin/env python3
"""
Ollama & NVMe Model Sharing Bridge Engine
Configures Ollama to share and utilize the pre-built GGUF model weights, subagents,
and vector mirrors stored on C: and D: NVMe drives without re-downloading.
"""

import os
import sys
import json
import sqlite3
import platform

ACCOUNT_EMAIL = "sounddharma@gmail.com"
GCP_PROJECT_ID = "anaconda-google-project-sounddharma"

# Model paths on NVMe drives
PRIMARY_NVME_MODEL = r"C:\AI_Dedicated_Storage_1TB\models_gguf\Llama-3.3-70B-Instruct-Q4_K_M.gguf"
SECONDARY_NVME_MODEL = r"D:\AI_Dedicated_Storage_Secondary\models_gguf_mirror\Llama-3.3-70B-Instruct-Q4_K_M.gguf"

POSIX_SECONDARY_MODEL = "/mnt/d/AI_Dedicated_Storage_Secondary/models_gguf_mirror/Llama-3.3-70B-Instruct-Q4_K_M.gguf"

def get_current_os():
    return platform.system()

def create_ollama_modelfile(target_dir):
    os.makedirs(target_dir, exist_ok=True)
    modelfile_path = os.path.join(target_dir, "Modelfile.llama3.3")

    model_src = POSIX_SECONDARY_MODEL if get_current_os() != "Windows" else SECONDARY_NVME_MODEL.replace("\\", "/")

    content = f"""# Ollama Modelfile sharing local NVMe GGUF weights
FROM {model_src}

# System Prompt Template for Cobo-San / UAO Subagents
SYSTEM "" You are an expert AI subagent in the UAO system running on dual NVMe storage with zero-cost local inference. ""

# Parameters optimized for 24-core i9-14900K and NVMe throughput
PARAMETER num_ctx 8192
PARAMETER temperature 0.7
PARAMETER top_p 0.9
"""

    with open(modelfile_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[+] Created Ollama Modelfile sharing NVMe GGUF weights: {modelfile_path}")
    return modelfile_path

def generate_environment_config():
    print("\n=== OLLAMA & NVME MODEL SHARING ENVIRONMENT CONFIG ===")
    print("Add the following environment variable to Windows / WSL2 to point Ollama directly to D: Drive:")
    print("--------------------------------------------------------------------------")
    print(r"  Windows PowerShell: $env:OLLAMA_MODELS = 'D:\AI_Dedicated_Storage_Secondary\models_gguf_mirror'")
    print(r"  System Environment: OLLAMA_MODELS=D:\AI_Dedicated_Storage_Secondary\models_gguf_mirror")
    print(r"  Linux / WSL2: export OLLAMA_MODELS=/mnt/d/AI_Dedicated_Storage_Secondary/models_gguf_mirror")
    print("--------------------------------------------------------------------------\n")

def main():
    print("=== OLLAMA & NVME MODEL SHARING BRIDGE ENGINE ===")
    target_dir = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\templates\ollama"
    if get_current_os() != "Windows":
        target_dir = "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/templates/ollama"

    create_ollama_modelfile(target_dir)
    generate_environment_config()
    print("[OK] NVME MODEL SHARING CONFIGURATION CREATED WITH 100% SUCCESS!")

if __name__ == "__main__":
    main()
