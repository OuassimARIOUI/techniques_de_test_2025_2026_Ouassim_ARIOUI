"""
Minimal HTTP API wrapper used by tests.

This module exposes a small `/triangulate/<id>` endpoint. When Flask is not
available a tiny fake application is provided so tests can run without the
dependency.
"""

try:
    from flask import Flask, Response
except Exception:
    Flask = None
    Response = None

import re

import requests

from .binary_utils import decode_pointset, encode_triangles
from .core import triangulate_points


def _valid_id(s: str) -> bool:
    """
    Return True when ``s`` is an allowed identifier for pointset ids.

    Allowed characters are ASCII letters, digits, underscore and hyphen.
    """
    return bool(re.match(r"^[A-Za-z0-9_-]+$", s))


def _triangulate_handler(pointset_id: str):
    """
    Handle triangulation requests in a test-friendly way.

    This simplified handler validates the id format and simulates a
    "not found" case for the id "99999999". The real implementation is not
    part of the teaching exercises and returns 501 for other ids.
    """
    # invalid format
    if not _valid_id(pointset_id):
        return (b"Invalid id format", 400, "text/plain")

    # contact PointSetManager (PSM)
    psm_url = f"http://localhost:9999/pointset/{pointset_id}"
    try:
        r = requests.get(psm_url, timeout=1.0)
    except Exception:
        # PSM unreachable -> service unavailable
        return (b"PointSetManager unreachable", 503, "text/plain")

    if r.status_code == 404:
        return (b"Not Found", 404, "text/plain")

    if r.status_code != 200:
        return (b"Bad response from PSM", 502, "text/plain")

    # r.content should be binary PointSet
    try:
        pts = decode_pointset(r.content)
    except ValueError:
        return (b"Corrupted PointSet", 502, "text/plain")

    # triangulate
    try:
        tris = triangulate_points(pts)
    except Exception:
        return (b"Triangulation failed", 500, "text/plain")

    # encode triangles
    try:
        body = encode_triangles(tris)
    except Exception:
        return (b"Encoding failed", 500, "text/plain")

    return (body, 200, "application/octet-stream")


if Flask is not None:
    app = Flask(__name__)

    @app.get("/triangulate/<pointset_id>")
    def triangulate(pointset_id):
        """
        HTTP handler for `/triangulate/<pointset_id>`.

        Returns a Flask `Response` when Flask is available, otherwise a
        (body, status) tuple is returned which the tests also accept.
        """
        body, status, ctype = _triangulate_handler(pointset_id)
        if Response is not None:
            return Response(body, status=status, mimetype=ctype)
        return body, status
else:
    # Minimal fake app for tests when Flask is not installed.
    class _FakeResponse:
        def __init__(self, body, status):
            # body may be bytes or (bytes,str) tuple; set attributes similar to Flask
            self.data = body.encode() if isinstance(body, str) else body
            self.status_code = status
            self.mimetype = "application/octet-stream" 
            if isinstance(body, (bytes, bytearray)) :
                "application/octet-stream"
            else :
               "text/plain"

    class _FakeClient:
        def get(self, path):
            # path expected /triangulate/<id>
            parts = path.rstrip('/').split('/')
            if len(parts) >= 3 and parts[-2] == 'triangulate':
                pid = parts[-1]
                body, status, ctype = _triangulate_handler(pid)
                return _FakeResponse(body, status)
            return _FakeResponse(b'Not Found', 404)

        def post(self, path):
            # only GET supported
            return _FakeResponse(b'Method Not Allowed', 405)

    class _FakeApp:
        def test_client(self):
            return _FakeClient()

    app = _FakeApp()
