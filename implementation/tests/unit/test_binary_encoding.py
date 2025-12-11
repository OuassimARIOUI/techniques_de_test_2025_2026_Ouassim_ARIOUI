import struct
from triangulator.binary_utils import decode_pointset, encode_triangles

def test_decode_simple_pointset():
    # pointset: 2 points : (1.0, 2.0), (3.0, 4.0)
    data = struct.pack("Iffff", 2, 1.0, 2.0, 3.0, 4.0)
    pts = decode_pointset(data)
    assert pts == [(1.0, 2.0), (3.0, 4.0)]

def test_decode_wrong_size():
    # announces 3 points but provides only 2
    data = struct.pack("Iffff", 3, 1.0, 2.0, 3.0, 4.0)
    import pytest
    with pytest.raises(ValueError):
        decode_pointset(data)

def test_decode_nan_values():
    import pytest
    nan = float("nan")
    data = struct.pack("Iff", 1, nan, 2.0)
    with pytest.raises(ValueError):
        decode_pointset(data)

def test_encode_simple_triangle():
    triangles = [(0,1,2)]
    binary = encode_triangles(triangles)
    # Expected format: count + indices
    expected = struct.pack("IIII", 1, 0, 1, 2)
    assert binary == expected

def test_encode_multiple_triangles():
    triangles = [(0,1,2), (2,3,0)]
    binary = encode_triangles(triangles)
    tcount = struct.unpack("I", binary[:4])[0]
    assert tcount == 2

def test_decode_corrupted_binary():
    import pytest
    corrupted = b"\x00\x00\x00\x02\xFF\xFF\xAA"  # invalid binary
    with pytest.raises(ValueError):
        decode_pointset(corrupted)
