import requests
import json
import os


years = ['2025', '2024', '2023', '2022','2021', '2020', '2019', '2018']
series_num = ['2', '3']
for series in series_num:
    for year in years:
        print(year)
        print(series)

        drivers ={}
        races ={}




        race_order = []

        all_race_ids = requests.get(f'https://cf.nascar.com/cacher/{year}/race_list_basic.json').json()



        for i in all_race_ids[f'series_{series}']:
            race_order.append(i['race_id'])


        print(race_order)





        # url = 'https://cf.nascar.com/cacher/2025/1/5551/weekend-feed.json'

        # race_order = [5546, 5547, 5551, 5549, 5548, 5583, 5553, 5558, 5550, 5555, 5554, 5557, 5561, 5562,5563, 5568, 5573, 5552, 5570, 5576, 5569, 5565, 5556, 5571, 5566, 5577, 5572, 5574, 5575, 5564, 5578, 5567, 5579, 5581, 5582, 5580, 5584, 5585]

        driver_standings = requests.get(f'https://cf.nascar.com/cacher/{year}/{series}/final/{series}-drivers-points.json')
        driver_standings_json = driver_standings.json()

        # with open('2025/data/drivers.json', 'r') as driverFile:
        #     driver = json.load(driverFile)


        # with open('2025/data/races.json', 'r') as raceFile:

        #     races = json.load(raceFile)


        def gather_data(url, race_results):

            if race_results['weekend_race'] is not None:
                print('race name',race_results['weekend_race'][0]['race_name'])
                print(url)
                # race_results = {}
                
                # race_results = requests.get(url)

                # race_results = race_results.json()
                if race_results['weekend_race'][0]['race_name'] not in races:
                    races[race_results['weekend_race'][0]['race_name']] = {}
                for placement in race_results['weekend_race'][0]['results']:
                    if placement['driver_id'] not in drivers and placement['finishing_position'] != 0:

                        drivers[placement['driver_id']] = {"elo": 1000, "race_num": 0, "name": placement['driver_fullname']}




                    if int(placement['finishing_position']) > 0:

                        races[race_results['weekend_race'][0]['race_name']][placement['finishing_position']] = {}
                        races[race_results['weekend_race'][0]['race_name']][placement['finishing_position']]['name'] = placement['driver_fullname']
                        races[race_results['weekend_race'][0]['race_name']][placement['finishing_position']]['driver_id'] = placement['driver_id']

                        races[race_results['weekend_race'][0]['race_name']][placement['finishing_position']]['placement'] = placement['finishing_position']

                        drivers[placement['driver_id']]["race_num"]+=1

                    








        # json.dump(drivers, '2025/data/drivers.json')
        # json.dump(races, '2025/data/races.json')


        race_results = {}

        for i in race_order:




            race_results = requests.get(f'https://cf.nascar.com/cacher/{year}/{series}/{i}/weekend-feed.json')
            print(race_results.status_code)


            try:
                json_race_results = race_results.json()
            except requests.exceptions.JSONDecodeError:
                print("Error: Failed to parse JSON, breaking loop.")
                print(f"Raw response:\n{race_results.text}")  # Debugging info
                continue  # Stop if JSON parsing fails



            gather_data(f'https://cf.nascar.com/cacher/{year}/{series}/{i}/weekend-feed.json', json_race_results)

            



        for i in driver_standings_json:
            drivers_name = i['driver_id']
            print('driver_id:', drivers_name )
            if drivers_name in drivers:
                if i['starts'] >= sum(1 for race in races.values() if race) -1:
                    drivers[drivers_name]['full_time'] = True
                else:
                    drivers[drivers_name]['full_time'] = False

                drivers[drivers_name]['wins'] = i['wins']
                drivers[drivers_name]['playoff_points'] = i['playoff_points']
                drivers[drivers_name]['playoff_rank'] = i['playoff_rank']
                drivers[drivers_name]['playoff_rank'] = i['playoff_rank']
                if 'points_earned' in drivers[drivers_name]:
                    drivers[drivers_name]['points_earned'] = i['points_earned']
                else:
                    drivers[drivers_name]['points_earned'] = i['points']

                drivers[drivers_name]['position'] = i['position']


            if series == "1":
                name_series = "NascarCup"
            if series == "2":
                name_series = "NascarXfinity"
            if series == "3":
                name_series = "NascarTruck"

            os.makedirs(f'{name_series}/{year}', exist_ok=True)
            with open(f'{name_series}/{year}/drivers.json', 'w') as driverFile:
                json.dump(drivers, driverFile)

            with open(f'{name_series}/{year}/races.json', 'w') as raceFile:
                json.dump(races, raceFile)
