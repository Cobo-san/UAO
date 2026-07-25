#!/bin/bash
# ==============================================================================
# LOCUTUS UAO: UNIVERSAL LINUX MULTI-OS COBO-SAN INSTALLER & KERNEL BOOTSTRAP
# ==============================================================================
# This script is designed to run on ANY zero-cost free-tier VM (Debian, Ubuntu, 
# AlmaLinux, openSUSE, Amazon Linux) to instantly inject the Synaptic Kernels, 
# MCP servers, and Anaconda AI Environmental Stacks.
# ==============================================================================

echo "[*] Locutus Global Matrix: Bootstrapping UAO Linux Environment..."

# 1. OS Detection & Base Package Installation
if [ -f /etc/debian_version ]; then
    echo "  [+] OS Detected: Debian/Ubuntu (Azure/GCP)"
    sudo apt-get update -y
    sudo apt-get install -y python3-pip python3-venv git curl wget jq build-essential nodejs npm
elif [ -f /etc/redhat-release ]; then
    echo "  [+] OS Detected: AlmaLinux / RHEL / Amazon Linux (GCP/AWS)"
    sudo dnf install -y python3-pip git curl wget jq gcc-c++ make nodejs npm
elif [ -f /etc/os-release ] && grep -q "openSUSE" /etc/os-release; then
    echo "  [+] OS Detected: openSUSE Leap (Oracle Cloud)"
    sudo zypper install -y python3-pip git curl wget jq gcc-c++ nodejs npm
else
    echo "  [-] OS Not Officially Mapped. Attempting standard generic install..."
fi

# 2. Setup the Universal Storage Paths
echo "[*] Constructing Locutus Master Paths..."
sudo mkdir -p /opt/UAO/synaptic_matrix
sudo mkdir -p /opt/UAO/mcp_servers
sudo chown -R $USER:$USER /opt/UAO

# 3. Injecting the Synaptic Kernels & MCP Engines
echo "[*] Installing Anaconda AI MCP Servers..."
# We will use 'uv' to manage rapid python environments as per the Anaconda standard
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Setup the primary virtual environment for the Synaptic Kernels
uv venv /opt/UAO/synaptic_matrix/.venv
source /opt/UAO/synaptic_matrix/.venv/bin/activate

# Install the environmental stacks required for the MCPs
uv pip install fastapi uvicorn sqlite-utils psutil requests aiohttp

# 4. Synchronize with Master GitHub Matrix
echo "[*] Synchronizing Master Cobo-San Payload from GitHub..."
cd /opt/UAO
git init
git remote add origin https://github.com/Cobo-san/UAO.git
git pull origin main

# 5. Execute 32-Byte Binary IPC Generation & Permissions
echo "[*] Generating Synaptic IPC Headers..."
chmod +x /opt/UAO/bin/master_compile_and_build.py
python3 /opt/UAO/bin/master_compile_and_build.py

echo "=========================================================================="
echo "  [OK] COBO-SAN LINUX KERNEL, MCP & ANACONDA STACKS SUCCESSFULLY DEPLOYED!"
echo "=========================================================================="
