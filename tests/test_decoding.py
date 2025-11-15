from toonit.decoding.decoder import decode

def test_decode_basic():
    result = decode("hello")
    assert result == "hello"
