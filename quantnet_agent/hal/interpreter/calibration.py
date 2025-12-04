from quantnet_mq.schema.models import calibration, Status as responseStatus
from quantnet_mq import Code
from quantnet_agent.hal.HAL import CMDInterpreter
import logging

log = logging.getLogger(__name__)


class Calibration(CMDInterpreter):

    def __init__(self, hal):
        super().__init__(hal)

    async def srcInit(self, request):
        log.info("Received calibration src init: %s", request.serialize())
        if "lightsource" not in self.hal.devs:
            rc = 4
            return calibration.srcInitResponse(status=responseStatus(code=rc, value=Code(rc).name))
        else:
            res = self.hal.devs["lightsource"].status
            if res == 0:
                rc = 0
                return calibration.srcInitResponse(status=responseStatus(code=rc, value=Code(rc).name))
            else:
                rc = 6
                return calibration.srcInitResponse(status=responseStatus(code=rc, value=Code(rc).name))

    async def generate(self, request):
        log.info("Received calibration laser generation : %s", request.serialize())
        if "lightsource" not in self.hal.devs:
            rc = 4
            return calibration.srcInitResponse(status=responseStatus(code=rc, value=Code(rc).name))
        else:
            res = await self.hal.devs["lightsource"].generate(request.payload["cal_light"])
            if res == 0:
                rc = 0
                return calibration.generationResponse(status=responseStatus(code=rc, value=Code(rc).name))
            else:
                rc = 6
                return calibration.generationResponse(status=responseStatus(code=rc, value=Code(rc).name))

    async def cleanUp(self, request):
        log.info("Received calibration cleanup : %s", request.serialize())
        if "lightsource" not in self.hal.devs:
            rc = 4
            return calibration.cleanUpResponse(status=responseStatus(code=rc, value=Code(rc).name))
        else:
            res = await self.hal.devs["lightsource"].cleanUp()
            if res == 0:
                rc = 0
                return calibration.cleanUpResponse(status=responseStatus(code=rc, value=Code(rc).name))
            else:
                rc = 6
                return calibration.cleanUpResponse(status=responseStatus(code=rc, value=Code(rc).name))

    async def dstInit(self, request):
        log.info("Received calibration dst init: %s", request.serialize())
        if "epc" not in self.hal.devs:
            rc = 4
            return calibration.dstInitResponse(
                status=responseStatus(code=rc, value=Code(rc).name), reason="EPS not found"
            )
        elif "polarimeter" not in self.hal.devs:
            rc = 4
            return calibration.dstInitResponse(
                status=responseStatus(code=rc, value=Code(rc).name), reason="Polarimeter not found"
            )
        else:
            is_epc_init = self.hal.devs["epc"].status
            is_pm_init = self.hal.devs["polarimeter"].status
            status = is_epc_init + is_pm_init
            if status == 0:
                rc = 0
                return calibration.dstInitResponse(status=responseStatus(code=rc, value=Code(rc).name))
            else:
                rc = 6
                return calibration.dstInitResponse(status=responseStatus(code=rc, value=Code(rc).name))

    async def measure(self, request):
        log.info("Received calibration laser calibration : %s", request.serialize())
        if "polarimeter" not in self.hal.devs:
            rc = 4
            return calibration.calibrationResponse(status=responseStatus(code=rc, value=Code(rc).name))
        else:
            res = await self.hal.devs["polarimeter"].measure()
            if res == 0:
                rc = 0
                return calibration.calibrationResponse(status=responseStatus(code=rc, value=Code(rc).name))
            else:
                rc = 6
                return calibration.calibrationResponse(status=responseStatus(code=rc, value=Code(rc).name))

    def get_commands(self):
        commands = {
            "calibration.srcInit": [self.srcInit, "quantnet_mq.schema.models.calibration.srcInit"],
            "calibration.generation": [self.generate, "quantnet_mq.schema.models.calibration.generation"],
            "calibration.cleanUp": [self.cleanUp, "quantnet_mq.schema.models.calibration.cleanUp"],
            "calibration.dstInit": [self.dstInit, "quantnet_mq.schema.models.calibration.dstInit"],
            "calibration.calibration": [self.measure, "quantnet_mq.schema.models.calibration.calibration"]
            }
        return commands
