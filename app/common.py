"""Classes, functions and import mutual for several .py project files."""

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

terrain_lock = Lock()  # Safe memory sharing, secures terrain (map) usage by animals (animal movement/procreation)
stats_lock = Lock()  # Safe memory sharing, secures statistics array usage by animals (animals born/deceased)

can_run = Event()  # Responsible for pausing simulation
terminate_threads = Event()  # Responsible for terminating simulation in order to re-run it


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
    Up_Right = 5
    Down_Right = 6
    Down_Left = 7
    Up_Left = 8


class Colour(Enum):
    White = 1
    Grey = 2
    Black = 3


def check_terrain_boundaries(x, y):
    """Checks whether we are within terrain (map) boundaries."""
    return 0 <= x < cfg.N and 0 <= y < cfg.N


def set_terrain_value(x, y, value):
    """Safe multi-threading memory sharing."""
    global terrain_lock
    with terrain_lock:
        cfg.terrain[x][y] = value


def set_stats(animal_species, value):
    """Safe multi-threading memory sharing."""
    global stats_lock
    with stats_lock:
        cfg.stats[animal_species] += value


# Auxiliary function
def error_exit(file_name, def_name, message):
    print("[", file_name, "] ", "[", def_name, "] ", "ERROR: ", message)
    return
