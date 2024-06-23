from GraphCompatibilityAnalyzer.GraphCompatibilityAnalyzer import generate_reports
from demo import *

if __name__ == "__main__":
    xmi_graph = XmiGraph('source_data/bankomat_2.xml')
    graphs = xmi_graph.get_graphs()
    graph = xmi_graph.use_cases_wrappers[1].scenario_wrapper.get_graph()
    node_labels = {node: node.name for node in graph.nodes()}
    # GraphVisualizer.visualize_graph(graph, node_labels)

    # for graph in graphs:
    #     node_labels = {node: node.name for node in graph.nodes()}
    #     GraphVisualizer.visualize_graph(graph, node_labels)

    bpmnGraphs = []
    bpmnFilesPaths = ["source_data/bpmn/autoryzacja_uzytkownika.bpmn", "source_data/bpmn/Wplata.bpmn"]
    for bpmnFilePath in bpmnFilesPaths:
        bpmnGraphs.append(BpmnGraph(bpmnFilePath))

    bpmn_graph_1 = bpmnGraphs[0]
    bpmn_graph_2 = bpmnGraphs[1]
    node_labels = {node: node.name for node in bpmn_graph_2.get_graph().nodes()}
    # GraphVisualizer.visualize_graph(bpmn_graph_2.get_graph(), node_labels)

    paths_a = xmi_graph.use_cases_wrappers[0].scenario_wrapper.get_paths()
    paths_b = bpmn_graph_1.get_paths()

    tuple1 = (xmi_graph.use_cases_wrappers[0], bpmnGraphs[0])
    tuple2 = (xmi_graph.use_cases_wrappers[1], bpmnGraphs[1])
    tuple_list = [tuple1, tuple2]
    generate_reports(tuple_list)
