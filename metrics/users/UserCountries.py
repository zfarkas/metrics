from ..base.QueryBase import QueryBase

import time
import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_country_code
from phonenumbers.phonenumberutil import region_code_for_number
import pycountry

class UserCountries(QueryBase):

    def run(self, users):
        self.country_count = {}
        for user in users:
            pn = phonenumbers.parse('+' + str(user))
            country = pycountry.countries.get(alpha_2=region_code_for_number(pn)).name
            if country not in self.country_count:
                self.country_count[country] = 0
            self.country_count[country] += 1
        return {"user_counties_count": len(self.country_count)}

    def get_county_count(self):
        return self.country_count
