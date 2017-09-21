from metrics.chat.ChatConvNum import ChatConvNum
from metrics.chat.ChatConvNum import ChatMessageNum
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
import json
import time

with open("/etc/caret-metrics/config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

auth_provider = PlainTextAuthProvider(
        username=cfg['CASSANDRA_USERNAME'], password=cfg['CASSANDRA_PASSWORD'])
cluster = Cluster(cfg['CASSANDRA_HOSTS'], auth_provider=auth_provider)
session = cluster.connect()



mau = MonthlyActiveUsers(session)
dau = DailyActiveUsers(session)
queries = [DeviceData(session), PhoneNumberData(session), mau, dau, DailyMessages(session), MonthlyMessages(session), ChatConvNum(session)]

rv = {}

for query in queries:
    qclassname = query.__class__.__name__
    print '%s : %s - START' % (time.time(), qclassname)
    qres = query.run()
    print '%s : %s - END' % (time.time(), qclassname)
    rv[qclassname] = qres

with open('/tmp/metrics-result.json', 'w') as fp:
    json.dump(rv, fp, sort_keys=True, indent=4)
