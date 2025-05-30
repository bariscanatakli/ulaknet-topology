import unittest
from src.topology.mininet_topology import create_mininet_topology
from src.parser.gml_parser import parse_gml

class TestMininetTopology(unittest.TestCase):

    def setUp(self):
        self.file_path = '../data/Ulaknet.gml'
        self.nodes, self.edges = parse_gml(self.file_path)

    def test_create_mininet_topology(self):
        # Test if the topology is created successfully
        net = create_mininet_topology(self.nodes, self.edges)
        self.assertIsNotNone(net)
        self.assertEqual(len(net.nodes), len(self.nodes))
        self.assertEqual(len(net.links), len(self.edges))

    def test_node_attributes(self):
        # Test if node attributes are correctly set
        net = create_mininet_topology(self.nodes, self.edges)
        for node in self.nodes:
            self.assertIn(node['id'], net.nodes)
            self.assertEqual(net.nodes[node['id']].label, node['label'])
            self.assertEqual(net.nodes[node['id']].longitude, node['longitude'])
            self.assertEqual(net.nodes[node['id']].latitude, node['latitude'])
            self.assertEqual(net.nodes[node['id']].country, node['country'])

    def test_edge_attributes(self):
        # Test if edge attributes are correctly set
        net = create_mininet_topology(self.nodes, self.edges)
        for edge in self.edges:
            self.assertIn((edge['source'], edge['target']), net.links)
            self.assertEqual(net.links[(edge['source'], edge['target'])].link_label, edge['link_label'])

if __name__ == '__main__':
    unittest.main()