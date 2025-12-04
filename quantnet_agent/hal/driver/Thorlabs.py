from ThorlabsPM100 import ThorlabsPM100, USBTMC
import numpy as np
from quantnet_agent.hal.hwclasses import LightMeasurement
import logging

log = logging.getLogger(__name__)


class PM100D(LightMeasurement):
    def __init__(self, config):
        inst = USBTMC(device=config["device"])
        self.dev = ThorlabsPM100(inst=inst)
        self.pd_bandwidth = self.dev.input.pdiode.filter.lpass.state
        self.avg_count = self.dev.sense.average.count
        log.info(f"Initialized PM100D with bw={self.pd_bandwidth} avr={self.avg_count} wavelength={self.wavelength}")
        log.info(f"Configuration: {self.getconfigure}")

    @property
    def read(self):
        return self.dev.read

    @property
    def wavelength(self):
        return self.dev.sense.correction.wavelength

    @property
    def power(self, count=10):
        request = type('', (), {})()
        request.count = count
        self.measure(request)

    @property
    def getconfigure(self):
        return self.dev.getconfigure

    def measure(self, request):
        log.info(f"Reading: {request.count} measurements")
        power = np.array([self.dev.read for _ in range(request.count)])
        return power
