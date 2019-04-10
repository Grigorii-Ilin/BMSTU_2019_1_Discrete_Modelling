import rng

GENERATOR = 0
SERVICE_DEVICE = 1
STATISTIC_TIME = 2
END_TIME = 3

ACTIVITIES_COUNT = 4


def get_start_params(a, b, lmbd, t_end):
    sbs = [0.0 for _ in range(ACTIVITIES_COUNT)]
    sbs[GENERATOR] = rng.get_uniform_rng(a, b)
    sbs[SERVICE_DEVICE] = sbs[GENERATOR] + rng.get_exponential_rng(lmbd)
    sbs[STATISTIC_TIME] = 0.0
    sbs[END_TIME] = t_end + 0.0001

    queue_length = 0
    times = []
    memory_blocks_count = []

    return sbs, queue_length, times, memory_blocks_count


def get_current_activity_and_time(sbs):
    activity_current = GENERATOR
    time_current = sbs[activity_current]

    for activity in range(SERVICE_DEVICE, ACTIVITIES_COUNT):
        if sbs[activity] <= time_current:
            activity_current = activity
            time_current = sbs[activity_current]

    return activity_current, time_current


def model(a, b,  lmbd, dt, t_end, reentry_prob=0.0):
    sbs, queue_length, times, memory_blocks_count = get_start_params(a, b, lmbd, t_end)

    while True:
        activity_current, time_current = get_current_activity_and_time(sbs)

        if activity_current == GENERATOR:
            queue_length+=1
            sbs[GENERATOR] = time_current + rng.get_uniform_rng(a, b)

        elif activity_current == SERVICE_DEVICE:
            if reentry_prob < rng.get_0_1_rng():
                queue_length-=1

            shift_from_start_time = sbs[GENERATOR] if queue_length == 0 else time_current
            sbs[SERVICE_DEVICE] = shift_from_start_time + rng.get_exponential_rng(lmbd)

        elif activity_current == STATISTIC_TIME:
            memory_blocks_count.append(queue_length)
            times.append(time_current)
            sbs[STATISTIC_TIME] = time_current + dt

        elif activity_current == END_TIME:
            break

    memory_blocks_max = max(memory_blocks_count)
    return {'times':times, 'memory_blocks_count':memory_blocks_count, 'memory_blocks_max':memory_blocks_max}