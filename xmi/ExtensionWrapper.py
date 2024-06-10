import xml.etree.ElementTree as ET


class ExtensionWrapper:
    def __init__(self, extension: ET.Element):
        self._guid = extension.attrib.get('guid')
        if self._guid:
            self._guid = self._guid.strip('{}')
        self._level = extension.attrib.get('level')
        self._join = extension.attrib.get('join')

    @property
    def guid(self) -> str:
        return self._guid

    @property
    def level(self) -> str:
        return self._level

    @property
    def join(self) -> str:
        return self._join
