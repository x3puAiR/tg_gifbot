
#!/bin/sh

# Alpine Linux Python 3 and FFmpeg Installation Script
# This script installs Python 3, pip, FFmpeg, and necessary build dependencies

set -e 

echo "=========================================="
echo "Alpine Linux Setup Script"
echo "Installing Python 3, pip, and FFmpeg"
echo "=========================================="

# Step 1: Update package index
echo ""
echo "[1/6] Updating package index..."
apk update

# Step 2: Install Python 3, pip, and bash
echo ""
echo "[2/6] Installing Python 3, pip, and bash..."
apk add --no-cache python3 python3-dev py3-pip bash

# Verify Python installation
echo "Python version installed:"
python3 --version

# Step 3: Install FFmpeg and its dependencies
echo ""
echo "[3/6] Installing FFmpeg..."
apk add --no-cache ffmpeg

# Verify FFmpeg installation
echo ""
echo "FFmpeg version installed:"
ffmpeg -version | head -n 1

# Step 4: Install build dependencies for Python packages that might need compilation
echo ""
echo "[4/6] Installing build dependencies..."
apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    zlib-dev \
    jpeg-dev \
    openjpeg-dev \
    linux-headers

# Step 5: Upgrade pip
echo ""
echo "[5/6] Upgrading pip..."
python3 -m pip install --upgrade pip

echo "pip version:"
pip3 --version

# Step 6: Clean up to reduce image size
echo ""
echo "[6/6] Cleaning up package cache..."
rm -rf /var/cache/apk/*

# Summary
echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Installed Software:"
echo "  - Python: $(python3 --version)"
echo "  - pip: $(pip3 --version | cut -d' ' -f1-2)"
echo "  - FFmpeg: $(ffmpeg -version | head -n 1 | cut -d' ' -f1-3)"
echo ""
echo "You can now use python3, pip3, and ffmpeg commands."
echo "=========================================="

echo ">>> Setup tgbot configuration"
