# Python file containing a basic implementation of a graph data structure.
from random import random as rand

# Node class to represent each vertex in the graph. Includes a distance to start attribute.
class Node:
    def __init__(self, name):
        self.name = name
        self.edges = {}  # Dictionary to hold edges and their weights

    def add_edge(self, neighbor, weight):
        self.edges[neighbor] = weight

    def get_neighbors(self):
        return self.edges.keys()

# Graph class to represent the entire graph
class Graph:

    # Initialize graph from adjacency matrix if provided
    def __init__(self, matrix=None): 
        self.nodes = {}  # Dictionary to hold nodes by their names

        # Populate graph from adjacency matrix
        if matrix is not None:
            self.nodes = {}
            for i in range(len(matrix)):
                self.add_node("V" + str(i))
            for i in range(len(matrix)):
                for j in range(len(matrix)):
                    if matrix[i][j] != 0:
                        self.add_edge("V" + str(i), "V" + str(j), matrix[i][j])
    
    # Add a node to the graph manually
    def add_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)
    
    # Add an edge between two nodes with a specified weight, creates nodes if they don't exist
    def add_edge(self, from_node, to_node, weight):
        self.add_node(from_node)
        self.add_node(to_node)
        self.nodes[from_node].add_edge(to_node, weight)
        self.nodes[to_node].add_edge(from_node, weight)

    # Getter for the list of node names
    def get_node_names(self):
        return list(self.nodes.keys())

