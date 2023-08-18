class BpmnNode:
    def __init__(self, node_id, name):
        self.id = node_id
        self.name = name

    def __str__(self):
        return f"id: {self.id}, name: {self.name}"