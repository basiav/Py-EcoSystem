import threading
from threading import Thread, active_count, Lock, Event
import time
import random
import os
import pygame
import pygame.freetype as pf
import matplotlib.pyplot as plt
import matplotlib

from enum import Enum
import config as cfg

import matplotlib.backends.backend_agg as agg
from matplotlib.figure import Figure

matplotlib.use("Agg")

terrain_lock = Lock()
stats_lock = Lock()

can_run = Event()
terminate_threads = Event()


class Animals(Enum):
    Rabbit = 1
    Wolf_Female = 2
    Wolf_Male = 3
    Wolf_In_General = 4


class Directions(Enum):
    Up = 1
    Right = 2
    Down = 3
    Left = 4


def check_terrain_boundaries(x, y):
    return 0 <= x < cfg.N and 0 <= y < cfg.N


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


def node_neighbours(neighbour_direction, row, column):
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


def set_terrain_value(x, y, value):
    global terrain_lock
    with terrain_lock:
        cfg.terrain[x][y] = value


def set_stats(animal_species, value):
    global stats_lock
    with stats_lock:
        cfg.stats[animal_species] += value
