from quantnet_agent.hal.HAL import LocalTaskInterpreter
import logging

log = logging.getLogger(__name__)


class Cavity_Calibration(LocalTaskInterpreter):

    def __init__(self, hal):
        super().__init__(hal)

    def run(self, *arg, **kwargs):
        log.debug("Running Cavity calibration")

    def stop(self):
        log.info("Stopping dumy local task")
