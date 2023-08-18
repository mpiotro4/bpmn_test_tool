class BpmnNode:
    def __init__(self, node_id, name, decision_var_val=None, decision_var=None):
        self.id = node_id
        self.name = name
        self._decision_var = decision_var
        self._decision_var_val = decision_var_val

    @property
    def decision_var(self):
        return self._decision_var

    @decision_var.setter
    def decision_var(self, value):
        self._decision_var = value

    @property
    def decision_var_val(self):
        return self._decision_var_val

    @decision_var_val.setter
    def decision_var_val(self, value):
        self._decision_var_val = value

    def __str__(self):
        parts = [f"id: {self.id}", f"name: {self.name}"]

        if self._decision_var is not None:
            parts.append(f"decision_var: {self._decision_var}")
        if self._decision_var_val is not None:
            parts.append(f"decision_var_val: {self._decision_var_val}")

        return ", ".join(parts)
