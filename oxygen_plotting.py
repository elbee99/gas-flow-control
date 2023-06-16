import serial
import time
import datetime
import matplotlib.pyplot as plt

import numpy as np
from oxygen_sensor import read_O2_sensor

# opens the COM3 port which is what the O2 sensor was when I plugged it in
# check to see if it is COM3 before running
# Will try optimise so it selects automatically soon
def oxygen_plotting(filename='oxygen_conc.txt'):
    """
    Reads the oxygen sensor, records the data over time in a text file
    and plots the data in real time
    Args:
        filename (str, optional): Relative or absolute path to the desired 
        file location of oxygen sensor data. Defaults to 'oxygen_conc.txt'.
    """
    with open(filename, 'w') as f:
        start_time = time.time()
        fig, ax = plt.subplots()
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('O$_2$ conc. (%)')
        line, = ax.plot([],[])
        f.write('Start time=\t{}\n'.format(datetime.datetime.now()))
        f.write('Time (s)\tO2 conc. (ppm)\n')
        while True:
            oxygen_ppm = read_O2_sensor()
            print(oxygen_ppm)
            oxygen_percent=float(oxygen_ppm)/10e3
            current_time = time.time()-start_time 
            data_line = str("{:.2f}".format(current_time))+'\t'+oxygen_ppm

            xdata, ydata = line.get_xdata(),line.get_ydata()
            xdata = np.append(xdata,current_time)
            ydata = np.append(ydata,float(oxygen_ppm)/10e3)

            line.set_data(xdata,ydata)
            ax.relim()
            ax.autoscale_view()

            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.1)
            f.write(data_line)
            f.write('\n')

if __name__ == "__main__":
    oxygen_plotting()
