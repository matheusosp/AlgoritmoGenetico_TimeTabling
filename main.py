import copy
import random
from typing import List

import Pyro5.api
import socket

from Chromosome import Chromosome
from Crossover import Crossover
from Mutation import Mutation
from Rating import Rating


class Main:
    def __init__(self):
        pass


if __name__ == "__main__":
    print("Iniciando Client do AG")
    population_size = 10
    rating = Rating()
    courses = ["Ciência da Computação (Matutino)", "Engenharia Mecânica (Matutino)", "Engenharia Química (Matutino)"]
    # generationCCChromosomes = []
    # generationEMChromosomes = []
    # generationEQChromosomes = []

    generationChromosomes = []
    for course in courses:
        generationCount = 0
        while generationCount < population_size:
            # if generationCount == 0:
            #     chromosome = Chromosome(1000, initialValues)
            # else:
            chromosome = Chromosome(course, 1000, None)
            chromosome.generateRandom()
            generationChromosomes.append(chromosome)
            # if chromosome.course == "Ciência da Computação (Matutino)":
            #     generationCCChromosomes.append(chromosome)
            # if chromosome.course == "Engenharia Mecânica (Matutino)":
            #     generationEMChromosomes.append(chromosome)
            # if chromosome.course == "Engenharia Química (Matutino)":
            #     generationEQChromosomes.append(chromosome)
            generationCount += 1

    for chromosome in generationChromosomes:
        rating.rate(chromosome)
    # for chromosome in generationCCChromosomes:
    #     print(str(chromosome.values) + " evaluation: " + str(chromosome.avaliation))
    # for chromosome in generationEMChromosomes:
    #     print(str(chromosome.values) + " evaluation: " + str(chromosome.avaliation))
    # for chromosome in generationEMChromosomes:
    #     print(str(chromosome.values) + " evaluation: " + str(chromosome.avaliation))
    count = 0
    bestchromosome = [
        Chromosome("Ciência da Computação (Matutino)", 0),
        Chromosome("Engenharia Mecânica (Matutino)", 0),
        Chromosome("Engenharia Química (Matutino)", 0)
    ]
    while count < 2000000:
        print("-------------------------------- Geração " + str(count) + " --------------------------------")

        # print("Seleção por eletismo")
        percentageChanceOfElitism = 10
        num_elements_to_copy = int(len(generationChromosomes) / percentageChanceOfElitism)
        elite_chromosomes = sorted(generationChromosomes, key=lambda x: x.avaliation, reverse=True)
        chosen_chromosomes = elite_chromosomes[:num_elements_to_copy]

        # print("Crossover")
        crossoverChancePercentage = 70
        generationChromosomes = Crossover.cross(crossoverChancePercentage, generationChromosomes, chosen_chromosomes)

        # print("Fazendo Mutação")
        mutationChancePercentage = 25
        Mutation.mutate(mutationChancePercentage, generationChromosomes)

        for chromosome in generationChromosomes:
            rating.rate(chromosome)
        if len(generationChromosomes) > 10:
            generationChromosomes = sorted(generationChromosomes, key=lambda x: x.avaliation, reverse=True)
            generationChromosomes = generationChromosomes[:population_size]

        print("Melhor cromossomo")
        print(str(generationChromosomes[0].values) + " evaluation: " + str(generationChromosomes[0].avaliation))
        if generationChromosomes[0].avaliation > bestchromosome.avaliation:
            bestchromosome = copy.deepcopy(generationChromosomes[0])
        if generationChromosomes[0].avaliation == 1000:
            break
        count += 1
    print("Ababou cupinxa")
    print("Melhor cromossomo")
    print(str(bestchromosome.values) + " evaluation: " + str(bestchromosome.avaliation))
