# toonit/utils/constants.py
from __future__ import annotations

from typing import Literal, Mapping

# ---------------------------------------------------------------------------
# List markers
# ---------------------------------------------------------------------------

LIST_ITEM_MARKER: str = "-"
LIST_ITEM_PREFIX: str = "- "

# ---------------------------------------------------------------------------
# Structural characters
# ---------------------------------------------------------------------------

COMMA: str = ","
COLON: str = ":"
SPACE: str = " "
PIPE: str = "|"
DOT: str = "."

# Basic control chars / escapes
TAB: str = "\t"
NEWLINE: str = "\n"
CARRIAGE_RETURN: str = "\r"
BACKSLASH: str = "\\"
DOUBLE_QUOTE: str = '"'

# ---------------------------------------------------------------------------
# Literal tokens
# ---------------------------------------------------------------------------

TRUE_LITERAL: str = "true"
FALSE_LITERAL: str = "false"
NULL_LITERAL: str = "null"

# If you later want different spellings (e.g. YES/NO), they should map here.

# ---------------------------------------------------------------------------
# Delimiters
# ---------------------------------------------------------------------------

DelimiterKey = Literal["comma", "tab", "pipe"]
Delimiter = Literal[",", "\t", "|"]

DELIMITERS: Mapping[DelimiterKey, Delimiter] = {
    "comma": COMMA,
    "tab": TAB,
    "pipe": PIPE,
}

DEFAULT_DELIMITER: Delimiter = DELIMITERS["comma"]
