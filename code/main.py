import psutil
import time
import sys

from SQL_file_writer import SQL_file_writer
from cpu_mo import cpu_mo
from diskio_mo import diskio_mo
from diskusage_mo import diskusage_mo
from memory_mo import memory_mo
from SQL_conductor import SQL_conductor
from concurrent.futures import ThreadPoolExecutor
from monitor import monitor

def main():
    if sys.argv[1] == "write":
        SQL_file_writer("test", sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "monitor":
        x = monitor(sys.argv[2],sys.argv[3])
        for i in range(len(x[0])):
            print("time:"+str(x[0][i])+" cpu:"+str(x[1][i])+" memory:"+str(x[2][i])+" io:"+str(x[3][i]))

if __name__ == "__main__":
    main()
