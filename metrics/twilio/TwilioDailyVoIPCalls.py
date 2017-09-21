from ..base.QueryBase import QueryBase

import datetime

class TwilioDailyCalls(QueryBase):

    timespan = 24*60*60

    def run(self):
        voip_call_count = 0
        voice_call_count = 0

        since = datetime.datetime.now()
        d = datetime.timedelta(secons=-timespan)
        since += d

        calls = sels.session.calls.list(start_time_after=since)
        for call in calls:
            if call.from_.startswith('client:'):
                voip_call_count += 1
            else:
                voice_call_count += 1

        return {"voip_call_count": voip_call_count, "voice_call_count": voice_call_count}
