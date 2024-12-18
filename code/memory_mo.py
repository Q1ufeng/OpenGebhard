import psutil
import time


def memory_mo(duration):
    interval = 0.5

    times = []
    memory_usages = []

    start_time = time.time()
    last_time = start_time
    while time.time()-start_time < duration:
        memory_usage = psutil.virtual_memory().percent
        if time.time() - last_time > interval:
            times.append(time.time() - start_time)
            memory_usages.append(memory_usage)
            last_time = time.time()
    return times, memory_usages
