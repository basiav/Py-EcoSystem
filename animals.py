from common import Thread, Animals, time, random, check_boundaries, set_terrain_value, set_stats
import config
import common

sleep_time = 0.2

x_dirs = [0, 1, 1, 1, 0, -1, -1, -1]
y_dirs = [1, 1, 0, -1, -1, -1, 0, 1]


def check_overpopulation(x, y):
    for i in range(0, len(x_dirs) - 1):
        new_x, new_y = x + x_dirs[i], y + y_dirs[i]
        if check_boundaries(new_x, new_y) and config.terrain[new_x][new_y] is None:
            return x + x_dirs[i], y + y_dirs[i]
    return False


def find_neighbour(x, y, animal):
    for i in range(0, len(x_dirs) - 1):
        new_x, new_y = x + x_dirs[i], y + y_dirs[i]
        if check_boundaries(new_x, new_y) and config.terrain[new_x][new_y] == animal:
            return x + x_dirs[i], y + y_dirs[i]
    return False


class Animal(Thread):
    def __init__(self, x, y, identity):
        common.can_run.wait()
        self.x = x
        self.y = y
        self.identity = identity
        set_terrain_value(x, y, self.identity)
        Thread.__init__(self)

    def make_move(self, destination_x, destination_y):
        set_terrain_value(self.x, self.y, None)
        self.x = destination_x
        self.y = destination_y
        set_terrain_value(self.x, self.y, self.identity)

    #def check_if_alive(self):
    #    return not common.terminate_threads.is_set()


class Rabbit(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, Animals.Rabbit)
        set_stats('rabbits', 1)

    def check_if_alive(self):
        return config.terrain[self.x][self.y] == Animals.Rabbit

    def run(self):
        while True and not common.terminate_threads.is_set():
            common.can_run.wait()
            if not self.check_if_alive():
                set_terrain_value(self.x, self.y, None)
                set_stats('rabbits', -1)
                break

            #if not super(Rabbit, self).check_if_alive():
            if common.terminate_threads.is_set():
                break

            time.sleep(sleep_time)

            nx = self.x + random.randint(-1, 1)
            ny = self.y + random.randint(-1, 1)

            if (not check_boundaries(nx, ny)) or (nx == self.x and ny == self.y):
                continue

            if config.terrain[nx][ny] == Animals.Rabbit and random.randint(1, 100) < config.rabbit_reproduction_chances:

                # Rabbits won't reproduce unless there's at lest one free field around
                check = check_overpopulation(nx, ny)
                if check:
                    new_rabbit = Rabbit(check[0], check[1])
                    new_rabbit.start()

            elif config.terrain[nx][ny] is None:
                self.make_move(nx, ny)


class Wolf(Animal):
    def __init__(self, x, y):
        identity = Animals.Wolf_Female if random.randint(0, 1) == 0 else Animals.Wolf_Male
        super().__init__(x, y, identity)
        self.energy = 10
        if self.identity == Animals.Wolf_Female:
            set_stats('wolves_females', 1)
        elif self.identity == Animals.Wolf_Male:
            set_stats('wolves_males', 1)

    def check_if_alive(self):
        return self.energy > 0

    def increase_energy(self):
        self.energy = self.energy + 1 if self.energy < 10 else 10

    def decrease_energy(self):
        self.energy = self.energy - 0.1 if self.energy > 0 else 0

    def opposite(self):
        if self.identity == Animals.Wolf_Female:
            return Animals.Wolf_Male
        elif self.identity == Animals.Wolf_Male:
            return Animals.Wolf_Female
        else:
            return None

    def run(self):
        while True and not common.terminate_threads.is_set():
            common.can_run.wait()
            if not self.check_if_alive():
                set_terrain_value(self.x, self.y, None)
                if self.identity == Animals.Wolf_Female:
                    set_stats('wolves_females', -1)
                elif self.identity == Animals.Wolf_Male:
                    set_stats('wolves_males', -1)
                break

            #if not super(Wolf, self).check_if_alive():
            #    break
            if common.terminate_threads.is_set():
                break

            time.sleep(sleep_time)

            neighbour_rabbit = find_neighbour(self.x, self.y, Animals.Rabbit)
            neighbour_wolf_female = find_neighbour(self.x, self.y, Animals.Wolf_Female)

            if not neighbour_rabbit:
                if self.identity == Animals.Wolf_Male and neighbour_wolf_female is not False:
                    nx, ny = neighbour_wolf_female[0], neighbour_wolf_female[1]

                else:
                    nx = self.x + random.randint(-1, 1)
                    ny = self.y + random.randint(-1, 1)
                    if not check_boundaries(nx, ny):
                        continue

                if config.terrain[nx][ny] == self.opposite() and self.opposite() is not None:

                    # Wolves won't reproduce unless there's at lest one free field around
                    check = check_overpopulation(nx, ny)
                    if check and random.randint(1, 100) < config.wolf_reproduction_chances:
                        new_wolf = Wolf(check[0], check[1])
                        new_wolf.start()

                elif config.terrain[nx][ny] is None:
                    self.make_move(nx, ny)
                    self.decrease_energy()

            else:
                self.make_move(neighbour_rabbit[0], neighbour_rabbit[1])
                self.increase_energy()
