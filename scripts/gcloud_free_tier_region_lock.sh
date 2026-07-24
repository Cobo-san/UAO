#!/bin/bash
# GCP Distro-to-Region 1-to-1 Free Tier Enforcer Shell Script
# Automatically assigns:
# - AlmaLinux-10 --> us-central1 (Iowa)
# - Ubuntu       --> us-west1    (Oregon)

set -e

echo "=== Initializing Distro-to-Region Dedicated Free Tier Lock ==="

DISTRO_NAME="unknown"
if [ -f /etc/os-release ]; then
    if grep -qi "alma" /etc/os-release; then
        DISTRO_NAME="AlmaLinux"
        TARGET_REGION="us-central1"
        TARGET_ZONE="us-central1-a"
    elif grep -qi "ubuntu" /etc/os-release; then
        DISTRO_NAME="Ubuntu"
        TARGET_REGION="us-west1"
        TARGET_ZONE="us-west1-a"
    fi
fi

if [ "$DISTRO_NAME" = "unknown" ]; then
    TARGET_REGION="us-central1"
    TARGET_ZONE="us-central1-a"
fi

echo "[*] Detected Distro: $DISTRO_NAME"
echo "[*] Assigned Dedicated Free Tier Region: $TARGET_REGION ($TARGET_ZONE)"

echo "[1/3] Deploying Regional Profile (/etc/profile.d/gcp_free_tier.sh)..."
cat <<EOF | tee /etc/profile.d/gcp_free_tier.sh > /dev/null
# Dedicated Distro-to-Region Free Tier Enforcer ($DISTRO_NAME)
export GCP_ASSIGNED_DISTRO="$DISTRO_NAME"
export CLOUDSDK_COMPUTE_REGION="$TARGET_REGION"
export CLOUDSDK_COMPUTE_ZONE="$TARGET_ZONE"
export CLOUDSDK_CORE_DISABLE_PROMPTS="1"
EOF
chmod +x /etc/profile.d/gcp_free_tier.sh

echo "[2/3] Configuring gcloud CLI defaults if installed..."
if command -v gcloud &>/dev/null; then
    gcloud config set compute/region "$TARGET_REGION"
    gcloud config set compute/zone "$TARGET_ZONE"
    gcloud config set core/disable_prompts true
    echo "  [+] gcloud compute/region locked to $TARGET_REGION"
else
    echo "  [!] gcloud CLI not found in PATH yet, profile guardrails deployed."
fi

echo "[3/3] Executing Python Guardrail Engine..."
if command -v python3 &>/dev/null; then
    python3 "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/scripts/gcloud_free_tier_region_lock.py"
fi

echo "=== DEDICATED DISTRO-TO-REGION FREE LOCK ENFORCED FOR $DISTRO_NAME ==="
