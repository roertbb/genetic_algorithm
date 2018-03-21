from gen_instance import InstanceGenerator
from gen_random_solution import RandomSolutionGenerator
from genetic_algorithm import GeneticAlgorithm

def gen_instances(how_many, name, number_of_tasks, min_task_time, max_task_time, maint_over_min, min_maint_time, max_maint_time):
    instance_generator = InstanceGenerator(number_of_tasks, name, min_task_time, max_task_time, maint_over_min, min_maint_time, max_maint_time)
    for i in range(how_many):
        instance_generator.gen_instance()

def gen_instances_div(how_many, name, number_of_tasks, min_task_time, max_task_time, maint_over_min, min_maint_time, max_maint_time, div):
    instance_generator = InstanceGenerator(number_of_tasks, name, min_task_time, max_task_time, maint_over_min, min_maint_time, max_maint_time)
    for i in range(how_many):
        instance_generator.gen_instance_same_time(div)

gen_instances(1, 'instance_test', 50, 1, 20, 0, 1, 20)
# gen_instances(10, 'instance_test', 50, 1, 20, 0, 1, 20, 2)