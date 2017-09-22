from ..base.QueryBase import QueryBase

import datetime

class TwilioDailySMS(QueryBase):

    timespan = 24*60*60

    def run(self):
        total_sms_count = 0
        unique_numbers = set()

        since = datetime.datetime.now()
        d = datetime.timedelta(seconds=-self.timespan)
        since += d

        messages = self.session.messages.list(date_sent_after=since)
        for msg in messages:
            total_sms_count += 1
            unique_numbers.add(msg.to)

        return {"total_sms_count": total_sms_count, "unique_sms_numbers_count": len(unique_numbers)}
