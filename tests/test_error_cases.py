# tests/test_error_cases.py
import pytest
import pytoon


def test_decode_invalid_missing_brace():
    with pytest.raises(Exception):
        pytoon.decode("{a: 1")


def test_decode_invalid_structure():
    with pytest.raises(Exception):
        pytoon.decode("[1, 2, ]")


def test_decode_garbage_text():
    with pytest.raises(Exception):
        pytoon.decode("%%% !!! @@@")
