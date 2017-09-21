from ..base.QueryBase import QueryBase

import time

class DailyActiveUsers(QueryBase):

    timespan = 24*60*60

    def run(self):
        self.session.set_keyspace('ejabberd')
        self.active_users = []
        timestamp = int(time.time())
        lasts = self.session.execute('select * from last')
        for last in lasts:
            if timestamp-int(last.seconds) <= self.timespan:
                self.active_users.append(int(last.username))
        return {"active_users_count": len(self.active_users)}

    def get_users(self):
        return self.active_users
