from deap import cma,creator,base,tools,algorithms
import math
import numpy
import random
IND_SIZE = 30
#define the fitness to maximaize
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
#define the individual in population as a list
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("attribute", random.random)
#initiate 30 weights in the individual as random values
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attribute, n=IND_SIZE)
#add individual to population
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#fitness function
def evaluate(individual):
    val = math.ceil(sum(individual))
    if(val>0 and val<20) and (val%2==1):
        #if (theta - theta')^2 /2 is close to expected result. Reinforce positively.
        return 1,
    else:
        #else reinforce regatively
        return  0,

#output check
def check(individual,extra):
    if(extra=="h"):
        print math.ceil(sum(individual.fitness.values))

    print math.ceil(sum(individual))

#register operators
toolbox.register("mate", tools.cxTwoPoints)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)
toolbox.register("check", check)


def main():
    numpy.random.seed(128)

    #population count =50 individuals
    pop = toolbox.population(n=50)
    print("Before\n\n")
    print map(toolbox.check,pop,"")
    print("\n\n")
    print(pop[0])

    #define cma strategy, where it restarts sigma is step-size and lambda_ offspring
    strategy = cma.Strategy(centroid=pop[0], sigma=3.0, lambda_=5.0)
    toolbox.register("generate", strategy.generate, creator.Individual)
    toolbox.register("update", strategy.update)

    #get the best of the results - here I am getting every one from population for testing
    hof = tools.HallOfFame(50)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    #define number of generation and stats and pass in the hallOfFame for cmaes to do its work
    algorithms.eaGenerateUpdate(toolbox, ngen=250, stats=stats, halloffame=hof)
    print("After\n\n")
    print map(toolbox.check,hof,"")
    print("\n\n")


main()