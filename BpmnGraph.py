import xml.etree.ElementTree as ET

import networkx as nx
from matplotlib import pyplot as plt

from BpmnNode import BpmnNode


class BpmnGraph:
    SEQUENCE_FLOW = './/bpmn:sequenceFlow'
    USER_TASK = './/bpmn:userTask'
    EXCLUSIVE_GATEWAY = './/bpmn:exclusiveGateway'
    SERVICE_TASK = './/bpmn:serviceTask'
    END_EVENT = './/bpmn:endEvent'
    START_EVENT = './/bpmn:startEvent'
    TARGET_NODE = 'targetRef'
    SOURCE_NODE = 'sourceRef'
    nodes = []
    namespace = {
        'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL'
    }

    def __init__(self, path):
        self.path = path
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.sequence_flows = self.root.findall(BpmnGraph.SEQUENCE_FLOW, self.namespace)
        self.user_tasks = self.root.findall(BpmnGraph.USER_TASK, self.namespace)
        self.exclusive_gateways = self.root.findall(BpmnGraph.EXCLUSIVE_GATEWAY, self.namespace)
        self.service_tasks = self.root.findall(BpmnGraph.SERVICE_TASK, self.namespace)
        self.end_event = self.root.findall(BpmnGraph.END_EVENT, self.namespace)
        self.start_event = self.root.findall(BpmnGraph.START_EVENT, self.namespace)
        self.G = nx.Graph()
        self._create_all_nodes()
        self._create_all_edges()

    def get_all_paths(self):
        start_node = self._get_start_node()
        end_node = self._get_end_node()
        all_paths = list(nx.all_simple_paths(self.G, source=start_node, target=end_node))
        return all_paths

    def visualize_all_paths(self):
        all_paths = self.get_all_paths()
        if not all_paths:
            print("No paths found.")
            return

        pos = nx.spring_layout(self.G)  # Layout algorithm for visualization

        for path_index, path in enumerate(all_paths, start=1):
            plt.figure(figsize=(8, 6))

            # Create a subgraph containing only nodes and edges in the current path
            path_subgraph = self.G.subgraph(path).copy()

            # Draw all nodes and edges in the main graph (non-path elements)
            node_labels = {node: node.name for node in self.G.nodes()}  # Use node names as labels
            nx.draw(self.G, pos, node_size=500, node_color='lightblue', font_size=8, labels=node_labels)
            nx.draw_networkx_edges(self.G, pos, edgelist=self.G.edges(), edge_color='gray', alpha=0.5)

            # Draw nodes and edges in the current path with different styles
            path_node_labels = {node: node.name for node in path_subgraph.nodes()}  # Use node names as labels
            nx.draw(path_subgraph, pos, node_size=500, node_color='red', font_size=8,
                    edge_color='red', width=2, labels=path_node_labels)

            plt.title(f"Path {path_index}")
            plt.show()

    def _get_start_node(self):
        return self._get_node_by_id(self.start_event[0].get('id'))

    def _get_end_node(self):
        return self._get_node_by_id(self.end_event[0].get('id'))

    def get_graph(self):
        return self.G

    def print_all_sequence_flows(self):
        for flow in self.sequence_flows:
            print(f"Source: {flow.get('sourceRef')}, Target: {flow.get('targetRef')}")

    def print_all_nodes(self):
        for node in self.G.nodes:
            print(node)

    def print_all_edges(self):
        for edge in self.G.edges:
            source_node, target_node = edge
            print(f"Edge: {source_node} -> {target_node}")

    def _create_all_edges(self):
        for flow in self.sequence_flows:
            source_node = self._get_node_by_id(flow.get(self.SOURCE_NODE))
            target_node = self._get_node_by_id(flow.get(self.TARGET_NODE))
            # print(f"Source: {source_node}, Target: {target_node}")
            self.G.add_edge(source_node, target_node)

    def _create_all_nodes(self):
        self._for_all_nodes(function=self._create_nodes)
        for node in self.nodes:
            self.G.add_node(node)

    def _create_nodes(self, nodes):
        for node in nodes:
            self.nodes.append(BpmnNode(node_id=node.get('id'), name=node.get('name')))

    def _print_nodes(self, nodes):
        for node in nodes:
            print(f"id: {node.get('id')}, name: {node.get('name')}")

    def _get_all_sequence_flows(self):
        source_target_refs = [(sf.get('sourceRef'), sf.get('targetRef')) for sf in self.sequence_flows]
        return source_target_refs

    def _for_all_nodes(self, function):
        function(self.user_tasks)
        function(self.exclusive_gateways)
        function(self.service_tasks)
        function(self.end_event)
        function(self.start_event)

    def _get_node_by_id(self, target_id):
        for node in self.nodes:
            if node.id == target_id:
                return node
        return None

    def __del__(self):
        self.sequence_flows.clear()
        self.user_tasks.clear()
        self.exclusive_gateways.clear()
        self.service_tasks.clear()
        self.end_event.clear()
        self.start_event.clear()
        self.G.clear()
        self.nodes.clear()
