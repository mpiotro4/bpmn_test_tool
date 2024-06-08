import networkx as nx
import matplotlib.pyplot as plt
from TestGenerator import TestGenerator
from FeatureGenerator import FeatureGenerator
from BpmnGraph import BpmnGraph

if __name__ == "__main__":
    # bpmnGraph = BpmnGraph("task_process.bpmn")
    bpmnGraph = BpmnGraph("diagram_1.bpmn")
    graph = bpmnGraph.get_graph()
    node_labels = {node: node.name for node in graph.nodes()}

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, labels=node_labels, node_size=2000, node_color='skyblue', font_size=10, font_color='black')
    plt.show()

    # bpmnGraph.print_all_nodes()
    # bpmnGraph.print_all_edges()
    # bpmnGraph.print_all_sequence_flows()



    paths = bpmnGraph.get_all_paths()
    FeatureGenerator.generate_feature("result.feature", paths)
    TestGenerator.generate_feature("result.java", bpmnGraph)

    print("All Paths:")
    for path in paths:
        print(" -> ".join(node.name for node in path))
    bpmnGraph.visualize_all_paths()
