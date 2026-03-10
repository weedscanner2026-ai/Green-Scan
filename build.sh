#!/usr/bin/env bash
# Render build script

echo "Installing system dependencies for Pillow..."
apt-get update
apt-get install -y libjpeg-dev zlib1g-dev

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Build completed successfully!"
