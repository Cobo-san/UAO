import os
import subprocess

def evaluate_and_verify():
    print("==========================================================================")
    print("   LOCUTUS WORKFLOW: EVALUATE | VERIFY | OPTIMIZE | ADJUST                ")
    print("==========================================================================")

    # 1. Evaluate Dependencies
    print("[*] Evaluating Cloud CLI Dependencies...")
    
    # Check Azure CLI
    az_check = subprocess.run(["az", "--version"], capture_output=True, text=True, shell=True)
    if az_check.returncode == 0:
        print("  [+] VERIFIED: Azure CLI (az) is installed and accessible.")
    else:
        print("  [-] ADJUSTMENT REQUIRED: Azure CLI is missing. Locutus will bypass Azure provisioning until installed.")
        
    # Check Oracle CLI
    oci_check = subprocess.run(["oci", "--version"], capture_output=True, text=True, shell=True)
    if oci_check.returncode == 0:
        print("  [+] VERIFIED: Oracle Cloud CLI (oci) is installed and accessible.")
    else:
        print("  [-] ADJUSTMENT REQUIRED: Oracle Cloud CLI is missing. Locutus will bypass OCI provisioning until installed.")
        
    # Check AWS CLI
    aws_check = subprocess.run(["aws", "--version"], capture_output=True, text=True, shell=True)
    if aws_check.returncode == 0:
        print("  [+] VERIFIED: AWS CLI (aws) is installed and accessible.")
    else:
        print("  [-] ADJUSTMENT REQUIRED: AWS CLI is missing. Locutus will bypass AWS EC2 provisioning until installed.")
        
    # 2. Optimize & Adjust (SSH Keys)
    print("\n[*] Optimizing Global Zero-Trust Security Keys...")
    ssh_dir = r"C:\Users\Monica Fugazi\.ssh"
    key_path = os.path.join(ssh_dir, "Locutus_Global_RSA")
    os.makedirs(ssh_dir, exist_ok=True)
    
    if not os.path.exists(key_path):
        print(f"  [-] ADJUSTMENT: Global SSH key missing. Generating now...")
        subprocess.run(f'ssh-keygen -t rsa -b 4096 -N "" -f "{key_path}" -C "locutus_global_matrix"', shell=True)
        print(f"  [+] OPTIMIZED: Generated Locutus_Global_RSA at {key_path}")
    else:
        print(f"  [+] VERIFIED: Locutus_Global_RSA key already exists.")

    print("==========================================================================")
    print(" [OK] EVALUATION COMPLETE. READY FOR: BUILD | COMPILE | SAVE MEMORIES")
    print("==========================================================================")

if __name__ == "__main__":
    evaluate_and_verify()
