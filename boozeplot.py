import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import datetime as dt

def boozeplot():
    time = []
    temps = [[],[],[],[],[],[]]
    with open("temps.log", 'r') as f:
        for line in f:
            samples = line.split(',')
            for x in range(6):
                temps[x].append(samples[x+1])
            time.append(dt.datetime.strptime(samples[0],"%c"))

    plt.plot_date(time, temps[0], '-', label = "Fridge chamber")
    plt.plot_date(time, temps[1], '-', label = "Freezer chamber")
    plt.plot_date(time, temps[2], '-', label = "Hefeweizen")
    plt.plot_date(time, temps[3], '-', label = "Pilsner")
    plt.title("Ozerato Temps")
    plt.xlabel("Time")
    plt.ylabel("Temperature (F)")
    plt.grid(True)
    plt.legend()
    plt.show()
    
    
    
    
            
            
