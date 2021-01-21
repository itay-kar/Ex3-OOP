import json


class Node:

    def __init__(self, node_id: int, node_pos: tuple = None):
        self.id = node_id
        self.pos = node_pos

    def __repr__(self):
        return "id: " + str(self.id) + ", pos: " + str(self.pos)


class DiGraph:

    def __init__(self):
        self.Nodes = dict()
        self.in_Edges = dict()
        self.out_Edges = dict()
        self.mc = 0
        self.edge_size = 0

    def v_size(self) -> int:
        return len(self.Nodes.keys())

    def e_size(self) -> int:
        if len(self.in_Edges.values()) == len(self.out_Edges.values()):
            return len(self.in_Edges.values())
        else:
            return -1

    def get_all_v(self) -> dict:
        return self.Nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.in_Edges[id1]

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.out_Edges[id1]

    def get_mc(self) -> int:
        return self.mc

    def add_node(self, id1: int, pos: tuple = None) -> bool:
        if id1 in self.Nodes.keys():
            return False
        else:
            self.Nodes[id1] = Node(id1, pos)
            self.in_Edges[id1] = dict()
            self.out_Edges[id1] = dict()
            self.mc += 1
            return True

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self.Nodes.keys() or id2 not in self.Nodes.keys() or weight < 0 or id1 == id2:
            return False
        self.in_Edges[id2][id1] = weight
        self.out_Edges[id1][id2] = weight
        self.edge_size += 1
        self.mc += 1
        return True

    def remove_edge(self, id1: int, id2: int) -> bool:
        if id1 not in self.Nodes.keys() or id2 not in self.Nodes.keys() \
                or id1 == id2 or id2 not in self.out_Edges[id1].keys() or id1 not in self.in_Edges[id2].keys():
            return False
        del self.in_Edges[id2][id1]
        del self.out_Edges[id1][id2]
        self.edge_size -= 1
        self.mc += 1
        return True

    def toJson(self):
        f = {"Nodes": self.Nodes, "Edges": self.out_Edges}
        return json.dumps(f, sort_keys=True, indent=2, default=lambda o: o.__dict__)

    def __repr__(self):
        return "Graph : " "V: " + str(self.v_size()) + " , Edges : " + str(self.edge_size)
