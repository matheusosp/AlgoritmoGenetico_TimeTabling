import base64
import copy
import pickle
import time

import Pyro5.api

from Chromosome import Chromosome
from Crossover import Crossover
from Mutation import Mutation


class TimetablingResolver:
    def __init__(self):
        self.population_size = 50
        self.servers_disponiveis = 3
        self.num_chromosomes_elitism = 4
        self.crossover_chance_percentage = 70
        self.mutation_chance_percentage = 25
        self.generation_length_to_send = int(self.population_size / self.servers_disponiveis)
        self.courses = ["Ciência da Computação (Matutino)", "Engenharia Mecânica (Matutino)",
                        "Engenharia Química (Matutino)"]
        self.connection_uris = ["PYRO:obj_4ee4540b8c6c445bbcf035807cefbe4a@192.168.1.2:30456",
                                "PYRO:obj_f7ddd4bf17144560b1188bed16496098@192.168.1.2:30496",
                                "PYRO:obj_48635ca9a9dc4e3c8567453f252113ec@192.168.1.2:30575"]

    def start(self):
        generation_chromosomes = []
        generation_chromosomes_to_send = [[] for _ in range(self.servers_disponiveis)]
        # initialValuesCC = [1, 3, 6, 9, 15, 14, 20, 21, 0, 0, 3, 2, 11, 11, 17, 16, 21, 70, 0, 0, 5, 1, 7, 12, 15, 13, 18, 70, 0, 0, 4, 4, 7, 10, 17, 14, 20, 19, 0, 0, 2, 5, 10, 8, 16, 13, 19, 18, 0, 0]
        # initialValuesEM = [27, 24, 29, 30, 36, 35, 47, 43, 48, 49, 24, 22, 31, 31, 37, 34, 40, 46, 71, 71, 26, 22, 28, 29, 34, 39, 44, 40, 71, 71, 23, 26, 28, 33, 39, 35, 47, 41, 71, 48, 23, 25, 32, 30, 38, 36, 42, 45, 71, 49]
        # initialValuesEQ = [50, 50, 62, 62, 69, 66, 0, 0, 0, 0, 51, 53, 56, 58, 65, 67, 0, 0, 0, 0, 53, 55, 60, 57, 64, 64, 0, 0, 0, 0, 55, 51, 61, 63, 68, 67, 0, 0, 0, 0, 54, 52, 59, 58, 66, 65, 0, 0, 0, 0]
        for course in self.courses:
            generation_count = 0
            # if course == "Engenharia Química (Matutino)":
            while generation_count < self.population_size:
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
                index_generation_send = generation_count // self.generation_length_to_send
                if index_generation_send  > self.servers_disponiveis - 1:
                    index_generation_send = self.servers_disponiveis -1
                generation_chromosomes_to_send[index_generation_send].append(chromosome)
                generation_count += 1

        new_generation_chromosomes = []
        uri_index = 0
        for subarray in generation_chromosomes_to_send:
            rating = Pyro5.api.Proxy(self.connection_uris[uri_index])
            serialized_chromosomes = pickle.dumps(subarray)
            new_generation_chromosome = pickle.loads(base64.b64decode(rating.rate(serialized_chromosomes)["data"]))
            new_generation_chromosomes.extend(new_generation_chromosome)
            uri_index += 1
        generation_chromosomes = copy.deepcopy(new_generation_chromosomes)

        count = 0
        outro_count = 0
        best_chromosome = []
        start_time = time.perf_counter()
        while count < 2000000:
            print("-------------------------------- Geração " + str(count) + " --------------------------------")
            grouped_chromosomes_by_course = {}
            generation_chromosomes_to_send = [[] for _ in range(self.servers_disponiveis)]
            for chromosome in generation_chromosomes:
                course = chromosome.course
                if course not in grouped_chromosomes_by_course:
                    grouped_chromosomes_by_course[course] = []
                grouped_chromosomes_by_course[course].append(chromosome)

            new_generation = []
            for course, course_chromosomes in grouped_chromosomes_by_course.items():
                elite_chromosomes = sorted(course_chromosomes, key=lambda x: x.avaliation, reverse=True)
                chosen_chromosomes = elite_chromosomes[:self.num_chromosomes_elitism]

                new_course_chromosomes = Crossover.cross(self.crossover_chance_percentage, course_chromosomes,
                                                         chosen_chromosomes,
                                                         course)

                Mutation.mutate(self.mutation_chance_percentage, new_course_chromosomes, course)

                if len(new_course_chromosomes) > self.population_size:
                    new_course_chromosomes = new_course_chromosomes[:self.population_size]
                new_generation.extend(new_course_chromosomes)

                start = 0
                end = self.generation_length_to_send
                index_generation_send = 0
                while index_generation_send < self.servers_disponiveis:
                    if index_generation_send == self.servers_disponiveis -1:
                        end = self.population_size
                    generation_chromosomes_to_send[index_generation_send].extend(new_course_chromosomes[start:end])
                    start = end
                    end += self.generation_length_to_send
                    index_generation_send += 1

            new_generation_chromosomes = []
            uri_index = 0
            for subarray in generation_chromosomes_to_send:
                rating = Pyro5.api.Proxy(self.connection_uris[uri_index])
                serialized_chromosomes = pickle.dumps(subarray)
                new_generation_chromosome = pickle.loads(base64.b64decode(rating.rate(serialized_chromosomes)["data"]))
                new_generation_chromosomes.extend(new_generation_chromosome)
                uri_index += 1

            generation_chromosomes = copy.deepcopy(new_generation_chromosomes)

            summed_chromosomes = []
            for index in range(len(grouped_chromosomes_by_course[generation_chromosomes[0].course])):
                full_chromosome = []
                for course, course_chromosomes in grouped_chromosomes_by_course.items():
                    full_chromosome.append(course_chromosomes[index])
                summed_chromosomes.append(((sum(chrom.avaliation for chrom in full_chromosome),full_chromosome)))

            sorted_summed_chromosomes = sorted(summed_chromosomes, key=lambda x: x[0], reverse=True)
            if sorted_summed_chromosomes[0][0] > (sum(chrom.avaliation for chrom in best_chromosome)):
                best_chromosome = copy.deepcopy(sorted_summed_chromosomes[0][1])
            if sorted_summed_chromosomes[0][0] >= 29900:
                outro_count += 1
            if sorted_summed_chromosomes[0][0] == 30000:
                break
            print("Melhor avaliação: " + str(sorted_summed_chromosomes[0][0]))

            if outro_count == 50:
                outro_count = 0
                new_random_population = self.population_size / 2
                generation_chromosomes_to_send = [[] for _ in range(self.servers_disponiveis)]

                for course, course_chromosomes in grouped_chromosomes_by_course.items():
                    new_course_chromosomes = []
                    index = 0
                    for chrom in course_chromosomes:
                        if index >= new_random_population:
                            chromosome = Chromosome(course, 10000, None)
                            chromosome.generateRandom()
                            generation_chromosomes[index] = chromosome
                            new_course_chromosomes.append(chromosome)
                        else:
                            new_course_chromosomes.append(chrom)
                        index += 1

                    start = 0
                    end = self.generation_length_to_send
                    index_generation_send = 0
                    while index_generation_send < self.servers_disponiveis:
                        if index_generation_send == self.servers_disponiveis -1:
                            end = self.population_size
                        generation_chromosomes_to_send[index_generation_send].extend(new_course_chromosomes[start:end])
                        start = end
                        end += self.generation_length_to_send
                        index_generation_send += 1

                new_generation_chromosomes = []
                uri_index = 0
                for subarray in generation_chromosomes_to_send:
                    rating = Pyro5.api.Proxy(self.connection_uris[uri_index])
                    serialized_chromosomes = pickle.dumps(subarray)
                    new_generation_chromosome = pickle.loads(
                        base64.b64decode(rating.rate(serialized_chromosomes)["data"]))
                    new_generation_chromosomes.extend(new_generation_chromosome)
                    uri_index += 1

                generation_chromosomes = copy.deepcopy(new_generation_chromosomes)
            count += 1

        print("Ababou cupinxa")
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Tempo total de execução: {elapsed_time:.2f} segundos")

        print("Melhor cromossomo")
        for chrom in best_chromosome:
            print(str(chrom.course) + " - " + str(chrom.values) + " evaluation: " +
                  str(chrom.avaliation))


if __name__ == "__main__":
    print("Iniciando Client do AG")
    solver = TimetablingResolver()
    solver.start()
