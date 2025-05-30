#!/bin/bash

echo "Restarting Open vSwitch services..."

# Make sure the modules are loaded
sudo modprobe openvswitch

# Start or restart the service
sudo service openvswitch-switch start

# Wait a moment for the service to initialize
sleep 2

# Check if the service is running properly
if sudo ovs-vsctl show &> /dev/null; then
    echo "Open vSwitch is now running."
else
    echo "Failed to start Open vSwitch. Please check your installation."
    echo "Attempting manual initialization..."
    
    # Manual initialization if service command fails
    sudo /etc/init.d/openvswitch-switch restart
    sleep 2
    
    # Check again
    if sudo ovs-vsctl show &> /dev/null; then
        echo "Open vSwitch is now running."
    else
        echo "ERROR: Could not start Open vSwitch. Mininet will not function properly."
    fi
fi
