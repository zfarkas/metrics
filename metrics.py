from metrics.chat.ChatConvNum import ChatConvNum
from metrics.chat.ChatMessageNum import ChatMessageNum
from metrics.chat.DailyMessages import DailyMessages
from metrics.chat.MonthlyMessages import MonthlyMessages
from metrics.kamelefon.DeviceData import DeviceData
from metrics.kamelefon.PhoneNumberData import PhoneNumberData
from metrics.users.DailyActiveUsers import DailyActiveUsers
from metrics.users.MonthlyActiveUsers import MonthlyActiveUsers
from metrics.users.UserCountries import UserCountries
from metrics.twilio.TwilioDailyCalls import TwilioDailyCalls
from metrics.twilio.TwilioMonthlyCalls import TwilioMonthlyCalls
from metrics.twilio.TwilioDailySMS import TwilioDailySMS
from metrics.twilio.TwilioMonthlySMS import TwilioMonthlySMS

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from twilio.rest import Client

import yaml
import json
import time

with open("/etc/caret-metrics/config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

auth_provider = PlainTextAuthProvider(
        username=cfg['CASSANDRA_USERNAME'], password=cfg['CASSANDRA_PASSWORD'])
cluster = Cluster(cfg['CASSANDRA_HOSTS'], auth_provider=auth_provider)
session = cluster.connect()

twilio_session = Client(cfg['TWILIO_ACCOUNT_SID'], cfg['TWILIO_ACCOUNT_TOKEN'])

mau = MonthlyActiveUsers(session)
dau = DailyActiveUsers(session)
queries = [
    TwilioDailyCalls(twilio_session), TwilioMonthlyCalls(twilio_session),
    TwilioDailySMS(twilio_session), TwilioMonthlySMS(twilio_session),
    ChatMessageNum(session), DailyMessages(session), MonthlyMessages(session), ChatConvNum(session),
    DeviceData(session), PhoneNumberData(session),
    mau, dau]

rv = {}

for query in queries:
    qclassname = query.__class__.__name__
    print '%s : %s - START' % (time.time(), qclassname)
    qres = query.run()
    print '%s : %s - END' % (time.time(), qclassname)
    rv[qclassname] = qres

with open('/tmp/metrics-result.json', 'w') as fp:
    json.dump(rv, fp, sort_keys=True, indent=4)
