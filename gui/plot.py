import config as cfg
from common import pygame, Directions, time
from animals import *
from fence import *
from gui.gui_elements import GUIElements, active_threads_string, total_animals_no, create_legend, print_settings


class Plot:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.tiles = cfg.N
        self.width_scale = self.width // self.tiles
        self.height_scale = self.height // self.tiles
        self.quit = False

    def render_plot(self, plot_img, canvas, plot):
        plot_surface = pygame.image.fromstring(plot_img, canvas.get_width_height(), "RGB")
        scaled_plot_surface = pygame.transform.scale(plot_surface, (350, 350))
        plot.window.blit(scaled_plot_surface, (plot.width, 0))

    def render_text(self, my_font, plot):
        text_bg_surf = pygame.Surface((plot.width_scale * 7, plot.height_scale + 30))
        active_threads_text_line = GUIElements.TextLine(my_font, plot, (255, 255, 255),
                                                        plot.width + abs((plot.window.get_width() - plot.width) // 5),
                                                        plot.height * 0.7, text_bg_surf, active_threads_string())
        total_animals_text_line = GUIElements.TextLine(my_font, plot, (255, 255, 255),
                                                       plot.width + abs((plot.window.get_width() - plot.width) // 5),
                                                       plot.height * 0.7 + 30, text_bg_surf, total_animals_no(),
                                                       bg=False)
        active_threads_text_line.render()
        total_animals_text_line.render()

    def render_legend(self, plot):
        plot.window.blit(plot.legend, (plot.width + abs((plot.window.get_width() - plot.width) // 4),
                                       plot.height // 2 * 1.075))

    def quit_plot(self):
        self.quit = True
        pygame.quit()


class PlotPhotos(Plot):
    def __init__(self, width, height, agg):
        window = pygame.display.set_mode(flags=pygame.RESIZABLE)
        super().__init__(window, window.get_width() * 3 // 4, window.get_height())
        self.running = True
        self.pause = False

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

    def get_pause_button(self, active_colour):
        pause_button_dims = (105, 70)
        pause_button_pos = (self.width + abs((self.window.get_width() - self.width) // 8), self.height * 0.815)
        pause_button_active_colour = active_colour
        pause_button_highlight_colour = (255, 255, 255)
        pause_button = GUIElements.Button(pause_button_pos, pause_button_dims, pause_button_active_colour,
                                          pause_button_highlight_colour)
        pause_img = pygame.image.load('resources/pause.png')
        pause_img_scaled = pygame.transform.scale(pause_img,
                                                  (pause_button_dims[0], (int(pause_button_dims[
                                                                                  0] * pause_img.get_height() // pause_img.get_width()))))
        return pause_button, pause_img_scaled

    def get_resume_button(self, active_colour):
        resume_button_dims = (105, 70)
        resume_button_pos = (self.width + abs((self.window.get_width() - self.width) // 8), self.height * 0.815)
        resume_button_active_colour = active_colour
        resume_button_highlight_colour = (255, 255, 255)
        resume_button = GUIElements.Button(resume_button_pos, resume_button_dims, resume_button_active_colour,
                                           resume_button_highlight_colour)
        resume_img = pygame.image.load('resources/resume.png')
        resume_img_scaled = pygame.transform.scale(resume_img,
                                                   (resume_button_dims[0], (int(resume_button_dims[
                                                                                    0] * resume_img.get_height() // resume_img.get_width()))))
        return resume_button, resume_img_scaled

    def get_escape_button(self, active_colour):
        escape_button_dims = (105, 70)
        escape_button_pos = (self.width + abs((self.window.get_width() - self.width) // 8 * 4.5), self.height * 0.815)
        escape_button_active_colour = active_colour
        escape_button_highlight_colour = (255, 255, 255)
        escape_button = GUIElements.Button(escape_button_pos, escape_button_dims, escape_button_active_colour,
                                           escape_button_highlight_colour)
        escape_img = pygame.image.load('resources/quit_return.png')
        escape_img_scaled = pygame.transform.scale(escape_img,
                                                   (int(escape_button_dims[0] * 0.985), (int(escape_button_dims[
                                                                                                 0] * escape_img.get_height() // escape_img.get_width()))))
        return escape_button, escape_img_scaled

    def update(self, plot_img, canvas):
        pygame.time.delay(1)

        self.window.blit(self.bg, (0, 0))

        # Colour Settings
        blue_1 = "#587e76"
        blue_2 = "#588c7e"
        dark_raspberry = "#c94c4c"
        olive = (100, 100, 0)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = False

        pause_button, pause_img_scaled = self.get_pause_button(olive)
        resume_button, resume_img_scaled = self.get_resume_button(blue_2)
        escape_button, escape_img_scaled = self.get_escape_button(olive)

        surface = pygame.Surface((self.width_scale, self.height_scale), pygame.SRCALPHA)
        surface.set_alpha(150)

        if cfg.N <= 20:
            lwd = 5
        elif cfg.N <= 30:
            lwd = 3
        elif cfg.N <= 50:
            lwd = 2
        else:
            lwd = 1

        for i in range(0, self.tiles):
            # for i in reversed(range(0, self.tiles)):
            for j in range(0, self.tiles):
                # Display background
                pygame.draw.rect(surface, olive, surface.get_rect())
                self.window.blit(surface, (i * self.width_scale, j * self.height_scale))

                # Display rabbits
                if cfg.terrain[i][j] == Animals.Rabbit:
                    self.window.blit(self.rabbit, (i * self.width_scale, j * self.height_scale))

                # Display wolves
                if cfg.terrain[i][j] == Animals.Wolf_Male:
                    self.window.blit(self.wolf_male, (i * self.width_scale, j * self.height_scale))

                if cfg.terrain[i][j] == Animals.Wolf_Female:
                    self.window.blit(self.wolf_female, (i * self.width_scale, j * self.height_scale))

                current_fence_node = get_fence_node_idx(i, j)
                neighbours_list = cfg.fence[current_fence_node]

                for neighbour_node in neighbours_list:
                    start_x, start_y = get_fence_node_dirs(current_fence_node)[0] * self.width_scale, \
                                       get_fence_node_dirs(current_fence_node)[1] * self.height_scale
                    end_x, end_y = get_fence_node_dirs(neighbour_node)[0] * self.width_scale, \
                                   get_fence_node_dirs(neighbour_node)[1] * self.height_scale
                    # if (start_x, start_y) != (i, j) and (end_x, end_y) != ():
                    colour = [random.randint(0, 255) for _ in range(3)]
                    pygame.draw.line(self.window, (0, 0, 0), (start_x, start_y), (end_x, end_y), lwd)

        self.render_plot(plot_img, canvas, self)

        self.render_legend(self)

        self.render_text(pygame.font.SysFont('arial', 20), self)

        pause_button.render(self.window)

        if self.pause:
            self.window.blit(resume_img_scaled, (resume_button.start_x, resume_button.start_y * 1.025))

        else:
            self.window.blit(pause_img_scaled, (pause_button.start_x, pause_button.start_y * 1.0125))

        escape_button.render(self.window)
        self.window.blit(escape_img_scaled, (escape_button.start_x, escape_button.start_y * 1.0125))

        # pygame.draw.line(self.window, (0, 0, 0), (300, 100), (300 + self.width_scale, 100), 4)
        # pygame.draw.rect(self.window, (0, 0, 0), pygame.Rect(400, 400, self.width_scale, self.height_scale))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True

        if click:
            if pause_button.collidepoint(mouse_x, mouse_y) and not self.pause:
                print("[PLOT] pausing simulation...")
                self.pause = True
            elif pause_button.collidepoint(mouse_x, mouse_y) and self.pause:
                print("[PLOT] resuming simulation...")
                self.pause = False

            elif escape_button.collidepoint(mouse_x, mouse_y):
                print("[PLOT] quit simulation button has just been pressed...")
                self.pause = True
                self.running = False

        pygame.display.update()


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

    def reenter_start_menu(self):
        self.quit = False

    def update(self):
        settings_button_dims = (200, 200)
        settings_button_pos = (self.width // 2 - settings_button_dims[1], self.height // 4)
        settings_button_active_colour = (100, 100, 0)
        settings_button_highlight_colour = (255, 255, 255)
        settings_button = GUIElements.Button(settings_button_pos, settings_button_dims,
                                             settings_button_active_colour,
                                             settings_button_highlight_colour)
        settings_img = pygame.image.load('resources/go_to_settings.png')
        settings_img_scaled = pygame.transform.scale(settings_img,
                                                     (settings_button_dims[0], (int(settings_button_dims[
                                                                                        0] * settings_img.get_height() // settings_img.get_width()))))

        start_button_dims = (200, 200)
        start_button_pos = (self.width // 2, settings_button_pos[1] + settings_button_dims[1])
        start_button_active_colour = (100, 100, 0)
        start_button_highlight_colour = (255, 255, 255)
        start_button = GUIElements.Button(start_button_pos, start_button_dims, start_button_active_colour,
                                          start_button_highlight_colour)
        start_sim_img = pygame.image.load('resources/start_sim_def_params.png')
        start_sim_img_scaled = pygame.transform.scale(start_sim_img,
                                                      (start_button_dims[0], (int(start_button_dims[
                                                                                      0] * start_sim_img.get_height() // start_sim_img.get_width()))))

        while not self.start_game:
            pygame.time.delay(1)

            # surface = pygame.Surface((self.width_scale, self.height_scale))

            self.window.blit(self.bg, (0, 0))

            mouse_x, mouse_y = pygame.mouse.get_pos()
            click = False

            settings_button.render(self.window)
            self.window.blit(settings_img_scaled, (settings_button_pos[0], settings_button_pos[1] * 1.3))

            start_button.render(self.window)
            self.window.blit(start_sim_img_scaled, (start_button_pos[0], start_button_pos[1] * 1.15))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.quit = True
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        click = True

            if click:
                if start_button.collidepoint(mouse_x, mouse_y):
                    print("[START MENU] start_game has just been clicked!")
                    print_settings()
                    self.start_game = True
                    # self.quit_plot()
                    pygame.quit()

                elif settings_button.collidepoint(mouse_x, mouse_y):
                    print("[START MENU] going to settings...")
                    settings_menu = SettingsMenu(self.window, self)
                    settings_menu.update()

            if self.quit or self.start_game:
                if pygame.get_init():
                    pygame.quit()
                break

            pygame.display.update()

        if self.start_game:
            pygame.quit()


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

    def get_map_button(self, active_colour, start_x, start_y):
        map_button_dims = (200, 70)
        map_button_active_colour = active_colour
        map_button_highlight_colour = (255, 255, 255)
        map_button = GUIElements.Button((start_x, start_y), map_button_dims, map_button_active_colour,
                                        map_button_highlight_colour)
        map_img = pygame.image.load('resources/map_settings.png')
        map_img_scaled = pygame.transform.scale(map_img,
                                                (int(map_button_dims[0] * 0.985), (int(map_button_dims[
                                                                                           0] * map_img.get_height() // map_img.get_width()))))
        return map_button, map_img_scaled

    def update(self):
        slider_width, slider_height = 300, 6
        # slider_colour = "#3e4444"  # gray
        slider_colour = "#840032"  # pink
        default_N = 10

        N_slider_x, N_slider_y = 100, self.height * 0.2
        rabbits_no_slider_x, rabbits_no_slider_y = 100, N_slider_y + 50
        wolves_no_slider_x, wolves_no_slider_y = 100, rabbits_no_slider_y + 50
        rabbit_reproduction_rate_slider_x, rabbit_reproduction_rate_slider_y = 100, wolves_no_slider_y + 50
        wolf_reproduction_rate_slider_x, wolf_reproduction_rate_slider_y = 100, rabbit_reproduction_rate_slider_y + 50

        slider_N = GUIElements.Slider(N_slider_x, N_slider_y, slider_width, slider_height, slider_colour)
        slider_rabbits = GUIElements.Slider(rabbits_no_slider_x, rabbits_no_slider_y, slider_width, slider_height,
                                            slider_colour)
        # slider_colour = "#2F4F4F"
        # slider_colour = (0, 0, 0)
        # slider_colour = "#343a40"
        # slider_colour = "#38040e"
        # slider_colour = "#85182a"

        slider_wolves = GUIElements.Slider(wolves_no_slider_x, wolves_no_slider_y, slider_width, slider_height,
                                           slider_colour)
        slider_rabbit_reproduction_rate = GUIElements.Slider(rabbit_reproduction_rate_slider_x,
                                                             rabbit_reproduction_rate_slider_y, slider_width,
                                                             slider_height,
                                                             slider_colour)
        slider_wolf_reproduction_rate = GUIElements.Slider(wolf_reproduction_rate_slider_x,
                                                           wolf_reproduction_rate_slider_y, slider_width, slider_height,
                                                           slider_colour)

        slider_N.set_default_range(default_N, default_N * 10)

        button_dims = (200, 70)

        map_button, map_img_scaled = self.get_map_button((100, 100, 0),
                                                         self.window.get_width() // 2 - button_dims[0] // 2 * 1.2,
                                                         wolf_reproduction_rate_slider_y + button_dims[1] // 4 * 3)

        start_button_dims = button_dims
        start_button_pos = (self.window.get_width() // 2 + button_dims[0] // 4,
                            (map_button.start_y + 1.5 * start_button_dims[1]))
        start_button_active_colour = (100, 100, 0)
        start_button_highlight_colour = (255, 255, 255)
        start_button = GUIElements.Button(start_button_pos, start_button_dims, start_button_active_colour,
                                          start_button_highlight_colour)
        start_sim_img = pygame.image.load('resources/save_and_start_simulation.png')
        start_sim_img_scaled = pygame.transform.scale(start_sim_img,
                                                      (start_button_dims[0], (int(start_button_dims[
                                                                                      0] * start_sim_img.get_height() // start_sim_img.get_width()))))

        start_menu_button_dims = button_dims
        start_menu_button_pos = (self.window.get_width() // 4 - start_button_dims[0] // 2,
                                 (map_button.start_y + 1.5 * start_button_dims[1]))
        start_menu_button_active_colour = (100, 100, 0)
        start_menu_button_highlight_colour = (255, 255, 255)
        start_menu_button = GUIElements.Button(start_menu_button_pos, start_menu_button_dims,
                                               start_menu_button_active_colour,
                                               start_menu_button_highlight_colour)
        back_to_start_menu_img = pygame.image.load('resources/back_to_start_menu.png')
        back_to_start_menu_img_scaled = pygame.transform.scale(back_to_start_menu_img,
                                                               (start_menu_button_dims[0], (int(start_menu_button_dims[
                                                                                                    0] * back_to_start_menu_img.get_height() // back_to_start_menu_img.get_width()))))

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
            slider_rabbit_reproduction_rate.perform(self.window)
            slider_wolf_reproduction_rate.perform(self.window)

            text_bg_surf = pygame.Surface((self.width_scale * 3, self.height_scale * 1.5))
            modified_N = slider_N.get_scaled_value()
            text_N = GUIElements.TextLine(pygame.font.SysFont('arial', 20), self, (255, 255, 255),
                                          slider_N.start_x + slider_width * 1.1,
                                          N_slider_y - slider_height * 5 // 2 + slider_height // 2, text_bg_surf,
                                          "N: " + str(modified_N), bg=False)
            text_N.render()

            slider_rabbits.set_default_range(0, (1 * modified_N) // 2)
            modified_rabbits_no = slider_rabbits.get_scaled_value()
            text_rabbits = GUIElements.TextLine(pygame.font.SysFont('arial', 20), self, (255, 255, 255),
                                                slider_rabbits.start_x + slider_width * 1.1,
                                                slider_rabbits.start_y - slider_height * 5 // 2 + slider_height // 2,
                                                text_bg_surf,
                                                "Rabbits: " + str(modified_rabbits_no), bg=False)
            text_rabbits.render()

            slider_wolves.set_default_range(0, (1 * modified_N) // 2)
            modified_wolves_no = slider_wolves.get_scaled_value()
            text_wolves = GUIElements.TextLine(pygame.font.SysFont('arial', 20), self, (255, 255, 255),
                                               slider_wolves.start_x + slider_width * 1.1,
                                               slider_wolves.start_y - slider_height * 5 // 2 + slider_height // 2,
                                               text_bg_surf,
                                               "Wolves: " + str(modified_wolves_no), bg=False)
            text_wolves.render()

            slider_rabbit_reproduction_rate.set_default_range(0, 1)
            rabbit_modified_reproduction_chances = slider_rabbit_reproduction_rate.get_scaled_value(decimal=True)
            text_rabbit_reproduction_chances = GUIElements.TextLine(pygame.font.SysFont('arial', 20), self,
                                                                    (255, 255, 255),
                                                                    slider_rabbit_reproduction_rate.start_x + slider_width * 1.1,
                                                                    slider_rabbit_reproduction_rate.start_y - slider_height * 5 // 2 + slider_height // 2,
                                                                    text_bg_surf,
                                                                    "Rabbit Reproduction Chances: " + str(
                                                                        rabbit_modified_reproduction_chances / 100),
                                                                    bg=False)
            text_rabbit_reproduction_chances.render()

            slider_wolf_reproduction_rate.set_default_range(0, 1)
            wolf_modified_reproduction_chances = slider_wolf_reproduction_rate.get_scaled_value(decimal=True)
            text_wolf_reproduction_chances = GUIElements.TextLine(pygame.font.SysFont('arial', 20), self,
                                                                  (255, 255, 255),
                                                                  slider_wolf_reproduction_rate.start_x + slider_width * 1.1,
                                                                  slider_wolf_reproduction_rate.start_y - slider_height * 5 // 2 + slider_height // 2,
                                                                  text_bg_surf,
                                                                  "Wolf Reproduction Chances: " + str(
                                                                      wolf_modified_reproduction_chances / 100),
                                                                  bg=False)
            text_wolf_reproduction_chances.render()

            cfg.N, cfg.rabbit_no, cfg.wolf_no, cfg.rabbit_reproduction_chances, cfg.wolf_reproduction_chances \
                = modified_N, modified_rabbits_no, modified_wolves_no, rabbit_modified_reproduction_chances, wolf_modified_reproduction_chances
            cfg.terrain = [[None for _ in range(cfg.N)] for _ in range(cfg.N)]
            cfg.fence = [list() for _ in range((cfg.N + 1) ** 2)]

            start_button.render(self.window)
            self.window.blit(start_sim_img_scaled, (start_button_pos[0], start_button_pos[1] * 0.99))

            start_menu_button.render(self.window)
            self.window.blit(back_to_start_menu_img_scaled, (start_menu_button_pos[0], start_menu_button_pos[1] * 0.99))

            map_button.render(self.window)
            self.window.blit(map_img_scaled, (map_button.start_x, map_button.start_y * 1.035))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.quit_plot()
                    self.start_menu.quit_plot()
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
                    cfg.set_default_parameters()
                    self.start_menu.update()

                elif map_button.collidepoint(mouse_x, mouse_y):
                    print("[SETTINGS MENU] entering map menu...")
                    map_menu = MapMenu(self.window, self)
                    map_menu.update()

            if self.quit or self.settings_ready:
                break

            pygame.display.update()


class MapMenu(Plot):
    def __init__(self, window, settings_menu):
        super().__init__(window, window.get_width(), window.get_height())
        self.map_ready = False
        self.settings_menu = settings_menu

        pygame.display.set_caption("Map Settings")

        bg_img = pygame.image.load('resources/grass_2.jpg')

        self.bg = pygame.transform.scale(bg_img, (self.width, self.height))

    def get_save_button(self, active_colour, start_x, start_y):
        save_button_dims = (200, 70)
        save_button_active_colour = active_colour
        save_button_highlight_colour = (255, 255, 255)
        save_button = GUIElements.Button((start_x, start_y), save_button_dims, save_button_active_colour,
                                         save_button_highlight_colour)
        save_img = pygame.image.load('resources/map_settings.png')
        save_img_scaled = pygame.transform.scale(save_img,
                                                 (int(save_button_dims[0] * 0.985),
                                                  (int(save_button_dims[0] * save_img.get_height() //
                                                       save_img.get_width()))))
        return save_button, save_img_scaled

    def get_fence_slider(self):
        # slider_colour = "#3e4444"  # gray
        slider_colour = "#840032"  # pink
        slider_width, slider_height = 300, 6
        fence_slider_x, fence_slider_y = 100, self.height * 0.7
        min_fence_elements = 0

        slider_fence = GUIElements.Slider(fence_slider_x, fence_slider_y, slider_width, slider_height, slider_colour)
        slider_fence.set_default_range(min_fence_elements,
                                       (min_fence_elements + 1) * 3)  # FIX THIS, HOW MANY MAZE ISLANDS MAX???

        return slider_fence

    def get_fence_slider_text(self, slider_fence):
        text_bg_surf = pygame.Surface((self.width_scale * 3, self.height_scale * 1.5))
        slider_width, slider_height = 300, 6
        fence_slider_x, fence_slider_y = 100, self.height * 0.7
        modified_fence_elements = slider_fence.get_scaled_value()
        text_fence = GUIElements.TextLine(pygame.font.SysFont('arial', 20), self, (255, 255, 255),
                                          slider_fence.start_x + slider_width * 1.1,
                                          fence_slider_y - slider_height * 5 // 2 + slider_height // 2, text_bg_surf,
                                          "Fence Islands: " + str(modified_fence_elements), bg=False)

        return text_fence

    def update_config_fence_settings(self, slider_fence):
        cfg.fence_elements = slider_fence.get_scaled_value()

    def generate_random_fence(self):
        print(config.N)
        reset_fence()
        dfs_build(451)

    def draw_current_mazes(self):
        lwd = 3
        surface = pygame.Surface((self.width_scale, self.height_scale), pygame.SRCALPHA)
        surface.set_alpha(150)
        olive = (100, 100, 0)

        for i in range(0, self.tiles):
            for j in range(0, self.tiles):
                current_fence_node = get_fence_node_idx(i, j)
                neighbours_list = cfg.fence[current_fence_node]

                for neighbour_node in neighbours_list:
                    start_x, start_y = get_fence_node_dirs(current_fence_node)[0] * self.width_scale, \
                                       get_fence_node_dirs(current_fence_node)[1] * self.height_scale
                    end_x, end_y = get_fence_node_dirs(neighbour_node)[0] * self.width_scale, \
                                   get_fence_node_dirs(neighbour_node)[1] * self.height_scale
                    pygame.draw.line(self.window, (0, 0, 0), (start_x, start_y), (end_x, end_y), lwd)
                # Display background
                pygame.draw.rect(surface, olive, surface.get_rect())
                self.window.blit(surface, (i * self.width_scale, j * self.height_scale))
                pass

    def update(self):
        # Colour Settings
        blue_1 = "#587e76"
        blue_2 = "#588c7e"
        dark_raspberry = "#c94c4c"
        olive = (100, 100, 0)

        button_dims = (200, 70)
        save_button, save_img_scaled = self.get_save_button((100, 100, 0),
                                                            self.window.get_width() // 2 - button_dims[0] // 2 * 1.2,
                                                            self.window.get_height() * 0.7 + button_dims[1] // 4 * 3)
        slider_fence = self.get_fence_slider()

        while not self.map_ready:
            pygame.time.delay(1)

            self.window.blit(self.bg, (0, 0))

            mouse_x, mouse_y = pygame.mouse.get_pos()
            click = False

            surface = pygame.Surface((self.width_scale, self.height_scale), pygame.SRCALPHA)
            surface.set_alpha(150)

            slider_fence.perform(self.window)
            text_fence = self.get_fence_slider_text(slider_fence)
            text_fence.render()
            self.update_config_fence_settings(slider_fence)

            save_button.render(self.window)
            self.window.blit(save_img_scaled, (save_button.start_x, save_button.start_y * 1.035))

            # for i in range(0, self.tiles):
            #     for j in range(0, self.tiles):
            #         # Display background
            #         pygame.draw.rect(surface, olive, surface.get_rect())
            #         self.window.blit(surface, (i * self.width_scale, j * self.height_scale))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.quit_plot()
                    self.settings_menu.quit_plot()
                    self.settings_menu.start_menu.quit_plot()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        click = True

            if self.quit:
                break

            self.draw_current_mazes()

            if click:
                if save_button.collidepoint(mouse_x, mouse_y):
                    print("[MAP SETTINGS MENU] saving map settings and going back to main settings menu...")
                    self.map_ready = True
                    self.settings_menu.update()
                    print("Generated Fence Settings: ", cfg.fence)

                else:
                    self.generate_random_fence()

            if self.quit or self.map_ready:
                break

            pygame.display.update()
