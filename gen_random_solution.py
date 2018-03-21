from random import shuffle, randint
from solution import Solution

class RandomSolutionGenerator:
    def __init__(self, num_of_solution, machine1, machine2, maintenance):
        self.num_of_solution = num_of_solution
        self.machine1 = machine1
        self.machine2 = machine2
        self.maintenance = maintenance

    def gen_random_solution(self):
        self.maintenance.sort(key = lambda x: x.start_t)

        initial_population = []

        for i in range(self.num_of_solution):
            sol = Solution([],[],[],[])

            op1 = list(range(1,len(self.machine1)+1))
            shuffle(op1)

            # rewrite maintenances
            self.maintenance.sort(key = lambda x: x.start_t)
            for m in self.maintenance:
                sol.m1.append(-m.tid)
                sol.st_m1.append(m.start_t)
            self.maintenance.sort(key = lambda x: x.tid)

            # put ops on machine1
            for i in range(len(op1)):
                fit = False

                # try to fit before first op
                if self.machine1[op1[i]-1].ready_t + self.machine1[op1[i]-1].exec_t <= sol.st_m1[0]:
                    sol.m1.insert(0, op1[i]) 
                    sol.st_m1.insert(0, self.machine1[op1[i]-1].ready_t)
                    fit = True
                    # break

                # try to fit task before other tasks
                for j in range(len(sol.m1)-1):

                    if fit:
                        break

                    prev1 = (self.machine1[sol.m1[j]-1].exec_t if sol.m1[j] > 0 else self.maintenance[(-sol.m1[j])-1].exec_t)
                    prev_end = prev1 + sol.st_m1[j]
                    
                    dx = self.machine1[op1[i]-1].ready_t - prev_end
                    dx = dx if dx > 0 else 0

                    if self.machine1[op1[i]-1].exec_t <= sol.st_m1[j+1] - (prev_end + dx):
                        start_t = max(prev_end, self.machine1[op1[i]-1].ready_t)
                        sol.m1.insert(j+1, op1[i])
                        sol.st_m1.insert(j+1, start_t)
                        fit = True
                        break

                # else put task as last one on machine1
                if not fit:
                    prev_end = sol.st_m1[-1] + (self.machine1[sol.m1[-1]-1].exec_t if sol.m1[-1] > 0 else self.maintenance[(-sol.m1[-1])-1].exec_t)
                    start_t = max(prev_end, self.machine1[op1[i]-1].ready_t)
                    sol.m1.append(op1[i])
                    sol.st_m1.append(start_t)

            # read order from machine1 - as order on [sol.m1] of ops and put ops on machine 2 in that order
            for i in range(len(sol.m1)):
                if sol.m1[i] > 0:
                    if len(sol.m2) == 0:
                        sol.m2.append(sol.m1[i])
                        sol.st_m2.append(sol.st_m1[i] + self.machine1[sol.m1[i]-1].exec_t)
                    else:
                        sol.m2.append(sol.m1[i])
                        sol.st_m2.append(max(sol.st_m1[i] + self.machine1[sol.m1[i]-1].exec_t, sol.st_m2[-1] + self.machine2[sol.m2[-1]-1].exec_t))
                        
            # rest
            sol.calc_fitness(self.machine1, self.machine2)

            # sol.test_solution(self.machine1, self.machine2, self.maintenance)
            initial_population.append(sol)

        return initial_population

    def gen_random_solution_dummy(self):
        self.maintenance.sort(key = lambda x: x.start_t)

        initial_population = []

        for i in range(self.num_of_solution):
            sol = Solution([],[],[],[])

            op1 = list(range(1, len(self.machine1)+1)) # create list of ops to put
            shuffle(op1)
            self.maintenance.sort(key = lambda x: x.start_t)
            op2 = op1[:] # copy list - ops on machine2 will be placed in the same order
            for m in self.maintenance:
                sol.m1.append(-m.tid)
                sol.st_m1.append(m.start_t)

            self.maintenance.sort(key = lambda x: x.tid)
            sol.put_ops_on_machine1(op1, self.machine1, self.maintenance)
            sol.put_ops_on_machine2(op2, self.machine1, self.machine2)

            sol.calc_fitness(self.machine1, self.machine2)

            # sol.test_solution(self.machine1, self.machine2, self.maintenance)
            initial_population.append(sol)

        return initial_population

        

        
