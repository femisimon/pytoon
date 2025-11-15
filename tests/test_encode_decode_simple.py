# tests/test_encode_decode_simple.py
import pytoon


def test_basic_encode_decode():
    data = {"a": 1, "b": True, "c": "hello"}
    text = pytoon.encode(data)
    out = pytoon.decode(text)
    assert out == data
