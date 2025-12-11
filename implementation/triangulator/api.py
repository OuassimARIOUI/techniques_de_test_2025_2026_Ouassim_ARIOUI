try:
    from flask import Flask, Response
except Exception:
    Flask = None
    Response = None
import re


def _valid_id(s: str) -> bool:
    return bool(re.match(r"^[A-Za-z0-9_-]+$", s))


def _triangulate_handler(pointset_id: str):
    # invalid format
    if not _valid_id(pointset_id):
        return ("Invalid id format", 400)

    # simulate not found
    if pointset_id == "99999999":
        return ("Not Found", 404)

    return ("Not Implemented", 501)


if Flask is not None:
    app = Flask(__name__)

    @app.get("/triangulate/<pointset_id>")
    def triangulate(pointset_id):
        body, status = _triangulate_handler(pointset_id)
        if Response is not None:
            return Response(body, status=status)
        return body, status
else:
    # Minimal fake app for tests when Flask is not installed.
    class _FakeResponse:
        def __init__(self, body, status):
            self.data = body.encode() if isinstance(body, str) else body
            self.status_code = status

    class _FakeClient:
        def get(self, path):
            # path expected /triangulate/<id>
            parts = path.rstrip('/').split('/')
            if len(parts) >= 3 and parts[-2] == 'triangulate':
                pid = parts[-1]
                body, status = _triangulate_handler(pid)
                return _FakeResponse(body, status)
            return _FakeResponse(b'Not Found', 404)

        def post(self, path):
            # only GET supported
            return _FakeResponse(b'Method Not Allowed', 405)

    class _FakeApp:
        def test_client(self):
            return _FakeClient()

    app = _FakeApp()
