class Solution:
    def __init__(self, m1, st_m1, m2, st_m2):
        self.m1 = m1
        self.st_m1 = st_m1
        self.m2 = m2
        self.st_m2 = st_m2
        self.fitness = 0

    # test solution
    def test_solution(self, machine1, machine2, maintenance):
        errors = []

        for i in range(1, len(self.m1)-1):
            exec_t = maintenance[(-(self.m1[i-1]))-1].exec_t if self.m1[i-1] < 0 else machine1[self.m1[i-1]-1].exec_t
            if self.st_m1[i] < self.st_m1[i-1] + exec_t:
                errors.append(["ops overlaping", i, self.fitness])

        # op started before ready time
        for i in self.m2:
            if self.st_m2[self.m2.index(i)] < machine1[i-1].exec_t + self.st_m1[self.m1.index(i)]:
                errors.append(["op2 starts before op1 ends", i])

        for i in errors:
            print(i)
            
    def put_ops_on_machine1(self, ops, machine1, maintenance):
        last_op_id = 0
        op_on_machine = False

        for i in range(0, len(self.m1)):
            if self.m1[i] > 0:
                last_op_id = i
                op_on_machine = True

        for op in ops:
            while not op_on_machine:
                prev_end = 0
                if last_op_id != 0:
                    prev_end = self.st_m1[last_op_id-1]+maintenance[(-self.m1[last_op_id-1])-1].exec_t

                if (last_op_id == len(self.m1)):
                    start_t = max(machine1[op-1].ready_t, prev_end)
                    self.m1.append(op)
                    self.st_m1.append(start_t)
                    op_on_machine = True
                    break

                dx = machine1[op-1].ready_t - prev_end
                dx = dx if dx > 0 else 0

                if machine1[op-1].ready_t + machine1[op-1].exec_t <= self.st_m1[last_op_id] and dx + machine1[op-1].exec_t <= self.st_m1[last_op_id] - prev_end:
                    start_t = max(machine1[op-1].ready_t, prev_end)
                    self.m1.insert(last_op_id,op)
                    self.st_m1.insert(last_op_id,start_t)
                    op_on_machine = True

                if not op_on_machine:
                    last_op_id += 1

            else:
                while op not in self.m1:

                    prev1 = (machine1[self.m1[last_op_id]-1].exec_t if self.m1[last_op_id] > 0 else maintenance[(-self.m1[last_op_id])-1].exec_t)
                    prev_end =  prev1 + self.st_m1[last_op_id]
                    
                    dx = machine1[op-1].ready_t - prev_end
                    dx = dx if dx > 0 else 0

                    if last_op_id == len(self.m1)-1:
                        start_t = max(prev_end, machine1[op-1].ready_t)
                        self.m1.append(op)
                        self.st_m1.append(start_t)
                        last_op_id += 1

                    elif machine1[op-1].exec_t <= self.st_m1[last_op_id+1] - (prev_end + dx):
                        start_t = max(prev_end, machine1[op-1].ready_t)
                        self.m1.insert(last_op_id+1, op)
                        self.st_m1.insert(last_op_id+1, start_t)
                        last_op_id += 1

                    else:
                        last_op_id += 1

    def put_ops_on_machine2(self, ops, machine1, machine2):
        it_m2 = 0
        for op1 in self.m1:
            if op1 > 0 and op1 == ops[it_m2]:
                if len(self.st_m2) != 0:
                    prev_task_end = self.st_m2[-1] + machine2[self.m2[-1]-1].exec_t
                else:
                    prev_task_end = 0
                self.m2.append(op1)
                self.st_m2.append(max(prev_task_end, self.st_m1[self.m1.index(op1)] + machine1[op1-1].exec_t))
                it_m2 += 1

    def calc_fitness(self, machine1, machine2):
        sum_of_end_times = 0
        for i in range(0, len(self.m1)-1):
            if (self.m1[i] > 0):
                sum_of_end_times += self.st_m1[i] + machine1[self.m1[i]-1].exec_t
        for i in range(0, len(self.m2)-1):
            sum_of_end_times += self.st_m2[i] + machine2[self.m2[i]-1].exec_t
        self.fitness = sum_of_end_times
