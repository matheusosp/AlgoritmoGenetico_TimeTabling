import random

from DisciplinasRepository import DisciplinasRepository


class Chromosome:
    def __init__(self, course, isMatutino, avaliation=100, values=None):
        if values is None:
            values = []
        self.values = values
        self.course = course
        self.avaliation = avaliation
        self.isMatutino = isMatutino
        self.disciplinasRepository = DisciplinasRepository(isMatutino)

    def generateRandom(self):
        for i in range(50):
            dia_escolhido = self.get_chosen_day(i)
            fase_escolhida = self.get_chosen_phase(i + 1)
            disciplinas_disponiveis = (self.disciplinasRepository
                                       .get_disciplinas_por_curso_fase_e_dia(self.course, fase_escolhida,
                                                                             dia_escolhido))
            if disciplinas_disponiveis:
                ids_das_disciplinas = [disciplina['id'] for disciplina in disciplinas_disponiveis]
                id_aleatorio = random.choice(ids_das_disciplinas)
                self.values.append(id_aleatorio)
            else:
                self.values.append(0)

    def get_chosen_phase(self, i):
        fase_escolhida = "0"
        if self.isMatutino:
            if i in (1, 2, 11, 12, 21, 22, 31, 32, 41, 42):
                fase_escolhida = "2"
            if i in (3, 4, 13, 14, 23, 24, 33, 34, 43, 44):
                fase_escolhida = "4"
            if i in (5, 6, 15, 16, 25, 26, 35, 36, 45, 46):
                fase_escolhida = "6"
            if i in (7, 8, 17, 18, 27, 28, 37, 38, 47, 48):
                fase_escolhida = "8"
            if i in (9, 10, 19, 20, 29, 30, 39, 40, 49, 50):
                fase_escolhida = "10"
        else:
            if i in (1, 2, 11, 12, 21, 22, 31, 32, 41, 42):
                fase_escolhida = "1"
            if i in (3, 4, 13, 14, 23, 24, 33, 34, 43, 44):
                fase_escolhida = "2"
            if i in (5, 6, 15, 16, 25, 26, 35, 36, 45, 46):
                fase_escolhida = "3"
            if i in (7, 8, 17, 18, 27, 28, 37, 38, 47, 48):
                fase_escolhida = "4"
            if i in (9, 10, 19, 20, 29, 30, 39, 40, 49, 50):
                fase_escolhida = "5"
        return fase_escolhida

    def get_period(self, index):
        if index in (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49):
            return "8h-10h"
        elif index in (2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50):
            return "10h-12h"
        return None

    def getDisciplineNamebyGene(self, gene):
        if gene == 0:
            return "Sem Aula"
        discipline_Name = self.disciplinasRepository.getDisicplinaByGene(gene)

        return discipline_Name['Disciplina']

    def getProfessorbyGene(self, gene):
        if gene == 0:
            return "Sem Aula"
        professor = self.disciplinasRepository.getDisicplinaByGene(gene)["Professor"]

        return professor

    def get_genes_by_phase(self, phase):
        genes_in_phase = []
        for i in range(len(self.values)):
            gene_phase = self.get_chosen_phase(i + 1)
            if gene_phase == phase:
                genes_in_phase.append((i, self.values[i]))
        return genes_in_phase

    def get_genes_disciplinas_by_period_and_phase(self, period, phase):
        genes_in_period_and_phase = []
        for i in range(len(self.values)):
            gene_period = self.get_period(i + 1)
            gene_phase = self.get_chosen_phase(i + 1)
            if gene_period == period and gene_phase == phase:
                genes_in_period_and_phase.append(self.getDisciplineNamebyGene(self.values[i]))
        return genes_in_period_and_phase

    def get_genes_professor_by_period_and_phase(self, period, phase):
        genes_in_period_and_phase = []
        for i in range(len(self.values)):
            gene_period = self.get_period(i + 1)
            gene_phase = self.get_chosen_phase(i + 1)
            if gene_period == period and gene_phase == phase:
                genes_in_period_and_phase.append(self.getProfessorbyGene(self.values[i]))
        return genes_in_period_and_phase

    def set_values(self, values):
        self.values = values

    @staticmethod
    def get_chosen_day(number):
        if 0 <= number <= 9:
            return 1
        elif 10 <= number <= 19:
            return 2
        elif 20 <= number <= 29:
            return 3
        elif 30 <= number <= 39:
            return 4
        elif 40 <= number <= 49:
            return 5
