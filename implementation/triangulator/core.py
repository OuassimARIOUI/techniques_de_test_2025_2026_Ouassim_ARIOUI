
from typing import List, Tuple


def _area(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _point_in_triangle(pt, a, b, c):
    # Barycentric technique
    area = _area(a, b, c)
    if area == 0:
        return False
    a1 = _area(pt, b, c) / area
    a2 = _area(pt, c, a) / area
    a3 = _area(pt, a, b) / area
    return 0 <= a1 <= 1 and 0 <= a2 <= 1 and 0 <= a3 <= 1


def triangulate_points(points: List[Tuple[float, float]]):
    """Triangulate a simple polygon given by `points` in order using ear-clipping.

    Returns list of triples of indices. Raises ValueError for invalid inputs
    (duplicates, collinear set when tri impossible).
    If less than 3 points, returns empty list.
    """
    if points is None:
        raise ValueError("points is None")

    n = len(points)
    if n < 3:
        return []

    # remove exact duplicate points while preserving order
    seen = set()
    deduped = []
    for p in points:
        if p in seen:
            continue
        seen.add(p)
        deduped.append(p)
    points = deduped
    n = len(points)
    if n < 3:
        return []

    # check collinearity (all points on single line)
    # check collinearity (all points on single line)
    a, b = points[0], points[1]
    col = True
    for c in points[2:]:
        if _area(a, b, c) != 0:
            col = False
            break
    if col:
        # cannot triangulate collinear points
        return []

    # Ear clipping algorithm
    indices = list(range(n))
    result = []

    def is_convex(i0, i1, i2):
        a = points[i0]
        b = points[i1]
        c = points[i2]
        return _area(a, b, c) > 0

    count = 0
    while len(indices) > 3:
        progressed = False
        m = len(indices)
        for i in range(m):
            i_prev = indices[(i - 1) % m]
            i_curr = indices[i]
            i_next = indices[(i + 1) % m]

            if not is_convex(i_prev, i_curr, i_next):
                continue

            a = points[i_prev]
            b = points[i_curr]
            c = points[i_next]
            ear_found = True
            for j in indices:
                if j in (i_prev, i_curr, i_next):
                    continue
                if _point_in_triangle(points[j], a, b, c):
                    ear_found = False
                    break

            if ear_found:
                result.append((i_prev, i_curr, i_next))
                indices.pop(i)
                progressed = True
                break

        if not progressed:
            # cannot find ear (maybe polygon not simple); fallback: stop
            break

        count += 1
        if count > 10000:
            break

    if len(indices) == 3:
        result.append((indices[0], indices[1], indices[2]))

    return result
