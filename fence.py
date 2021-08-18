import config as cfg
from common import Directions


def get_fence_node_idx(x, y):
    return x * (cfg.N + 1) + y


def get_fence_node_dirs(node_idx):
    col = node_idx % (cfg.N + 1)
    row = (node_idx - col) // (cfg.N + 1)
    return row, col


def fence_border(node_idx):
    row, col = get_fence_node_dirs(node_idx)
    borders = []
    if row == 0:
        borders.append(Directions.Up)
    if row == cfg.N:
        borders.append(Directions.Down)
    if col == 0:
        borders.append(Directions.Left)
    if col == cfg.N:
        borders.append(Directions.Right)
    return borders


def get_node_neighbours(neighbour_direction, row, column):
    try:
        node = get_fence_node_idx(row, column)
        if node < 0 or node > (cfg.N + 1) ** 2:
            raise NameError("NodeIndexValueError")
    except NameError:
        print("NodeIndexValue: ", node)
        raise

    if neighbour_direction == Directions.Up and Directions.Up not in fence_border(node):
        return get_fence_node_idx(row - 1, column)

    elif neighbour_direction == Directions.Right and Directions.Right not in fence_border(node):
        return get_fence_node_idx(row, column + 1)

    elif neighbour_direction == Directions.Down and Directions.Down not in fence_border(node):
        return get_fence_node_idx(row + 1, column)

    elif neighbour_direction == Directions.Left and Directions.Left not in fence_border(node):
        return get_fence_node_idx(row, column - 1)

