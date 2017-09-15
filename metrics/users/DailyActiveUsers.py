from ..base.QueryBase import QueryBase

import time

class DailyActiveUsers(QueryBase):

    def run(self):
        self.session.set_keyspace('ejabberd')
        self.dau_users = []
        timestamp = int(time.time())
        lasts = self.session.execute('select * from last')
        for last in lasts:
            if timestamp-int(last.seconds) <= 24*60*60:
                self.dau_users.append(int(last.username))
        return {"dau_users_count": len(self.dau_users)}

    def get_users(self):
        return self.dau_users
