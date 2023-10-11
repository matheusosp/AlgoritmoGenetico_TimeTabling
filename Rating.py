import base64
import pickle
import socket

import Pyro5.api

from Chromosome import Chromosome
from MatutinoRepository import MatutinoRepository
from ProfessorRepository import ProfessorRepository


@Pyro5.api.expose
class Rating(object):
    def __init__(self):
        self.matutinoRepository = MatutinoRepository()
        self.professorRepository = ProfessorRepository()

    def rate(self, data):
        decoded_bytes = base64.b64decode(data["data"])
        generation_chromosomes = pickle.loads(decoded_bytes)

        chromosome: Chromosome
        for chromosome in generation_chromosomes:
            chromosome.avaliation = 10000
            avaliation = 10000

            # Demérito: Professor Indisponível -5
            avaliation = self.teacher_is_unavailable(chromosome, chromosome.avaliation)
            # Demérito: Turma sem alguma disciplina -30
            avaliation = self.check_workload(chromosome, avaliation, chromosome.course)

            chromosome.avaliation = avaliation

        # Demérito: Choque de horario Professor -50
        self.schedule_conflict(generation_chromosomes)

        grouped_chromosomes_by_course = self.get_grouped_chromosomes(generation_chromosomes)
        summed_chromosomes = self.get_summed_chromosomes(grouped_chromosomes_by_course,len(grouped_chromosomes_by_course[generation_chromosomes[0].course]))

        return pickle.dumps((generation_chromosomes, grouped_chromosomes_by_course, summed_chromosomes))

    def get_summed_chromosomes(self, grouped_chromosomes_by_course, population_size):
        summed_chromosomes = []
        for index in range(population_size):
            full_chromosome = []
            for course, course_chromosomes in grouped_chromosomes_by_course.items():
                full_chromosome.append(course_chromosomes[index])
            summed_chromosomes.append((sum(chrom.avaliation for chrom in full_chromosome), full_chromosome))

        return summed_chromosomes

    def get_grouped_chromosomes(self, generation_chromosomes):
        grouped_chromosomes_by_course = {}
        for chromosome in generation_chromosomes:
            course = chromosome.course
            if course not in grouped_chromosomes_by_course:
                grouped_chromosomes_by_course[course] = []
            grouped_chromosomes_by_course[course].append(chromosome)

        return grouped_chromosomes_by_course

    def teacher_is_unavailable(self, chromosome, avaliation):
        count = 0
        for gene in chromosome.values:
            if gene != 0:
                teacher = self.matutinoRepository.getTeacherByDisciplineId(gene)
                dia = (chromosome.get_chosen_day(count))
                unavailable = self.professorRepository.teacher_work_inday(teacher, dia)
                if unavailable:
                    avaliation -= 5
            count += 1
        return avaliation

    def schedule_conflict(self, generation_chromosomes):
        professors_all_days_generations = self.get_professors_by_weekday(generation_chromosomes)
        for professors_all_days in professors_all_days_generations:
            for day in professors_all_days:
                for period in professors_all_days[day]:
                    professors = professors_all_days[day][period]["professores"]
                    unique_professors = set()

                    for teacher, chromosome in professors:
                        if teacher in unique_professors:
                            chromosome.avaliation -= 50
                        else:
                            unique_professors.add(teacher)

    def check_workload(self, chromosome, avaliation, course):
        for phase in ["2", "4", "6", "8", "10"]:
            required_disciplines = self.matutinoRepository.getDisciplinesByPhaseAndCourse(course, phase)

            for discipline in required_disciplines:
                required_ch = discipline["CH"]
                count = chromosome.values.count(discipline["id"])

                expected_genes = required_ch // 40
                if count == expected_genes:
                    continue

                penalty = abs(count - expected_genes) * 30
                avaliation -= penalty

        return avaliation

    def get_professors_by_weekday(self, generation_chromosomes):
        grouped_chromosomes_by_course = self.group_genes_by_course(generation_chromosomes)
        generation_full_chromosomes = self.group_full_chromosomes(generation_chromosomes, grouped_chromosomes_by_course)

        schedule_by_weekday_array = []
        for full_chromosomes in generation_full_chromosomes:
            schedule_by_weekday = {
                1: {
                    "8h-10h": {"professores": []},
                    "10h-12h": {"professores": []},
                },
                2: {
                    "8h-10h": {"professores": []},
                    "10h-12h": {"professores": []},
                },
                3: {
                    "8h-10h": {"professores": []},
                    "10h-12h": {"professores": []},
                },
                4: {
                    "8h-10h": {"professores": []},
                    "10h-12h": {"professores": []},
                },
                5: {
                    "8h-10h": {"professores": []},
                    "10h-12h": {"professores": []},
                },
            }
            for partial_chromosome in full_chromosomes:
                count = 0
                for gene in partial_chromosome.values:
                    if gene != 0:
                        teacher = self.matutinoRepository.getTeacherByDisciplineId(gene)
                        dia = (partial_chromosome.get_chosen_day(count))
                        period = partial_chromosome.get_period(count + 1)
                        schedule_by_weekday[dia][period]["professores"].append((teacher, partial_chromosome))
                    count += 1
            schedule_by_weekday_array.append(schedule_by_weekday.copy())

        return schedule_by_weekday_array

    def group_full_chromosomes(self, generationChromosomes, grouped_chromosomes_by_course):
        generation_full_chromosomes = []
        for index in range(len(grouped_chromosomes_by_course[generationChromosomes[0].course])):
            full_chromosome = []
            for course, course_chromosomes in grouped_chromosomes_by_course.items():
                full_chromosome.append(course_chromosomes[index])
            generation_full_chromosomes.append(full_chromosome)
        return generation_full_chromosomes

    def group_genes_by_course(self, generation_chromosomes):
        grouped_chromosomes_by_course = {}
        for chromosome in generation_chromosomes:
            course = chromosome.course
            if course not in grouped_chromosomes_by_course:
                grouped_chromosomes_by_course[course] = []
            grouped_chromosomes_by_course[course].append(chromosome)

        return grouped_chromosomes_by_course


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()

    print("Running RMI server...")
    server = Pyro5.api.Daemon(host=IP)
    uri = server.register(Rating)
    print(f"Server URI: {uri}")
    server.requestLoop()
    print("\tWaiting requests...")
