import pygame
import random
import os
import time
import math
from typing import Tuple
from .config import GameCnst



class RandomAttitude:
    def __init__(self):
        self.roll = self.get_random(35, 55)
        self.pitch = self.get_random(20, 50)

    #@staticmethod
    def get_random(self, minimum, maximum):
        return random.randrange(minimum, maximum, 1) * random.choice([-1, 1])

    def __iter__(self):
        return self

    def __next__(self):
#        yield self.roll, self.pitch
        self.roll = self.get_random(45, 75)
        self.pitch = self.get_random(30, 70)
        return self.roll, self.pitch


class UpsetRecoveryWindow:
    # def __new__(cls, test=True, presenter=None):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(UpsetRecoveryWindow, cls).__new__(cls)
    #     return cls.instance

    def __init__(self, test=True, presenter=None):
        self.presenter = presenter
        if test:
            self.experiment_number = GameCnst.CYCLE_NUMBER
            self.upset_positions = (attitude for attitude in GameCnst.UPSET_POSITIONS)
        else:
            self.experiment_number = 256
            self.upset_positions = RandomAttitude()

        self.roll_list = []
        self.pitch_list = []
        self.joystick_roll_list = []
        self.joystick_pitch_list = []
        self.experiment_results = {}
        self.pitch_coefficient = 11.35

        self.tick_counter = 0
        self.experiment_duration = GameCnst.FPS * GameCnst.EXPERIMENT_DURATION
        pygame.init()
     #   pygame.mixer.init()  # для звука
        self.screen = pygame.display.set_mode(GameCnst.WINDOW_SIZE, pygame.RESIZABLE)
        pygame.display.set_caption("Upset Recovery")
        self.game_clock = pygame.time.Clock()
        self.cycle_counter = 1
        window_size = self.screen.get_size()
        self.window_center = (window_size[0] / 2, window_size[1] / 2)
        self.indicator_surface = pygame.surface.Surface(window_size, pygame.SRCALPHA, 32)
        self.indicator_surface.convert_alpha()
        self.roll_indicator_surface = pygame.surface.Surface((400, 300), pygame.SRCALPHA, 32)
        self.roll_indicator_surface.convert_alpha()
        self.image_width = 736 * 2
        self.image_height = 2264
        self.frame_side_clearence = 0
        self.frame_image_clearence = 100
        self.frame_size = (window_size[0], window_size[0] - self.frame_image_clearence * 2)
        self.pfd_frame = pygame.surface.Surface(size=self.frame_size)
        self.frame_end_height = 64
        self.upper_frame_end = pygame.rect.Rect((
            self.frame_side_clearence,
            self.frame_image_clearence - self.frame_end_height,
            self.image_width - 2 * self.image_width,
            self.frame_end_height
        ))
        self.lower_frame_end = pygame.rect.Rect((
            self.frame_side_clearence,
            self.frame_size[1] + self.frame_image_clearence,
            self.image_width - 2 * self.image_width,
            self.frame_end_height
        ))

        self.frame_center = (self.frame_size[0] / 2, self.frame_size[1] - self.frame_side_clearence / 2)

        self.background = pygame.surface.Surface((self.image_width, self.image_height), pygame.SRCALPHA, 32)
        self.background.convert_alpha()
        self.background_y = self.window_center[1]
        self.background_center = self.window_center
        upset_positions = next(self.upset_positions)
        self.roll = upset_positions[0]
        self.pitch = upset_positions[1]
        self.pfd_image = pygame.image.load(os.path.abspath(os.path.dirname(__file__)) + os.sep + 'pfd.png').convert()
        self.pfd_rect = self.pfd_image.get_rect(bottomright=(self.image_width, self.image_height))
        self.number_font = self.initialize_font(size=100)



        # indicators
        flat_roll_pointer_tip_y = self.background_center[1] - GameCnst.ROLL_POINTER_TIP_ELEVATION
        roll_pointer_tip_y = 150 - GameCnst.ROLL_POINTER_TIP_ELEVATION
        self.flat_roll_pointer = [
            (self.window_center[0], flat_roll_pointer_tip_y),
            (self.window_center[0] + GameCnst.ROLL_POINTER_WIDTH / 2, flat_roll_pointer_tip_y - GameCnst.ROLL_POINTER_HEIGHT),
            (self.window_center[0] - GameCnst.ROLL_POINTER_WIDTH / 2, flat_roll_pointer_tip_y - GameCnst.ROLL_POINTER_HEIGHT)
        ]
        self.list_of_points = []
        for degrees in [10, 20, 30, 45, 60]:
            for direction in [True, False]:
                self.list_of_points.append(self.calculate_roll_indicator_points(degrees, direction))

        # self.roll_pointer = [
        #     (self.window_center[0], roll_pointer_tip_y),
        #     (self.window_center[0] + GameCnst.ROLL_POINTER_WIDTH, roll_pointer_tip_y + GameCnst.ROLL_POINTER_HEIGHT),
        #     (self.window_center[0] - GameCnst.ROLL_POINTER_WIDTH, roll_pointer_tip_y + GameCnst.ROLL_POINTER_HEIGHT)
        # ]

        self.roll_pointer = [
            (200, roll_pointer_tip_y),
            (200 + GameCnst.ROLL_POINTER_WIDTH, roll_pointer_tip_y + GameCnst.ROLL_POINTER_HEIGHT),
            (200 - GameCnst.ROLL_POINTER_WIDTH, roll_pointer_tip_y + GameCnst.ROLL_POINTER_HEIGHT)
        ]
        self.crosshair_L_part = [
            [self.window_center[0] - GameCnst.CROSSHAIR_CLEARANCE - GameCnst.CROSSHAIR_WIDTH, self.window_center[1]],
            [self.window_center[0] - GameCnst.CROSSHAIR_CLEARANCE, self.window_center[1]],
            [self.window_center[0] - GameCnst.CROSSHAIR_CLEARANCE, self.window_center[1] + GameCnst.CROSSHAIR_HEIGHT]
        ]
        self.crosshair_R_part = [
            (self.window_center[0] + GameCnst.CROSSHAIR_CLEARANCE + GameCnst.CROSSHAIR_WIDTH, self.window_center[1]),
            (self.window_center[0] + GameCnst.CROSSHAIR_CLEARANCE, self.window_center[1]),
            (self.window_center[0] + GameCnst.CROSSHAIR_CLEARANCE, self.window_center[1] + GameCnst.CROSSHAIR_HEIGHT)
        ]

    def countdown(self, screen, count_times: int):
        ticks_in_seconds = 1000
        last = pygame.time.get_ticks()
        counts = ['GO!', *range(1, count_times + 1)]
        self.render_number(screen, counts.pop())
        while counts:
            now = pygame.time.get_ticks()
            if now - last >= ticks_in_seconds:
                last = now
                count = counts.pop()
                self.render_number(screen, count)


    def initialize_font(
            self,
            font_family: str = 'didot.ttc',
            size: int = 128,
            bold: bool = True
    ):
        return pygame.font.SysFont(font_family, size, bold)

    def render_number(self, screen, number: int) -> None:
        screen.fill(GameCnst.BLACK)
        number_img = self.number_font.render(str(number), True, GameCnst.GREEN)
        place = number_img.get_rect(center=self.window_center)
        screen.blit(number_img, place)
        pygame.display.update()

    def calculate_roll_indicator_points(self, degrees, positive=True):
        if degrees in [30, 60]:
            line_length = GameCnst.ROLL_INDICATOR_LINE_LENGTH * 2
        else:
            line_length = GameCnst.ROLL_INDICATOR_LINE_LENGTH
        if positive:
            pos = 1
        else:
            pos = -1
        rads = math.radians(degrees)
        clearence_start = (
            GameCnst.ROLL_INDICATOR_LINE_CLEARANCE * math.sin(rads),
            GameCnst.ROLL_INDICATOR_LINE_CLEARANCE * math.cos(rads))
        y_start = self.window_center[1] - clearence_start[1]
        clearance_and_length = GameCnst.ROLL_INDICATOR_LINE_CLEARANCE + line_length
        clearence_end = (clearance_and_length * math.sin(rads),
                         clearance_and_length * math.cos(rads))
        y_end = self.window_center[1] - clearence_end[1]
        return (self.window_center[0] + clearence_start[0] * pos, y_start), (self.window_center[0] + clearence_end[0] * pos, y_end)

    def run(self):

        self.countdown(self.screen, GameCnst.INTERVAL)

        running = True
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(j) for j in range(pygame.joystick.get_count())]
        for j in joysticks:
            j.init()
            print(j.get_name())

        if not joysticks:
            joystick_roll, joystick_pitch = None, None

        while running:


            self.game_clock.tick(GameCnst.FPS)

            # Ввод процесса (события)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    return None

                #if event.type == pygame.JOYAXISMOTION:
            for joystick in joysticks:
                joystick_roll, joystick_pitch = self.get_joystick_declinations(
                    joystick
                )
                self.roll += joystick_roll
                corrected_pitch = self.get_corrected_picth_declination(
                    joystick_pitch
                )
                if -72 < self.pitch + corrected_pitch < 72:
                    self.pitch += corrected_pitch

            self.parameters_update(joystick_roll, joystick_pitch)

            self.render_pfd()



    def get_corrected_picth_declination(self, joystick_pitch) -> float:
        roll_cosinus = math.cos(math.radians(self.roll))
        pitch_normalizer = ((90 - abs(self.pitch)) / 90) * \
                           (1 - abs(math.sin(math.radians(self.pitch))) + 0.09)
        pitch_normalizer = 0.25 + pitch_normalizer * 0.75

        upset_modifier = 1 if roll_cosinus >= 0 else -1
        if joystick_pitch >= 0:
            joy_pitch = joystick_pitch * roll_cosinus * pitch_normalizer * 0.7
        else:
            joy_pitch = joystick_pitch * 0.3 * pitch_normalizer * upset_modifier\
                        - joystick_pitch * 0.1 * pitch_normalizer * roll_cosinus

        joy_pitch -= (0.4 * (math.sin(math.radians(self.roll)) ** 2) +
                      0.03 * (1 - upset_modifier)) * (0.12 + pitch_normalizer)

        return joy_pitch

    def get_joystick_declinations(self, joystick) -> Tuple[float, float]:
        pos_axis_0 = joystick.get_axis(0)
        pos_axis_1 = joystick.get_axis(1)
        joystick_roll = pos_axis_0 \
            if abs(pos_axis_0) > 0.12 else 0
        joystick_pitch = pos_axis_1 \
            if abs(pos_axis_1) > 0.12 else 0
        return joystick_roll, joystick_pitch

    def render_pfd(self):
        self.screen.fill(GameCnst.BLACK)
        self._draw_skybox(self.screen)
        self.background.blit(
            self.pfd_image,
            (self.pfd_rect.x, self.pitch * self.pitch_coefficient)
        )
        rotated_background = pygame.transform.rotate(self.background, self.roll)
        rotated_rect = rotated_background.get_rect(center=self.window_center)
        self.screen.blit(rotated_background, rotated_rect)  # ЭТО РАБОТАЕТ
        self._draw_shutters(self.screen)
        self._draw_inidicator(self.screen)
        pygame.display.flip()

    def _draw_skybox(self, screen) -> None:
        mid_height = GameCnst.WINDOW_HEIGHT // 2
        rect_height = mid_height - GameCnst.SHUTTER_HEIGHT
        pygame.draw.rect(
            screen,
            GameCnst.SKYBLUE,
            (0, GameCnst.SHUTTER_HEIGHT, GameCnst.WINDOW_WIDTH, rect_height),
            width=0
        )
        pygame.draw.rect(
            screen,
            GameCnst.GROUNDBROWN,
            (0, mid_height, GameCnst.WINDOW_WIDTH, rect_height),
            width=0
        )

    def parameters_update(
            self,
            joystick_roll: float,
            joystick_pitch: float
    ) -> None:
        center_x, center_y = self.window_center
        self.background_y = center_y + self.pitch * self.pitch_coefficient
        self.background_center = (center_x, self.background_y)

        self.roll_list.append(self.roll)
        self.joystick_roll_list.append(joystick_roll)
        self.pitch_list.append(self.pitch)
        self.joystick_pitch_list.append(joystick_pitch)

        self.tick_counter += 1
        if self.tick_counter > self.experiment_duration:
            self.experiment_results[self.cycle_counter] = dict(
                zip(
                    ['roll_list', 'pitch_list', 'joy_roll', 'joy_pitch'],
                    [self.roll_list, self.pitch_list,
                     self.joystick_roll_list, self.joystick_pitch_list]
                )
            )

            if self.cycle_counter == self.experiment_number:
                self.presenter.write_experiment_data(self.experiment_results)
                for i in self.experiment_results.keys():
                    for j in self.experiment_results[i].keys():
                        print(f' {i} {j} --- {self.experiment_results[i][j]}')
                running = False
                pygame.quit()
                return self.experiment_results
            self.countdown(self.screen, GameCnst.INTERVAL)

            self.roll_list = []
            self.joystick_roll_list = []
            self.pitch_list = []
            self.joystick_pitch_list = []

            # upset_positions = next(self.upset_positions)
            # self.roll, self.pitch = upset_positions[0], upset_positions[1]

            self.roll, self.pitch = next(self.upset_positions)
            self.tick_counter = 0
            self.cycle_counter += 1

    def draw_center_circle(self) -> None:
        pygame.draw.circle(
            self.screen,
            GameCnst.GREEN,
            self.window_center,
            5,
            3
        )

    def _draw_shutters(self, screen) -> None:

        shutter_radius = 24

        pygame.draw.rect(
            screen,
            GameCnst.BLACK,
            (0, 0, 736, 100),
            width=0)

        pygame.draw.rect(
            screen,
            GameCnst.SKYBLUE,
            (0, 0, GameCnst.WINDOW_WIDTH, GameCnst.SHUTTER_HEIGHT),
            width=0,
            border_top_left_radius=shutter_radius,
            border_top_right_radius=shutter_radius
        )

        pygame.draw.rect(
            screen,
            GameCnst.BLACK,
            (0, GameCnst.WINDOW_WIDTH, self.image_width - 30, 200),
            width=0
        )

        visible_height = GameCnst.WINDOW_HEIGHT - GameCnst.SHUTTER_HEIGHT

        pygame.draw.rect(
            screen,
            GameCnst.GROUNDBROWN,
            (0, visible_height, GameCnst.WINDOW_WIDTH, GameCnst.SHUTTER_HEIGHT),
            width=0,
            border_bottom_left_radius=shutter_radius,
            border_bottom_right_radius=shutter_radius
        )

    def _draw_inidicator(self, screen) -> None:
        rotated_roll_indicator = pygame.transform.rotate(
            self.roll_indicator_surface,
            self.roll
        )

        indicator_rotated_rect = rotated_roll_indicator.get_rect(
            center=self.window_center
        )
        for points in self.list_of_points:
            x, y = points
            pygame.draw.line(
                self.indicator_surface,
                GameCnst.WHITE,
                x,
                y,
                4
            )
        pygame.draw.polygon(
            self.indicator_surface, GameCnst.WHITE,
            points=self.flat_roll_pointer)
        pygame.draw.aalines(
            self.indicator_surface, GameCnst.WHITE, True,
            points=self.flat_roll_pointer)
        pygame.draw.polygon(
            self.roll_indicator_surface, GameCnst.WHITE,
            points=self.roll_pointer)
        pygame.draw.aalines(
            self.roll_indicator_surface, GameCnst.WHITE, True,
            points=self.roll_pointer)
        pygame.draw.lines(
            self.indicator_surface, GameCnst.WHITE, closed=False,
            points=self.crosshair_L_part,
            width=GameCnst.CROSSHAIR_THICKNESS)
        pygame.draw.lines(self.indicator_surface, GameCnst.WHITE, False,
                          self.crosshair_R_part,
                          GameCnst.CROSSHAIR_THICKNESS)
        screen.blit(self.indicator_surface, (0, 0))
        screen.blit(rotated_roll_indicator, indicator_rotated_rect)



def parse_constant(key: str, value) -> str:
    return f'{key}={value}'


def write_to_configuration(config_constancts: dict) -> None:
    home_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    configuration_path = f'{home_dir}{os.sep}configuration.txt'
    with open(configuration_path) as config:
        total_constants = '\n'.join(
            [parse_constant(*item) for item in config_constancts.items()]
        )
        config.write(total_constants)


if __name__ == '__main__':
    game = UpsetRecoveryWindow()
    game.run()

