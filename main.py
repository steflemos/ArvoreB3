class BTreeNode:  # Arvore B
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

    def remove(self, key):
        if not self.root.keys:
            return
        if key in self.root.keys:
            if len(self.root.keys) == 1:
                if self.root.children:
                    self.root = self.root.children[0]
                else:
                    self.root.keys.remove(key)
            else:
                self.remove_key_from_node(self.root, key)
        else:
            self.remove_key_from_node(self.root, key)

    def remove_key_from_node(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            if node.is_leaf:
                node.keys.remove(key)
            else:
                key_pred = self.get_predecessor(node, i)
                if len(node.children[i].keys) >= self.t:
                    node.keys[i] = key_pred
                    self.remove_key_from_node(node.children[i], key_pred)
                else:
                    key_succ = self.get_successor(node, i)
                    node.keys[i] = key_succ
                    self.remove_key_from_node(node.children[i + 1], key_succ)
        else:
            if node.is_leaf:
                return
            if len(node.children[i].keys) < self.t:
                self.fix_child(node, i)
            self.remove_key_from_node(node.children[i], key)

    def get_predecessor(self, node, idx):
        current = node.children[idx]
        while not current.is_leaf:
            current = current.children[-1]
        return current.keys[-1]

    def get_successor(self, node, idx):
        current = node.children[idx + 1]
        while not current:
            current = current.children[0]
        return current.keys[0]

    def fix_child(self, node, idx):
        if idx > 0 and len(node.children[idx - 1].keys) >= self.t:
            self.borrow_from_left_sibling(node, idx)
        elif idx < len(node.children) - 1 and len(node.children[idx + 1].keys) >= self.t:
            self.borrow_from_right_sibling(node, idx)
        else:
            if idx < len(node.children):
                self.merge_children(node, idx)
            else:
                self.merge_children(node, idx - 1)

    def borrow_from_left_sibling(self, node, idx):
        child = node.children[idx]
        left_sibling = node.children[idx - 1]

        child.keys.insert(0, node.keys[idx - 1])
        node.keys[idx - 1] = left_sibling.keys.pop()
        if not left_sibling.is_leaf:
            child.children.insert(0, left_sibling.children.pop())

    def borrow_from_right_sibling(self, node, idx):
        child = node.children[idx]
        right_sibling = node.children[idx + 1]

        child.keys.append(node.keys[idx])
        node.keys[idx] = right_sibling.keys.pop(0)
        if not right_sibling.is_leaf:
            child.children.append(right_sibling.children.pop(0))

    def merge_children(self, node, idx):
        left_child = node.children[idx]
        right_child = node.children[idx + 1]

        left_child.keys.append(node.keys.pop(idx))
        left_child.keys.extend(right_child.keys)
        if not right_child.is_leaf:
            left_child.children.extend(right_child.children)

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
keys = [3, 7, 1, 5, 9, 2, 4, 6, 8, 10, 89,
        54, 22, 24, 96, 16, 13, 28, 31, 48, 102]

for key in keys:
    b_tree.insert(key)

b_tree.display()  # Exibir a árvore B
print(b_tree.search(5))  # True
print(b_tree.search(8))  # False

# Para remover um valor, você pode usar:
b_tree.remove(24)
b_tree.display()  # Exibir a árvore B após a remoção do valor 7
