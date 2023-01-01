from airquality import get_stations, Reading
from datetime import datetime


def test_get_stations():
    all_stations = get_stations()
    for each_station in all_stations:
        if each_station.get_id() == 355:
            station  = each_station
    assert station.get_id() == 355
    assert station.get_name() == "Zgierz, ul. Mielczarskiego"
    assert station.get_city_name() == "Zgierz"
    assert station.get_position() == (51.856692, 19.421231)
    assert str(station) == 'Zgierz, ul. Mielczarskiego'


def test_get_sensors():
    all_stations = get_stations()
    for each_station in all_stations:
        if each_station.get_id() == 355:
            station  = each_station
    all_sensors = station.get_sensors()
    sensor = all_sensors[0]
    assert sensor.get_name() == 'tlenek węgla'
    assert sensor.get_code() == 'CO'
    assert sensor.get_id() == 2370
    assert str(sensor.get_station()) == 'Zgierz, ul. Mielczarskiego'


def test_get_readings(monkeypatch):
    all_stations = get_stations()
    for each_station in all_stations:
        if each_station.get_id() == 355:
            station  = each_station
    all_sensors = station.get_sensors()
    sensor = all_sensors[0]

    def get_fake_reading(a):
        return Reading(sensor, 'CO', datetime.fromisoformat('2022-12-28 14:00:00'), 100)
    monkeypatch.setattr('airquality.Sensor.get_reading', get_fake_reading)
    reading = sensor.get_reading()
    assert reading.key == 'CO'
    assert reading.date == datetime(2022, 12, 28, 14, 0)
    assert reading.value == 100
    assert reading.get_sensor().get_id() == 2370