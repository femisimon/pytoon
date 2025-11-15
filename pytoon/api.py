# pytoon/api.py

"""
Public API for PyToon.
This wraps the internal encoding, decoding, and parser modules
in a stable, user-facing interface.
"""

# Import actual encoder/decoder functions that currently exist
from .encoding.encoder import encode as _encode
from .decoding.decoder import decode as _decode   # <-- FIXED

# Parser import (correct path)
from .parser.parser import Parser                  # <-- FIXED


def encode(value):
    """Encode a Python object into Toon format."""
    return _encode(value)


def decode(text):
    """Decode a Toon-formatted string into a Python object."""
    return _decode(text)


def loads(text):
    """Parse Toon text and return the AST (no semantic decoding)."""
    parser = Parser(text)
    return parser.parse()


def dumps(value):
    """Encode + stringify in one step."""
    return encode(value)
