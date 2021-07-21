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


def check_boundaries(x, y):
    return 0 <= x < cfg.N and 0 <= y < cfg.N


def set_terrain_value(x, y, value):
    global terrain_lock
    with terrain_lock:
        cfg.terrain[x][y] = value


def set_stats(animal_species, value):
    global stats_lock
    with stats_lock:
        cfg.stats[animal_species] += value
