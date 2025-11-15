# pytoon/utils/literal_utils.py
from __future__ import annotations

from .constants import TRUE_LITERAL, FALSE_LITERAL, NULL_LITERAL


def is_boolean_or_null_literal(token: str) -> bool:
    """
    Return True if the token is exactly the TOON boolean/null literal:
    - "true"
    - "false"
    - "null"
    """
    return token in (TRUE_LITERAL, FALSE_LITERAL, NULL_LITERAL)


def is_numeric_literal(token: str) -> bool:
    """
    Checks if a token represents a valid numeric literal.

    Rules (matching the TS version):
    - Empty string is not numeric.
    - No leading zeros for integers (except "0" itself).
      - "0"      -> allowed
      - "0.5"    -> allowed
      - "01"     -> rejected
      - "00.1"   -> rejected
    - Must be a finite float from Python's point of view.
    """
    if not token:
        return False

    # Must not have leading zeros (except for "0" or decimals like "0.5")
    if len(token) > 1 and token[0] == "0" and token[1] != ".":
        return False

    try:
        numeric_value = float(token)
    except ValueError:
        return False

    # Reject NaN / infinities just to mirror Number.isFinite behavior
    if numeric_value == float("inf") or numeric_value == float("-inf"):
        return False

    # Python's float doesn't have a NaN equality, so we check via comparison to itself
    if numeric_value != numeric_value:  # NaN check
        return False

    return True
