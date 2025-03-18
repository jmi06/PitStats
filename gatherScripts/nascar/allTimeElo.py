import json
import statistics
import os


def generate_allTimeElo():


    series_to_search = ['NascarCup', 'NascarTruck', 'NascarXfinity']




    for series in series_to_search:
        # print(series)

        all_time_drivers = {}
        all_time_races = {}

        with open(f'data/{series}/All/races.json') as raceFile:
            all_time_races = json.load(raceFile)
        with open(f'data/{series}/All/drivers.json') as driverFile:
            all_time_drivers = json.load(driverFile)







        for driver in all_time_drivers:
            if driver not in all_time_drivers:
                all_time_drivers[driver] = {"elo": 1000}







        for year in all_time_races:
            # print(year)



            for race in all_time_races[year]:
                # print(race)

                for position in all_time_races[year][race]:
                    # print(races[race][position]['driver_id'])
                    # print(position)
                    field_elo = []
                    drivers_ahead = []
                    drivers_behind = []
                    driver_elo = round(all_time_drivers[str(all_time_races[year][race][position]['driver_id'])]['elo'],2)
                    k = 4

                    for num_position in all_time_races[year][race]:
                        if int(num_position) < int(position):
                            field_elo.append(round(all_time_drivers[str(all_time_races[year][race][num_position]['driver_id'])]['elo'],2))
                            # print('ahead')
                        if int(num_position) > int(position):
                            field_elo.append(round(all_time_drivers[str(all_time_races[year][race][num_position]['driver_id'])]['elo'],2))
                            # print('behind')


                    # print(drivers_behind)
                    if len(drivers_ahead) > 0: 
                        avg_drivers_ahead = statistics.mean(drivers_ahead)
                    else:
                        avg_drivers_ahead = 0

                    if len(drivers_behind) > 0: 
                        avg_drivers_behind = statistics.mean(drivers_behind)
                    else:
                        avg_drivers_behind = 0



                    average_field_elo = statistics.mean(field_elo)
                    # expected_score = 1/ (1+ (10)** ((avg_drivers_ahead-driver_elo)/400)   )
                    # driver_score = (len(race) - int(position))/(len(race)-1)
                    # new_elo = driver_elo + k * (driver_score - expected_score)
                    total_drivers = len(race)
                    # expected_ahead = 1 / (1+(10)**((avg_drivers_ahead-driver_elo) / 400) )
                    # expected_behind = 1 / (1+(10)**((driver_elo-avg_drivers_behind) / 400) )

                    # new_elo = driver_elo + ( k/(total_drivers-1)) * ( (total_drivers-int(position)) - (int(position) -1 ) * expected_ahead + (total_drivers-int(position)) * expected_behind   )

                    expected_score = 1 / (1 +(10)**((average_field_elo-driver_elo)/400))
                    score = (total_drivers - int(all_time_races[year][race][position]['placement'])) / (total_drivers -1)
                    new_elo = driver_elo +k*(score - expected_score)
                    new_elo = round(new_elo,2)
                    delta_elo = round(new_elo - driver_elo,2)
                    # print('expected_score', expected_score)
                    
                    # print('score', score)

                    # new_elo = driver_elo + ( k/(total_drivers-1)) * ( (total_drivers-int(position)) - (int(position) -1 ) * expected_ahead + (total_drivers-int(position)) * expected_behind   )


                    all_time_races[year][race][position]['delta_elo'] = delta_elo


                    all_time_races[year][race][position]['elo_before'] = round(driver_elo,2)
                    all_time_races[year][race][position]['elo_after'] = round(new_elo,2)



                    all_time_drivers[str(all_time_races[year][race][position]['driver_id'])]['elo'] = new_elo

        # str(races[race][position]['driver_id'])



        with open(f'data/{series}/All/drivers.json', 'w') as eloFile:
            json.dump(all_time_drivers, eloFile)


        with open(f'data/{series}/All/races.json', 'w') as finalRaceFile:
            json.dump(all_time_races, finalRaceFile)
