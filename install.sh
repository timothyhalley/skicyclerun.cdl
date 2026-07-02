#!/usr/bin/env bash

# ============================================================
# ComfyUI Model Sync Installer
# Author: TIMOTHY + Copilot
# Description: Installs Python dependencies for the model
#              extraction + download system.
# ============================================================

set -e  # Stop on error
set -o pipefail

# ------------------------------------------------------------
# Emoji helpers
# ------------------------------------------------------------
INFO="🔵"
OK="🟢"
WARN="🟡"
ERR="🔴"

# ------------------------------------------------------------
# Step 1: Check Python availability
# ------------------------------------------------------------
echo "$INFO Checking Python installation..."

if ! command -v python3 >/dev/null 2>&1; then
    echo "$ERR Python3 is not installed. Please install Python 3.10+ first."
    exit 1
fi

echo "$OK Python found: $(python3 --version)"

# ------------------------------------------------------------
# Step 2: Create virtual environment (optional but recommended)
# ------------------------------------------------------------
VENV_DIR=".venv"

echo "$INFO Creating virtual environment at $VENV_DIR..."

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "$OK Virtual environment created."
else
    echo "$WARN Virtual environment already exists. Skipping creation."
fi

# Activate venv
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
echo "$OK Virtual environment activated."

# ------------------------------------------------------------
# Step 3: Upgrade pip
# ------------------------------------------------------------
echo "$INFO Upgrading pip..."
pip install --upgrade pip
echo "$OK pip upgraded."

# ------------------------------------------------------------
# Step 4: Install HuggingFace ecosystem
# ------------------------------------------------------------
echo "$INFO Installing HuggingFace libraries..."

pip install -U huggingface_hub transformers datasets accelerate hf_transfer

echo "$OK HuggingFace libraries installed."

# ------------------------------------------------------------
# Step 5: Install project requirements
# ------------------------------------------------------------
if [ -f "requirements.txt" ]; then
    echo "$INFO Installing project requirements..."
    pip install -r requirements.txt
    echo "$OK requirements.txt installed."
else
    echo "$WARN requirements.txt not found. Skipping."
fi

# ------------------------------------------------------------
# Step 6: Final message
# ------------------------------------------------------------
echo ""
echo "============================================================"
echo "$OK Installation complete!"
echo "🎉 Your ComfyUI Model Sync environment is ready!"