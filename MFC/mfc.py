import random
from pprint import pprint


DELTA_T = 0.01

class UnitAbstract:
    def __init__(self, mean_value, difference_btw_mean):
        self.working_time = 0.0
        self.is_action = False
        self.t_i = []

        self.left_border = mean_value - difference_btw_mean
        self.right_border = mean_value + difference_btw_mean


    def set_work_time(self):
        if self.left_border == self.right_border:
            self.working_time = self.left_border
        else:
            self.working_time = random.uniform(self.left_border, self.right_border)

    def dec_work_time_and_get_is_action(self):
        self.is_action = False
        if self.working_time <= 0.0:
            return 

        self.working_time-=DELTA_T
        
        if self.working_time <= 0.0:
            self.is_action = True
            return 


class People_generator(UnitAbstract):
    def __init__(self):
        super().__init__(10, 2)
        self.ALL = 300
        self.go_away = 0
        self.come = 0
        self.set_work_time()


    def new_ppl(self):
        if self.come==self.ALL:
            return

        self.come+=1
        self.set_work_time()


    def inc_go_away(self):
        self.go_away+=1


class Specialist(UnitAbstract):
    def __init__(self, work_time_mean, work_time_difference, cpu):
        super().__init__(work_time_mean, work_time_difference)
        self.cpu = cpu

    def is_free(self):
        return self.working_time <= 0.0

        #if self.working_time>0.0:
        #    return False

        #if self.cpu.working_time>0 or self.cpu.queue_len>=2:
        #    return False

        #return True

    def append_ppl(self):
        self.set_work_time()
        self.t_i.append(self.working_time)


class Cpu(UnitAbstract):
    def __init__(self, work_time_mean):
        super().__init__(work_time_mean, 0)
        self.queue_len = 0

    def add_doc_to_work(self):
        if self.queue_len == 0:
            self.set_work_time()

        self.queue_len+=1
        #self.t_i.append(0.0)
        self.t_i.insert(0, 0.0)

    def del_doc_from_work(self):
        cpu.queue_len-=1

        if self.queue_len >= 1:
            self.set_work_time()

    def add_dt_to_active_t_i(self):
        for i in range(self.queue_len):
            self.t_i[i]+=DELTA_T

            #index=len(self.t_i)-i-1
            #self.t_i[index]+=DELTA_T

def get_cpus():
    cpus = []
    cpus.append(Cpu(15))
    cpus.append(Cpu(30))    
    return cpus

def get_specialists(cpus):
    specs = []
    specs.append(Specialist(20.0,5.0, cpus[0]))
    specs.append(Specialist(40.0,10.0, cpus[0]))
    specs.append(Specialist(40.0,20.0, cpus[1]))
    #specs.sort(key=lambda x: x.left_border + x.cpu.left_border)
    specs.sort(key=lambda x: x.right_border)  
    return specs

def is_modelling_done(ppl_gen, specs, cpus):
    if ppl_gen.come <= ppl_gen.ALL - 1:
        return False

    for spec in specs:
        if not(spec.is_free()):
            return False

    for cpu in cpus:
        if cpu.queue_len>=1:
            return False

    return True

def print_result(ppl_gen, specs, cpus):
    print('ppl_gen')
    print(ppl_gen.go_away/ppl_gen.ALL)

    for spec in specs:
        print('spec')
        if spec.t_i == []:
            continue
        pprint(spec.t_i)
        print(sum(spec.t_i) / len(spec.t_i))

    for cpu in cpus:
        print('cpu')
        if cpu.t_i == []:
            continue
        pprint(cpu.t_i)
        print(sum(cpu.t_i) / len(cpu.t_i))


ppl_gen = People_generator()
cpus=get_cpus()
specs=get_specialists(cpus)

all_units = []
all_units.append(ppl_gen)
all_units.extend(specs)
all_units.extend(cpus)

time_left = 0.0

#print(time_left, ppl_gen.come)

while not(is_modelling_done(ppl_gen, specs, cpus)):
    for unit in all_units:
        unit.dec_work_time_and_get_is_action()

    for cpu in cpus:
        cpu.add_dt_to_active_t_i()
    
    time_left+=DELTA_T

    if ppl_gen.is_action:
        ppl_gen.new_ppl()
        #print(time_left, ppl_gen.come, ppl_gen.go_away)

        for spec in specs:
            if spec.is_free():
                spec.append_ppl()
                #spec.set_work_time()
                break
        else:
            #ppl_gen.go_away+=1
            ppl_gen.inc_go_away()

    for spec in specs:
        if spec.is_action:
            spec.cpu.add_doc_to_work()

    for cpu in cpus:
        if cpu.is_action:
            cpu.del_doc_from_work()
            #cpu.queue_len-=1

    if round(time_left * 100) % 100 == 0:        
        print(time_left, ppl_gen.come, ppl_gen.go_away)

print_result(ppl_gen, specs, cpus)