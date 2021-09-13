#!/usr/bin/python3
import sys
sys.path.append('../')

import threading
from common import plt
from animals import *
from fence import *
from gui.plot import PlotPhotos, StartMenu
import config

import matplotlib
import matplotlib.backends.backend_agg as agg
from matplotlib.figure import Figure

matplotlib.use("Agg")


def terminate_animal_threads():
    # Set terminate_threads Event() flag
    common.terminate_threads.set()

    if not common.terminate_threads.is_set():
        raise Exception("[MAIN, start_simulation] ERROR: threading.Event terminate_threads should have been set by now")

    # Join all the Animal threads
    for thread in threading.enumerate():
        if thread != threading.main_thread():
            thread.join()

    if threading.active_count() != 1:
        raise Exception("[MAIN, start_simulation] ERROR: "
                        "All threads except for the main one should have been joint by now")


def create_start_menu():
    return StartMenu(800, 650)


def create_sample_fence():
    dfs_build()


def start_simulation():
    plot = PlotPhotos(agg)

    fig = Figure(figsize=(2, 2), dpi=800)
    canvas = agg.FigureCanvasAgg(fig)

    N, wyspa, rabbit_no, wolf_no, rabit_reproduction_chances, wolf_reproduction_chances, stats, stats_arrs \
        = config.get_aliased_global_variable_names()

    def update_stats_arr():
        stats_arrs['rabbits'].append(stats['rabbits'])
        stats_arrs['wolves_females'].append(stats['wolves_females'])
        stats_arrs['wolves_males'].append(stats['wolves_males'])

    def create_bar_img():
        update_stats_arr()
        nonlocal canvas, fig
        fig.clf()
        ax = fig.add_subplot()
        ax.plot(range(len(stats_arrs['rabbits'])), stats_arrs['rabbits'], color="yellow")
        ax.plot(range(len(stats_arrs['wolves_females'])), stats_arrs['wolves_females'], color="pink")
        ax.plot(range(len(stats_arrs['wolves_males'])), stats_arrs['wolves_males'], color="blue")
        ax.set_title("Animal population in Time", fontsize=8)
        ax.set_xlabel('distance (m)')
        ax.set_ylabel('Damped oscillation')
        canvas.draw()
        renderer = canvas.get_renderer()
        return renderer.tostring_rgb()

    def create_animal_on_random_pos(animal):
        return Rabbit(random.randint(0, N - 1), random.randint(0, N - 1)) if animal == Animals.Rabbit \
            else Wolf(random.randint(0, N - 1), random.randint(0, N - 1))

    plt.xlim(0, 1)
    plt.ylim(0, 20)

    common.can_run.set()
    common.terminate_threads.clear()

    once = False
    while plot.running or not plot.pause:
        minimum = min(wolf_no, rabbit_no)
        image = create_bar_img()

        while not once:
            for _ in range(minimum):
                # Rabbits
                create_animal_on_random_pos(Animals.Rabbit).start()
                plot.update(image, canvas)

                # Wolves
                create_animal_on_random_pos(Animals.Wolf_In_General).start()
                plot.update(image, canvas)

                time.sleep(0.1)

            if minimum == wolf_no:
                for _ in range(abs(wolf_no - rabbit_no)):
                    # Rabbits
                    create_animal_on_random_pos(Animals.Rabbit).start()
                    plot.update(image, canvas)

            elif minimum == rabbit_no:
                # Wolves
                for _ in range(abs(wolf_no - rabbit_no)):
                    create_animal_on_random_pos(Animals.Wolf_In_General).start()
                    plot.update(image, canvas)

            once = True

        if plot.quit:
            plot.quit_plot()
            break

        plot.update(image, canvas)

        if plot.pause and common.can_run.is_set():
            common.can_run.clear()
        if not plot.pause and not common.can_run.is_set():
            common.can_run.set()
        if plot.pause and not plot.running:
            common.can_run.set()

    terminate_animal_threads()
    return plot


def main():
    common.terminate_threads.set()

    start_menu = create_start_menu()
    escape = start_menu.quit

    reset_fence()

    while not escape:
        start_menu.update()
        if start_menu.start_game:
            if not start_menu.memorise_fence:
                create_sample_fence()
            print("[MAIN] Starting simulation!")
            res = start_simulation()
            print("[MAIN] Simulation over")
            res.quit_plot()

        if not start_menu.quit:
            start_menu = create_start_menu()
            config.set_default_parameters()
            reset_fence()

        escape = start_menu.quit

    print("[MAIN] Goodbye! :)")


if __name__ == '__main__':
    main()
