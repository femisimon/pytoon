# tests/test_error_cases.py
import pytest
import toonit


def test_decode_invalid_missing_brace():
    with pytest.raises(Exception):
        toonit.decode("{a: 1")


def test_decode_invalid_structure():
    with pytest.raises(Exception):
        toonit.decode("[1, 2, ]")


def test_decode_garbage_text():
    with pytest.raises(Exception):
        toonit.decode("%%% !!! @@@")
