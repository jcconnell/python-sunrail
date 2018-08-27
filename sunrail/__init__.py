"""Sunrail API."""

from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
import requests
import datetime


SUNRAIL_URL = 'http://sunrail.com'
STATUS_URL = '{}/wp-admin/admin-ajax.php'.format(SUNRAIL_URL)
TOKEN_URL = '{}/api/tokenizer/get_token/'.format(SUNRAIL_URL)
ALERT_URL = '{}/api/alerts/get_alerts/'.format(SUNRAIL_URL)
ATTRIBUTION = 'Information provided by sunrail.com'
HTTP_POST = 'POST'
#HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
HEADERS = {'User-Agent':'Sunrail Python API Wrapper'}
DATA = [('action', 'get_station_feed')]
DIRECTIONS = ['N', 'S']
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

def _validate_direction(direction):
    """Validate direction is N or S."""
    if direction not in DIRECTIONS:
        raise ValueError("Invalid Direction: Only 'N' or 'S'.")
    return True


class SunRail():
    """SunRail API wrapper."""

    def __init__(self, include_stations=None, exclude_stations=None,
                 include_trains=None, exclude_trains=None, direction=None):
        self.stations = set(STATIONS)
        self.trains = set(NORTHBOUND_TRAINS + SOUTHBOUND_TRAINS)
        self.direction = ['N', 'S']
        # data[0]['Directions'][0]['StopTimes'][0]['TrainId'] == 'P340'
        self.data = None
        self.delays = []
        self.alerts = []
        if direction:
            _validate_direction(direction)
            self.direction = [direction]
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

    def update(self):
        """Updates the train data."""
        status = requests.post(STATUS_URL, headers=HEADERS,
                               data=DATA, timeout=10)
        status.raise_for_status()
        self.data = status.json()

        request_token = requests.get(TOKEN_URL, headers=HEADERS,
                                     timeout=10)
        request_token.raise_for_status()
        token = request_token.json()['result']['token']

        alert_params = {'token':token}
        request_alerts = requests.get(ALERT_URL, headers=HEADERS,
                                      params=alert_params, timeout=10)
        request_alerts.raise_for_status()
        if 'result' in request_alerts.json():
            self.alerts = request_alerts.json()['result']
        self.alerts = []

    def get_delays(self):
        """Return any delays for trains we're interested in."""
        if len(self.delays) == 0:
            return None
        return self.delays

    def get_alerts(self):
        """Return any alerts for trains we're interested in."""
        if len(self.alerts) == 0:
            return None
        for train in self.trains:
            if train in self.alerts:
                return self.alerts
        return None

    def get_all(self):
        """Gets the train status."""
        northbound_status = []
        southbound_status = []
        if self.data is None:
            return None
        data = self.data
        for station in data:
            if station['Id'] in self.stations:
                for direction in station['Directions']:
                    if (direction['Direction'] is 'N' and
                        direction['Direction'] in self.direction):
                        for time in direction['StopTimes']:
                            if time['TrainId'] in self.trains:
                                data = {'station':station['Name'],
                                     'station_lat':station['Lat'],
                                     'station_lon':station['Lon'],
                                     'train_id':time['TrainId'],
                                     'arrival_time':time['ArrivalTime'],
                                     'delayed':time['DelayFlag']}
                                northbound_status.append(data)
                                if time['DelayFlag'] == True:
                                    self.delays.append(data)

                    elif direction['Direction'] in self.direction:
                        for time in direction['StopTimes']:
                            if time['TrainId'] in self.trains:
                                data = {'station':station['Name'],
                                     'station_lat':station['Lat'],
                                     'station_lon':station['Lon'],
                                     'train_id':time['TrainId'],
                                     'arrival_time':time['ArrivalTime'],
                                     'delayed':time['DelayFlag']}
                                southbound_status.append(data)
                                if time['DelayFlag'] == True:
                                    self.delays.append(data)

            return {'N':northbound_status, 'S':southbound_status}

    def get_next(self):
        """Gets the train status."""
        northbound_status = []
        southbound_status = []
        if self.data is None:
            return None
        data = self.data
        for station in data:
            if station['Id'] in self.stations:
                for direction in station['Directions']:
                    if (direction['Direction'] is 'N' and
                        direction['Direction'] in self.direction):
                        time = direction['StopTimes'][0]
                        if time['TrainId'] in self.trains:
                            data = {'station':station['Name'],
                                    'station_lat':station['Lat'],
                                    'station_lon':station['Lon'],
                                    'train_id':time['TrainId'],
                                    'arrival_time':time['ArrivalTime'],
                                    'delayed':time['DelayFlag']}
                            northbound_status.append(data)
                            if time['DelayFlag'] == True:
                                self.delays.append(data)

                    elif direction['Direction'] in self.direction:
                        time = direction['StopTimes'][0]
                        if time['TrainId'] in self.trains:
                            data = {'station':station['Name'],
                                    'station_lat':station['Lat'],
                                    'station_lon':station['Lon'],
                                    'train_id':time['TrainId'],
                                    'arrival_time':time['ArrivalTime'],
                                    'delayed':time['DelayFlag']}
                            southbound_status.append(data)
                            if time['DelayFlag'] == True:
                                self.delays.append(data)

        return {'N':northbound_status, 'S':southbound_status}
