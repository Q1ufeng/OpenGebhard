import psutil
import time


def monitor(duration, interval):
    times = []
    cpu_usages = []
    memory_usages = []
    disk_io_speeds = []

    prev_disk_io = psutil.disk_io_counters()
    prev_io_sum = prev_disk_io.read_bytes + prev_disk_io.write_bytes

    start_time = time.time()
    last_time = start_time
    while time.time() - start_time < duration:
        memory_usage = psutil.virtual_memory().percent

        if time.time() - last_time > interval:
            memory_usages.append(memory_usage)

            curr_disk_io = psutil.disk_io_counters()
            curr_io_sum = curr_disk_io.read_bytes + curr_disk_io.write_bytes
            io_speed = (curr_io_sum - prev_io_sum) / ((time.time() - last_time) * 1024 * 1024)
            prev_io_sum = curr_io_sum
            times.append(time.time() - start_time)
            disk_io_speeds.append(io_speed)

            cpu_usage = psutil.cpu_percent(interval=None)
            cpu_usages.append(cpu_usage)

            last_time = time.time()
    return times, cpu_usages, memory_usages, disk_io_speeds
