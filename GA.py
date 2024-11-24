import numpy as np
import copy

class Gen:
    def __init__(self):
        self.source_hidden_layer = np.random.rand() < .5
        self.source = np.random.randint(0,7)
        if self.source_hidden_layer:
            self.target = np.random.randint(0,2)
        else:
            self.target = np.random.randint(0,7)
        self.weight = np.random.uniform(-1,1)

class Genome:
    def __init__(self):
        self.length = 16
        self.genes = [Gen() for _ in range(self.length)]
        self.hidden_layer_bias = np.random.uniform(-1, 1, 7)  
        self.output_layer_bias = np.random.uniform(-1, 1, 2)



class GeneticAlgorithm:
    def __init__(self,popsize):
        self.popsize = popsize
        self.population = [Genome() for _ in range(self.popsize)]
        self.score = np.zeros((self.popsize))
        self.elite = None
        self.eliteScore = None
            
    def updateScore(self,newScore):
        self.score = newScore

    def tournament_selection(self):
        i1 = np.random.randint(self.popsize)
        i2 = np.random.randint(self.popsize)
        if self.score[i1] > self.score[i2]:
            return i1
        else:
            return i2
    
    def crossover(self, genoma1, genoma2):
        offspring = copy.deepcopy(genoma1)
        Ncrossovers = np.random.randint(1,5)
        for i in range(Ncrossovers):
            idx = np.random.randint(0,16)
            offspring.genes[idx].source_hidden_layer = genoma2.genes[idx].source_hidden_layer
            offspring.genes[idx].source = genoma2.genes[idx].source
            offspring.genes[idx].target = genoma2.genes[idx].target
        return offspring
    

    def mutation(self,genoma):
        offspring = copy.deepcopy(genoma)
        Nmutations = np.random.randint(0,5)
        for i in range(Nmutations):
            idx = np.random.randint(0,16)
            offspring.genes[idx] = Gen()
        return offspring
    
    def getNextGeneration1(self):

        offspring = []
        idxs = np.argsort(self.score)[::-1]

        # the 5% remains excactly
        for i in idxs[:int(self.popsize*0.05)]:
            offspring.append(copy.deepcopy(self.population[i]))

        # another 5% is new
        for i in idxs[:int(self.popsize*0.05)]:
            offspring.append(Genome())

        # 30% mutate from the best genome
        for i in range(int(self.popsize*0.3)):
            offspring.append(self.mutation(self.population[idxs[0]]))

        # 40% mutate from a random choice among the 5% of the best genomes
        for i in range(int(self.popsize*.4)):
            offspring.append(self.mutation(self.population[np.random.choice(idxs[:int(self.popsize*0.05)])]))

        # 20% crossover between 2 choices among the 5% of the best genomes
        for i in range(int(self.popsize*.2)):
            p1 = self.population[np.random.choice(idxs[:int(self.popsize*0.05)])]
            p2 = self.population[np.random.choice(idxs[:int(self.popsize*0.05)])]
            offspring.append(self.crossover(p1,p2))
        
        print(len(offspring))

        self.population = offspring
        return offspring

    

   






