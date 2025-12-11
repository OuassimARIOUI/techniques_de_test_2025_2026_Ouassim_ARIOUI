import struct
import math


def decode_pointset(binary_data: bytes):
    """Decode a PointSet from binary format.

    Format expected:
      - 4 bytes unsigned long: number of points (N)
      - N * (4 bytes float X + 4 bytes float Y)

    Returns list of (x, y) tuples.
    Raises ValueError on invalid/corrupted input.
    """
    if not isinstance(binary_data, (bytes, bytearray)):
        raise ValueError("binary_data must be bytes")

    # need at least 4 bytes for the count
    if len(binary_data) < 4:
        raise ValueError("data too short for header")

    try:
        count = struct.unpack_from("I", binary_data, 0)[0]
    except struct.error as e:
        raise ValueError("cannot unpack header") from e

    expected_size = 4 + count * 8
    if len(binary_data) != expected_size:
        raise ValueError(f"invalid data size: expected {expected_size}, got {len(binary_data)}")

    pts = []
    offset = 4
    for i in range(count):
        try:
            x, y = struct.unpack_from("ff", binary_data, offset)
        except struct.error as e:
            raise ValueError("cannot unpack point data") from e
        if math.isnan(x) or math.isnan(y):
            raise ValueError("NaN value in pointset")
        pts.append((x, y))
        offset += 8

    return pts


def encode_triangles(triangles):
    """Encode triangle index list into binary: [count][i0][i1][i2]...[...]

    triangles: iterable of triple indices (ints)
    Returns bytes.
    """
    if triangles is None:
        raise ValueError("triangles is None")

    tlist = list(triangles)
    count = len(tlist)
    # pack header then indices
    fmt = "I" + "III" * count
    values = [count]
    for tri in tlist:
        if not (isinstance(tri, (list, tuple)) and len(tri) == 3):
            raise ValueError("each triangle must be a triple of indices")
        values.extend([int(tri[0]), int(tri[1]), int(tri[2])])

    return struct.pack(fmt, *values)
