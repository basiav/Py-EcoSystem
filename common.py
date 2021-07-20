from threading import Thread, active_count
import time
import random
import os
import pygame
import pygame.freetype as pf
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
from matplotlib.figure import Figure

from enum import Enum
import config as cfg


class Animals(Enum):
    Rabbit = 1
    Wolf_Female = 2
    Wolf_Male = 3
    Wolf_In_General = 4


def check_boundaries(x, y):
    return 0 <= x < cfg.N and 0 <= y < cfg.N
