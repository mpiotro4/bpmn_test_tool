import matplotlib.pyplot as plt
import networkx as nx


class GraphCompatibilityAnalyzer:

    # todo: make it work for xmi graph
    def get_paths(self, G1: nx.Graph):
        start_node = list(G1.nodes)[0]
        end_node = list(G1.nodes)[-1]
        paths = list(nx.all_simple_paths(G1, source=start_node, target=end_node))
        return paths


    def calculate_compatibility(self, G1: nx.Graph, G2: nx.Graph, alfa: float) -> float:
        node_compatibility = self.calculate_node_compatibility_ratio(G1, G2)
        path_compatibility = self.calculate_path_compatibility_ratio(G1, G2)
        return alfa * node_compatibility + (1 - alfa) * path_compatibility

    def calculate_node_compatibility_ratio(self, A: nx.Graph, B: nx.Graph) -> float:
        nodes1 = set(A.nodes)
        nodes2 = set(B.nodes)

        common_nodes = set(A.nodes()).intersection(set(B.nodes()))
        ratio = len(common_nodes) / len(A.nodes())
        return ratio

    def calculate_path_compatibility_ratio(self, A: nx.Graph, B: nx.Graph) -> float:
        # Pobierz wszystkie ścieżki w grafie A
        paths_A = self.get_paths(A)
        compatible_paths = 0

        # Iteracja przez każdą ścieżkę w grafie A
        for path_A in paths_A:
            path_A_set = set(path_A)
            # Sprawdzenie, czy istnieje jakakolwiek ścieżka w grafie B, która zawiera wszystkie węzły z path_A
            paths_B = list(nx.all_simple_paths(B, source=path_A[0], target=path_A[-1]))
            for path_B in paths_B:
                if path_A_set.issubset(set(path_B)):
                    compatible_paths += 1
                    break

        # Oblicz współczynnik kompatybilności ścieżek
        ratio = compatible_paths / len(paths_A) if paths_A else 0
        return ratio

