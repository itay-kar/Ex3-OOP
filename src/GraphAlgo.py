import json
import sys
import random
import math
from DiGraph import DiGraph
import matplotlib.pyplot as plt
from typing import List


class GraphAlgo:

    def __init__(self, g: DiGraph = DiGraph()):
        self.graph = g
        self.node_dist: dict = {}

    def get_graph(self) -> DiGraph:
        return self.graph

    #  function load_from_json , this function load a Directed weighted graph from a json file into a DiGraph object
    # returns True if load succeeded , False o.w.

    def load_from_json(self, file_name: str) -> bool:
        with open(file_name, encoding="utf-8") as f:
            graph_loader = json.load(f)
            loaded_graph = DiGraph()
            for x in graph_loader["Nodes"]:
                if "pos" in x.keys():
                    loaded_graph.add_node(x["id"], x["pos"])
                else:
                    loaded_graph.add_node(x["id"])

            for n in graph_loader["Edges"]:
                loaded_graph.add_edge(n["src"], n["dest"], n["w"])

                self.graph = loaded_graph
        return True

    # this function save a copy of graph details into a json file.

    def save_to_json(self, file_name: str) -> bool:
        with open(file_name, "w+", encoding="utf-8") as file:
            graph_str = self.graph.toJson()
            file.write(graph_str)
            file.close()
            return True

        return False

    # shortest path
    def shortest_path(self, id1: int, id2: int) -> (float, list):
        for x in self.graph.Nodes.keys():
            self.node_dist[x] = self.dijkstra_algo(x, id2)

        if self.node_dist[id1][id2] is sys.maxsize:
            return float('inf'), []

        distance = self.node_dist[id1][id2]
        src = id1
        nodes_route = [src]

        while src != id2:
            for x in self.graph.out_Edges[src].keys():
                if x == id2:
                    nodes_route.append(x)

                    return self.node_dist[id1][id2], nodes_route

                if self.node_dist[x] is not None and \
                        self.node_dist[x][id2] is not sys.maxsize and \
                        math.isclose(distance, self.node_dist[src][x] + self.node_dist[x][id2]):
                    nodes_route.append(x)
                    distance -= self.node_dist[src][x]
                    src = x

        return None

    #    connected_comp

    def connected_component(self, id1: int) -> list:
        scc = [id1]
        for x in self.graph.Nodes.keys():
            self.node_dist[x] = self.dijkstra_algo(x, id1)

        for x in self.graph.Nodes.keys():
            if self.node_dist[id1][x] is not sys.maxsize and \
                    self.node_dist[x][id1] is not sys.maxsize and x not in scc:
                scc.append(x)
        return scc

    # connected_comps
    def connected_components(self) -> List[list]:
        graph_scc: List = []

        for x in self.graph.Nodes.keys():
            k = 0
            for j in range(len(graph_scc)):
                if x in graph_scc[j]:
                    k = 1
            if k != 1:
                graph_scc.insert(x, list(self.connected_component(x)))

        return graph_scc

    # min distance used for dijkstra algo
    def minDistance(self, dist, node_set):

        # Initialize minimum distance for next node
        node_distance = sys.maxsize
        min_key = -1

        # shortest path tree
        for node_key in self.graph.Nodes.keys():
            if dist[node_key] < node_distance and node_set[node_key] is False:
                node_distance = dist[node_key]
                min_key = node_key

        return min_key

    # dijkstra algorithm

    def dijkstra_algo(self, src, dest):
        dist = [sys.maxsize] * len(self.graph.Nodes)
        dist[src] = 0
        node_set = [False] * len(self.graph.Nodes)

        for i in range(len(self.graph.Nodes)):
            u = self.minDistance(dist, node_set)
            if u == -1:
                break

            # Put the minimum distance vertex in the
            # shotest path tree
            node_set[u] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shotest path tree
            for key in self.graph.out_Edges[u].keys():
                if self.graph.out_Edges[u][key] > 0 and \
                        node_set[key] is False and \
                        dist[key] > dist[u] + self.graph.out_Edges[u][key]:
                    dist[key] = dist[u] + self.graph.out_Edges[u][key]

        return dist

    # this part plots the graph details about how it works should be added

    def plot_graph(self) -> None:
        all_nodes = self.graph.get_all_v()
        x = []
        y = []
        for i in all_nodes.values():
            if i.pos is not None:
                x.append(float(i.pos.split(",")[0]))
                y.append(float(i.pos.split(",")[1]))
            else:
                x_random = random.random() + 35.0
                y_random = random.random()
                i.pos = (str(x_random) + "," + str(y_random) + "," + str(0.0))
                x.append(x_random)
                y.append(y_random)

        n = [j for j in all_nodes.keys()]
        fig, ax = plt.subplots()
        ax.scatter(x, y)
        for p, txt in enumerate(n):
            ax.annotate(n[p], (x[p], y[p]))

        for i in all_nodes.keys():
            for j in self.graph.all_out_edges_of_node(i).keys():
                x1_coordinate = float(str(all_nodes.get(i).pos.split(",")[0]))
                y1_coordinate = float(str(all_nodes.get(i).pos.split(",")[1]))
                x2_coordinate = float(str(all_nodes.get(j).pos.split(",")[0]))
                y2_coordinate = float(str(all_nodes.get(j).pos.split(",")[1]))
                plt.arrow(x1_coordinate, y1_coordinate, (x2_coordinate - x1_coordinate),
                          (y2_coordinate - y1_coordinate), length_includes_head=True, width=0.00001,
                          head_width=0.00020, head_length=0.0003, color='Black')

        plt.ylabel("y axis")
        plt.title("OOP_Ex3")
        plt.xlabel("x axis")
        plt.title("My Graph")
        plt.show()
