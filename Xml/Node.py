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

    def text(self):
        return self.node.text

    def attrib(self, attName: str):
        return self.node.attrib[attName]
