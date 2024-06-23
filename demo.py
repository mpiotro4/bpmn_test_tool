import networkx as nx
import matplotlib.pyplot as plt

from GraphVisualizer import GraphVisualizer
from TestGenerator import TestGenerator
from bpmn.FeatureGenerator import FeatureGenerator
from bpmn.BpmnWrapper import BpmnWrapper
from xmi.XmiWrapper import XmiWrapper
def run_demo():
    file_path = 'source_data/bankomat.xml'
    xmi_graph = XmiWrapper(file_path)
    graphs = xmi_graph.get_graphs()
    for graph in graphs:
        node_labels = {node: node.name for node in graph.nodes()}
        GraphVisualizer.visualize_graph(graph, node_labels)


def run_graph_join_example():
    G1 = nx.path_graph(5)  # Graf o 5 wierzchołkach (0, 1, 2, 3, 4)
    G2 = nx.path_graph(4)  # Graf o 4 wierzchołkach (0, 1, 2, 3)

    offset = len(G1)

    # Przesunięcie numeracji wierzchołków w G2
    G2 = nx.relabel_nodes(G2, lambda x: x + offset)
    G = nx.compose(G1, G2)
    G.add_edge(2, offset)

    # Dodanie krawędzi łączącej koniec nowego grafu do węzła 3 w G1
    G.add_edge(3, offset + len(G2) - 1)
    pos = nx.spring_layout(G)  # Układ wierzchołków
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, font_size=16)
    plt.show()


def run_bpmn_demo():
    bpmnGraph = BpmnWrapper("source_data/task_process.bpmn")
    # bpmnGraph = BpmnGraph("source_data/diagram_1.bpmn")
    graph = bpmnGraph.get_graph()
    node_labels = {node: node.name for node in graph.nodes()}

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, labels=node_labels, node_size=2000, node_color='skyblue', font_size=10, font_color='black')
    plt.show()

    bpmnGraph.print_all_nodes()
    bpmnGraph.print_all_edges()
    bpmnGraph.print_all_sequence_flows()

    paths = bpmnGraph.get_all_paths()
    FeatureGenerator.generate_feature("output/result.feature", paths)
    TestGenerator.generate_feature("output/result.java", bpmnGraph)

    print("All Paths:")
    for path in paths:
        print(" -> ".join(node.name for node in path))
    bpmnGraph.visualize_all_paths()


def get_first_graph():
    G = nx.DiGraph()

    # Dodawanie krawędzi do grafu (początkowa ścieżka: A -> B)
    G.add_edge('A', 'B')

    # Dodawanie krawędzi do grafu (rozgałęzienie: B -> C oraz B -> D)
    G.add_edge('B', 'C')
    G.add_edge('B', 'D')
    G.add_edge('B', 'G')
    G.add_edge('G', 'E')

    # Dodawanie krawędzi do grafu (połączenie końców: C -> E oraz D -> E)
    G.add_edge('C', 'E')
    G.add_edge('D', 'E')

    G.add_edge('E', 'F')
    return G


def get_second_graph():
    G = nx.DiGraph()

    G.add_edge('1', 'A')
    G.add_edge('A', 'B')
    G.add_edge('B', '2')

    G.add_edge('2', 'C')
    G.add_edge('2', 'D')

    G.add_edge('C', '3')
    G.add_edge('3', '4')
    G.add_edge('4', '5')

    G.add_edge('D', '5')

    G.add_edge('5', 'E')
    G.add_edge('E', 'F')

    return G

def draw_graph_with_highlights(G, common_nodes, unique_nodes, title):
    pos = nx.spring_layout(G)
    node_colors = ['orange' if node in common_nodes else 'red' if node in unique_nodes else 'skyblue' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=16)
    plt.title(title)
    plt.show()

def draw_paths(G, common_nodes, unique_nodes, title):
    paths = list(nx.all_simple_paths(G, source=list(G.nodes)[0], target=list(G.nodes)[-1]))
    for i, path in enumerate(paths):
        subgraph = nx.Graph()
        edges_in_path = list(zip(path, path[1:]))
        subgraph.add_edges_from(edges_in_path)
        draw_graph_with_highlights(subgraph, common_nodes, unique_nodes, f'{title} - Path {i + 1}: {path}')

def highlight_nodes_not_in_B(G_A: nx.Graph, G_B: nx.Graph):
    common_nodes = set(G_A.nodes()).intersection(set(G_B.nodes()))
    unique_nodes_A = set(G_A.nodes()).difference(set(G_B.nodes()))

    node_colors = ['red' if node in unique_nodes_A else 'skyblue' for node in G_A.nodes()]

    pos = nx.spring_layout(G_A)  # Można użyć różnych układów w zależności od potrzeb
    nx.draw(G_A, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=16)
    plt.title('Graph A with nodes not in Graph B highlighted')
    plt.show()

