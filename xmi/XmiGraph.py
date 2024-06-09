import xml.etree.ElementTree as ET
from itertools import chain
from typing import List
import networkx as nx
from xmi.XmiNode import XmiNode
from xmi.XmiConstants import XmiConstants as XC


class XmiGraph:
    def __init__(self, path):
        self.path = path
        self.use_cases_wrappers = []
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self._create_use_cases(self.root.findall(XC.USE_CASE, XC.XMI_NAMESPACE))

    def get_graphs(self) -> List[nx.DiGraph]:
        return list(chain.from_iterable(use_case_wrapper.get_graphs() for use_case_wrapper in self.use_cases_wrappers))

    def _create_use_cases(self, use_cases):
        self.use_cases_wrappers.extend(UseCaseWrapper(use_case) for use_case in use_cases)


class UseCaseWrapper:
    def __init__(self, use_case):
        self.scenarios = use_case.findall(XC.SCENARIO, XC.XMI_NAMESPACE)
        self.scenario_wrappers = []
        self._create_scenarios()

    def get_graphs(self) -> List[nx.DiGraph]:
        return [scenario_wrapper.get_graph() for scenario_wrapper in self.scenario_wrappers]

    def _create_scenarios(self):
        self.scenario_wrappers.extend(ScenarioWrapper(scenario) for scenario in self.scenarios)


class ScenarioWrapper:
    def __init__(self, scenario):
        self.G = nx.DiGraph()
        self.nodes = []
        self.steps = scenario.findall(XC.STEP, XC.XMI_NAMESPACE)
        self._create_all_nodes()
        self._create_all_edges()

    def get_graph(self) -> nx.DiGraph:
        return self.G

    def _create_all_nodes(self):
        self.nodes.extend(XmiNode(step.attrib.get(XC.GUID), step.attrib.get(XC.NAME)) for step in self.steps)

    def _create_all_edges(self):
        self.G.add_edges_from(zip(self.nodes, self.nodes[1:]))
