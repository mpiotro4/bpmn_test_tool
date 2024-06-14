import xml.etree.ElementTree as ET
from xmi.XmiConstants import XmiConstants as XC

class ExtensionWrapper:
    def __init__(self, extension: ET.Element):
        self._guid = extension.attrib.get(XC.GUID)
        if self._guid:
            self._guid = self._guid.strip('{}')
        self._level = extension.attrib.get(XC.LEVEL)
        self._join = extension.attrib.get(XC.JOIN)

    @property
    def guid(self) -> str:
        return self._guid

    @property
    def level(self) -> str:
        return self._level

    @property
    def join(self) -> str:
        return self._join
