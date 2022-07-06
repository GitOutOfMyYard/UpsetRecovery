from enum import Enum
from dotenv import dotenv_values
from os import path, sep
from json import loads
from typing import List, Tuple

WINDOW_SIZE = (400, 600)
SCREEN_CENTER = (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)


class Colour(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    SKYBLUE = (0, 204, 255)
    GROUNDBROWN = (153, 102, 51)



class DefaultGameCnst:
    WINDOW_SIZE = (700, 800)
    FPS = 60

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    SKYBLUE = (0, 204, 255)
    GROUNDBROWN = (153, 102, 51)

    TIME_TO_RECOVER = 6

    ROLL_POINTER_HEIGHT = 16
    ROLL_POINTER_WIDTH = 6
    ROLL_POINTER_TIP_ELEVATION = 128

    ROLL_INDICATOR_LINE_LENGTH = 8
    ROLL_INDICATOR_LINE_CLEARANCE = 128

    CROSSHAIR_WIDTH = 36
    CROSSHAIR_HEIGHT = 24
    CROSSHAIR_CLEARANCE = 8
    CROSSHAIR_THICKNESS = 3

    UPSET_POSITIONS = [
        (-40, 30), (35, 40), (40, -35), (55, 35),
        (-60, -30), (-150, -30), (-60, 40), (150, 20),
        (40, -30), (-35, -40), (-40, 35), (-55, -35),
        (60, 30), (150, 30), (60, -40), (-150, -20)
    ]

    CYCLE_NUMBER = len(UPSET_POSITIONS)
    EXPERIMENT_DURATION = 6
    INTERVAL = 3


APP_ROOT = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
USER_CONFIGS_PATH = path.join(APP_ROOT, 'configuration.txt')
CONFIG = dotenv_values(USER_CONFIGS_PATH)


def load_upset_positions(config) -> List[Tuple[float, float]]:
    return list(map(tuple, loads(config['UPSET_POSITIONS'])))


class GameCnst:
    WINDOW_WIDTH = int(CONFIG['WINDOW_WIDTH'])
    WINDOW_HEIGHT = int(CONFIG['WINDOW_HEIGHT'])

    WINDOW_SIZE = (
        int(CONFIG['WINDOW_WIDTH']),
        int(CONFIG['WINDOW_HEIGHT'])
    )
    FPS = 60

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    SKYBLUE = (0, 204, 255)
    GROUNDBROWN = (153, 102, 51)

    TIME_TO_RECOVER = int(CONFIG['TIME_TO_RECOVER'])

    ROLL_POINTER_HEIGHT = 16
    ROLL_POINTER_WIDTH = 6
    ROLL_POINTER_TIP_ELEVATION = 128

    ROLL_INDICATOR_LINE_LENGTH = 8
    ROLL_INDICATOR_LINE_CLEARANCE = 128

    CROSSHAIR_WIDTH = 36
    CROSSHAIR_HEIGHT = 24
    CROSSHAIR_CLEARANCE = 8
    CROSSHAIR_THICKNESS = 3

    UPSET_POSITIONS = load_upset_positions(CONFIG)

    CYCLE_NUMBER = len(UPSET_POSITIONS)
    EXPERIMENT_DURATION = int(CONFIG['EXPERIMENT_DURATION'])
    INTERVAL = int(CONFIG['INTERVAL'])
    SHUTTER_HEIGHT = 100

class Turbulence(Enum):
    SEVERANCE = float(CONFIG['TURBULENCE_SEVERANCE'])
    FLUCTUATIONS = float(CONFIG['TURBULENCE_FLUCTUATIONS'])


class Controller(Enum):
    X_COFF = 1
    Y_COFF = 1

