class BTreeNode: #Arvore B
    def __init__(self, is_leaf=True):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode()
        self.t = t  # Ordem da árvore B

    def insert(self, key):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            new_node = BTreeNode(is_leaf=False)
            new_node.children.append(root)
            self.split_child(new_node, 0)
            self.root = new_node
            self.insert_non_full(new_node, key)
        else:
            self.insert_non_full(root, key)

    def insert_non_full(self, x, key):
        i = len(x.keys) - 1
        if x.is_leaf:
            x.keys.append(None)
            while i >= 0 and key < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = key
        else:
            while i >= 0 and key < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                if key > x.keys[i]:
                    i += 1
            self.insert_non_full(x.children[i], key)

    def split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(is_leaf=y.is_leaf)
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:2 * t - 1]
        y.keys = y.keys[0:t - 1]
        if not y.is_leaf:
            z.children = y.children[t:2 * t]
            y.children = y.children[0:t]

    def search(self, key, x=None):
        if x is None:
            x = self.root
        i = 0
        while i < len(x.keys) and key > x.keys[i]:
            i += 1
        if i < len(x.keys) and key == x.keys[i]:
            return True
        elif x.is_leaf:
            return False
        else:
            return self.search(key, x.children[i])

    def display(self, x=None, level=0):
        if x is None:
            x = self.root
        print(f"Level {level}: {x.keys}")
        level += 1
        if not x.is_leaf:
            for child in x.children:
                self.display(child, level)

# Exemplo de uso:
b_tree = BTree(3)  # Árvore B de ordem 3
keys = [3, 7, 1, 5, 9, 2, 4, 6, 8, 10, 89, 54, 22, 24, 96, 16, 13, 28, 31, 48, 102]

for key in keys:
    b_tree.insert(key)

b_tree.display()  # Exibir a árvore B
print(b_tree.search(5))  # True
print(b_tree.search(11))  # False
