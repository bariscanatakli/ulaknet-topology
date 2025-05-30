#!/bin/bash

# Get the absolute path of the repository root directory
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Installing Python dependencies..."
sudo pip3 install -r "${REPO_ROOT}/requirements.txt"

echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-dev python3-tk

echo "Creating required directories..."
mkdir -p "${REPO_ROOT}/output"

echo "Dependencies installed successfully."
