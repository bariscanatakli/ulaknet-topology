#!/bin/bash

echo "Generating ULAKNET topology visualization..."
cd ../src
python3 -c "from visualization.network_visualizer import visualize_network; visualize_network('../output/ulaknet_topology.png')"
echo "Visualization saved to output/ulaknet_topology.png"
