import requests
from datetime import datetime

urls = {
    'findAll': 'https://api.gios.gov.pl/pjp-api/rest/station/findAll',
    'sensors': 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/{stationId}',
    'getData': 'https://api.gios.gov.pl/pjp-api/rest/data/getData/{sensorId}'
}

def get_stations():
    stations = requests.get(urls['findAll']).json()
    return [Station(each_station) for each_station in stations]


class AirApiObject:
    def __init__(self, data):
        self._data = data

    def get_id(self):
        return self._data['id']

    def _get(self, key):
        return self._data[key]


class Station(AirApiObject):
    def get_name(self):
        return self._get('stationName')

    def get_position(self):
        lat = self._get('gegrLat')
        lon = self._get('gegrLon')
        return (float(lat), float(lon))

    def get_city_name(self):
        return self._get('city')['name']

    def get_city_data(self):
        return self._get('commune')

    def get_sensors(self):
        id = self._get('id')
        sensors_json = requests.get(urls['sensors'].format(stationId=id)).json()
        return [Sensor(sensor, self) for sensor in sensors_json]

    def __str__(self) -> str:
        return self.get_name()


class Sensor(AirApiObject):
    def __init__(self, data, station):
        super().__init__(data)
        self._station = station

    def get_name(self):
        return self._get('param')['paramName']

    def get_code(self):
        return self._get('param')['paramCode']

    def get_station(self):
        return self._station

    def get_reading(self):
        id = self._get('id')
        readings = requests.get(urls['getData'].format(sensorId=id)).json()
        key = readings['key']
        values = readings['values']
        return [
            Reading(self,
                    key,
                    datetime.fromisoformat(value['date']),
                    value['value'])
            for value in values
        ]


class Reading:
    def __init__(self, sensor, key, date, value):
        self._sensor = sensor
        self.key = key
        self.date = date
        self.value = value

    def get_sensor(self):
        return self._sensor

    def __str__(self) -> str:
        return f'{self.key}: {self.value} on {self.date}'