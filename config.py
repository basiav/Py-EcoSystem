N = 30
terrain = [[None for _ in range(N)] for _ in range(N)]

rabbit_no = 30
wolf_no = 18

rabbit_reproduction_chances = 30
wolf_reproduction_chances = 30

stats = {'rabbits': 0, 'wolves_females': 0, 'wolves_males': 0}
stats_arrs = {'rabbits': [], 'wolves_females': [], 'wolves_males': []}


def get_aliased_global_variable_names():
    global N, terrain, rabbit_no, wolf_no, rabbit_reproduction_chances, wolf_reproduction_chances, stats, stats_arrs
    return N, terrain, rabbit_no, wolf_no, rabbit_reproduction_chances, wolf_reproduction_chances, stats, stats_arrs


def get_default_settings():
    global N, terrain, rabbit_no, wolf_no, rabbit_reproduction_chances, wolf_reproduction_chances, stats, stats_arrs
    N = 30
    terrain = [[None for _ in range(N)] for _ in range(N)]

    rabbit_no = 20
    wolf_no = 30

    rabbit_reproduction_chances = 30
    wolf_reproduction_chances = 30

    stats = {'rabbits': 0, 'wolves_females': 0, 'wolves_males': 0}
    stats_arrs = {'rabbits': [], 'wolves_females': [], 'wolves_males': []}
