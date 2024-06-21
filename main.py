from GraphCompatibilityAnalyzer.GraphCompatibilityAnalyzer import GraphCompatibilityAnalyzer
from demo import *

if __name__ == "__main__":
    xmi_graph = XmiGraph('source_data/bankomat.xml')
    graphs = xmi_graph.get_graphs()
    # for graph in graphs:
    node_labels = {node: node.name for node in graphs[3].nodes()}
    GraphVisualizer.visualize_graph(graphs[3], node_labels)

    bpmnGraph = BpmnGraph("source_data/task_process copy.bpmn")
    graph = bpmnGraph.get_graph()
    node_labels = {node: node.name for node in graph.nodes()}
    GraphVisualizer.visualize_graph(graph, node_labels)

    node_labels = {node: node.name for node in graphs[0].nodes()}
    GraphVisualizer.visualize_graph(graphs[0], node_labels)

    graph_comparator = GraphCompatibilityAnalyzer()
    print(graph_comparator.calculate_node_compatibility_ratio(graphs[0], graph))

    paths_a = xmi_graph.use_cases_wrappers[0].scenario_wrappers[0].get_paths()
    paths_b = bpmnGraph.get_all_paths()
    print(graph_comparator.calculate_path_compatibility_ratio(paths_a, paths_b))

    # print(graph_comparator.calculate_compatibility(graphs[0], graph, 0.5))
