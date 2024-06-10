from typing import List, Optional
import xml.etree.ElementTree as ET

from xmi.ExtensionWrapper import ExtensionWrapper
from xmi.XmiConstants import XmiConstants as XC

import networkx as nx

from xmi.ScenarioWrapper import ScenarioWrapper
class UseCaseWrapper:
    def __init__(self, use_case: ET.Element):
        self.scenarios = use_case.findall(XC.SCENARIO, XC.XMI_NAMESPACE)
        self.scenario_wrappers: List[ScenarioWrapper] = []
        self._create_scenarios()
        self.merge_scenarios()

    def get_graphs(self) -> List[nx.DiGraph]:
        return [scenario_wrapper.get_graph() for scenario_wrapper in self.scenario_wrappers]

    def _create_scenarios(self):
        self.scenario_wrappers.extend(ScenarioWrapper(scenario) for scenario in self.scenarios)

    def find_scenario_by_id(self, search_id: str) -> Optional[ScenarioWrapper]:
        return next(
            (scenario_wrapper for scenario_wrapper in self.scenario_wrappers if scenario_wrapper.id == search_id), None)

    def merge_scenarios(self):
        to_remove = []
        for scenario_wrapper in self.scenario_wrappers:
            for extension_wrapper in scenario_wrapper.get_extension_wrappers():
                source_scenario = self.find_scenario_by_id(extension_wrapper.guid)
                if source_scenario:
                    merged_graph = nx.compose(source_scenario.get_graph(), scenario_wrapper.get_graph())
                    scenario_wrapper.set_graph(merged_graph)
                    to_remove.append(source_scenario)
        self.scenario_wrappers = [sw for sw in self.scenario_wrappers if sw not in to_remove]