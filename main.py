import networkx as nx
import matplotlib.pyplot as plt  # For visualization (optional)

from BpmnGraph import BpmnGraph

# Create a graph
G = nx.DiGraph()

# Add edges to the graph
G.add_edge('A', 'B')
G.add_edge('A', 'C')
G.add_edge('B', 'C')
G.add_edge('C', 'D')
G.add_edge('A', 'D')

# Find all simple paths from 'A' to 'D'
start_node = 'A'
end_node = 'D'
all_paths = list(nx.all_simple_paths(G, source=start_node, target=end_node))

# Example usage:
if __name__ == "__main__":
    # # Print all paths
    # print(f"All paths from {start_node} to {end_node}:")
    # for path in all_paths:
    #     print(" -> ".join(path))
    #

    bpmnGraph = BpmnGraph("process_graph.bpmn")
    graph = bpmnGraph.get_graph()
    node_labels = {node: node.name for node in graph.nodes()}  # Use 'name' attribute as node labels
    pos = nx.spring_layout(graph)  # Positioning of nodes
    nx.draw(graph, pos, labels=node_labels, node_size=2000, node_color='skyblue', font_size=10, font_color='black')
    plt.show()

    bpmnGraph.print_all_nodes()
    bpmnGraph.print_all_edges()

    paths = bpmnGraph.get_all_paths()
    print("All Paths:")
    for path in paths:
        print(" -> ".join(node.name for node in path))
    bpmnGraph.visualize_all_paths()
