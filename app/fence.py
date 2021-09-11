import config as cfg
from common import Directions, random, check_terrain_boundaries, error_exit, Colour

node_colours = [Colour.White for _ in range((cfg.N + 1) ** 2)]
parents = [None for _ in range((cfg.N + 1) ** 2)]
children = [None for _ in range((cfg.N + 1) ** 2)]


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


def delete_wall(start_node, end_node):
    allowed_proximity_directions = [Directions.Up, Directions.Right, Directions.Down, Directions.Left]
    if neighbours_relations(start_node, end_node) not in allowed_proximity_directions and \
            neighbours_relations(end_node, start_node) not in allowed_proximity_directions:
        error_exit("fence.py", "build_vertex", "Given nodes are not neighbours, thus wall cannot be deleted")
    elif end_node in cfg.fence[start_node]:
        delete_vertex(start_node, end_node)
    elif start_node in cfg.fence[end_node]:
        delete_vertex(end_node, start_node)


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


def reset_parents():
    global parents
    parents = [None for _ in range((cfg.N + 1) ** 2)]


def get_random_corner_fence_location(randint_1, randint_2):
    start_row = random.randint(int(0.1 * cfg.N), int(0.5 * cfg.N)) if randint_1 % 2 == 0 \
        else random.randint(int(0.5 * cfg.N), int(0.9 * cfg.N))
    start_col = random.randint(int(0.1 * cfg.N), int(0.5 * cfg.N)) if randint_2 % 2 == 0 \
        else random.randint(int(0.5 * cfg.N), int(0.9 * cfg.N))
    return start_row, start_col


def dfs_build(start_node_idx):
    # reset_fence()
    # print("dfs_config_build | N: ", cfg.N)
    reset_node_colours()
    reset_parents()
    start_row, start_col = int(1 / 2 * cfg.N), int(1 / 2 * cfg.N)
    start_node_idx = get_fence_node_idx(start_row, start_col)
    parents[start_node_idx] = start_node_idx
    if cfg.fence_elements <= 1:
        max_wall_length = int(cfg.N)
    elif cfg.fence_elements <= 3:
        max_wall_length = int(cfg.N * 3 / 4)
    else:
        max_wall_length = int(cfg.N * 2 / 3)
    for i in range(0, cfg.fence_elements):
        if i >= 1:
            start_row, start_col = get_random_corner_fence_location(random.randint(0, 1), random.randint(0, 1))
            start_node_idx = get_fence_node_idx(start_row, start_col)
        if bool(fence_border(start_node_idx)):
            print("[fence.py] [dfs_build] error: start_node_idx turned out to be at map border, illegal placement. "
                  "Repeat the procedure.")
            i -= 1
            continue
        dfs_visit(start_node_idx, max_wall_length, 0)
        # get_more_paths(get_fence_node_dirs(start_node_idx)[0], get_fence_node_dirs(start_node_idx)[1], 10, 10)
    idx_1 = random.choice([x for x in parents if x is not None])
    idx_2 = random.choice([x for x in parents if x is not None])
    res = get_first_common_parent(idx_1, idx_2, start_node_idx)
    print(res)
    print("start_node_idx", start_node_idx, "idx_1", idx_1, "idx_2", idx_2)
    print("idx_1 PARENT PATH")
    print_parent_path(idx_1)
    print("idx_2 PARENT PATH")
    print_parent_path(idx_2)
    get_maze_path(idx_1, idx_2, start_node_idx)
    # reverse_path(idx_1, start_node_idx)
    # print_reversed_path(start_node_idx, idx_1)
    # print("Fence", cfg.fence)


def dfs_visit(current_node, wall_no, walls_already_built):
    global node_colours, parents
    node_colours[current_node] = Colour.Grey

    if walls_already_built >= wall_no:
        return

    possible_dirs_set = {1, 2, 3, 4}
    neighbours = []
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
            parents[chosen_neighbour] = current_node
            neighbours.append(chosen_neighbour)
            dfs_visit(chosen_neighbour, wall_no, walls_already_built + 1)
            if len(possible_dirs_set) <= 1:
                node_colours[current_node] = Colour.Black
                # random_neighbour = random.choice(neighbours)
                # if random.randint(0, 4) % 3 == 0:
                #     delete_wall(random_neighbour, current_node)
                return

        # if len(possible_dirs_set) <= 1:
        #     # node_colours[current_node] = Colour.Black
        #     return


def get_more_paths(start_row, start_col, end_row, end_col):
    global node_colours
    start_surrounding_nodes = [get_surrounding_nodes(Directions(i), start_row, start_col)[_] for _ in range(0, 2) for i
                               in range(1, 5)]
    start_surrounding_nodes = list(set(start_surrounding_nodes))
    end_surrounding_nodes = [get_surrounding_nodes(Directions(i), end_row, end_col)[_] for _ in range(0, 2) for i
                             in range(1, 5)]
    end_surrounding_nodes = list(set(end_surrounding_nodes))
    print(start_surrounding_nodes)
    print(end_surrounding_nodes)
    for node in start_surrounding_nodes:
        if node_colours[node] is Colour.Grey:
            previous_grey_node, black_node = get_next_black_node(node, node)
            print(previous_grey_node, black_node)
            while previous_grey_node != black_node:
                print(previous_grey_node, black_node)
                delete_wall(previous_grey_node, black_node)
                node = get_next_black_node(black_node, previous_grey_node)[1]
                previous_grey_node, black_node = get_next_black_node(node, previous_grey_node)


def get_maze_path(start_node, end_node, start_node_idx):
    first_common_parent = get_first_common_parent(start_node, end_node, start_node_idx)
    node_with_shorter_path = first_common_parent["node_with_shorter_path"]
    node_with_longer_path = start_node if node_with_shorter_path == end_node else end_node
    first_common_node_idx = first_common_parent["first_common_idx"]

    reverse_path(node_with_shorter_path, first_common_node_idx)
    print_reversed_path(first_common_node_idx, node_with_shorter_path)

    start_next_black_node = get_next_black_node(node_with_longer_path, node_with_longer_path)[1]
    next_black_node = get_next_black_node(start_next_black_node, start_next_black_node)[1]
    if next_black_node in cfg.fence[start_next_black_node]:
        starting_node = next_black_node
    else:
        starting_node = start_next_black_node
    



def get_next_black_node(current_node, previous_node):
    global node_colours
    if current_node < 0 or current_node > (cfg.N + 1) ** 2 or node_colours[current_node] is Colour.White:
        return previous_node, previous_node
    if node_colours[current_node] is Colour.Black:
        # node_colours[current_node] = Colour.Grey
        return previous_node, current_node

    possible_dirs_set = {1, 2, 3, 4}
    while possible_dirs_set:
        dir_no = random.sample(possible_dirs_set, 1)  # returned in a form a list
        possible_dirs_set.remove(dir_no[0])
        direction = Directions(dir_no[0])

        current_row, current_col = get_fence_node_dirs(current_node)
        chosen_neighbour = get_node_neighbour(direction, current_row, current_col)
        if chosen_neighbour:
            return get_next_black_node(chosen_neighbour, current_node)
    return current_node, current_node


def get_first_common_parent(node_idx_1, node_idx_2, start_node_idx):
    global parents
    node_idx_1_parent_path = set()
    i = node_idx_1
    node_idx_1_parent_path.add(i)
    while i != start_node_idx:
        node_idx_1_parent_path.add(parents[i])
        i = parents[i]
    i = node_idx_2
    length = 0
    while i != start_node_idx:
        length += 1
        if i in node_idx_1_parent_path:
            node_with_shorter_path = node_idx_2 if length < len(node_idx_1_parent_path) else node_idx_1
            return {
                "node_with_shorter_path": node_with_shorter_path,
                "first_common_idx": i,
                "path_length": length if length < len(node_idx_1_parent_path) else len(node_idx_1_parent_path)
            }
        i = parents[i]
    print("No common path")
    return False


def print_parent_path(node_idx):
    print(node_idx)
    if node_idx == parents[node_idx]:
        return
    print_parent_path(parents[node_idx])


def print_reversed_path(node_from, node_to):
    if children[node_from] is None or node_from == node_to:
        return
    print("Reversed path", node_from)
    print_reversed_path(children[node_from], node_to)


# children = [None for _ in range((cfg.N + 1) ** 2)]
def reverse_path(node_beginning, node_end):
    global parents, children
    if node_beginning == node_end:
        # children[node_beginning] = node_beginning
        # print("End point | CHILD of ", node_beginning, "is",  children[node_beginning])
        return
    children[parents[node_beginning]] = node_beginning
    # print("CHILD of ", node_beginning, "is", children[node_beginning])
    reverse_path(parents[node_beginning], node_end)
