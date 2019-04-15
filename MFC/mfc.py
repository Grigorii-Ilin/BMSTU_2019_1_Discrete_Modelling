import random
from pprint import pprint


DELTA_T = 0.01

class UnitAbstract:
    def __init__(self, mean_value, difference_btw_mean):
        self.working_time = 0.0

        self.left_border = mean_value - difference_btw_mean
        self.right_border = mean_value + difference_btw_mean
    
    #def __str__(self):
    #    return str(self.__class__) + ": " + str(self.__dict__)

    def set_work_time(self):
        if self.left_border == self.right_border:
            self.working_time = self.left_border
        else:
            self.working_time = random.uniform(self.left_border, self.right_border)

    def dec_work_time_and_get_is_action(self):
        #if not(self.is_work):
        #    return False

        self.is_action = False
        if self.working_time <= 0.0:
            return #False

        self.working_time-=DELTA_T
        
        if self.working_time <= 0.0:
            self.is_action = True
            return #True
        #return False


class People_generator(UnitAbstract):
    def __init__(self):
        #self.get_borders(10, 2)
        super().__init__(10, 2)
        self.ALL = 300
        self.go_away = 0
        self.come = 0
        self.set_work_time()

    def new_ppl(self):
        self.come+=1
        self.set_work_time()

    #def __str__(self):
    #    super().__str__()

    #def __str__(self):
    #    return str(self.__class__) + ": " + str(self.__dict__)

    #def calc_one_human(is_service):
    #    
    #    pass

    #def set_preferred_specialists(self, specialists):
    #    self.
class Specialist(UnitAbstract):
    def __init__(self, work_time_mean, work_time_difference, cpu):#, people_prefer):
        super().__init__(work_time_mean, work_time_difference)
        #self.get_borders(work_time_mean, work_time_difference)
        #self.people_prefer = people_prefer
        self.cpu = cpu
        #self.working_time=0.0

    #def __str__(self):
    #    super().__str__()

    def is_free(self):
        if self.working_time>0.0:
            return False

        if self.cpu.working_time>0 or self.cpu.queue_len>=2:
            return False

        #return self.working_time+self.cpu.working_time<=0
        return True



class Cpu(UnitAbstract):
    def __init__(self, work_time_mean):#, specialist_indexes):
        super().__init__(work_time_mean, 0)
        #self.get_borders(work_time_mean)
        #self.specialist_indexes=specialist_indexes
        self.queue_len = 0
        #self.working_time=0.0

    #def __str__(self):
    #    super().__str__()

    def add_doc_to_work(self):
        if self.queue_len==0:
            self.set_work_time()

        self.queue_len+=1



ppl_gen = People_generator()

cpus = []
cpus.append(Cpu(15))
cpus.append(Cpu(30))

specs = []
specs.append(Specialist(20.0,5.0, cpus[0]))
specs.append(Specialist(40.0,10.0, cpus[0]))
specs.append(Specialist(40.0,20.0, cpus[1]))
specs.sort(key=lambda x: x.left_border + x.cpu.left_border)

all_units = []
all_units.append(ppl_gen)
all_units.extend(specs)
all_units.extend(cpus)

time_left=0.0

print(time_left, ppl_gen.come)

while ppl_gen.come <= ppl_gen.ALL-1:
    #print(all_units)
    for unit in all_units:
        unit.dec_work_time_and_get_is_action()

    
    time_left+=DELTA_T

    if ppl_gen.is_action:
        ppl_gen.new_ppl()
        print(time_left, ppl_gen.come, ppl_gen.go_away)

        for spec in specs:
            #if spec.working_time<=0:
            if spec.is_free():
                spec.set_work_time()
                break
        else:
            ppl_gen.go_away+=1

    for spec in specs:
        if spec.is_action:
            spec.cpu.add_doc_to_work()

    for cpu in cpus:
        if cpu.is_action:
            cpu.queue_len-=1

print(time_left, ppl_gen.come, ppl_gen.go_away)