import networkx as nx
import matplotlib.pyplot as plt
import os
import sys

# Add the parent directory to the path so we can import the config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.ulaknet_config import NODES, LINKS, HOSTS

def visualize_network(output_path='ulaknet_topology.png'):
    """
    Create a visualization of the ULAKNET topology
    """
    G = nx.Graph()
    
    # Add nodes with attributes
    for node, attrs in NODES.items():
        G.add_node(node, **attrs)
    
    # Add edges with attributes
    for src, dst, attrs in LINKS:
        G.add_edge(src, dst, **attrs)
    
    # Create position layout
    pos = nx.spring_layout(G, k=0.15, iterations=50, seed=42)
    
    # Draw the network
    plt.figure(figsize=(20, 15))
    
    # Draw nodes by type
    core_nodes = [n for n, attrs in NODES.items() if attrs['type'] == 'core']
    regional_nodes = [n for n, attrs in NODES.items() if attrs['type'] == 'regional']
    edge_nodes = [n for n, attrs in NODES.items() if attrs['type'] == 'edge']
    
    nx.draw_networkx_nodes(G, pos, nodelist=core_nodes, node_color='red', 
                          node_size=800, alpha=0.8, label='Core')
    nx.draw_networkx_nodes(G, pos, nodelist=regional_nodes, node_color='blue', 
                          node_size=600, alpha=0.8, label='Regional')
    nx.draw_networkx_nodes(G, pos, nodelist=edge_nodes, node_color='green', 
                          node_size=400, alpha=0.8, label='Edge')
    
    # Draw edges by type
    backbone_edges = [(u, v) for u, v, d in LINKS if d.get('type') == 'backbone']
    distribution_edges = [(u, v) for u, v, d in LINKS if d.get('type') == 'distribution']
    access_edges = [(u, v) for u, v, d in LINKS if d.get('type') == 'access']
    
    nx.draw_networkx_edges(G, pos, edgelist=backbone_edges, width=3, 
                          alpha=0.7, edge_color='red', label='Backbone')
    nx.draw_networkx_edges(G, pos, edgelist=distribution_edges, width=2, 
                          alpha=0.5, edge_color='blue', label='Distribution')
    nx.draw_networkx_edges(G, pos, edgelist=access_edges, width=1, 
                          alpha=0.3, edge_color='green', label='Access')
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
    
    # Add host count annotations
    for node, count in HOSTS.items():
        if count > 0:
            x, y = pos[node]
            plt.text(x, y-0.08, f"({count} hosts)", 
                    horizontalalignment='center', size=10, 
                    bbox=dict(facecolor='white', alpha=0.6))
    
    plt.axis('off')
    plt.title('ULAKNET Network Topology')
    plt.legend(loc='upper right')
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Network visualization has been saved to '{output_path}'")

if __name__ == '__main__':
    # If run directly, generate and save the visualization
    output_dir = os.path.join(os.path.dirname(os.path.dirname(
                 os.path.dirname(os.path.abspath(__file__)))), 'output')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'ulaknet_topology.png')
    visualize_network(output_path)
