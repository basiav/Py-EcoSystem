import config as cfg
from common import Directions, random, check_terrain_boundaries, error_exit, Colour

node_colours = [Colour.White for _ in range((cfg.N + 1) ** 2)]


def paint_fence_white():
    global node_colours
    node_colours = [Colour.White for _ in range((cfg.N + 1) ** 2)]


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
        # if not (Directions.Up in fence_border(upper_left_node_idx)) and not (Directions.Up in fence_border(
        #         upper_right_node_idx)):
        return upper_left_node_idx, upper_right_node_idx

    elif direction == Directions.Right:
        upper_right_node_idx = get_fence_node_idx(x_coord, y_coord + 1)
        lower_right_node_idx = get_fence_node_idx(x_coord + 1, y_coord + 1)
        # if not (Directions.Right in fence_border(upper_right_node_idx)) and not (Directions.Right in fence_border(
        #         lower_right_node_idx)):
        return upper_right_node_idx, lower_right_node_idx

    elif direction == Directions.Down:
        lower_left_node_idx = get_fence_node_idx(x_coord + 1, y_coord)
        lower_right_node_idx = get_fence_node_idx(x_coord + 1, y_coord + 1)
        # if not (Directions.Down in fence_border(lower_right_node_idx)) and not (Directions.Down in fence_border(
        #         lower_right_node_idx)):
        return lower_left_node_idx, lower_right_node_idx

    elif direction == Directions.Left:
        upper_left_node_idx = get_fence_node_idx(x_coord, y_coord)
        lower_left_node_idx = get_fence_node_idx(x_coord + 1, y_coord)
        # if not (Directions.Left in fence_border(upper_left_node_idx)) and not (Directions.Left in fence_border(
        #         lower_left_node_idx)):
        return upper_left_node_idx, lower_left_node_idx


def get_move_direction(delta_x, delta_y):
    if delta_x == 0 and delta_y == 1:
        return Directions.Up
    elif delta_x == 1 and delta_y == 1:
        return Directions.Up_Right
    elif delta_x == 1 and delta_y == 0:
        return Directions.Right
    elif delta_x == 1 and delta_y == -1:
        return Directions.Down_Right
    elif delta_x == 0 and delta_y == -1:
        return Directions.Down
    elif delta_x == -1 and delta_y == -1:
        return Directions.Down_Left
    elif delta_x == -1 and delta_y == 0:
        return Directions.Left
    elif delta_x == -1 and delta_y == 1:
        return Directions.Up_Left


def can_make_move(current_row, current_column, delta_x, delta_y):
    if not check_terrain_boundaries(current_row - delta_y, current_column + delta_x):  # Column-Row/X_coord-Y_coord
        # modification
        return False

    move_direction = get_move_direction(delta_x, delta_y)
    if move_direction in [Directions.Up, Directions.Right, Directions.Down, Directions.Left]:
        surrounding_node_idx_1, surrounding_node_idx_2 = get_surrounding_nodes(move_direction, current_row,
                                                                               current_column)
        if surrounding_node_idx_1 and surrounding_node_idx_2:
            return not check_if_wall_exists(surrounding_node_idx_1, surrounding_node_idx_2)

    elif move_direction in [Directions.Up_Right, Directions.Down_Right, Directions.Down_Left, Directions.Up_Left]:
        if move_direction == Directions.Up_Right:
            can_move_right_up, can_move_up_right = False, False
            surrounding_node_idx_1, surrounding_node_idx_2 = get_surrounding_nodes(Directions.Right, current_row,
                                                                                   current_column)
            if surrounding_node_idx_1 and surrounding_node_idx_2:
                can_move_right = not check_if_wall_exists(surrounding_node_idx_1, surrounding_node_idx_2)
                can_move_up = can_make_move(current_row, current_column + 1, 0, 1)
                can_move_right_up = can_move_right and can_move_up
            surrounding_node_idx_1, surrounding_node_idx_2 = get_surrounding_nodes(Directions.Up, current_row,
                                                                                   current_column)
            if surrounding_node_idx_1 and surrounding_node_idx_2:
                can_move_up = not check_if_wall_exists(surrounding_node_idx_1, surrounding_node_idx_2)
                can_move_right = can_make_move(current_row - 1, current_column, 1, 0)
                can_move_up_right = can_move_up and can_move_right

            return can_move_right_up or can_move_up_right

        elif move_direction == Directions.Down_Right:
            can_move_right_down, can_move_down_right = False, False
            surrounding_node_idx_1, surrounding_node_idx_2 = get_surrounding_nodes(Directions.Right, current_row,
                                                                                   current_column)
            if surrounding_node_idx_1 and surrounding_node_idx_2:
                can_move_right = not check_if_wall_exists(surrounding_node_idx_1, surrounding_node_idx_2)
                can_move_down = can_make_move(current_row, current_column + 1, 0, -1)
                can_move_right_down = can_move_right and can_move_down

            surrounding_node_idx_1, surrounding_node_idx_2 = get_surrounding_nodes(Directions.Down, current_row,
                                                                                   current_column)
            if surrounding_node_idx_1 and surrounding_node_idx_2:
                can_move_down = not check_if_wall_exists(surrounding_node_idx_1, surrounding_node_idx_2)
                can_move_right = can_make_move(current_row + 1, current_column, 1, 0)
                can_move_down_right = can_move_down and can_move_right

            return can_move_right_down or can_move_down_right

        elif move_direction == Directions.Down_Left:
            can_move_left_down, can_move_down_left = False, False
            surrounding_node_idx_1, surrounding_node_idx_2 = get_surrounding_nodes(Directions.Left, current_row,
                                                                                   current_column)
            if surrounding_node_idx_1 and surrounding_node_idx_2:
                can_move_left = not check_if_wall_exists(surrounding_node_idx_1, surrounding_node_idx_2)
                can_move_down = can_make_move(current_row, current_column - 1, 0, -1)
                can_move_left_down = can_move_left and can_move_down

            surrounding_node_idx_1, surrounding_node_idx_2 = get_surrounding_nodes(Directions.Down, current_row,
                                                                                   current_column)
            if surrounding_node_idx_1 and surrounding_node_idx_2:
                can_move_down = not check_if_wall_exists(surrounding_node_idx_1, surrounding_node_idx_2)
                can_move_left = can_make_move(current_row + 1, current_column, -1, 0)
                can_move_down_left = can_move_down and can_move_left

            return can_move_left_down or can_move_down_left

        elif move_direction == Directions.Up_Left:
            can_move_left_up, can_move_up_left = False, False
            surrounding_node_idx_1, surrounding_node_idx_2 = get_surrounding_nodes(Directions.Left, current_row,
                                                                                   current_column)
            if surrounding_node_idx_1 and surrounding_node_idx_2:
                can_move_left = not check_if_wall_exists(surrounding_node_idx_1, surrounding_node_idx_2)
                can_move_up = can_make_move(current_row, current_column - 1, 0, 1)
                can_move_left_up = can_move_left and can_move_up
            surrounding_node_idx_1, surrounding_node_idx_2 = get_surrounding_nodes(Directions.Up, current_row,
                                                                                   current_column)
            if surrounding_node_idx_1 and surrounding_node_idx_2:
                can_move_up = not check_if_wall_exists(surrounding_node_idx_1, surrounding_node_idx_2)
                can_move_left = can_make_move(current_row - 1, current_column, -1, 0)
                can_move_up_left = can_move_up and can_move_left

            return can_move_left_up or can_move_up_left

    else:
        return False


def add_vertex(node_idx_1, node_idx_2):
    cfg.fence[node_idx_1].append(node_idx_2)


def delete_vertex(node_idx_1, node_idx_2):
    cfg.fence[node_idx_1].remove(node_idx_2)


def check_if_wall_exists(node_idx_1, node_idx_2):
    return node_idx_2 in cfg.fence[node_idx_1] or node_idx_1 in cfg.fence[node_idx_2]


def build_vertex(start_node, end_node):
    allowed_proximity_directions = [Directions.Up, Directions.Right, Directions.Down, Directions.Left]
    if neighbours_relations(start_node, end_node) not in allowed_proximity_directions and \
            neighbours_relations(end_node, start_node) not in allowed_proximity_directions:
        error_exit("fence.py", "build_vertex", "Given nodes are not neighbours, thus wall cannot be built")
    elif end_node in cfg.fence[start_node] and start_node in cfg.fence[end_node]:
        delete_vertex(end_node, start_node)  # Removing redundancy
    elif not check_if_wall_exists(start_node, end_node):
        add_vertex(start_node, end_node)


def build_wall(from_node, to_node):
    pass


def delete_all_walls():
    for i in range(0, ((cfg.N + 1) ** 2) - 1):
        # cfg.fence[i].clear()
        cfg.fence[i] = list()


def reset_fence():
    delete_all_walls()
    paint_fence_white()


def get_random_factor(walls_already_built, wall_no):
    if walls_already_built < (wall_no // 2):
        random_factor = True
    else:
        random_factor = False
    if random.randint(0, 1) % 2 == 0:
        random_factor = True
    return random_factor


def reset_node_colours():
    global node_colours
    node_colours = [Colour.White for _ in range((cfg.N + 1) ** 2)]


def dfs_build(start_node_idx):
    # reset_fence()
    # print("dfs_config_build | N: ", cfg.N)
    reset_node_colours()
    start_row, start_col = int(1 / 2 * cfg.N), int(1 / 2 * cfg.N)
    start_node_idx = get_fence_node_idx(start_row, start_col)
    max_wall_length = int(cfg.N * 2 / 3)
    for i in range(0, cfg.fence_elements):
        if i >= 1:
            start_row, start_col = int(0.8 * cfg.N), int(0.8 * cfg.N)
            start_node_idx = get_fence_node_idx(start_row, start_col)
            max_wall_length = int(cfg.N * 2 / 3)
        if bool(fence_border(start_node_idx)):
            print("[fence.py] [dfs_build] error: start_node_idx turned out to be at map border, illegal placement. "
                  "Repeat the procedure.")
            i -= 1
            continue
        dfs_visit(start_node_idx, max_wall_length, 0)

    # print("Fence", cfg.fence)


def dfs_visit(current_node, wall_no, walls_already_built):
    node_colours[current_node] = Colour.Grey

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

        if chosen_neighbour and not check_if_wall_exists(current_node, chosen_neighbour) and \
                node_colours[chosen_neighbour] is Colour.White:
            build_vertex(current_node, chosen_neighbour)
            dfs_visit(chosen_neighbour, wall_no, walls_already_built + 1)
            if len(possible_dirs_set) <= 1:
                return

        # if len(possible_dirs_set) <= 1:
        #     # node_colours[current_node] = Colour.Black
        #     return
