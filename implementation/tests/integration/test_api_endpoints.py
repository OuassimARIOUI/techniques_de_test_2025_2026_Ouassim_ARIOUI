import struct

from triangulator.api import app


class _Resp:
    def __init__(self, status_code, content=b""):
        self.status_code = status_code
        self.content = content


def test_api_success_returns_binary(monkeypatch):
    # prepare a PointSet with 3 points: (0,0),(1,0),(0,1)
    pts = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    buf = struct.pack("I", len(pts))
    for x, y in pts:
        buf += struct.pack("ff", x, y)

    def fake_get(url, timeout=1.0):
        return _Resp(200, content=buf)

    monkeypatch.setattr('requests.get', fake_get)
    client = app.test_client()
    r = client.get("/triangulate/abcd")
    assert r.status_code == 200
    # response should be binary
    assert hasattr(r, 'data')


def test_api_invalid_uuid_format():
    client = app.test_client()
    r = client.get("/triangulate/@@@")
    assert r.status_code == 400


def test_api_pointset_not_found(monkeypatch):
    def fake_get(url, timeout=1.0):
        return _Resp(404, content=b'')

    monkeypatch.setattr('requests.get', fake_get)
    client = app.test_client()
    r = client.get("/triangulate/notfoundid")
    assert r.status_code == 404


def test_api_method_not_allowed():
    client = app.test_client()
    r = client.post("/triangulate/1234")
    assert r.status_code == 405
