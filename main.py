import networkx as nx
import matplotlib.pyplot as plt

from GraphVisualizer import GraphVisualizer
from TestGenerator import TestGenerator
from bpmn.FeatureGenerator import FeatureGenerator
from bpmn.BpmnGraph import BpmnGraph
from xmi.XmiGraph import XmiGraph

if __name__ == "__main__":
    file_path = 'source_data/bankomat.xml'
    xmi_graph = XmiGraph(file_path)
    graphs = xmi_graph.get_graphs()
    for graph in graphs:
        node_labels = {node: node.name for node in graph.nodes()}
        GraphVisualizer.visualize_graph(graph, node_labels)

    G1 = nx.path_graph(5)  # Graf o 5 wierzchołkach (0, 1, 2, 3, 4)
    G2 = nx.path_graph(4)  # Graf o 4 wierzchołkach (0, 1, 2, 3)

    offset = len(G1)

    # Przesunięcie numeracji wierzchołków w G2
    G2 = nx.relabel_nodes(G2, lambda x: x + offset)
    G = nx.compose(G1, G2)
    # G.add_edge(2, offset)

    # Dodanie krawędzi łączącej koniec nowego grafu do węzła 3 w G1
    # G.add_edge(3, offset + len(G2) - 1)
    pos = nx.spring_layout(G)  # Układ wierzchołków
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, font_size=16)
    plt.show()
    # node_labels = {node: node.name for node in xmi_graph.get_graph().nodes()}
    # GraphVisualizer.visualize_graph(xmi_graph.get_graph(), node_labels)

    # bpmnGraph = BpmnGraph("task_process.bpmn")
    # bpmnGraph = BpmnGraph("source_data/diagram_1.bpmn")
    # graph = bpmnGraph.get_graph()
    # node_labels = {node: node.name for node in graph.nodes()}
    #
    # pos = nx.spring_layout(graph)
    # nx.draw(graph, pos, labels=node_labels, node_size=2000, node_color='skyblue', font_size=10, font_color='black')
    # plt.show()

    # bpmnGraph.print_all_nodes()
    # bpmnGraph.print_all_edges()
    # bpmnGraph.print_all_sequence_flows()



    # paths = bpmnGraph.get_all_paths()
    # FeatureGenerator.generate_feature("output/result.feature", paths)
    # TestGenerator.generate_feature("output/result.java", bpmnGraph)
    #
    # print("All Paths:")
    # for path in paths:
    #     print(" -> ".join(node.name for node in path))
    # bpmnGraph.visualize_all_paths()
