# Collection of test graphs for graph algorithms
import graph

# Example test graphs with explicit edges and weights
def create_test_graph_1():
    g = graph.Graph()
    g.add_edge('A', 'B', 1)
    g.add_edge('A', 'C', 4)
    g.add_edge('B', 'C', 2)
    g.add_edge('B', 'D', 5)
    g.add_edge('C', 'D', 1)
    return g

def create_test_graph_2():
    g = graph.Graph()
    g.add_edge('X', 'Y', 3)
    g.add_edge('X', 'Z', 6)
    g.add_edge('Y', 'Z', 2)
    g.add_edge('Y', 'W', 4)
    g.add_edge('Z', 'W', 1)
    return g

# example test graphs using adjacency matrices
def create_test_graph_3():
    matrix = [
        [0, 2, 0, 1],
        [2, 0, 3, 2],
        [0, 3, 0, 4],
        [1, 2, 4, 0]
    ]
    g = graph.Graph(matrix)
    return g

def create_test_graph_4():
    matrix = [
        [0, 5, 0, 4, 0],
        [5, 0, 3, 0, 0],
        [0, 3, 0, 7, 0],
        [4, 0, 7, 0, 1],
        [0, 0, 0, 1, 0]
    ]
    g = graph.Graph(matrix)
    return g

# Example very big test graph
def create_large_test_graph():
    g = graph.Graph()
    for i in range(20):
        g.add_node(f'V{i}')
    for i in range(20):
        for j in range(i + 1, 20):
            if (j - i) < 9:
                g.add_edge(f'V{i}', f'V{j}', (i + j) % 10 + 1)
    return g

if __name__ == "__main__":
    #g1 = create_test_graph_1()

    #g2 = create_test_graph_2()

    #g3 = create_test_graph_3()

    g4 = create_test_graph_4()

    #large_g = create_large_test_graph()