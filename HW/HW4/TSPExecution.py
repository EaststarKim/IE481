from TravelingSalesmanProblem import *

#data_mode = 'Random'
height = 500
width = 700
cities = 15

data_mode = 'Load'
csvfile = "TSP1.csv"

numOffsprings=70
numPopulation=100
mutationFactor = 0.5
time = 180

tsp = TravelingSalesmanProblem(data_mode,csvfile,cities,height, width, time)
routes, utility, distance, elapsedTime = tsp.performEvolution(numOffsprings, numPopulation, mutationFactor)

currentCity = 0
route = ''
for itr in range(len(routes)):
    route = route + '->' + str(currentCity)
    currentCity = routes[currentCity]
print ("===== 20180065, Student =====")
print ("Routes : %s" %(route))
print ("Distance : ", distance)
print ("Elapsed time : ", elapsedTime, "secs")
