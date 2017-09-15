from ..base.QueryBase import QueryBase

class DeviceData(QueryBase):

    def run(self):
        self.session.set_keyspace('kamelefon')
        devices = self.session.execute('select * from device')
        device_count = 0
        ios_count = 0
        android_count = 0
        for device in devices:
            device_count += 1
            if device.device_os.startswith('android'):
                android_count += 1
            if device.device_os.startswith('ios'):
                ios_count += 1
        return {"device_count": device_count, "android_count": android_count, "ios_count": ios_count}
