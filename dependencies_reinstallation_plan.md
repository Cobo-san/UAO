# Complete System Image & Dependencies Re-installation Plan 🌐🛠️

**Account Target**: `sounddharma@gmail.com`  
**GCP Project ID**: `anaconda-google-project-sounddharma`  
**Conda Environment**: `anaconda_google_project`  
**Re-installation Target**: 100% Reproducible Bare-Metal / Fresh OS Restore  
**Monthly Spend Target**: `$0.00 ABSOLUTE ZERO-COST GUARANTEED`

---

## 📋 Step 1: Pre-Requisites & Hardware Workspace Preparation

1. **Host Hardware Setup**:
   - Intel i9-14900K (or equivalent 24+ logical thread CPU)
   - Primary NVMe SSD mounted to `C:\AI_Dedicated_Storage_1TB`
   - Secondary NVMe SSD mounted to `D:\AI_Dedicated_Storage_Secondary`
   - Ensure local Llama 3.3 70B model file `Llama-3.3-70B-Instruct-Q4_K_M.gguf` is placed in `D:\AI_Dedicated_Storage_Secondary\models_gguf_mirror\`.

2. **Google Drive Sync Mounting**:
   - Mount Google Drive account (`sounddharma@gmail.com`) to `C:\Users\Monica Fugazi\GoogleDrive_sounddharma`.

---

## 🐍 Step 2: Conda Environment & Python Dependencies Installation

Run the following commands in PowerShell / Terminal:

```bash
# 1. Create Conda Environment from environment.yml
conda env create -f environment.yml

# 2. Activate Conda Environment
conda activate anaconda_google_project

# 3. Verify Pinned Dependencies
pip install -r requirements.txt
```

### Pinned Dependencies Package Manifest:
```text
cirq==1.7.0
openfermion==1.8.1
numpy==2.5.1
scipy==1.18.0
requests==2.34.2
urllib3==2.7.0
setuptools==83.0.0
```

---

## ⚙️ Step 3: Automated Database & System Re-hydration

Run the single-command automated restoration script:

```bash
python "C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\reinstall_master_system_and_dependencies.py"
```

This script will automatically:
1. Re-create `universal_synaptic_matrix.sqlite` database and populate all 19 system tables.
2. Initialize 32-Byte Binary IPC Header (`0x41494756` v2) across local NVMe and Google Drive paths.
3. Re-populate 45 Synaptic MCP Routes across ports `8080–8091`.
4. Re-establish GCP 1-to-1 Regional Free Tier locks (`us-east1`, `us-central1`, `us-west1`).
5. Re-register 8 Zero-Cost instances and 10 Multi-Continent global mirrors.
6. Re-launch Antigravity Live Terminal Server (Port 9999) and Cockpit HUD Dashboard.

---

## 🧪 Step 4: Verification & Audit Execution

Execute the full empirical verification suite:

```bash
# Run Master Functional Testing Suite
python "C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\run_master_functional_tests.py"

# Run Live System Status Diagnostic
python "C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\verify_system_status.py"
```

**Target Output**: `6/6 Functional Tests Passed (100% Success) | System Status: 100% OPERATIONAL`.

---

> [!NOTE]
> All dependency manifests (`requirements.txt`, `environment.yml`, `dependencies_manifest.json`) and complete system image packages have been serialized to Google Drive (`sounddharma@gmail.com`).
