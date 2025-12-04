from quantnet_mq.schema.models import calibration, Status as responseStatus
from quantnet_mq import Code
from quantnet_agent.hal.HAL import CMDInterpreter
import logging

log = logging.getLogger(__name__)


class Calibration(CMDInterpreter):

    def __init__(self, hal):
        super().__init__(hal)

    async def srcInit(self, request):
        log.info("Received calibration src init in test interpreter: %s", request.serialize())
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

    def get_commands(self):
        commands = {
            "calibration.srcInit": [self.srcInit, "quantnet_mq.schema.models.calibration.srcInit"]
            }
        return commands
