import rng
#from enum import Enum

#class Activities(Enum):
GENERATOR = 0
SERVICE_DEVICE = 1
STATISTIC_TIME = 2
END_TIME = 3

ACTIVITIES_COUNT = 4


def get_start_sbs(a, b, lmbd, dt, t_end):
    sbs = [0.0 for _ in range(ACTIVITIES_COUNT)]

    sbs[GENERATOR] = rng.get_uniform_rng(a, b)
    sbs[SERVICE_DEVICE] = sbs[GENERATOR] + rng.get_exponential_rng(lmbd)
    sbs[STATISTIC_TIME] = 0.0
    sbs[END_TIME] = t_end+0.0001

    return sbs


def model(a, b,  lmbd, dt, t_end, reentry_probability=-1.0):
    sbs = get_start_sbs(a, b, lmbd, dt, t_end)
    #generated_count = 0
    #serviced_count = 0
    queue_length = 0
    #time_current = 0.0
    times = []
    memory_blocks_count = []

    while True:
        current_activity = GENERATOR
        time_current = sbs[current_activity]

        for activity in range(SERVICE_DEVICE, ACTIVITIES_COUNT):
            if sbs[activity] <= time_current:
                time_current = sbs[activity]
                current_activity = activity



        if current_activity == GENERATOR:
            #time_current=sbs[GENERATOR]
            #generated_count+=1
            queue_length+=1
            sbs[GENERATOR] = time_current + rng.get_uniform_rng(a, b)

        elif current_activity == SERVICE_DEVICE:
            #time_current=sbs[SERVICE_DEVICE]

            if reentry_probability < rng.get_0_1_rng():
                queue_length-=1
            #else:
            #    print("re-entry")

            #sbs[SERVICE_DEVICE] = time_current + rng.get_exponential_rng(lmbd)
            #if queue_length == 0:
            #    sbs[SERVICE_DEVICE]+=sbs[GENERATOR]

            if queue_length == 0:
                sbs[SERVICE_DEVICE] = sbs[GENERATOR] + rng.get_exponential_rng(lmbd)
            elif queue_length >= 1:
                sbs[SERVICE_DEVICE] = time_current + rng.get_exponential_rng(lmbd)

        elif current_activity == STATISTIC_TIME:
            #time_current=sbs[STATISTIC_TIME]
            memory_blocks_count.append(queue_length)
            times.append(time_current)
            sbs[STATISTIC_TIME] = time_current + dt

        elif current_activity == END_TIME:
            break

        #print(sbs)
        #print(current_activity, queue_length, time_current )

    memory_blocks_max = max(memory_blocks_count)
    return times, memory_blocks_count, memory_blocks_max