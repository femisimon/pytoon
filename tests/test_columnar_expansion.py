# tests/test_columnar_expansion.py
import toonit


def test_columnar_list_of_dicts():
    rows = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
    ]

    encoded = toonit.encode(rows)
    decoded = toonit.decode(encoded)

    assert decoded == rows
