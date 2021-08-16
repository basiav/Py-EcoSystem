N = 30
terrain = [[None for _ in range(N)] for _ in range(N)]

rabbit_no = 30
wolf_no = 20

rabbit_reproduction_chances = 30
wolf_reproduction_chances = 10

stats = {'rabbits': 0, 'wolves_females': 0, 'wolves_males': 0}
stats_arrs = {'rabbits': [], 'wolves_females': [], 'wolves_males': []}

fence = [list() for _ in range((N + 1) ** 2)]


def get_aliased_global_variable_names():
    global N, terrain, rabbit_no, wolf_no, rabbit_reproduction_chances, wolf_reproduction_chances, stats, stats_arrs
    return N, terrain, rabbit_no, wolf_no, rabbit_reproduction_chances, wolf_reproduction_chances, stats, stats_arrs


def set_default_parameters():
    global N, terrain, rabbit_no, wolf_no, rabbit_reproduction_chances, wolf_reproduction_chances, stats, stats_arrs
    global fence
    N = 30
    terrain = [[None for _ in range(N)] for _ in range(N)]

    rabbit_no = 30
    wolf_no = 20

    rabbit_reproduction_chances = 30
    wolf_reproduction_chances = 10

    stats = {'rabbits': 0, 'wolves_females': 0, 'wolves_males': 0}
    stats_arrs = {'rabbits': [], 'wolves_females': [], 'wolves_males': []}

    fence = [list() for _ in range((N + 1) ** 2)]
