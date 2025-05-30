import unittest
from src.parser.gml_parser import parse_gml

class TestGMLParser(unittest.TestCase):

    def setUp(self):
        self.file_path = '../data/Ulaknet.gml'
        self.nodes, self.edges = parse_gml(self.file_path)

    def test_nodes(self):
        self.assertIsInstance(self.nodes, list)
        self.assertGreater(len(self.nodes), 0)
        for node in self.nodes:
            self.assertIn('id', node)
            self.assertIn('label', node)
            self.assertIn('longitude', node)
            self.assertIn('latitude', node)
            self.assertIn('country', node)

    def test_edges(self):
        self.assertIsInstance(self.edges, list)
        self.assertGreater(len(self.edges), 0)
        for edge in self.edges:
            self.assertIn('source', edge)
            self.assertIn('target', edge)
            self.assertIn('link_label', edge)

if __name__ == '__main__':
    unittest.main()