import xml.etree.ElementTree as ET
import networkx as nx

from GraphVisualizer import GraphVisualizer
from xmi.XmiNode import XmiNode
import matplotlib.pyplot as plt


class XmiGraph:
    nodes = []

    namespace = {
        'xmi': 'http://schema.omg.org/spec/XMI/2.1'
    }

    def __init__(self, path):
        self.path = path
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.use_cases = self.root.findall('.//element[@xmi:type="uml:UseCase"]', self.namespace)[0]
        self.scenarios = self.use_cases.findall('.//EAScenarioContent', self.namespace)[0]
        self.steps = self.scenarios.findall('.//step')
        self.extensions = self.use_cases.findall('.//extension')
        self.G = nx.DiGraph()
        self._create_all_nodes()
        self._create_all_edges()

    def get_graph(self):
        return self.G

    def _create_all_nodes(self):
        for step in self.steps:
            self.nodes.append(XmiNode(step.attrib.get('guid'), step.attrib.get('name')))

    def _create_all_edges(self):
        for i in range(len(self.nodes) - 1):
            self.G.add_edge(self.nodes[i], self.nodes[i + 1])
