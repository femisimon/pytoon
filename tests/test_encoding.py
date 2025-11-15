from toonit.encoding.encoder import encode

def test_encode_basic():
    result = encode("hello")
    assert isinstance(result, str)
