import json
import time
from pathlib import Path

import requests

from config import ATHLETE_STATS_URL, ATHLETE_URL, CLIENT_ID, CLIENT_SECRET, OAUTH_TOKEN_URL, STRAVA_REFRESH_TOKEN


class StravaBase(object):
    def __init__(self):
        self.cred_path = Path.home() / '.strava.json'
        if not self.cred_path.exists():
            with open(self.cred_path, 'w') as f:
                json.dump({'access_token': 0, 'expires_at': 0}, f)

        self.access_token = self._get_access_token()
        self.header = {'Authorization': f'Bearer {self.access_token}'}

    def _get_access_token(self):

        with open(self.cred_path, 'r') as f:
            creds = json.load(f)

        if creds['expires_at'] < time.time():
            response = requests.post(
                url=OAUTH_TOKEN_URL,
                data={
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'grant_type': 'refresh_token',
                    'refresh_token': STRAVA_REFRESH_TOKEN
                }
            )
            response.raise_for_status()
            strava_tokens = response.json()
            creds = {'access_token': strava_tokens['access_token'], 'expires_at': strava_tokens['expires_at']}
            with open(self.cred_path, 'w') as f:
                json.dump(creds, f)
        return creds['access_token']

    def make_request(self, url):
        resp = requests.get(url, headers=self.header)
        resp.raise_for_status()
        return resp.json()


class GearCheck(StravaBase):
    def list_gear(self):
        info = self.make_request(ATHLETE_URL)
        stats = self.make_request(ATHLETE_STATS_URL)
        bikes = info['bikes']
        total = total_distance = stats['all_ride_totals']['distance']
        for bike in bikes:
            name = bike['name']
            if name == 'Poop Machine':
                continue
            print(f"{name}:", f"{(bike['distance'] * .000621371192):.2f}")
            total_distance -= bike['distance']

        print(f"Poop Machine: {total_distance * .000621371192:.2f}")
        print(f"Total mileage: {total * .000621371192:.2f}")


if __name__ == '__main__':
    GearCheck().list_gear()
