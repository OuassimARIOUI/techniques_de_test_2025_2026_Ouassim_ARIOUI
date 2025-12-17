from triangulator.core import triangulate_points


def test_triangle_basic_case():
    pts = [(0, 0), (1, 0), (0, 1)]
    tris = triangulate_points(pts)
    assert tris == [(0, 1, 2)]


def test_square_two_triangles():
    pts = [(0, 0), (1, 0), (1, 1), (0, 1)]
    result = triangulate_points(pts)
    assert len(result) == 2


def test_convex_hexagon():
    pts = [(0, 0), (2, 0), (3, 1), (2, 2), (0, 2), (-1, 1)]
    result = triangulate_points(pts)
    assert len(result) == 4


def test_collinear_points_returns_empty():
    pts = [(0, 0), (1, 0), (2, 0)]
    result = triangulate_points(pts)
    assert result == []


def test_duplicate_points_handled():
    pts = [(0, 0), (1, 0), (1, 0), (0, 1)]
    result = triangulate_points(pts)
    # after deduplication we have 3 points -> one triangle
    assert result == [(0, 1, 2)]


def test_empty_input():
    assert triangulate_points([]) == []


def test_single_point():
    assert triangulate_points([(0, 0)]) == []


def test_two_points():
    assert triangulate_points([(0, 0), (1, 0)]) == []
