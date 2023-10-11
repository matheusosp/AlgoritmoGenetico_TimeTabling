from ProfessorRepository import ProfessorRepository


class MatutinoRepository:
    def __init__(self):
        self.professor_repository = ProfessorRepository()
        self.courses = {
            "Ciência da Computação (Matutino)": {
                "2": [
                    {
                        "Disciplina": "Programação Orientada a Objetos",
                        "CH": 80,
                        "Professor": "Alexandre Perin de Souza",
                        "id":1
                    },
                    {
                        "Disciplina": "Arquitetura e Organização de Computadores",
                        "CH": 80,
                        "Professor": "Robson Costa",
                        "id": 2
                    },
                    {
                        "Disciplina": "Linguagens e Paradigmas de Programação",
                        "CH": 80,
                        "Professor": "Wilson Castello Branco Neto",
                        "id": 3
                    },
                    {
                        "Disciplina": "Álgebra Linear e Geometria Analítica",
                        "CH": 80,
                        "Professor": "Vilma Gisele Karsburg",
                        "id": 4
                    },
                    {
                        "Disciplina": "Introdução à Redes de Computadores",
                        "CH": 80,
                        "Professor": "Robson Costa",
                        "id": 5
                    },
                ],
                "4": [
                    {
                        "Disciplina": "Grafos",
                        "CH": 40,
                        "Professor": "Wilson Castello Branco Neto",
                        "id": 6
                    },
                    {
                        "Disciplina": "Fundamentos de Bancos de Dados",
                        "CH": 80,
                        "Professor": "Fabio Aiub Sperotto",
                        "id": 7
                    },
                    {
                        "Disciplina": "Teoria da Computação",
                        "CH": 40,
                        "Professor": "Wilson Castello Branco Neto",
                        "id": 8
                    },
                    {
                        "Disciplina": "Teoria da Computação",
                        "CH": 40,
                        "Professor": "Alexandre Perin de Souza",
                        "id": 9
                    },
                    {
                        "Disciplina": "Introdução à Engenharia de Software",
                        "CH": 80,
                        "Professor": "Alexandre Perin de Souza",
                        "id": 10
                    },
                    {
                        "Disciplina": "Cálculo Numérico",
                        "CH": 80,
                        "Professor": "Vilma Gisele Karsburg",
                        "id": 11
                    },
                    {
                        "Disciplina": "Informática e Sociedade",
                        "CH": 40,
                        "Professor": "Fernando Weber Albiero",
                        "id": 12
                    },
                ],
                "6": [
                    {
                        "Disciplina": "Computação Gráfica",
                        "CH": 80,
                        "Professor": "Vilson Heck Junior",
                        "id": 13
                    },
                    {
                        "Disciplina": "Segurança Computacional",
                        "CH": 80,
                        "Professor": "Robson Costa",
                        "id": 14
                    },
                    {
                        "Disciplina": "Eletiva I",
                        "CH": 80,
                        "Professor": "Carlos Andres Ferrero",
                        "id": 15
                    },
                    {
                        "Disciplina": "Inteligência Artificial",
                        "CH": 80,
                        "Professor": "Wilson Castello Branco Neto",
                        "id": 16
                    },
                    {
                        "Disciplina": "Sistemas Distribuídos",
                        "CH": 80,
                        "Professor": "Robson Costa",
                        "id": 17
                    },
                ],
                "8": [
                    {
                        "Disciplina": "Trabalho de Conclusão de Curso",
                        "CH": 80,
                        "Professor": "Alexandre Perin de Souza",
                        "id": 18
                    },
                    {
                        "Disciplina": "Trabalho de Conclusão de Curso (Orientador)",
                        "CH": 80,
                        "Professor": "Orientador",
                        "id": 70
                    },
                    {
                        "Disciplina": "Eletiva III",
                        "CH": 80,
                        "Professor": "Vilson Heck Junior",
                        "id": 19
                    },
                    {
                        "Disciplina": "Eletiva IV",
                        "CH": 80,
                        "Professor": "Fernando Weber Albiero",
                        "id": 20
                    },
                    {
                        "Disciplina": "Gerência de Projetos",
                        "CH": 80,
                        "Professor": "Leonardo Bravo Estacio",
                        "id": 21
                    },
                ],
            },
            "Engenharia Mecânica (Matutino)": {
                "2": [
                    {
                        "Disciplina": "Cálculo II",
                        "CH": 80,
                        "Professor": "Ailton Durigon",
                        "id": 22
                    },
                    {
                        "Disciplina": "Álgebra Linear",
                        "CH": 80,
                        "Professor": "Juliana Mercedes Rheinheimer",
                        "id": 23
                    },
                    {
                        "Disciplina": "Física I",
                        "CH": 80,
                        "Professor": "Eliana Fernandes Borragini",
                        "id": 24
                    },
                    {
                        "Disciplina": "Estatística e Probabilidade",
                        "CH": 40,
                        "Professor": "Vilma Gisele Karsburg",
                        "id": 25
                    },
                    {
                        "Disciplina": "Desenho Técnico II",
                        "CH": 80,
                        "Professor": "Natalia Madalena Boelter",
                        "id": 26
                    },
                    {
                        "Disciplina": "Comunicação e Expressão",
                        "CH": 40,
                        "Professor": "Paula Clarice Santos G. de Jesus",
                        "id": 27
                    },
                ],
                "4": [
                    {
                        "Disciplina": "Cálculo IV",
                        "CH": 80,
                        "Professor": "Ailton Durigon",
                        "id": 28
                    },
                    {
                        "Disciplina": "Física III",
                        "CH": 80,
                        "Professor": "Eliana Fernandes Borragini",
                        "id": 29
                    },
                    {
                        "Disciplina": "Termodinâmica",
                        "CH": 80,
                        "Professor": "Matheus Fontanelle Pereira",
                        "id": 30
                    },
                    {
                        "Disciplina": "Mecânica dos Sólidos",
                        "CH": 80,
                        "Professor": "Anderson Luis Garcia Correia",
                        "id": 31
                    },
                    {
                        "Disciplina": "Ciência e Tecnologia dos Materiais",
                        "CH": 40,
                        "Professor": "Rafael Gustavo Schreiber",
                        "id": 32
                    },
                    {
                        "Disciplina": "Metrologia",
                        "CH": 40,
                        "Professor": "Ricardo Teran Muhl",
                        "id": 33
                    },
                ],
                "6": [
                    {
                        "Disciplina": "Transferência de Calor",
                        "CH": 80,
                        "Professor": "Matheus Fontanelle Pereira",
                        "id": 34
                    },
                    {
                        "Disciplina": "Mecanismos",
                        "CH": 80,
                        "Professor": "Anderson Luis Garcia Correia",
                        "id": 35
                    },
                    {
                        "Disciplina": "Elementos de Máquina I",
                        "CH": 80,
                        "Professor": "Rafael Gustavo Schreiber",
                        "id": 36
                    },
                    {
                        "Disciplina": "Materiais de Construção Mecânica",
                        "CH": 40,
                        "Professor": "Cláudio Marques Schaeffer",
                        "id": 37
                    },
                    {
                        "Disciplina": "Usinagem",
                        "CH": 40,
                        "Professor": "Ariton Araldi",
                        "id": 38
                    },
                    {
                        "Disciplina": "Atividades de Extensão II",
                        "CH": 80,
                        "Professor": "Fernando da Silva Osório",
                        "id": 39
                    },
                ],
                "8": [
                    {
                        "Disciplina": "Máquinas Térmicas",
                        "CH": 80,
                        "Professor": "Matheus Fontanelle Pereira",
                        "id": 40
                    },
                    {
                        "Disciplina": "Conformação e Fundição",
                        "CH": 40,
                        "Professor": "Rafael Gustavo Schreiber",
                        "id": 41
                    },
                    {
                        "Disciplina": "Conformação e Fundição",
                        "CH": 40,
                        "Professor": "Cláudio Marques Schaeffer",
                        "id": 42
                    },
                    {
                        "Disciplina": "Eletiva I",
                        "CH": 40,
                        "Professor": "Diego Augusto Gonzaga",
                        "id": 43
                    },
                    {
                        "Disciplina": "Eletiva II",
                        "CH": 40,
                        "Professor": "Rogério da Silva",
                        "id": 44
                    },
                    {
                        "Disciplina": "Manufatura Auxiliada por Computador",
                        "CH": 40,
                        "Professor": "Ariton Araldi",
                        "id": 45
                    },
                    {
                        "Disciplina": "Gestão de Qualidade e Produção",
                        "CH": 40,
                        "Professor": "Larisse Kupski",
                        "id": 46
                    },
                    {
                        "Disciplina": "Atividades de Extensão III",
                        "CH": 80,
                        "Professor": "Natalia Madalena Boelter",
                        "id": 47
                    },
                ],
                "10": [
                    {
                        "Disciplina": "Trabalho de Conclusão de Curso II",
                        "CH": 80,
                        "Professor": "Matheus Fontanelle Pereira",
                        "id": 48
                    },
                    {
                        "Disciplina": "Atividades de Extensão V",
                        "CH": 80,
                        "Professor": "Fernando da Silva Osório",
                        "id": 49
                    },
                    {
                        "Disciplina": "Sem aula",
                        "CH": 240,
                        "Professor": "Nenhum",
                        "id": 71
                    },
                ],
            },
            "Engenharia Química (Matutino)": {
                "2": [
                    {
                        "Disciplina": "Álgebra Linear",
                        "CH": 80,
                        "Professor": "Geovani Raulino",
                        "id": 50
                    },
                    {
                        "Disciplina": "Cálculo I",
                        "CH": 80,
                        "Professor": "Ailton Durigon",
                        "id": 51
                    },
                    {
                        "Disciplina": "Desenho Técnico",
                        "CH": 40,
                        "Professor": "Ricardo Teran Muhl",
                        "id": 52
                    },
                    {
                        "Disciplina": "Física I",
                        "CH": 80,
                        "Professor": "Eliana Fernandes Borragini",
                        "id": 53
                    },
                    {
                        "Disciplina": "Metodologia da Pesquisa",
                        "CH": 40,
                        "Professor": "Taiana Maria Deboni",
                        "id": 54
                    },
                    {
                        "Disciplina": "Química Orgânica I",
                        "CH": 80,
                        "Professor": "Carolina Berger",
                        "id": 55
                    },
                ],
                "4": [
                    {
                        "Disciplina": "Atividades de Extensão I",
                        "CH": 40,
                        "Professor": "Gustavo Henrique S. Flores Ponce",
                        "id": 56
                    },
                    {
                        "Disciplina": "Administração para Engenharia",
                        "CH": 40,
                        "Professor": "Thiago Meneghel Rodrigues",
                        "id": 57
                    },
                    {
                        "Disciplina": "Cálculo III",
                        "CH": 80,
                        "Professor": "Geovani Raulino",
                        "id": 58
                    },
                    {
                        "Disciplina": "Ciência e Tecnologia dos Materiais",
                        "CH": 40,
                        "Professor": "Jaqueline Suave",
                        "id": 59
                    },
                    {
                        "Disciplina": "Estatística II",
                        "CH": 40,
                        "Professor": "Gustavo Henrique S. Flores Ponce",
                        "id": 60
                    },
                    {
                        "Disciplina": "Físico-química II",
                        "CH": 40,
                        "Professor": "Marco Aurélio Woehl",
                        "id": 61
                    },
                    {
                        "Disciplina": "Informática e Programação",
                        "CH": 80,
                        "Professor": "Eder Corvalão",
                        "id": 62
                    },
                    {
                        "Disciplina": "Química Analítica II",
                        "CH": 40,
                        "Professor": "Haroldo Gregório de Oliveira",
                        "id": 63
                    },
                ],
                "6": [
                    {
                        "Disciplina": "Projeto Integrador II",
                        "CH": 80,
                        "Professor": "Haroldo Gregório de Oliveira",
                        "id": 64
                    },
                    {
                        "Disciplina": "Cinética Química",
                        "CH": 80,
                        "Professor": "Jaqueline Suave",
                        "id": 65
                    },
                    {
                        "Disciplina": "Cálculo Numérico",
                        "CH": 80,
                        "Professor": "Vilma Gisele Karsburg",
                        "id": 66
                    },
                    {
                        "Disciplina": "Fenômenos de Transporte I",
                        "CH": 80,
                        "Professor": "Gustavo Henrique S. Flores Ponce",
                        "id": 67
                    },
                    {
                        "Disciplina": "Segurança na Indústria",
                        "CH": 40,
                        "Professor": "Michael Ramos Nunes",
                        "id": 68
                    },
                    {
                        "Disciplina": "Termodinâmica I",
                        "CH": 40,
                        "Professor": "Diego Bittencourt Machado",
                        "id": 69
                    },

                ],
            },
        }
    def get_disciplinas_por_dia(self, dia):
        disciplinas_disponiveis = []
        for curso, fases in self.courses.items():
            for fase, disciplinas in fases.items():
                for disciplina in disciplinas:
                    professor = disciplina["Professor"]
                    horario_professor = self.professor_repository.get_schedule(professor)
                    if horario_professor and horario_professor[dia - 1] != "x":
                        disciplinas_disponiveis.append(disciplina)
        return disciplinas_disponiveis
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
                if horario_professor and horario_professor[dia - 1] != "x":
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
    repo = MatutinoRepository()

    curso_escolhido = "Ciência da Computação (Matutino)"
    fase_escolhida = "4"
    dia_escolhido = 1

    disciplinas_disponiveis = repo.get_disciplinas_por_curso_fase_e_dia(curso_escolhido, fase_escolhida, dia_escolhido)

    if disciplinas_disponiveis:
        print(f"Disciplinas disponíveis para o curso {curso_escolhido}, fase {fase_escolhida} na segunda-feira:")
        for disciplina in disciplinas_disponiveis:
            print(f"Disciplina: {disciplina['Disciplina']}")
            print(f"Professor: {disciplina['Professor']}")
            print()
    else:
        print(f"Nenhuma disciplina disponível para o curso {curso_escolhido}, fase {fase_escolhida} na segunda-feira.")
    # dia_escolhido = 1
    # disciplinas_na_segunda = repo.get_disciplinas_por_dia(dia_escolhido)
    #
    # if disciplinas_na_segunda:
    #     print(f"Disciplinas disponíveis na segunda-feira:")
    #     for disciplina in disciplinas_na_segunda:
    #         print(f"Disciplina: {disciplina['Disciplina']}")
    #         print(f"Professor: {disciplina['Professor']}")
    #         print()
    # else:
    #     print("Nenhuma disciplina disponível na segunda-feira.")

    # course = "Ciência da Computação (Matutino)"
    # phase = "4"
    #
    # disciplines = repo.getDisciplinesByPhaseAndCourse(course, phase)
    #
    # if len(disciplines) > 0:
    #     print(f"Disciplinas do curso {course} na fase {phase}:")
    #     for discipline in disciplines:
    #         print(f"Disciplina: {discipline['Disciplina']}")
    #         print(f"CH: {discipline['CH']}")
    #         print(f"Professor: {discipline['Professor']}")
    #         print()
    # else:
    #     print(f"Nenhuma disciplina encontrada para o curso {course} na fase {phase}")