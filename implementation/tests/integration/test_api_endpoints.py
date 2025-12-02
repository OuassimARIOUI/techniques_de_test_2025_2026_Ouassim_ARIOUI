from triangulator.api import app

def test_api_default_returns_501():
    client = app.test_client()
    r = client.get("/triangulate/abcd")
    assert r.status_code == 501

def test_api_invalid_uuid_format():
    client = app.test_client()
    r = client.get("/triangulate/@@@")
    assert r.status_code == 400   # behavior expected in final version

def test_api_pointset_not_found():
    client = app.test_client()
    r = client.get("/triangulate/99999999")
    assert r.status_code == 404

def test_api_method_not_allowed():
    client = app.test_client()
    r = client.post("/triangulate/1234")
    assert r.status_code == 405
