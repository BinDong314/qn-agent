import logging
from quantnet_agent.hal.HAL import CoreInterpreter
from quantnet_mq.schema.models import scheduler, Status
from datetime import datetime, timezone, timedelta
from quantnet_agent.common.constants import Constants
from quantnet_mq import Code
from quantnet_mq.schema.models import Schedule

log = logging.getLogger(__name__)


class Scheduler(CoreInterpreter):

    def __init__(self, node):
        super().__init__(node)

    async def get_schedule(self, request):
        log.info(f"Received get_schedule request : {request.serialize()}")
        start_time = datetime.fromtimestamp(request.payload["startTime"]._value, timezone.utc)
        slot_size = timedelta(seconds=request.payload["slotSize"]._value)
        if slot_size != Constants.SLOTSIZE:
            scheduler.getScheduleResponse(
                status=Status(code=Code.INVALID_ARGUMENT.value, value=Code.INVALID_ARGUMENT.name),
                payload="Slot size does not match",
            )
        num_slots = request.payload["numSlots"]._value
        result = await self.node.scheduler.get_free_timeslot(start_time, num_slots)
        rc = result["code"]
        return scheduler.getScheduleResponse(
            status=Status(code=rc.value, value=rc.name), payload=Schedule(timeslots=result["value"])
        )

    def get_commands(self):
        commands = {"scheduler.getSchedule": [self.get_schedule, "quantnet_mq.schema.models.scheduler.getSchedule"]}
        return commands
