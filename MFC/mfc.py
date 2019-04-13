import random

class UnitAbstract:
    def get_borders(self, mean_value, difference_btw_mean=0):
        self.left_border = mean_value - difference_btw_mean
        self.right_border = mean_value + difference_btw_mean

    def set_work_time(self):
        if self.left_border == self.right_border:
            self.work_time = self.left_border
        else:
            self.work_time = random.uniform(self.left_border, self.right_border)

    def dec_work_time_and_get_is_action(self):
        #if not(self.is_work):
        #    return False
        if self.is_work <= 0.0:
            return False

        DELTA_T = 0.01
        self.is_work-=DELTA_T
        
        if self.is_work <= 0.0:
            return True
        return False


class People_generator(UnitAbstract):
    def __init__(self):
        self.get_borders(10, 2)
        self.people_max = 300
        self.away_count = 0

    def set_preferred_specialists(self, specialists):
        pass

class Specialist(UnitAbstract):
    def __init__(self, work_time_mean, work_time_difference, cpu_id):#, people_prefer):
        self.get_borders(work_time_mean, work_time_difference)
        #self.people_prefer = people_prefer
        self.cpu_id=cpu_id

class Cpu(UnitAbstract):
    def __init__(self, work_time_mean):#, specialist_indexes):
        self.get_borders(work_time_mean)
        #self.specialist_indexes=specialist_indexes
        self.waited = 0


if __name__ == "main":
    people_generator = People_generator()

    specialists = []
    specialists.append(Specialist(20.0,5.0, 0))
    specialists.append(Specialist(30.0,10.0, 0))
    specialists.append(Specialist(40.0,15.0, 1))

    cpus = []
    cpus.append(Cpu(15))
    cpus.append(Cpu(30))

    people_generator
