import random


class Mutation:
    def __init__(self):
        pass

    @staticmethod
    def mutate(probability, chromosomes,course):
        for chromosome in chromosomes:
            if random.randint(1, 100) <= probability:
                mutation_index = random.randint(0, 49)
                day = chromosome.get_chosen_day(mutation_index)
                phase = chromosome.get_chosen_phase(mutation_index + 1)
                disciplinas_disponiveis = (chromosome.matutinoRepository
                                           .get_disciplinas_por_curso_fase_e_dia(course, phase,
                                                                                 day))
                new_gene_value = 0
                if disciplinas_disponiveis:
                    ids_das_disciplinas = [disciplina['id'] for disciplina in disciplinas_disponiveis]
                    id_aleatorio = random.choice(ids_das_disciplinas)
                    new_gene_value = id_aleatorio
                chromosome.values[mutation_index] = new_gene_value