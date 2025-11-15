# pytoon/decoding/decoder.py
from __future__ import annotations

from typing import Any

from pytoon.core.scanner import Scanner
from pytoon.core.parser import Parser
from pytoon.decoding.normalize import normalize_node
from pytoon.decoding.validation import validate_root_node


def decode(text: str) -> Any:
    """
    High-level TOON decoder.

    Steps:
    1. Tokenize (Scanner)
    2. Parse (Parser)
    3. Validate AST shape
    4. Normalize AST → Python-native structures
    """
    scanner = Scanner(text)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)
    root = parser.parse()

    validate_root_node(root)
    return normalize_node(root)
