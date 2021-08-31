import config as cfg
from common import Directions, random


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


def get_node_neighbour(neighbour_direction, row, column):
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


def neighbours_relations(node, neighbour):
    if get_node_neighbour(Directions.Up, get_fence_node_dirs(node)[0], get_fence_node_dirs(node)[1]) == neighbour:
        return Directions.Up
    elif get_node_neighbour(Directions.Right, get_fence_node_dirs(node)[0], get_fence_node_dirs(node)[1]) == neighbour:
        return Directions.Right
    elif get_node_neighbour(Directions.Down, get_fence_node_dirs(node)[0], get_fence_node_dirs(node)[1]) == neighbour:
        return Directions.Down
    elif get_node_neighbour(Directions.Left, get_fence_node_dirs(node)[0], get_fence_node_dirs(node)[1]) == neighbour:
        return Directions.Left


def add_vertex(node_idx_1, node_idx_2):
    cfg.fence[node_idx_1].append(node_idx_2)


def delete_vertex(node_idx_1, node_idx_2):
    cfg.fence[node_idx_1].remove(node_idx_2)


def check_if_wall_exists(node_idx_1, node_idx_2):
    return node_idx_2 in cfg.fence[node_idx_1] or node_idx_1 in cfg.fence[node_idx_2]


def build_vertex(start_node, end_node):
    if end_node in cfg.fence[start_node] and start_node in cfg.fence[end_node]:
        delete_vertex(end_node, start_node)  # Removing redundancy
    elif not check_if_wall_exists(start_node, end_node):
        add_vertex(start_node, end_node)


def build_wall(from_node, to_node):
    pass


def dfs_build(start_node_idx):
    for neighbour in cfg.fence[start_node_idx]:
        print(neighbour)
        dfs_visit(neighbour, 1, 17)
    print("Fence", cfg.fence)


def dfs_visit(current_node, i, max_rounds):
    if i > max_rounds:
        return

    # for dir in Directions:
    #     next_row, next_col = get_fence_node_dirs(current_node)
    #     next_node = get_node_neighbour(dir, next_row, next_col)
    #     if next_node and bool(fence_border(next_node)):
    #         build_vertex(current_node, next_node)
    #         dfs_visit(next_node, i + 1, max_rounds)
    repeat = True
    while repeat:
        dir_no = random.randint(1, 4)
        dir = Directions(dir_no)
        print(dir)
        next_row, next_col = get_fence_node_dirs(current_node)
        next_node = get_node_neighbour(dir, next_row, next_col)
        if next_node and bool(fence_border(next_node)):
            repeat = False
            build_vertex(current_node, next_node)
            dfs_visit(next_node, i + 1, max_rounds)
