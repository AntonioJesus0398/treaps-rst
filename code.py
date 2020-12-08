import random

INF = 2 ** 31

class TreapNode:
    def __init__(self, key, priority):
        self.key = key
        self.priority = priority
        self.left_child = None
        self.right_child = None


class Treap:

    def __init__(self):
        self._root = None

    def find(self, key):
        def _find(key, root):
            if root == None:
                return False
            if root.key == key:
                return True
            elif key < root.key:
                return _find(key, root.left_child)
            else:
                return _find(key, root.right_child)

        return _find(key, self._root)

    def insert(self, key):
        def _insert(item, node):
            key, priority = item
            if not node:
                node = TreapNode(key, priority)
            elif key < node.key:
                node.left_child = _insert(item, node.left_child)
                if node.left_child.priority > node.priority:
                    node = self._rotate_right(node)
            elif key > node.key:
                node.right_child = _insert(item, node.right_child)
                if node.right_child.priority > node.priority:
                    node = self._rotate_left(node)
            return node

        priority = random.randint(1, INF)
        if self._root == None:
            self._root = TreapNode(key, priority)
        else:
            self._root = _insert((key, priority), self._root)

    def _rotate_right(self, root):
        new_root = root.left_child
        root.left_child = new_root.right_child
        new_root.right_child = root
        return new_root

    def _rotate_left(self, root):
        new_root = root.right_child
        root.right_child = new_root.left_child
        new_root.left_child = root
        return new_root

    @property
    def items(self):
        def _items(root):
            if not root:
                return []
            return _items(root.left_child)  + [root.key] + _items(root.right_child)

        return _items(self._root)

    def delete(self, key):
        def _delete(key, root):
            if not root:
                raise Exception(f"The item {key} doesn't exist in the collection")
            elif key < root.key:
                root.left_child = _delete(key, root.left_child)
            elif key > root.key:
                root.right_child = _delete(key, root.right_child)
            else:
                root = _delete_root(root)
            return root

        def _delete_root(root):
            if _is_leaf(root):
                root = None
            elif not root.left_child or (root.right_child and root.left_child.priority < root.right_child.priority):
                root = self._rotate_left(root)
                root.left_child = _delete_root(root.left_child)
            else:
                root = self._rotate_right(root)
                root.right_child = _delete_root(root.right_child)
            return root

        def _is_leaf(node):
            return not node.left_child and not node.right_child

        self._root = _delete(key, self._root)
