#!/bin/bash

echo "Cleaning up any existing Mininet instances..."
sudo mn -c

echo "Making sure Open vSwitch is running..."
bash "$(dirname "$0")/restart_ovs.sh"

# Check if OVS is running
if ! sudo ovs-vsctl show &> /dev/null; then
    echo "ERROR: Open vSwitch is not running. Cannot continue."
    exit 1
fi

echo "Running ULAKNET Topology..."
cd ../ulaknet-topology-project-1/src
sudo python3 main.py

echo "Mininet topology has been set up successfully."
echo ""
echo "If you encountered issues with missing commands like traceroute or iperf,"
echo "please run: bash scripts/install_host_tools.sh"