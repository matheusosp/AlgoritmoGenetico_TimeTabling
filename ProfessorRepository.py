class ProfessorRepository:
    def __init__(self):
        self.data = {}
        self.data["Ailton Durigon"] = ["x", None, None, None, None]
        self.data["Alexandre Perin de Souza"] = [None, "x", None, None, None]
        self.data["Anderson Luis Garcia Correia"] = [None, None, "x", None, None]
        self.data["Ariton Araldi"] = [None, None, None, "x", None]
        self.data["Carlos Andres Ferrero"] = [None, None, None, None, "x"]
        self.data["Carolina Berger"] = ["x", "x", None, None, None]
        self.data["Cláudio Marques Schaeffer"] = ["x", None, None, None, None]
        self.data["Diego Augusto Gonzaga"] = [None, None, "x", None, None]
        self.data["Diego Bittencourt Machado"] = [None, None, "x", None, None]
        self.data["Douglas Carvalho Morais"] = [None, None, None, None, "x"]
        self.data["Eder Corvalão"] = [None, None, "x", "x", "x"]
        self.data["Eliana Fernandes Borragini"] = [None, None, None, "x", None]
        self.data["Fabio Aiub Sperotto"] = [None, None, None, None, "x"]
        self.data["Fernando da Silva Osório"] = [None, "x", None, None, None]
        self.data["Fernando Weber Albiero"] = [None, "x", None, None, None]
        self.data["Gabriel Granzotto Madruga"] = [None, None, "x", "x", None]
        self.data["Geovani Raulino"] = [None, None, "x", "x", None]
        self.data["Gustavo Henrique S. Flores Ponce"] = ["x", None, None, None, None]
        self.data["Haroldo Gregório de Oliveira"] = [None, None, None, None, "x"]
        self.data["Jaqueline Suave"] = [None, None, "x", None, None]
        self.data["Jeferson Fraytag"] = ["x", None, None, None, None]
        self.data["João Augusto da Silva Bueno"] = ["x", None, None, None, None]
        self.data["Joelma Kremer"] = [None, "x", None, None, None]
        self.data["Juliana Mercedes Rheinheimer"] = [None, "x", None, None, None]
        self.data["Julio Azambuja da Silveira"] = [None, None, None, "x", None]
        self.data["Larisse Kupski"] = [None, None, None, None, None]
        self.data["Leonardo Bravo Estacio"] = [None, None, None, None, None]
        self.data["Marco Aurélio Woehl"] = [None, None, None, None, "x"]
        self.data["Marisa Santos Sanson"] = ["x", None, None, None, None]
        self.data["Matheus Fontanelle Pereira"] = [None, None, None, None, None]
        self.data["Michael Ramos Nunes"] = [None, None, "x", None, None]
        self.data["Natalia Madalena Boelter"] = [None, "x", None, None, None]
        self.data["Paula Clarice Santos G. de Jesus"] = [None, None, None, None, None]
        self.data["Rafael Gustavo Schreiber"] = [None, None, "x", None, None]
        self.data["Ricardo Teran Muhl"] = ["x", None, None, None, None]
        self.data["Robson Costa"] = [None, None, None, None, None]
        self.data["Rogério da Silva"] = [None, None, None, None, "x"]
        self.data["Samuel Ferreira de Melo"] = [None, None, None, "x", None]
        self.data["Taiana Maria Deboni"] = ["x", "x", None, None, None]
        self.data["Thiago Henrique Mombach"] = [None, None, None, "x", None]
        self.data["Thiago Meneghel Rodrigues"] = [None, None, None, None, None]
        self.data["Vilma Gisele Karsburg"] = [None, None, None, None, None]
        self.data["Vilson Heck Junior"] = ["x", "x", None, None, None]
        self.data["Wilson Castello Branco Neto"] = [None, None, None, "x", None]
        self.data["Orientador"] = [None, None, None, None, None]
        self.data["Nenhum"] = [None, None, None, None, None]

    def get_schedule(self, professor_name):
        if professor_name in self.data:
            return [(dia, self.data[professor_name][dia - 1]) for dia in range(1, 6)]
        else:
            return None

    def teacher_work_inday(self, professor_name, dia):
        if professor_name in self.data and 1 <= dia <= 5:
            status = self.data[professor_name][dia - 1]
            return status == "x"
        else:
            return False
if __name__ == "__main__":
    repo = ProfessorRepository()
    nome_professor = "Carolina Berger"
    horario = repo.get_schedule(nome_professor)
    if horario:
        print(f"Horário de trabalho de {nome_professor}:")
        for dia, status in horario:
            if status == "x":
                print(f"Dia {dia}: Não trabalha")
            else:
                print(f"Dia {dia}: Trabalha")
    else:
        print(f"Professor {nome_professor} não encontrado.")
