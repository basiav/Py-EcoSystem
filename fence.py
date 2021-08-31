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


def get_surrounding_nodes(direction, x_coord, y_coord):
    if direction == Directions.Up:
        upper_left_node_idx = get_fence_node_idx(x_coord, y_coord)
        upper_right_node_idx = get_fence_node_idx(x_coord, y_coord + 1)
        if not (Directions.Up in fence_border(upper_left_node_idx)) and not (Directions.Up in fence_border(
                upper_right_node_idx)):
            return upper_left_node_idx, upper_right_node_idx

    elif direction == Directions.Right:
        upper_right_node_idx = get_fence_node_idx(x_coord, y_coord + 1)
        lower_right_node_idx = get_fence_node_idx(x_coord + 1, y_coord + 1)
        if not (Directions.Right in fence_border(upper_right_node_idx)) and not (Directions.Right in fence_border(
                lower_right_node_idx)):
            return upper_right_node_idx, lower_right_node_idx

    elif direction == Directions.Down:
        lower_left_node_idx = get_fence_node_idx(x_coord + 1, y_coord)
        lower_right_node_idx = get_fence_node_idx(x_coord + 1, y_coord + 1)
        if not (Directions.Down in fence_border(lower_right_node_idx)) and not (Directions.Down in fence_border(
                lower_right_node_idx)):
            return lower_left_node_idx, lower_right_node_idx

    elif direction == Directions.Left:
        upper_left_node_idx = get_fence_node_idx(x_coord, y_coord)
        lower_left_node_idx = get_fence_node_idx(x_coord + 1, y_coord)
        if not (Directions.Left in fence_border(upper_left_node_idx)) and not (Directions.Left in fence_border(
                lower_left_node_idx)):
            return upper_left_node_idx, lower_left_node_idx


def get_move_direction(delta_x, delta_y):
    if delta_x == 0 and delta_y == 1:
        return Directions.Up
    elif delta_x == 1 and delta_y == 0:
        return Directions.Right
    elif delta_x == 0 and delta_y == -1:
        return Directions.Down
    elif delta_x == -1 and delta_y == 0:
        return Directions.Left


def can_make_move(current_x, current_y, delta_x, delta_y):
    move_direction = get_move_direction(delta_x, delta_y)
    surrounding_node_idx_1, surrounding_node_idx_2 = get_surrounding_nodes(move_direction, current_x, current_y)
    return not check_if_wall_exists(surrounding_node_idx_1, surrounding_node_idx_2)


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
    print(bool(fence_border(start_node_idx)))
    dfs_visit(start_node_idx, 20, 0)
    print("Fence", cfg.fence)


def dfs_visit(current_node, wall_no, walls_already_built):
    if walls_already_built >= wall_no:
        return

    possible_dirs_set = {1, 2, 3, 4}
    while possible_dirs_set:
        dir_no = random.sample(possible_dirs_set, 1)  # returned in a form a list
        possible_dirs_set.remove(dir_no[0])
        direction = Directions(dir_no[0])

        # Checking whether we can follow that direction: whether a wall exists - and more??? for the future
        current_row, current_col = get_fence_node_dirs(current_node)
        chosen_neighbour = get_node_neighbour(direction, current_row, current_col)

        if chosen_neighbour and not check_if_wall_exists(current_node, chosen_neighbour):
            build_vertex(current_node, chosen_neighbour)
            dfs_visit(chosen_neighbour, wall_no, walls_already_built + 1)
