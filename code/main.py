import psutil
import time
from cpu_mo import cpu_mo
from diskio_mo import diskio_mo
from diskusage_mo import diskusage_mo
from memory_mo import memory_mo
from SQL_conductor import SQL_conductor
from concurrent.futures import ThreadPoolExecutor
from monitor import monitor

def main():
    SQL_conductor()
    #x = monitor(5,1)
    #for i in range(3):
    #    print("time:"+str(x[0][i])+"cpu:"+str(x[1][i])+"memory:"+str(x[2][i])+"disk:"+str(x[3][i])+"io:"+str(x[4][i]))

if __name__ == "__main__":
    main()
