# Genetic algorithm for solving scheduling problem

Student project for combinatorial optimization

## Content
- run.py - genetic algorithm runner
- run_gen_inst.py - instance generator runner

- gen_instance - problem instance generator
- gen_random_solution - random solution generator
- genetic_algorith - main class of metaheuristic
- solution.py, task.py - helper classes

- instance, directory - directories, where examined data is stored

## Problem description

- Flowshop, m = 2 machines, n - number of tasks
- indivisible operations
- for 1st machine, k maintenance breaks - random start time and duration (k>=4)
- ready time for each operation on 1st machine, that's not exceeding half the time of all operations on 1st machine

## 

## Instance generation

Edit last line of script
```
gen_instances(10, 'instance_test', 50, 1, 20, 0, 1, 20)
```
parameters description:
- number of instances,
- primary name - script adds numbers from 0 to n-1
- number of tasks
- minimal duration time
- maximal duration time
- % of maintenance above k = ceil(number_of_tasks/4)
- minimal maintenance time
- maximal maintenance time

second generator creates intances with the same sum of operation's duration time, but number of tasks is divided by **div**, where **div** is last parameter

## Genetic algorithm

In order to automatically run another instances, we prepared script, that's been reading **.csv** files and run the algorithm for choosen instance.

example file:
```
instance_name;size_of_initial_population;max_population_size;dest_population_size;time;mutation_percentage;crossover_percentage;roulette_percentage;save_sufix;savdirectory;gen;
instance0;50;150;50;60;12;86;100,76,52;_id1;test_solution;0;
```

parameters description:
- instance_name - name of file from **instance** directory
- size_of_initial_population
- max_population - when such population size is exceeded, selection is going to shrink number of solution
- dest_population - population size after selection
- time - how long the algorithm works
- mutation_percentage
- crossover_percentage
- roulette_percentage - all 3 are genetic algorithm parameters
- save_sufix - sufix after name, describing parameter which is examined
- savedirectory - names of the directory where solution is saved
- gen - type of generator, which was used to create initial population (0 - naive algorithm, 1- random algorithm)

## Authors
 
- Małgorzata Brzuchalska
- Robert Banaszak (@roertbb)