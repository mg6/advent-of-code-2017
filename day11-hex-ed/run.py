#!/usr/bin/env python3

N  = 'n'
NE = 'ne'
SE = 'se'
S  = 's'
SW = 'sw'
NW = 'nw'


def cube_to_qr(p):
    """Convert cube coordinates to axial in q-type hexagonal grid."""
    x, y, z = p
    q, r = x, z
    return q, r


def qr_to_cube(p):
    """Convert axial coordinates to cube in q-type hexagonal grid."""
    q, r = p
    x, y, z = q, r, -q-r
    return x, y, z


def hex_path_points(movements, start_point=(0, 0)):
    """Generate all points from start, making steps according to movement list."""
    (q, r) = start_point

    for mov in movements:
        if mov == N:
            r -= 1
        elif mov == NE:
            q += 1
            r -= 1
        elif mov == SE:
            q += 1
        elif mov == S:
            r += 1
        elif mov == SW:
            q -= 1
            r += 1
        elif mov == NW:
            q -= 1

        yield q, r


def hex_path(movements, point=(0, 0)):
    """Return final point after performing steps from movement list."""
    for point in hex_path_points(movements, point):
        pass
    return point


def hex_distance(a=(0, 0), b=(0, 0)):
    """Return distance between two points in axial coordinate system."""
    ax, ay, az = qr_to_cube(a)
    bx, by, bz = qr_to_cube(b)
    return max(abs(ax - bx), abs(ay - by), abs(az - bz))


def puzzle_final_distance(movements):
    """Get final distance from the beginning."""
    return hex_distance(hex_path(movements))


def puzzle_max_distance(movements):
    """Return maximal distance from the beginning along the path."""
    return max(hex_distance(p) for p in hex_path_points(movements))


assert hex_path([NE, NE, NE]) == (3, -3)
assert hex_path([NE, NE, SW, SW]) == (0, 0)
assert hex_path([NE, NE, S, S]) == (2, 0)
assert hex_path([SE, SW, SE, SW, SW]) == (-1, 3)

assert hex_distance(hex_path([NE, NE, NE])) == 3
assert hex_distance(hex_path([NE, NE, SW, SW])) == 0
assert hex_distance(hex_path([NE, NE, S, S])) == 2
assert hex_distance(hex_path([SE, SW, SE, SW, SW])) == 3


if __name__ == '__main__':
    with open('input') as f:
        s = f.read().strip()
        movements = s.split(',')
        print(puzzle_final_distance(movements))
        print(puzzle_max_distance(movements))
