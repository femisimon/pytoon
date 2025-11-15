# toonit/core/writer.py
from __future__ import annotations

from typing import Any, Dict, List

from toonit.core.primitives import is_primitive  # we’ll add this below
from toonit.utils.constants import (
    DEFAULT_DELIMITER,
    SPACE,
)
from toonit.utils.string_utils import escape_string


class Writer:
    """
    Low-level writer for TOON-like text output.

    This version is intentionally conservative and JSON-adjacent:
    - Objects → { key: value, ... }
    - Lists   → [value, value, ...]
    - Primitives encoded with TOON-friendly rules.

    Later, when we mirror TOON's more compact columnar format,
    we can refine _write_list / _write_object without changing
    the public API: write(value) -> str.
    """

    def __init__(self, indent: int = 2, delimiter: str = DEFAULT_DELIMITER):
        self.indent = indent
        self.delimiter = delimiter

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------

    def write(self, value: Any) -> str:
        """Encode a Python value into TOON text."""
        return self._write_value(value, level=0).rstrip() + "\n"

    # ---------------------------------------------------------------------
    # Internal dispatch
    # ---------------------------------------------------------------------

    def _write_value(self, value: Any, level: int) -> str:
        if is_primitive(value):
            return self._write_primitive(value)

        if isinstance(value, list):
            return self._write_list(value, level)

        if isinstance(value, dict):
            return self._write_object(value, level)

        # Fallback: convert to string and quote
        return self._write_primitive(str(value))

    # ---------------------------------------------------------------------
    # Primitive / scalar encoding
    # ---------------------------------------------------------------------

    def _write_primitive(self, value: Any) -> str:
        if value is True:
            return "true"
        if value is False:
            return "false"
        if value is None:
            return "null"

        if isinstance(value, (int, float)):
            return repr(value)

        # Everything else: encode as a quoted string
        s = str(value)
        return f"\"{escape_string(s)}\""

    # ---------------------------------------------------------------------
    # Lists
    # ---------------------------------------------------------------------

    def _write_list(self, items: List[Any], level: int) -> str:
        if not items:
            return "[]"

        inner_indent = SPACE * (self.indent * (level + 1))
        current_indent = SPACE * (self.indent * level)

        parts: List[str] = ["["]

        # First item on new line
        for idx, item in enumerate(items):
            prefix = self.delimiter if idx > 0 else ""
            item_str = self._write_value(item, level + 1)
            parts.append(f"\n{inner_indent}{prefix}{item_str}")

        parts.append(f"\n{current_indent}]")
        return "".join(parts)

    # ---------------------------------------------------------------------
    # Objects
    # ---------------------------------------------------------------------

    def _write_object(self, obj: Dict[str, Any], level: int) -> str:
        if not obj:
            return "{}"

        inner_indent = SPACE * (self.indent * (level + 1))
        current_indent = SPACE * (self.indent * level)

        parts: List[str] = ["{"]

        keys = list(obj.keys())
        for idx, key in enumerate(keys):
            prefix = self.delimiter if idx > 0 else ""
            key_str = self._encode_key(key)
            value_str = self._write_value(obj[key], level + 1)
            parts.append(f"\n{inner_indent}{prefix}{key_str}: {value_str}")

        parts.append(f"\n{current_indent}}}")
        return "".join(parts)

    # ---------------------------------------------------------------------
    # Key encoding
    # ---------------------------------------------------------------------

    def _encode_key(self, key: str) -> str:
        """
        Encode an object key.

        For now:
        - if the key is "simple" (no spaces, no special chars), leave bare
        - otherwise, quote it like a string
        """
        if key and key.replace("_", "").isalnum():
            return key

        return f"\"{escape_string(key)}\""
