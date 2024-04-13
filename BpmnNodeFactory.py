from BpmnNode import BpmnNode
from BpmnConstants import BpmnConstants as BC


class BpmnNodeFactory:
    @staticmethod
    def create_node(node_id, name, node_type):
        if node_type == BC.USER_TASK:
            return UserTask(node_id, name)
        elif node_type == BC.EXCLUSIVE_GATEWAY:
            return ExclusiveGateway(node_id, name)
        elif node_type == BC.SERVICE_TASK:
            return ServiceTask(node_id, name)
        elif node_type == BC.END_EVENT:
            return EndEvent(node_id, name)
        elif node_type == BC.START_EVENT:
            return StartEvent(node_id, name)
        else:
            return BpmnNode(node_id, name)


class UserTask(BpmnNode):
    def __init__(self, node_id, name):
        super().__init__(node_id, name)

    def generate_step(self):
        return f"""assertThat(instance).isWaitingAt("{self.id}");"""


class ExclusiveGateway(BpmnNode):
    def __init__(self, node_id, name):
        super().__init__(node_id, name)

    def generate_step(self):
        return ""
        # return f"""assertThat(instance).hasPassed("{self.id}");"""


class ServiceTask(BpmnNode):
    def __init__(self, node_id, name):
        super().__init__(node_id, name)

    def generate_step(self):
        return f"""Map<String, Object> variables = new HashMap<>();
    variables.put("{self.decision_var}", "{self.decision_var_val}");
    complete(task(), variables);"""
        # return f"""assertThat(instance).hasPassed("{self.id}");"""


class EndEvent(BpmnNode):
    def __init__(self, node_id, name):
        super().__init__(node_id, name)

    def generate_step(self):
        return f"""assertThat(instance).hasPassed("{self.id}").isEnded();"""


class StartEvent(BpmnNode):
    def __init__(self, node_id, name):
        super().__init__(node_id, name)

    def generate_step(self):
        return "assertThat(instance).isStarted();"
