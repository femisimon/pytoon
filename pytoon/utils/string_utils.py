# pytoon/utils/string_utils.py
from __future__ import annotations

from typing import Optional

from .constants import (
    BACKSLASH,
    CARRIAGE_RETURN,
    DOUBLE_QUOTE,
    NEWLINE,
    TAB,
)


def escape_string(value: str) -> str:
    """
    Escapes special characters in a string for TOON encoding.

    Mirrors the TS implementation:

    - `\`  -> `\\`
    - `"`  -> `\"`
    - `\n` -> `\\n`
    - `\r` -> `\\r`
    - `\t` -> `\\t`
    """
    return (
        value.replace(BACKSLASH, BACKSLASH + BACKSLASH)
        .replace(DOUBLE_QUOTE, BACKSLASH + DOUBLE_QUOTE)
        .replace(NEWLINE, BACKSLASH + "n")
        .replace(CARRIAGE_RETURN, BACKSLASH + "r")
        .replace(TAB, BACKSLASH + "t")
    )


def unescape_string(value: str) -> str:
    """
    Reverse of `escape_string` for decoding.

    This isn't shown in the snippet you shared, but decoders will need it,
    so we implement the natural inverse of the escape rules.
    """
    # We'll parse with a small state machine rather than chained replaces,
    # to avoid double-unescaping.
    result_chars: list[str] = []
    i = 0
    length = len(value)

    while i < length:
        ch = value[i]
        if ch != BACKSLASH:
            result_chars.append(ch)
            i += 1
            continue

        # Backslash: check next char for escape code
        if i + 1 >= length:
            # Trailing backslash – keep it literal
            result_chars.append(BACKSLASH)
            i += 1
            continue

        esc = value[i + 1]
        if esc == "n":
            result_chars.append(NEWLINE)
        elif esc == "r":
            result_chars.append(CARRIAGE_RETURN)
        elif esc == "t":
            result_chars.append(TAB)
        elif esc == BACKSLASH:
            result_chars.append(BACKSLASH)
        elif esc == DOUBLE_QUOTE:
            result_chars.append(DOUBLE_QUOTE)
        else:
            # Unknown escape – keep as-is (`\x` -> both chars)
            result_chars.append(BACKSLASH)
            result_chars.append(esc)

        i += 2

    return "".join(result_chars)


def find_closing_quote(content: str, start_index: int = 0) -> int:
    """
    Find the index of the next unescaped DOUBLE_QUOTE in `content`,
    starting from the given index which is assumed to be the position
    of the *opening* quote.

    Returns -1 if no matching closing quote is found.

    This is equivalent to the `findClosingQuote` helper used in decoders.
    """
    i = start_index + 1  # skip the opening quote
    escaped = False

    while i < len(content):
        ch = content[i]

        if escaped:
            escaped = False
            i += 1
            continue

        if ch == BACKSLASH:
            escaped = True
            i += 1
            continue

        if ch == DOUBLE_QUOTE:
            return i

        i += 1

    return -1


def find_first_unquoted_char(content: str, target: str) -> int:
    """
    Find the index of the first occurrence of `target` that is NOT inside
    double quotes, and not part of an escaped quote.

    This mirrors the tail of the TS implementation you shared, which:
    - walks the string
    - toggles `inQuotes` when seeing a non-escaped DOUBLE_QUOTE
    - returns index when it sees `target` and `!inQuotes`
    """
    if not target or len(target) != 1:
        raise ValueError("target must be a single character")

    i = 0
    in_quotes = False
    escaped = False

    while i < len(content):
        ch = content[i]

        if escaped:
            escaped = False
            i += 1
            continue

        if ch == BACKSLASH:
            escaped = True
            i += 1
            continue

        if ch == DOUBLE_QUOTE:
            in_quotes = not in_quotes
            i += 1
            continue

        if ch == target and not in_quotes:
            return i

        i += 1

    return -1
