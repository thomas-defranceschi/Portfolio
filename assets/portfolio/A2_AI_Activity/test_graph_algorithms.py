import graph_collection as test_graphs
from graph_algorithms import *

g1 = test_graphs.create_test_graph_1()
g2 = test_graphs.create_test_graph_2()
g3 = test_graphs.create_test_graph_3()
g4 = test_graphs.create_test_graph_4()
g5 = test_graphs.create_large_test_graph()

start_nodes = ['A', 'X', 'V0', 'V0', 'V0']
end_nodes = ['D', 'Z', 'V3', 'V4', 'V19']

graph_list = [g1, g2, g3, g4, g5]
test_list = []
failed_tests = []
completed_tests = []

class NotImplementedYet(Exception):
    pass

def notify_test_start(test_func):
    print("========================================")
    print("Starting next test : ", test_func.__name__, "\n")

def notify_test_success(test_func):
    print(f"\n{test_func.__name__}: All test cases passed!")
    print("========================================\n")

def report(test_name, case_desc, got, expected):
    status = "PASS" if got == expected else "FAIL"
    print(f"""{test_name}: [{case_desc}] {status} 
    got=     {got} 
    expected={expected}""")

def ensure_return(value, func_name):
    if value is None:
        raise NotImplementedYet(f"{func_name} returned None (not implemented)")
    return value

def a_heuristic(node):
    heuristic_values = {
        "A": 3,"B": 2,"C": 0,"D": 0,
        "X": 5,"Y": 2,"Z": 0,"W": 0,
        "V0": 0,"V1": 1,"V2": 3,"V3": 0,"V4": 0,
        "V5": 6,"V6": 4,"V7": 3,"V8": 2,"V9": 1,
        "V10": 2,"V11": 0,"V12": 1,"V13": 2,"V14": 3,
        "V15": 4,"V16": 4,"V17": 3,"V18": 2,"V19": 0,
    }
    return heuristic_values.get(node, float('inf'))

def test_d_create_distance_dict():
    global start_nodes
    expected_dicts = [
        {'A': 0, 'B': float('inf'), 'C': float('inf'), 'D': float('inf')},
        {'X': 0, 'Y': float('inf'), 'Z': float('inf'), 'W': float('inf')},
        {'V0': 0, 'V1': float('inf'), 'V2': float('inf'), 'V3': float('inf')},
        {'V0': 0, 'V1': float('inf'), 'V2': float('inf'), 'V3': float('inf'), 'V4': float('inf')},
        {'V0': 0, 'V1': float('inf'), 'V2': float('inf'), 'V3': float('inf'), 'V4': float('inf'),
         'V5': float('inf'), 'V6': float('inf'), 'V7': float('inf'), 'V8': float('inf'), 'V9': float('inf'),
         'V10': float('inf'), 'V11': float('inf'), 'V12': float('inf'), 'V13': float('inf'), 'V14': float('inf'),
         'V15': float('inf'), 'V16': float('inf'), 'V17': float('inf'), 'V18': float('inf'), 'V19': float('inf')}
    ]
    for idx, (g, start, expected) in enumerate(zip(graph_list, start_nodes, expected_dicts), 1):
        dist_dict = ensure_return(d_create_distance_dict(g, start), "d_create_distance_dict")
        report("test_d_create_distance_dict", f"graph {idx} start {start}", dist_dict, expected)
        if dist_dict != expected:
            return False
    return True
test_list.append(test_d_create_distance_dict)

def test_d_create_unvisited_node_list():
    global start_nodes
    expected_unvisited = [
        {'B', 'C', 'D'},
        {'Y', 'Z', 'W'},
        {'V1', 'V2', 'V3'},
        {'V1', 'V2', 'V3', 'V4'},
        {'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19'}
    ]
    for idx, (g, start, expected) in enumerate(zip(graph_list, start_nodes, expected_unvisited), 1):
        unvisited = ensure_return(d_create_unvisited_node_list(g, start), "d_create_unvisited_node_list")
        unvisited_set = set(unvisited)
        report("test_d_create_unvisited_node_list", f"graph {idx} start {start}", unvisited_set, expected)
        if unvisited_set != expected:
            return False
    return True
test_list.append(test_d_create_unvisited_node_list)

def test_d_create_previous_node_dict():
    expected_dicts = [
        {'A': None, 'B': None, 'C': None, 'D': None},
        {'X': None, 'Y': None, 'Z': None, 'W': None},
        {'V0': None, 'V1': None, 'V2': None, 'V3': None},
        {'V0': None, 'V1': None, 'V2': None, 'V3': None, 'V4': None},
        {'V0': None, 'V1': None, 'V2': None, 'V3': None, 'V4': None,
         'V5': None, 'V6': None, 'V7': None, 'V8': None, 'V9': None,
         'V10': None, 'V11': None, 'V12': None, 'V13': None, 'V14': None,
         'V15': None, 'V16': None, 'V17': None, 'V18': None, 'V19': None}
    ]
    for idx, (g, expected) in enumerate(zip(graph_list, expected_dicts), 1):
        prev_dict = ensure_return(d_create_previous_node_dict(g), "d_create_previous_node_dict")
        report("test_d_create_previous_node_dict", f"graph {idx}", prev_dict, expected)
        if prev_dict != expected:
            return False
    return True

test_list.append(test_d_create_previous_node_dict)

def test_d_select_next_node():
    global start_nodes
    for idx, (g, start) in enumerate(zip(graph_list, start_nodes), 1):
        dist_dict = ensure_return(d_create_distance_dict(g, start), "d_create_distance_dict")
        unvisited = ensure_return(d_create_unvisited_node_list(g, start), "d_create_unvisited_node_list")
        for node in unvisited:
            if node in g.nodes[start].edges:
                dist_dict[node] = g.nodes[start].edges[node]
        expected_node = min(unvisited, key=lambda n: dist_dict[n])
        node = ensure_return(d_select_next_node(unvisited, dist_dict), "d_select_next_node")
        report("test_d_select_next_node", f"graph {idx} start {start}", node, expected_node)
        if node != expected_node:
            return False
    return True

test_list.append(test_d_select_next_node)

def test_d_update_distances():
    global start_nodes
    expected_updated = [
        {'A': 0, 'B': 1, 'C': 4, 'D': float('inf')},
        {'X': 0, 'Y': 3, 'Z': 6, 'W': float('inf')},
        {'V0': 0, 'V1': 2, 'V2': float("inf"), 'V3': 1},
        {'V0': 0, 'V1': 5, 'V2': float('inf'), 'V3': 4, 'V4': float('inf')},
        {'V0': 0, 'V1': 2, 'V2': 3, 'V3': 4, 'V4': 5,
         'V5': 6, 'V6': 7, 'V7': 8, 'V8': 9, 'V9': float('inf'),
         'V10': float('inf'), 'V11': float('inf'), 'V12': float('inf'), 'V13': float('inf'), 'V14': float('inf'),
         'V15': float('inf'), 'V16': float('inf'), 'V17': float('inf'), 'V18': float('inf'), 'V19': float('inf')}
    ]
    for idx, (g, start, expected) in enumerate(zip(graph_list, start_nodes, expected_updated), 1):
        dist_dict = ensure_return(d_create_distance_dict(g, start), "d_create_distance_dict")
        unvisited = ensure_return(d_create_unvisited_node_list(g, start), "d_create_unvisited_node_list")
        previous_node_dict = ensure_return(d_create_previous_node_dict(g), "d_create_previous_node_dict")
        updated = ensure_return(d_update_distances(g, start, dist_dict, unvisited, previous_node_dict), "d_update_distances")
        report("test_d_update_distances", f"graph {idx} start {start}", updated, expected)
        if updated != expected:
            return False
    return True

test_list.append(test_d_update_distances)

def test_d_completion_reached():
    global end_nodes
    simulated_distance_dicts = [
        {'A': 0, 'B': 1, 'C': 2, 'D': 3},
        {'X': 0, 'Y': float('inf'), 'Z': float('inf'), 'W': float('inf')},
        {'V0': 0, 'V1': 2, 'V2': float('inf'), 'V3': float('inf')},
        {'V0': 0, 'V1': 5, 'V2': float('inf'), 'V3': float('inf'), 'V4': float('inf')},
        {'V0': 0, 'V1': 2, 'V2': 3, 'V3': 4, 'V4': 5,
         'V5': 6, 'V6': 7, 'V7': 8, 'V8': 9, 'V9': float('inf'),
         'V10': float('inf'), 'V11': float('inf'), 'V12': float('inf'), 'V13': float('inf'), 'V14': float('inf'),
         'V15': float('inf'), 'V16': float('inf'), 'V17': float('inf'), 'V18': float('inf'), 'V19': float('inf')}
    ]
    simulated_unvisited_lists = [
        [],
        ['X', 'Z', 'W'],
        ['V2', 'V3'],
        ['V1', 'V2', 'V3'],
        ['V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19']
    ]
    expected_results = [True, False, True, True, False]
    for idx, (end, dist_dict, unvisited, expected) in enumerate(zip(end_nodes, simulated_distance_dicts, simulated_unvisited_lists, expected_results), 1):
        result = ensure_return(d_completion_reached(end, dist_dict, unvisited), "d_completion_reached")
        report("test_d_completion_reached", f"graph {idx} end {end}", result, expected)
        if result != expected:
            return False
    return True

test_list.append(test_d_completion_reached)

def test_d_trace_back_path():
    global start_nodes
    global end_nodes
    previous_dicts = [
        {'A': None, 'B': 'A', 'C': 'B', 'D': 'C', 'E': 'D'},
        {'X': None, 'Y': 'X', 'Z': 'Y'},
        {'V0': None, 'V1': 'V0', 'V2': 'V1', 'V3': 'V1'},
        {'V0': None, 'V1': 'V0', 'V2': 'V1', 'V3': 'V1', 'V4': 'V2'},
        {'V0': None, 'V1': 'V0', 'V2': 'V1', 'V3': 'V2', 'V4': 'V3', 'V5': 'V4',
         'V6': 'V5', 'V7': 'V6', 'V8': 'V7', 'V9': 'V3', 'V10': 'V9',
         'V11': 'V10', 'V12': 'V11', 'V13': 'V12', 'V14': 'V9', 'V15': 'V14',
         'V16': 'V15', 'V17': 'V14', 'V18': 'V17', 'V19': 'V17'}
    ]
    expected_paths = [
        ['A', 'B', 'C', 'D'],
        ['X', 'Y', 'Z'],
        ['V0', 'V1', 'V3'],
        ['V0', 'V1', 'V2', 'V4'],
        ['V0', 'V1', 'V2', 'V3', 'V9', 'V14', 'V17', 'V19']
    ]
    for idx, (start, end, prev_dict, expected) in enumerate(zip(start_nodes, end_nodes, previous_dicts, expected_paths), 1):
        path = ensure_return(d_trace_back_path(start, end, prev_dict), "d_trace_back_path")
        report("test_d_trace_back_path", f"simulation {idx} start {start} end {end}", path, expected)
        if path != expected:
            return False
    return True

test_list.append(test_d_trace_back_path)

def test_dijkstra():
    global graph_list
    global start_nodes
    global end_nodes
    expected_distances = [
        4,
        5,
        1,
        5,
        5,
    ]
    expected_paths = [
        ['A', 'B', 'C', 'D'],
        ['X', 'Y', 'Z'],
        ['V0', 'V3'],
        ['V0', 'V3', 'V4'],
        ['V0', 'V1', 'V9', 'V11', 'V19']
    ]
    expected_results = [[dist, path] for dist, path in zip(expected_distances, expected_paths)]
    for idx, (g, start, end, expected) in enumerate(zip(graph_list, start_nodes, end_nodes, expected_results), 1):
        path = ensure_return(dijkstra(g, start, end), "dijkstra")
        report("test_dijkstra", f"graph {idx} start {start} end {end}", path, expected)
        if path != expected:
            return False
    return True

test_list.append(test_dijkstra)

def test_a_create_open_set():
    global start_nodes, graph_list
    expected_sets = [
        ['A'],
        ['X'],
        ['V0'],
        ['V0'],
        ['V0']
    ]
    for idx, (graph, start, expected) in enumerate(zip(graph_list, start_nodes, expected_sets), 1):
        open_set = ensure_return(a_create_open_set(graph, start), "a_create_open_set")
        report("test_a_create_open_set", f"graph {idx} start {start}", open_set, expected)
        if open_set != expected:
            return False
    return True

test_list.append(test_a_create_open_set)

def test_a_create_closed_set():
    global graph_list
    expected_sets = [
        [],
        [],
        [],
        [],
        []
    ]
    for idx, (graph, expected) in enumerate(zip(graph_list, expected_sets), 1):
        closed_set = ensure_return(a_create_closed_set(graph), "a_create_closed_set")
        report("test_a_create_closed_set", f"graph {idx}", closed_set, expected)
        if closed_set != expected:
            return False
    return True

test_list.append(test_a_create_closed_set)

def test_a_create_g_dict():
    global start_nodes, graph_list
    expected_dicts = [
        {'A': 0, 'B': float('inf'), 'C': float('inf'), 'D': float('inf')},
        {'X': 0, 'Y': float('inf'), 'Z': float('inf'), 'W': float('inf')},
        {'V0': 0, 'V1': float('inf'), 'V2': float('inf'), 'V3': float('inf')},
        {'V0': 0, 'V1': float('inf'), 'V2': float('inf'), 'V3': float('inf'), 'V4': float('inf')},
        {'V0': 0, 'V1': float('inf'), 'V2': float('inf'), 'V3': float('inf'), 'V4': float('inf'),
         'V5': float('inf'), 'V6': float('inf'), 'V7': float('inf'), 'V8': float('inf'), 'V9': float('inf'),
         'V10': float('inf'), 'V11': float('inf'), 'V12': float('inf'), 'V13': float('inf'), 'V14': float('inf'),
         'V15': float('inf'), 'V16': float('inf'), 'V17': float('inf'), 'V18': float('inf'), 'V19': float('inf')}
    ]
    for idx, (g, start, expected) in enumerate(zip(graph_list, start_nodes, expected_dicts), 1):
        g_dict = ensure_return(a_create_g_dict(g, start), "a_create_g_dict")
        report("test_a_create_g_dict", f"graph {idx} start {start}", g_dict, expected)
        if g_dict != expected:
            return False
    return True

test_list.append(test_a_create_g_dict)

def test_a_create_came_from_dict():
    global graph_list
    expected_dicts = [
        {'A': None, 'B': None, 'C': None, 'D': None},
        {'X': None, 'Y': None, 'Z': None, 'W': None},
        {'V0': None, 'V1': None, 'V2': None, 'V3': None},
        {'V0': None, 'V1': None, 'V2': None, 'V3': None, 'V4': None},
        {'V0': None, 'V1': None, 'V2': None, 'V3': None, 'V4': None,
         'V5': None, 'V6': None, 'V7': None, 'V8': None, 'V9': None,
         'V10': None, 'V11': None, 'V12': None, 'V13': None, 'V14': None,
         'V15': None, 'V16': None, 'V17': None, 'V18': None, 'V19': None}
    ]
    for idx, (g, expected) in enumerate(zip(graph_list, expected_dicts), 1):
        came_from = ensure_return(a_create_came_from_dict(g), "a_create_came_from_dict")
        report("test_a_create_came_from_dict", f"graph {idx}", came_from, expected)
        if came_from != expected:
            return False
    return True

test_list.append(test_a_create_came_from_dict)

def test_a_select_lowest_f_score_node():
    # Fabricated scenarios with varied f = g + h scores (not always first node)
    scenarios = [
        ("g1", ['A', 'B', 'C'], {'A': 2, 'B': 1, 'C': 4}, 'B'),           # B: 1+2=3 < A:5 < C:4
        ("g2", ['X', 'Y', 'Z'], {'X': 0, 'Y': 1, 'Z': 2}, 'Z'),            # Z: 2+0=2 < Y:3 < X:5
        ("g3", ['V0', 'V1', 'V2', 'V3'], {'V0': 5, 'V1': 2, 'V2': 4, 'V3': 1}, 'V3'),  # V3:1+0=1
        ("g4", ['V0', 'V3', 'V4'], {'V0': 4, 'V3': 2, 'V4': 1}, 'V4'),    # V4:1+0=1 last in list
        ("g5", ['V9', 'V11', 'V14', 'V17', 'V19'], {'V9': 3, 'V11': 5, 'V14': 0, 'V17': 1, 'V19': 2}, 'V19')
        # V19:2+0=2 < V14:0+3=3 < V9:4 < V17:4 < V11:5
    ]
    for idx, (label, open_set, g_dict, expected) in enumerate(scenarios, 1):
        node = ensure_return(a_select_lowest_f_score_node(open_set, g_dict, a_heuristic, end_nodes[idx-1]), "a_select_lowest_f_score_node")
        report("test_a_select_lowest_f_score_node", f"scenario {idx} {label}", node, expected)
        if node != expected:
            return False
    return True

test_list.append(test_a_select_lowest_f_score_node)

def test_a_compute_tentative_g_score():
    scenarios = [
        ("g1", 'A', 'B', {'A': 0, 'B': 1}, 1),  # A->B cost 1
        ("g2", 'X', 'Y', {'X': 0, 'Y': 3}, 3),  # X->Y cost 3
        ("g3", 'V0', 'V3', {'V0': 0, 'V3': 1}, 1),  # V0->V3 cost 1
        ("g4", 'V0', 'V3', {'V0': 0, 'V3': 5}, 4),  # V0->V3 cost 4
        ("g5", 'V0', 'V1', {'V0': 0, 'V1': 2}, 2)   # V0->V1 cost 2
    ]
    for idx, (label, current, neighbor, g_dict, expected) in enumerate(scenarios, 1):
        tentative_g = ensure_return(a_compute_tentative_g_score(current, neighbor, g_dict, graph_list[idx-1]), "a_compute_tentative_g_score")
        report("test_a_compute_tentative_g_score", f"scenario {idx} {label}", tentative_g, expected)
        if tentative_g != expected:
            return False
    return True

test_list.append(test_a_compute_tentative_g_score)

def test_a_update_scores():
    # Scenario tuple fields:
    # (label, current, neighbor, g_dict, came_from, graph, open_set,
    #  expected_g, expected_open_set, expected_came_from)
    scenarios = [
        # Update needed: neighbor g = inf; should set to cost and add to open_set
        ("update_inf", 'A', 'B',
         {'A': 0, 'B': float('inf')}, {}, graph_list[0], [],
         1, ['B'], {'B': 'A'}),
        # No update: existing g lower than tentative (tentative 3 > existing 2)
        ("no_update_lower_exists", 'X', 'Y',
         {'X': 0, 'Y': 2}, {}, graph_list[1], [],
         2, [], {}),
        # No update: equality (tentative 4 == existing 4) should not change or add
        ("no_update_equal", 'A', 'C',
         {'A': 0, 'C': 4}, {}, graph_list[0], [],
         4, [], {}),
        # Update with neighbor already in open_set: g improves; no duplicate added
        ("update_already_in_open", 'V0', 'V1',
         {'V0': 0, 'V1': 10}, {}, graph_list[4], ['V1'],
         2, ['V1'], {'V1': 'V0'}),
        # Update needed normal case: neighbor g = inf; add to open_set
        ("update_inf_g4", 'V0', 'V3',
         {'V0': 0, 'V3': float('inf')}, {}, graph_list[3], [],
         4, ['V3'], {'V3': 'V0'}),
    ]
    for idx, (label, current, neighbor, g_dict, came_from, graph, open_set,
              expected_g, expected_open_set, expected_came_from) in enumerate(scenarios, 1):
        a_update_scores(current, neighbor, g_dict, came_from, graph, open_set)
        got_g = g_dict[neighbor]
        report("test_a_update_scores", f"scenario {idx} {label} g_score", got_g, expected_g)
        if got_g != expected_g:
            return False
        report("test_a_update_scores", f"scenario {idx} {label} open_set", open_set, expected_open_set)
        if open_set != expected_open_set:
            return False
        # Filter came_from to only the neighbor for comparison clarity
        neighbor_cf = {neighbor: came_from.get(neighbor)} if neighbor in came_from else {}
        report("test_a_update_scores", f"scenario {idx} {label} came_from", neighbor_cf, expected_came_from)
        if neighbor_cf != expected_came_from:
            return False
    return True

test_list.append(test_a_update_scores)

def test_a_completion_reached():
    scenarios = [
        # Current is end node
        ("current_is_end", 'D', 'D', ['A', 'B'], True),
        # Open set empty
        ("open_set_empty", 'A', 'D', [], True),
        # Neither condition met
        ("neither_condition", 'A', 'D', ['B', 'C'], False),
    ]
    for idx, (label, current, end, open_set, expected) in enumerate(scenarios, 1):
        result = ensure_return(a_completion_reached(current, end, open_set), "a_completion_reached")
        report("test_a_completion_reached", f"scenario {idx} {label}", result, expected)
        if result != expected:
            return False
    return True

test_list.append(test_a_completion_reached)

def test_astar():
    global graph_list
    global start_nodes
    global end_nodes
    expected_distances = [
        4,
        5,
        1,
        5,
        5,
    ]
    expected_paths = [
        ['A', 'B', 'C', 'D'],
        ['X', 'Y', 'Z'],
        ['V0', 'V3'],
        ['V0', 'V3', 'V4'],
        ['V0', 'V1', 'V9', 'V11', 'V19']
    ]
    expected_results = [[dist, path] for dist, path in zip(expected_distances, expected_paths)]
    for idx, (g, start, end, expected) in enumerate(zip(graph_list, start_nodes, end_nodes, expected_results), 1):
        path = ensure_return(astar(g, start, end, a_heuristic), "astar")
        report("test_astar", f"graph {idx} start {start} end {end}", path, expected)
        if path != expected:
            return False
    return True

test_list.append(test_astar)

# Optionally run all tests when this script is executed directly
if __name__ == "__main__":
    for test_func in test_list:
        notify_test_start(test_func)
        try:
            if test_func():
                notify_test_success(test_func)
                completed_tests.append(test_func.__name__)
            else:
                failed_tests.append(test_func.__name__)
        except NotImplementedYet as e:
            print(e)
            break
    print("Completed tests:", completed_tests)
    if failed_tests:
        print("Some tests failed:", failed_tests)
    else:
        print("""

**********************************************
**     All tests passed successfully!")     **
**********************************************

Congratulations on completing your homework!
Remember to submit your code.
              
I also recommend you make some notes about
what you learned while working on these!
""")
    

