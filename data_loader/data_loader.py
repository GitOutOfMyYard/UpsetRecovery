import json
import os
from typing import Union, List, Dict, Tuple, Generator
from collections import namedtuple
import pandas
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from enum import Enum
from dataclasses import dataclass
from collections import defaultdict


cur_dir = os.path.abspath(os.path.dirname(__file__))
home_dir = os.path.dirname(cur_dir)
result_dir = home_dir + os.sep + 'results'


MeanValue = namedtuple('MeanValue', 'value length')


@dataclass
class TimingData:
    experiment_number: int
    successful_recovery: bool
    recovery_start: float
    recovery_end: float
    upside_down: bool
    nose_up: bool


class Sensivity(Enum):
    pitch = 0.07
    roll = 0.07


def is_movement_started(
        value: float,
        previous_value: float,
        movement_type: Sensivity
) -> bool:
    if all(
            (
                    abs(previous_value) <= movement_type.value,
                    abs(value) > movement_type.value
            )
    ):
        return True
    else:
        return False


FlightParameters = namedtuple(
    'FlightParameters',
    'joystick_roll joystick_pitch roll pitch'
)


class RecoveryEventParameters(FlightParameters):
    pass


class NeutralAttitude(Enum):
    roll = 5
    pitch = 5


class BlindZone(Enum):
    roll = 2
    pitch = 2


class SituationValues(Enum):
    Correct = 2
    PartiallyCorrect = 1
    Neutral = 0
    Wrong = -1


class RollCorrectnessRelations:
    def __init__(self):
        self.conformity = {
            RecoveryEventParameters(0, 0, 0, 0): 1,
            RecoveryEventParameters(1, 0, 0, 0): 0,
            RecoveryEventParameters(0, 1, 0, 0): 0,
            RecoveryEventParameters(-1, 0, 0, 0): 0,
            RecoveryEventParameters(0, -1, 0, 0): 0,
            RecoveryEventParameters(1, 1, 0, 0): 0,
            RecoveryEventParameters(-1, -1, 0, 0): 0,
            RecoveryEventParameters(1, -1, 0, 0): 0,
            RecoveryEventParameters(-1, 1, 0, 0): 0,

            RecoveryEventParameters(0, 0, 1, 0): 0,
            RecoveryEventParameters(1, 0, 1, 0): -1,
            RecoveryEventParameters(0, 1, 1, 0): 0,
            RecoveryEventParameters(-1, 0, 1, 0): 1,
            RecoveryEventParameters(0, -1, 1, 0): 0,
            RecoveryEventParameters(1, 1, 1, 0): -1,
            RecoveryEventParameters(-1, -1, 1, 0): 1,
            RecoveryEventParameters(1, -1, 1, 0): -1,
            RecoveryEventParameters(-1, 1, 1, 0): 1,

            RecoveryEventParameters(0, 0, -1, 0): 0,
            RecoveryEventParameters(1, 0, -1, 0): 1,
            RecoveryEventParameters(0, 1, -1, 0): 0,
            RecoveryEventParameters(-1, 0, -1, 0): -1,
            RecoveryEventParameters(0, -1, -1, 0): 0,
            RecoveryEventParameters(1, 1, -1, 0): 1,
            RecoveryEventParameters(-1, -1, -1, 0): -1,
            RecoveryEventParameters(1, -1, -1, 0): 1,
            RecoveryEventParameters(-1, 1, -1, 0): -1,

            RecoveryEventParameters(0, 0, 0, 1): -1,
            RecoveryEventParameters(1, 0, 0, 1): 1,
            RecoveryEventParameters(0, 1, 0, 1): -1,
            RecoveryEventParameters(-1, 0, 0, 1): 1,
            RecoveryEventParameters(0, -1, 0, 1): 0,
            RecoveryEventParameters(1, 1, 0, 1): 1,
            RecoveryEventParameters(-1, -1, 0, 1): 1,
            RecoveryEventParameters(1, -1, 0, 1): 1,
            RecoveryEventParameters(-1, 1, 0, 1): 1,

            RecoveryEventParameters(0, 0, 0, -1): 1,
            RecoveryEventParameters(1, 0, 0, -1): -1,
            RecoveryEventParameters(0, 1, 0, -1): 1,
            RecoveryEventParameters(-1, 0, 0, -1): -1,
            RecoveryEventParameters(0, -1, 0, -1): 0,
            RecoveryEventParameters(1, 1, 0, -1): -1,
            RecoveryEventParameters(-1, -1, 0, -1): -1,
            RecoveryEventParameters(1, -1, 0, -1): -1,
            RecoveryEventParameters(-1, 1, 0, -1): -1,

            RecoveryEventParameters(0, 0, 1, 1): 0,
            RecoveryEventParameters(1, 0, 1, 1): 1,
            RecoveryEventParameters(0, 1, 1, 1): -1,
            RecoveryEventParameters(-1, 0, 1, 1): -1,
            RecoveryEventParameters(0, -1, 1, 1): 1,
            RecoveryEventParameters(1, 1, 1, 1): 1,
            RecoveryEventParameters(-1, -1, 1, 1): -1,
            RecoveryEventParameters(1, -1, 1, 1): 1,
            RecoveryEventParameters(-1, 1, 1, 1): -1,

            RecoveryEventParameters(0, 0, -1, -1): 0,
            RecoveryEventParameters(1, 0, -1, -1): 1,
            RecoveryEventParameters(0, 1, -1, -1): -1,
            RecoveryEventParameters(-1, 0, -1, -1): -1,
            RecoveryEventParameters(0, -1, -1, -1): -1,
            RecoveryEventParameters(1, 1, -1, -1): 1,
            RecoveryEventParameters(-1, -1, -1, -1): -1,
            RecoveryEventParameters(1, -1, -1, -1): 1,
            RecoveryEventParameters(-1, 1, -1, -1): -1,

            RecoveryEventParameters(0, 0, 1, -1): 0,
            RecoveryEventParameters(1, 0, 1, -1): -1,
            RecoveryEventParameters(0, 1, 1, -1): -1,
            RecoveryEventParameters(-1, 0, 1, -1): 1,
            RecoveryEventParameters(0, -1, 1, -1): -1,
            RecoveryEventParameters(1, 1, 1, -1): -1,
            RecoveryEventParameters(-1, -1, 1, -1): 1,
            RecoveryEventParameters(1, -1, 1, -1): -1,
            RecoveryEventParameters(-1, 1, 1, -1): 1,

            RecoveryEventParameters(0, 0, -1, 1): 0,
            RecoveryEventParameters(1, 0, -1, 1): -1,
            RecoveryEventParameters(0, 1, -1, 1): -1,
            RecoveryEventParameters(-1, 0, -1, 1): 1,
            RecoveryEventParameters(0, -1, -1, 1): 1,
            RecoveryEventParameters(1, 1, -1, 1): -1,
            RecoveryEventParameters(-1, -1, -1, 1): 1,
            RecoveryEventParameters(1, -1, -1, 1): -1,
            RecoveryEventParameters(-1, 1, -1, 1): 1,

        }


class PitchCorrectness:
    def __init__(self):
        self.conformity = {
            RecoveryEventParameters(0, 0, 0, 0): 1,
            RecoveryEventParameters(1, 0, 0, 0): 0,
            RecoveryEventParameters(0, 1, 0, 0): 0,
            RecoveryEventParameters(-1, 0, 0, 0): 0,
            RecoveryEventParameters(0, -1, 0, 0): 0,
            RecoveryEventParameters(1, 1, 0, 0): 0,
            RecoveryEventParameters(-1, -1, 0, 0): 0,
            RecoveryEventParameters(1, -1, 0, 0): 0,
            RecoveryEventParameters(-1, 1, 0, 0): 0,

            RecoveryEventParameters(0, 0, 1, 0): 0,
            RecoveryEventParameters(1, 0, 1, 0): 0,
            RecoveryEventParameters(0, 1, 1, 0): 0,
            RecoveryEventParameters(-1, 0, 1, 0): 1,
            RecoveryEventParameters(0, -1, 1, 0): 0,
            RecoveryEventParameters(1, 1, 1, 0): 0,
            RecoveryEventParameters(-1, -1, 1, 0): 1,
            RecoveryEventParameters(1, -1, 1, 0): 0,
            RecoveryEventParameters(-1, 1, 1, 0): 1,

            RecoveryEventParameters(0, 0, -1, 0): 0,
            RecoveryEventParameters(1, 0, -1, 0): 1,
            RecoveryEventParameters(0, 1, -1, 0): 0,
            RecoveryEventParameters(-1, 0, -1, 0): 0,
            RecoveryEventParameters(0, -1, -1, 0): 0,
            RecoveryEventParameters(1, 1, -1, 0): 1,
            RecoveryEventParameters(-1, -1, -1, 0): 0,
            RecoveryEventParameters(1, -1, -1, 0): 1,
            RecoveryEventParameters(-1, 1, -1, 0): 0,

            RecoveryEventParameters(0, 0, 0, 1): 0,
            RecoveryEventParameters(1, 0, 0, 1): 1,
            RecoveryEventParameters(0, 1, 0, 1): -1,
            RecoveryEventParameters(-1, 0, 0, 1): 1,
            RecoveryEventParameters(0, -1, 0, 1): 1,
            RecoveryEventParameters(1, 1, 0, 1): -1,
            RecoveryEventParameters(-1, -1, 0, 1): 1,
            RecoveryEventParameters(1, -1, 0, 1): 1,
            RecoveryEventParameters(-1, 1, 0, 1): -1,

            RecoveryEventParameters(0, 0, 0, -1): 0,
            RecoveryEventParameters(1, 0, 0, -1): -1,
            RecoveryEventParameters(0, 1, 0, -1): 1,
            RecoveryEventParameters(-1, 0, 0, -1): -1,
            RecoveryEventParameters(0, -1, 0, -1): -1,
            RecoveryEventParameters(1, 1, 0, -1): 1,
            RecoveryEventParameters(-1, -1, 0, -1): -1,
            RecoveryEventParameters(1, -1, 0, -1): -1,
            RecoveryEventParameters(-1, 1, 0, -1): 1,

            RecoveryEventParameters(0, 0, 1, 1): 0,
            RecoveryEventParameters(1, 0, 1, 1): 1,
            RecoveryEventParameters(0, 1, 1, 1): -1,
            RecoveryEventParameters(-1, 0, 1, 1): -1,
            RecoveryEventParameters(0, -1, 1, 1): 1,
            RecoveryEventParameters(1, 1, 1, 1): -1,
            RecoveryEventParameters(-1, -1, 1, 1): 1,
            RecoveryEventParameters(1, -1, 1, 1): 1,
            RecoveryEventParameters(-1, 1, 1, 1): -1,

            RecoveryEventParameters(0, 0, -1, -1): 0,
            RecoveryEventParameters(1, 0, -1, -1): 1,
            RecoveryEventParameters(0, 1, -1, -1): -1,
            RecoveryEventParameters(-1, 0, -1, -1): 0,
            RecoveryEventParameters(0, -1, -1, -1): -1,
            RecoveryEventParameters(1, 1, -1, -1): 1,
            RecoveryEventParameters(-1, -1, -1, -1): -1,
            RecoveryEventParameters(1, -1, -1, -1): -1,
            RecoveryEventParameters(-1, 1, -1, -1): -1,

            RecoveryEventParameters(0, 0, 1, -1): 0,
            RecoveryEventParameters(1, 0, 1, -1): -1,
            RecoveryEventParameters(0, 1, 1, -1): -1,
            RecoveryEventParameters(-1, 0, 1, -1): 1,
            RecoveryEventParameters(0, -1, 1, -1): -1,
            RecoveryEventParameters(1, 1, 1, -1): -1,
            RecoveryEventParameters(-1, -1, 1, -1): -1,
            RecoveryEventParameters(1, -1, 1, -1): -1,
            RecoveryEventParameters(-1, 1, 1, -1): 1,

            RecoveryEventParameters(0, 0, -1, 1): 0,
            RecoveryEventParameters(1, 0, -1, 1): -1,
            RecoveryEventParameters(0, 1, -1, 1): -1,
            RecoveryEventParameters(-1, 0, -1, 1): 1,
            RecoveryEventParameters(0, -1, -1, 1): 1,
            RecoveryEventParameters(1, 1, -1, 1): -1,
            RecoveryEventParameters(-1, -1, -1, 1): 1,
            RecoveryEventParameters(1, -1, -1, 1): 1,
            RecoveryEventParameters(-1, 1, -1, 1): -1
        }


class EventValuesConformity:


    def __init__(self):
        self.conformity = {

            RecoveryEventParameters(0, 0, 0, 0): 2,
            RecoveryEventParameters(1, 0, 0, 0): -1,
            RecoveryEventParameters(0, 1, 0, 0): -1,
            RecoveryEventParameters(-1, 0, 0, 0): -1,
            RecoveryEventParameters(0, -1, 0, 0): -1,
            RecoveryEventParameters(1, 1, 0, 0): -1,
            RecoveryEventParameters(-1, -1, 0, 0): -1,
            RecoveryEventParameters(1, -1, 0, 0): -1,
            RecoveryEventParameters(-1, 1, 0, 0): -1,

            RecoveryEventParameters(0, 0, 2, 0): 0,
            RecoveryEventParameters(1, 0, 2, 0): -1,
            RecoveryEventParameters(0, 1, 2, 0): -1,
            RecoveryEventParameters(-1, 0, 2, 0): 2,
            RecoveryEventParameters(0, -1, 2, 0): -1,
            RecoveryEventParameters(1, 1, 2, 0): -1,
            RecoveryEventParameters(-1, -1, 2, 0): 1,
            RecoveryEventParameters(1, -1, 2, 0): -1,
            RecoveryEventParameters(-1, 1, 2, 0): 1,

            RecoveryEventParameters(0, 0, -2, 0): 0,
            RecoveryEventParameters(1, 0, -2, 0): 2,
            RecoveryEventParameters(0, 1, -2, 0): -1,
            RecoveryEventParameters(-1, 0, -2, 0): -1,
            RecoveryEventParameters(0, -1, -2, 0): -1,
            RecoveryEventParameters(1, 1, -2, 0): 1,
            RecoveryEventParameters(-1, -1, -2, 0): -1,
            RecoveryEventParameters(1, -1, -2, 0): 1,
            RecoveryEventParameters(-1, 1, -2, 0): -1,

            RecoveryEventParameters(0, 0, 0, 2): 0,
            RecoveryEventParameters(1, 0, 0, 2): -1,
            RecoveryEventParameters(0, 1, 0, 2): -1,
            RecoveryEventParameters(-1, 0, 0, 2): -1,
            RecoveryEventParameters(0, -1, 0, 2): 1,
            RecoveryEventParameters(1, 1, 0, 2): -1,
            RecoveryEventParameters(-1, -1, 0, 2): 2,
            RecoveryEventParameters(1, -1, 0, 2): 2,
            RecoveryEventParameters(-1, 1, 0, 2): -1,

            RecoveryEventParameters(0, 0, 0, -2): 0,
            RecoveryEventParameters(1, 0, 0, -2): -1,
            RecoveryEventParameters(0, 1, 0, -2): 2,
            RecoveryEventParameters(-1, 0, 0, -2): -1,
            RecoveryEventParameters(0, -1, 0, -2): -1,
            RecoveryEventParameters(1, 1, 0, -2): 1,
            RecoveryEventParameters(-1, -1, 0, -2): -1,
            RecoveryEventParameters(1, -1, 0, -2): -1,
            RecoveryEventParameters(-1, 1, 0, -2): 1,

            RecoveryEventParameters(0, 0, 2, 2): 0,
            RecoveryEventParameters(1, 0, 2, 2): 2,
            RecoveryEventParameters(0, 1, 2, 2): -1,
            RecoveryEventParameters(-1, 0, 2, 2): -1,
            RecoveryEventParameters(0, -1, 2, 2): 2,
            RecoveryEventParameters(1, 1, 2, 2): -1,
            RecoveryEventParameters(-1, -1, 2, 2): 1,
            RecoveryEventParameters(1, -1, 2, 2): 2,
            RecoveryEventParameters(-1, 1, 2, 2): -1,

            RecoveryEventParameters(0, 0, -2, -2): 0,
            RecoveryEventParameters(1, 0, -2, -2): 2,
            RecoveryEventParameters(0, 1, -2, -2): 1,
            RecoveryEventParameters(-1, 0, -2, -2): -1,
            RecoveryEventParameters(0, -1, -2, -2): -1,
            RecoveryEventParameters(1, 1, -2, -2): 1,
            RecoveryEventParameters(-1, -1, -2, -2): -1,
            RecoveryEventParameters(1, -1, -2, -2): -1,
            RecoveryEventParameters(-1, 1, -2, -2): -1,

            RecoveryEventParameters(0, 0, 2, -2): 0,
            RecoveryEventParameters(1, 0, 2, -2): -1,
            RecoveryEventParameters(0, 1, 2, -2): 1,
            RecoveryEventParameters(-1, 0, 2, -2): 2,
            RecoveryEventParameters(0, -1, 2, -2): -1,
            RecoveryEventParameters(1, 1, 2, -2): -1,
            RecoveryEventParameters(-1, -1, 2, -2): -1,
            RecoveryEventParameters(1, -1, 2, -2): -1,
            RecoveryEventParameters(-1, 1, 2, -2): 1,

            RecoveryEventParameters(0, 0, -2, 2): 0,
            RecoveryEventParameters(1, 0, -2, 2): -1,
            RecoveryEventParameters(0, 1, -2, 2): -1,
            RecoveryEventParameters(-1, 0, -2, 2): 2,
            RecoveryEventParameters(0, -1, -2, 2): 2,
            RecoveryEventParameters(1, 1, -2, 2): -1,
            RecoveryEventParameters(-1, -1, -2, 2): 2,
            RecoveryEventParameters(1, -1, -2, 2): 1,
            RecoveryEventParameters(-1, 1, -2, 2): -1,



            RecoveryEventParameters(0, 0, 1, 0): 0,
            RecoveryEventParameters(1, 0, 1, 0): -1,
            RecoveryEventParameters(0, 1, 1, 0): -1,
            RecoveryEventParameters(-1, 0, 1, 0): 2,
            RecoveryEventParameters(0, -1, 1, 0): -1,
            RecoveryEventParameters(1, 1, 1, 0): -1,
            RecoveryEventParameters(-1, -1, 1, 0): 1,
            RecoveryEventParameters(1, -1, 1, 0): -1,
            RecoveryEventParameters(-1, 1, 1, 0): 1,

            RecoveryEventParameters(0, 0, -1, 0): 0,
            RecoveryEventParameters(1, 0, -1, 0): 2,
            RecoveryEventParameters(0, 1, -1, 0): -1,
            RecoveryEventParameters(-1, 0, -1, 0): -1,
            RecoveryEventParameters(0, -1, -1, 0): -1,
            RecoveryEventParameters(1, 1, -1, 0): 1,
            RecoveryEventParameters(-1, -1, -1, 0): -1,
            RecoveryEventParameters(1, -1, -1, 0): 1,
            RecoveryEventParameters(-1, 1, -1, 0): -1,

            RecoveryEventParameters(0, 0, 0, 1): 0,
            RecoveryEventParameters(1, 0, 0, 1): -1,
            RecoveryEventParameters(0, 1, 0, 1): -1,
            RecoveryEventParameters(-1, 0, 0, 1): -1,
            RecoveryEventParameters(0, -1, 0, 1): 2,
            RecoveryEventParameters(1, 1, 0, 1): -1,
            RecoveryEventParameters(-1, -1, 0, 1): 1,
            RecoveryEventParameters(1, -1, 0, 1): 1,
            RecoveryEventParameters(-1, 1, 0, 1): -1,

            RecoveryEventParameters(0, 0, 0, -1): 0,
            RecoveryEventParameters(1, 0, 0, -1): -1,
            RecoveryEventParameters(0, 1, 0, -1): 2,
            RecoveryEventParameters(-1, 0, 0, -1): -1,
            RecoveryEventParameters(0, -1, 0, -1): -1,
            RecoveryEventParameters(1, 1, 0, -1): 1,
            RecoveryEventParameters(-1, -1, 0, -1): -1,
            RecoveryEventParameters(1, -1, 0, -1): -1,
            RecoveryEventParameters(-1, 1, 0, -1): 1,

            RecoveryEventParameters(0, 0, 1, 1): 0,
            RecoveryEventParameters(1, 0, 1, 1): -1,
            RecoveryEventParameters(0, 1, 1, 1): -1,
            RecoveryEventParameters(-1, 0, 1, 1): 1,
            RecoveryEventParameters(0, -1, 1, 1): 1,
            RecoveryEventParameters(1, 1, 1, 1): -1,
            RecoveryEventParameters(-1, -1, 1, 1): 2,
            RecoveryEventParameters(1, -1, 1, 1): 1,
            RecoveryEventParameters(-1, 1, 1, 1): -1,

            RecoveryEventParameters(0, 0, -1, -1): 0,
            RecoveryEventParameters(1, 0, -1, -1): 2,
            RecoveryEventParameters(0, 1, -1, -1): 1,
            RecoveryEventParameters(-1, 0, -1, -1): -1,
            RecoveryEventParameters(0, -1, -1, -1): -1,
            RecoveryEventParameters(1, 1, -1, -1): 2,
            RecoveryEventParameters(-1, -1, -1, -1): -1,
            RecoveryEventParameters(1, -1, -1, -1): -1,
            RecoveryEventParameters(-1, 1, -1, -1): -1,

            RecoveryEventParameters(0, 0, 1, -1): 0,
            RecoveryEventParameters(1, 0, 1, -1): -1,
            RecoveryEventParameters(0, 1, 1, -1): 1,
            RecoveryEventParameters(-1, 0, 1, -1): 2,
            RecoveryEventParameters(0, -1, 1, -1): -1,
            RecoveryEventParameters(1, 1, 1, -1): -1,
            RecoveryEventParameters(-1, -1, 1, -1): -1,
            RecoveryEventParameters(1, -1, 1, -1): -1,
            RecoveryEventParameters(-1, 1, 1, -1): 2,

            RecoveryEventParameters(0, 0, -1, 1): 0,
            RecoveryEventParameters(1, 0, -1, 1): 1,
            RecoveryEventParameters(0, 1, -1, 1): -1,
            RecoveryEventParameters(-1, 0, -1, 1): -1,
            RecoveryEventParameters(0, -1, -1, 1): 2,
            RecoveryEventParameters(1, 1, -1, 1): -1,
            RecoveryEventParameters(-1, -1, -1, 1): 1,
            RecoveryEventParameters(1, -1, -1, 1): 2,
            RecoveryEventParameters(-1, 1, -1, 1): -1,

            RecoveryEventParameters(0, 0, 2, 1): 0,
            RecoveryEventParameters(1, 0, 2, 1): -1,
            RecoveryEventParameters(0, 1, 2, 1): -1,
            RecoveryEventParameters(-1, 0, 2, 1): 2,
            RecoveryEventParameters(0, -1, 2, 1): 1,
            RecoveryEventParameters(1, 1, 2, 1): -1,
            RecoveryEventParameters(-1, -1, 2, 1): 2,
            RecoveryEventParameters(1, -1, 2, 1): -1,
            RecoveryEventParameters(-1, 1, 2, 1): -1,

            RecoveryEventParameters(0, 0, -2, -1): 0,
            RecoveryEventParameters(1, 0, -2, -1): 2,
            RecoveryEventParameters(0, 1, -2, -1): 1,
            RecoveryEventParameters(-1, 0, -2, -1): -1,
            RecoveryEventParameters(0, -1, -2, -1): -1,
            RecoveryEventParameters(1, 1, -2, -1): 2,
            RecoveryEventParameters(-1, -1, -2, -1): -1,
            RecoveryEventParameters(1, -1, -2, -1): -1,
            RecoveryEventParameters(-1, 1, -2, -1): -1,

            RecoveryEventParameters(0, 0, 2, -1): 0,
            RecoveryEventParameters(1, 0, 2, -1): -1,
            RecoveryEventParameters(0, 1, 2, -1): 1,
            RecoveryEventParameters(-1, 0, 2, -1): 2,
            RecoveryEventParameters(0, -1, 2, -1): -1,
            RecoveryEventParameters(1, 1, 2, -1): -1,
            RecoveryEventParameters(-1, -1, 2, -1): -1,
            RecoveryEventParameters(1, -1, 2, -1): -1,
            RecoveryEventParameters(-1, 1, 2, -1): 2,

            RecoveryEventParameters(0, 0, -2, 1): 0,
            RecoveryEventParameters(1, 0, -2, 1): 2,
            RecoveryEventParameters(0, 1, -2, 1): -1,
            RecoveryEventParameters(-1, 0, -2, 1): -1,
            RecoveryEventParameters(0, -1, -2, 1): 1,
            RecoveryEventParameters(1, 1, -2, 1): -1,
            RecoveryEventParameters(-1, -1, -2, 1): -1,
            RecoveryEventParameters(1, -1, -2, 1): 2,
            RecoveryEventParameters(-1, 1, -2, 1): -1,

            RecoveryEventParameters(0, 0, 1, 2): 0,
            RecoveryEventParameters(1, 0, 1, 2): 1,
            RecoveryEventParameters(0, 1, 1, 2): -1,
            RecoveryEventParameters(-1, 0, 1, 2): -1,
            RecoveryEventParameters(0, -1, 1, 2): 2,
            RecoveryEventParameters(1, 1, 1, 2): -1,
            RecoveryEventParameters(-1, -1, 1, 2): 1,
            RecoveryEventParameters(1, -1, 1, 2): 2,
            RecoveryEventParameters(-1, 1, 1, 2): -1,

            RecoveryEventParameters(0, 0, -1, -2): 0,
            RecoveryEventParameters(1, 0, -1, -2): 1,
            RecoveryEventParameters(0, 1, -1, -2): 2,
            RecoveryEventParameters(-1, 0, -1, -2): -1,
            RecoveryEventParameters(0, -1, -1, -2): -1,
            RecoveryEventParameters(1, 1, -1, -2): 2,
            RecoveryEventParameters(-1, -1, -1, -2): -1,
            RecoveryEventParameters(1, -1, -1, -2): -1,
            RecoveryEventParameters(-1, 1, -1, -2): -1,

            RecoveryEventParameters(0, 0, 1, -2): 0,
            RecoveryEventParameters(1, 0, 1, -2): -1,
            RecoveryEventParameters(0, 1, 1, -2): 1,
            RecoveryEventParameters(-1, 0, 1, -2): 2,
            RecoveryEventParameters(0, -1, 1, -2): -1,
            RecoveryEventParameters(1, 1, 1, -2): -1,
            RecoveryEventParameters(-1, -1, 1, -2): -1,
            RecoveryEventParameters(1, -1, 1, -2): -1,
            RecoveryEventParameters(-1, 1, 1, -2): 2,

            RecoveryEventParameters(0, 0, -1, 2): 0,
            RecoveryEventParameters(1, 0, -1, 2): -1,
            RecoveryEventParameters(0, 1, -1, 2): -1,
            RecoveryEventParameters(-1, 0, -1, 2): 1,
            RecoveryEventParameters(0, -1, -1, 2): 2,
            RecoveryEventParameters(1, 1, -1, 2): -1,
            RecoveryEventParameters(-1, -1, -1, 2): 2,
            RecoveryEventParameters(1, -1, -1, 2): 1,
            RecoveryEventParameters(-1, 1, -1, 2): -1

        }


ROLL_THRESHOLD = 10
PITCH_THRESHOLD = 10


class RecoveryActionsChecker:

    def __init__(self):
        self.reference = EventValuesConformity().conformity
        self.roll_reference = RollCorrectnessRelations().conformity
        self.pitch_reference = PitchCorrectness().conformity

    @staticmethod
    def _register_movement_event_parameter(
            parameter: float,
            blind_zone_type
    ) -> int:
        result = 0
        if abs(parameter) >= blind_zone_type.value:
            result = 1 if parameter > 0 else -1
        return result

    @staticmethod
    def register_attitude_parameter(parameter, threshold, blind_zone):
        result = 0
        if abs(parameter) >= blind_zone.value:
            result = 1 if parameter > 0 else -1
        if abs(parameter) >= threshold:
            result = 2 if parameter > 0 else -2
        return result

    @staticmethod
    def _is_attitude_neutral(roll, pitch) -> bool:
        return all(
            (
                abs(roll) <= NeutralAttitude.roll.value,
                abs(pitch) <= NeutralAttitude.pitch.value
            )
        )

    def _transform_parameters_into_movement_event(
            self,
            joystick_roll: float,
            joystick_pitch: float,
            roll: float,
            pitch: float
    ) -> RecoveryEventParameters:
        return RecoveryEventParameters(
            joystick_roll=self._register_movement_event_parameter(
                parameter=joystick_roll,
                blind_zone_type=Sensivity.roll
            ),
            joystick_pitch=self._register_movement_event_parameter(
                parameter=joystick_pitch,
                blind_zone_type=Sensivity.pitch
            ),
            roll=self.register_attitude_parameter(
                parameter=roll,
                threshold=ROLL_THRESHOLD,
                blind_zone=BlindZone.roll
            ),
            pitch=self.register_attitude_parameter(
                parameter=pitch,
                threshold=PITCH_THRESHOLD,
                blind_zone=BlindZone.pitch
            )
        )

    def check_correctness(
            self,
            joystick_roll: float,
            joystick_pitch: float,
            roll: float,
            pitch: float,
            reference
    ) -> float:
        event_state = self._transform_parameters_into_movement_event(
            joystick_roll=joystick_roll,
            joystick_pitch=joystick_pitch,
            roll=roll,
            pitch=pitch
        )
        return reference[event_state]

    def check_single_deflection_correctness(
            self,
            joystick_roll: float,
            joystick_pitch: float,
            roll: float,
            pitch: float
    ) -> float:
        event_state = self._transform_parameters_into_movement_event(
            joystick_roll=joystick_roll,
            joystick_pitch=joystick_pitch,
            roll=roll,
            pitch=pitch
        )
        return self.reference[event_state]

    def _check_roll_correctness_only(
            self,
            event_state: RecoveryEventParameters
    ) -> int:
        roll_correctness_methods_references = {
            -1: self._check_negative_pitch_roll_correctness,
            0: self._check_zero_pitch_roll_correctness,
            1: self._check_positive_pitch_roll_correctness
        }
        return roll_correctness_methods_references[int(event_state.pitch)](
            event_state
        )

    def _check_zero_pitch_roll_correctness(self, event_state) -> int:
        result = -1
        if event_state.joystick_roll == 0:
            result = 0
        elif event_state.roll == -event_state.joystick_roll:
            result = 1
        return result

    def _check_positive_pitch_roll_correctness(self, event_state) -> int:
        if event_state.joystick_roll == 0 and event_state.roll != 0:
            result = 1
        elif event_state.joystick_roll == 0 and event_state.roll == 0:
            result = -1
        elif event_state.roll == event_state.joystick_roll:
            result = 1
        elif event_state.roll == -event_state.joystick_roll:
            result = -1
        return result

    def _check_negative_pitch_roll_correctness(self, event_state) -> int:
        if event_state.joystick_roll == 0 and event_state.roll == 0:
            result = 1
        elif event_state.joystick_roll == 0 and event_state.roll != 0:
            result = -1
        elif event_state.roll == event_state.joystick_roll:
            result = -1
        elif event_state.roll == -event_state.joystick_roll:
            result = 1
        return result

def find_average_with_exceptions(values: list) -> tuple:
    summa = 0
    length = 0
    counts = []
    count = 0
    for value in values:
        count += 1
        if value is not None:
            summa += value
            length += 1
        else:
            counts.append(count)
    result = summa / length if length else None
    return result, length, counts


start_movement_list = []

start_movement_list_per_user = []

experiment_results = {}


def load_experiment_data(file_name='experiment_js'):
    with open(os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + os.sep + 'results' + os.sep + file_name) as f:
        data_list = []
        for line in f:
            data = json.loads(line)
            data_list.append(data)
            print(data_list)
    return data_list


def load_experiment_data_generator(file_name='experiment_js'):
    with open(
            os.path.dirname(os.path.abspath(os.path.dirname(__file__))
                            ) + os.sep + 'results' + os.sep + file_name) as f:
        return (json.loads(line) for line in f)


def make_dataframe(data_list):
    return pandas.DataFrame.from_records([(d,) for d in data_list],)



class ResultsAnalyser:

    def __init__(self):
        self.data = None
        self.chars_to_strip = (' ', '\n', '\t')
        self.output_path = ''
        self.user_path_name = ''
        self.analyser = RecoveryActionsChecker()
        self.timing_data = {}
        self.mean_values = defaultdict(lambda: defaultdict(list))

    def format_field_text(self, text: str) -> str:
        if text.startswith(self.chars_to_strip) or text.endswith(self.chars_to_strip):
            return self.format_field_text(text.strip())
        else:
            return text

    def build_user_patn_name(self, user_credentials: dict) -> str:
        last_name = self.format_field_text(user_credentials["last_name"])
        first_name = self.format_field_text(user_credentials["first_name"])
        return f"{last_name}_{first_name}"

    def make_path_name(self, user: dict):
        self.user_path_name = self.build_user_patn_name(user)
        self.output_path = result_dir + os.sep + self.user_path_name
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

    def analize_data(
            self,
            roll_list: list,
            pitch_list: list,
            joy_roll: list,
            joy_pitch: list,
            exp_num: int = 0,
            user: dict = {'last_name': "default", 'first_name': "user"}
    ):

        roll_correctness = []
        pitch_correctness = []
        complex_correctness = []
        total_events = []
        for params in zip(joy_roll, joy_pitch, roll_list, pitch_list):
            complex_correctness.append(
                self.analyser.check_correctness(
                    *params,
                    self.analyser.reference
                )
            )
            total_events.append(
                self.analyser._transform_parameters_into_movement_event(
                    *params
                )
            )
        self.make_plots_and_tables(
            joy_roll=joy_roll,
            joy_pitch=joy_pitch,
            roll_list=roll_list,
            pitch_list=pitch_list,
            complex_correctness=complex_correctness,
            roll_correctness_list=roll_correctness,
            pitch_correctness_list=pitch_correctness,
            exp_num=exp_num,
            total_events=total_events
        )
        self.calculate_timings(complex_correctness, roll_list, pitch_list, exp_num)

    def create_timing_file(self):
        path = self.output_path + os.sep + 'timings.txt'
        self.write_timing(path, 'Результаты\n', 'w')

    def calculate_timings(self, correctness: list[float], rolls: list[float], pitchs: list[float], exp_number: int):
        additional_roll_name = ''
        if self.starts_with_upside_roll(rolls):
            additional_roll_name = 'upside_roll'
        additional_roll_name = self.append_pitch_start_to_directory_name(
            additional_roll_name, float(pitchs[1]))
        path = self.output_path + os.sep + f'{additional_roll_name}timings.txt'

        succesfull_start = self.register_correct_defliction_trend(correctness)
        any_start = self.register_first_after_neutral_defliction_trend(correctness)
        start = any_start
        if not any_start:
            start = succesfull_start
        end = self.register_successful_recovery(rolls, pitchs, 15)

        self.timing_data[exp_number] = TimingData(
            experiment_number=exp_number,
            successful_recovery=bool(end),
            recovery_start=start,
            recovery_end=end,
            upside_down=abs(float(rolls[1])) > 90,
            nose_up=float(pitchs[1]) > 0
        )

        result_string = f'Попытка номер : {exp_number}' \
                        f'\nНачало вывода : ' \
                        f'{self.get_formatted_timing(start)}' \
                        f'\nУспешный вывод : ' \
                        f'{self.get_formatted_timing(end)}' \
                        f'\n'
        self.write_timing(path, result_string, 'a')

    @staticmethod
    def convert_click_to_seconds(click: int) -> float:
        return click / 60

    def get_formatted_timing(self, click: int) -> str:
        if click:
            return f'{self.convert_click_to_seconds(click)} сек.'
        return 'Нет корректного результата'

    def register_correct_defliction_trend(self, complex_correctness: List[float]) -> int:
        _, previous_value, *rest_of_values = complex_correctness
        for click, value in enumerate(rest_of_values):
            if value == 2 and previous_value != 2:
                return click
            previous_value = value

    def register_first_after_neutral_defliction_trend(self, complex_correctness: List[float]) -> int:
        neutral_position_counter = 0
        neutural_trigger_value = 5
        in_neutral_position = False
        _, previous_value, *rest_of_values = complex_correctness
        for click, value in enumerate(rest_of_values):
            if value == 0:
                neutral_position_counter += 1
            else:
                neutral_position_counter = 0

            if neutral_position_counter >= neutural_trigger_value:
                in_neutral_position = True

            if in_neutral_position and value != 0:
                return click




    @staticmethod
    def register_successful_recovery(
            rolls: float,
            pitchs: float,
            duration: int = 1
    ) -> int:
        recovered = 0
        _, *attitudes = zip(rolls, pitchs)
        for click, value in enumerate(attitudes):
            roll, pitch = value
            if RecoveryActionsChecker._is_attitude_neutral(roll, pitch):
                recovered += 1
                if recovered >= duration:
                    return click
            else:
                recovered = 0

    def write_timing(self, path: str, content: str, mode: str = 'a') -> None:
        with open(path, mode=mode, encoding='utf-8') as file:
            file.write(content)

    def make_plots_and_tables(
            self,
            joy_roll: list[float],
            joy_pitch: list[float],
            roll_list: list[float],
            pitch_list: list[float],
            complex_correctness: list[float],
            roll_correctness_list: list[float],
            pitch_correctness_list: list[float],
            exp_num: int,
            total_events
    ):

        additional_roll_name = ''
        if self.starts_with_upside_roll(roll_list):
            additional_roll_name = 'upside_roll'

        additional_roll_name = self.append_pitch_start_to_directory_name(
            additional_roll_name, float(pitch_list[1]))

        self.make_plot(
            colors=self._make_colorfull_tuples(complex_correctness),
            deflicktions=joy_roll,
            plot_name='roll_total_correctness',
            experiment_number=exp_num,
            separate_dir_name=f'{additional_roll_name}total_roll_plots'
        )
        self.make_plot(
            colors=self._make_colorfull_tuples(complex_correctness),
            deflicktions=joy_pitch,
            plot_name='pitch_total_correctness',
            experiment_number=exp_num,
            separate_dir_name=f'{additional_roll_name}total_pitch_plots'
        )


        self.make_attitude_plot(
            roll_list,
            pitch_list,
            'attitudes',
            exp_number=exp_num,
            separate_dir_name=f'{additional_roll_name}attitudes'
        )

        self.make_excel(
            correctness=complex_correctness,
            joy_roll=joy_roll,
            joy_pitch=joy_pitch,
            roll=roll_list,
            pitch=pitch_list,
            experiment_number=exp_num,
            total_events=total_events
        )

    def make_excel(
            self,
            correctness: list,
            roll: list,
            pitch: list,
            joy_roll: list,
            joy_pitch: list,
            experiment_number: int,
            total_events,
            file_name: str = ''
    ) -> None:
        joy_roll.insert(0, 'отклонение ручки по крену')
        joy_pitch.insert(0, 'отклонение ручки по тангажу')
        roll.insert(0, 'крен')
        pitch.insert(0, 'тангаж')
        total_events.insert(0, 'event_filters')
        correctness.insert(0, 'Правильность действий')
        dataframe = self.make_dataframe(
            joy_roll, joy_pitch, roll, pitch, correctness, total_events
        )
        if file_name:
            file_name = f'{file_name}_'

        additional_roll_name = ''
        if self.starts_with_upside_roll(roll):
            additional_roll_name = 'upside_roll'

        additional_roll_name = self.append_pitch_start_to_directory_name(additional_roll_name, float(pitch[1]))

        separate_dir_name = f'{additional_roll_name}excel_tables'
        self.make_dir_if_not_exist(separate_dir_name)
        dataframe.to_excel(
            self.output_path + os.sep + separate_dir_name + os.sep + file_name
            + f'{self.user_path_name}_experiment_{experiment_number}.xlsx'
        )

    def append_pitch_start_to_directory_name(
            self,
            name: str,
            pitch: float
    ) -> str:
        if pitch > 0:
            name = f'{name}{os.sep}nose_up{os.sep}'
        elif pitch < 0:
            name = f'{name}{os.sep}nose_down{os.sep}'
        return name

    def starts_with_upside_roll(self, roll_list: List[str]) -> bool:
        return abs(float(roll_list[1])) >= 95

    def make_dir_if_not_exist(self, dir_name: str):
        target_path = self.output_path + os.sep + dir_name
        if not os.path.exists(target_path):
            os.makedirs(target_path, exist_ok=True)

    def make_attitude_plot(
            self,
            rolls,
            pitchs,
            plot_name: str,
            exp_number: int,
            file_name: str = '',
            separate_dir_name: str = None
    ) -> None:
        if file_name:
            file_name = f'{file_name}_'
        plt.ylim((-180, 180))
        args = []
        ROLL_COLOR = 'b'
        PITCH_COLOR = 'r'

        for num, attitude in enumerate(zip(rolls, pitchs)):
            roll, pitch = attitude
            args.extend([num, roll, f'o{ROLL_COLOR}'])
            args.extend([num, pitch, f'o{PITCH_COLOR}'])

        plt.plot(*args, markeredgewidth=0.5)
        plt.grid()
        plt.ylabel(plot_name)
        final_path = self.generate_file_name(
            separate_dir_name=separate_dir_name,
            file_name=file_name,
            experiment_number=exp_number,
            plot_name=plot_name
        )
        plt.savefig(final_path)
        plt.clf()

    def make_plot(
            self,
            colors: list,
            deflicktions: list,
            plot_name: str,
            experiment_number: int,
            file_name: str = '',
            separate_dir_name: str = None
    ):
        if file_name:
            file_name = f'{file_name}_'
        dot_size = 8
        plt.ylim((-1.2, 1.2))
        plt.grid()
        args = []
        for num, deflick in enumerate(deflicktions):
            args.extend([num, deflick, f'o{next(colors)}'])
        try:
            plt.plot(*args, markeredgewidth=0.5)
        except Exception as e:
            a = 5
        plt.ylabel(plot_name)
        final_path = self.generate_file_name(
            separate_dir_name=separate_dir_name,
            file_name=file_name,
            experiment_number=experiment_number,
            plot_name=plot_name
        )
        plt.savefig(final_path)
        plt.clf()

    def generate_file_name(
            self,
            separate_dir_name: str,
            file_name: str,
            experiment_number: int,
            plot_name: str
    ) -> str:
        path = self.output_path
        if separate_dir_name:
            self.make_dir_if_not_exist(separate_dir_name)
            path = f'{path}{os.sep}{separate_dir_name}'
        plot_file_name = f'{file_name}_{self.user_path_name}'
        if experiment_number is not None:
            plot_file_name = f'{plot_file_name}_experiment_{experiment_number}'
        if plot_name is not None:
            plot_file_name = f'{plot_file_name}_plot_{plot_name}'
        return f'{path}{os.sep}{file_name}{plot_file_name}'

    def make_learning_plots(self, user: dict = {}):
        self.make_block_learning_plots()
        self.make_learning_plots_by_upset_type()

    def make_learning_plots_by_upset_type(self):
        data_by_type = {}
        for timing in self.timing_data.values():
            if not data_by_type.get((timing.upside_down, timing.nose_up)):
                data_by_type[(timing.upside_down, timing.nose_up)] = []
            data_by_type[(timing.upside_down, timing.nose_up)].append(self.get_timing_score_for_learning_plot(timing))

        for key in data_by_type.keys():
            plt.ylim((0, 210))
            plot_name = 'normal_'
            title = 'Нормальное положение '
            if key[0]:
                plot_name = 'upside_down_'
                title = 'Перевёрнутое положение '

            if key[1]:
                plot_name = f'{plot_name}nose_up'
                title = f'{title}на кабрирование'

            else:
                plot_name = f'{plot_name}nose_down'
                title = f'{title}на пикирование'



            plt.ylabel('Условные баллы')
            plt.title(title)
            plt.xlabel("Номер повторения")
            plt.plot(range(1, len(data_by_type[key]) + 1), data_by_type[key], markeredgewidth=2)

            plt.xticks(ticks=list(range(1, len(data_by_type[key]) + 1)),
                       labels=list(range(1, len(data_by_type[key]) + 1)))

            plt.grid()

            final_path = self.generate_file_name(
                separate_dir_name='learning_by_type',
                file_name=plot_name,
                experiment_number=None,
                plot_name=None
            )
            plt.savefig(final_path)
            plt.clf()


    def get_timing_score_for_learning_plot(self, timing_data: TimingData) -> float:
        result = 0
        if timing_data.recovery_end:
            result = 360 - timing_data.recovery_end
        return result

    def make_block_learning_plots(self):
        plt.ylim((0, 5))
        args = []
        datas = []
        for number in self.timing_data.keys():
            if number % 4 == 0:
                datas.append(self.timing_data[number])
                recovered_times = len([timer_data.successful_recovery for timer_data in datas if timer_data.successful_recovery])
                args.append(recovered_times)
                datas.clear()
            else:
                datas.append(self.timing_data[number])
        plt.plot(range(1, len(args) + 1), args, markeredgewidth=2)
        plt.xticks(ticks=list(range(1, len(args) + 1)), labels=list(range(1, len(args) + 1)))
        plt.grid()
        plt.title('Научаемость по блокам')
        plt.ylabel('Кол-во успешных выводов')
        plt.xlabel('Номер блока')
        final_path = self.generate_file_name(
            separate_dir_name='learning_blocks',
            file_name='learning_blocks_plot',
            experiment_number=None,
            plot_name=None
        )
        plt.savefig(final_path)
        plt.clf()

    def write_medium_timigs(self):
        start_nose_up, end_nose_up, start_nose_down, end_nose_down = self.get_mean_timings_nose_up_down(False)

        upside_start_nose_up, upside_end_nose_up, upside_start_nose_down, upside_end_nose_down = self.get_mean_timings_nose_up_down(True)

        self.append_medium_timing(start_nose_up, end_nose_up, start_nose_down, end_nose_down, False)
        self.append_medium_timing(upside_start_nose_up, upside_end_nose_up, upside_start_nose_down, upside_end_nose_down, True)

        path = self.output_path + os.sep + f'mean_timings.txt'
        result_string = f'среднее начало нос вверх -  {start_nose_up.value} количество учтённых попыткок {start_nose_up.length}' \
                        f'\nсреднее конец нос вверх -  {end_nose_up.value} количество учтённых попыткок {end_nose_up.length}' \
                        f'\nсреднее начало нос вниз -  {start_nose_down.value} количество учтённых попыткок {start_nose_down.length}' \
                        f'\nсреднее конец нос вниз -  {end_nose_down.value} количество учтённых попыткок {end_nose_down.length}' \
                        f'\nПеревёрнутые' \
                        f'\nсреднее начало нос вверх -  {upside_start_nose_up.value} количество учтённых попыткок {upside_start_nose_up.length}' \
                        f'\nсреднее конец нос вверх -  {upside_end_nose_up.value} количество учтённых попыткок {upside_end_nose_up.length}' \
                        f'\nсреднее начало нос вниз -  {upside_start_nose_down.value} количество учтённых попыткок {upside_start_nose_down.length}' \
                        f'\nсреднее конец нос вниз -  {upside_end_nose_down.value} количество учтённых попыткок {upside_end_nose_down.length}'

        self.write_timing(path, result_string, 'w')


    def append_medium_timing(
            self,
            start_nose_up: MeanValue,
            end_nose_up: MeanValue,
            start_nose_down: MeanValue,
            end_nose_down: MeanValue,
            is_bottom_up: bool
    ) -> None:

        self.mean_values[is_bottom_up]['start_nose_up'].append(start_nose_up)
        self.mean_values[is_bottom_up]['end_nose_up'].append(end_nose_up)
        self.mean_values[is_bottom_up]['start_nose_down'].append(start_nose_down)
        self.mean_values[is_bottom_up]['end_nose_down'].append(end_nose_down)


    def get_mean_timings_nose_up_down(self, is_bottom_up: bool
                                      ) -> Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
        start_nose_up = self.get_mean_and_number(
            self.collect_one_typed_timing('recovery_start', is_bottom_up, True)
        )
        end_nose_up = self.get_mean_and_number(
            self.collect_one_typed_timing('recovery_end', is_bottom_up, True)
        )

        start_nose_down = self.get_mean_and_number(
            self.collect_one_typed_timing('recovery_start', is_bottom_up, False)
        )
        end_nose_down = self.get_mean_and_number(
            self.collect_one_typed_timing('recovery_end', is_bottom_up, False)
        )
        return start_nose_up, end_nose_up, start_nose_down, end_nose_down


    def get_mean_and_number(self, array: List[float]) -> MeanValue:
        prepared_array = [value for value in array if value is not None]
        mean = self.get_mean(prepared_array) if prepared_array else 0
        return MeanValue(mean, len(prepared_array))

    def get_mean(self, array: List[float]):
        return (sum(array) / len(array)) / 60

    def collect_one_typed_timing(
            self,
            timing_type: str,
            is_bottom_up: bool,
            is_nose_up: bool
    ) -> List[float]:
        result = []
        for timing in self.timing_data.values():
            if timing.nose_up == is_nose_up and timing.upside_down == is_bottom_up:
                result.append(getattr(timing, timing_type))
        return result


    def _make_colorfull_tuples(
            self,
            correctness: list
    ) -> Generator:
        colours_referense = {-1: 'r', 0: 'b', 1: 'y', 2: 'g'}
        return (colours_referense[num] for num in correctness)

    @staticmethod
    def _make_three_colored_tuples(
            correctness: list
    ) -> Generator:
        colours_referense = {-1: 'r', 0: 'y', 1: 'g'}
        return (colours_referense[num] for num in correctness)

    @staticmethod
    def make_dataframe(*columns: list) -> pandas.DataFrame:
        return pandas.DataFrame.from_records([data for data in zip(*columns)])

    def read_data(self):
        self.data = self.load_experiment_data()

    @staticmethod
    def load_experiment_data(file_name='experiment_js'):
        with open(os.path.dirname(os.path.abspath(os.path.dirname(
                __file__))) + os.sep + 'results' + os.sep + file_name) as f:
            data_list = []
            for line in f:
                data = json.loads(line)
                data_list.append(data)
        return data_list

    def process_all_data(self):
        self.read_data()

        for chunk in self.data:
            user = chunk['user']
            conditions = chunk['experiment_conditions']
            results = chunk['experiment_results']
            print(user)
            print('Data processing')
            roll_delay_by_user = []
            pitch_delay_by_user = []
            self.make_path_name(user)
            self.create_timing_file()

            self.timing_data.clear()

            try:
                for k, v in results.items():
                    experiment_number = int(k)
                    roll_list = v['roll_list']
                    pitch_list = v['pitch_list']
                    joy_roll = v['joy_roll']
                    joy_pitch = v['joy_pitch']
                    roll_delay_by_user.append(
                        fetch_delay_by_experiment(joy_roll, Sensivity.roll)
                    )
                    pitch_delay_by_user.append(
                        fetch_delay_by_experiment(joy_pitch, Sensivity.pitch)
                    )
                    self.analize_data(roll_list, pitch_list, joy_roll, joy_pitch,
                                      experiment_number, user)
            except Exception as e:
                print(f'exception {e} during handling {chunk["user"]}  ')
                continue

            self.make_learning_plots(user)
            self.write_medium_timigs()

        self.make_medium_value_excel()


    def make_medium_value_excel(self) -> None:

        data = [('start_nose_up', 'end_nose_up', 'start_nose_down', 'end_nose_down'),
            *zip(
                self.mean_values[False]['start_nose_up'],
                self.mean_values[False]['end_nose_up'],
                self.mean_values[False]['start_nose_down'],
                self.mean_values[False]['end_nose_down']
            )]

        data = self.unpack_mean_values()

        dataframe = pandas.DataFrame.from_records(data)

        dataframe.to_excel(
            os.path.dirname(self.output_path) + os.sep + 'mean_values.xlsx'
        )

    def unpack_mean_values(self) -> List[float]:

        data = []
        data_dict = defaultdict(list)
        for parameter in ('start_nose_up', 'end_nose_up', 'start_nose_down', 'end_nose_down'):
            for row_number, unpacked_row in enumerate(self.unpack_single_mean_values(False, parameter)):
                data_dict[row_number].extend(unpacked_row)
        first_row = ('start_nose_up' ,'length' , 'end_nose_up','length'  'start_nose_down','length' , 'end_nose_down','length' )
        return [first_row , *list(data_dict.values())]


    def unpack_single_mean_values(self, is_bottom_up: bool, parameter: str):
        rows = []
        for value in self.mean_values[is_bottom_up][parameter]:
            rows.append([value.value, value.length])
        return rows



count_duration = 1 / 60


def fetch_delay_by_experiment(deviations: list, movement_type: Sensivity) -> float:
    previous_deviation, *other_deviations = deviations
    counter = 0
    for deviation in other_deviations:
        counter += 1
        if is_movement_started(previous_deviation, deviation, movement_type):
            return count_duration * counter


results_analyser = ResultsAnalyser()


results_analyser.process_all_data()
