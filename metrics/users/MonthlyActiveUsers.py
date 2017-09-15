from ..base.QueryBase import QueryBase

import time

class MonthlyActiveUsers(QueryBase):

    def run(self):
        self.session.set_keyspace('ejabberd')
        self.mau_users = []
        timestamp = int(time.time())
        lasts = self.session.execute('select * from last')
        for last in lasts:
            if timestamp-int(last.seconds) <= 30*24*60*60:
                self.mau_users.append(int(last.username))
        return {"mau_users_count": len(self.mau_users)}

    def get_users(self):
        return self.mau_users
