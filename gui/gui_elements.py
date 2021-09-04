import threading

import pygame
from matplotlib import pyplot as plt

import config as cfg


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
                centered_start_positions = [self.start_x + self.width / 2 - text_width / 2,
                                            self.start_y + self.height / 2 - text_height / 2]
                text_line = GUIElements.TextLine(font, plot, font_colour, centered_start_positions[0],
                                                 centered_start_positions[1], None, text,
                                                 text_shadow_colour=(255, 255, 255), bg_colour=(0, 0, 0), bg=False,
                                                 shadow=False)
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
    print("[GUI ELEMENTS - SETTINGS]", "[N:", cfg.N, "]", "[Rabbits: ", cfg.rabbit_no, "]", "[Wolves: ", cfg.wolf_no, "]",
          "[Rabbit Reproduction Chances:", cfg.rabbit_reproduction_chances / 100, "]",
          "[Wolf Reproduction Chances:", cfg.wolf_reproduction_chances / 100, "]")
