#!/bin/bash

# CentOS 7 Python 3.6 and FFmpeg Installation Script
# This script handles deprecated CentOS 7 repositories and installs required software

set -e  # Exit on error

echo "=========================================="
echo "CentOS 7 Setup Script"
echo "Installing Python 3.6 and FFmpeg"
echo "=========================================="

# Step 1: Fix CentOS 7 repository URLs (vault.centos.org)
echo ""
echo "[1/5] Updating CentOS repository mirrors to vault.centos.org..."
sed -i 's|^mirrorlist=|#mirrorlist=|g' /etc/yum.repos.d/CentOS-*.repo
sed -i 's|^#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*.repo

# Clean yum cache
yum clean all
yum makecache

echo "Repository URLs updated successfully!"

# Step 2: Install Python 3.6
echo ""
echo "[2/5] Installing Python 3.6..."
yum install -y python3

# Verify Python installation
echo "Python version installed:"
python3 --version

# Install pip for Python 3
echo ""
echo "[3/5] Installing pip for Python 3..."
yum install -y python3-pip

# Upgrade pip
python3 -m pip install --upgrade pip

echo "pip version:"
pip3 --version

# Step 3: Install EPEL repository for FFmpeg dependencies
echo ""
echo "[4/5] Installing EPEL repository..."
yum install -y epel-release

# Update EPEL repo to vault as well
sed -i 's|^metalink=|#metalink=|g' /etc/yum.repos.d/epel.repo
sed -i 's|^#baseurl=http://download.fedoraproject.org/pub/epel|baseurl=http://archives.fedoraproject.org/pub/archive/epel|g' /etc/yum.repos.d/epel.repo

# Install RPM Fusion repository for FFmpeg
echo "Installing RPM Fusion repository..."
yum localinstall -y --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm

# Step 4: Install FFmpeg
echo ""
echo "[5/5] Installing FFmpeg..."
yum install -y ffmpeg ffmpeg-devel

# Verify FFmpeg installation
echo ""
echo "FFmpeg version installed:"
ffmpeg -version | head -n 1

# Step 5: Summary
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
