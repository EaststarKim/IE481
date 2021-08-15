from GeneticAlgorithmProblem import *
import random
import math
import time
import csv

class TravelingSalesmanProblem(GeneticAlgorithmProblem):
    
    genes = []
    dicLocations = {}
    gui = ''
    best = ''
    time = 0
    city_n = 0 #number of cities == number of genes
    dis = [] #distance pre-calculation

    def __init__(self, data_mode,csvfile,numCities, height, width, time):
        self.time = time
        if data_mode == 'Random':
            for itr in range(numCities):
                x = random.uniform(0, width)
                y = random.uniform(0, height)
                coordinate = [x, y]
                self.dicLocations[itr] = coordinate
        elif data_mode == 'Load':
            with open(csvfile, 'r') as my_csv:
                contents = list(csv.reader(my_csv, delimiter=","))
                self.city_n=len(contents)
                for itr in range(self.city_n):
                    x,y= contents[itr][0],contents[itr][1]
                    self.dicLocations[itr] = [float(x),float(y)]

    #def registerGUI(self, gui):
    #    self.gui = gui

    def calculateDistance(self):
        #dis : city_n * city_n matrix
        for i in range(self.city_n):
            self.dis.append([0]*self.city_n)

        for i in range(self.city_n):
            for j in range(i+1,self.city_n):
                city1=self.dicLocations[i]
                city2=self.dicLocations[j]
                self.dis[i][j]=self.dis[j][i]=math.sqrt(math.pow(city1[0]-city2[0],2)+math.pow(city1[1]-city2[1],2))

    def performEvolution(self, numOffsprings, numPopulation, mutationFactor):
        #if self.gui != '':
        #    self.gui.start()
        startTime = time.time()
        self.calculateDistance()
        population = self.createInitialPopulation(numPopulation)
        self.best=GeneticAlgorithmInstance()
        self.best.setGenotype(population[0].getGenotype().copy())
        prev=population[0]
        cnt=-1
        while True:
            currentTime = time.time()
            if (currentTime - startTime) >= self.time:
                break
            offsprings = {}
            for itr in range(numOffsprings):
                p1, p2 = self.selectParents(population)

                offsprings[itr] = self.crossoverParents(p1, p2)
                factor=mutationFactor + 1/(1 + currentTime - startTime)

                self.mutation(offsprings[itr], factor)

            population = self.substitutePopulation(population, offsprings)

            mostFittest = self.findBestSolution(population)
            if self.calculateTotalDistance(self.best) > self.calculateTotalDistance(mostFittest):
                self.best.setGenotype(mostFittest.getGenotype().copy())
            print(self.calculateTotalDistance(self.best))
            if prev != mostFittest:
                cnt = 0
            prev=mostFittest
            cnt+=1
            if cnt>30:
                cnt=1
                t=int(self.city_n/5)
                for p in population:
                    for j in range(t):
                        self.mutation(p,1)
            #if self.gui != '':
            #    self.gui.update()

        endTime = time.time()
        return self.best.getGenotype(), self.fitness(self.best), self.calculateTotalDistance(self.best), (endTime - startTime)

    def fitness(self, instance):
        distance=self.calculateTotalDistance(instance)
        utility = 10000.0 / distance
        return utility
    
    def calculateTotalDistance(self, instance):
        genotype = instance.getGenotype()
        currentCity = 0
        distance = 0.0
        for itr in range(self.city_n-1):
            nextCity = genotype[currentCity]
            distance+=self.dis[currentCity][nextCity]
            currentCity = nextCity
        return distance

    def createInitialPopulation(self, numPopulation):
        population = []
        for itr in range(numPopulation):
            genotype = list(range(self.city_n))
            while self.isInfeasible(genotype):
                random.shuffle(genotype)
            instance = GeneticAlgorithmInstance()
            instance.setGenotype(genotype)
            population.append(instance)
        return population
        
    def isInfeasible(self, genotype):
        currentCity = 0
        visitedCity = {}
        for itr in range(self.city_n):
            visitedCity[currentCity] = 1
            currentCity = genotype[currentCity]

        return len(visitedCity.keys()) != self.city_n
        
    def findBestSolution(self, population):
        idxMaximum = -1
        max = -99999
        for itr in range(len(population)):
            if max < self.fitness(population[itr]):
                max = self.fitness(population[itr])
                idxMaximum = itr
        return population[idxMaximum]
    
    def selectParents(self, population):
        rankFitness = {}
        originalFitness = {}
        maxUtility = -999999
        minUtility = 999999
        for itr in range(len(population)):
            originalFitness[itr] = self.fitness(population[itr])
            maxUtility=max(maxUtility,originalFitness[itr])
            minUtility=min(minUtility,originalFitness[itr])

        k=5
        total = 0.0
        for itr in range(len(population)):
            rankFitness[itr] = originalFitness[itr]-minUtility+(maxUtility-minUtility)/(k-1)
            total+=rankFitness[itr]
        
        idx1 = -1
        idx2 = -1
        while idx1 == idx2:
            dart = random.uniform(0, total)
            sum = 0.0
            for itr in range(len(population)):
                sum+=rankFitness[itr]
                if dart <= sum:
                    idx1 = itr
                    break
            dart = random.uniform(0, total)
            sum = 0.0
            for itr in range(len(population)):
                sum+=rankFitness[itr]
                if dart <= sum:
                    idx2 = itr
                    break
        return population[idx1], population[idx2]
            
    def crossoverParents(self, instance1, instance2):
        newInstance = GeneticAlgorithmInstance()

        dicNeighbor = {}
        for itr in range(self.city_n):
            neighbor = {}
            neighbor1 = self.getNeighborCity(instance1, itr)
            neighbor2 = self.getNeighborCity(instance2, itr)
            neighbor[neighbor1[0]] = 1
            neighbor[neighbor1[1]] = 1
            neighbor[neighbor2[0]] = 1
            neighbor[neighbor2[1]] = 1
            dicNeighbor[itr] = neighbor.keys()
        
        currentCity = 0
        visitedCity = {}
        path = [0]*self.city_n
        for itr in range(self.city_n):
            visitedCity[currentCity] = 1
            nextCity = self.getNeighborNotVisitedCity(list(visitedCity.keys()), dicNeighbor)
            if nextCity == -1:
                for i in range(self.city_n):
                    if visitedCity.get(i)==None: #Not visited yet
                        nextCity=i
                if nextCity==-1:
                    nextCity=0
            path[currentCity] = nextCity
            currentCity = nextCity

        newInstance.setGenotype(path)
        return newInstance       
    
    def getNeighborNotVisitedCity(self, lstVisitedCity, dicNeighbor):
        cities = list(dicNeighbor.keys())
        for itr in range(len(lstVisitedCity)):
            cities.remove(lstVisitedCity[itr])
        candidates = []
        for itr in range(len(cities)):
            location = cities[itr]
            candidates.append(location)
        if len(candidates) == 0:
            return -1
        random.shuffle(candidates)
        return candidates[0]
        
    def getNeighborCity(self, instance, currentCity):
        genotype = instance.getGenotype()
        ret1=-1
        for itr in range(self.city_n):
            if genotype[itr] == currentCity:
                ret1 = itr
                break
        ret2 = genotype[currentCity]
        neighbor = [ret1, ret2]
        return neighbor
    
    def mutation(self, instance, factor):
        genotype = instance.getGenotype()
        mutationDone = random.random()<factor
        while mutationDone == True:
            idx1 = random.randint(0, self.city_n-1)
            idx2 = random.randint(0, self.city_n-1)
            genotype[idx1],genotype[idx2]=genotype[idx2],genotype[idx1]
            if self.isInfeasible(genotype):
                mutationDone = True
            else:
                mutationDone = False
        instance.setGenotype(genotype)

    def substitutePopulation(self, population, children):
        for itr1 in range(len(population)):
            for itr2 in range(itr1+1,len(population)):
                if self.fitness(population[itr1]) < self.fitness(population[itr2]):
                    population[itr1], population[itr2] = population[itr2], population[itr1]
        for itr in range(len(children)):
            population[len(population)-len(children)+itr] = children[itr]
        return population
