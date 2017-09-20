from metrics.chat.ChatConvNum import ChatConvNum
from metrics.chat.DailyMessages import DailyMessages
from metrics.chat.MonthlyMessages import MonthlyMessages
from metrics.kamelefon.DeviceData import DeviceData
from metrics.kamelefon.PhoneNumberData import PhoneNumberData
from metrics.users.DailyActiveUsers import DailyActiveUsers
from metrics.users.MonthlyActiveUsers import MonthlyActiveUsers
from metrics.users.UserCountries import UserCountries

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

import yaml

with open("/etc/caret-metrics/config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

auth_provider = PlainTextAuthProvider(
        username=cfg['CASSANDRA_USERNAME'], password=cfg['CASSANDRA_PASSWORD'])
cluster = Cluster(cfg['CASSANDRA_HOSTS'], auth_provider=auth_provider)
session = cluster.connect()

mau = MonthlyActiveUsers(session)
dau = DailyActiveUsers(session)
userc = UserCountries(session)
queries = [mau, dau, DailyMessages(session), MonthlyMessages(session)]

for query in queries:
    print query.run()

print userc.run(mau.get_users())
