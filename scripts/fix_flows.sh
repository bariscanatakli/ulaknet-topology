#!/bin/bash

echo "Adding flow rules to all switches..."

# Get list of switches
switches=$(sudo ovs-vsctl list-br)

for switch in $switches; do
    echo "Setting up flows for $switch"
    # Clear existing flows
    sudo ovs-ofctl del-flows $switch
    
    # Add basic forwarding rules
    sudo ovs-ofctl add-flow $switch "priority=1000,arp,actions=FLOOD"
    sudo ovs-ofctl add-flow $switch "priority=900,ip,actions=NORMAL"
    
    echo "Flows configured for $switch"
done

echo "All switches configured."
echo "Waiting for network convergence..."
sleep 5
echo "Done."
