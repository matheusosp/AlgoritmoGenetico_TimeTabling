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
        self.population_size = 30
        self.num_chromosomes_elitism = 4
        self.crossover_chance_percentage = 70
        self.mutation_chance_percentage = 45
        self.courses = ["Ciência da Computação (Matutino)", "Engenharia Mecânica (Matutino)",
                        "Engenharia Química (Matutino)"]
        self.connection_uris = ["PYRO:obj_70cfe45528f14f919a224fac42600dc9@192.168.1.7:45069",
                                "PYRO:obj_4d0507b778154613a974755945d848c2@192.168.1.7:45099",
                                "PYRO:obj_059a466efb3c4c4b918b95a26297a077@192.168.1.7:45103"]
        self.servers_disponiveis = len(self.connection_uris)
        self.generation_length_to_send = int(self.population_size / self.servers_disponiveis)

    def start(self):
        generation_chromosomes = []
        generation_chromosomes_to_send = [[] for _ in range(self.servers_disponiveis)]
        for course in self.courses:
            generation_count = 0
            while generation_count < self.population_size:
                chromosome = Chromosome(course, 10000, None)
                chromosome.generateRandom()
                generation_chromosomes.append(chromosome)
                index_generation_send = generation_count // self.generation_length_to_send
                if index_generation_send > self.servers_disponiveis - 1:
                    index_generation_send = self.servers_disponiveis - 1
                generation_chromosomes_to_send[index_generation_send].append(chromosome)
                generation_count += 1

        new_generation_chromosomes = []
        grouped_chromosomes_by_course = {}
        summed_chromosomes = []
        uri_index = 0
        for subarray in generation_chromosomes_to_send:
            rating = Pyro5.api.Proxy(self.connection_uris[uri_index])
            serialized_chromosomes = pickle.dumps(subarray)
            res = pickle.loads(base64.b64decode(rating.rate(serialized_chromosomes)["data"]))
            new_generation_chromosomes.extend(res[0])
            for key, value in res[1].items():
                if key in grouped_chromosomes_by_course:
                    grouped_chromosomes_by_course[key].extend(value)
                else:
                    grouped_chromosomes_by_course[key] = value
            summed_chromosomes.extend(res[2])
            uri_index += 1

        count = 0
        outro_count = 0
        best_chromosome = []
        start_time = time.perf_counter()
        while count < 2000000:
            print("-------------------------------- Geração " + str(count) + " --------------------------------")

            generation_chromosomes_to_send = [[] for _ in range(self.servers_disponiveis)]
            new_generation = []
            for course, course_chromosomes in grouped_chromosomes_by_course.items():
                elite_chromosomes = sorted(course_chromosomes, key=lambda x: x.avaliation, reverse=True)
                chosen_chromosomes = elite_chromosomes[:self.num_chromosomes_elitism]

                new_course_chromosomes = Crossover.cross(self.crossover_chance_percentage, course_chromosomes,
                                                         chosen_chromosomes,
                                                         course)

                if len(new_course_chromosomes) > self.population_size:
                    new_course_chromosomes = new_course_chromosomes[:self.population_size]

                Mutation.mutate(self.mutation_chance_percentage, new_course_chromosomes, course,
                                self.num_chromosomes_elitism)
                new_generation.extend(new_course_chromosomes)

                start = 0
                end = self.generation_length_to_send
                index_generation_send = 0
                while index_generation_send < self.servers_disponiveis:
                    if index_generation_send == self.servers_disponiveis - 1:
                        end = self.population_size
                    generation_chromosomes_to_send[index_generation_send].extend(new_course_chromosomes[start:end])
                    start = end
                    end += self.generation_length_to_send
                    index_generation_send += 1

            new_generation_chromosomes = []
            grouped_chromosomes_by_course = {}
            summed_chromosomes = []
            uri_index = 0
            for subarray in generation_chromosomes_to_send:
                rating = Pyro5.api.Proxy(self.connection_uris[uri_index])
                serialized_chromosomes = pickle.dumps(subarray)
                res = pickle.loads(base64.b64decode(rating.rate(serialized_chromosomes)["data"]))
                new_generation_chromosomes.extend(res[0])
                for key, value in res[1].items():
                    if key in grouped_chromosomes_by_course:
                        grouped_chromosomes_by_course[key].extend(value)
                    else:
                        grouped_chromosomes_by_course[key] = value
                summed_chromosomes.extend(res[2])
                uri_index += 1

            sorted_summed_chromosomes = sorted(summed_chromosomes, key=lambda x: x[0], reverse=True)
            if sorted_summed_chromosomes[0][0] > (sum(chrom.avaliation for chrom in best_chromosome)):
                best_chromosome = copy.deepcopy(sorted_summed_chromosomes[0][1])
            if sorted_summed_chromosomes[0][0] >= 29900:
                outro_count += 1
            if sorted_summed_chromosomes[0][0] == 30000:
                break
            print("Melhor avaliação: " + str(sorted_summed_chromosomes[0][0]))

            # if outro_count == 60:
            #     outro_count = 0
            #     new_random_population = self.population_size / 2
            #     generation_chromosomes_to_send = [[] for _ in range(self.servers_disponiveis)]
            #
            #     for course, course_chromosomes in grouped_chromosomes_by_course.items():
            #         new_course_chromosomes = []
            #         index = 0
            #         for chrom in course_chromosomes:
            #             if index >= new_random_population:
            #                 chromosome = Chromosome(course, 10000, None)
            #                 chromosome.generateRandom()
            #                 new_course_chromosomes.append(chromosome)
            #             else:
            #                 new_course_chromosomes.append(chrom)
            #             index += 1
            #
            #         start = 0
            #         end = self.generation_length_to_send
            #         index_generation_send = 0
            #         while index_generation_send < self.servers_disponiveis:
            #             if index_generation_send == self.servers_disponiveis - 1:
            #                 end = self.population_size
            #             generation_chromosomes_to_send[index_generation_send].extend(new_course_chromosomes[start:end])
            #             start = end
            #             end += self.generation_length_to_send
            #             index_generation_send += 1

                # new_generation_chromosomes = []
                # grouped_chromosomes_by_course = {}
                # summed_chromosomes = []
                # uri_index = 0
                # for subarray in generation_chromosomes_to_send:
                #     rating = Pyro5.api.Proxy(self.connection_uris[uri_index])
                #     serialized_chromosomes = pickle.dumps(subarray)
                #     res = pickle.loads(base64.b64decode(rating.rate(serialized_chromosomes)["data"]))
                #     new_generation_chromosomes.extend(res[0])
                #     for key, value in res[1].items():
                #         if key in grouped_chromosomes_by_course:
                #             grouped_chromosomes_by_course[key].extend(value)
                #         else:
                #             grouped_chromosomes_by_course[key] = value
                #     summed_chromosomes.extend(res[2])
                #     uri_index += 1
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
