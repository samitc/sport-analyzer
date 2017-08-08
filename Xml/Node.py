import xml.etree.ElementTree as etree


class Node:
    def __init__(self, node: etree):
        self.node = node

    def findSon(self, sonName: str):
        return Node(self.node.find(sonName))

    def findSons(self, sonsName: str):
        return map(Node, self.node.findall(sonsName))
