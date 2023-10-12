from MatutinoRepository import MatutinoRepository
from ProfessorRepository import ProfessorRepository
from VespertinoRepository import VespertinoRepository


class DisciplinasRepository:
    def __init__(self, isMatutino):
        self.professor_repository = ProfessorRepository(isMatutino)
        self.courses = {}
        self.isMatutino = isMatutino
        if isMatutino:
            self.courses = MatutinoRepository.get_courses()
        else:
            self.courses = VespertinoRepository.get_courses()
    def getDisicplinaByGene(self, gene):
        for course_name, semesters in self.courses.items():
            for semester, disciplines in semesters.items():
                for discipline in disciplines:
                    if discipline["id"] == gene:
                        return discipline

        return None

    def get_fases_disponiveis_por_curso(self, curso):
        if curso in self.courses:
            return list(self.courses[curso].keys())
        else:
            return []

    def get_disciplinas_por_curso_fase_e_dia(self, curso, fase, dia):
        disciplinas_disponiveis = []
        if curso in self.courses and fase in self.courses[curso] and dia in range(1, 6):
            for disciplina in self.courses[curso][fase]:
                professor = disciplina["Professor"]
                horario_professor = self.professor_repository.get_schedule(professor)
                if horario_professor and horario_professor[dia - 1][1] != "x":
                    disciplinas_disponiveis.append(disciplina)

        return disciplinas_disponiveis

    def getDisciplinesByPhaseAndCourse(self, course, phase):
        if course in self.courses and phase in self.courses[course]:
            return self.courses[course][phase]
        else:
            return []

    def getTeacherByDisciplineId(self, discipline_id):
        for course_name, semesters in self.courses.items():
            for semester, disciplines in semesters.items():
                for discipline in disciplines:
                    if discipline["id"] == discipline_id:
                        return discipline["Professor"]
        return None

    def get_disciplinas_por_curso(self, curso):
        disciplinas_curso = []
        if curso in self.courses:
            for fase, disciplinas in self.courses[curso].items():
                disciplinas_curso.extend(disciplinas)
        return disciplinas_curso

    def get_disciplinas_faltantes_no_cromossomo(self, cromossomo, curso, fase):
        disciplinas_faltantes = []
        required_disciplines = self.getDisciplinesByPhaseAndCourse(curso, fase)

        for discipline in required_disciplines:
            required_ch = discipline["CH"]
            count = cromossomo.count(discipline["id"])

            expected_genes = required_ch // 40
            if count < expected_genes:
                disciplinas_faltantes.append(discipline["id"])

        return disciplinas_faltantes

    def get_genes_com_excesso_de_carga_horaria(self, cromossomo, curso, fase):
        genes_com_excesso = []
        required_disciplines = self.getDisciplinesByPhaseAndCourse(curso, fase)

        for discipline in required_disciplines:
            required_ch = discipline["CH"]
            all_genes_disciplina = [gene for gene in cromossomo if gene[1] == discipline["id"]]
            count = len(all_genes_disciplina)

            expected_genes = required_ch // 40
            if count > expected_genes:
                genes_com_excesso.extend([gene[0] for gene in all_genes_disciplina])

        return genes_com_excesso


if __name__ == "__main__":
    repo = DisciplinasRepository(True)
