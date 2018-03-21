from gen_instance import InstanceGenerator
from gen_random_solution import RandomSolutionGenerator
from genetic_algorithm import GeneticAlgorithm

def gen_instances(how_many, name, number_of_tasks, min_task_time, max_task_time, maint_over_min, min_maint_time, max_maint_time):
    instance_generator = InstanceGenerator(number_of_tasks, name, min_task_time, max_task_time, maint_over_min, min_maint_time, max_maint_time)
    for i in range(how_many):
        instance_generator.gen_instance()

def solve(filename):
    f = open(filename, "r")
    f.readline()
    
    for line in f.readlines():
        temp = line.split(';')

        inst_path = "instance/" + temp[0] + ".txt"

        ops1, ops2, maint, num_of_tasks, num_of_inst = InstanceGenerator.load_instance_from_file(inst_path)
        ops = [ops1, ops2, maint]

        num_of_init_sol = int(temp[1])
        random_solution_generator = RandomSolutionGenerator(num_of_init_sol, *ops)
        if int(temp[10]) == 0:
            initial_population = random_solution_generator.gen_random_solution()
        else:
            initial_population = random_solution_generator.gen_random_solution_dummy()

        max_population = int(temp[2])
        destined_population = int(temp[3])
        time = int(temp[4])
        mutation_percentage = [int(x) for x in temp[5].split(',')]
        crossover_percentage = [int(x) for x in temp[6].split(',')]
        roulette_percentage = [int(x) for x in temp[7].split(',')]

        save_data = [num_of_inst, temp[0] + temp[8], temp[9]]

        print("starting " + temp[0] + temp[8])

        ga = GeneticAlgorithm(num_of_tasks, *ops, initial_population, max_population, destined_population, time, mutation_percentage, crossover_percentage, roulette_percentage, save_data)
        ga.solve()

    f.close()
    print("done")

solve("example_wrap.csv")