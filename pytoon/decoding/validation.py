# pytoon/decoding/validation.py
from __future__ import annotations

from pytoon.core.types import (
    Node,
    LiteralNode,
    ListNode,
    ObjectNode
)


def validate_root_node(node: Node):
    """
    Ensure the AST root is structurally valid.
    More validations can be added later.
    """
    if isinstance(node, LiteralNode):
        return

    if isinstance(node, ListNode):
        for n in node.items:
            validate_root_node(n)
        return

    if isinstance(node, ObjectNode):
        for k, v in node.entries.items():
            validate_root_node(v)
        return

    raise ValueError(f"Invalid root node type: {node}")
