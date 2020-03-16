import requests
import json
from datetime import datetime, timedelta


class CovidApi(object):
    def __init__(self, url: str):
        self.url = url

    def get_countries(self) -> list:

        countries = {}
        r = requests.get(f"{self.url}/countries")
        if r.status_code == 200:
            raw_countries = json.loads(r.text)
            for raw_country_dict in raw_countries:
                countries[raw_country_dict.get("Slug")] = [raw_country_dict.get("Country"),raw_country_dict.get("Slug")]
                [countries[raw_country_dict.get("Slug")].append(province) for province in raw_country_dict.get("Provinces") if province != ""]
            return countries

        return {}

    def get_full_status_by_country(self, country: str):
        request_confirmed = requests.get(f"{self.url}/total/country/{country}/status/confirmed")
        request_deaths = requests.get(f"{self.url}/total/country/{country}/status/deaths")
        request_recovered = requests.get(f"{self.url}/total/country/{country}/status/recovered")
        yesterday = datetime.utcnow().date() - timedelta(days=1)
        if request_confirmed.status_code == 200 and request_deaths.status_code == 200 and request_recovered.status_code == 200:

            confirmed_value = json.loads(request_confirmed.text)[-1]["Cases"]
            deaths_value = json.loads(request_deaths.text)[-1]["Cases"]
            recovered_value = json.loads(request_recovered.text)[-1]["Cases"]
            print(f"{confirmed_value} {deaths_value} {recovered_value}")
            return f"*Confirmed cases:* {confirmed_value} \n *Recovered Patients:* {recovered_value}\n *Confirmed deaths:* {deaths_value}\n"
        else:
            print(request_confirmed.status_code)
            print(request_recovered.status_code)
            print(request_deaths.status_code)