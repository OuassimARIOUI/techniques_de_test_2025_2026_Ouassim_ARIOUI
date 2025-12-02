import requests
from triangulator.api import app

def test_psm_unreachable():
    # simulate unreachable PSM
    try:
        requests.get("http://localhost:9999/not_exist", timeout=0.001)
    except Exception:
        pass
    # later API must return 503

def test_psm_corrupted_response():
    # simulate corrupted binary returned by PSM
    corrupted = b"\xFF\x00"
    # Normally decode_pointset should fail on this
    from triangulator.binary_utils import decode_pointset
    decode_pointset(corrupted)
