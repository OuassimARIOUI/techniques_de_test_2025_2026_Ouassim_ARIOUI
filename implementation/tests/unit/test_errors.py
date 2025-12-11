from triangulator.binary_utils import decode_pointset
import pytest


def test_invalid_header():
    data = b"\xFF\xFF"  # too small
    with pytest.raises(ValueError):
        decode_pointset(data)


def test_negative_index_error():
    # not possible binary, but simulate wrong structure
    data = b"\xFF\xFF\xFF\xFF"  # huge count
    with pytest.raises(ValueError):
        decode_pointset(data)


def test_unexpected_exception_logged():
    bad_data = b"RANDOMGARBAGE"
    with pytest.raises(ValueError):
        decode_pointset(bad_data)
