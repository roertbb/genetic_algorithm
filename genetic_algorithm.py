from time import time
from random import randint, random
from task import Task
from solution import Solution
from math import ceil, floor
import os

import matplotlib.pyplot as plt

class GeneticAlgorithm:
    def __init__(self, num_of_tasks, machine1, machine2, maintenance, population, max_pop, dest_pop, time, mut_percent, cross_percent, roulette_percent, save_data):
        self.num_of_tasks = num_of_tasks
        self.machine1 = machine1
        self.machine2 = machine2
        self.maintenance = maintenance
        self.population = population
        self.max_pop = max_pop
        self.dest_pop = dest_pop
        self.time = time
        self.mut_percent = mut_percent
        self.cross_percent = cross_percent
        self.roulette_percent = roulette_percent
        self.save_data = save_data
        self.iter_num = 0

    def solve(self):

        begin_fitness = self.population[0].fitness
        for p in self.population:
            if p.fitness < begin_fitness:
                begin_fitness = p.fitness
        print(begin_fitness)

        r_percent = self.roulette_percent[0]
        m_percent = self.mut_percent[0]
        c_percent = self.cross_percent[0]

        start_time = time()
        while True:

            pop_len = len(self.population)

            for i in range(0, pop_len):
                c = randint(1,100)
                if (c < self.mut_percent[0]):
                    self.mutate()

            for i in range(0, pop_len):
                c = randint(1,100)
                if (c < self.cross_percent[0]):
                    self.crossover()

            self.iter_num += 1

            it_end_time = time()
            dt = it_end_time - start_time
            if dt >= self.time:
                break

            r_percent = self.roulette_percent[floor(((it_end_time-start_time)/self.time)*(len(self.roulette_percent)))]
            m_percent = self.mut_percent[floor(((it_end_time-start_time)/self.time)*(len(self.mut_percent)))]
            c_percent = self.cross_percent[floor(((it_end_time-start_time)/self.time)*(len(self.cross_percent)))]

            if len(self.population) > self.max_pop:
                c = randint(1,100)
                if c < r_percent:
                    self.roulette()
                else:
                    self.tournament()

        print('iter:{}'.format(self.iter_num))

        min_fitness = self.population[0].fitness
        for p in self.population:
            if p.fitness < min_fitness:
                min_fitness = p.fitness
        print(min_fitness)

        self.save_solution_to_file(begin_fitness)

    def save_solution_to_file(self, begin_fitness):
        # [number_of_instance, instance_name, destination_folder]
        fittest = self.population[0]
        for sol in self.population:
            if sol.fitness < fittest.fitness:
                fittest = sol

        if not os.path.isdir("solution/" + self.save_data[2]):
            os.makedirs("solution/" + self.save_data[2])

        f = open("solution/" + self.save_data[2] + "/" + self.save_data[1] + ".txt","w+")
        f.write('**** {} ****\n'.format(self.save_data[0]))
        f.write('{}, {}\n'.format(fittest.fitness,begin_fitness))

        idle_counter = 1
        num_of_maint = 0
        sum_of_maint = 0
        num_of_idle1 = 0
        sum_of_idle1 = 0
        num_of_idle2 = 0
        sum_of_idle2 = 0

        # machine1
        f.write("M1: ")
        prev_end = 0
        for i in range(len(fittest.m1)):
            if fittest.st_m1[i] > prev_end:
                f.write("idle{}_M1, {}, {}; ".format(idle_counter, prev_end, fittest.st_m1[i] - prev_end))
                num_of_idle1 += 1
                sum_of_idle1 += fittest.st_m1[i] - prev_end

            if fittest.m1[i] < 0:
                f.write("maint{}_M1, {}, {}; ".format(-fittest.m1[i], fittest.st_m1[i], self.maintenance[(-fittest.m1[i])-1].exec_t))
                prev_end = fittest.st_m1[i] + self.maintenance[(-fittest.m1[i])-1].exec_t
                num_of_maint += 1
                sum_of_maint += self.maintenance[(-fittest.m1[i])-1].exec_t 
            else:
                f.write("op1_{}, {}, {}; ".format(fittest.m1[i], fittest.st_m1[i], self.machine1[fittest.m1[i]-1].exec_t))
                prev_end = fittest.st_m1[i] + self.machine1[fittest.m1[i]-1].exec_t
        # machine2
        f.write("\nM2: ")
        prev_end = 0
        for i in range(len(fittest.m2)):
            if fittest.st_m2[i] > prev_end:
                f.write("idle{}_M2, {}, {}; ".format(idle_counter, prev_end, fittest.st_m2[i] - prev_end))
                num_of_idle2 += 1
                sum_of_idle2 += fittest.st_m2[i] - prev_end

            f.write("op2_{}, {}, {}; ".format(fittest.m2[i], fittest.st_m2[i], self.machine2[fittest.m2[i]-1].exec_t))
            prev_end = fittest.st_m2[i] + self.machine2[fittest.m2[i]-1].exec_t
        
        f.write("\n{}, {}\n{}, {}\n{}, {}\n{}, {}\n**** EOF ****".format(num_of_maint, sum_of_maint, 0, 0, num_of_idle1, sum_of_idle1, num_of_idle2, sum_of_idle2))
        f.close()
        print("saved data to solution/" + self.save_data[2] + "/" + self.save_data[1] + ".txt")

    def roulette(self):
        # loop through population - find best solution and calculate arbitral number indicating "fitness"
        # the lower sum of time -> the bigger amount of "points" 

        best = self.population[0]
        num = [0]
        sum_of_points = 0
        for pop in self.population:
            sum_of_points += (1/pop.fitness)*(self.num_of_tasks*1000)
            num.append(sum_of_points)
            if pop.fitness < best.fitness:
                best = pop

        # create new population and append best solution
        new_population = []
        new_population.append(best)

        best_id = self.population.index(best)

        # choose solution according to probability
        for i in range(0, self.dest_pop-1):
            x = best_id
            while(self.population[x] in new_population):
                rand = random() * num[-1]
                begin = 0 
                end = len(self.population)-1
                x = (begin+end)//2
                while(rand<=num[x] or rand>=num[x+1]):
                    if num[x] > rand:
                        end = x
                    else:
                        begin = x+1
                    x = (begin+end)//2 
            new_population.append(self.population[x])

        self.population = new_population

    def tournament(self):
        ratio = len(self.population)/self.dest_pop
        higher = ceil(ratio)
        lower = floor(ratio)
        n_higher = int(round((len(self.population)/self.dest_pop - lower)*self.dest_pop))
        n_lower = int(self.dest_pop - n_higher)

        new_population = []

        for i in range(n_higher):
            sol_to_tour = []
            for j in range(higher):
                sol_to_tour.append(self.population.pop(randint(0,len(self.population)-1)))
            best_fitness = sol_to_tour[0]
            for sol in sol_to_tour:
                if sol.fitness < best_fitness.fitness:
                    best_fitness = sol
            new_population.append(best_fitness)

        for i in range(n_lower):
            sol_to_tour = []
            for j in range(lower):
                sol_to_tour.append(self.population.pop(randint(0,len(self.population)-1)))
            best_fitness = sol_to_tour[0]
            for sol in sol_to_tour:
                if sol.fitness < best_fitness.fitness:
                    best_fitness = sol
            new_population.append(best_fitness)

        self.population = new_population

    def mutate(self):
        sol_to_mut = self.population[randint(0,len(self.population)-1)]

        op_id = randint(1, self.num_of_tasks-1)

        ord_num = randint(0, self.num_of_tasks-2)
        ord_num = [ord_num, ord_num]

        new_solution = Solution([],[],[],[])
        op1 = []
        op2 = []

        for i in range(0, len(sol_to_mut.m1)):
            if ord_num[0] == 0:
                op1.append(op_id)
                ord_num[0] = self.num_of_tasks+1

            if sol_to_mut.m1[i] < 0:
                new_solution.m1.append(sol_to_mut.m1[i])
                new_solution.st_m1.append(sol_to_mut.st_m1[i])

            elif sol_to_mut.m1[i] != op_id:
                op1.append(sol_to_mut.m1[i])
                ord_num[0] -= 1

        new_solution.put_ops_on_machine1(op1, self.machine1, self.maintenance)

        for i in range(0, len(sol_to_mut.m2)):
            if ord_num[1] == 0:
                op2.append(op_id)
                ord_num[1] = self.num_of_tasks+1
            if sol_to_mut.m2[i] != op_id:
                op2.append(sol_to_mut.m2[i])
                ord_num[1] -= 1

        new_solution.put_ops_on_machine2(op2, self.machine1, self.machine2)
        new_solution.calc_fitness(self.machine1, self.machine2)

        self.population.append(new_solution)

    def crossover(self):
        id1 = randint(0, len(self.population)-1)
        id2 = randint(0, len(self.population)-1)
        while id1 == id2:
            id2 = randint(0, len(self.population)-1)

        sol1 = self.population[id1]
        sol2 = self.population[id2]

        unselected_sol1 = [i for i in range(1,self.num_of_tasks+1)]
        unselected_sol2 = [i for i in range(1,self.num_of_tasks+1)]

        num_of_ops = [self.num_of_tasks//2, self.num_of_tasks//2, self.num_of_tasks//2, self.num_of_tasks//2]

        cross_sol1 = Solution([],[],[],[])
        cross_sol2 = Solution([],[],[],[])

        last_task_id = [0, 0]

        for i in range(0, len(sol1.m1)-1):
            if sol1.m1[i] < 0 or num_of_ops[0] > 0:
                cross_sol1.m1.append(sol1.m1[i])
                cross_sol1.st_m1.append(sol1.st_m1[i])
                if sol1.m1[i] > 0:
                    unselected_sol1.remove(sol1.m1[i])
                    num_of_ops[0] -= 1
                    last_task_id[0] = len(cross_sol1.m1)-1

        for i in range(0, len(sol2.m1)-1):
            if sol2.m1[i] < 0 or num_of_ops[2] > 0:
                cross_sol2.m1.append(sol2.m1[i])
                cross_sol2.st_m1.append(sol2.st_m1[i])
                if sol2.m1[i] > 0:
                    unselected_sol2.remove(sol2.m1[i])
                    num_of_ops[2] -= 1
                    last_task_id[1] = len(cross_sol2.m1)-1

        uninserted_cross1 = []
        uninserted_cross2 = []

        for op in sol2.m1:
            if op > 0 and op in unselected_sol1:
                uninserted_cross1.append(op)
                unselected_sol1.remove(op)

        for op in sol1.m1:
            if op > 0 and op in unselected_sol2:
                uninserted_cross2.append(op)
                unselected_sol2.remove(op)
            
        cross_sol1.put_ops_on_machine1(uninserted_cross1, self.machine1, self.maintenance)
        cross_sol2.put_ops_on_machine1(uninserted_cross2, self.machine1, self.maintenance)

        for i in range(0, len(sol1.m2)):
            if num_of_ops[1] > 0:
                cross_sol1.m2.append(sol1.m2[i])
                cross_sol1.st_m2.append(sol1.st_m2[i])
                num_of_ops[1] -= 1
            else:
                unselected_sol1.append(sol1.m2[i])

        for i in range(0, len(sol2.m2)):
            if num_of_ops[3] > 0:
                cross_sol2.m2.append(sol2.m2[i])
                cross_sol2.st_m2.append(sol2.st_m2[i])
                num_of_ops[3] -= 1
            else:
                unselected_sol2.append(sol2.m2[i])

        uninserted_cross1 = []
        uninserted_cross2 = []

        for i in sol2.m2:
            if i in unselected_sol1:
                uninserted_cross1.append(i)

        for i in sol1.m2:
            if i in unselected_sol2:
                uninserted_cross2.append(i)

        cross_sol1.put_ops_on_machine2(uninserted_cross1, self.machine1, self.machine2)
        cross_sol2.put_ops_on_machine2(uninserted_cross2, self.machine1, self.machine2)

        cross_sol1.calc_fitness(self.machine1, self.machine2)
        cross_sol2.calc_fitness(self.machine1, self.machine2)

        self.population.append(cross_sol1)
        self.population.append(cross_sol2)

    