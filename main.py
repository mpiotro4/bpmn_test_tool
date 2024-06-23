from GraphCompatibilityAnalyzer.GraphCompatibilityAnalyzer import generate_reports
from demo import *
from xmi.UseCaseWrapper import UseCaseWrapper

if __name__ == "__main__":
    bpmnWrappers = []
    bpmnFilesPaths = ["source_data/bpmn/autoryzacja_uzytkownika.bpmn",
                      "source_data/bpmn/Obsluga_sprawdzenia_salda.bpmn",
                      "source_data/bpmn/Obsluga_wplaty.bpmn",
                      "source_data/bpmn/Obsluga_wyplaty.bpmn",
                      "source_data/bpmn/sprawdzenie_pin.bpmn",
                      "source_data/bpmn/Sprawdzenie_salda.bpmn",
                      "source_data/bpmn/Wplata.bpmn",
                      "source_data/bpmn/Wyplata.bpmn"
                      ]

    for bpmnFilePath in bpmnFilesPaths:
        bpmnWrappers.append(BpmnWrapper(bpmnFilePath))

    bpmn_autoryzacja = bpmnWrappers[0]
    bpmn_obsluga_sprawdzenia_salda = bpmnWrappers[1]
    bpmn_obsluga_wplaty = bpmnWrappers[2]
    bpmn_obsluga_wyplaty = bpmnWrappers[3]
    bpmn_sprawdzenie_pin = bpmnWrappers[4]
    bpmn_sprawdzenie_salda = bpmnWrappers[5]
    bpmn_wplata = bpmnWrappers[6]
    bpmn_wyplata = bpmnWrappers[7]

    xmi_wrapper = XmiWrapper('source_data/bankomat_2.xml')
    use_case_autoryzacja = xmi_wrapper.use_cases_wrappers[0]
    use_case_obsluga_sprawdzenia_salda = xmi_wrapper.use_cases_wrappers[1]
    use_case_obsluga_wplaty = xmi_wrapper.use_cases_wrappers[2]
    use_case_obsluga_wyplaty = xmi_wrapper.use_cases_wrappers[3]
    use_case_sprawdznie_pin = xmi_wrapper.use_cases_wrappers[4]
    use_case_sprawdzenie_salda = xmi_wrapper.use_cases_wrappers[5]
    use_case_wplata = xmi_wrapper.use_cases_wrappers[6]
    use_case_wyplata = xmi_wrapper.use_cases_wrappers[7]

    graph = use_case_wyplata.scenario_wrapper.get_graph()
    # node_labels = {node: node.name for node in graph.nodes()}
    # GraphVisualizer.visualize_graph(graph, node_labels)

    graph_wrappers = [
        (use_case_autoryzacja, bpmn_autoryzacja),
        (use_case_obsluga_sprawdzenia_salda, bpmn_obsluga_sprawdzenia_salda),
        (use_case_obsluga_wyplaty, bpmn_obsluga_wyplaty),
        (use_case_obsluga_wplaty, bpmn_obsluga_wplaty),
        (use_case_sprawdznie_pin, bpmn_sprawdzenie_pin),
        (use_case_sprawdzenie_salda, bpmn_sprawdzenie_salda),
        (use_case_wplata, bpmn_wplata),
        (use_case_wyplata, bpmn_wyplata)
    ]

    generate_reports(graph_wrappers)
