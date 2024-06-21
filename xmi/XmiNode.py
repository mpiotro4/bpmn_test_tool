class XmiNode:
    def __init__(self, node_guid, name, level):
        self.guid = node_guid
        self.name = name
        self.level = level

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)