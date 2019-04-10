import rng

def model(a, b,  lmbd, dt, t_end, reentry_probability=-1.0):
    times = [0]
    memory_blocks_count = [0]
    times_to_create_next_by_generator = rng.get_uniform_rng(a, b)
    times_to_service_device_done = rng.get_exponential_rng(lmbd) 

    while times[-1] < t_end:
        times_to_create_next_by_generator-=dt

        if memory_blocks_count[-1] >= 1:
            times_to_service_device_done-=dt

        new_memory_blocks_count = memory_blocks_count[-1]

        if times_to_create_next_by_generator <= 0.0:
            new_memory_blocks_count+=1
            times_to_create_next_by_generator = rng.get_uniform_rng(a, b)

        if times_to_service_device_done <= 0.0: 
            if reentry_probability < rng.get_0_1_rng():
                new_memory_blocks_count-=1
            times_to_service_device_done = rng.get_exponential_rng(lmbd)

        memory_blocks_count.append(new_memory_blocks_count)
        times.append(times[-1] + dt)

    memory_blocks_max = max(memory_blocks_count)
    return {'times':times, 'memory_blocks_count':memory_blocks_count, 'memory_blocks_max':memory_blocks_max}