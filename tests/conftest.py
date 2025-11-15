# tests/conftest.py
import pytest
import pytoon


@pytest.fixture
def sample_object():
    return {
        "name": "Femi",
        "age": 30,
        "roles": ["engineer", "writer"],
        "meta": {"active": True, "score": 9.5},
    }
