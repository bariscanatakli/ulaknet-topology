#!/usr/bin/env python3

from mininet.cli import CLI
from mininet.log import setLogLevel, info
import sys
import time
import os
from topology.mininet_topology import create_mininet_topology, start_network

# Import the visualization module
try:
    from visualization.network_visualizer import visualize_network
    visualization_available = True
except ImportError:
    info('*** Visualization modules not available. Skipping visualization.\n')
    visualization_available = False

def perform_network_tests(net):
    """
    Perform basic connectivity tests on the network
    """
    info('*** Performing network tests\n')
    
    # Wait a bit to let the network fully converge
    info('*** Waiting for network convergence...\n')
    time.sleep(5)
    
    # Check if hosts have common network tools
    info('*** Checking for network tools\n')
    h1 = net.get('h1')
    
    # Check for traceroute
    has_traceroute = 'Usage' in h1.cmd('which traceroute')
    if not has_traceroute:
        info('Traceroute not found. You may want to run scripts/install_host_tools.sh\n')
    
    # Check for wget
    has_wget = 'Usage' in h1.cmd('which wget')
    if not has_wget:
        info('Wget not found. You may want to run scripts/install_host_tools.sh\n')
    
    # Check for iperf
    has_iperf = 'Usage' in h1.cmd('which iperf')
    if not has_iperf:
        info('Iperf not found. You may want to run scripts/install_host_tools.sh\n')
    
    # Test connectivity between specific hosts
    info('*** Testing connectivity between select hosts\n')
    
    # Test from Ankara to Istanbul
    h1 = net.get('h1')
    h4 = net.get('h4')
    info(f'*** Pinging from Ankara (h1) to Istanbul (h4): ')
    result = h1.cmd(f'ping -c3 -W2 {h4.IP()}')
    if '0% packet loss' in result:
        info('Success!\n')
    else:
        info('Failed\n')
        info(f'{result}\n')
    
    # Test from Istanbul to Izmir
    h7 = net.get('h7')
    info(f'*** Pinging from Istanbul (h4) to Izmir (h7): ')
    result = h4.cmd(f'ping -c3 -W2 {h7.IP()}')
    if '0% packet loss' in result:
        info('Success!\n')
    else:
        info('Failed\n')
        info(f'{result}\n')
    
    # Show command examples to the user
    info('\n*** Example commands for Mininet CLI:\n')
    info('h1 ping h4                   # Test connectivity\n')
    info('h1 python -m http.server 80 &  # Start web server\n')
    info('h4 wget -O- h1:80              # Access web server\n')
    if has_iperf:
        info('iperf h1 h4                   # Test bandwidth\n')
    if has_traceroute:
        info('h1 traceroute h16             # Show route\n')

    # View routes
    info('*** Viewing routes from h1\n')
    info(h1.cmd('route -n'))
    info('\n*** Viewing routes from h4\n')
    info(h4.cmd('route -n'))

def check_controller_connectivity(net):
    """
    Check if switches are connected to the controller and retry if necessary
    """
    info('*** Checking controller connectivity\n')
    max_retries = 3
    for retry in range(max_retries):
        connected_count = 0
        for switch in net.switches:
            result = switch.cmd('ovs-vsctl show | grep is_connected')
            if 'true' in result:
                connected_count += 1
        
        if connected_count == len(net.switches):
            info(f'*** All {connected_count} switches connected to controller\n')
            return True
        else:
            info(f'*** Only {connected_count}/{len(net.switches)} switches connected. Retrying ({retry+1}/{max_retries})...\n')
            time.sleep(5)  # Wait before retrying
    
    info('*** Warning: Not all switches could connect to the controller. Continue anyway...\n')
    return False

def main():
    # Set log level
    setLogLevel('info')
    
    # Generate network visualization if available
    if visualization_available:
        info('*** Generating network visualization\n')
        output_path = os.path.join(os.path.dirname(__file__), '..', 'output', 'ulaknet_topology.png')
        try:
            visualize_network(output_path)
            info(f'*** Network visualization saved to {output_path}\n')
        except Exception as e:
            info(f'*** Error generating visualization: {e}\n')
    
    # Create topology
    info('*** Creating ULAKNET topology\n')
    net = create_mininet_topology()
    
    # Start network
    info('*** Starting network\n')
    net = start_network(net)
    
    # Perform basic tests
    perform_network_tests(net)
    
    # Run CLI
    info('*** Running CLI\n')
    CLI(net)
    
    # Stop network
    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    main()