import unittest
from bpmn.BpmnGraph import BpmnGraph
from bpmn.BpmnConstants import BpmnConstants as BC

class TestBpmnGraph(unittest.TestCase):

    def setUp(self):
        self.bpmn_graph = BpmnGraph("process_graph.bpmn")

    def test_node_creation(self):
        # Test if nodes are properly created during initialization
        nodes = self.bpmn_graph.nodes
        self.assertEqual(len(nodes), len(self.bpmn_graph.user_tasks) + len(self.bpmn_graph.exclusive_gateways) +
                         len(self.bpmn_graph.service_tasks) + len(self.bpmn_graph.end_event) + len(
            self.bpmn_graph.start_event))
        # Make sure nodes have valid IDs and names
        for node in nodes:
            self.assertIsNotNone(node.id)
            self.assertIsNotNone(node.name)

    def test_edge_creation(self):
        # Test if edges are properly created during initialization
        graph = self.bpmn_graph.G
        sequence_flows = self.bpmn_graph.sequence_flows
        for flow in sequence_flows:
            source_node = self.bpmn_graph._get_node_by_id(flow.get(BC.SOURCE_NODE))
            target_node = self.bpmn_graph._get_node_by_id(flow.get(BC.TARGET_NODE))
            self.assertTrue(graph.has_edge(source_node, target_node))

    def test_node_lookup(self):
        # Test if node lookup works correctly
        node_id = self.bpmn_graph.user_tasks[0].get('id')
        node = self.bpmn_graph._get_node_by_id(node_id)
        self.assertIsNotNone(node)
        self.assertEqual(node.id, node_id)


if __name__ == '__main__':
    unittest.main()
