# tests/test_encode_decode_simple.py
import toonit


def test_basic_encode_decode():
    data = {"a": 1, "b": True, "c": "hello"}
    text = toonit.encode(data)
    out = toonit.decode(text)
    assert out == data
