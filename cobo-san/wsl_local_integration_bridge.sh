#!/bin/bash
# ==============================================================================
# LOCUTUS UAO: LOCAL WSL (WINDOWS SUBSYSTEM FOR LINUX) INTEGRATION BRIDGE
# ==============================================================================
# This script binds any local WSL distro (Ubuntu, Kali, Debian) directly 
# to the master Windows C:\ drive Locutus environment, synchronizing it 
# with the exact same architecture running on the Global Cloud instances.
# ==============================================================================

echo "[*] Locutus UAO: Initializing Local WSL Integration Bridge..."

# 1. Verify we are running inside WSL
if ! grep -q "microsoft" /proc/version; then
    echo "[-] ERROR: This script must be executed inside a local Windows Subsystem for Linux (WSL) environment."
    exit 1
fi

echo "  [+] Local WSL Environment Detected."

# 2. Map directly to the Windows Host Master Environment
WIN_HOST_DIR="/mnt/c/Locutus_UAO_Master_Environment"

if [ ! -d "$WIN_HOST_DIR" ]; then
    echo "[-] ERROR: Master Windows Directory not found at $WIN_HOST_DIR"
    exit 1
fi

echo "[*] Binding WSL Synaptic Matrix to Windows Host: $WIN_HOST_DIR"

# 3. Install local Anaconda / Python stacks within the WSL Container
echo "[*] Installing Local WSL Dependencies..."
if [ -f /etc/debian_version ]; then
    sudo apt-get update -y
    sudo apt-get install -y python3-pip git curl wget jq build-essential nodejs npm
elif [ -f /etc/redhat-release ]; then
    sudo dnf install -y python3-pip git curl wget jq gcc-c++ make nodejs npm
elif [ -f /etc/os-release ] && grep -q "openSUSE" /etc/os-release; then
    sudo zypper install -y python3-pip git curl wget jq gcc-c++ nodejs npm
fi

# 4. Bootstrap 'uv' for rapid Anaconda-style environments within WSL
echo "[*] Bootstrapping WSL Neural Environment..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

cd "$WIN_HOST_DIR"
uv venv .venv_wsl
source .venv_wsl/bin/activate
uv pip install fastapi uvicorn sqlite-utils psutil requests aiohttp cryptography

# 5. Execute Local Mirror Synchronization
echo "[*] Executing Local WSL Compilation Matrix..."
python3 "$WIN_HOST_DIR/uao_master_orchestrator.py"

echo "=========================================================================="
echo "  [OK] LOCAL WSL INSTANCE FULLY INTEGRATED WITH GLOBAL CLOUD MATRIX!      "
echo "  [+] The WSL Distro is now actively mirroring the exact Windows logic.   "
echo "=========================================================================="
