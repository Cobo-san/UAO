#!/bin/bash
# Universal Cross-OS Bridge Setup Script for Linux / WSL Distros
# Enables universal NVMe, Google Drive, AI Agent, Metadata, Repos, and Binary IPC access.

set -e

echo "=== Initializing Universal Cross-OS Google Drive, NVMe & AI Agent Bridge ==="

# 1. Standardize NVMe, Google Drive & Repos Mount Paths
PRIMARY_NVME_SRC="/mnt/c/AI_Dedicated_Storage_1TB"
SECONDARY_NVME_SRC="/mnt/d/AI_Dedicated_Storage_Secondary"
GOOGLE_DRIVE_SRC="/mnt/c/Users/Monica Fugazi/GoogleDrive_sounddharma"
LIVING_REPO_SRC="/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository"
BRAIN_SRC="/mnt/c/Users/Monica Fugazi/.gemini/antigravity-cli/brain"

# Target Symlinks
PRIMARY_LINK="/var/ai_storage_primary"
SECONDARY_LINK="/var/ai_storage_secondary"
GDRIVE_LINK="/var/google_drive_sounddharma"
LIVING_REPO_LINK="/var/living_repository"
BRAIN_LINK="/var/ai_brain"

GOLDEN_DB_LINK="/var/golden_image_db"
SYNAPTIC_DRIVE_LINK="/var/synaptic_matrix_drive"
SNAPSHOTS_LINK="/var/snapshots_archive"
STAGING_LINK="/var/staging_15day_drive"

echo "[1/4] Configuring Symlinks for NVMe, Google Drive, and Project Repos..."
[ -d "$PRIMARY_NVME_SRC" ] && ln -sfn "$PRIMARY_NVME_SRC" "$PRIMARY_LINK" && echo "  + $PRIMARY_LINK -> $PRIMARY_NVME_SRC"
[ -d "$SECONDARY_NVME_SRC" ] && ln -sfn "$SECONDARY_NVME_SRC" "$SECONDARY_LINK" && echo "  + $SECONDARY_LINK -> $SECONDARY_NVME_SRC"
[ -d "$GOOGLE_DRIVE_SRC" ] && ln -sfn "$GOOGLE_DRIVE_SRC" "$GDRIVE_LINK" && echo "  + $GDRIVE_LINK -> $GOOGLE_DRIVE_SRC"
[ -d "$LIVING_REPO_SRC" ] && ln -sfn "$LIVING_REPO_SRC" "$LIVING_REPO_LINK" && echo "  + $LIVING_REPO_LINK -> $LIVING_REPO_SRC"
[ -d "$BRAIN_SRC" ] && ln -sfn "$BRAIN_SRC" "$BRAIN_LINK" && echo "  + $BRAIN_LINK -> $BRAIN_SRC"

# Google Drive Subdirectories
[ -d "$GOOGLE_DRIVE_SRC/Golden_Image_Database" ] && ln -sfn "$GOOGLE_DRIVE_SRC/Golden_Image_Database" "$GOLDEN_DB_LINK" && echo "  + $GOLDEN_DB_LINK -> Golden_Image_Database"
[ -d "$GOOGLE_DRIVE_SRC/Parallel_Synaptic_Database_Matrix" ] && ln -sfn "$GOOGLE_DRIVE_SRC/Parallel_Synaptic_Database_Matrix" "$SYNAPTIC_DRIVE_LINK" && echo "  + $SYNAPTIC_DRIVE_LINK -> Parallel_Synaptic_Database_Matrix"
[ -d "$GOOGLE_DRIVE_SRC/Snapshots_Reversion_Archive" ] && ln -sfn "$GOOGLE_DRIVE_SRC/Snapshots_Reversion_Archive" "$SNAPSHOTS_LINK" && echo "  + $SNAPSHOTS_LINK -> Snapshots_Reversion_Archive"
[ -d "$GOOGLE_DRIVE_SRC/Staging_Build_15Day_Test" ] && ln -sfn "$GOOGLE_DRIVE_SRC/Staging_Build_15Day_Test" "$STAGING_LINK" && echo "  + $STAGING_LINK -> Staging_Build_15Day_Test"

# 2. Deploy Universal Global Environment File into /etc/profile.d/
echo "[2/4] Deploying Universal Environment Variables (/etc/profile.d/universal_ai_agents.sh)..."
cat <<'EOF' | tee /etc/profile.d/universal_ai_agents.sh > /dev/null
# Universal Cross-OS AI & Storage Environment Config
export AI_STORAGE_PRIMARY="/var/ai_storage_primary"
export AI_STORAGE_SECONDARY="/var/ai_storage_secondary"
export GOOGLE_DRIVE_SOUNDDHARMA="/var/google_drive_sounddharma"
export GOLDEN_IMAGE_DB="/var/golden_image_db"
export SYNAPTIC_MATRIX_DRIVE="/var/synaptic_matrix_drive"
export LIVING_REPOSITORY="/var/living_repository"
export AI_BRAIN_ROOT="/var/ai_brain"
export SYNAPTIC_MATRIX_DB="/var/living_repository/synaptic_matrix/universal_synaptic_matrix.sqlite"
export SYNAPTIC_MATRIX_BINARY="/var/living_repository/synaptic_matrix/universal_ipc_state.bin"
export PATH="$PATH:/var/living_repository/bin"
EOF
chmod +x /etc/profile.d/universal_ai_agents.sh

# 3. Execute Universal Binary IPC Engine Python script
echo "[3/4] Running Universal Binary IPC Engine sync..."
if command -v python3 &>/dev/null; then
    python3 "$LIVING_REPO_SRC/bin/universal_binary_ipc_engine.py"
else
    echo "  ! python3 not found, skipping immediate Python run."
fi

echo "[4/4] Verification check..."
ls -la /var/ai_storage_primary /var/ai_storage_secondary /var/google_drive_sounddharma /var/golden_image_db /var/living_repository

echo "=== UNIFORM GOOGLE DRIVE, NVME & REPO BRIDGE SETUP COMPLETE ==="
