import datagatherer
import elo
import allTimeDataGatherer
import allTimeElo


print('dataGather')

datagatherer.gatherData()


print('Generate Elo')
elo.generate_elo()

print('gatherAllTimeData')
allTimeDataGatherer.gatherAllTimeData()

print('alltime elo')
allTimeElo.generate_allTimeElo()