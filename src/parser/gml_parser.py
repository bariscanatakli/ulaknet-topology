import xml.etree.ElementTree as ET

def parse_gml(file_path):
    nodes = []
    edges = []
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    for node in root.findall('node'):
        node_id = int(node.get('id'))
        label = node.find('label').text if node.find('label') is not None else None
        longitude = float(node.find('Longitude').text) if node.find('Longitude') is not None else None
        latitude = float(node.find('Latitude').text) if node.find('Latitude') is not None else None
        country = node.find('Country').text if node.find('Country') is not None else None
        nodes.append({
            'id': node_id,
            'label': label,
            'longitude': longitude,
            'latitude': latitude,
            'country': country
        })

    for edge in root.findall('edge'):
        source = int(edge.get('source'))
        target = int(edge.get('target'))
        link_label = edge.find('LinkLabel').text if edge.find('LinkLabel') is not None else None
        edges.append({
            'source': source,
            'target': target,
            'link_label': link_label
        })

    return nodes, edges

def main():
    file_path = '../data/Ulaknet.gml'
    nodes, edges = parse_gml(file_path)
    print("Nodes:", nodes)
    print("Edges:", edges)

if __name__ == "__main__":
    main()