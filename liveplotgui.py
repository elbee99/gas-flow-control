from alicat_flowmeter_control import flow_control
from alicat import FlowController

flow_controller_O2 = FlowController(port='COM3')
flow_controller_Ar = FlowController(port='COM5')

flow_controller_O2.set_gas('O2')
flow_controller_Ar.set_gas('Ar')

import tkinter as tk
from tkinter import simpledialog
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
plt.ioff()
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import datetime
#fixed flow rate/oxygen concentration control
def main():
    
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    # app frame
    app = ctk.CTk()
    bv1=ctk.BooleanVar(value=False)
    setpoint=ctk.StringVar(value='0')
    app.geometry("800x800")
    app.title("Flow Control")
    GUIfont = ctk.CTkFont(family="Arial", size=12, weight="normal")

    def stopplotting():
        bv1.set(0)
        print(bv1.get())
    def plotting():
        bv1.set(1)
        oxygen_plotting()
        print(bv1.get())
    #Stop button
    app.run_button = ctk.CTkButton(app, text="Stop",border_color="dark-blue", command=stopplotting)
    app.run_button.grid(row=10,column=0,columnspan=1,padx=20,pady=5)

    #Start button
    app.run_button = ctk.CTkButton(app, text="Start",border_color="dark-blue", command=plotting)
    app.run_button.grid(row=10,column=1,columnspan=1,padx=20,pady=5)

    
    # generate the figure and plot object which will be linked to the root element
    from oxygen_sensor import read_O2_sensor

    # opens the COM3 port which is what the O2 sensor was when I plugged it in
    # check to see if it is COM3 before running
    # Will try optimise so it selects automatically soon
    start_time = time.time()
    fig, ax = plt.subplots()
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('O$_2$ conc. (%)')
    line, = ax.plot([],[])
    canvas = FigureCanvasTkAgg(fig,master=app)
    canvas.get_tk_widget().grid(row=0, column=0,  rowspan=9, columnspan=2, padx=(20, 5), pady=(100, 5), sticky="ew")
    
    def oxygen_plotting(filename='oxygen_conc.txt'):
        """
        Reads the oxygen sensor, records the data over time in a text file
        and plots the data in real time
        Args:
            filename (str, optional): Relative or absolute path to the desired 
            file location of oxygen sensor data. Defaults to 'oxygen_conc.txt'.
        """
        
        with open(filename, 'w') as f:
            
            f.write('Start time=\t{}\n'.format(datetime.datetime.now()))
            f.write('Time (s)\tO2 conc. (ppm)\n')

            

            oxygen_ppm = read_O2_sensor()
            print(oxygen_ppm)
            oxygen_percent=float(oxygen_ppm)/10e3
            current_time = time.time()-start_time 
            data_line = str("{:.2f}".format(current_time))+'\t'+oxygen_ppm

            xdata, ydata = line.get_xdata(),line.get_ydata()
            xdata = np.append(xdata,current_time)
            ydata = np.append(ydata,float(oxygen_ppm)/10e3)
            setpointstring=setpoint.get()
            setpoint_line = np.ones(len(xdata))*float(setpointstring)
            ax.plot(xdata,setpoint_line,'r--')
            line.set_data(xdata,ydata)
            ax.relim()
            ax.autoscale_view()

            fig.canvas.flush_events()
            canvas = FigureCanvasTkAgg(fig,master=app)
            canvas.get_tk_widget().grid(row=0, column=0,  rowspan=9, columnspan=2, padx=(20, 5), pady=(100, 5), sticky="ew")
            
            f.write(data_line)
            f.write('\n')

            if bv1.get() == True:
                plottingqueue = app.after(100000,oxygen_plotting())
            else:
                app.after_cancel(plottingqueue)
    app.mainloop()


if __name__ == "__main__":
    main()