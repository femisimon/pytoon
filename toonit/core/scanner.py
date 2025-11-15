# toonit/core/scanner.py
from __future__ import annotations

from typing import List

from toonit.core.types import Token
from toonit.utils.string_utils import find_closing_quote
from toonit.utils.constants import (
    SPACE,
    NEWLINE,
    TAB,
    CARRIAGE_RETURN,
    DOUBLE_QUOTE,
    BACKSLASH
)


WHITESPACE = {SPACE, TAB, NEWLINE, CARRIAGE_RETURN}


class Scanner:
    """
    Low-level scanner that turns TOON text into tokens.

    Full parsing rules will be added when we port parser.ts,
    but this scaffold already supports:
    - quoted strings
    - symbols like ':', ',', '|'
    - identifiers / barewords
    """

    def __init__(self, source: str):
        self.source = source
        self.length = len(source)
        self.index = 0

    def eof(self) -> bool:
        return self.index >= self.length

    def peek(self) -> str:
        return self.source[self.index] if not self.eof() else ""

    def advance(self) -> str:
        ch = self.peek()
        self.index += 1
        return ch

    # -----------------------------------------------------------------------
    # Main scanning loop
    # -----------------------------------------------------------------------

    def scan_tokens(self) -> List[Token]:
        tokens: List[Token] = []

        while not self.eof():
            ch = self.peek()

            # Skip whitespace
            if ch in WHITESPACE:
                self.advance()
                continue

            # Quoted string
            if ch == DOUBLE_QUOTE:
                tokens.append(self._scan_string())
                continue

            # Symbols
            if ch in {":", ",", "|", "-", "{", "}", "[", "]"}:
                tokens.append(Token(type="symbol", value=self.advance(), position=self.index - 1))
                continue

            # Identifiers / numbers / booleans
            tokens.append(self._scan_bareword())

        return tokens

    # -----------------------------------------------------------------------
    # Scan quoted string
    # -----------------------------------------------------------------------

    def _scan_string(self) -> Token:
        start = self.index
        opening = self.advance()  # consume "
        end = find_closing_quote(self.source, start)

        if end == -1:
            raise ValueError("Unterminated string literal")

        raw = self.source[start : end + 1]
        self.index = end + 1
        return Token(type="string", value=raw, position=start)

    # -----------------------------------------------------------------------
    # Scan unquoted barewords (keys, numbers, true/false/null, etc.)
    # -----------------------------------------------------------------------

    def _scan_bareword(self) -> Token:
        start = self.index
        chars = []

        while not self.eof():
            ch = self.peek()
            if ch in WHITESPACE or ch in {":", ",", "|", "-", "{", "}", "[", "]"}:
                break
            chars.append(self.advance())

        return Token(type="bareword", value="".join(chars), position=start)
