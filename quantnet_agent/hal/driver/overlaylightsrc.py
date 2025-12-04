from quantnet_agent.hal.hwclasses import LightSrc

import serial
import time
import socket
import asyncio

import logging

log = logging.getLogger(__name__)

polH = "S 4\n"
polD = "S 5\n"
polV = "S 6\n"
polA = "S 7\n"
polLCP = "S 2\n"
polRCP = "S 13\n"


class OverlayLightSrc(LightSrc):
    def __init__(self, *args, **kwargs):
        log.info("Initializing overlay LightSource")
        props = args[0]
        self.serial_dev = props['device']
        self.baud_rate = props['baud_rate']
        self.bsm_ip = props['bsm_ip']
        self.bsm_port = int(props['bsm_port'])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 5005))
        self.sock.setblocking(False)
        asyncio.create_task(self.serve())
        super().__init__(args, kwargs)

    def src_init(self, request):
        return 0

    async def serve(self):
        loop = asyncio.get_running_loop()
        self.dev_PSG, self.msg_device = self._connect()
        while True:
            log.info("Waiting for data")
            data = await loop.sock_recv(self.sock, 1024)
            log.info(data)
            msg_devflag, msg_write, msg_read, polset_error = self._polSET(data.decode())
            complete_msg = msg_devflag + "\n" + msg_write + "\n" + msg_read + "\n" + polset_error
            log.info(complete_msg)
            self.sock.sendto(complete_msg.encode(), (self.bsm_ip, self.bsm_port))

    async def generate(self, _):
        return 0

    def is_device_connected(self, port_name):
        try:
            ser = serial.Serial(port_name)
            ser.close()
            return True
        except serial.SerialException:
            return False

    def _connect(self):
        try:
            dev = serial.Serial(port=self.serial_dev, baudrate=self.baud_rate, timeout=0.1)
        except Exception as e:
            log.error(f"Could not connect to serial port {self.serial_dev}: {e}")
            return None, ""
        log.info(dev.name)
        msg_device = "####### PSG is connected ############# "
        log.info(msg_device)
        return dev, msg_device

    def _polSET(self, PSGpol):
        try:
            dev_connected_flag = self.is_device_connected(self.serial_dev)

            if dev_connected_flag:
                msg_devflag = "device connected flag:1, PSG is already connected"
                log.info(msg_devflag)
            else:
                msg_devflag = "device connected flag:0, PSG was not connected. Connecting now"
                log.info(msg_devflag)
                self.dev_PSG, self.msg_device = self._connect()

            try:
                self.dev_PSG.write(PSGpol.encode())
                msg_write = "Written: Ok"
                log.info(msg_write)
            except Exception as e:
                log.info(e)
                msg_write = "Write ISSUE"
                log.info(msg_write)

            time.sleep(1)
            try:
                self.dev_PSG.read(20)
                msg_read = "Read: Ok"
                log.info(msg_read)
            except Exception as e:
                log.info(e)
                msg_read = "Read Issue"
            polset_error = "Polset error None"
            log.info(polset_error)
        except Exception as e:
            polset_error = f"Polarization: Could NOT set: {e}"
            log.info(polset_error)

        return msg_devflag, msg_write, msg_read, polset_error

    def _disconnect(self, dev):
        try:
            msg_disconnect = "####### PSG is disconnected ############# "
            log.info(msg_disconnect)
            dev.close
        except Exception:
            msg_disconnect = "PSG: Could NOT disconnect"

        return msg_disconnect

    def wavelength(self, freq):
        pass

    def power(self, power):
        pass

    async def cleanUp(self):
        return 0
