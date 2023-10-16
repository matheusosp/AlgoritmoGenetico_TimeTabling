import base64
import copy
import csv
import multiprocessing
import pickle
import socket
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
        self.courses = None
        self.connection_uris = self.request_string_list("192.168.1.7",8888).split('\n')
        self.servers_disponiveis = len(self.connection_uris)
        self.generation_length_to_send = int(self.population_size / self.servers_disponiveis)

    def request_string_list(self, server_host, server_port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_host, server_port))

        client.send("GET_LIST".encode('utf-8'))
        response = client.recv(4096).decode('utf-8')
        client.close()

        return response

    def start(self, isMatutino, courses, show_print):
        self.courses = courses
        generation_chromosomes_to_send = [[] for _ in range(self.servers_disponiveis)]
        # test1 = [1, 1, 8, 8, 14, 14, 20, 20, 0, 0, 5, 4, 12, 13, 17, 16, 23, 25, 0, 0, 2, 7, 9, 11, 15, 17, 21, 22, 0, 0, 2, 5, 13, 10, 18, 19, 22, 24, 0, 0, 6, 3, 9, 12, 16, 17, 22, 21, 0, 0]
        # test2 = [26, 26, 33, 33, 40, 40, 49, 49, 0, 0, 28, 29, 37, 35, 43, 44, 55, 54, 0, 0, 30, 27, 38, 39, 46, 47, 55, 53, 0, 0, 31, 32, 36, 35, 45, 48, 52, 50, 0, 0, 27, 29, 34, 37, 42, 41, 51, 50, 0, 0]
        # test3 = [56, 56, 61, 61, 66, 66, 71, 71, 0, 0, 60, 58, 65, 63, 69, 70, 74, 73, 0, 0, 57, 58, 65, 64, 67, 70, 72, 76, 0, 0, 57, 59, 64, 62, 69, 68, 73, 75, 0, 0, 60, 59, 63, 62, 68, 67, 72, 75, 0, 0]
        for course in self.courses:
            generation_count = 0
            while generation_count < self.population_size:
                # if generation_count == 0 and course == "Técnico em Informática para Internet (Vespertino)":
                #     chromosome = Chromosome(course,isMatutino,10000, test1)
                # elif generation_count == 0 and course == "Técnico em Mecatrônica (Vespertino)":
                #     chromosome = Chromosome(course, isMatutino,10000, test2)
                # elif generation_count == 0 and course == "Técnico em Administração (Vespertino)":
                #     chromosome = Chromosome(course, isMatutino,10000, test3)
                # else:
                chromosome = Chromosome(course, isMatutino, 10000, None)
                chromosome.generateRandom()
                index_generation_send = generation_count // self.generation_length_to_send
                if index_generation_send > self.servers_disponiveis - 1:
                    index_generation_send = self.servers_disponiveis - 1
                generation_chromosomes_to_send[index_generation_send].append(chromosome)
                generation_count += 1

        grouped_chromosomes_by_course, summed_chromosomes = self.apply_rate(generation_chromosomes_to_send)

        count = 0
        outro_count = 0
        best_chromosome = []
        sorted_summed_chromosomes = sorted(summed_chromosomes, key=lambda x: x[0], reverse=True)
        if sorted_summed_chromosomes[0][0] > (sum(chrom.avaliation for chrom in best_chromosome)):
            best_chromosome = copy.deepcopy(sorted_summed_chromosomes[0][1])
        if sorted_summed_chromosomes[0][0] == 30000:
            count = 2000000
        # start_time = time.perf_counter()
        while count < 2000000:
            if show_print:
                print("-------------------------------- Geração " + str(count) + " --------------------------------")

            generation_chromosomes_to_send = [[] for _ in range(self.servers_disponiveis)]
            new_generation = []
            for course, course_chromosomes in grouped_chromosomes_by_course.items():
                elite_chromosomes = sorted(course_chromosomes, key=lambda x: x.avaliation, reverse=True)
                chosen_chromosomes = elite_chromosomes[:self.num_chromosomes_elitism]

                new_course_chromosomes = Crossover.cross(self.crossover_chance_percentage, course_chromosomes,
                                                         chosen_chromosomes, course, isMatutino)

                if len(new_course_chromosomes) > self.population_size:
                    new_course_chromosomes = new_course_chromosomes[:self.population_size]

                Mutation.mutate(self.mutation_chance_percentage, new_course_chromosomes, course,
                                self.num_chromosomes_elitism)
                new_generation.extend(new_course_chromosomes)

                self.update_generation_chromosomes_to_send(generation_chromosomes_to_send, new_course_chromosomes)

            grouped_chromosomes_by_course, summed_chromosomes = self.apply_rate(generation_chromosomes_to_send)

            sorted_summed_chromosomes = sorted(summed_chromosomes, key=lambda x: x[0], reverse=True)
            if sorted_summed_chromosomes[0][0] > (sum(chrom.avaliation for chrom in best_chromosome)):
                best_chromosome = copy.deepcopy(sorted_summed_chromosomes[0][1])
            if sorted_summed_chromosomes[0][0] >= 29900:
                outro_count += 1
            if sorted_summed_chromosomes[0][0] == 30000:
                break
            if show_print:
                print("Melhor avaliação: " + str(sorted_summed_chromosomes[0][0]))

            if outro_count == 1000:
                outro_count = 0
                new_random_population = self.population_size / 2
                generation_chromosomes_to_send = [[] for _ in range(self.servers_disponiveis)]

                for course, course_chromosomes in grouped_chromosomes_by_course.items():
                    new_course_chromosomes = []
                    index = 0
                    for chrom in course_chromosomes:
                        if index >= new_random_population:
                            chromosome = Chromosome(course, isMatutino, 10000, None)
                            chromosome.generateRandom()
                            new_course_chromosomes.append(chromosome)
                        else:
                            new_course_chromosomes.append(chrom)
                        index += 1

                    self.update_generation_chromosomes_to_send(generation_chromosomes_to_send, new_course_chromosomes)

                grouped_chromosomes_by_course, summed_chromosomes = self.apply_rate(generation_chromosomes_to_send)
            count += 1

        print("Ababou cupinxa")
        # end_time = time.perf_counter()
        # elapsed_time = end_time - start_time
        # print(f"Tempo total de execução: {elapsed_time:.2f} segundos")
        print("Melhor cromossomo")
        for chrom in best_chromosome:
            print(str(chrom.course) + " - " + str(chrom.values) + " evaluation: " +
                  str(chrom.avaliation))

        types_filenames = ["horarios_professores", "horarios_disciplinas"]
        type_professor = True
        for filename in types_filenames:
            if isMatutino:
                turno = "_(Matutino).csv"
            else:
                turno = "_(Vespertino).csv"
            filename += turno
            self.save_best_chromosome_to_csv(best_chromosome, filename, type_professor)
            type_professor = False

    def update_generation_chromosomes_to_send(self, generation_chromosomes_to_send, new_course_chromosomes):
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

    def apply_rate(self, generation_chromosomes_to_send):
        grouped_chromosomes_by_course = {}
        summed_chromosomes = []
        uri_index = 0
        for subarray in generation_chromosomes_to_send:
            rating = Pyro5.api.Proxy(self.connection_uris[uri_index])
            serialized_chromosomes = pickle.dumps(subarray)
            res = pickle.loads(base64.b64decode(rating.rate(serialized_chromosomes)["data"]))
            for key, value in res[1].items():
                if key in grouped_chromosomes_by_course:
                    grouped_chromosomes_by_course[key].extend(value)
                else:
                    grouped_chromosomes_by_course[key] = value
            summed_chromosomes.extend(res[2])
            uri_index += 1
        return grouped_chromosomes_by_course, summed_chromosomes

    def run_with_matutino(self):
        coursesMatutino = ["Ciência da Computação (Matutino)", "Engenharia Mecânica (Matutino)",
                           "Engenharia Química (Matutino)"]
        self.start(True, coursesMatutino,True)

    def run_without_matutino(self):
        coursesVespertino = ["Técnico em Informática para Internet (Vespertino)", "Técnico em Mecatrônica (Vespertino)",
                             "Técnico em Administração (Vespertino)"]
        self.start(False, coursesVespertino,True)

    def save_best_chromosome_to_csv(self, best_chromosome, filename, type_professor):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')

            chrom: Chromosome
            for chrom in best_chromosome:
                course = chrom.course
                writer.writerow([course])
                writer.writerow(['', '', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'])

                fases_disponiveis = chrom.disciplinasRepository.get_fases_disponiveis_por_curso(course)
                for fase in fases_disponiveis:
                    periods = ["8h-10h", "10h-12h"]
                    for period in periods:
                        if type_professor:
                            chromosome_by_phase_and_period = chrom.get_genes_professor_by_period_and_phase(period, fase)
                        else:
                            chromosome_by_phase_and_period = chrom.get_genes_disciplinas_by_period_and_phase(period,
                                                                                                             fase)
                        row = [fase + "a fase", period]
                        row.extend(chromosome_by_phase_and_period)
                        writer.writerow(row)


if __name__ == "__main__":
    print("Iniciando Client do AG")
    solver = TimetablingResolver()

    process_matutino = multiprocessing.Process(target=solver.run_with_matutino)
    process_vespertino = multiprocessing.Process(target=solver.run_without_matutino)

    start_time = time.perf_counter()

    process_matutino.start()
    process_vespertino.start()

    process_matutino.join()
    process_vespertino.join()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Tempo total de execução: {elapsed_time:.2f} segundos")
