class Task:
    def __init__(self, tid, ttype, exec_t, ready_t):
        self.tid = tid
        self.ttype = ttype
        self.exec_t = exec_t
        self.ready_t = ready_t