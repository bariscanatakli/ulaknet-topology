#!/usr/bin/env python3

import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from visualization.network_visualizer import visualize_network

if __name__ == '__main__':
    output_path = os.path.join(os.path.dirname(__file__), '..', 'output', 'ulaknet_topology.png')
    visualize_network(output_path)
    print(f"Visualization saved to {output_path}")
