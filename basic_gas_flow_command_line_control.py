from alicat import FlowController
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
    app.geometry("1200x800")
    app.title("Flow Control")
    GUIfont = ctk.CTkFont(family="Arial", size=12, weight="normal")

    # argon flow rate
    app.ArFlow_label = ctk.CTkLabel(app, text="Argon Flow Rate", font=GUIfont)
    app.ArFlow_label.grid(row=0, column=0, padx=(20, 5), pady=(100, 5), sticky="ew")
    app.ArFlow_entry = ctk.CTkEntry(app, placeholder_text="30.00-100.00", border_color="white", validate="key")
    app.ArFlow_entry.grid(row=0, column=2, columnspan=1, padx=5, pady=(100, 5), sticky="ew")
    app.ArFlow_unit_label = ctk.CTkLabel(app, text="sccm", font=GUIfont)
    app.ArFlow_unit_label.grid(row=0, column=3, padx=(5, 20), pady=(100, 5), sticky="ew")

    # oxygen flow rate
    app.O2Flow_label = ctk.CTkLabel(app, text="Oxygen Flow Rate", font=GUIfont)
    app.O2Flow_label.grid(row=2, column=0, padx=(20, 5), pady=5, sticky="ew")
    app.O2Flow_entry = ctk.CTkEntry(app, placeholder_text="0.00-30.00", border_color="white", validate="key")
    app.O2Flow_entry.grid(row=2, column=2, columnspan=1, padx=5, sticky="ew")
    app.O2Flow_unit_label = ctk.CTkLabel(app, text="sccm", font=GUIfont)
    app.O2Flow_unit_label.grid(row=2, column=3, padx=(5, 20), pady=(10, 5), sticky="ew")
   
    #Update Button
    app.run_button = ctk.CTkButton(app, text="Update",border_color="dark-blue")
    app.run_button.grid(row=3,column=0,columnspan=4,padx=20,pady=5)

    #oxygen percentage
    app.O2End_label = ctk.CTkLabel(app, text="Oxygen % Concentration", font=GUIfont)
    app.O2End_label.grid(row=4, column=0, padx=(20, 5), pady=5, sticky="ew")
    app.O2End_entry = ctk.CTkEntry(app, placeholder_text="0.00-30.00", border_color="white", validate="key")
    app.O2End_entry.grid(row=4, column=2, columnspan=1, padx=5, sticky="ew")
    app.O2End_unit_label = ctk.CTkLabel(app, text="%", font=GUIfont)
    app.O2End_unit_label.grid(row=4, column=3, padx=(5, 20), pady=(10, 5), sticky="ew") 
    def updatesetpoint():
        setpoint.set(app.O2End_entry.get())
        print(setpoint)
    #Update Button
    app.run_button = ctk.CTkButton(app, text="Update",border_color="dark-blue", command=updatesetpoint)
    app.run_button.grid(row=5,column=0,columnspan=4,padx=20,pady=5)
    def stopplotting():
        bv1.set(0)
        print(bv1.get())
    def plotting():
        bv1.set(1)
        oxygen_plotting()
        print(bv1.get())
    #Stop button
    app.run_button = ctk.CTkButton(app, text="Stop",border_color="dark-blue", command=stopplotting)
    app.run_button.grid(row=10,column=6,columnspan=1,padx=20,pady=5)

    #Start button
    app.run_button = ctk.CTkButton(app, text="Start",border_color="dark-blue", command=plotting)
    app.run_button.grid(row=10,column=7,columnspan=1,padx=20,pady=5)

    
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
    canvas.get_tk_widget().grid(row=0, column=6,  rowspan=9, columnspan=2, padx=(20, 5), pady=(100, 5), sticky="ew")
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
            canvas.get_tk_widget().grid(row=0, column=6,  rowspan=9, columnspan=2, padx=(20, 5), pady=(100, 5), sticky="ew")
            
            f.write(data_line)
            f.write('\n')
            if bv1.get() == True:
                plottingqueue = app.after(100000,oxygen_plotting())
            else:
                app.after_cancel(plottingqueue)
    
    app.mainloop()
        

    # flow_controller_O2 = FlowController(port='COM3')
    # flow_controller_Ar = FlowController(port='COM5')

    # print(flow_controller_O2.get())
    # print(flow_controller_Ar.get())

    # flow_controller_O2.set_gas('O2')
    # flow_controller_Ar.set_gas('Ar')

    # def controlled_system(oxygen_flow_rate,argon_flow_rate):
    #     flow_controller_O2.set_flow_rate(oxygen_flow_rate)
    #     flow_controller_Ar.set_flow_rate(argon_flow_rate)
    #create gui to take user defined oxygen and argon flow rates and pass them to controlled_system:

    # root = tk.Tk()


    # argon_flow_rate = simpledialog.askfloat("Input", "Enter argon flow rate in sccm",
    #                             parent=root,
    #                             minvalue=0, maxvalue=100)
    # oxygen_flow_rate = simpledialog.askfloat("Input", "Enter oxygen flow rate in sccm",
    #                             parent=root,
    #                             minvalue=0, maxvalue=100)
    # # controlled_system(argon_flow_rate,oxygen_flow_rate)
    # print(argon_flow_rate)
    # print(oxygen_flow_rate)
    # root.withdraw()

    
    
        # argon_flow_rate = float(input('Enter argon flow rate in sccm: '))
        # oxygen_flow_rate = float(input('Enter oxygen flow rate in sccm: '))
        # controlled_system(argon_flow_rate,oxygen_flow_rate)



if __name__ == "__main__":
    main()