import xml.etree.ElementTree as etree


class Node:
    def __init__(self, node: etree):
        self.node = node

    def findSon(self, sonName: str):
        temp = self.node.find(sonName)
        if temp is None:
            return None
        return Node(temp)

    def findSons(self, sonsName: str):
        temp = self.node.findall(sonsName)
        if temp is None:
            return None
        return map(Node, temp)

    def getText(self):
        return self.node.text

    def setText(self, text):
        self.node.text = text

    def getAttrib(self, attName: str):
        return self.node.attrib[attName]

    def setAttrib(self, attName: str, val):
        self.node.attrib[attName] = val

    def remove(self, son):
        self.node.remove(son.node)

    def add(self, name, text=None, attrib=dict()):
        element = etree.SubElement(self.node, name, attrib)
        element.text = text
        return Node(element)
