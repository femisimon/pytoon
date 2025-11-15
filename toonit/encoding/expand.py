# toonit/encoding/expand.py
from __future__ import annotations

from typing import Any, Dict, List


def expand_columns(rows: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
    """
    Expand a list of dicts into TOON-style column lists.

    Example:
        [
            {a: 1, b: 2},
            {a: 3, b: 4}
        ]

    →   {
            a: [1, 3],
            b: [2, 4]
        }

    This mirrors expandObjectRows() logic from TypeScript.
    """
    if not rows:
        return {}

    # Gather all keys
    keys = set()
    for row in rows:
        keys |= set(row.keys())

    expanded: Dict[str, List[Any]] = {k: [] for k in keys}

    # Fill column lists
    for row in rows:
        for key in keys:
            expanded[key].append(row.get(key, None))

    return expanded
