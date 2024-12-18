import psutil
import time


def cpu_mo(duration):
    interval = 0.5

    times = []
    cpu_usages = []

    start_time = time.time()
    last_time = start_time
    while time.time()-start_time < duration:
        if time.time() - last_time > interval:
            times.append(time.time()-start_time)
            cpu_usage = psutil.cpu_percent(interval=None)
            cpu_usages.append(cpu_usage)
            last_time = time.time()

    return times, cpu_usages
