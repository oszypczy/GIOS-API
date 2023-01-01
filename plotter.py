from matplotlib import pyplot as plt
import airquality
import sys
import argparse


def list_stations(args):
    pattern = args.list_stations
    all_stations = airquality.get_stations()
    for station in all_stations:
        if not pattern:
            print(f'{station.get_id()}\t{station.get_name()}')
            continue
        if pattern in station.get_name():
            print(f'{station.get_id()}\t{station.get_name()}')


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument('--list-stations')
    parser.add_argument('--list-all-stations', action='store_true')
    parser.add_argument('--station-id')
    parser.add_argument('--save', action='store_true')
    args = parser.parse_args(arguments[1:])
    if args.list_stations or args.list_all_stations:
        list_stations(args)
        return
    all_stations = airquality.get_stations()
    for station in all_stations:
        if str(station.get_id()) == args.station_id:
            final_station = station
    all_sensors = final_station.get_sensors()
    for sensor in all_sensors:
        readings = sensor.get_reading()
        keys = [reading.date for reading in readings]
        values = [reading.value for reading in readings]
        plt.plot(keys, values, 'o-', label=sensor.get_name(), markersize=3)
    plt.legend()
    plt.title(label=final_station.get_name())
    if args.save:
        plt.savefig(f'{final_station.get_name()}.pdf', format='pdf')
    plt.show()


if __name__ == '__main__':
    main(sys.argv)