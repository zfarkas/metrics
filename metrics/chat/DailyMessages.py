from ..base.QueryBase import QueryBase

import time

class DailyMessages(QueryBase):

    timespan = 24*60*60

    def run(self):
        self.session.set_keyspace('ejabberd')
        self.msg_ids = set()
        timestamp = int(time.time())
        msg_tss = self.session.execute('SELECT msg_id, timestamp from caret_message_timestamps')
        print 'Timespan: %s' % self.timespan
        for msg_ts in msg_tss:
            if msg_ts.timestamp is not None:
                if msg_ts.timestamp.year < 1900:
                    continue
                ts = int(msg_ts.timestamp.strftime('%s'))
                if timestamp-ts <= self.timespan:
                    self.msg_ids.add(msg_ts.msg_id)

        self.msg_senders = set()
        stmt = self.session.prepare('SELECT from_jid from caret_messages where msg_id=?')
        for msg_id in self.msg_ids:
            rows = self.session.execute(stmt, [msg_id])
            for r in rows:
                self.msg_senders.add(r.from_jid)

        return {"msg_count": len(self.msg_ids), "msg_senders_count": len(self.msg_senders)}

    def get_msg_ids(self):
        return self.msg_ids

    def get_msg_senders(self):
        return self.msg_senders
