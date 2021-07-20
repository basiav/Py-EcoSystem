import threading

from matplotlib import pyplot as plt
from matplotlib.figure import Figure

import config as cfg
from common import pygame, Enum, matplotlib
from animals import *


def active_threads_string():
    return 'Currently active threads: ' + str(threading.active_count())


def total_animals_no():
    return 'Total animals number: ' + str(sum(cfg.stats.values()))


def create_legend():
    labels = ["Rabbits", "Wolves females", "Wolves males"]
    colors = ["yellow", "pink", "blue"]
    f = lambda m, c: plt.plot([], [], marker=m, color=c, ls="none")[0]
    handles = [f("s", colors[i]) for i in range(3)]
    legend = plt.legend(handles=handles, labels=labels, loc=3, framealpha=1, frameon=True)
    fig = legend.figure
    fig.canvas.draw()
    bbox = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig("resources/legend.png", dpi="figure", bbox_inches=bbox)
    return pygame.image.load('resources/legend.png')


def print_settings():
    print("Settings:", "[ N: ", cfg.N, "]", "[ Rabbits: ", cfg.rabbit_no, "]", "[ Wolves: ", cfg.wolf_no, "]",
          "[ Reproduction chances: ", cfg.reproduction_chances / 100, "]")


class GUIElements:
    class Slider:
        def __init__(self, start_x, start_y, width, height, active_colour):
            self.start_x = start_x
            self.start_y = start_y
            self.width = width
            self.height = height
            self.active_colour = active_colour
            self.highlight_colour = (255, 255, 255)
            self.scroll_x_center = self.start_x

        def set_default_range(self, minimum, maximum):
            self.min = minimum
            self.max = maximum

        def get_scaled_value(self, decimal=False):
            if decimal:
                res = int((self.min + (self.max - self.min) * (
                        self.scroll_x_center - self.start_x) / (
                           self.width) * 10))
                if res == 10:
                    return res / 10 * 100
                return (res % 10) / 10 * 100

            return self.min + (self.max - self.min) * (
                        self.scroll_x_center - self.start_x) // (
                             self.width)

        def perform(self, window):
            scroll_rect_width, scroll_rect_height = self.width // 22, self.height * 5

            mouse_x, mouse_y = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            scroll_line = pygame.Surface((self.width, self.height))
            scroll_rect = pygame.Surface((scroll_rect_width, scroll_rect_height))

            if self.start_x + self.width >= mouse_x >= self.start_x and self.start_y + scroll_rect_height > mouse_y > self.start_y - scroll_rect_height:
                pygame.draw.rect(scroll_line, self.highlight_colour, scroll_line.get_rect())
                pygame.draw.rect(scroll_rect, self.highlight_colour, scroll_rect.get_rect())
                if click[0]:
                    self.scroll_x_center = mouse_x
            else:
                pygame.draw.rect(scroll_line, self.active_colour, scroll_line.get_rect())
                pygame.draw.rect(scroll_rect, self.active_colour, scroll_rect.get_rect())

            # Draw scroll line
            window.blit(scroll_line, (self.start_x, self.start_y))
            # Draw scroll rectangle
            window.blit(scroll_rect, (self.scroll_x_center, self.start_y - scroll_rect_height // 2 + self.height // 2))

    class TextLine:
        def __init__(self, font, plot_object, font_colour, start_x, start_y, text_bg_surface, text_content,
                     text_shadow_colour=(0, 0, 30), bg_colour=(0, 0, 0), bg=True, shadow=True):
            self.font = font
            self.plot = plot_object
            self.font_colour = font_colour
            self.start_x = start_x
            self.start_y = start_y
            self.text_content = text_content
            self.text_bg_surface = text_bg_surface
            self.bg_colour = bg_colour
            self.text_shadow_colour = text_shadow_colour
            self.bg = bg
            self.shadow = shadow

        def render(self):
            if self.bg:
                pygame.draw.rect(self.text_bg_surface, self.bg_colour, self.text_bg_surface.get_rect())
                self.plot.window.blit(self.text_bg_surface,
                                      (self.start_x, self.start_y))
            if self.shadow:
                text_line = self.font.render(self.text_content, True, self.font_colour, self.text_shadow_colour)
            else:
                text_line = self.font.render(self.text_content, True, self.font_colour)
            self.plot.window.blit(text_line, (self.start_x, self.start_y))

    class Button:
        def __init__(self, start_pos, dimensions, active_colour, highlight_colour):
            self.start_x = start_pos[0]
            self.start_y = start_pos[1]
            self.width = dimensions[0]
            self.height = dimensions[1]
            self.active_colour = active_colour
            self.highlight_colour = highlight_colour
            self.clicked = False
            self.Rect = None

        def render(self, window, **kwargs):
            self.Rect = pygame.Rect(self.start_x, self.start_y, self.width, self.height)
            pygame.draw.rect(window, self.active_colour, self.Rect)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            text = kwargs.get('text')
            plot = kwargs.get('plot')
            font = kwargs.get('font', pygame.font.SysFont('arial', 20))
            font_colour = kwargs.get('font_colour', (0, 0, 0))

            render_text = 'text' in kwargs

            if render_text:
                text_width, text_height = font.size(text)
                centered_start_positions = [self.start_x + self.width / 2 - text_width / 2, self.start_y + self.height / 2 - text_height / 2]
                text_line = GUIElements.TextLine(font, plot, font_colour, centered_start_positions[0],
                                                 centered_start_positions[1], None, text,
                                                 text_shadow_colour=(255, 255, 255), bg_colour=(0, 0, 0), bg=False, shadow=False)
                text_line.render()

            if self.highlight_colour:
                if self.start_x + self.width >= mouse_x >= self.start_x and self.start_y + self.height >= mouse_y >= self.start_y:
                    pygame.draw.rect(window, self.highlight_colour, self.Rect)

                    if render_text:
                        text_line.render()

                    if click[0]:
                        self.clicked = True
            else:
                pygame.draw.rect(window, self.active_colour, self.Rect)
                if click[0]:
                    self.clicked = True

        def collidepoint(self, mouse_x, mouse_y):
            return self.Rect.collidepoint(mouse_x, mouse_y)


class Plot:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.tiles = cfg.N
        self.width_scale = self.width // self.tiles
        self.height_scale = self.height // self.tiles

    def render_plot(self, plot_img, canvas, plot):
        plot_surface = pygame.image.fromstring(plot_img, canvas.get_width_height(), "RGB")
        scaled_plot_surface = pygame.transform.scale(plot_surface, (350, 350))
        plot.window.blit(scaled_plot_surface, (plot.width, 0))

    def render_text(self, my_font, plot):
        text_bg_surf = pygame.Surface((plot.width_scale * 7, plot.height_scale + 30))
        active_threads_text_line = GUIElements.TextLine(my_font, plot, (255, 255, 255),
                                                        plot.width + abs((plot.window.get_width() - plot.width) // 5),
                                                        plot.height * 4 // 5, text_bg_surf, active_threads_string())
        total_animals_text_line = GUIElements.TextLine(my_font, plot, (255, 255, 255),
                                                       plot.width + abs((plot.window.get_width() - plot.width) // 5),
                                                       plot.height * 4 // 5 + 30, text_bg_surf, total_animals_no(),
                                                       bg=False)
        active_threads_text_line.render()
        total_animals_text_line.render()

    def render_legend(self, plot):
        plot.window.blit(plot.legend, (plot.width + abs((plot.window.get_width() - plot.width) // 4), 400))


class PlotPhotos(Plot):
    def __init__(self, width, height, agg):
        window = pygame.display.set_mode(flags=pygame.RESIZABLE)
        super().__init__(window, window.get_width() * 3 // 4, window.get_height())
        self.running = True

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Visualisation")
        # self.window = pygame.display.set_mode((self.width, self.height))

        bg_img = pygame.image.load('resources/grass_2.jpg')
        rabbit_img = pygame.image.load('resources/rabbit2.jpg')
        wolf_male_img = pygame.image.load('resources/wolf_male.jpg')
        wolf_female_img = pygame.image.load('resources/wolf_female.jpg')

        self.bg = pygame.transform.scale(bg_img, (self.width, self.height))
        self.rabbit = pygame.transform.scale(rabbit_img, (int(self.width_scale), int(self.height_scale)))
        self.wolf_male = pygame.transform.scale(wolf_male_img, (int(self.width_scale), int(self.height_scale)))
        self.wolf_female = pygame.transform.scale(wolf_female_img, (int(self.width_scale), int(self.height_scale)))
        self.agg = agg
        self.legend = create_legend()

    def update(self, plot_img, canvas):
        pygame.time.delay(1)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False

        self.window.blit(self.bg, (0, 0))

        # Settings
        COL1 = "#587e76"
        COL2 = "#588c7e"
        COL3 = "#c94c4c"
        COL4 = "#588c7e"

        surface = pygame.Surface((self.width_scale, self.height_scale), pygame.SRCALPHA)
        surface.set_alpha(200)

        for i in range(0, self.tiles):
            for j in range(0, self.tiles):
                # Display background
                pygame.draw.rect(surface, COL4, surface.get_rect())
                self.window.blit(surface, (i * self.width_scale, j * self.height_scale))

                # Display rabbits
                if cfg.terrain[i][j] == Animals.Rabbit:
                    self.window.blit(self.rabbit, (i * self.width_scale, j * self.height_scale))

                # Display wolves
                if cfg.terrain[i][j] == Animals.Wolf_Male:
                    self.window.blit(self.wolf_male, (i * self.width_scale, j * self.height_scale))

                if cfg.terrain[i][j] == Animals.Wolf_Female:
                    self.window.blit(self.wolf_female, (i * self.width_scale, j * self.height_scale))

        self.render_plot(plot_img, canvas, self)

        self.render_legend(self)

        self.render_text(pygame.font.SysFont('arial', 20), self)

        pygame.display.update()

    pygame.quit()


class StartMenu(Plot):
    def __init__(self, width, height):
        # window = pygame.display.set_mode(flags=pygame.RESIZABLE)
        window = pygame.display.set_mode((width, height))
        super().__init__(window, width, height)
        self.start_game = False

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Start Menu")

        bg_img = pygame.image.load('resources/grass_2.jpg')
        rabbit_img = pygame.image.load('resources/rabbit2.jpg')
        wolf_male_img = pygame.image.load('resources/wolf_male.jpg')
        wolf_female_img = pygame.image.load('resources/wolf_female.jpg')

        self.bg = pygame.transform.scale(bg_img, (self.width, self.height))
        self.rabbit = pygame.transform.scale(rabbit_img, (int(self.width_scale), int(self.height_scale)))
        self.wolf_male = pygame.transform.scale(wolf_male_img, (int(self.width_scale), int(self.height_scale)))
        self.wolf_female = pygame.transform.scale(wolf_female_img, (int(self.width_scale), int(self.height_scale)))

    def quit_start_menu(self):
        pygame.quit()

    def update(self):
        while not self.start_game:
            pygame.time.delay(1)

            # surface = pygame.Surface((self.width_scale, self.height_scale))

            self.window.blit(self.bg, (0, 0))

            mouse_x, mouse_y = pygame.mouse.get_pos()

            click = False
            start_button_pos = (300, 300)
            start_button_dims = (200, 100)
            start_button_active_colour = (100, 100, 0)
            start_button_highlight_colour = (255, 255, 255)
            start_button = GUIElements.Button(start_button_pos, start_button_dims, start_button_active_colour,
                                              start_button_highlight_colour)
            start_button.render(self.window)
            start_sim_img = pygame.image.load('resources/start_sim_def_params.png')
            start_sim_img_scaled = pygame.transform.scale(start_sim_img,
                                                          (start_button_dims[0], (int(start_button_dims[0] * start_sim_img.get_height() // start_sim_img.get_width()))))
            self.window.blit(start_sim_img_scaled, (start_button_pos[0], start_button_pos[1] * 1.05))

            settings_button_pos = (100, 100)
            settings_button_dims = (200, 200)
            settings_button_active_colour = (100, 100, 0)
            settings_button_highlight_colour = (255, 255, 255)
            settings_button = GUIElements.Button(settings_button_pos, settings_button_dims, settings_button_active_colour,
                                              settings_button_highlight_colour)
            settings_button.render(self.window)
            settings_img = pygame.image.load('resources/go_to_settings.png')
            settings_img_scaled = pygame.transform.scale(settings_img,
                                                          (settings_button_dims[0], (int(settings_button_dims[0] * settings_img.get_height() // settings_img.get_width()))))
            self.window.blit(settings_img_scaled, (settings_button_pos[0], settings_button_pos[1] * 1.5))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        click = True

            if click:
                if start_button.collidepoint(mouse_x, mouse_y):
                    print("[START MENU] start_game has just been clicked!")
                    print_settings()
                    self.start_game = True

                elif settings_button.collidepoint(mouse_x, mouse_y):
                    print("[START MENU] going to settings...")
                    settings_menu = SettingsMenu(self.window, self)
                    settings_menu.update()

            pygame.display.update()

    # pygame.quit()


class SettingsMenu(Plot):
    def __init__(self, window, previous_start_menu):
        super().__init__(window, window.get_width(), window.get_height())
        self.settings_ready = False
        self.start_menu = previous_start_menu

        pygame.display.set_caption("Settings Menu")

        bg_img = pygame.image.load('resources/grass_2.jpg')
        rabbit_img = pygame.image.load('resources/rabbit2.jpg')
        wolf_male_img = pygame.image.load('resources/wolf_male.jpg')
        wolf_female_img = pygame.image.load('resources/wolf_female.jpg')

        self.bg = pygame.transform.scale(bg_img, (self.width, self.height))
        self.rabbit = pygame.transform.scale(rabbit_img, (int(self.width_scale), int(self.height_scale)))
        self.wolf_male = pygame.transform.scale(wolf_male_img, (int(self.width_scale), int(self.height_scale)))
        self.wolf_female = pygame.transform.scale(wolf_female_img, (int(self.width_scale), int(self.height_scale)))

    def update(self):
        slider_width, slider_height = 300, 6
        slider_colour = "#3e4444"
        default_N = 10

        N_slider_x, N_slider_y = 100, 100
        rabbits_no_slider_x, rabbits_no_slider_y = 100, 200
        wolves_no_slider_x, wolves_no_slider_y = 100, 300
        rabbit_reproduction_rate_slider_x, rabbit_reproduction_rate_slider_y = 100, 400

        slider_N = GUIElements.Slider(N_slider_x, N_slider_y, slider_width, slider_height, slider_colour)
        slider_rabbits = GUIElements.Slider(rabbits_no_slider_x, rabbits_no_slider_y, slider_width, slider_height,
                                            slider_colour)
        slider_wolves = GUIElements.Slider(wolves_no_slider_x, wolves_no_slider_y, slider_width, slider_height,
                                           slider_colour)
        slider_reproduction_rate = GUIElements.Slider(rabbit_reproduction_rate_slider_x,
                                                      rabbit_reproduction_rate_slider_y, slider_width, slider_height,
                                                      slider_colour)

        slider_N.set_default_range(default_N, default_N * 10)

        start_button_dims = (200, 70)
        start_button_pos = (self.window.get_width() // 2 + start_button_dims[0] // 4,
                            (rabbit_reproduction_rate_slider_y + start_button_dims[1]))
        start_button_active_colour = (100, 100, 0)
        start_button_highlight_colour = (255, 255, 255)
        start_button = GUIElements.Button(start_button_pos, start_button_dims, start_button_active_colour,
                                          start_button_highlight_colour)
        start_sim_img = pygame.image.load('resources/save_and_start_simulation.png')
        start_sim_img_scaled = pygame.transform.scale(start_sim_img,
                                                      (start_button_dims[0], (int(start_button_dims[0] * start_sim_img.get_height() // start_sim_img.get_width()))))

        start_menu_button_dims = (200, 70)
        start_menu_button_pos = (self.window.get_width() // 4 - start_button_dims[0] // 2,
                            (rabbit_reproduction_rate_slider_y + start_button_dims[1]))
        start_menu_button_active_colour = (100, 100, 0)
        start_menu_button_highlight_colour = (255, 255, 255)
        start_menu_button = GUIElements.Button(start_menu_button_pos, start_menu_button_dims, start_menu_button_active_colour,
                                          start_menu_button_highlight_colour)
        back_to_start_menu_img = pygame.image.load('resources/back_to_start_menu.png')
        back_to_start_menu_img_scaled = pygame.transform.scale(back_to_start_menu_img,
                                                      (start_menu_button_dims[0], (int(start_menu_button_dims[0] * back_to_start_menu_img.get_height() // back_to_start_menu_img.get_width()))))

        while not self.settings_ready:
            pygame.time.delay(1)

            # Settings
            # surface = pygame.Surface((self.width_scale, self.height_scale))

            self.window.blit(self.bg, (0, 0))

            mouse_x, mouse_y = pygame.mouse.get_pos()

            click = False

            slider_N.perform(self.window)
            slider_rabbits.perform(self.window)
            slider_wolves.perform(self.window)
            slider_reproduction_rate.perform(self.window)

            text_bg_surf = pygame.Surface((self.width_scale * 3, self.height_scale * 1.5))
            modified_N = slider_N.get_scaled_value()
            text_N = GUIElements.TextLine(pygame.font.SysFont('arial', 20), self, (255, 255, 255),
                                          slider_N.start_x + slider_width * 1.1, N_slider_y - slider_height * 5 // 2 + slider_height // 2, text_bg_surf,
                                          "N: " + str(modified_N), bg=False)
            text_N.render()

            slider_rabbits.set_default_range(0, (1 * modified_N) // 2)
            modified_rabbits_no = slider_rabbits.get_scaled_value()
            text_rabbits = GUIElements.TextLine(pygame.font.SysFont('arial', 20), self, (255, 255, 255),
                                          slider_rabbits.start_x + slider_width * 1.1, slider_rabbits.start_y - slider_height * 5 // 2 + slider_height // 2, text_bg_surf,
                                          "Rabbits: " + str(modified_rabbits_no), bg=False)
            text_rabbits.render()

            slider_wolves.set_default_range(0, (1 * modified_N) // 2)
            modified_wolves_no = slider_wolves.get_scaled_value()
            text_wolves = GUIElements.TextLine(pygame.font.SysFont('arial', 20), self, (255, 255, 255),
                                          slider_wolves.start_x + slider_width * 1.1, slider_wolves.start_y - slider_height * 5 // 2 + slider_height // 2, text_bg_surf,
                                          "Wolves: " + str(modified_wolves_no), bg=False)
            text_wolves.render()

            slider_reproduction_rate.set_default_range(0, 1)
            modified_reproduction_chances = slider_reproduction_rate.get_scaled_value(decimal=True)
            text_reproduction_chances = GUIElements.TextLine(pygame.font.SysFont('arial', 20), self, (255, 255, 255),
                                          slider_reproduction_rate.start_x + slider_width * 1.1, slider_reproduction_rate.start_y - slider_height * 5 // 2 + slider_height // 2, text_bg_surf,
                                          "Rabbit Reproduction Chances: " + str(modified_reproduction_chances / 100), bg=False)
            text_reproduction_chances.render()

            cfg.N, cfg.rabbit_no, cfg.wolf_no, cfg.reproduction_chances = modified_N, modified_rabbits_no, modified_wolves_no, modified_reproduction_chances
            cfg.terrain = [[None for _ in range(cfg.N)] for _ in range(cfg.N)]

            start_button.render(self.window)
            self.window.blit(start_sim_img_scaled, (start_button_pos[0], start_button_pos[1] * 0.99))

            start_menu_button.render(self.window)
            self.window.blit(back_to_start_menu_img_scaled, (start_menu_button_pos[0], start_menu_button_pos[1] * 0.99))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        click = True

            if click:
                if start_button.collidepoint(mouse_x, mouse_y):
                    print("[SETTINGS MENU] start_game has just been clicked!")
                    print_settings()
                    self.start_menu.start_game = True
                    self.settings_ready = True

                elif start_menu_button.collidepoint(mouse_x, mouse_y):
                    print("[SETTINGS MENU] going back to start menu...")
                    self.settings_ready = True
                    cfg.get_default_settings()
                    self.start_menu.update()

            pygame.display.update()


class TilesPlot(Plot):
    def __init__(self, width, height):
        window = pygame.display.set_mode(flags=pygame.RESIZABLE)
        super().__init__(window, window.get_width(), window.get_height())
        self.running = True

        pygame.init()
        # self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Visualisation")

    def update(self):
        pygame.time.delay(1)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False

        COL1 = "#587e76"
        COL2 = "#588c7e"
        COL3 = "#c94c4c"
        COL4 = "#588c7e"
        surface = pygame.Surface((self.width_scale, self.height_scale), pygame.SRCALPHA)
        surface_rabbit = pygame.Surface((self.width_scale, self.height_scale))
        surface_wolf = pygame.Surface((self.width_scale, self.height_scale))
        surface.set_alpha(200)
        lwd = 1

        for i in range(0, self.tiles):
            for j in range(0, self.tiles):
                # if wyspa[i][j] != "k":
                #    pygame.draw.rect(surface_rabbit, (0, 0, 0), surface_rabbit.get_rect())
                #    self.window.blit(surface_rabbit, (i * self.width_scale, j * self.height_scale))

                # if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                #    pygame.draw.rect(surface, COL1, surface.get_rect())
                #    self.window.blit(surface, (i * self.width_scale, j * self.height_scale))
                # pass

                # if (i % 2 == 0 and j % 2 != 0) or (i % 2 != 0 and j % 2 == 0):
                #    pygame.draw.rect(surface, COL2, surface.get_rect())
                #    self.window.blit(surface, (i * self.width_scale, j * self.height_scale))
                # pass

                pygame.draw.rect(surface, (0, 0, 0), surface.get_rect())
                self.window.blit(surface, (i * self.width_scale, j * self.height_scale))

                if cfg.terrain[i][j] == Animals.Rabbit:
                    pygame.draw.rect(surface_rabbit, COL3, surface_rabbit.get_rect())
                    self.window.blit(surface_rabbit, (i * self.width_scale, j * self.height_scale))

                if cfg.terrain[i][j] == Animals.Wolf:
                    pygame.draw.rect(surface_wolf, COL2, surface_wolf.get_rect())
                    self.window.blit(surface_wolf, (i * self.width_scale, j * self.height_scale))

        pygame.display.update()

    pygame.quit()
