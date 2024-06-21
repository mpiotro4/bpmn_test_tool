from typing import List
import networkx as nx

class GraphCompatibilityAnalyzer:

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

    def calculate_path_compatibility_ratio(self, paths_a: List, paths_b: List) -> float:
        # Pobierz wszystkie ścieżki w grafie A
        compatible_paths = 0

        # Iteracja przez każdą ścieżkę w grafie A
        for path_A in paths_a:
            path_A_set = set(path_A)
            # Sprawdzenie, czy istnieje jakakolwiek ścieżka w grafie B, która zawiera wszystkie węzły z path_A
            for path_B in paths_b:
                if path_A_set.issubset(set(path_B)):
                    compatible_paths += 1
                    break

        # Oblicz współczynnik kompatybilności ścieżek
        ratio = compatible_paths / len(paths_a) if paths_a else 0
        return ratio

