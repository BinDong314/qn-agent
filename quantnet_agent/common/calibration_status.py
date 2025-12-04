from enum import Enum


class Calibration_status(Enum):
    FULL = "Full_scale_calibration"
    LIGHT = "Lightweight_calibration"
    CHECK = "Status_check"
