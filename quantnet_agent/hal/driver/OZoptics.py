import serial
from quantnet_agent.hal.hwclasses import Filter
import logging

log = logging.getLogger(__name__)


class OZOptics(Filter):
    def __init__(self, config):
        self.ser = serial.Serial(
            port=config["port"],
            baudrate=config["baudrate"],
            timeout=1,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
        )

        log.info(f"Initialized OZOptics EPC with port={config['port']}")
        self.buflen = 2048

    @property
    def okay(self):
        return True if self.ser else False

    def __ask(self, cmd):
        if self.ser:
            self.ser.write(f"{cmd}\r\n".encode())
            return self.ser.read(self.buflen).decode()

    @property
    def help(self):
        return self.__ask("?")

    def _mode_ac(self):
        self.__ask("MAC")

    def _mode_dc(self):
        self.__ask("MDC")

    def dst_init(self, request):
        log.info("Initializing for Calibration")
        return 0

    def calibrate(self, request):
        log.info("Starting Calibration")
        return 0
