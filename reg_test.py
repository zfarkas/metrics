import requests
import uuid
import time
import datetime
import yaml

from twilio.rest import Client


with open("/etc/caret-metrics/config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

api_base = cfg['REST_API_BASE']

phone = cfg['REG_CHECK_NUMBER']
devid = uuid.uuid4()

def init_reg():
    init_dict = {
        'phoneNumber': phone,
        'registrationType': 'text',
        'isLandline': 0,
        'deviceType': 'RegChecker',
        'deviceOS': 'android',
        'deviceManufacturer': 'zfarkas',
        'deviceModel': 'RegChecker',
        'deviceUUID': str(devid)
    }
    init_req = requests.post(api_base + '/registration/initiate', json = init_dict)
    return init_req


def finalize_reg(reg_id, pin):
    finalize_dict = {
        'phoneNumber': phone,
        'pin': pin,
        'deviceUUID': str(devid)
    }
    finalize_req = requests.post(api_base + '/registration/verification/' + reg_id, json = finalize_dict)
    return finalize_req


def check_twilio_sms():
    account_sid = cfg['TWILIO_ACCOUNT_SID']
    auth_token = cfg['TWILIO_ACCOUNT_TOKEN']
    client = Client(account_sid, auth_token)

    for attempt in range(0, 4):
        records = client.messages.list(date_sent_after=datetime.datetime.utcnow()+datetime.timedelta(minutes=-1))
        for sms in records:
            if sms.to == phone and sms.status == 'sent':
                pin = sms.body.split()[-1]
                return pin
        time.sleep(2)

    return -1


def unmount(token):
    unmount_dict = {
        'token': token
    }
    unmount_req = requests.post(api_base + '/registration/unmount/' + phone[1:] + '/' + str(devid), json = unmount_dict)
    return unmount_req


init_resp = init_reg()
if init_resp.status_code != requests.codes.ok:
    print 'FAILURE: registration initialization failed (%s): %s' % (init_resp.status_code, init_resp.text)
    quit()
reg_id = init_resp.json()['id']

pin = check_twilio_sms()
if pin == -1:
    print 'FAILURE: could not query PIN code sent!'
    quit()

finalize_resp = finalize_reg(reg_id, pin)
if finalize_resp.status_code != requests.codes.ok:
    print 'FAILURE: registration finalization failed (%s): %s' % (finalize_resp.status_code, finalize_resp.text)
    quit()
token = finalize_resp.json()['token']

unmount_resp = unmount(token)
if unmount_resp.status_code != requests.codes.ok:
    print 'FAILURE: phone number unmount failed (%s): %s' % (unmount_resp.status_code, unmount_resp.text)
    quit()
print 'OK'
