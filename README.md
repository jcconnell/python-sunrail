python-sunrail
==============================================================================================================================================================================================

Provides basic API to [Sunrail](https://sunrail.com/).

## Install

`pip install sunrail`

## Usage

```python
from sunrail import SunRail

sr = SunRail()
sr.update()
sr.get_next()
```

## Advanced Usage

```python
from sunrail import SunRail

# Only these stations
sr = SunRail(include_stations['17', '2'])

# All stations but these exclusions
sr = SunRail(exclude_stations['17', '2'])

# Only these trains
sr = SunRail(include_trains['P301', 'P340'])

# All trains but these exclusions
sr = SunRail(exclude_trains['P301', 'P340'])

# Only northbound trains
sr = SunRail(direction='N')

```

## Available Stations, Trains & Directions
```python
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
```

## Example Alert
```json
{
   "status":"ok",
   "result":[
      {
         "id":6758,
         "title":"",
         "message":"Trains P304 is cancelled. All other trains on time.",
         "enabled":true,
         "currentdate":"08\/27\/2018 11:52 AM",
         "link":null
      }
   ],
   "cached":true,
   "limit":25,
   "total":1
}
```

## Development

Pull requests welcome.

## Disclaimer

Not affiliated with sunrail.com. Use at your own risk.

## Notes

See `example_response.json` and `pretty_example_response.json` for an example of the API response.
