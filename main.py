import base64
import copy
import pickle
import uuid

import Pyro5.api
from Pyro5.api import SerializedBlob

from Chromosome import Chromosome
from ChromosomePickle import ChromosomeSerializer
from Crossover import Crossover
from Mutation import Mutation


class Main:
    def __init__(self):
        pass


if __name__ == "__main__":
    print("Iniciando Client do AG")
    population_size = 50
    courses = ["Ciência da Computação (Matutino)", "Engenharia Mecânica (Matutino)", "Engenharia Química (Matutino)"]

    generation_chromosomes = []
    # initialValuesCC = [1, 3, 6, 9, 15, 14, 20, 21, 0, 0, 3, 2, 11, 11, 17, 16, 21, 70, 0, 0, 5, 1, 7, 12, 15, 13, 18, 70, 0, 0, 4, 4, 7, 10, 17, 14, 20, 19, 0, 0, 2, 5, 10, 8, 16, 13, 19, 18, 0, 0]
    # initialValuesEM = [27, 24, 29, 30, 36, 35, 47, 43, 48, 49, 24, 22, 31, 31, 37, 34, 40, 46, 71, 71, 26, 22, 28, 29, 34, 39, 44, 40, 71, 71, 23, 26, 28, 33, 39, 35, 47, 41, 71, 48, 23, 25, 32, 30, 38, 36, 42, 45, 71, 49]
    # initialValuesEQ = [50, 50, 62, 62, 69, 66, 0, 0, 0, 0, 51, 53, 56, 58, 65, 67, 0, 0, 0, 0, 53, 55, 60, 57, 64, 64, 0, 0, 0, 0, 55, 51, 61, 63, 68, 67, 0, 0, 0, 0, 54, 52, 59, 58, 66, 65, 0, 0, 0, 0]
    for course in courses:
        generationCount = 0
        # if course == "Engenharia Química (Matutino)":
        while generationCount < population_size:
            # if generationCount == 0 and course == "Ciência da Computação (Matutino)":
            #     chromosome = Chromosome(course,10000, initialValuesCC)
            # elif generationCount == 0 and course == "Engenharia Mecânica (Matutino)":
            #     chromosome = Chromosome(course, 10000, initialValuesEM)
            # elif generationCount == 0 and course == "Engenharia Química (Matutino)":
            #     chromosome = Chromosome(course, 10000, initialValuesEQ)
            # else:
            chromosome = Chromosome(course, 10000, None)
            chromosome.generateRandom()
            generation_chromosomes.append(chromosome)
            generationCount += 1

    grouped_chromosomes_by_course = {}
    for chromosome in generation_chromosomes:
        course = chromosome.course
        if course not in grouped_chromosomes_by_course:
            grouped_chromosomes_by_course[course] = []
        grouped_chromosomes_by_course[course].append(chromosome)

    generation_full_chromosomes = []
    for index in range(len(grouped_chromosomes_by_course[generation_chromosomes[0].course])):
        full_chromosome = []
        for course, course_chromosomes in grouped_chromosomes_by_course.items():
            full_chromosome.append(course_chromosomes[index])
        generation_full_chromosomes.append(full_chromosome)

    servers_disponiveis = 1
    tamanho_subarray = len(generation_full_chromosomes)
    subarrays = []

    for i in range(servers_disponiveis):
        inicio = i * tamanho_subarray
        fim = (i + 1) * tamanho_subarray if i < servers_disponiveis - 1 else None
        subarray = generation_full_chromosomes[inicio:fim]
        if fim is None and inicio < len(generation_full_chromosomes):
            subarray += generation_full_chromosomes[inicio + tamanho_subarray:]

        subarrays.append(subarray)

    new_generation_chromosomes = []
    connection_uris = ["PYRO:obj_c0edd45b2e5c442283a20b0ee9e119d7@192.168.1.7:37218"]
    uri_index = 0
    for subarray in subarrays:
        rating = Pyro5.api.Proxy(connection_uris[uri_index])
        serialized_chromosomes = pickle.dumps(subarray)
        new_generation_chromosome = pickle.loads(base64.b64decode(rating.rate(serialized_chromosomes)["data"]))
        new_generation_chromosomes.append(new_generation_chromosome)
        uri_index += 1
    generation_chromosomes = copy.deepcopy(new_generation_chromosomes[0])

    count = 0
    outrocount = 0
    bestchromosome = []
    while count < 2000000:
        print("-------------------------------- Geração " + str(count) + " --------------------------------")
        grouped_chromosomes_by_course = {}
        for chromosome in generation_chromosomes:
            course = chromosome.course
            if course not in grouped_chromosomes_by_course:
                grouped_chromosomes_by_course[course] = []
            grouped_chromosomes_by_course[course].append(chromosome)

        new_generation = []
        for course, course_chromosomes in grouped_chromosomes_by_course.items():
            # if course == "Engenharia Química (Matutino)":
            # print("Seleção por eletismo")
            # percentageChanceOfElitism = 10
            # num_elements_to_copy = int(population_size / percentageChanceOfElitism)
            num_elements_to_copy = 4
            elite_chromosomes = sorted(course_chromosomes, key=lambda x: x.avaliation, reverse=True)
            chosen_chromosomes = elite_chromosomes[:num_elements_to_copy]

            # print("Crossover")
            crossoverChancePercentage = 70
            new_course_chromosomes = Crossover.cross(crossoverChancePercentage, course_chromosomes, chosen_chromosomes,
                                                     course)

            # print("Fazendo Mutação")
            mutationChancePercentage = 25
            Mutation.mutate(mutationChancePercentage, new_course_chromosomes, course)

            if len(new_course_chromosomes) > population_size:
                new_course_chromosomes = new_course_chromosomes[:population_size]
            new_generation.extend(new_course_chromosomes)

        generation_chromosomes = copy.deepcopy(new_generation)
        # print("Melhor cromossomo")
        # print(str(course_chromosomes[0].course) + " - " + str(course_chromosomes[0].values) + " evaluation: " +
        #       str(course_chromosomes[0].avaliation))

        generation_full_chromosomes1 = []
        for index in range(len(grouped_chromosomes_by_course[generation_chromosomes[0].course])):
            full_chromosome = []
            for course, course_chromosomes in grouped_chromosomes_by_course.items():
                full_chromosome.append(course_chromosomes[index])
            generation_full_chromosomes1.append(full_chromosome)
        grouped_chromosomes_by_course = {}
        for chromosome in generation_chromosomes:
            course = chromosome.course
            if course not in grouped_chromosomes_by_course:
                grouped_chromosomes_by_course[course] = []
            grouped_chromosomes_by_course[course].append(chromosome)

        generation_full_chromosomes = []
        for index in range(len(grouped_chromosomes_by_course[generation_chromosomes[0].course])):
            full_chromosome = []
            for course, course_chromosomes in grouped_chromosomes_by_course.items():
                full_chromosome.append(course_chromosomes[index])
            generation_full_chromosomes.append(full_chromosome)

        subarrays = []
        for i in range(servers_disponiveis):
            inicio = i * tamanho_subarray
            fim = (i + 1) * tamanho_subarray if i < servers_disponiveis - 1 else None
            subarray = generation_full_chromosomes[inicio:fim]
            if fim is None and inicio < len(generation_full_chromosomes):
                subarray += generation_full_chromosomes[inicio + tamanho_subarray:]

            subarrays.append(subarray)

        new_generation_chromosomes = []
        uri_index = 0
        for subarray in subarrays:
            rating = Pyro5.api.Proxy(connection_uris[uri_index])
            serialized_chromosomes = pickle.dumps(subarray)
            new_generation_chromosome = pickle.loads(base64.b64decode(rating.rate(serialized_chromosomes)["data"]))
            new_generation_chromosomes.append(new_generation_chromosome)
            uri_index += 1
        generation_chromosomes = copy.deepcopy(new_generation_chromosomes[0])

        summed_chromosomes = [(sum(chrom.avaliation for chrom in full_chromosomes), full_chromosomes) for
                              full_chromosomes in generation_full_chromosomes1]
        sorted_summed_chromosomes = sorted(summed_chromosomes, key=lambda x: x[0], reverse=True)
        if sorted_summed_chromosomes[0][0] > (sum(chrom.avaliation for chrom in bestchromosome)):
            bestchromosome = copy.deepcopy(sorted_summed_chromosomes[0][1])
        if sorted_summed_chromosomes[0][0] >= 29900:
            outrocount += 1
        if sorted_summed_chromosomes[0][0] == 30000:
            break
        print("Melhor avaliação: " + str(sorted_summed_chromosomes[0][0]))

        if outrocount == 50:
            outrocount = 0
            new_random_population = population_size / 2
            index = 0
            generationCount = 0
            for chrom in generation_chromosomes:
                if generationCount >= new_random_population:
                    chromosome = Chromosome(chrom.course, 10000, None)
                    chromosome.generateRandom()
                    generation_chromosomes[index] = chromosome
                generationCount += 1
                if generationCount == population_size:
                    generationCount = 0
                index += 1
                grouped_chromosomes_by_course = {}
                for chromosome in generation_chromosomes:
                    course = chromosome.course
                    if course not in grouped_chromosomes_by_course:
                        grouped_chromosomes_by_course[course] = []
                    grouped_chromosomes_by_course[course].append(chromosome)

                generation_full_chromosomes = []
                for index in range(len(grouped_chromosomes_by_course[generation_chromosomes[0].course])):
                    full_chromosome = []
                    for course, course_chromosomes in grouped_chromosomes_by_course.items():
                        full_chromosome.append(course_chromosomes[index])
                    generation_full_chromosomes.append(full_chromosome)

                servers_disponiveis = 1
                tamanho_subarray = len(generation_full_chromosomes)
                subarrays = []

                for i in range(servers_disponiveis):
                    inicio = i * tamanho_subarray
                    fim = (i + 1) * tamanho_subarray if i < servers_disponiveis - 1 else None
                    subarray = generation_full_chromosomes[inicio:fim]
                    if fim is None and inicio < len(generation_full_chromosomes):
                        subarray += generation_full_chromosomes[inicio + tamanho_subarray:]

                    subarrays.append(subarray)

                new_generation_chromosomes = []
                uri_index = 0
                for subarray in subarrays:
                    rating = Pyro5.api.Proxy(connection_uris[uri_index])
                    serialized_chromosomes = pickle.dumps(subarray)
                    new_generation_chromosome = pickle.loads(base64.b64decode(rating.rate(serialized_chromosomes)["data"]))
                    new_generation_chromosomes.append(new_generation_chromosome)
                    uri_index += 1
                generation_chromosomes = copy.deepcopy(new_generation_chromosomes[0])
        count += 1

    print("Ababou cupinxa")
    print("Melhor cromossomo")
    for chrom in bestchromosome:
        print(str(chrom.course) + " - " + str(chrom.values) + " evaluation: " +
              str(chrom.avaliation))
