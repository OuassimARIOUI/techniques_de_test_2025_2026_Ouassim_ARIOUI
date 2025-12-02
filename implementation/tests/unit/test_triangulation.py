from triangulator.core import triangulate_points

def test_triangle_basic_case():
    pts = [(0,0), (1,0), (0,1)]
    tris = triangulate_points(pts)
    assert tris == [(0,1,2)]

def test_square_two_triangles():
    pts = [(0,0),(1,0),(1,1),(0,1)]
    result = triangulate_points(pts)
    assert len(result) == 2

def test_convex_hexagon():
    pts = [(0,0),(2,0),(3,1),(2,2),(0,2),(-1,1)]
    result = triangulate_points(pts)
    assert len(result) == 4

def test_collinear_points():
    pts = [(0,0),(1,0),(2,0)]
    triangulate_points(pts)    # must fail

def test_duplicate_points():
    pts = [(0,0),(1,0),(1,0),(0,1)]
    triangulate_points(pts)    # must fail

def test_empty_input():
    triangulate_points([])

def test_single_point():
    triangulate_points([(0,0)])

def test_two_points():
    triangulate_points([(0,0),(1,0)])
