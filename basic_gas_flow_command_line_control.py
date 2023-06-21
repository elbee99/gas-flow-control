from alicat_flowmeter_control import flow_control_basic
from alicat import FlowController
from simple_pid import PID

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
    def updateflowrate():
        flow_controller_O2.set_flow_rate(float(app.O2Flow_entry.get()))
        flow_controller_Ar.set_flow_rate(float(app.ArFlow_entry.get()))
        print(app.ArFlow_entry.get(),app.O2Flow_entry.get())

    #Update Button
    app.run_button = ctk.CTkButton(app, text="Update",border_color="dark-blue", command=updateflowrate)
    app.run_button.grid(row=3,column=0,columnspan=4,padx=20,pady=5)

    #oxygen percentage
    app.O2End_label = ctk.CTkLabel(app, text="Oxygen % Concentration", font=GUIfont)
    app.O2End_label.grid(row=4, column=0, padx=(20, 5), pady=5, sticky="ew")
    app.O2End_entry = ctk.CTkEntry(app, placeholder_text="0.00-30.00", border_color="white", validate="key")
    app.O2End_entry.grid(row=4, column=2, columnspan=1, padx=5, sticky="ew")
    app.O2End_unit_label = ctk.CTkLabel(app, text="%", font=GUIfont)
    app.O2End_unit_label.grid(row=4, column=3, padx=(5, 20), pady=(10, 5), sticky="ew") 

    # Shared dictionary to store the flag
    shared_data = {'continue_running': True}

    def updatesetpoint():  #press enter to update setpoint 

        # Disable the update button
        app.run_button.configure(state="disabled")
        shared_data['continue_running'] = True

        setpoint.set(app.O2End_entry.get())
        target_O2_set_point = float(setpoint.get())
        pid = PID(1,0.02,0, sample_time = 1, setpoint=target_O2_set_point, output_limits=(12,24), starting_output=target_O2_set_point)
        
        def flow_control_O2(target_O2_set_point=target_O2_set_point):
            if not shared_data['continue_running']:
                return

            oxygen_percent = float(read_O2_sensor())*10e-5
            print('Oxygen Percent: ',oxygen_percent,'Target O2 Set Point: ',target_O2_set_point)
            if abs(oxygen_percent-target_O2_set_point) < 1.5:
                print('pid code')
                PID_setpoint = pid(oxygen_percent) #this is the setpoint required the PID controller
                #we need to get current value and feed back into the PID controller
                oxygen_percent = flow_control_basic(100,PID_setpoint)
            else:
                flow_control_basic(100,target_O2_set_point)

            if shared_data['continue_running']:
                app.after(100,flow_control_O2)

        flow_control_O2()

    def cancel_updatesetpoint():
        
        # Enable the update button
        app.run_button.configure(state="normal")
        app.run_button.configure(command=updatesetpoint) 
        state = app.run_button.cget("state")
        print("Button state:", state)
        shared_data['continue_running'] = False
        # if the O2 percent is 1.5 or more away from the setpoint, then update the flow rate
        # flow_control(100,float(setpoint.get()))
        
        # flow_control(100,float(setpoint.get()))
        # print(setpoint)


    # Button to cancel updatesetpoint()
    cancel_button = ctk.CTkButton(app, text="Cancel", border_color="dark-blue", command=cancel_updatesetpoint)
    cancel_button.grid(row=6, column=0, columnspan=4, padx=20, pady=5)

    #Update Button
    app.run_button = ctk.CTkButton(app, text="Update",border_color="dark-blue", command=updatesetpoint)
    app.run_button.grid(row=5,column=0,columnspan=4,padx=20,pady=5)
    #once the setpoint button is pressed, allow the flow control to kick in
    

    def stopplotting():
        bv1.set(0)
        print(bv1.get())
    def plotting():
        bv1.set(1)
        button_start_time = time.time()
        oxygen_plotting(start_time=button_start_time)
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
    default_start_time = time.time()
    fig, ax = plt.subplots()
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('O$_2$ conc. (%)')
    line, = ax.plot([],[])
    canvas = FigureCanvasTkAgg(fig,master=app)
    canvas.get_tk_widget().grid(row=0, column=6,  rowspan=9, columnspan=2, padx=(20, 5), pady=(100, 5), sticky="ew")
    def oxygen_plotting(start_time=default_start_time,filename='oxygen_conc.txt'):
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
    # def flow_control(argon_flow_rate,oxygen_flow_rate,start_time=time.time(),control_time=10):
    #     pid = PID(1,0.02,0, sample_time = 1, setpoint=O2_set_point, output_limits=(12,24), starting_output=O2_set_point)
    #     def controlled_system(total_flow=total_flow, O2_set_point=O2_set_point,current_O2_percent = float(read_O2_sensor())/1000):
    #         flow_controller_O2.set_flow_rate(total_flow*O2_set_point/100)
    #         flow_controller_Ar.set_flow_rate(total_flow-(total_flow*O2_set_point/100))
    #         # print(current_O2_percent)
    #         return current_O2_percent
    #     if type(control_time) == float or type(control_time) == int:
    #         time.time()-start_time < control_time:
    #             print('Runtime is {0:.2f} seconds'.format(time.time()-start_time))
    #             oxygen_percent = float(read_O2_sensor())*10e-5
    #             if abs(oxygen_percent-O2_set_point) < 1:
    #                 PID_setpoint = pid(oxygen_percent) #this is the setpoint required the PID controller
    #                 #we need to get current value and feed back into the PID controller
    #                 oxygen_percent = controlled_system(total_flow,PID_setpoint,oxygen_percent)
    #             else:
    #                 controlled_system(total_flow,O2_set_point,oxygen_percent)
    #     else:
    #         while True:
    #             oxygen_percent = float(read_O2_sensor())*10e-3
    #             if abs(oxygen_percent-O2_set_point) < 1:
    #                 PID_setpoint = pid(oxygen_percent) #this is the setpoint required the PID controller
    #                 #we need to get current value and feed back into the PID controller
    #                 oxygen_percent = controlled_system(total_flow,PID_setpoint,oxygen_percent)
    #             else:
    #                 controlled_system(total_flow,O2_set_point,oxygen_percent)
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