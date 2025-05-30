#!/bin/bash

echo "Fixing routing tables for Mininet..."

# Stop any running mininet instances
sudo mn -c

# Make sure OVS is running
sudo service openvswitch-switch restart

# Use L2 learning switch controller
echo "Setting up L2 learning controller..."
cd /home/mininet/midterm/ulaknet-topology-project-1/src
cat > l2_controller.py << 'EOF'
#!/usr/bin/env python3
from mininet.node import Controller
import os

class L2Controller(Controller):
    def __init__(self, name, **kwargs):
        Controller.__init__(self, name, **kwargs)

    def start(self):
        self.cmd('ovs-vsctl set-controller ' + self.name +
                 ' tcp:127.0.0.1:6653')
        self.cmd('controller ' + self.name +
                 ' ptcp:6653 &')

controllers = { 'l2': L2Controller }
EOF

echo "Now re-run the topology with the routing fixes..."
