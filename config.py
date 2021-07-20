N = 30
wyspa = [[None for _ in range(N)] for _ in range(N)]

rabbit_no = 20
wolf_no = 30

reproduction_chances = 30

stats = {'rabbits': 0, 'wolves_females': 0, 'wolves_males': 0}
stats_arrs = {'rabbits': [], 'wolves_females': [], 'wolves_males': []}


def get_aliased_global_variable_names():
    global N, wyspa, rabbit_no, wolf_no, reproduction_chances, stats, stats_arrs
    return N, wyspa, rabbit_no, wolf_no, reproduction_chances, stats, stats_arrs


def get_default_settings():
    global N, wyspa, rabbit_no, wolf_no, reproduction_chances, stats, stats_arrs
    N = 30
    wyspa = [[None for _ in range(N)] for _ in range(N)]

    rabbit_no = 20
    wolf_no = 30

    reproduction_chances = 30

    stats = {'rabbits': 0, 'wolves_females': 0, 'wolves_males': 0}
    stats_arrs = {'rabbits': [], 'wolves_females': [], 'wolves_males': []}
