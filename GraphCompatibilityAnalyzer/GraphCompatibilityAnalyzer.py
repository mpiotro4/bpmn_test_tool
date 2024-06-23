from typing import List
import networkx as nx

from bpmn.BpmnWrapper import BpmnWrapper
from xmi.UseCaseWrapper import UseCaseWrapper


def calculate_node_compatibility_ratio(G1: nx.Graph, G2: nx.Graph) -> float:
    nodes1 = set(G1.nodes)
    nodes2 = set(G2.nodes)
    common_nodes = nodes1.intersection(nodes2)
    return len(common_nodes) / len(nodes1) if nodes1 else 0


def calculate_path_compatibility_ratio(paths_a: List[List], paths_b: List[List]) -> float:
    compatible_paths = 0

    # Iteracja przez każdą ścieżkę w grafie A
    for path_A in paths_a:
        path_A_set = set(path_A)
        # Sprawdzenie, czy istnieje jakakolwiek ścieżka w grafie B, która zawiera wszystkie węzły z path_A
        for path_B in paths_b:
            if path_A_set.issubset(set(path_B)):
                compatible_paths += 1
                break
    return compatible_paths / len(paths_a) if paths_a else 0


def generate_graph_compatibility_info(G1: nx.Graph, G2: nx.Graph, paths_a: List[List], paths_b: List[List]) -> tuple:
    nodes1 = set(G1.nodes)
    nodes2 = set(G2.nodes)

    common_nodes = nodes1.intersection(nodes2)
    missing_nodes = nodes1.difference(nodes2)

    compatible_paths = []
    missing_paths = []

    for path_A in paths_a:
        path_A_set = set(path_A)
        compatible = False
        for path_B in paths_b:
            if path_A_set.issubset(set(path_B)):
                compatible_paths.append(path_A)
                compatible = True
                break
        if not compatible:
            missing_paths.append(path_A)

    node_compatibility = calculate_node_compatibility_ratio(G1, G2)
    path_compatibility = calculate_path_compatibility_ratio(paths_a, paths_b)

    return common_nodes, missing_nodes, compatible_paths, missing_paths, node_compatibility, path_compatibility


def highlight_missing_path(path: List, original_paths: List[List]) -> str:
    for original_path in original_paths:
        missing_indices = [i for i, node in enumerate(path) if node not in original_path]
        if missing_indices:
            highlighted_path = ""
            for i, node in enumerate(path):
                if i in missing_indices:
                    highlighted_path += f"<span style='color:#ff9999'>{node}</span>"
                else:
                    highlighted_path += str(node)
                if i < len(path) - 1:
                    highlighted_path += " -> "
            return highlighted_path
    return ' -> '.join(map(str, path))


def generate_markdown_report(G1: nx.Graph, G2: nx.Graph, paths_a: List[List], paths_b: List[List]) -> str:
    common_nodes, missing_nodes, compatible_paths, missing_paths, node_compatibility, path_compatibility = generate_graph_compatibility_info(
        G1, G2, paths_a, paths_b)

    report = "# Raport zgodności przypadku użycia UML z procesem biznesowym w notacji BPMN\n\n"
    report += "## Grafy\n"
    report += f"- **G1:** {G1.name}\n"
    report += f"- **G2:** {G2.name}\n"
    report += "\n"

    report += "## Wierzchołki\n"
    report += f"- Liczba wierzchołków G1: **{len(G1.nodes)}**\n"
    report += f"- Liczba wierzchołków G2: **{len(G2.nodes)}**\n"
    report += f"- Liczba wspólnych wierzchołków: **{len(common_nodes)}**\n"
    report += f"- Brakujące wierzchołki w G2: **{len(missing_nodes)}** - " + ', '.join(
        str(node) for node in missing_nodes) + "\n"
    report += "\n"

    report += "## Ścieżki\n"
    report += f"- Liczba ścieżek w G1: **{len(paths_a)}**\n"
    report += f"- Liczba ścieżek w G2: **{len(paths_b)}**\n"
    report += f"- Kompatybilne ścieżki: **{len(compatible_paths)}**\n"
    report += f"- Brakujące ścieżki w G2: **{len(missing_paths)}**\n"
    if missing_paths:
        for path in missing_paths:
            highlighted_path = highlight_missing_path(path, paths_b)
            report += f"  - Ścieżka: {highlighted_path}\n"

    alfa = 0.5
    compatibility_ratio = alfa * node_compatibility + (1 - alfa) * path_compatibility

    report += "## Współczynniki kompatybilności\n"
    report += f"- Współczynnik kompatybilności wierzchołków: **{node_compatibility:.2f}**\n"
    report += f"- Współczynnik kompatybilności ścieżek: **{path_compatibility:.2f}**\n"
    report += f"- Wynikowy współczynnik kompatybilności grafów: **{compatibility_ratio:.2f}**\n"
    report += "\n"

    return report


def generate_report(G1: nx.Graph, G2: nx.Graph, paths_a: List, paths_b: List) -> str:
    common_nodes, missing_nodes, compatible_paths, missing_paths, node_compatibility, path_compatibility = generate_graph_compatibility_info(
        G1, G2, paths_a, paths_b)

    report = f"### Raport zgodności grafów G1 - '{G1.name}' i G2 - '{G2.name}':\n\n"

    report += "#### Wierzchołki:\n"
    report += f"Liczba wierzchołków G1: {len(G1.nodes)}\n"
    report += f"Liczba wierzchołków G2: {len(G2.nodes)}\n"
    report += f"Liczba wspólnych wierzchołków: {len(common_nodes)}\n"
    report += f"Brakujące wierzchołki w G2: {len(missing_nodes)} - {missing_nodes}\n"
    report += "###########################################\n\n"

    report += "#### Ścieżki:\n"
    report += f"Liczba ścieżek w G1: {len(paths_a)}\n"
    report += f"Liczba ścieżek w G2: {len(paths_b)}\n"
    report += f"Kompatybilne ścieżki: {len(compatible_paths)}\n"
    report += f"Brakujące ścieżki w G2: {len(missing_paths)} - {missing_paths}\n"
    report += "###########################################\n\n"

    alfa = 0.5
    compatibility_ratio = alfa * node_compatibility + (1 - alfa) * path_compatibility

    report += "#### Współczynniki kompatybilności:\n"
    report += f"Współczynnik kompatybilności wierzchołków: {node_compatibility:.2f}\n"
    report += f"Współczynnik kompatybilności ścieżek: {path_compatibility:.2f}\n"
    report += f"Wynikowy współczynnik kompatybilności grafów: {compatibility_ratio:.2f}\n"
    report += "###########################################\n"

    return report


def generate_reports(graphs_wrappers: List[tuple[UseCaseWrapper, BpmnWrapper]], generate_txt: bool = False,
                     generate_md: bool = True):
    for wrappers in graphs_wrappers:
        paths_a = wrappers[0].scenario_wrapper.get_paths()
        paths_b = wrappers[1].get_paths()
        graph_a = wrappers[0].scenario_wrapper.get_graph()
        graph_b = wrappers[1].get_graph()

        file_name = graph_a.name + "_" + graph_b.name

        if generate_txt:
            report = generate_report(graph_a, graph_b, paths_a, paths_b)
            with open(f'output/{file_name}.txt', 'w') as file:
                file.write(report)

        if generate_md:
            report = generate_markdown_report(graph_a, graph_b, paths_a, paths_b)
            with open(f'output/{file_name}.md', 'w') as file:
                file.write(report)


def calculate_compatibility(G1: nx.Graph, G2: nx.Graph, path_a, path_b, alfa: float) -> float:
    node_compatibility = calculate_node_compatibility_ratio(G1, G2)
    path_compatibility = calculate_path_compatibility_ratio(path_a, path_b)
    return alfa * node_compatibility + (1 - alfa) * path_compatibility
