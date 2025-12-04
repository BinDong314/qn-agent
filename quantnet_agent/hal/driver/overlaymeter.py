from quantnet_agent.hal.hwclasses import LightMeasurement
import logging
import socket
import asyncio


log = logging.getLogger(__name__)


class OverlayMeter(LightMeasurement):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log.info("Initializing LightMeter hardware")
        props = args[0]
        self.bsm_ip = props['bsm_ip']
        self.bsm_port = int(props['bsm_port'])
        self._send_message(self.bsm_ip, self.bsm_port, b'init')

    @property
    def status(self):
        return self._status

    @property
    def wavelength(self):
        pass

    @wavelength.setter
    def wavelength(self, freq):
        pass

    @property
    def power(self):
        pass

    def sweep(self):
        pass

    async def measure(self):
        await self._send_message_async(self.bsm_ip, self.bsm_port, b'calib')
        return 0

    async def cleanUp(self):
        await self._send_message_async(self.bsm_ip, self.bsm_port, b'cleanup')
        return 0

    async def _send_message_async(self, ip, port, msg):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._send_message, ip, port, msg)

    def _send_message(self, ip, port, msg):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.sendall(msg)
        result = s.recv(1024)
        if result != b'0':
            raise Exception(f"Failed to handle {msg}")
        s.close()
