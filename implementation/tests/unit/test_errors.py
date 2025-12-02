from triangulator.binary_utils import decode_pointset

def test_invalid_header():
    data = b"\xFF\xFF"  # too small
    decode_pointset(data)

def test_negative_index_error():
    # not possible binary, but simulate wrong structure
    data = b"\xFF\xFF\xFF\xFF"  # huge count
    decode_pointset(data)

def test_unexpected_exception_logged():
    bad_data = b"RANDOMGARBAGE"
    decode_pointset(bad_data)
