#!/bin/bash

echo "Fixing network configuration..."

# Stop any running mininet instances
sudo mn -c

# Reset OpenFlow module
sudo rmmod openvswitch
sudo modprobe openvswitch

# Restart Open vSwitch service
sudo service openvswitch-switch restart

# Clean up any remaining interfaces
sudo ip link | grep -o 's[0-9]*-eth[0-9]*' | while read -r iface; do
    sudo ip link del "$iface" 2>/dev/null
done

# Clean up any lingering processes
sudo pkill -f ryu-manager
sudo pkill -f controller
sudo pkill -f ovs

echo "Network reset complete. You can now run the topology again."
