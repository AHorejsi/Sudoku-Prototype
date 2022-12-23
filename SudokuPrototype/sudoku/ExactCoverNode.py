from __future__ import annotations
from typing import NoReturn


class _ExactCoverNode:
    def __init__(self):
        self.up = self
        self.down = self
        self.left = self
        self.right = self

    @staticmethod
    def make_with_column(column: _ExactCoverNode) -> _ExactCoverNode:
        new = _ExactCoverNode()
        new.column = column
        new.size = 0

        return new

    def hook_down(self, other: _ExactCoverNode) -> _ExactCoverNode: # Check if return is necessary
        other.down = self.down
        other.down.up = other
        other.up = self
        self.down = other

        return other

    def hook_right(self, other: _ExactCoverNode) -> _ExactCoverNode: # Check if return is necessary
        other.right = self.right
        other.right.left = other
        other.left = self
        self.right = other

        return other

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
