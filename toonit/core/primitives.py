# toonit/core/primitives.py
from __future__ import annotations

from typing import Any

from toonit.utils.literal_utils import (
    is_boolean_or_null_literal,
    is_numeric_literal
)
from toonit.utils.constants import (
    TRUE_LITERAL,
    FALSE_LITERAL,
    NULL_LITERAL
)
from toonit.utils.string_utils import unescape_string


def decode_literal(token: str) -> Any:
    if token == TRUE_LITERAL:
        return True
    if token == FALSE_LITERAL:
        return False
    if token == NULL_LITERAL:
        return None

    if is_numeric_literal(token):
        if "." in token:
            return float(token)
        return int(token)

    # Quoted string
    if token.startswith('"') and token.endswith('"'):
        inner = token[1:-1]
        return unescape_string(inner)

    # Fallback: treat bare words as literal strings
    return token


# toonit/core/primitives.py

def is_primitive(value) -> bool:
    return isinstance(value, (str, int, float, bool)) or value is None
