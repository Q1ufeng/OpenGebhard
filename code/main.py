import psutil
import time
import sys

from SQL_file_writer import SQL_file_writer
from SQL_conductor import SQL_conductor
from concurrent.futures import ThreadPoolExecutor
from monitor import monitor
import pickle
import matplotlib.pyplot as plt

def to_same_length(combined = [],lenm = 0):
    print(combined[0])
    print(lenm)
    print(len(combined))
    len2 = int(combined[0])
    slice1 = combined[1:1+len2]+([0]*(lenm-len2))
    slice2 = combined[1+len2:1+2*len2]+([0]*(lenm-len2))
    slice3 = combined[1+2*len2:1+3*len2]+([0]*(lenm-len2))
    return slice1+slice2+slice3
    
    

def main():
    if sys.argv[1] == "write":
        SQL_file_writer("test", int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
        
    elif sys.argv[1] == "exp_pg":
        x = monitor(int(sys.argv[2]),1)
        data_width = len(x[0])
        combined_list = [data_width] + x[1] + x[2] + x[3]
        for i in range(len(x[0])):
            with open('../PKLs/pg_data.pkl'+str(sys.argv[3]),'wb') as f:
                pickle.dump(combined_list,f)
                
    elif sys.argv[1] == "exp_gs":
        x = monitor(int(sys.argv[2]),1)
        data_width = len(x[0])
        combined_list = [data_width] + x[1] + x[2] + x[3]
        for i in range(len(x[0])):
            with open('../PKLs/gs_data.pkl'+str(sys.argv[3]),'wb') as f:
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
            with open ('../PKLs/pg_data.pkl'+str(i+1),'rb') as f:
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
            with open ('../PKLs/gs_data.pkl'+str(i+1),'rb') as f:
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
            
        lenm = int(max(pg_data_1[0],pg_data_2[0],pg_data_3[0],pg_data_4[0],pg_data_5[0],pg_data_6[0],pg_data_7[0],pg_data_8[0],pg_data_9[0],gs_data_1[0],gs_data_2[0],gs_data_3[0],gs_data_4[0],gs_data_5[0],gs_data_6[0],gs_data_7[0],gs_data_8[0],gs_data_9[0]))
        
        pg_data_1=to_same_length(pg_data_1,lenm)
        pg_data_2=to_same_length(pg_data_2,lenm)
        pg_data_3=to_same_length(pg_data_3,lenm)
        pg_data_4=to_same_length(pg_data_4,lenm)
        pg_data_5=to_same_length(pg_data_5,lenm)
        pg_data_6=to_same_length(pg_data_6,lenm)
        pg_data_7=to_same_length(pg_data_7,lenm)
        pg_data_8=to_same_length(pg_data_8,lenm)
        pg_data_9=to_same_length(pg_data_9,lenm)        
        gs_data_1=to_same_length(gs_data_1,lenm)
        gs_data_2=to_same_length(gs_data_2,lenm)
        gs_data_3=to_same_length(gs_data_3,lenm)
        gs_data_4=to_same_length(gs_data_4,lenm)
        gs_data_5=to_same_length(gs_data_5,lenm)
        gs_data_6=to_same_length(gs_data_6,lenm)
        gs_data_7=to_same_length(gs_data_7,lenm)
        gs_data_8=to_same_length(gs_data_8,lenm)
        gs_data_9=to_same_length(gs_data_9,lenm)

        times = []
        for i in range(lenm):
            times.append(i)
            
        pg_avg = []
        gs_avg = []
        pg_var = []
        gs_var = []

            
        for i in range(3*lenm):
            pg_avg.append((pg_data_1[i]+pg_data_2[i]+pg_data_3[i]+pg_data_4[i]+pg_data_5[i]+pg_data_6[i]+pg_data_7[i]+pg_data_8[i]+pg_data_9[i])/9)
            gs_avg.append((gs_data_1[i]+gs_data_2[i]+gs_data_3[i]+gs_data_4[i]+gs_data_5[i]+gs_data_6[i]+gs_data_7[i]+gs_data_8[i]+gs_data_9[i])/9)
            pg_mean = (pg_data_1[i]+pg_data_2[i]+pg_data_3[i]+pg_data_4[i]+pg_data_5[i]+pg_data_6[i]+pg_data_7[i]+pg_data_8[i]+pg_data_9[i])/9
            gs_mean = (gs_data_1[i]+gs_data_2[i]+gs_data_3[i]+gs_data_4[i]+gs_data_5[i]+gs_data_6[i]+gs_data_7[i]+gs_data_8[i]+gs_data_9[i])/9
            pg_var.append(((pg_data_1[i]-pg_mean)**2+(pg_data_2[i]-pg_mean)**2+(pg_data_3[i]-pg_mean)**2+(pg_data_4[i]-pg_mean)**2+(pg_data_5[i]-pg_mean)**2+(pg_data_6[i]-pg_mean)**2+(pg_data_7[i]-pg_mean)**2+(pg_data_8[i]-pg_mean)**2+(pg_data_9[i]-pg_mean)**2)/9)
            gs_var.append(((gs_data_1[i]-gs_mean)**2+(gs_data_2[i]-gs_mean)**2+(gs_data_3[i]-gs_mean)**2+(gs_data_4[i]-gs_mean)**2+(gs_data_5[i]-gs_mean)**2+(gs_data_6[i]-gs_mean)**2+(gs_data_7[i]-gs_mean)**2+(gs_data_8[i]-gs_mean)**2+(gs_data_9[i]-gs_mean)**2)/9)
        
        pg_cpu_usage_avg = pg_avg[0:lenm]
        pg_memory_usage_avg = pg_avg[lenm:2*lenm]
        pg_disk_io_speed_avg = pg_avg[2*lenm:3*lenm]
        
        pg_cpu_usage_var = pg_var[0:lenm]
        pg_memory_usage_var = pg_var[lenm:2*lenm]
        pg_disk_io_speed_var = pg_var[2*lenm:3*lenm]
        
        gs_cpu_usage_avg = gs_avg[0:lenm]
        gs_memory_usage_avg = gs_avg[lenm:2*lenm]
        gs_disk_io_speed_avg = gs_avg[2*lenm:3*lenm]
        
        gs_cpu_usage_var = gs_var[0:lenm]
        gs_memory_usage_var = gs_var[lenm:2*lenm]
        gs_disk_io_speed_var = gs_var[2*lenm:3*lenm]
        
        plt.figure(figsize=(10,6))
        plt.plot(times, pg_cpu_usage_avg,label='Postgres',color='blue')
        plt.plot(times,gs_cpu_usage_avg,label='OpenGauss',color='red')
        plt.title('avg_CPU_usage(%)',fontsize=16)
        plt.xlabel('Time',fontsize=12)
        plt.ylabel('CPU_usage',fontsize=12)
        plt.savefig('../JPGs/avg_cpu_usage.jpg',format='jpg',dpi=1500)

        plt.figure(figsize=(10,6))
        plt.plot(times, pg_memory_usage_avg,label='Postgres',color='blue')
        plt.plot(times,gs_memory_usage_avg,label='OpenGauss',color='red')
        plt.title('avg_Memory_usage(%)',fontsize=16)
        plt.xlabel('Time',fontsize=12)
        plt.ylabel('Memory_usage',fontsize=12)
        plt.savefig('../JPGs/avg_memory_usage.jpg',format='jpg',dpi=1500)

        plt.figure(figsize=(10,6))
        print("times: "+str(len(times)))
        print("avg: "+str(len(pg_disk_io_speed_avg)))
        plt.plot(times, pg_disk_io_speed_avg,label='Postgres',color='blue')
        plt.plot(times,gs_disk_io_speed_avg,label='OpenGauss',color='red')
        plt.title('avg_Disk_io_speed(Mb/s)',fontsize=16)
        plt.xlabel('Time',fontsize=12)
        plt.ylabel('Disk_io_speed',fontsize=12)
        plt.savefig('../JPGs/avg_disk_io_speed.jpg',format='jpg',dpi=1500)
        
        plt.figure(figsize=(10,6))
        plt.plot(times, pg_cpu_usage_var,label='Postgres',color='blue')
        plt.plot(times,gs_cpu_usage_var,label='OpenGauss',color='red')
        plt.title('var_CPU_usage',fontsize=16)
        plt.xlabel('Time',fontsize=12)
        plt.ylabel('CPU_usage',fontsize=12)
        plt.savefig('../JPGs/var_cpu_usage.jpg',format='jpg',dpi=1500)

        plt.figure(figsize=(10,6))
        plt.plot(times, pg_memory_usage_var,label='Postgres',color='blue')
        plt.plot(times,gs_memory_usage_var,label='OpenGauss',color='red')
        plt.title('var_Memory_usage',fontsize=16)
        plt.xlabel('Time',fontsize=12)
        plt.ylabel('Memory_usage',fontsize=12)
        plt.savefig('../JPGs/var_memory_usage.jpg',format='jpg',dpi=1500)

        plt.figure(figsize=(10,6))
        plt.plot(times, pg_disk_io_speed_var,label='Postgres',color='blue')
        plt.plot(times,gs_disk_io_speed_var,label='OpenGauss',color='red')
        plt.title('var_Disk_io_speed',fontsize=16)
        plt.xlabel('Time',fontsize=12)
        plt.ylabel('Disk_io_speed',fontsize=12)
        plt.savefig('../JPGs/var_disk_io_speed.jpg',format='jpg',dpi=1500)

if __name__ == "__main__":
    main()
