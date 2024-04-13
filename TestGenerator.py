class TestGenerator:
    @staticmethod
    def generate_feature(filename, bpmn_graph):
        paths = bpmn_graph.get_all_paths()
        with open(filename, "w") as file:
            for index, path in enumerate(paths):
                TestGenerator._generate_test_case(file, path, index, bpmn_graph)

    @staticmethod
    def _generate_test_case(file, path, index, bpmn_graph):
        file.write("@Test\n")
        file.write(f"public void scenario{index + 1}() {{\n")
        file.write(f"""\tfinal ProcessInstance instance = runtimeService().startProcessInstanceByKey("{bpmn_graph.get_process_id()}");\n""")
        for index, node in enumerate(path):
            TestGenerator._generate_step(node, file)
        file.write("}\n\n")

    @staticmethod
    def _generate_step(node, file):
        file.write("\t")
        file.write(node.generate_step())
        file.write("\n")
