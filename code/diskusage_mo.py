import psutil
import time


# Mb

def diskusage_mo(duration):
    interval = 0.5

    times = []
    diskusages = []

    usage = psutil.disk_usage("F:")
    diskusage0 = usage.used / (1024 ** 2)

    start_time = time.time()
    last_time = start_time
    while time.time() - start_time < duration:
        if time.time() - last_time > interval:
            times.append(time.time() - start_time)
            usage = psutil.disk_usage("F:")
            diskusage = usage.used / (1024 ** 2) - diskusage0
            diskusages.append(diskusage)
            last_time = time.time()

    print(diskusage0)
    return times, diskusages