from random import randint
from math import ceil, floor
from os import listdir
from task import Task

# instance_generator = InstanceGenerator(num_of_task, min_task_time, max_task_time, maint_over_min, min_maint_time, max_maint_time)

class InstanceGenerator:

    def __init__(self, num_of_tasks, name, min_task_time, max_task_time, maint_over_min, min_maint_time, max_maint_time):
        self.num_of_tasks = num_of_tasks
        self.name = name
        self.min_task_time = min_task_time
        self.max_task_time = max_task_time
        self.maint_over_min = maint_over_min
        self.min_maint_time = min_maint_time
        self.max_maint_time = max_maint_time

    def gen_instance_same_time(self, div):
        op_on_machine1_1 = []
        op_on_machine2_1 = []
        op_on_machine1_2 = []
        op_on_machine2_2 = []
        op_on_machine1_3 = []
        op_on_machine2_3 = []
        maintenance = []
        sum_of_exec_time1 = 0
        sum_of_exec_time2 = 0

        # gen tasks on machine1
        for i in range(self.num_of_tasks):
            exec_time = randint(self.min_task_time, self.max_task_time) # a <= x <= b
            sum_of_exec_time1 += exec_time
            op_on_machine1_1.append(Task(i+1, "op1", exec_time, 0))

        # gen tasks on machine2
        for i in range(self.num_of_tasks):
            exec_time = randint(self.min_task_time, self.max_task_time) 
            sum_of_exec_time2 += exec_time
            op_on_machine2_1.append(Task(i+1, "op2", exec_time, 0))

        # gen maintenances
        for i in range(ceil(ceil(self.num_of_tasks / 4) * (1+self.maint_over_min/100))): 
            exec_time = randint(self.min_maint_time, self.max_maint_time)
            # sum_of_exec_time1 += exec_time
            maint = Task(i+1, "maint", exec_time, 0)
            maint.start_t = 0
            maintenance.append(maint)

        # set ready_time after calculating sum_of_exec_time
        for i in range(self.num_of_tasks):
            op_on_machine1_1[i].ready_t = randint(1, sum_of_exec_time1//2) # integer division

        # calc maintenance start_time and prevent from overlaping
        maintenance.sort(key = lambda x: x.exec_t, reverse=True)
        for i in range(len(maintenance)):
            can_exec = False
            while not can_exec:
                can_exec = True
                start_time = randint(0,sum_of_exec_time1-1)
                end_time = start_time + maintenance[i].exec_t
                for j in range(len(maintenance)):
                    if (start_time >= maintenance[j].start_t and start_time <  maintenance[j].start_t + maintenance[j].exec_t) or (end_time >=  maintenance[j].start_t and end_time <  maintenance[j].start_t + maintenance[j].exec_t):
                        can_exec = False
                if can_exec:
                    #  maintenance_start_t[i] = start_time
                     maintenance[i].start_t = start_time

        # second instance
        for i in range(floor(self.num_of_tasks/div)):
            op_on_machine1_2.append(Task(i+1, "op1", 0, 0))

        for i in range(sum_of_exec_time1):
            randid = randint(0,floor(self.num_of_tasks/div)-1)
            op_on_machine1_2[randid].exec_t += 1

        # set ready_time after calculating sum_of_exec_time
        for i in range(floor(self.num_of_tasks/div)):
            op_on_machine1_2[i].ready_t = randint(1, sum_of_exec_time1//2) # integer division

        for i in range(floor(self.num_of_tasks/div)):
            op_on_machine2_2.append(Task(i+1, "op2", 0, 0))

        for i in range(sum_of_exec_time2):
            randid = randint(0,floor(self.num_of_tasks/div)-1)
            op_on_machine2_2[randid].exec_t += 1

        self.instance_to_file(op_on_machine1_1, op_on_machine2_1, maintenance)
        self.instance_to_file(op_on_machine1_2, op_on_machine2_2, maintenance, "_"+str(div)+"div")
        return (op_on_machine1_1, op_on_machine2_1, maintenance)
        
    def gen_instance(self):
        op_on_machine1 = []
        op_on_machine2 = []
        maintenance = []
        sum_of_exec_time = 0

        # gen tasks on machine1
        for i in range(self.num_of_tasks):
            exec_time = randint(self.min_task_time, self.max_task_time) # a <= x <= b
            sum_of_exec_time += exec_time
            op_on_machine1.append(Task(i+1, "op1", exec_time, 0))

        # gen tasks on machine2
        for i in range(self.num_of_tasks):
            exec_time = randint(self.min_task_time, self.max_task_time) 
            op_on_machine2.append(Task(i+1, "op2", exec_time, 0))

        # gen maintenances
        for i in range(ceil(ceil(self.num_of_tasks / 4) * (1+self.maint_over_min/100))):
            exec_time = randint(self.min_maint_time, self.max_maint_time)
            # sum_of_exec_time += exec_time
            maint = Task(i+1, "maint", exec_time, 0)
            maint.start_t = 0
            maintenance.append(maint)

        # set ready_time after calculating sum_of_exec_time
        for i in range(self.num_of_tasks):
            op_on_machine1[i].ready_t = randint(1, sum_of_exec_time//2) # integer division

        # calc maintenance start_time and prevent from overlaping
        maintenance.sort(key = lambda x: x.exec_t, reverse=True)
        for i in range(len(maintenance)):
            can_exec = False
            while not can_exec:
                can_exec = True
                start_time = randint(0,sum_of_exec_time-1)
                end_time = start_time + maintenance[i].exec_t
                for j in range(len(maintenance)):
                    if (start_time >= maintenance[j].start_t and start_time <  maintenance[j].start_t + maintenance[j].exec_t) or (end_time >=  maintenance[j].start_t and end_time <  maintenance[j].start_t + maintenance[j].exec_t):
                        can_exec = False
                if can_exec:
                    #  maintenance_start_t[i] = start_time
                     maintenance[i].start_t = start_time

        self.instance_to_file(op_on_machine1, op_on_machine2, maintenance)
        return (op_on_machine1, op_on_machine2, maintenance)

    def instance_to_file(self, machine1, machine2, maintenance, sufix = ""):
        instances = listdir('./instance/')
        without_div = filter(lambda k: 'div' not in k, instances)
        n = list(map(lambda s: int(s[len(self.name):-4]), list(filter(lambda f: f[:len(self.name)] == self.name, without_div))))
        n.sort()
        num_of_instance = n[-1]+1 if len(n)>0 else 0
        if (sufix != ""):
            num_of_instance -= 1
        filename = 'instance/'+self.name+str(num_of_instance)+sufix+'.txt'
        f = open(filename,"w+")
        f.write('**** {} ****\n'.format(num_of_instance))
        f.write('{}\n'.format(len(machine1)))
        for i in range(len(machine1)):
            f.write('{};{};1;2;{};\n'.format(machine1[i].exec_t,machine2[i].exec_t,machine1[i].ready_t))
        maintenance.sort(key=lambda x: x.tid)
        for i in range(len(maintenance)):
            f.write('{};1;{};{}\n'.format(maintenance[i].tid, maintenance[i].exec_t, maintenance[i].start_t))
        f.write('*** EOF ***')
        f.close()

    @staticmethod
    def load_instance_from_file(filename):
        f = open(filename,"r")
        instance_num = int(f.readline().split(' ')[1])
        num_of_ops = int(f.readline().split('\n')[0])
        
        ops1 = []
        ops2 = []
        maint = []

        for i in range(0, num_of_ops):
            temp = f.readline().split(';')
            ops1.append(Task(i+1,"op1",int(temp[0]),int(temp[4])))
            ops2.append(Task(i+1,"op2",int(temp[1]),0))

        temp = f.readline()
        while(temp != "*** EOF ***"):
            temp = temp.split(';')
            maint.append(Task(int(temp[0]),"maint",int(temp[2]),0))
            maint[-1].start_t = int(temp[3].split('\n')[0])
            temp = f.readline()
        
        return (ops1, ops2, maint, num_of_ops, instance_num)