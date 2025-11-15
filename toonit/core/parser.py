# toonit/core/parser.py
from __future__ import annotations

from typing import List, Optional

from toonit.core.types import (
    Token,
    Node,
    LiteralNode,
    ObjectNode,
    ListNode
)
from toonit.core.primitives import decode_literal
from toonit.core.scanner import Scanner

class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        """
        Accepts either:
        - a raw TOON string → auto-scan into tokens
        - a List[Token] → use directly
        """

        # Auto-tokenize if raw string provided
        if isinstance(tokens, str):
            tokens = Scanner(tokens).scan_tokens()

        # Must now be a list of Token
        self.tokens = tokens
        self.index = 0


    # -----------------------------------------------------------------------
    # Core utilities
    # -----------------------------------------------------------------------

    def eof(self) -> bool:
        return self.index >= len(self.tokens)

    def peek(self) -> Optional[Token]:
        return None if self.eof() else self.tokens[self.index]

    def advance(self) -> Token:
        tok = self.peek()
        if tok is None:
            raise ParseError("Unexpected end of input")
        self.index += 1
        return tok

    def match(self, value: str) -> bool:
        tok = self.peek()
        if tok and tok.value == value:
            self.advance()
            return True
        return False

    def expect(self, value: str):
        tok = self.advance()
        if tok.value != value:
            raise ParseError(f"Expected '{value}' but got '{tok.value}' at {tok.position}")

    # -----------------------------------------------------------------------
    # Public Entry
    # -----------------------------------------------------------------------

    def parse(self) -> Node:
        """Parse a single TOON value."""
        node = self.parse_value()

        if not self.eof():
            tok = self.peek()
            raise ParseError(f"Unexpected token '{tok.value}' after complete value")

        return node

    # -----------------------------------------------------------------------
    # Values
    # -----------------------------------------------------------------------

    def parse_value(self) -> Node:
        tok = self.peek()
        if tok is None:
            raise ParseError("Unexpected end of input while parsing value")

        # Object: { ... }
        if tok.value == "{":
            return self.parse_object()

        # List: [ ... ]
        if tok.value == "[":
            return self.parse_list()

        # String literal: "..."
        if tok.type == "string":
            raw = self.advance().value
            return LiteralNode(kind="string", value=decode_literal(raw))

        # Bareword literal: true, false, null, number, identifiers
        if tok.type == "bareword":
            raw = self.advance().value
            return LiteralNode(kind="literal", value=decode_literal(raw))

        raise ParseError(f"Unexpected token '{tok.value}' at position {tok.position}")

    # -----------------------------------------------------------------------
    # Lists
    # -----------------------------------------------------------------------

    def parse_list(self) -> ListNode:
        self.expect("[")
        items: List[Node] = []

        # Empty list
        if self.match("]"):
            return ListNode(kind="list", items=items)

        # First item
        items.append(self.parse_value())

        # Remaining items
        while self.match(","):
            items.append(self.parse_value())

        self.expect("]")
        return ListNode(kind="list", items=items)

    # -----------------------------------------------------------------------
    # Objects
    # -----------------------------------------------------------------------

    def parse_object(self) -> ObjectNode:
        self.expect("{")
        entries = {}

        # Empty object
        if self.match("}"):
            return ObjectNode(kind="object", entries=entries)

        # Parse first key
        key = self.parse_key()
        self.expect(":")
        entries[key] = self.parse_value()

        # More pairs
        while self.match(","):
            key = self.parse_key()
            self.expect(":")
            entries[key] = self.parse_value()

        self.expect("}")
        return ObjectNode(kind="object", entries=entries)

    # -----------------------------------------------------------------------
    # Keys
    # -----------------------------------------------------------------------

    def parse_key(self) -> str:
        tok = self.peek()
        if tok is None:
            raise ParseError("Unexpected end of input while reading key")

        if tok.type in ("string", "bareword"):
            self.advance()
            raw = tok.value
            # Strip quotes for object keys
            if tok.type == "string" and raw.startswith('"') and raw.endswith('"'):
                return raw[1:-1]
            return raw

        raise ParseError(f"Invalid object key '{tok.value}' at {tok.position}")
