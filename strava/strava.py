import datetime
import json
import time
from pathlib import Path

import requests

from config import ATHLETE_STATS_URL, ATHLETE_URL, CLIENT_ID, CLIENT_SECRET, OAUTH_TOKEN_URL, STRAVA_REFRESH_TOKEN

METERS_TO_MILES = 0.00062


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


class Stats(StravaBase):
    def ytd_totals(self):
        _stats = {}
        day_of_year = datetime.datetime.now().timetuple().tm_yday
        stats = self.make_request(ATHLETE_STATS_URL)
        _stats['ytd_ride'] = round((stats['ytd_ride_totals']['distance']
                                    * METERS_TO_MILES), 2)
        _stats['ytd_run'] = round((stats['ytd_run_totals']['distance']
                                   * METERS_TO_MILES), 2)
        _stats['avg_run'] = round(_stats['ytd_run'] / day_of_year, 2)
        _stats['avg_ride'] = round(_stats['ytd_ride'] / day_of_year, 2)
        return _stats


class GearCheck(StravaBase):

    def list_gear(self):
        _stats = {'bikes': [],
                  'total_distance': 0
                  }
        info = self.make_request(ATHLETE_URL)
        stats = self.make_request(ATHLETE_STATS_URL)
        bikes = info['bikes']
        total = total_distance = stats['all_ride_totals']['distance']
        for bike in bikes:
            name = bike['name']
            if name == 'Poop Machine':
                continue
            _stats['bikes'].append({'name': name, 'distance': round(bike['distance'] * METERS_TO_MILES, 2)})
            total_distance -= bike['distance']

        _stats['bikes'].append({'name': 'Poop Machine', 'distance': round(total_distance * METERS_TO_MILES, 2)})
        _stats['total_distance'] = round(total * METERS_TO_MILES, 2)
        return _stats
