from node import Node

class MerkleTree:
    def __init__(self, values):
        self.root = None
        self.buildTree(values)

    def buildTree(self, values):
        print("Obliczanie skrotu drzewa Merkle'a z transakcji")
        leaves = [Node(None, None, Node.hash(value), value) for value in values]

        #powtorz ostatni glos jezeli jest ich nieparzysta ilosc
        if len(leaves) % 2 == 1:
            last_node = leaves[-1]
            leaves.append(Node(last_node.left, last_node.right, last_node.value, last_node.content))
        self.root = self.buildTreeRec(leaves)

    def buildTreeRec(self, nodes):
        if len(nodes) == 0:
            return None

        half = len(nodes) // 2

        if half == 0:
            return Node(nodes[0], nodes[0], Node.hash(nodes[0].value),
                        nodes[0].content)

        left = self.buildTreeRec(nodes[:half])
        right = self.buildTreeRec(nodes[half:])

        value = Node.hash(left.value + right.value)
        content = left.content + "+" + right.content

        return Node(left, right, value, content)


    def getRootHash(self):
        return self.root.value