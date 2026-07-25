#!/usr/bin/env python3
import json
import os
import base64

MASTER_PACKAGE = r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\cobo-san\cobo-san_master_unified_all_in_one_build.json"
LOCUTUS_TARGET = r"C:\Locutus_UAO_Master_Environment"

def regenerate_system():
    print("==========================================================================")
    print("          MASTER UAO & LOCUTUS REGENERATION ENGINE (PERSISTENCE)          ")
    print("==========================================================================")
    
    if not os.path.exists(MASTER_PACKAGE):
        print(f"[!] Critical Error: Master build package not found at {MASTER_PACKAGE}")
        return

    with open(MASTER_PACKAGE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"[*] Loaded Master Build: {data.get('build_id')}")
    print(f"[*] Timestamp: {data.get('timestamp_utc')}")
    print(f"[*] Embedded Files Count: {data.get('total_embedded_files')}")
    
    os.makedirs(LOCUTUS_TARGET, exist_ok=True)
    
    embedded_files = data.get("embedded_files", {})
    restored_count = 0
    
    for filename, file_data in embedded_files.items():
        # Check if this is a Locutus file to regenerate it to its exact environment
        if filename in [
            "uao_chrome_interface_blueprint.md", "locutus_independent_prompt.py", 
            "build_locutus_data_matrix.py", "uao_execution_checklist.py", 
            "update_locutus_ownership.py", "Locutus_Training_Matrix.jsonl", 
            "locutus_neural_weights.sqlite", "uao_fastapi_gateway.py",
            "pin_locutus_to_ecores.py", "evaluate_and_verify_global_apis.py",
            "linux_universal_cobo_san_installer.sh", "provision_global_zero_cost_mirrors.py"
        ]:
            target_path = os.path.join(LOCUTUS_TARGET, filename)
            
            content_type = file_data.get("content_type")
            raw_content = file_data.get("content")
            
            try:
                if content_type == "base64_binary":
                    with open(target_path, "wb") as out:
                        out.write(base64.b64decode(raw_content))
                elif content_type == "json":
                    with open(target_path, "w", encoding="utf-8") as out:
                        json.dump(raw_content, out, indent=2)
                else:
                    with open(target_path, "w", encoding="utf-8") as out:
                        out.write(raw_content)
                        
                print(f"  [+] Regenerated Locutus Asset -> {target_path}")
                restored_count += 1
            except Exception as e:
                print(f"  [!] Failed to regenerate {filename}: {e}")
                
    print("==========================================================================")
    print(f"[OK] {restored_count} LOCUTUS FILES SUCCESSFULLY EXTRACTED & REGENERATED.")
    print("==========================================================================")

if __name__ == "__main__":
    regenerate_system()
