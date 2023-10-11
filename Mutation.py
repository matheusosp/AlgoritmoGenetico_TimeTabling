import random


class Mutation:
    def __init__(self):
        pass

    @staticmethod
    def mutate(probability, chromosomes,course, num_elitism):
        count = 0
        for chromosome in chromosomes:
            if random.randint(1, 100) <= probability:
                mutation_index = random.randint(0, 49)
                if count < num_elitism:
                    fases_disponiveis = chromosome.matutinoRepository.get_fases_disponiveis_por_curso(course)
                    for fase in fases_disponiveis:
                        chromosome_by_phase = chromosome.get_genes_by_phase(fase)
                        mutation_index_com_excesso = chromosome.matutinoRepository.get_genes_com_excesso_de_carga_horaria(
                            chromosome_by_phase, course, fase)
                        if len(mutation_index_com_excesso) > 0:
                            mutation_index = random.choice(mutation_index_com_excesso)
                day = chromosome.get_chosen_day(mutation_index)
                phase = chromosome.get_chosen_phase(mutation_index + 1)
                disciplinas_disponiveis = (chromosome.matutinoRepository
                                           .get_disciplinas_por_curso_fase_e_dia(course, phase,day))

                chromosome_by_phase = chromosome.get_genes_by_phase(phase)
                disciplinas_faltantes = (chromosome.matutinoRepository
                                         .get_disciplinas_faltantes_no_cromossomo([gene [1] for gene in chromosome_by_phase],course, phase))

                new_gene_value = 0

                ids_das_disciplinas = [disciplina['id'] for disciplina in disciplinas_disponiveis]
                if disciplinas_disponiveis:
                    id_aleatorio = random.choice(ids_das_disciplinas)
                    new_gene_value = id_aleatorio

                if len(disciplinas_faltantes) != 0:
                    id_aleatorio = random.choice(disciplinas_faltantes)
                    if id_aleatorio in ids_das_disciplinas:
                        new_gene_value = id_aleatorio
                        mutation_index_com_excesso = chromosome.matutinoRepository.get_genes_com_excesso_de_carga_horaria(
                            chromosome_by_phase, course, phase)
                        mutation_index = random.choice(mutation_index_com_excesso)
                chromosome.values[mutation_index] = new_gene_value
            count += 1