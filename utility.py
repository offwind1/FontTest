def add_point(*args):
    ox, oy = 0, 0
    for x, y in args:
        ox += x
        oy += y

    return ox, oy


def add_point_x(*args):
    x, y = add_point(*args)
    return x


def add_point_y(*args):
    x, y = add_point(*args)
    return y
