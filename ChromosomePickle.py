import json

import Pyro5.api
from Chromosome import Chromosome  # Certifique-se de importar a classe Chromosome


class ChromosomeSerializer:
    @staticmethod
    def dumps(obj):
        data = []
        for chromosome in obj:
            chromosome_data = {
                'values': chromosome.values,
                'course': chromosome.course,
                'avaliation': chromosome.avaliation
                # Adicione outras propriedades aqui, se necessário
            }
            data.append(chromosome_data)
        # Serializa a lista de dicionários em uma string JSON
        serialized_data = json.dumps(data)
        return serialized_data.encode('utf-8')

    @staticmethod
    def loads( data):
        decoded_data = data.decode('utf-8')
        data_list = json.loads(decoded_data)
        # Cria uma lista de instâncias de Chromosome com os dados desserializados
        chromosomes = []
        for chromosome_data in data_list:
            chromosome = Chromosome(
                course=chromosome_data['course'],
                avaliation=chromosome_data['avaliation'],
                values=chromosome_data['values']
                # Adicione outras propriedades aqui, se necessário
            )
            chromosomes.append(chromosome)
        return chromosomes