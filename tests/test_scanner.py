from toonit.parser.scanner import Scanner

def test_scanner_init():
    s = Scanner("hello")
    assert s.source == "hello"
