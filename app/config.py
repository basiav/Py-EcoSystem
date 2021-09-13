N = 30
terrain = [[None for _ in range(N)] for _ in range(N)]

rabbit_no = 30
wolf_no = 20

rabbit_reproduction_chances = 25
wolf_reproduction_chances = 10

stats = {'rabbits': 0, 'wolves_females': 0, 'wolves_males': 0}
stats_arrs = {'rabbits': [], 'wolves_females': [], 'wolves_males': []}

fence = [list() for _ in range((N + 1) ** 2)]
fence_flag = True
fence_elements = 1

specials = [None for _ in range((N + 1) ** 2)]
deleted_walls = set()
start_end_points = {
    "start": None,
    "end": None,
    "starting_node": None,
    "ending_node": None
}
maze_solution = set()


def get_aliased_global_variable_names():
    global N, terrain, rabbit_no, wolf_no, rabbit_reproduction_chances, wolf_reproduction_chances, stats, stats_arrs
    return N, terrain, rabbit_no, wolf_no, rabbit_reproduction_chances, wolf_reproduction_chances, stats, stats_arrs


def set_default_parameters():
    global N, terrain, rabbit_no, wolf_no, rabbit_reproduction_chances, wolf_reproduction_chances, stats, stats_arrs
    global fence, fence_flag, fence_elements
    global specials, deleted_walls, start_end_points, maze_solution
    N = 30
    terrain = [[None for _ in range(N)] for _ in range(N)]

    rabbit_no = 30
    wolf_no = 20

    rabbit_reproduction_chances = 25
    wolf_reproduction_chances = 10

    stats = {'rabbits': 0, 'wolves_females': 0, 'wolves_males': 0}
    stats_arrs = {'rabbits': [], 'wolves_females': [], 'wolves_males': []}

    fence = [list() for _ in range((N + 1) ** 2)]
    fence_flag = True
    fence_elements = 1

    specials = [None for _ in range((N + 1) ** 2)]
    deleted_walls = set()
    start_end_points = {
        "start": None,
        "end": None,
        "starting_node": None,
        "ending_node": None
    }
    maze_solution = set()


def redeclare_fence():
    global fence, fence_elements
    fence = [list() for _ in range((N + 1) ** 2)]
    fence_elements = 1
