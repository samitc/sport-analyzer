import xml.etree.ElementTree as etree

import Xml.Node as Node


class Xml:
    def __init__(self, xmlFile: str):
        self.filePath = xmlFile
        self.tree = etree.parse(xmlFile)

    def regNamespace(self, prefix: str, uri: str):
        etree.register_namespace(prefix, uri)

    def getRoot(self):
        return Node.Node(self.tree.getroot())
