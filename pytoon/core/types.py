# pytoon/core/types.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union


# ---------------------------------------------------------------------------
# Token Types
# ---------------------------------------------------------------------------

@dataclass
class Token:
    type: str        # e.g. "string", "number", "boolean", "null", "symbol"
    value: str
    position: int


# ---------------------------------------------------------------------------
# Node Types for AST
# ---------------------------------------------------------------------------

@dataclass
class LiteralNode:
    kind: str        # "string", "number", "boolean", "null"
    value: Any


@dataclass
class ListNode:
    kind: str        # "list"
    items: List["Node"]


@dataclass
class ObjectNode:
    kind: str        # "object"
    entries: Dict[str, "Node"]


Node = Union[LiteralNode, ListNode, ObjectNode]
