from common import Thread, Animals, time, random, check_boundaries, set_terrain_value, set_stats
import config

sleep_time = 0.2

x_dirs = [0, 1, 1, 1, 0, -1, -1, -1]
y_dirs = [1, 1, 0, -1, -1, -1, 0, 1]


def check_overpopulation(x, y):
    for i in range(0, len(x_dirs) - 1):
        new_x, new_y = x + x_dirs[i], y + y_dirs[i]
        if check_boundaries(new_x, new_y) and config.terrain[new_x][new_y] is None:
            return x + x_dirs[i], y + y_dirs[i]
    return False


def find_neighbour_rabbit(x, y):
    for i in range(0, len(x_dirs) - 1):
        new_x, new_y = x + x_dirs[i], y + y_dirs[i]
        if check_boundaries(new_x, new_y) and config.terrain[new_x][new_y] is Animals.Rabbit:
            return x + x_dirs[i], y + y_dirs[i]
    return False


class Animal(Thread):
    def __init__(self, x, y, identity):
        self.x = x
        self.y = y
        self.identity = identity
        # config.terrain[x][y] = self.identity
        set_terrain_value(x, y, self.identity)
        Thread.__init__(self)

    def make_move(self, destination_x, destination_y):
        # config.terrain[self.x][self.y] = None
        set_terrain_value(self.x, self.y, None)
        self.x = destination_x
        self.y = destination_y
        # config.terrain[self.x][self.y] = self.identity
        set_terrain_value(self.x, self.y, self.identity)


class Rabbit(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, Animals.Rabbit)
        # config.stats['rabbits'] += 1
        set_stats('rabbits', 1)

    def check_if_alive(self):
        return config.terrain[self.x][self.y] == Animals.Rabbit

    def run(self):
        while True:
            if not self.check_if_alive():
                # config.terrain[self.x][self.y] = None
                set_terrain_value(self.x, self.y, None)
                # config.stats['rabbits'] -= 1
                set_stats('rabbits', -1)
                break

            time.sleep(sleep_time)

            nx = self.x + random.randint(-1, 1)
            ny = self.y + random.randint(-1, 1)

            if (not check_boundaries(nx, ny)) or (nx == self.x and ny == self.y):
                continue

            if config.terrain[nx][ny] == Animals.Rabbit and random.randint(1, 100) < config.reproduction_chances:

                # Rabbits won't reproduce unless there's at lest one free field around
                check = check_overpopulation(nx, ny)
                if check:
                    new_rabbit = Rabbit(check[0], check[1])
                    new_rabbit.start()

            # elif config.terrain[nx][ny] is None:
            #    self.make_move(nx, ny)
            else:
                self.make_move(nx, ny)


class Wolf(Animal):
    def __init__(self, x, y):
        identity = Animals.Wolf_Female if random.randint(0, 1) == 0 else Animals.Wolf_Male
        super().__init__(x, y, identity)
        self.energy = 10
        if self.identity == Animals.Wolf_Female:
            # config.stats['wolves_females'] += 1
            set_stats('wolves_females', 1)
        elif self.identity == Animals.Wolf_Male:
            # config.stats['wolves_males'] += 1
            set_stats('wolves_males', 1)

    def check_if_alive(self):
        return self.energy > 0

    def increase_energy(self):
        self.energy = self.energy + 1 if self.energy < 10 else 10

    def decrease_energy(self):
        self.energy = self.energy - 0.1 if self.energy > 0 else 0

    def run(self):
        while True:
            if not self.check_if_alive():
                # config.terrain[self.x][self.y] = None
                set_terrain_value(self.x, self.y, None)
                if self.identity == Animals.Wolf_Female:
                    # config.stats['wolves_females'] -= 1
                    set_stats('wolves_females', -1)
                elif self.identity == Animals.Wolf_Male:
                    # config.stats['wolves_males'] -= 1
                    set_stats('wolves_males', -1)
                break

            time.sleep(sleep_time)

            neighbour_rabbit = find_neighbour_rabbit(self.x, self.y)

            if not neighbour_rabbit:
                nx = self.x + random.randint(-1, 1)
                ny = self.y + random.randint(-1, 1)
                if not check_boundaries(nx, ny):
                    continue

                if config.terrain[nx][ny] == self.identity:
                    # break  # królik ginie
                    # w = Wolf(nx, ny)
                    # w.start()
                    # pass
                    pass

                self.make_move(nx, ny)
                self.decrease_energy()

            else:
                self.make_move(neighbour_rabbit[0], neighbour_rabbit[1])
                self.increase_energy()
