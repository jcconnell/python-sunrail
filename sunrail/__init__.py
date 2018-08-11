"""Sunrail API."""

from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
import requests
import datetime


API_URL = 'http://sunrail.com/wp-admin/admin-ajax.php'
SUNRAIL_URL = 'https://sunrail.com'
ATTRIBUTION = 'Information provided by sunrail.com'
HTTP_POST = 'POST'
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
DATA = [('action', 'get_station_feed')]
STATIONS = {'17': "Debary",
            '2': "Sanford",
            '3': "Lake Mary",
            '15': "Longwood",
            '4': "Altamonte Springs",
            '16': "Maitland",
            '5': "Winter Park / Amtrak",
            '6': "Florida Hospital Health Village",
            '7': "Lynx Central",
            '14': "Church Street",
            '8': "Orlando Health / Amtrak",
            '9': "Sand Lake Road",
            '21': "Meadow Woods",
            '22': "Tupperware",
            '23': "Kissimmee / Amtrak",
            '24': "Poinciana"}
NORTHBOUND_TRAINS = ['P302', 'P304', 'P306', 'P308', 'P310', 'P312', 'P314',         # Morning
                     'P316', 'P318', 'P320', 'P322', 'P324',                         # Afternoon
                     'P326', 'P328', 'P330', 'P332', 'P334', 'P336', 'P338', 'P340'] # Evening

SOUTHBOUND_TRAINS = ['P301', 'P303', 'P305', 'P307', 'P309', 'P311', 'P313', 'P315', # Morning
                     'P317', 'P319', 'P321', 'P323',                                 # Afternoon
                     'P325', 'P327', 'P329', 'P331', 'P333', 'P335', 'P337', 'P339'] # Evening
ROUTES = NORTHBOUND_TRAINS + SOUTHBOUND_TRAINS

def _validate_stations(stations):
    """Validate station is a member of stations."""
    for station in stations:
        if station not in STATIONS:
            raise ValueError('Invalid station: {}'.format(station))
    return True

def _validate_train_ids(train_ids):
    """Validate train ID is a member of the route."""
    for train_id in train_ids:
        if train_id not in ROUTES:
            raise ValueError('Invalid train_id: {}'.format(train_id))
    return True


class SunRail():
    """SunRail API wrapper."""

    def __init__(self, include_stations=None, exclude_stations=None,
                 include_trains=None, exclude_trains=None):
        self.stations = set(STATIONS)
        self.trains = set(NORTHBOUND_TRAINS + SOUTHBOUND_TRAINS)
        if include_stations:
            _validate_stations(include_stations)
            self.stations = set(include_stations)
        if include_trains:
            _validate_train_ids(include_trains)
            self.trains = set(include_trains)
        if exclude_stations:
            _validate_stations(exclude_stations)
            self.stations -= set(exclude_stations)
        if exclude_trains:
            _validate_train_ids(exclude_trains)
            self.trains -= set(exclude_trains)

    def get_train_status(self):
        """Gets the train status."""
        resp = requests.post(API_URL, headers=HEADERS, data=DATA)
        northbound_status = []  # type: List[Dict[str, str]]
        southbound_status = []  # type: List[Dict[str, str]]
        resp.raise_for_status()
        data = resp.json()
        # data[0]['Directions'][0]['StopTimes'][0]['TrainId'] == 'P340'
        stations = [station for station in data if station['Id'] in self.stations]
        for station in data: # data[0...n]
            for direction in station['Directions']: # data[n].directions[N...S]
                if direction['Direction'] is 'N':
                    for time in direction['StopTimes']: # data[n].Directions[n].StopTimes[0...n]
                        if time['TrainId'] in self.trains:
                            northbound_status.append(time)
                else: # Direction is S
                    for time in direction['StopTimes']:
                        if time['TrainId'] in self.trains:
                            southbound_status.append(time)
        return trains #[northbound_status, southbound_status]
