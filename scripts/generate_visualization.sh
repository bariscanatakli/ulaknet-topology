#!/bin/bash

echo "Generating enhanced ULAKNET topology visualization on Turkey map..."

# Get the root directory of the project
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Create output directory if it doesn't exist
mkdir -p "$PROJECT_DIR/output"

# Make sure the output directory is writable
chmod -R 777 "$PROJECT_DIR/output"

# Run the visualization script
cd "$PROJECT_DIR/src"
sudo python3 -c "from visualization.network_visualizer import visualize_network; visualize_network('../output/ulaknet_topology.png')"

# Check if the visualization was created
if [ -f "$PROJECT_DIR/output/ulaknet_topology.png" ]; then
    echo "Visualization successfully generated and saved to output/ulaknet_topology.png"
    
    # Fix permissions
    sudo chown mininet:mininet "$PROJECT_DIR/output/ulaknet_topology.png"
    
    # Try to display the image if in a graphical environment
    if command -v display &> /dev/null; then
        echo "Displaying visualization..."
        display "$PROJECT_DIR/output/ulaknet_topology.png" &
    elif command -v xdg-open &> /dev/null; then
        echo "Opening visualization..."
        xdg-open "$PROJECT_DIR/output/ulaknet_topology.png" &
    else
        echo "To view the visualization, open: $PROJECT_DIR/output/ulaknet_topology.png"
    fi
elif [ -f "/tmp/ulaknet_topology.png" ]; then
    echo "Visualization saved to /tmp/ulaknet_topology.png"
    # Copy from temp location to project
    sudo cp "/tmp/ulaknet_topology.png" "$PROJECT_DIR/output/"
    sudo chown mininet:mininet "$PROJECT_DIR/output/ulaknet_topology.png"
    echo "Copied to output/ulaknet_topology.png"
else
    echo "Error: Failed to generate visualization"
fi
