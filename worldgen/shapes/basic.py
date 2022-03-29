def sphere(x, y, z):
    """(x-x0)^2 + (y-y0)^2 + (z-z0)^2 - r^2 = 0"""
    x0 = 8
    y0 = 8
    z0 = 8
    r = 4
    return r * r - ((x - x0) * (x - x0) + (y - y0) * (y - y0) + (z - z0) * (z - z0))


def hyperboloid(x, y, z):
    r = 4
    offset = 8
    """(x-x0)^2 + (y-y0)^2 + (z-z0)^2 - r^2 = 0"""
    return (x - offset) * (x - offset) - (y - offset) * (y - offset) + (z - offset) * (z - offset) - r * r
