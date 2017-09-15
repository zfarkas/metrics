from ..base.QueryBase import QueryBase

class PhoneNumberData(QueryBase):

    def run(self):
        self.session.set_keyspace('kamelefon')
        phone_numbers = self.session.execute('select * from phone_number')
        business_count = 0
        public_count = 0
        landline_count = 0
        phone_count = 0
        for pnum in phone_numbers:
            phone_count += 1
            if pnum.is_business:
                business_count += 1
            if pnum.is_public:
                public_count += 1
            if pnum.islandline:
                landline_count += 1
        return {"phone_numbers": phone_count, "business_count": business_count, "public_count": public_count, "landline_count": landline_count}
