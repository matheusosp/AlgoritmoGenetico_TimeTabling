from MatutinoRepository import MatutinoRepository
from ProfessorRepository import ProfessorRepository


class Rating:
    def __init__(self):
        self.matutinoRepository = MatutinoRepository()
        self.professorRepository = ProfessorRepository()

    def rate(self, chromosome):

        # Demérito: Professor Indisponível -5
        avaliation = self.teacher_is_unavailable(chromosome, chromosome.avaliation)

        # Demérito: Choque de horario Professor -10
        avaliation = self.schedule_conflict(chromosome, avaliation)

        # Demérito: Turma sem alguma disciplina -30
        avaliation = self.check_workload(chromosome, avaliation)

        # Demérito: Turma com aula em fase que não existe no curso -10
        # avaliation = self.check_days_without_classes(chromosome, avaliation)

        # Demérito: Turma com aula desnecessaria durante a semana -10 (quando não tem CH suficiente para todos os dias)
        # avaliation = self.check_days_without_classes(chromosome, avaliation)

        chromosome.avaliation = avaliation
        chromosome.was_evaluated = True

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

    def schedule_conflict(self, chromosome, avaliation):
        genes_groupedby_period = self.group_genes_by_day_and_period(chromosome)
        for period,period_value in genes_groupedby_period.items():
            # print(period)
            for day,day_values in period_value.items():
                # print(day)
                professor_set = set()
                for gene, professor in day_values:
                    if professor is not None and professor in professor_set:
                        avaliation -= 10
                    professor_set.add(professor)

        return avaliation

    def check_workload(self, chromosome, avaliation):
        course = "Ciência da Computação (Matutino)"
        for phase in ["2", "4", "6", "8", "10"]:
            required_disciplines = self.matutinoRepository.getDisciplinesByPhaseAndCourse(course, phase)

            for discipline in required_disciplines:
                required_ch = discipline["CH"]
                count = chromosome.values.count(discipline["id"])

                # Calcula o número esperado de genes com base na carga horária
                expected_genes = required_ch // 40

                if count == expected_genes:
                    continue

                # Calcula a penalização com base na diferença entre os genes encontrados e os esperados
                penalty = abs(count - expected_genes) * 30
                avaliation -= penalty

        return avaliation

    def check_days_without_classes(self, chromosome, avaliation):
        course = "Ciência da Computação (Matutino)"
        available_phases = list(self.matutinoRepository.courses.get(course, {}).keys())

        for phase_index, gene in enumerate(chromosome.values):
            phase = chromosome.get_chosen_phase(phase_index + 1)
            if phase not in available_phases:
                if gene != 0:
                    avaliation -= 10

        return avaliation

    def group_genes_by_day_and_period(self, chromosome):
        grouped_genes = {
            "8h-10h": {"1": [], "2": [], "3": [], "4": [], "5": []},
            "10h-12h": {"1": [], "2": [], "3": [], "4": [], "5": []}
        }

        for i, gene in enumerate(chromosome.values):
            gene_day = chromosome.get_chosen_day(i)
            gene_period = chromosome.get_period(i + 1)
            professor = self.matutinoRepository.getTeacherByDisciplineId(gene)

            if gene_period and gene_day:
                grouped_genes[gene_period][str(gene_day)].append((gene,professor))

        return grouped_genes

    def unnecessary_classes_during_the_week(self, chromosome, avaliation):
        course = "Ciência da Computação (Matutino)"
        for phase in ["2", "4", "6", "8", "10"]:
            required_disciplines = self.matutinoRepository.getDisciplinesByPhaseAndCourse(course, phase)
            total_required_hours = sum(discipline["CH"] for discipline in required_disciplines)
            total_assigned_hours = sum(chromosome.values.count(discipline["id"]) * 40 for discipline in required_disciplines)

            if total_assigned_hours > total_required_hours:
                # Há aulas desnecessárias durante a semana
                excess_hours = total_assigned_hours - total_required_hours
                avaliation -= 10 * (excess_hours // 80)  # Deduz 10 pontos para cada dia com aulas desnecessárias

        return avaliation
