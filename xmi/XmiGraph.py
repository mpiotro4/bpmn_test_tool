import xml.etree.ElementTree as ET
from itertools import chain

import networkx as nx

from GraphVisualizer import GraphVisualizer
from xmi.XmiNode import XmiNode
import matplotlib.pyplot as plt
from xmi.XmiConstants import XmiConstants as XC


class XmiGraph:
    def __init__(self, path):
        self.path = path
        self.use_cases_wrappers = []
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self._create_use_cases(self.root.findall(XC.USE_CASE, XC.XMI_NAMESPACE))

    def get_graphs(self):
        return list(chain.from_iterable(use_case_wrapper.get_graphs() for use_case_wrapper in self.use_cases_wrappers))

    def _create_use_cases(self, use_cases):
        for use_case in use_cases:
            self.use_cases_wrappers.append(UseCaseWrapper(use_case))


class UseCaseWrapper:
    def __init__(self, use_case):
        self.scenarios = use_case.findall(XC.SCENARIO, XC.XMI_NAMESPACE)
        self.scenario_wrappers = []
        self._create_scenarios()

    def get_graphs(self):
        return [scenario_wrapper.get_graph() for scenario_wrapper in self.scenario_wrappers]

    def _create_scenarios(self):
        for scenario in self.scenarios:
            self.scenario_wrappers.append(ScenarioWrapper(scenario))


class ScenarioWrapper:
    def __init__(self, scenario):
        self.G = nx.DiGraph()
        self.nodes = []
        self.steps = scenario.findall(XC.STEP, XC.XMI_NAMESPACE)
        self._create_all_nodes()
        self._create_all_edges()

    def get_graph(self):
        return self.G

    def _create_steps(self):
        for step in self.steps:
            self.nodes.append(XmiNode(step.attrib.get(XC.GUID), step.attrib.get(XC.NAME)))

    def _create_all_nodes(self):
        for step in self.steps:
            self.nodes.append(XmiNode(step.attrib.get('guid'), step.attrib.get('name')))

    def _create_all_edges(self):
        for i in range(len(self.nodes) - 1):
            self.G.add_edge(self.nodes[i], self.nodes[i + 1])
