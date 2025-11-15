# tests/test_folding.py
import toonit
from toonit.encoding.folding import fold_object


def test_folding_simple():
    data = {"a": {"b": 1, "c": 2}}
    folded = fold_object(data)

    assert folded == {"a.b": 1, "a.c": 2}


def test_folding_through_encode_decode():
    data = {"a": {"b": 1, "c": 2}}
    out = toonit.decode(toonit.encode(data))
    assert out == data
