import networkx as nx
from matplotlib import pyplot as plt


class GraphVisualizer:
    @staticmethod
    def visualize_graph(graph, node_labels):
        plt.close('all')

        # Zwiększ rozmiar figury
        # plt.figure(figsize=(20, 20))

        # Użyj układu sprężynowego z dostosowanymi parametrami
        # pos = nx.spring_layout(graph, k=0.25, iterations=25)
        pos = nx.spring_layout(graph)
        # Rysuj graf
        nx.draw(graph, pos, labels=node_labels, node_size=500, node_color="skyblue", font_size=10, font_color="black")

        # Pokaż wykres
        plt.show()

    @staticmethod
    def visualize_paths(graph, paths):
        if not paths:
            print("No paths found.")
            return

        pos = nx.spring_layout(graph)

        for path_index, path in enumerate(paths, start=1):
            plt.figure(figsize=(8, 6))

            path_subgraph = graph.subgraph(path).copy()

            node_labels = {node: node.name for node in graph.nodes()}
            nx.draw(graph, pos, node_size=500, node_color='lightblue', font_size=8, labels=node_labels)
            nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(), edge_color='gray', alpha=0.5)

            path_node_labels = {node: node.name for node in path_subgraph.nodes()}
            nx.draw(path_subgraph, pos, node_size=500, node_color='red', font_size=8,
                    edge_color='red', width=2, labels=path_node_labels)

            plt.title(f"Path {path_index}")
            plt.show()
