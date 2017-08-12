import xml.etree.ElementTree as etree

import Xml.Node as Node


class Xml:
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, str):
                self.initFromFile(arg)
            elif isinstance(arg, Node.Node):
                self.initFromTree(arg.node)

    def initFromTree(self, tree):
        self.tree = etree.ElementTree(element=tree)

    def initFromFile(self, xmlFile: str):
        self.filePath = xmlFile
        self.tree = etree.parse(xmlFile)

    def regNamespace(self, prefix: str, uri: str):
        etree.register_namespace(prefix, uri)

    def getRoot(self):
        return Node.Node(self.tree.getroot())

    def write(self, fileName):
        self.tree.write(fileName)
