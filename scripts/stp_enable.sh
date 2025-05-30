#!/bin/bash

echo "Enabling STP on all switches to prevent forwarding loops..."
for s in {1..19}; do
    sudo ovs-vsctl set bridge s$s stp_enable=true
    echo "Enabled STP on s$s"
done
echo "STP configuration complete. Please wait a few seconds for convergence."
