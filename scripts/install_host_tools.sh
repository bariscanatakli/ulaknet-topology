#!/bin/bash

echo "Installing necessary tools for Mininet hosts..."
sudo apt-get update
sudo apt-get install -y traceroute iperf wget python3-pip
echo "Installation complete."
