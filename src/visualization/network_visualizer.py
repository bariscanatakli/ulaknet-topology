import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import sys
from matplotlib.colors import LinearSegmentedColormap

# Add the parent directory to the path so we can import the config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.ulaknet_config import NODES, LINKS, HOSTS

# Geographical coordinates for Turkish cities (approximate latitude, longitude)
CITY_COORDS = {
    'ANKARA': (39.9334, 32.8597),
    'ISTANBUL': (41.0082, 28.9784),
    'IZMIR': (38.4237, 27.1428),
    'BURSA': (40.1885, 29.0610),
    'ANTALYA': (36.8969, 30.7133),
    'ADANA': (37.0000, 35.3213),
    'TRABZON': (41.0027, 39.7168),
    'ERZURUM': (39.9000, 41.2700),
    'ELAZIG': (38.6810, 39.2264),
    'GAZIANTEP': (37.0594, 37.3822),
    'KAYSERI': (38.7312, 35.4787),
    'KONYA': (37.8667, 32.4833),
    'SAMSUN': (41.2867, 36.3300),
    'DIYARBAKIR': (37.9144, 40.2306),
    'MALATYA': (38.3552, 38.3095),
    'VAN': (38.4891, 43.4089),
    'SIVAS': (39.7477, 37.0179),
    'ESKISEHIR': (39.7767, 30.5206),
    'KOCAELI': (40.7650, 29.9408),
}

def visualize_network(output_path='ulaknet_topology.png'):
    """
    Create a visualization of the ULAKNET topology on a map of Turkey
    """
    # Create the figure with a larger size
    plt.figure(figsize=(24, 18))
    
    # Create a simplified Turkey outline as the background instead of downloading an image
    create_turkey_outline()
    
    # Create a graph
    G = nx.Graph()
    
    # Add nodes with attributes
    for node, attrs in NODES.items():
        # Use geographical coordinates for node positions
        if node in CITY_COORDS:
            attrs['pos'] = CITY_COORDS[node]
        G.add_node(node, **attrs)
    
    # Add edges with attributes
    for src, dst, attrs in LINKS:
        G.add_edge(src, dst, **attrs)
    
    # Create position dictionary for matplotlib
    pos = {node: (CITY_COORDS[node][1], CITY_COORDS[node][0]) for node in G.nodes()}  # Swap lat/lon for display
    
    # Custom colormap for nodes
    node_cmap = LinearSegmentedColormap.from_list('ulaknet_nodes', ['red', 'blue', 'green'])
    
    # Draw nodes by type with improved style and smaller sizes
    core_nodes = [n for n, attrs in NODES.items() if attrs['type'] == 'core']
    regional_nodes = [n for n, attrs in NODES.items() if attrs['type'] == 'regional']
    edge_nodes = [n for n, attrs in NODES.items() if attrs['type'] == 'edge']
    
    # Draw core nodes (reduced size from 1200 to 800)
    nx.draw_networkx_nodes(G, pos, nodelist=core_nodes, node_color='darkred',
                          node_size=800, alpha=0.9, label='Core', 
                          edgecolors='black', linewidths=2)
    
    # Draw regional nodes (reduced size from 800 to 500)
    nx.draw_networkx_nodes(G, pos, nodelist=regional_nodes, node_color='darkblue',
                          node_size=500, alpha=0.9, label='Regional',
                          edgecolors='black', linewidths=1.5)
    
    # Draw edge nodes (reduced size from 600 to 300)
    nx.draw_networkx_nodes(G, pos, nodelist=edge_nodes, node_color='darkgreen',
                          node_size=300, alpha=0.9, label='Edge',
                          edgecolors='black', linewidths=1)
    
    # Draw edges by type with improved styling
    backbone_edges = [(u, v) for u, v, d in LINKS if d.get('type') == 'backbone']
    distribution_edges = [(u, v) for u, v, d in LINKS if d.get('type') == 'distribution']
    access_edges = [(u, v) for u, v, d in LINKS if d.get('type') == 'access']
    
    # Draw backbone links (thickest)
    nx.draw_networkx_edges(G, pos, edgelist=backbone_edges, width=4, 
                          alpha=0.8, edge_color='red', style='solid',
                          label='Backbone (40-100 Mbps)')
    
    # Draw distribution links (medium)
    nx.draw_networkx_edges(G, pos, edgelist=distribution_edges, width=2.5, 
                          alpha=0.7, edge_color='blue', style='solid',
                          label='Distribution (10-20 Mbps)')
    
    # Draw access links (thinnest)
    nx.draw_networkx_edges(G, pos, edgelist=access_edges, width=1.5, 
                          alpha=0.6, edge_color='green', style='dashed',
                          label='Access (5-10 Mbps)')
    
    # Draw node labels with improved appearance
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif',
                           font_weight='bold', font_color='black',
                           bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=6))
    
    # Add host count annotations
    for node, count in HOSTS.items():
        if count > 0:
            x, y = pos[node]
            plt.text(x, y-0.2, f"{count} hosts", horizontalalignment='center',
                    size=8, bbox=dict(facecolor='lightyellow', alpha=0.8, boxstyle='round,pad=0.3'),
                    zorder=100)  # High zorder to ensure it's on top
    
    # Improve plot appearance
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.title('ULAKNET Network Topology on Turkey Map', fontsize=24, fontweight='bold', pad=20)
    
    # Create a more readable legend with better formatting and smaller icons
    # Place it outside the main plot area for better visibility
    legend = plt.legend(
        bbox_to_anchor=(1.02, 1), 
        loc='upper left',
        frameon=True, 
        framealpha=0.95,
        title='Network Components', 
        title_fontsize=14,
        fancybox=True, 
        shadow=True, 
        fontsize=12,
        markerscale=0.7,  # Reduce the size of markers in the legend
        labelspacing=1.2  # Add more vertical space between legend items
    )
    
    # Make the legend background more visible
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('black')
    
    # Adjust figure to make room for the legend
    plt.subplots_adjust(right=0.85)
    
    # Add compass
    add_compass(plt.gca(), position=(0.05, 0.05))
    
    # Add scale bar
    add_scale_bar(plt.gca(), position=(0.05, 0.1))
    
    # Add ULAKNET logo or title
    plt.figtext(0.5, 0.02, 'ULAKNET - Turkish Academic Network', 
               fontsize=14, ha='center', fontweight='bold')
    
    # Ensure output directory exists and is writable
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Make sure we can write to the output file
    try:
        # Test if we can write to the directory
        with open(output_path, 'w') as f:
            f.write('')
    except PermissionError:
        # If permission denied, save to /tmp instead
        original_path = output_path
        output_path = os.path.join('/tmp', os.path.basename(output_path))
        print(f"Permission denied for {original_path}, saving to {output_path} instead")
    
    # Save with high quality
    plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.5)
    plt.close()
    
    print(f"Enhanced network visualization has been saved to '{output_path}'")

def create_turkey_outline():
    """
    Draw a simplified outline of Turkey as a background
    """
    # Approximate outline of Turkey as a polygon (longitude, latitude coordinates)
    turkey_outline = [
        (26.0, 42.0), (29.0, 41.8), (31.0, 41.2), (34.0, 42.1), (36.0, 42.3), (38.0, 40.9),
        (39.0, 41.5), (40.0, 41.1), (41.0, 41.7), (42.5, 41.5), (44.0, 41.0), (44.5, 39.5),
        (44.0, 38.5), (42.0, 37.5), (42.5, 36.5), (41.0, 36.0), (36.0, 36.0), (36.0, 36.5),
        (35.0, 36.0), (34.0, 36.0), (32.0, 36.0), (30.0, 36.0), (29.0, 36.5), (28.0, 36.5),
        (27.0, 36.0), (26.0, 36.0), (26.0, 38.5), (26.0, 40.0), (26.0, 42.0)
    ]
    
    # Extract x, y coordinates
    x_coords = [point[0] for point in turkey_outline]
    y_coords = [point[1] for point in turkey_outline]
    
    # Draw the outline
    plt.fill(x_coords, y_coords, color='lightblue', alpha=0.3)
    plt.plot(x_coords, y_coords, color='navy', linewidth=2, alpha=0.7)
    
    # Set map boundaries
    plt.xlim(25, 45)
    plt.ylim(35, 43)
    
    # Add a light grid for reference
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Add some major water bodies
    # Black Sea
    plt.text(34, 42.5, 'BLACK SEA', fontsize=12, ha='center', color='navy', alpha=0.7)
    # Mediterranean
    plt.text(32, 35.5, 'MEDITERRANEAN SEA', fontsize=12, ha='center', color='navy', alpha=0.7)
    # Aegean Sea
    plt.text(25.5, 38.5, 'AEGEAN\nSEA', fontsize=10, ha='center', color='navy', alpha=0.7)
    # Marmara Sea
    plt.text(28, 40.7, 'MARMARA', fontsize=8, ha='center', color='navy', alpha=0.7)

def download_turkey_map(output_path):
    """
    Try multiple sources for Turkey map or create a basic one
    """
    import urllib.request
    
    print("Attempting to obtain Turkey map...")
    
    # Try multiple URLs for a Turkey map
    map_urls = [
        "https://upload.wikimedia.org/wikipedia/commons/3/3d/Turkey_map.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/BlankMap-Turkey.png/1200px-BlankMap-Turkey.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Turkey_relief_location_map.jpg/1280px-Turkey_relief_location_map.jpg"
    ]
    
    success = False
    for url in map_urls:
        try:
            print(f"Trying to download map from {url}")
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Download the map
            urllib.request.urlretrieve(url, output_path)
            print(f"Turkey map downloaded to {output_path}")
            success = True
            break
        except Exception as e:
            print(f"Could not download map from {url}: {e}")
    
    if not success:
        print("Could not download any Turkey map. Using built-in outline instead.")

def add_compass(ax, position=(0.1, 0.1), size=0.05):
    """Add a compass to the map"""
    x, y = position
    width = size
    
    # Create the compass
    ax.annotate('N', xy=(x, y+width), xycoords='axes fraction',
               ha='center', va='center', fontsize=12, fontweight='bold')
    ax.annotate('S', xy=(x, y-width), xycoords='axes fraction',
               ha='center', va='center', fontsize=12, fontweight='bold')
    ax.annotate('E', xy=(x+width, y), xycoords='axes fraction',
               ha='center', va='center', fontsize=12, fontweight='bold')
    ax.annotate('W', xy=(x-width, y), xycoords='axes fraction',
               ha='center', va='center', fontsize=12, fontweight='bold')
    
    circle = plt.Circle((x, y), width, transform=ax.transAxes,
                       facecolor='white', edgecolor='black', alpha=0.7, zorder=10)
    ax.add_patch(circle)
    
    ax.plot([x, x], [y-width/2, y+width/2], transform=ax.transAxes,
           color='black', linewidth=1, zorder=11)
    ax.plot([x-width/2, x+width/2], [y, y], transform=ax.transAxes,
           color='black', linewidth=1, zorder=11)

def add_scale_bar(ax, position=(0.1, 0.05), width=0.2):
    """Add a scale bar to the map"""
    x, y = position
    
    # Draw scale bar (200km)
    ax.plot([x, x+width], [y, y], transform=ax.transAxes,
           color='black', linewidth=3, solid_capstyle='butt')
    
    # Add distance label
    ax.text(x+width/2, y-0.01, '200 km', transform=ax.transAxes,
           ha='center', va='top', fontsize=10)

if __name__ == '__main__':
    # If run directly, generate and save the visualization
    output_dir = os.path.join(os.path.dirname(os.path.dirname(
                 os.path.dirname(os.path.abspath(__file__)))), 'output')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'ulaknet_topology.png')
    visualize_network(output_path)
