import xml.etree.ElementTree as ET
from itertools import chain
from typing import List
import networkx as nx

from xmi.UseCaseWrapper import UseCaseWrapper
from xmi.XmiNode import XmiNode
from xmi.XmiConstants import XmiConstants as XC
from xmi.XmiUtils import transform_id


class XmiWrapper:
    def __init__(self, path: str):
        self.path = path
        self.use_cases_wrappers: List[UseCaseWrapper] = []
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self._create_use_cases(self.root.findall(XC.USE_CASE, XC.XMI_NAMESPACE))

    def get_graphs(self) -> List[nx.DiGraph]:
        return list(chain.from_iterable(use_case_wrapper.get_graphs() for use_case_wrapper in self.use_cases_wrappers))

    def _create_use_cases(self, use_cases: List[ET.Element]):
        self.use_cases_wrappers.extend(UseCaseWrapper(use_case) for use_case in use_cases)