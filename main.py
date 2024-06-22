from GraphCompatibilityAnalyzer.GraphCompatibilityAnalyzer import GraphCompatibilityAnalyzer
from demo import *

if __name__ == "__main__":
    xmi_graph = XmiGraph('source_data/bankomat_2.xml')
    graphs = xmi_graph.get_graphs()
    graph = xmi_graph.use_cases_wrappers[0].scenario_wrappers[0].get_graph()
    node_labels = {node: node.name for node in graph.nodes()}
    GraphVisualizer.visualize_graph(graph, node_labels)
    # for graph in graphs:
    #     node_labels = {node: node.name for node in graph.nodes()}
    #     GraphVisualizer.visualize_graph(graph, node_labels)

    bpmnGraph = BpmnGraph("source_data/bpmn/autoryzacja_uzytkownika.bpmn")
    graph = bpmnGraph.get_graph()
    node_labels = {node: node.name for node in graph.nodes()}
    GraphVisualizer.visualize_graph(graph, node_labels)

    graph_comparator = GraphCompatibilityAnalyzer()
    print(graph_comparator.calculate_node_compatibility_ratio(graphs[0], graph))

    paths_a = xmi_graph.use_cases_wrappers[0].scenario_wrappers[0].get_paths()
    paths_b = bpmnGraph.get_paths()
    print(graph_comparator.calculate_path_compatibility_ratio(paths_a, paths_b))
    report = graph_comparator.generate_report(graphs[0], graph, paths_a, paths_b)
    with open('output/report.txt', 'w') as file:
        file.write(report)

    report = graph_comparator.generate_markdown_report(graphs[0], graph, paths_a, paths_b)
    with open('output/report.md', 'w') as file:
        file.write(report)
