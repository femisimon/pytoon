# tests/test_round_trip.py
import toonit


def test_round_trip_consistency():
    data = {
        "info": {"name": "Femi", "city": "Lagos"},
        "list": [1, 2, 3],
        "flag": False,
    }

    encoded = toonit.encode(data)
    decoded = toonit.decode(encoded)
    reencoded = toonit.encode(decoded)

    # The decoded structure should equal original
    assert decoded == data

    # And reencoded text should remain stable
    assert reencoded == encoded
