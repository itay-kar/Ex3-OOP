import unittest
from src import DiGraph


class DiGraphTest(unittest.TestCase):

    def AddNode(self):
        graph = DiGraph.DiGraph
        pos = "0,0,0"
        graph.add_node(1, pos)
        self.assertEqual(1, graph.v_size())


if __name__ == '__main__':
    unittest.main()
