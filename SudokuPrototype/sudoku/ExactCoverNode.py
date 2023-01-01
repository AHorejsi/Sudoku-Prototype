from __future__ import annotations
from typing import NoReturn

class _ExactCoverNode:
    def __init__(self):
        self.up = self
        self.down = self
        self.left = self
        self.right = self

    def hook_down(self, other: _ExactCoverNode) -> NoReturn:
        other.down = self.down
        other.down.up = other
        other.up = self
        self.down = other

    def hook_right(self, other: _ExactCoverNode) -> NoReturn:
        other.right = self.right
        other.right.left = other
        other.left = self
        self.right = other

    def unlink_left_right(self) -> NoReturn:
        self.right.left = self.left
        self.left.right = self.right

    def relink_left_right(self) -> NoReturn:
        self.left.right = self
        self.right.left = self

    def unlink_up_down(self) -> NoReturn:
        self.up.down = self.down
        self.down.up = self.up

    def relink_up_down(self) -> NoReturn:
        self.up.down = self
        self.down.up = self

    def cover(self) -> NoReturn:
        if not hasattr(self, "column") or not hasattr(self, "size"):
            raise ValueError("Not a column node")

        self.unlink_left_right()

        node1 = self.down

        while node1 is not self:
            node2 = node1.left

            while node2 is not node1:
                node2.unlink_up_down()
                node2.column.size -= 1

                node2 = node2.right

            node1 = node1.down

    def uncover(self) -> NoReturn:
        if not hasattr(self, "column") or not hasattr(self, "size"):
            raise ValueError("Not a column node")

        node1 = self.up

        while node1 is not self:
            node2 = node1.left

            while node2 is not node1:
                node2.column.size += 1
                node2.relink_up_down()

                node2 = node2.left

            node1 = node1.up

        self.relink_left_right()
