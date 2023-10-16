import random

from Chromosome import Chromosome


class Crossover:

    @staticmethod
    def cross(crossoverChancePercentage, generationChromosomes, chosen_chromosomes,course, isMatutino):
        faATotal = sum(chromosome.avaliation for chromosome in generationChromosomes)
        final_chromosomes = chosen_chromosomes.copy()
        # final_chromosomes = []
        num_couples = (len(generationChromosomes)) // 2

        for _ in range(num_couples):
            parent1 = Crossover.selectParent(generationChromosomes, faATotal)
            parent2 = Crossover.selectParent(generationChromosomes, faATotal)

            parent1_grouped_by_phase = Crossover.group_chromosomes_by_phase(parent1)
            parent2_grouped_by_phase = Crossover.group_chromosomes_by_phase(parent2)

            final_chromosome_grouped = []
            for phase in parent1_grouped_by_phase:
                partialchromosome1_groupedby_phase = parent1_grouped_by_phase[phase]
                partialchromosome2_groupedby_phase = parent2_grouped_by_phase[phase]
                crossover_point = random.randint(0, len(partialchromosome1_groupedby_phase) - 1)
                if random.randint(1, 100) <= crossoverChancePercentage:
                    final_chromosome_grouped.append(
                        partialchromosome1_groupedby_phase[:crossover_point] + partialchromosome2_groupedby_phase[
                                                                               crossover_point:])
                    final_chromosome_grouped.append(
                        partialchromosome2_groupedby_phase[:crossover_point] + partialchromosome1_groupedby_phase[
                                                                               crossover_point:])
                else:
                    final_chromosome_grouped.extend([partialchromosome1_groupedby_phase])
                    final_chromosome_grouped.extend([partialchromosome2_groupedby_phase])

            final_chromosome1, final_chromosome2 = Crossover.build_chromosomes_from_tuples(len(chosen_chromosomes[0].values), final_chromosome_grouped)
            child1 = Chromosome(course,isMatutino,10000)
            child2 = Chromosome(course,isMatutino,10000)
            child1.set_values(final_chromosome1)
            child2.set_values(final_chromosome2)
            final_chromosomes.extend([child1, child2])

        return final_chromosomes

    @staticmethod
    def group_chromosomes_by_phase(chromosome):
        count = 0
        new_chromosomes_grouped = {}
        for gene in chromosome.values:
            phase = chromosome.get_chosen_phase(count + 1)
            if phase not in new_chromosomes_grouped:
                new_chromosomes_grouped[phase] = []
            new_chromosomes_grouped[phase].append((count, gene))
            count += 1
        return new_chromosomes_grouped

    @staticmethod
    def build_chromosomes_from_tuples(chromosome_length, gene_tuples):
        chromosome1 = [None] * chromosome_length
        chromosome2 = [None] * chromosome_length

        count = 0
        for partial_chromosome in gene_tuples:
            if count % 2 == 0:
                for index, gene in partial_chromosome:
                    chromosome1[index] = gene
            else:
                for index, gene in partial_chromosome:
                    chromosome2[index] = gene
            count += 1
        return chromosome1, chromosome2

    @staticmethod
    def selectParent(generationChromosomes, faATotal):
        # print(str(faATotal))
        parentRNG = random.uniform(0, faATotal)

        cumulative_faA = 0

        for chromosome in generationChromosomes:
            cumulative_faA += chromosome.avaliation
            if cumulative_faA >= parentRNG:
                return chromosome

        return None
