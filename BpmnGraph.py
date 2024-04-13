import xml.etree.ElementTree as ET
import re
import networkx as nx
from matplotlib import pyplot as plt

from BpmnConstants import BpmnConstants as BC
from BpmnNode import BpmnNode
from BpmnNodeFactory import BpmnNodeFactory
from BpmnVisualizer import BpmnVisualizer


class BpmnGraph:
    nodes = []
    namespace = {
        'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL'
    }

    def __init__(self, path):
        self.path = path
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.sequence_flows = self.root.findall(BC.SEQUENCE_FLOW, self.namespace)
        self.user_tasks = self.root.findall(BC.USER_TASK, self.namespace)
        self.exclusive_gateways = self.root.findall(BC.EXCLUSIVE_GATEWAY, self.namespace)
        self.service_tasks = self.root.findall(BC.SERVICE_TASK, self.namespace)
        self.end_event = self.root.findall(BC.END_EVENT, self.namespace)
        self.start_event = self.root.findall(BC.START_EVENT, self.namespace)
        self.G = nx.Graph()
        self._create_all_nodes()
        self._create_all_edges()
        self.process_id = self.root.find(BC.PROCESS, self.namespace).get("id")

    def get_process_id(self):
        return self.process_id

    def get_all_paths(self):
        start_node = self._get_start_node()
        end_node = self._get_end_node()
        all_paths = list(nx.all_simple_paths(self.G, source=start_node, target=end_node))
        return all_paths

    def visualize_all_paths(self):
        all_paths = self.get_all_paths()
        BpmnVisualizer.visualize_paths(self.G, all_paths)

    def _get_start_node(self):
        return self._get_node_by_id(self.start_event[0].get('id'))

    def _get_end_node(self):
        return self._get_node_by_id(self.end_event[0].get('id'))

    def get_graph(self):
        return self.G

    def print_all_sequence_flows(self):
        for flow in self.sequence_flows:
            print(f"Source: {flow.get('sourceRef')}, Target: {flow.get('targetRef')}")
            condition_expression = flow.find(BC.CONDITION_EXPRESSION, self.namespace)
            if condition_expression is not None:
                condition_text = condition_expression.text
                print(condition_text)

    def print_all_nodes(self):
        for node in self.G.nodes:
            print(node)

    def print_all_edges(self):
        for edge in self.G.edges:
            source_node, target_node = edge
            print(f"Edge: {source_node} -> {target_node}")

    def _create_all_edges(self):
        for flow in self.sequence_flows:
            source_node = self._get_node_by_id(flow.get(BC.SOURCE_NODE))
            target_node = self._get_node_by_id(flow.get(BC.TARGET_NODE))
            condition_expression = flow.find(BC.CONDITION_EXPRESSION, self.namespace)
            if condition_expression is not None:
                condition_text = condition_expression.text
                pattern = r"#\{(.*?) == '(.*?)'\}"
                matches = re.findall(pattern, condition_text)
                if matches:
                    var_name, var_value = matches[0]
                    source_node.decision_var = var_name
                    target_node.decision_var = var_name
                    target_node.decision_var_val = var_value

            self.G.add_edge(source_node, target_node)

    def _create_all_nodes(self):
        self._create_start_event_nodes(self.start_event)
        self._create_exclusive_gateways_nodes(self.exclusive_gateways)
        self._create_service_tasks_nodes(self.service_tasks)
        self._create_end_event_nodes(self.end_event)
        self._create_user_task_nodes(self.user_tasks)
        for node in self.nodes:
            self.G.add_node(node)

    def _create_start_event_nodes(self, nodes):
        for node in nodes:
            self.nodes.append(BpmnNodeFactory.create_node(
                node_id=node.get('id'),
                name=node.get('name'),
                node_type=BC.START_EVENT)
            )

    def _create_user_task_nodes(self, nodes):
        for node in nodes:
            self.nodes.append(BpmnNodeFactory.create_node(
                node_id=node.get('id'),
                name=node.get('name'),
                node_type=BC.USER_TASK)
            )

    def _create_exclusive_gateways_nodes(self, nodes):
        for node in nodes:
            self.nodes.append(BpmnNodeFactory.create_node(
                node_id=node.get('id'),
                name=node.get('name'),
                node_type=BC.EXCLUSIVE_GATEWAY)
            )

    def _create_service_tasks_nodes(self, nodes):
        for node in nodes:
            self.nodes.append(BpmnNodeFactory.create_node(
                node_id=node.get('id'),
                name=node.get('name'),
                node_type=BC.SERVICE_TASK)
            )

    def _create_end_event_nodes(self, nodes):
        for node in nodes:
            self.nodes.append(BpmnNodeFactory.create_node(
                node_id=node.get('id'),
                name=node.get('name'),
                node_type=BC.END_EVENT)
            )

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
