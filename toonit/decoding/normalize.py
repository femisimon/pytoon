# toonit/decoding/normalize.py
from __future__ import annotations
from typing import Any, Dict, List

from toonit.core.types import (
    LiteralNode,
    ListNode,
    ObjectNode,
    Node
)
from toonit.encoding.folding import unfold_object


# ----------------------------------------------------------
# Public: normalize AST → Python
# ----------------------------------------------------------

def normalize_node(node: Node) -> Any:
    """
    Convert AST nodes → Python-native values.
    """
    if isinstance(node, LiteralNode):
        return node.value

    if isinstance(node, ListNode):
        return [normalize_node(n) for n in node.items]

    if isinstance(node, ObjectNode):
        # Normalize child nodes directly
        raw = {k: normalize_node(v) for k, v in node.entries.items()}

        expanded = maybe_unexpand_columns(raw)
        return _unfold_structure(expanded)

    raise ValueError(f"Unknown node type: {node}")


# ----------------------------------------------------------
# Column-unexpansion (unchanged)
# ----------------------------------------------------------

def maybe_unexpand_columns(obj: Dict[str, Any]) -> Any:
    """
    If object values are *all equal-length lists*, assume it is
    columnar data and reconstruct rows.
    """

    if not obj:
        return obj

    values = list(obj.values())

    # Columnar only if all values are lists
    if not all(isinstance(v, list) for v in values):
        return obj

    length = len(values[0])
    if not all(len(v) == length for v in values):
        return obj

    rows: List[Dict[str, Any]] = []
    keys = list(obj.keys())

    for i in range(length):
        row = {key: obj[key][i] for key in keys}
        rows.append(row)

    return rows


def _unfold_structure(value: Any) -> Any:
    """
    Apply unfold_object to dictionaries (including nested dicts inside lists).
    """
    if isinstance(value, list):
        return [_unfold_structure(item) for item in value]

    if isinstance(value, dict):
        return unfold_object(value)

    return value
