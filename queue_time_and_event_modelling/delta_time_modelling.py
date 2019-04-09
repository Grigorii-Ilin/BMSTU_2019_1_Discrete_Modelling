import rng

def model(a, b,  lmbd, dt, t_end, reentry_probability=-1.0):
    times = [0,]
    memory_blocks_count_by_dt = [0,]
    #memory_blocks_max=0
    times_to_create_next_by_generator = rng.get_uniform_rng(a, b)
    times_to_service_device_done = rng.get_exponential_rng(lmbd) #0.0
    #is_service_device_working = False

    while times[-1] < t_end:
        times_to_create_next_by_generator-=dt

        if memory_blocks_count_by_dt[-1]>=1:
            times_to_service_device_done-=dt

        new_memory_blocks_count = memory_blocks_count_by_dt[-1]

        if times_to_create_next_by_generator <= 0.0:
            new_memory_blocks_count+=1
            times_to_create_next_by_generator = rng.get_uniform_rng(a, b)

        if times_to_service_device_done <= 0.0: #and memory_blocks_count_by_dt[-1]>=1:
            if reentry_probability < rng.get_0_1_rng():
                new_memory_blocks_count-=1
            times_to_service_device_done = rng.get_exponential_rng(lmbd)

            #if is_service_device_working:
            #    is_service_device_working = False
            #    if reentry_probability < rng.get_0_1_rng():
            #        new_memory_blocks_count-=1
            #else:
            #    if new_memory_blocks_count >= 1:
            #        is_service_device_working = True
            #        times_to_service_device_done = rng.get_exponential_rng(lmbd)

        memory_blocks_count_by_dt.append(new_memory_blocks_count)
        #memory_blocks_max=max(memory_blocks_count_by_dt[-1], memory_blocks_max)
        times.append(times[-1] + dt)

        #print(times_to_create_next_by_generator, times_to_service_device_done, new_memory_blocks_count)#, is_service_device_working)

    memory_blocks_max = max(memory_blocks_count_by_dt)
    return times, memory_blocks_count_by_dt, memory_blocks_max