# toonit/encoding/encoder.py
from __future__ import annotations

from typing import Any, Dict, List

from toonit.core.writer import Writer
from toonit.encoding.folding import fold_object
from toonit.encoding.expand import expand_columns


def encode(data: Any, *, indent: int = 2, delimiter: str = ",") -> str:
    """
    High-level encoder that:
    1. Normalizes Python objects
    2. Applies folding/columnar transforms
    3. Serializes with Writer
    """

    transformed = prepare_for_encoding(data)
    writer = Writer(indent=indent, delimiter=delimiter)
    return writer.write(transformed)


# --------------------------------------------------------------------------
# Pre-encoding transforms
# --------------------------------------------------------------------------

def prepare_for_encoding(value: Any) -> Any:

    if isinstance(value, dict):
        # Flatten nested dicts: {"a": {"b": 1}} → {"a.b": 1}
        flat = fold_object(value)
        # Recursively prepare values
        return {k: prepare_for_encoding(v) for k, v in flat.items()}

    if isinstance(value, list) and all(isinstance(i, dict) for i in value):
        return expand_columns(value)

    return value

