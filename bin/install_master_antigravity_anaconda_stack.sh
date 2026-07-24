#!/bin/bash
# Master Antigravity IDE & Anaconda AI Platform Stack Linux / WSL / FreeBSD 1-Click Installer

set -e

echo "========================================================================="
echo " MASTER ANTIGRAVITY IDE & ANACONDA AI PLATFORM STACK 1-CLICK INSTALLER"
echo "========================================================================="

LIVING_REPO="/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository"
if [ ! -d "$LIVING_REPO" ]; then
    LIVING_REPO="/var/living_repository"
fi

if command -v python3 &>/dev/null; then
    python3 "$LIVING_REPO/bin/install_master_antigravity_anaconda_stack.py"
else
    echo "[-] Error: python3 not found. Please install Python 3.12+ first."
    exit 1
fi
