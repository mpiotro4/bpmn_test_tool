import re


class XmiNode:
    def __init__(self, node_guid, name, level):
        self.guid = node_guid
        self.name = name
        self.level = level
        self.normalized_name = self.normalize(name)


    def normalize(self, s):
        # Usuwanie znaków interpunkcyjnych
        if s is not None:
            s = re.sub(r'[^\w\s]', '', s)
            # Ignorowanie wielkości liter
            return s.lower()

    def __eq__(self, other):
        return self.normalized_name == other.normalized_name

    def __hash__(self):
        return hash(self.normalized_name)

    def __str__(self):
        return self.name
