"""Fence (maze) generation engine and animal movement limitations due to fence placement."""

import config as cfg
from common import Directions, random, check_terrain_boundaries, error_exit, Colour

node_colours = [Colour.White for _ in range((cfg.N + 1) ** 2)]
parents = [None for _ in range((cfg.N + 1) ** 2)]
children = [None for _ in range((cfg.N + 1) ** 2)]
maze_elements_sets = [set() for _ in range(cfg.fence_elements)]


def paint_fence_white():
    """DFS tree maintenance."""
    global node_colours
    node_colours = [Colour.White for _ in range((cfg.N + 1) ** 2)]


def get_fence_node_idx(x, y):
    """Returns the index of the node given by its' x and y coordinates."""
    return x * (cfg.N + 1) + y


def get_fence_node_dirs(node_idx):
    """Returns x and y coordinates of the given node."""
    col = node_idx % (cfg.N + 1)
    row = (node_idx - col) // (cfg.N + 1)
    return row, col


def fence_border(node_idx):
    """Returns directions in which the given node is adjacent to the map's border, if they exist."""
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
    """Returns a neighbour of the node given by its' coordinates (row and column) and the direction to follow,
    if exists."""
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
    """Returns direction in which arg node borders with arg neighbour, if exists."""
    if get_node_neighbour(Directions.Up, get_fence_node_dirs(node)[0], get_fence_node_dirs(node)[1]) == neighbour:
        return Directions.Up
    elif get_node_neighbour(Directions.Right, get_fence_node_dirs(node)[0], get_fence_node_dirs(node)[1]) == neighbour:
        return Directions.Right
    elif get_node_neighbour(Directions.Down, get_fence_node_dirs(node)[0], get_fence_node_dirs(node)[1]) == neighbour:
        return Directions.Down
    elif get_node_neighbour(Directions.Left, get_fence_node_dirs(node)[0], get_fence_node_dirs(node)[1]) == neighbour:
        return Directions.Left


def get_surrounding_nodes(direction, x_coord, y_coord):
    """Returns all the nodes that border node given by args: x_coord, y_coord, provided that those nodes exist."""
    if direction == Directions.Up:
        upper_left_node_idx = get_fence_node_idx(x_coord, y_coord)
        upper_right_node_idx = get_fence_node_idx(x_coord, y_coord + 1)
        return upper_left_node_idx, upper_right_node_idx

    elif direction == Directions.Right:
        upper_right_node_idx = get_fence_node_idx(x_coord, y_coord + 1)
        lower_right_node_idx = get_fence_node_idx(x_coord + 1, y_coord + 1)
        return upper_right_node_idx, lower_right_node_idx

    elif direction == Directions.Down:
        lower_left_node_idx = get_fence_node_idx(x_coord + 1, y_coord)
        lower_right_node_idx = get_fence_node_idx(x_coord + 1, y_coord + 1)
        return lower_left_node_idx, lower_right_node_idx

    elif direction == Directions.Left:
        upper_left_node_idx = get_fence_node_idx(x_coord, y_coord)
        lower_left_node_idx = get_fence_node_idx(x_coord + 1, y_coord)
        return upper_left_node_idx, lower_left_node_idx


def get_move_direction(delta_x, delta_y):
    """Returns a movement direction given by the x and y vectors."""
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
    """Decides whether an animal can make a certain move or not, considering fence placement and map boundaries.

    :param current_row: current x position of an animal
    :param current_column: current y position of an animal
    :param delta_x: x coordinate of animal's movement vector
    :param delta_y: y coordinate of animal's movement vector
    :return: boolean
    """
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
    """Adds node_idx_2 to node_idx_1's fence-graph neighbours"""
    cfg.fence[node_idx_1].append(node_idx_2)


def delete_vertex(node_idx_1, node_idx_2):
    """Deletes node_idx_2 from node_idx_1's fence-graph neighbours"""
    cfg.fence[node_idx_1].remove(node_idx_2)


def check_if_wall_exists(node_idx_1, node_idx_2):
    """Checks whether a vertex exists between given two nodes."""
    return node_idx_2 in cfg.fence[node_idx_1] or node_idx_1 in cfg.fence[node_idx_2]


def build_vertex(start_node, end_node):
    """Builds a fence wall, first checking whether: - given nodes are placed in proper proximity (they have to be
    direct neighbours for the vertex to exist), - there's no redundancy (end_node will be placed in start_node's
    neighbourhood set and start_node will not be placed in end_node's neighbourhood set, particular node will be
    added to the neighbourhood set just once)
    """
    allowed_proximity_directions = [Directions.Up, Directions.Right, Directions.Down, Directions.Left]
    if neighbours_relations(start_node, end_node) not in allowed_proximity_directions and \
            neighbours_relations(end_node, start_node) not in allowed_proximity_directions:
        error_exit("fence.py", "build_vertex", "Given nodes are not neighbours, thus wall cannot be built")
    elif end_node in cfg.fence[start_node] and start_node in cfg.fence[end_node]:
        delete_vertex(end_node, start_node)  # Removing redundancy
    elif not check_if_wall_exists(start_node, end_node):
        add_vertex(start_node, end_node)


def delete_wall(start_node, end_node):
    """Deletes vertex between the two given nodes, checks whether they are direct neighbours and the vertex exists."""
    allowed_proximity_directions = [Directions.Up, Directions.Right, Directions.Down, Directions.Left]
    if neighbours_relations(start_node, end_node) not in allowed_proximity_directions and \
            neighbours_relations(end_node, start_node) not in allowed_proximity_directions:
        error_exit("fence.py", "delete_wall", "Given nodes are not neighbours, thus wall cannot be deleted")
    elif end_node in cfg.fence[start_node]:
        delete_vertex(start_node, end_node)
    elif start_node in cfg.fence[end_node]:
        delete_vertex(end_node, start_node)


def delete_all_walls():
    """Fence clean-up."""
    for i in range(0, ((cfg.N + 1) ** 2) - 1):
        cfg.fence[i] = list()


def reset_fence():
    """Fence clean-up."""
    delete_all_walls()
    paint_fence_white()


def reset_node_colours():
    """Fence clean-up."""
    global node_colours
    node_colours = [Colour.White for _ in range((cfg.N + 1) ** 2)]


def reset_parents_and_children():
    """Fence clean-up."""
    global parents, children
    parents = [None for _ in range((cfg.N + 1) ** 2)]
    children = [None for _ in range((cfg.N + 1) ** 2)]
    cfg.specials = [False for _ in range((cfg.N + 1) ** 2)]
    cfg.deleted_walls = set()
    cfg.start_end_points = {
        "start": None,
        "end": None,
        "starting_node": None,
        "ending_node": None
    }


def get_random_corner_fence_location(randint_1, randint_2):
    """Returns a randomised fence-generating starting (x, y) position."""
    start_row = random.randint(int(0.1 * cfg.N), int(0.5 * cfg.N)) if randint_1 % 2 == 0 \
        else random.randint(int(0.5 * cfg.N), int(0.9 * cfg.N))
    start_col = random.randint(int(0.1 * cfg.N), int(0.5 * cfg.N)) if randint_2 % 2 == 0 \
        else random.randint(int(0.5 * cfg.N), int(0.9 * cfg.N))
    return start_row, start_col


def get_node_colour(node_idx):
    """Test for DFS-based function."""
    walls_no = 0
    for dir in Directions:
        x, y = get_fence_node_dirs(node_idx)
        neighbour = get_node_neighbour(dir, x, y)
        if neighbour and check_if_wall_exists(neighbour, node_idx):
            walls_no += 1
    colour = Colour.White
    if walls_no == 1 or walls_no == 2:
        colour = Colour.Grey
    elif walls_no == 3 or walls_no == 4:
        colour = Colour.Black
    if colour != node_colours[node_idx]:
        print("[Error in colours]", "node_idx", node_idx, "walls_no", walls_no, node_colours[node_idx])
    return colour


def dfs_build():
    """Generuje n element??w labiryntu (p??otu):
    1. Wyznacza maksymaln?? g????boko???? przeszukiwania w DFS (maksymalna liczba postawionych ??cian p??otu w jednym cyklu
    wywo??a?? rekurencyjnych DFS) - na podstawie wielko??ci mapy terenu (N).
    2. Wyznacza losowe pocz??tki n poszczeg??lnych element??w ('wysp') labiryntu, czyli ??r??d??a n pierwotnych wywo??a?? DFS.
    3. Wywo??uje n razy procedur?? dfs_visit, tworz??c ??ciany n 'wysp' labiryntu.
    4. Wyznacza po 2 losowe punkty w obr??bie ka??dej 'wyspy' (ka??dego drzewa przeszukiwania wg????b), pomi??dzy kt??rymi
    tworzone b??dzie 'rozwi??zanie' labiryntu (patrz procedura get_maze_solution)."""
    global maze_elements_sets
    reset_node_colours()
    reset_parents_and_children()
    start_row, start_col = int(1 / 2 * cfg.N), int(1 / 2 * cfg.N)  # 2.
    start_node_idx = get_fence_node_idx(start_row, start_col)
    parents[start_node_idx] = start_node_idx
    maze_elements_sets = [set() for _ in range(cfg.fence_elements)]

    # 1.
    if cfg.fence_elements <= 1:
        max_wall_length = int(cfg.N)
    elif cfg.fence_elements <= 3:
        max_wall_length = int(cfg.N * 3 / 4)
    else:
        max_wall_length = int(cfg.N * 2 / 3)

    for i in range(0, cfg.fence_elements):
        if i >= 1:
            # 2.
            start_row, start_col = get_random_corner_fence_location(random.randint(0, 1), random.randint(0, 1))
            start_node_idx = get_fence_node_idx(start_row, start_col)
        if bool(fence_border(start_node_idx)):
            print("[fence.py] [dfs_build] error: start_node_idx turned out to be at map border, illegal placement. "
                  "Repeat the procedure.")
            i -= 1
            continue
        # 3.
        dfs_visit(start_node_idx, max_wall_length, 0, i)

        # 4.
        possible_tries = 5
        # Try 5 times in case the drawn nodes are not from the same DFS tree, which should not be the case, but safety
        for _ in range(possible_tries):
            idx_1 = random.choice([x for x in maze_elements_sets[i]])
            idx_2 = random.choice([x for x in maze_elements_sets[i]])
            res = get_first_common_parent(idx_1, idx_2, start_node_idx)
            if not res:
                continue
            else:
                get_maze_solution(idx_1, idx_2, start_node_idx)
                break


def dfs_visit(current_node, wall_no, walls_already_built, maze_element_id):
    """Buduje jedn?? pe??n?? 'wysp??' (element) labiryntu. Generowane s?? zbiory ??amanych otwartych, kt??rych boki mog?? by??
    wzgl??dem siebie jedynie prostopad??e lub r??wnoleg??e (wyb??r losowy). Zbi??r ??amanych reprezentuje ??ciany labiryntu,
    przestrzenie wewn??trz ??amanych reprezentuj?? korytarze labiryntu.

    Dzia??anie:
    Kolorujemy odwiedzany wierzcho??ek na szaro. Sprawdzamy, czy nie przekroczyli??my limitu ??cian stawianych
    w jednej serii wywo??a?? rekurencyjnych. Losujemy kierunek, w kt??rym postawimy ??cian?? (g??ra/prawo/d????/lewo).
    Sprawdzamy warunki postawienia ??ciany w tym kierunku - standardowe warunki DFS z jedn?? modyfikacj??:
    za wierzcho??ek czarny (przetworzony) uznajemy taki, z kt??rego wychodz?? 3 ??ciany. Gwarantuje to otwarty charakter
    ??amanych. Zatem wierzcho??ki, z kt??rych wychodz?? 1 lub 2 ??ciany s?? szare, wierzcho??ki, z kt??rych wychodz?? 3 ??ciany
    s?? czarne, a wierzcho??ki poza labiryntem s?? bia??e.

    W wyniku dzia??ania tej procedury powstaje zbi??r korytarzy labiryntu, bardziej lub mniej 'rozga????zionych'.
    S?? to jednak ??amane otwarte, zatem do ka??dej z nich da si?? wej???? z zewn??trz (spoza labiryntu), ale nie istniej??
    przej??cia pomi??dzy nimi (inne ni?? wyj??cie z korytarzy w obr??bie danej ??amanej poza labirynt i wej??cie do
    s??siaduj??cej ??amanej). Przej??cia pomi??dzy ??amanymi tworzone s?? w procedurze get_maze_solution."""
    global node_colours, parents, maze_elements_sets
    node_colours[current_node] = Colour.Grey
    maze_elements_sets[maze_element_id].add(current_node)

    if walls_already_built >= wall_no:
        return

    possible_dirs_set = {1, 2, 3, 4}
    explored_neighbours = []
    while possible_dirs_set:
        dir_no = random.sample(possible_dirs_set, 1)  # returned in a form a list
        possible_dirs_set.remove(dir_no[0])
        direction = Directions(dir_no[0])

        current_row, current_col = get_fence_node_dirs(current_node)
        chosen_neighbour = get_node_neighbour(direction, current_row, current_col)

        if chosen_neighbour and not check_if_wall_exists(current_node, chosen_neighbour) and \
                node_colours[chosen_neighbour] is Colour.White:
            build_vertex(current_node, chosen_neighbour)
            parents[chosen_neighbour] = current_node
            explored_neighbours.append(chosen_neighbour)
            dfs_visit(chosen_neighbour, wall_no, walls_already_built + 1, maze_element_id)

            # Any not-starting node case
            if len(explored_neighbours) >= 2 and walls_already_built > 0:
                node_colours[current_node] = Colour.Black
                return
            # Starting node case
            elif len(explored_neighbours) >= 3 and walls_already_built == 0:
                node_colours[current_node] = Colour.Black
                return


def get_path_twist_direction(current_black_node, nodes_path, i):
    """Wyznacza kierunek zakr??tu 'czyhaj??cego' za najbli??szym czarnym wierzcho??kiem na przemierzanej ??cie??ce nodes_path.

    :param current_black_node: Rozpatrywany czarny wierzcho??ek.
    :param nodes_path: Rozpatrywana ??cie??ka, kt??r?? pod????amy.
    :param i: Wska??nik na miejsce na ??cie??ce, w kt??rym aktualnie si?? znajdujemy (nr indeksu current_black_node w nodes_path)."""
    current_black_node_x, current_black_node_y = get_fence_node_dirs(current_black_node)
    twists_neighbours = []
    # Get all the surrounding nodes in all possible directions, let's call them neighbours
    neighbours = [get_node_neighbour(dir, current_black_node_x, current_black_node_y)
                  for dir in Directions if get_node_neighbour(dir, current_black_node_x, current_black_node_y) is not None]
    # Loop through them to look for wall connections with current_black_node
    if current_black_node is None:
        return
    for neighbour in neighbours:
        # If a wall exists (they're true neighbours) and we're not going backwards on our way - that's our path
        # intersection (path twists)
        if check_if_wall_exists(current_black_node, neighbour):
            if i <= 0:
                error_exit("fence.py", "get_path_twist_direction",
                           "i == 0, cannot get the backward node (nodes_path[i - 1]")
                break
            # The neighbour is not on our backwards way, we've not come from there
            if i > 0 and neighbour != nodes_path[i - 1]:
                twists_neighbours.append(neighbour)

    twists_directions = [neighbours_relations(current_black_node, x) for x in twists_neighbours]
    if len(twists_neighbours) != len(twists_directions) or i + 1 >= len(nodes_path):
        return
    left_turn_dir, left_turn_node, right_turn_dir, right_turn_node = None, None, None, None
    for dir, node in zip(twists_directions, twists_neighbours):
        if dir == Directions.Left:
            left_turn_dir, left_turn_node = dir, node
        if dir == Directions.Right:
            right_turn_dir, right_turn_node = dir, node
    for dir, node in zip(twists_directions, twists_neighbours):
        if dir not in [Directions.Left, Directions.Right]:
            if left_turn_dir and left_turn_node and right_turn_dir is None and right_turn_node is None:
                right_turn_dir, right_turn_node = Directions.Right, node
            elif right_turn_dir and right_turn_node and left_turn_dir is None and left_turn_node is None:
                left_turn_dir, left_turn_node = Directions.Left, node

    opposite = False
    if i > 0:
        current_black_node_idx = get_fence_node_idx(current_black_node_y, current_black_node_x)
        previous_node_idx = get_fence_node_idx(
            get_fence_node_dirs(nodes_path[i - 1])[1],
            get_fence_node_dirs(nodes_path[i - 1])[0]
        )
        if current_black_node_idx < previous_node_idx:
            opposite = False
        elif current_black_node_idx > previous_node_idx:
            opposite = True

    if i + 1 < len(nodes_path) and nodes_path[i + 1] == left_turn_node:
        return left_turn_dir if opposite else right_turn_dir
    elif i + 1 < len(nodes_path) and nodes_path[i + 1] == right_turn_node:
        return right_turn_dir if opposite else left_turn_dir


def get_opposite_wall_side(current_side):
    """If 'left' return 'right', if 'right' return 'left'"""
    if current_side is Directions.Left:
        return Directions.Right
    elif current_side is Directions.Right:
        return Directions.Left


def get_maze_solution(start_node, end_node, start_node_idx):
    """Wyznacza 'rozwi??zanie' labiryntu, tj. przej??cie pomi??dzy zadanymi punktami (wierzcho??kami).

    :param start_node: Start of the labirynth path.
    :param end_node: End of the labirynth path.
    :param start_node_idx: DFS source for technical purposes.

    Za??o??enia:
    Oba punkty s?? wierzcho??kami tego samego drzewa przeszukiwania wg????b, cho?? mog?? (a nawet powinny, dla efekt??w
    wizualnych) le??e?? na r????nych jego ga????ziach (po r????nych 'stronach' wierzcho??ka-??r??d??a DFS).

    Dzia??anie:
    Korzystaj??c z gotowego ju?? drzewa przeszukiwania wg????b (parents[]), wyznacza?? b??dziemy ??cie??k?? pomi??dzy zadanymi
    wiercho??kami.

    1. Rozpatrujemy ??cie??ki od danych wierzcho??k??w do wierzcho??ka-??r??d??a DFS i znajdujemy pierwszy (id??c od li??ci)
    wierzcho??ek wsp??lny dla obu tych ??cie??ek (mo??e by?? nim wierzcho??ek-??r??d??o DFS, je??li zadane wierzcho??ki znajduj?? si??
    na innych ga????ziach g????wnych drzewa). Wierzcho??ek ten wyznacza ??cie??k?? pomi??dzy zadanymi wierzcho??kami - nale??y
    wzi???? ??cie??k?? od jednego zadanego wierzcho??ka do wierzcho??ka wsp??lnego i po????czy?? j?? ze ??cie??k?? od drugiego zadanego
    wierzcho??ka do wiercho??ka wsp??lnego, ale 'odwr??con??' (zmiana kierunku kraw??dzi na przeciwny). Odwracamy kr??tsz??
    z ww. ??cie??ek, nast??pnie ??cie??ki '????czymy'. W otrzymanej ko??cowej ??cie??ce wierzcho??kiem pocz??tkowym jest ten,
    kt??ry jest bardziej oddalony od punktu wsp??lnego, a ko??cowym ten, kt??ry znajduje si?? bli??ej punktu wsp??lnego.

    2. W wygenerowanym w procedurze dfs_visit zbiorze ??cian kluczowe s?? wiercho??ki czarne. Ka??dy wiercho??ek czarny to
    styk 3 ??cian, co oznacza, ??e wyznacza on 2 lub 3 s??siaduj??ce ze sob?? ??amane otwarte (korytarze). Interesowa??
    nas b??dzie ci??g czarnych wiercho??k??w obecnych na otrzymanej w pkt. 1. ??cie??ce. Ka??de 2 s??siednie czarne wiercho??ki
    w tym ci??gu, kt??re jednocze??nie nie s??siaduj?? ze sob?? na ??cie??ce, wyznaczaj?? korytarz, kt??rym da si?? przej????
    (wzd??u??, zawartych pomi??dzy, wierzcho??k??w szarych). 'Przej??cie' przez labirynt polega?? b??dzie na przej??ciu
    'korytarzami' ww. ??cie??ki, usuwaj??c po drodze pewne kraw??dzie. Najpierw wybieramy wierzcho??ek pocz??tkowy
    (pierwszy czarny) oraz umownie 'stron??' ??ciany labiryntu, wzd??u?? kt??rej b??dziemy si?? porusza?? (umownie lewa/prawa).
    Nast??pnie, dop??ki nie przejdziemy ca??ej ??cie??ki:
        a) wybieramy nast??pny czarny wierzcho??ek
        b) oceniamy, czy da si?? z niego przej???? wzd??u?? 'naszej' strony ??cian do nast??pnego wierzcho??ka na ??cie??ce
        - poprzez ocen?? naszego po??o??enia wzgl??dem kraw??dzi s??siad??w wierzcho??ka z pkt. a). Wychodz?? z niego dwie
        kraw??dzie inne ni?? ta, z kt??rej przyszli??my, w tym jedna jest nast??pn?? kraw??dzi?? naszej ??cie??ki. Je??li jest to
        kraw??d?? 'lewa', a znajdujemy si?? po stronie 'lewej', to mo??emy bez problemu porusza?? si?? dalej po tej samej
        stronie. Je??li jednak jest to kraw??d?? 'prawa', a znajdujemy si?? po stronie lewej, usuwamy poprzedni?? kraw??d??
        (t??, z kt??rej przyszli??my) i zmieniamy stron?? na przeciwn??, co gwarantuje nam dalsze pod????anie ??cie??k??.
        W proc. dfs_visit powsta?? zbi??r ??amanych otwartych, czyli w zasadzie 'pseudolabirynt', zawsze mo??na wi??c przej????
        do s??siedniego korytarza cofaj??c si?? do wyj??cia i wchodz??c wej??ciem do s??siedniego, zatem teoretycznie nie
        by??oby potrzeby usuwania kraw??dzi. By??oby to jednak wybitnie nielabiryntowe, dlatego stosujemy przej??cie ??cie??k??
        z pkt. 1. z usuwaniem kraw??dzi w zale??no??ci od 'zakr??t??w' drzewa przeszukiwania wg????b."""
    first_common_parent = get_first_common_parent(start_node, end_node, start_node_idx)
    # Zgodno???? z za??o??eniami
    if not first_common_parent:
        return

    # 1.
    node_with_shorter_path = first_common_parent["node_with_shorter_path"]
    node_with_longer_path = start_node if node_with_shorter_path == end_node else end_node
    first_common_node_idx = first_common_parent["first_common_idx"]

    shorter_path_length = first_common_parent["path_length"]
    cfg.start_end_points["start"], cfg.start_end_points["end"] = node_with_longer_path, node_with_shorter_path
    longer_path_length = get_parent_path_length(node_with_longer_path, first_common_node_idx)
    total_length = shorter_path_length + longer_path_length

    reverse_path(node_with_shorter_path, first_common_node_idx)

    nodes_path = get_joined_nodes_path(node_with_shorter_path, first_common_node_idx, node_with_longer_path,
                                       total_length)

    # 2A.
    start_next_black_node = get_next_black_node(node_with_longer_path, node_with_longer_path, nodes_path, 0)[1]
    next_black_node = get_next_black_node(start_next_black_node, start_next_black_node, nodes_path, 0)[1]

    if check_if_wall_exists(next_black_node, start_next_black_node):
        starting_node = next_black_node
        i = get_next_black_node(start_next_black_node, start_next_black_node, nodes_path, 0)[2]
    else:
        starting_node = start_next_black_node
        i = get_next_black_node(node_with_longer_path, node_with_longer_path, nodes_path, 0)[2]
    if node_colours[starting_node] is not Colour.Black:
        error_exit("fence.py", "get_maze_solution", "starting_node is not Colour.Black")
    ending_node = get_closest_black_node(end_node)
    cfg.start_end_points["starting_node"], cfg.start_end_points["ending_node"] = starting_node, ending_node

    wall_side = Directions.Left if random.randint(0, 1) % 2 == 0 else Directions.Right

    # 2B.
    while i < len(nodes_path) - 1:
        previous_node, starting_node, i = get_next_black_node(nodes_path[i + 1], starting_node, nodes_path, i + 1)

        if i >= len(nodes_path) - 1:
            break

        if (previous_node and starting_node) and (previous_node != starting_node) \
                and (wall_side != get_path_twist_direction(starting_node, nodes_path, i)):
            wall_side = get_opposite_wall_side(wall_side)
            delete_wall(previous_node, starting_node)
            cfg.deleted_walls.add((previous_node, starting_node))
            cfg.deleted_walls.add((starting_node, previous_node))

    # Visualisation purposes
    for node in nodes_path:
        cfg.specials[node] = True


def get_joined_nodes_path(node_with_shorter_path, first_common_node_idx, node_with_longer_path, length):
    """Returns a path between any two given points within the same DFS tree (the same maze 'element'). Merges two paths:
    - the longer one (non-reversed), starting in node_with_longer_path and passing through its' following
    DFS-parent nodes (parents[]),
    - the shorter one (reversed), starting in node_with_shorter_path, which is a reverse of the DFS-parent-nodes
    path (children[]).
    Returns a concatenation of these two paths, hence a path between: node_with_longer_path and node_with_shorter_path.

    :param node_with_shorter_path: Beginning node of the path to reverse.
    :param first_common_node_idx: The first node that is mutual for both paths. It can be any node, including the DFS
    source node.
    :param node_with_longer_path: Beginning node of the the non-reversed path.
    :param length: The length of the path to be created.
    :return: An array in which the i-th element represents the i-th node on the path.
    """
    joined_path = [_ for _ in range(0, length - 1)]
    i = 0

    while node_with_longer_path != first_common_node_idx:
        joined_path[i] = node_with_longer_path
        node_with_longer_path = parents[node_with_longer_path]
        i += 1

    while first_common_node_idx != node_with_shorter_path:
        joined_path[i] = first_common_node_idx
        first_common_node_idx = children[first_common_node_idx]
        i += 1

    joined_path[i] = node_with_shorter_path

    return joined_path


def get_next_black_node(current_node, previous_node, nodes_path, i):
    """Returns a pair of the next black (DFS tree colouring) and its' predecessor on a given node path.

    :param current_node: The current node. We're searching for its' next black neighbour on the given path.
    :param previous_node: Predecessor of the current node. Needed for the purposes of the get_maze_solution function.
    :param nodes_path: The graph path to follow.
    :param i: Position on the graph path to follow.
    :return: Pair of (predecessor, next black node).
    """
    global node_colours
    if current_node < 0 or current_node > (cfg.N + 1) ** 2 \
            or node_colours[current_node] is Colour.White or i >= len(nodes_path) - 1:
        return previous_node, previous_node, i
    if node_colours[current_node] is Colour.Black:
        return previous_node, current_node, i
    else:
        return get_next_black_node(nodes_path[i + 1], current_node, nodes_path, i + 1)


# Auxiliary function
def get_closest_black_node(node_idx):
    while node_colours[node_idx] is not Colour.White and node_idx != parents[node_idx] \
            and parents[node_idx] is not None:
        if node_colours[node_idx] is Colour.Black:
            return node_idx
        node_idx = parents[node_idx]
    return node_idx


# Auxiliary function
def get_parent_path_length(child_node, parent_node):
    length = 1
    while child_node != parent_node:
        length += 1
        child_node = parents[child_node]
    return length


def get_first_common_parent(node_idx_1, node_idx_2, start_node_idx):
    """Takes two nodes and processes their DFS tree paths (parents[]). Searches for the first node that is mutual
    for those two paths (any node, including the DFS source, if the two nodes are on different DFS tree branches).

    :param node_idx_1: First node.
    :param node_idx_2: Second node.
    :param start_node_idx: DFS source node. Along with the 'parents' array, it constitutes the DFS tree.
    :return: A dictionary of {node with a shorter 'DFS parent' path to the DFS source; first mutual node; length of the shorter 'DFS parent' path}
    """
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


# For test purposes only
def print_parent_path(node_idx):
    print(node_idx)
    if node_idx == parents[node_idx]:
        return
    print_parent_path(parents[node_idx])


# For test purposes only
def print_reversed_path(node_from, node_to):
    print("Reversed path", node_from)
    if children[node_from] is None or node_from == node_to:
        return
    print_reversed_path(children[node_from], node_to)


def reverse_path(node_beginning, node_end):
    """Takes two nodes on one DFS tree branch, processes the DFS tree path between them and reverses this path."""
    global parents, children
    if node_beginning == node_end:
        return
    children[parents[node_beginning]] = node_beginning
    reverse_path(parents[node_beginning], node_end)
