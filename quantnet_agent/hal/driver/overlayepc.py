from quantnet_agent.hal.hwclasses import Filter
import logging
import socket

log = logging.getLogger(__name__)


class OverlayEPC(Filter):

    def __init__(self):
        log.info("Initializing EPC hardware")
        return 0

    def polarize(self, _):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("10.0.0.7", 5006))
        s.send(b"calibrate")
        result = s.recv(1024)
        if result == b"OK":
            return
        elif result == b"Not OK":
            raise Exception
        else:
            raise Exception

    def attenuate(self, strength):
        return super().attenuate(strength)
