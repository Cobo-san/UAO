import os
import sys
import json
import base64
import subprocess
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    print("[*] Installing Cryptography stack for zero-trust encryption...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# The 32-byte binary IPC header used as the universal master cryptographic salt
UAO_MASTER_SALT = b"0x41494756"
GOOGLE_DRIVE_DIR = r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\cobo-san"

def get_encryption_key(password="sounddharma@gmail.com+fugazi@circadomine.com"):
    """Derives a Fernet symmetric key from the Dual-Identity Master String and the UAO Salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=UAO_MASTER_SALT,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return Fernet(key)

def encrypt_credentials(template_path, output_enc_path):
    if not os.path.exists(template_path):
        print(f"[-] ERROR: Template file not found at {template_path}")
        return False
        
    with open(template_path, "rb") as f:
        data = f.read()
        
    fernet = get_encryption_key()
    encrypted_data = fernet.encrypt(data)
    
    with open(output_enc_path, "wb") as f:
        f.write(encrypted_data)
        
    print(f"[+] SUCCESS: Dual-Identity Credentials encrypted to Google Drive: {output_enc_path}")
    return True

def decrypt_credentials(enc_path):
    if not os.path.exists(enc_path):
        print(f"[-] ERROR: Encrypted credential file not found at {enc_path}")
        return None
        
    fernet = get_encryption_key()
    with open(enc_path, "rb") as f:
        encrypted_data = f.read()
        
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        creds = json.loads(decrypted_data.decode())
        print(f"[+] SUCCESS: Decrypted 14-Node Dual-Identity Matrix from Google Drive")
        return creds
    except Exception as e:
        print(f"[-] FATAL: Decryption failed. Incorrect key or corrupted matrix. {e}")
        return None

if __name__ == "__main__":
    print("==========================================================================")
    print("  LOCUTUS UAO: 14-NODE DUAL-IDENTITY CRYPTOGRAPHIC ENGINE                 ")
    print("==========================================================================")
    
    template = os.path.join(GOOGLE_DRIVE_DIR, "uao_global_credentials_template.json")
    enc_target = os.path.join(GOOGLE_DRIVE_DIR, "uao_cloud_credentials.enc")
    
    if os.path.exists(template):
        print("[*] Found plain-text 14-Node credential template. Encrypting to Google Drive...")
        encrypt_credentials(template, enc_target)
        print("[!] SECURITY WARNING: Please delete or secure the plain-text template.")
    else:
        print("[*] No template found. Attempting to decrypt active Dual-Identity matrix...")
        creds = decrypt_credentials(enc_target)
        if creds:
            print("[+] Active 14-Node Matrix Authorization Keys Loaded into Memory.")
