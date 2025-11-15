# tests/test_parser_core.py
from pytoon.core.scanner import Scanner
from pytoon.core.parser import Parser


def test_parse_basic_object():
    text = '{a: 1, b: "hi"}'
    scanner = Scanner(text)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)
    node = parser.parse()

    assert node.kind == "object"
    assert "a" in node.entries
    assert "b" in node.entries


def test_parse_list():
    text = "[1, 2, 3]"
    node = Parser(Scanner(text).scan_tokens()).parse()
    assert node.kind == "list"
    assert len(node.items) == 3
