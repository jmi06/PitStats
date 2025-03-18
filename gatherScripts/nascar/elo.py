import json
import statistics
import os

def generate_elo():

    series_to_search = ['NascarCup', 'NascarTruck', 'NascarXfinity']




    for series in series_to_search:

        years_to_search = sorted(os.listdir(f'data/{series}/'))
        years_to_search.remove('All')
        for year in years_to_search:
            print(series, year)
            for file in os.listdir(f'data/{series}/{year}'):
                print(os.listdir(f'data/{series}/{year}'))


                with open(f'data/{series}/{year}/races.json') as raceFile:
                    races = json.load(raceFile)
                with open(f'data/{series}/{year}/drivers.json') as driverFile:
                    drivers = json.load(driverFile)






                for race in races:
                    for position in races[race]:
                        print(races[race][position]['driver_id'])

                        field_elo = []
                        drivers_ahead = []
                        drivers_behind = []
                        driver_elo = round(drivers[str(races[race][position]['driver_id'])]['elo'],2)
                        k = 16

                        for num_position in races[race]:
                            if int(num_position) < int(position):
                                field_elo.append(round(drivers[str(races[race][num_position]['driver_id'])]['elo'],2))
                                # print('ahead')
                            if int(num_position) > int(position):
                                field_elo.append(round(drivers[str(races[race][num_position]['driver_id'])]['elo'],2))
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



                        # expected_score = 1/ (1+ (10)** ((avg_drivers_ahead-driver_elo)/400)   )
                        # driver_score = (len(race) - int(position))/(len(race)-1)
                        # new_elo = driver_elo + k * (driver_score - expected_score)
                        # field_elo = field_elo.append(drivers_ahead)
                        # field_elo = field_elo.append(drivers_behind)
                        average_field_elo = statistics.mean(field_elo)
                        # print('average', average_field_elo)
                        # print('old_elo', driver_elo)


                        total_drivers = len(race)
                        # expected_ahead = 1 / (1+(10)**((avg_drivers_ahead-driver_elo) / 400) )
                        # expected_behind = 1 / (1+(10)**((driver_elo-avg_drivers_behind) / 400) )




                        # ELO V1.0.0
                        expected_score = 1 / (1 +(10)**((average_field_elo-driver_elo)/400))
                        score = (total_drivers - int(races[race][position]['placement'])) / (total_drivers -1)
                        # print('expected_score', expected_score)
                        
                        # print('score', score)

                        # # new_elo = driver_elo + ( k/(total_drivers-1)) * ( (total_drivers-int(position)) - (int(position) -1 ) * expected_ahead + (total_drivers-int(position)) * expected_behind   )
                        new_elo = driver_elo +k*(score - expected_score)
                        new_elo = round(new_elo,2)
                        delta_elo = round(new_elo - driver_elo,2)


                        #ELO V2.0.0
                        # performance_rating = average_field_elo + 400 * (1 - int(position)/total_drivers)
                        # new_elo = driver_elo +k *(performance_rating - driver_elo)
                        # new_elo = round(new_elo,2)
                        # delta_elo = round(new_elo - driver_elo,2)



                        
                        races[race][position]['delta_elo'] = delta_elo





                        races[race][position]['elo_before'] = round(driver_elo,2)
                        races[race][position]['elo_after'] = round(new_elo,2)



                        drivers[str(races[race][position]['driver_id'])]['elo'] = new_elo

                # str(races[race][position]['driver_id'])



            with open(f'data/{series}/{year}/drivers.json', 'w') as eloFile:
                json.dump(drivers, eloFile)


            with open(f'data/{series}/{year}/races.json', 'w') as finalRaceFile:
                json.dump(races, finalRaceFile)
