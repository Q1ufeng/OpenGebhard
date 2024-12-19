import psutil
import time

def monitor(duration,interval) :
    times = []
    cpu_usages = []
    memory_usages = []
    disk_usages = []
    disk_io_speeds = []

    usage = psutil.disk_usage("F:")
    diskusage0 = usage.used / (1024 ** 2)

    prev_disk_io = psutil.disk_io_counters()
    prev_io_sum = prev_disk_io.read_bytes + prev_disk_io.write_bytes


    start_time = time.time()
    last_time = start_time
    while time.time()-start_time < duration:
        memory_usage = psutil.virtual_memory().percent

        if time.time() - last_time > interval:
            times.append(time.time() - start_time)

            usage = psutil.disk_usage("F:")
            diskusage = usage.used / (1024 ** 2) - diskusage0
            disk_usages.append(diskusage)

            memory_usages.append(memory_usage)

            curr_disk_io = psutil.disk_io_counters()
            curr_io_sum = curr_disk_io.read_bytes + curr_disk_io.write_bytes
            io_speed = (curr_io_sum - prev_io_sum) / 512
            times.append(time.time() - start_time)
            disk_io_speeds.append(io_speed)

            cpu_usage = psutil.cpu_percent(interval=None)
            cpu_usages.append(cpu_usage)

            last_time = time.time()
    return times,cpu_usages,memory_usages,disk_usages,disk_io_speeds