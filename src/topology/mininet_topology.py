from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
import time
from config.ulaknet_config import NODES, LINKS, HOSTS

def create_mininet_topology():
    """
    Create and return a Mininet topology for ULAKNET based on configuration.
    """
    # Create Mininet instance with TCLink for bandwidth and delay support
    net = Mininet(topo=None, build=False, ipBase='10.0.0.0/8', 
                  host=CPULimitedHost, link=TCLink, controller=OVSController)
    
    # Add controller
    info('*** Adding controller\n')
    c0 = net.addController(name='c0')
    
    # Add switches based on NODES configuration
    info('*** Adding switches\n')
    switches = {}
    switch_count = 0
    for node, attrs in NODES.items():
        switch_count += 1
        # Use canonical switch names (s1, s2, etc.) and store mapping
        switch_name = f's{switch_count}'
        switches[node] = net.addSwitch(switch_name, cls=OVSKernelSwitch, protocols='OpenFlow13')
        info(f'  Added switch {switch_name} for {node} ({attrs["type"]} node)\n')
    
    # Add hosts based on HOSTS configuration
    info('*** Adding hosts\n')
    hosts = {}
    host_count = 0
    for node, num_hosts in HOSTS.items():
        hosts[node] = []
        for i in range(num_hosts):
            host_count += 1
            host_name = f'h{host_count}'
            host_ip = f'10.0.{host_count//256}.{host_count%256}/16'
            host = net.addHost(host_name, cls=Host, ip=host_ip)
            hosts[node].append(host)
            info(f'  Added host {host_name} with IP {host_ip} to {node}\n')
            
            # Connect host to its switch
            net.addLink(host, switches[node])
    
    # Add links between switches based on LINKS configuration
    info('*** Adding links\n')
    for src, dst, attrs in LINKS:
        bw = attrs.get('bandwidth', 10)  # Default bandwidth 10 Mbps
        delay = attrs.get('delay', '5ms')  # Default delay 5ms
        link_type = attrs.get('type', 'standard')
        
        info(f'  Adding {link_type} link {src} <-> {dst} with {bw}Mbps, {delay} delay\n')
        net.addLink(switches[src], switches[dst], bw=bw, delay=delay)
    
    return net

def start_network(net):
    """
    Start the Mininet network with improved connection handling
    """
    net.build()
    
    # Start controller
    info('*** Starting controller\n')
    for controller in net.controllers:
        controller.start()
    
    # Start switches with a small delay between each
    info('*** Starting switches\n')
    for switch in net.switches:
        switch.start([net.controllers[0]])
        time.sleep(0.2)  # Add a small delay between starting each switch
    
    # Enable STP on all switches to prevent forwarding loops
    info('*** Enabling STP on switches\n')
    for switch in net.switches:
        cmd = f'ovs-vsctl set bridge {switch.name} stp_enable=true'
        switch.cmd(cmd)
    
    # Configure IP forwarding
    info('*** Configuring hosts\n')
    
    # Enable IP forwarding on all hosts
    for host in net.hosts:
        host.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    # Configure switches to use the learning controller
    info('*** Setting OpenFlow versions and flow rules\n')
    for switch in net.switches:
        # Use OpenFlow 1.3
        switch.cmd('ovs-vsctl set bridge {} protocols=OpenFlow13'.format(switch.name))
        
        # Add rules to forward ARP traffic and IP traffic
        # These commands help with basic connectivity
        switch.cmd('ovs-ofctl -O OpenFlow13 add-flow {} "priority=1000,arp,actions=FLOOD"'.format(switch.name))
        switch.cmd('ovs-ofctl -O OpenFlow13 add-flow {} "priority=900,ip,actions=NORMAL"'.format(switch.name))
    
    # Wait for network to stabilize
    info('*** Waiting for network to stabilize\n')
    time.sleep(5)  # Longer wait time for STP to converge
    
    # Configure all hosts to know about each other
    info('*** Setting up host routes\n')
    for src_host in net.hosts:
        for dst_host in net.hosts:
            if src_host != dst_host:
                # Add direct route to each host
                src_host.cmd(f'route add -host {dst_host.IP()} dev {src_host.defaultIntf().name}')
    
    # For debugging: show routes on each host
    info('*** Host routing tables\n')
    for host in net.hosts[:2]:  # Show only first few hosts to avoid clutter
        info(f'{host.name} routes:\n')
        info(f'{host.cmd("route -n")}\n')
    
    return net