import psutil
import time


# kB/s
def diskio_mo(duration):
    interval = 0.5

    times = []
    iospeeds = []

    prev_disk_io = psutil.disk_io_counters()
    prev_io_sum = prev_disk_io.read_bytes + prev_disk_io.write_bytes

    start_time = time.time()
    last_time = start_time

    while time.time() - start_time < duration:
        if time.time() - last_time > interval:
            curr_disk_io = psutil.disk_io_counters()
            curr_io_sum = curr_disk_io.read_bytes + curr_disk_io.write_bytes
            iospeed = (curr_io_sum - prev_io_sum) / 512
            times.append(time.time() - start_time)
            iospeeds.append(iospeed)
            last_time = time.time()

    return times, iospeeds
