from typing import List, Optional
import xml.etree.ElementTree as ET

from xmi.ExtensionWrapper import ExtensionWrapper
from xmi.XmiConstants import XmiConstants as XC

import networkx as nx

from xmi.ScenarioWrapper import ScenarioWrapper
from xmi.XmiNode import XmiNode


class UseCaseWrapper:
    def __init__(self, use_case: ET.Element):
        self.scenarios = use_case.findall(XC.SCENARIO, XC.XMI_NAMESPACE)
        self.scenario_wrappers: List[ScenarioWrapper] = []
        self._create_scenarios()
        self.merge_scenarios()
        self.scenario_wrapper = self.scenario_wrappers[0]

    def get_graphs(self) -> List[nx.DiGraph]:
        return [scenario_wrapper.get_graph() for scenario_wrapper in self.scenario_wrappers]

    def _create_scenarios(self):
        self.scenario_wrappers.extend(ScenarioWrapper(scenario) for scenario in self.scenarios)

    def find_scenario_by_id(self, search_id: str) -> Optional[ScenarioWrapper]:
        return next(
            (scenario_wrapper for scenario_wrapper in self.scenario_wrappers if scenario_wrapper.id == search_id), None)

    def merge_scenarios(self):
        """
        Merge scenarios based on their extension wrappers.
        """
        to_remove = []
        for scenario_wrapper in self.scenario_wrappers:
            for extension_wrapper in scenario_wrapper.get_extension_wrappers():
                source_scenario = self.find_scenario_by_id(extension_wrapper.guid)
                if source_scenario:
                    self._merge_scenario(scenario_wrapper, source_scenario, extension_wrapper)
                    to_remove.append(source_scenario)
        self.scenario_wrappers = [sw for sw in self.scenario_wrappers if sw not in to_remove]

    def _merge_scenario(self, target: ScenarioWrapper, source: ScenarioWrapper, extension_wrapper: ExtensionWrapper):
        """
        Merge the source scenario into the target scenario based on the given extension wrapper.
        """
        merged_graph = nx.compose(source.get_graph(), target.get_graph())
        node1 = self._find_merge_node(target, extension_wrapper)
        node2 = source.nodes[0]
        merged_graph.add_edge(node1, node2)

        join_merge_node = self._find_join_merge_node(extension_wrapper.join, target)
        if join_merge_node is not None:
            merged_graph.add_edge(source.nodes[-1], join_merge_node)

        target.set_graph(merged_graph)
        target.end_nodes.extend(source.end_nodes)

    def _find_join_merge_node(self, join_guid: str, target: ScenarioWrapper) -> Optional[XmiNode]:
        print("Join guid: " + join_guid)
        if join_guid != "End":
            print(target.find_node_by_guid(join_guid))
            return target.find_node_by_guid(join_guid)
        return None

    def _find_merge_node(self, scenario_wrapper: ScenarioWrapper, extension_wrapper: ExtensionWrapper):
        """
        Find the appropriate node in the scenario wrapper to merge with.
        """
        level_without_letter = ''.join(filter(str.isdigit, extension_wrapper.level))
        new_level = int(level_without_letter) - 1
        return scenario_wrapper.find_node_by_level(str(new_level))