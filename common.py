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


def get_fence_node_idx(x, y):
    return x * (cfg.N + 1) + y


def get_fence_node_dirs(node_idx):
    col = node_idx % (cfg.N + 1)
    row = (node_idx - col) // (cfg.N + 1)
    return row, col


def check_terrain_boundaries(x, y):
    return 0 <= x < cfg.N and 0 <= y < cfg.N


def fence_border(node_idx):
    row, col = get_fence_node_dirs(node_idx)
    if row == 0:
        return Directions.Up
    elif row == cfg.N + 1:
        return Directions.Down
    elif col == 0:
        return Directions.Left
    elif col == cfg.N + 1:
        return Directions.Right


def node_neighbours(neighbour_direction, row, column):
    upper_node = get_fence_node_idx(row - 1, column + 1)
    if neighbour_direction == Directions.Up and fence_border(upper_node) != Directions.Up:
        return upper_node

    right_node = get_fence_node_idx(row, column + 1)
    if neighbour_direction == Directions.Right and fence_border(right_node) != Directions.Right:
        return right_node

    lower_node = get_fence_node_idx(row + 1, column)
    if neighbour_direction == Directions.Down and fence_border(lower_node) != Directions.Down:
        return lower_node

    left_node = get_fence_node_idx(row, column - 1)
    if neighbour_direction == Directions.Left and fence_border(left_node) != Directions.Left:
        return lower_node


def set_terrain_value(x, y, value):
    global terrain_lock
    with terrain_lock:
        cfg.terrain[x][y] = value


def set_stats(animal_species, value):
    global stats_lock
    with stats_lock:
        cfg.stats[animal_species] += value
