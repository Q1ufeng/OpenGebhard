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
import pickle
import matplotlib.pyplot as plt

def main():
    if sys.argv[1] == "write":
        SQL_file_writer("test", int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    elif sys.argv[1] == "exp_pg":
        x = monitor(int(sys.argv[2]),1)
        data_width = len(x[0])
        combined_list = [data_width] + x[1] + x[2] + x[3]
        for i in range(len(x[0])):
            with open('pg_data.pkl','wb') as f:
                pickle.dump(combined_list,f)
    elif sys.argv[1] == "exp_gs":
        x = monitor(int(sys.argv[2]),1)
        data_width = len(x[0])
        combined_list = [data_width] + x[1] + x[2] + x[3]
        for i in range(len(x[0])):
            with open('gs_data.pkl','wb') as f:
                pickle.dump(combined_list,f)
    elif sys.argv[1] == "paint":
        with open ('pg_data.pkl','rb') as f:
            pg_data = pickle.load(f)
        with open('gs_data.pkl','rb') as f:
            gs_data = pickle.load(f)
        data_width_pg = int(pg_data[3])
        data_width_gs = int(gs_data[3])
        pg_insert_num = int(pg_data[0])
        gs_insert_num = int(gs_data[0])
        pg_transaction_num = int(pg_data[1])
        gs_transaction_num = int(gs_data[1])
        pg_insert_speed = round(float(pg_data[0])/int(pg_data[2]),3)
        gs_insert_speed = round(float(gs_data[0])/int(gs_data[2]),3)
        pg_transaction_speed = round(float(pg_data[1])/int(pg_data[2]),3)
        gs_transaction_speed = round(float(gs_data[1])/int(gs_data[2]),3)
        for i in range(len(pg_data)):
            pg_data[i] = float(pg_data[i])
        for i in range(len(gs_data)):
            gs_data[i] = float(gs_data[i])
        pg_cpu_usage = pg_data[1:1+data_width_pg]
        pg_memory_usage = pg_data[1+data_width_pg:1+2*data_width_pg]
        pg_disk_io_speed = pg_data[1+2*data_width_pg:1+3*data_width_pg]
        gs_cpu_usage = gs_data[1:1+data_width_gs]
        gs_memory_usage = gs_data[1+data_width_gs:1+2*data_width_gs]
        gs_disk_io_speed = gs_data[1+2*data_width_gs:1+3*data_width_gs]
        times = []
        for i in range(max(data_width_pg, data_width_gs)):
            times.append(i+1)
        if (data_width_pg<data_width_gs):
            pg_cpu_usage.extend([0] * (data_width_gs-data_width_pg))
            pg_memory_usage.extend([0] * (data_width_gs-data_width_pg))
            pg_disk_io_speed.extend([0] * (data_width_gs-data_width_pg))
        elif (data_width_gs<data_width_pg):
            gs_cpu_usage.extend([0] * (data_width_pg-data_width_gs))
            gs_memory_usage.extend([0] * (data_width_pg-data_width_gs))
            gs_disk_io_speed.extend([0] * (data_width_pg-data_width_gs))

        plt.figure(figsize=(10,6))
        plt.plot(times, pg_cpu_usage,label='Postgres',color='blue')
        plt.plot(times,gs_cpu_usage,label='OpenGauss',color='red')
        plt.title('CPU_usage(%)',fontsize=16)
        plt.xlabel('Time',fontsize=12)
        plt.ylabel('CPU_usage',fontsize=12)
        plt.savefig('/OpenGebhard/code/JPGs/cpu_usage.jpg',format='jpg',dpi=600)

        plt.figure(figsize=(10,6))
        plt.plot(times, pg_memory_usage,label='Postgres',color='blue')
        plt.plot(times,gs_memory_usage,label='OpenGauss',color='red')
        plt.title('Memory_usage(%)',fontsize=16)
        plt.xlabel('Time',fontsize=12)
        plt.ylabel('Memory_usage',fontsize=12)
        plt.savefig('/OpenGebhard/code/JPGs/memory_usage.jpg',format='jpg',dpi=600)

        plt.figure(figsize=(10,6))
        plt.plot(times, pg_disk_io_speed,label='Postgres',color='blue')
        plt.plot(times,gs_disk_io_speed,label='OpenGauss',color='red')
        plt.title('Disk_io_speed(Mb/s)',fontsize=16)
        plt.xlabel('Time',fontsize=12)
        plt.ylabel('Disk_io_speed',fontsize=12)
        plt.savefig('/OpenGebhard/code/JPGs/disk_io_speed.jpg',format='jpg',dpi=600)

if __name__ == "__main__":
    main()
