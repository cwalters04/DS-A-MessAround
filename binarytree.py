# Implement a binary Tree using nodes
from dataclasses import dataclass
from typing import Optional, Iterable, Generator

@dataclass
class Node:
    val : int
    left: Optional["Node"] = None
    right: Optional["Node"] = None

class BST:
    def __init__(self, values: Iterable[int] = ()):
        self.root: Optional[Node] = None
        for v in values:
            self.insert(v)

    # --- Insert --- 
    # Policy for duplicates: send equal values to the RIGHT (can flip).
    def insert(self, value: int) -> None:
        self.root = self._insert(self.root, value)

    def _insert(self, node: Optional[Node], value: int) -> Node:
        if node is None:
            return Node(value)
        if value < node.val:
            node.left = self._insert(node.left, value)
        else: # value >= node.val goes right
            node.right = self._insert(node.right, value)
        return node

    # -- Search -- 
    def contains(self, value: int) -> bool:
        cur = self.root
        while cur:
            if value == cur.val:
                return True
            cur = cur.left if value < cur.val else cur.right
        return False

    # -- Delete -- 
    def delete(self, value: int ) -> None:
        self.root = self._delete(self.root, value)

    def _delete(self, node: Optional[Node], value: int) -> Optional[Node]:
        if node is None:
            return None
        if value < node.val:
            node.left = self._delete(node.left, value)
        elif value > node.val:
            node.right = self._delete(node.right, value)
        else:
            # node to delete found 
            if node.left is None: # 0 or 1 child (right)
                return node.right
            if node.right is None: # 1 child (left)
                return node.left
            # 2 children: swap with inorder successor
            succ = self._min_node(node.right)
            node.val = succ.val
            node.right = self._delete(node.right, succ.val)

        return node

    def _min_node(self, node: Node) -> Node:
        while node.left:
            node = node.left
        return node
    
    def _max_node(self, node: Node) -> Node:
        while node.right:
            node = node.right
        return node

    # --- Traversals --- 
    def inorder(self) -> Generator[int, None, None]:
        yield from self._inorder(self.root)

    def _inorder(self, node: Optional[Node]) -> Generator[int, None, None]:
        if not node:
            return
        yield from self._inorder(node.left)
        yield node.val 
        yield from self._inorder(node.right)

    # -- Utilities --
    def sum(self) -> int:
        return self._sum(self.root)

    def _sum(self, node: Optional[Node]) -> int:
        if node is None:
            return 0
        return node.val + self._sum(node.left) + self._sum(node.right)

    def min(self) -> Optional[int]:
        return None if self.root is None else self._min_node(self.root).val

    def max(self) -> Optional[int]:
        return None if self.root is None else self._max_node(self.root).val

def main():
    t = BST([5, 2, 8, 1, 3, 7, 9, 3])

    print("Inorder traversal (initial):", list(t.inorder()))   # [1, 2, 3, 3, 5, 7, 8, 9]
    print("Contains 7?", t.contains(7))                        # True

    t.delete(2)
    print("After deleting 2:", list(t.inorder()))              # [1, 3, 3, 5, 7, 8, 9]

    print("Sum of all values:", t.sum())                       # 36
    print("Min and Max:", (t.min(), t.max()))                  # (1, 9)
main()
