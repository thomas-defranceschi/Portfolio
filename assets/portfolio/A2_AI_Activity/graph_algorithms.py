##########################################################################
# graph_algorithms.py
# This is the file you should write your code in.
# You shouldn't need to modify graph.py or test_graphs.py
# You shouldn't need to modify this file's header either.
# Remember to test intermediate functions as soon as they are written!
##########################################################################

from typing import Callable
from graph import Node, Graph
import test_graphs

##########################################################################
# Dikjstra's Algorithm intermediate functions to implement.
##########################################################################

# Return an initialised dictionary of distances to start.
# Should initialise to infinity if not start and zero if start
def d_create_distance_dict(graph, start_node_name) -> dict:
    # your implementation here
    ...

# Return an initialised list all unvisited nodes.
# Should contain all nodes in graph except the starting node 
def d_create_unvisited_node_list(graph, start_node_name) -> list:
    # your implementation here
    ...

# Return an initialised dictionary of previous nodes in path.
# Should initialised to None for each node.
def d_create_previous_node_dict(graph) -> dict:
    # your implementation here
    ...

# Return the next node to use for step 4-5.
def d_select_next_node(unvisited_list, distance_dict) -> str:
    # your implementation here
    ...

# Updates distance values, visited status, and previous_node according to step 4-5.
def d_update_distances(graph, current_node_name, distance_dict, unvisited_list, previous_node_dict) -> dict:
    # your implementation here
    ...

# Return True if dikjstra completed according to step 6.
def d_completion_reached(end_node, distance_dict, unvisited_list) -> bool:
    # your implementation here
    ...

# Trace back the path, starting from end_node until start_node
def d_trace_back_path(start_node, end_node, previous_node_dict) -> list:
    # your implementation here
    ...

##########################################################################
# Dikjstra's Algorithm. Don't modify the function header.
##########################################################################

def dijkstra(graph : Graph, start_node_name : str, end_node : str ) -> list:
    """
    Implements Dijkstra's algorithm to find the shortest path from start_node_name to end_node.
    
    Parameters:
    graph (Graph): The graph on which to perform the algorithm.
    start_node_name (str): The name of the starting node.
    end_node (str): The name of the ending node.
    
    Returns:
    list: The first element should be the distance of the shortest path,
          and the second element should be a list of node names representing the shortest path.
    """

    # your implementation here
    ...



##########################################################################
# Astar Algorithm intermediate functions to implement.
##########################################################################

# Creates the open set for Astar algorithm
def a_create_open_set(graph, start_node_name) -> list:
    # your implementation here
    ...

# Creates the closed set for Astar algorithm
def a_create_closed_set(graph) -> list:
    # your implementation here
    ...

# Return an initialised dictionary of distances to start.
# Should initialise to infinity if not start and zero if start
def a_create_g_dict(graph, start_node_name) -> dict:
    # your implementation here
    ...

# Return an initialised dictionary of f scores.
# Should initialise to infinity if not start and heuristic(start) if start
def a_create_f_dict(graph, start_node_name, heuristic) -> dict:
    # your implementation here
    ...

# Create the came_from dict for Astar algorithm
# Should initialise to None for each node.
def a_create_came_from_dict(graph) -> dict:
    # your implementation here
    ...

# Select the node in open set with lowest f_score
def a_select_lowest_f_score_node(open_set, g_dict, heuristic, end_node) -> str:
    # your implementation here
    ...

# Computes tentative g_score for a neighbor node
def a_compute_tentative_g_score(current_node_name, neighbor_node_name, g_dict, graph) -> float:
    # your implementation here
    ...

# Updates g_score, f_score, and came_from according to step 4(d) of
# the plain English description
def a_update_scores(current_node_name, neighbor_node_name, g_dict, f_dict, came_from, heuristic, graph) -> None:
    # your implementation here
    ...

# Return True if dikjstra completed according to step 6.
def a_completion_reached(graph, end_node, distance_dict, unvisited_list) -> bool:
    # your implementation here
    ...

##########################################################################
# Astar Algorithm. Don't modify the function header.
##########################################################################

def astar(graph : Graph, start_node_name : str, end_node : str, heuristic : Callable ) -> list:
    """
    Perform A* search on a graph to find a lowest-cost path between two nodes.
    
    Parameters:
    graph (Graph): The graph on which to perform the algorithm.
    start_node_name (str): The name of the starting node.
    end_node (str): The name of the ending node.
    heuristic (callable): A function returning the heuristic value of nodes.
    
    Returns:
    list: The first element should be the distance of the shortest path,
          and the second element should be a list of node names representing the shortest path.
    """

    # Your implementation here
    ...
