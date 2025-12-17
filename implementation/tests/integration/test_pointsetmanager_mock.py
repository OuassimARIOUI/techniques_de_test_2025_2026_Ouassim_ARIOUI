from triangulator.api import app


class _Resp:
    def __init__(self, status_code, content=b""):
        self.status_code = status_code
        self.content = content


def test_psm_unreachable(monkeypatch):
    def fake_get(url, timeout=1.0):
        raise Exception("connect error")

    monkeypatch.setattr('requests.get', fake_get)
    client = app.test_client()
    r = client.get("/triangulate/anyid")
    assert r.status_code == 503


def test_psm_corrupted_response(monkeypatch):
    corrupted = b"\xFF\x00"

    def fake_get(url, timeout=1.0):
        return _Resp(200, content=corrupted)

    monkeypatch.setattr('requests.get', fake_get)
    client = app.test_client()
    r = client.get("/triangulate/anyid")
    assert r.status_code == 502
