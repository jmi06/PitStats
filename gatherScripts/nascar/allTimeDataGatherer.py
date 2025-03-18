import requests
import json
import os

def gatherAllTimeData():
    series_to_search = ['NascarCup', 'NascarTruck', 'NascarXfinity']

    for series in series_to_search:
        years_files = sorted(os.listdir(f'data/{series}/'))
        print(years_files)
        years_files.remove('All')

        all_time_races = {}
        all_time_drivers = {}




        for year in years_files:
            with open(f'data/{series}/{year}/races.json') as raceFile:
                races = json.load(raceFile)

            all_time_races[year] = races


            with open(f'data/{series}/{year}/drivers.json') as driverFile:
                drivers = json.load(driverFile)

            for driver in drivers:
                if driver not in all_time_drivers:
                    all_time_drivers[driver] = drivers[driver]
                    all_time_drivers[driver]['elo'] = 1000
                    all_time_drivers[driver]['race_num'] = 0


                if driver in all_time_drivers:
                    all_time_drivers[driver]['race_num'] += drivers[driver]['race_num']




        with open(f'data/{series}/All/races.json' ,'w') as newraceFile:
            json.dump(all_time_races, newraceFile)


        with open(f'data/{series}/All/drivers.json' ,'w') as newdriverFile:
            json.dump(all_time_drivers, newdriverFile)






