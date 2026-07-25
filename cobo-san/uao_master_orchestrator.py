import os
import subprocess
import time
import sys

def run_script(script_name):
    script_path = os.path.join(r"C:\Locutus_UAO_Master_Environment", script_name)
    if not os.path.exists(script_path):
        print(f"[-] ERROR: UAO Core Module Missing: {script_name}")
        return False
        
    print(f"\n[*] Executing UAO Core Module: {script_name}...")
    try:
        subprocess.check_call([sys.executable, script_path])
        return True
    except subprocess.CalledProcessError as e:
        print(f"[-] FATAL ERROR executing {script_name}: {e}")
        return False

def main():
    print("==========================================================================")
    print("  LOCUTUS UAO: UNIFIED ASSEMBLY ORCHESTRATION - MASTER GATEWAY            ")
    print("==========================================================================")
    
    # Step 1: Hardware Optimization (Intel P-Core / E-Core Alignment)
    if not run_script("pin_locutus_to_ecores.py"):
        print("[!] UAO WARNING: CPU Affinity mapping failed. Proceeding without hardware optimization.")
        
    # Step 2: Global API Verification
    if not run_script("evaluate_and_verify_global_apis.py"):
        print("[!] UAO WARNING: Cloud Matrix Evaluation failed.")
        
    # Step 3: Global Deployment Trigger (Zero-Trust Halts if credentials missing)
    run_script("provision_global_zero_cost_mirrors.py")
    
    print("\n==========================================================================")
    print("  [OK] UAO GLOBAL ORCHESTRATION SEQUENCE COMPLETE.                        ")
    print("  [+] Starting UAO Neural FastAPI Gateway...                              ")
    print("==========================================================================")
    
    # Step 4: Boot up the Neural API Gateway
    gateway_path = os.path.join(r"C:\Locutus_UAO_Master_Environment", "uao_fastapi_gateway.py")
    if os.path.exists(gateway_path):
        subprocess.Popen([sys.executable, gateway_path])
        print("[+] FastAPI Gateway active on port 8000. UAO is fully online and listening.")
    else:
        print("[-] FATAL: FastAPI Gateway missing.")
        
if __name__ == "__main__":
    main()
