import os
import sys

def check_aws_auth():
    print("[*] Checking AWS Authentication for Sydney Amazon Linux Node...")
    aws_dir = os.path.expanduser("~/.aws")
    if not os.path.exists(aws_dir) or not os.path.exists(os.path.join(aws_dir, "credentials")):
        print("  [-] ERROR: AWS Credentials missing.")
        print("  [!] Please run 'aws configure' or place credentials in ~/.aws/credentials")
        return False
    print("  [+] AWS Credentials Found.")
    return True

def check_oci_auth():
    print("[*] Checking Oracle Cloud Authentication for Frankfurt openSUSE Node...")
    oci_dir = os.path.expanduser("~/.oci")
    if not os.path.exists(oci_dir) or not os.path.exists(os.path.join(oci_dir, "config")):
        print("  [-] ERROR: OCI Credentials missing.")
        print("  [!] Please place Oracle config in ~/.oci/config")
        return False
    print("  [+] OCI Credentials Found.")
    return True

def check_azure_auth():
    print("[*] Checking Azure Authentication for Hong Kong/Netherlands Nodes...")
    if not os.getenv("AZURE_CLIENT_ID") or not os.getenv("AZURE_TENANT_ID") or not os.getenv("AZURE_CLIENT_SECRET"):
        print("  [-] ERROR: Azure Service Principal environmental variables missing.")
        print("  [!] Please set AZURE_CLIENT_ID, AZURE_TENANT_ID, and AZURE_CLIENT_SECRET")
        return False
    print("  [+] Azure Credentials Found.")
    return True

def main():
    print("==========================================================================")
    print("  LOCUTUS UAO: GLOBAL ZERO-COST CLOUD PROVISIONING ENGINE                 ")
    print("==========================================================================")
    
    auth_status = {
        "AWS": check_aws_auth(),
        "OCI": check_oci_auth(),
        "Azure": check_azure_auth()
    }
    
    if not any(auth_status.values()):
        print("\n==========================================================================")
        print(" [!] EXECUTION HALTED: ZERO-TRUST CLOUD AUTHENTICATION REQUIRED")
        print(" Locutus requires your Cloud API Credentials to authorize the deployment.")
        print(" Please provide the credentials, and Locutus will resume provisioning.")
        print("==========================================================================")
        sys.exit(1)
        
    print("\n[+] Authentication verified. Initiating Global Deployment via Cloud SDKs...")
    # Cloud provisioning logic using boto3, oci, azure SDKs goes here once auth passes.

if __name__ == "__main__":
    main()
