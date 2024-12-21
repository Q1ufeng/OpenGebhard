import psutil
import time
import sys

from SQL_file_writer import SQL_file_writer
from SQL_conductor import SQL_conductor
from concurrent.futures import ThreadPoolExecutor
from monitor import monitor
import pickle
import matplotlib.pyplot as plt

def to_same_length(combined:list ,len:int):
    len2 = int(combined[0])
    slice1 = combined[1:1+len2].extend([0]*(len-len2))
    slice2 = combined[1+len2:1+2*len2].extend([0]*(len-len2))
    slice3 = combined[1+2*len2:1+3*len2].extend([0]*(len-len2))
    return slice1+slice2+slice3
    
    

def main():
    if sys.argv[1] == "write":
        SQL_file_writer("test", int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
        
    elif sys.argv[1] == "exp_pg":
        x = monitor(int(sys.argv[2]),1)
        data_width = len(x[0])
        combined_list = [data_width] + x[1] + x[2] + x[3]
        for i in range(len(x[0])):
            with open('pg_data.pkl'+str(sys.argv[3]),'wb') as f:
                pickle.dump(combined_list,f)
                
    elif sys.argv[1] == "exp_gs":
        x = monitor(int(sys.argv[2]),1)
        data_width = len(x[0])
        combined_list = [data_width] + x[1] + x[2] + x[3]
        for i in range(len(x[0])):
            with open('gs_data.pkl'+str(sys.argv[3]),'wb') as f:
                pickle.dump(combined_list,f)
                
    elif sys.argv[1] == "paint":
        pg_data_1 = []
        pg_data_2 = []
        pg_data_3 = []
        pg_data_4 = []
        pg_data_5 = []
        pg_data_6 = []
        pg_data_7 = []
        pg_data_8 = []
        pg_data_9 = []
        gs_data_1 = []
        gs_data_2 = []
        gs_data_3 = []
        gs_data_4 = []
        gs_data_5 = []
        gs_data_6 = []
        gs_data_7 = []
        gs_data_8 = []
        gs_data_9 = []
        for i in range (9) :
            with open ('pg_data.pkl'+str(i+1),'rb') as f:
                if i==0:
                    pg_data_1 = pickle.load(f)
                elif i==1:
                    pg_data_2 = pickle.load(f)
                elif i==2:
                    pg_data_3 = pickle.load(f)
                elif i==3:
                    pg_data_4 = pickle.load(f)
                elif i==4:
                    pg_data_5 = pickle.load(f)
                elif i==5:
                    pg_data_6 = pickle.load(f)
                elif i==6:
                    pg_data_7 = pickle.load(f)
                elif i==7:
                    pg_data_8 = pickle.load(f)
                elif i==8:
                    pg_data_9 = pickle.load(f)
            with open ('gs_data.pkl'+str(i+1),'rb') as f:
                if i==0:
                    gs_data_1 = pickle.load(f)
                elif i==1:
                    gs_data_2 = pickle.load(f)
                elif i==2:
                    gs_data_3 = pickle.load(f)
                elif i==3:
                    gs_data_4 = pickle.load(f)
                elif i==4:
                    gs_data_5 = pickle.load(f)
                elif i==5:
                    gs_data_6 = pickle.load(f)
                elif i==6:
                    gs_data_7 = pickle.load(f)
                elif i==7:
                    gs_data_8 = pickle.load(f)
                elif i==8:
                    gs_data_9 = pickle.load(f)
                    
            
        for i in range(len(pg_data_1)):
            pg_data_1[i] = float(pg_data_1[i])
        for i in range(len(gs_data_1)):
            gs_data_1[i] = float(gs_data_1[i])
            
        for i in range(len(pg_data_2)):
            pg_data_2[i] = float(pg_data_2[i])
        for i in range(len(gs_data_2)):
            gs_data_2[i] = float(gs_data_2[i])
            
        for i in range(len(pg_data_3)):
            pg_data_3[i] = float(pg_data_3[i])
        for i in range(len(gs_data_3)):
            gs_data_3[i] = float(gs_data_3[i])
            
        for i in range(len(pg_data_4)):
            pg_data_4[i] = float(pg_data_4[i])
        for i in range(len(gs_data_4)):
            gs_data_4[i] = float(gs_data_4[i])
            
        for i in range(len(pg_data_5)):
            pg_data_5[i] = float(pg_data_5[i])
        for i in range(len(gs_data_5)):
            gs_data_5[i] = float(gs_data_5[i])
            
        for i in range(len(pg_data_6)):
            pg_data_6[i] = float(pg_data_6[i])
        for i in range(len(gs_data_6)):
            gs_data_6[i] = float(gs_data_6[i])
            
        for i in range(len(pg_data_7)):
            pg_data_7[i] = float(pg_data_7[i])
        for i in range(len(gs_data_7)):
            gs_data_7[i] = float(gs_data_7[i])
            
        for i in range(len(pg_data_8)):
            pg_data_8[i] = float(pg_data_8[i])
        for i in range(len(gs_data_8)):
            gs_data_8[i] = float(gs_data_8[i])
            
        for i in range(len(pg_data_9)):
            pg_data_9[i] = float(pg_data_9[i])
        for i in range(len(gs_data_9)):
            gs_data_9[i] = float(gs_data_9[i])
            
        len = int(max(pg_data_1[0],pg_data_2[0],pg_data_3[0],pg_data_4[0],pg_data_5[0],pg_data_6[0],pg_data_7[0],pg_data_8[0],pg_data_9[0],gs_data_1[0],gs_data_2[0],gs_data_3[0],gs_data_4[0],gs_data_5[0],gs_data_6[0],gs_data_7[0],gs_data_8[0],gs_data_9[0]))
        
        pg_data_1=to_same_length(pg_data_1,len)
        pg_data_2=to_same_length(pg_data_2,len)
        pg_data_3=to_same_length(pg_data_3,len)
        pg_data_4=to_same_length(pg_data_4,len)
        pg_data_5=to_same_length(pg_data_5,len)
        pg_data_6=to_same_length(pg_data_6,len)
        pg_data_7=to_same_length(pg_data_7,len)
        pg_data_8=to_same_length(pg_data_8,len)
        pg_data_9=to_same_length(pg_data_9,len)        
        gs_data_1=to_same_length(gs_data_1,len)
        gs_data_2=to_same_length(gs_data_2,len)
        gs_data_3=to_same_length(gs_data_3,len)
        gs_data_4=to_same_length(gs_data_4,len)
        gs_data_5=to_same_length(gs_data_5,len)
        gs_data_6=to_same_length(gs_data_6,len)
        gs_data_7=to_same_length(gs_data_7,len)
        gs_data_8=to_same_length(gs_data_8,len)
        gs_data_9=to_same_length(gs_data_9,len)

        times = []
        for i in range(len):
            times.append(i)
            
        pg_avg = []
        gs_avg = []

            
        for i in range(3*len):
            pg_avg.append((pg_data_1[i]+pg_data_2[i]+pg_data_3[i]+pg_data_4[i]+pg_data_5[i]+pg_data_6[i]+pg_data_7[i]+pg_data_8[i]+pg_data_9[i])/9)
            gs_avg.append((gs_data_1[i]+gs_data_2[i]+gs_data_3[i]+gs_data_4[i]+gs_data_5[i]+gs_data_6[i]+gs_data_7[i]+gs_data_8[i]+gs_data_9[i])/9)
        
        pg_cpu_usage_avg = pg_avg[0:len]
        pg_memory_usage_avg = pg_avg[len+1,2*len+1]
        pg_disk_io_speed_avg = pg_avg[2*len+1,3*len+1]
        
        gs_cpu_usage_avg = gs_avg[0:len]
        gs_memory_usage_avg = gs_avg[len+1,2*len+1]
        gs_disk_io_speed_avg = gs_avg[2*len+1,3*len+1]
        
        plt.figure(figsize=(10,6))
        plt.plot(times, pg_cpu_usage_avg,label='Postgres',color='blue')
        plt.plot(times,gs_cpu_usage_avg,label='OpenGauss',color='red')
        plt.title('avg_CPU_usage(%)',fontsize=16)
        plt.xlabel('Time',fontsize=12)
        plt.ylabel('CPU_usage',fontsize=12)
        plt.savefig('/OpenGebhard/code/JPGs/avg_cpu_usage.jpg',format='jpg',dpi=1500)

        plt.figure(figsize=(10,6))
        plt.plot(times, pg_memory_usage_avg,label='Postgres',color='blue')
        plt.plot(times,gs_memory_usage_avg,label='OpenGauss',color='red')
        plt.title('avg_Memory_usage(%)',fontsize=16)
        plt.xlabel('Time',fontsize=12)
        plt.ylabel('Memory_usage',fontsize=12)
        plt.savefig('/OpenGebhard/code/JPGs/avg_memory_usage.jpg',format='jpg',dpi=1500)

        plt.figure(figsize=(10,6))
        plt.plot(times, pg_disk_io_speed_avg,label='Postgres',color='blue')
        plt.plot(times,gs_disk_io_speed_avg,label='OpenGauss',color='red')
        plt.title('avg_Disk_io_speed(Mb/s)',fontsize=16)
        plt.xlabel('Time',fontsize=12)
        plt.ylabel('Disk_io_speed',fontsize=12)
        plt.savefig('/OpenGebhard/code/JPGs/avg_disk_io_speed.jpg',format='jpg',dpi=1500)

if __name__ == "__main__":
    main()
