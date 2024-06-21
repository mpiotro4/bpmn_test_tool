from typing import List, Optional

import networkx as nx

from xmi.ExtensionWrapper import ExtensionWrapper
from xmi.XmiNode import XmiNode
from xmi.XmiUtils import transform_id
import xml.etree.ElementTree as ET
from xmi.XmiConstants import XmiConstants as XC


class ScenarioWrapper:
    def __init__(self, scenario: ET.Element):
        self.G = nx.DiGraph()
        self.nodes: List[XmiNode] = []
        self.id = transform_id(scenario.attrib.get(XC.SCHEMA_ID))
        self.extensions_wrappers: List[ExtensionWrapper] = []
        self._create_all_extensions(scenario.findall(XC.EXTENSION, XC.XMI_NAMESPACE))
        self.steps = scenario.findall(XC.STEP, XC.XMI_NAMESPACE)
        self._create_all_nodes()
        self._create_all_edges()
        self.start_node: XmiNode = self.nodes[0]
        self.end_nodes: List[XmiNode] = [self.nodes[-1]]

    def set_graph(self, graph: nx.DiGraph):
        self.G = graph

    def get_graph(self) -> nx.DiGraph:
        return self.G

    def _create_all_nodes(self):
        self.nodes.extend(XmiNode(step.attrib.get(XC.GUID), step.attrib.get(XC.NAME), step.attrib.get(XC.LEVEL))
                          for step in self.steps)
        self.G.add_nodes_from(self.nodes)

    def _create_all_edges(self):
        self.G.add_edges_from(zip(self.nodes, self.nodes[1:]))

    def _create_all_extensions(self, extensions: List[ET.Element]):
        self.extensions_wrappers.extend(ExtensionWrapper(extension) for extension in extensions)

    def get_extension_wrappers(self) -> List[ExtensionWrapper]:
        return self.extensions_wrappers

    def find_node_by_level(self, level: str) -> Optional[XmiNode]:
        for node in self.nodes:
            if node.level == level:
                return node
        return None
