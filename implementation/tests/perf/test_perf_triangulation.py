import pytest
from triangulator.core import triangulate_points

@pytest.mark.perf
def test_perf_large_triangulation():
    pts = [(i, i*2 % 17) for i in range(5000)]
    result = triangulate_points(pts)
    assert len(result) > 0
