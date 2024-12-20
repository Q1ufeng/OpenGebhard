import psutil
import time

from SQL_file_writer import SQL_file_writer
from cpu_mo import cpu_mo
from diskio_mo import diskio_mo
from diskusage_mo import diskusage_mo
from memory_mo import memory_mo
from SQL_conductor import SQL_conductor
from concurrent.futures import ThreadPoolExecutor
from monitor import monitor

def main():
    SQL_file_writer("test",10,30,5000)
    x = monitor(100,1)
    for i in range(len(x[0])):
        print("time:"+str(x[0][i])+" cpu:"+str(x[1][i])+" memory:"+str(x[2][i])+" io:"+str(x[3][i]))

if __name__ == "__main__":
    main()
