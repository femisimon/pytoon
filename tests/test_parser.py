from toonit.parser.parser import Parser

def test_parser_minimal():
    p = Parser("hello")
    result = p.parse()
    assert result is not None
