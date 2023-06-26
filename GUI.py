from alicat_flowmeter_control import flow_control_basic, flow_control
from alicat import FlowController

flow_controller_O2 = FlowController(port='COM3')
flow_controller_Ar = FlowController(port='COM5')

flow_controller_O2.set_gas('O2')
flow_controller_Ar.set_gas('Ar')


import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
# plt.ioff()
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import datetime
from oxygen_sensor import read_O2_sensor
from oxygen_plotting import oxygen_plotting
from pynput.keyboard import Key, Controller
from simple_pid import PID
keyboard = Controller()

#extract entered values from the respective entry_lists
#Variables for oxygen concentration mode
Number_of_point = 1
Point_label_list = []
Point_equal_label_list = []
Point_entry_list = []
Point_unit_label_list = []


Duration_label_list = []
Duration_equal_label_list = []
Duration_entry_list = []
Duration_unit_label_list =[]

##storing lists for the check functions
check_val_total_flow = [1] 
check_val_point = [1]
check_val_duration=[1]

#Varialbes for flow rate mode
Number_of_flow = 1
Flow_label_list = []
Flow_equal_label_list = []
Flow_entry_list = []
Flow_unit_label_list = []
Flow_Duration_label_list = []
Flow_Duration_equal_label_list = []
Flow_Duration_entry_list = []
Flow_Duration_unit_label_list =[]

##storing lists for the check functions
check_val_flow_total_flow = [1]
check_val_flow = [1]
check_val_flow_duration=[1]

#Current mode the user is interacting with
Mode="conc"

loop = True

# GUI function
def create_gui():
    global Number_of_point
    global Point_entry_list, Point_equal_label_list, Point_label_list, Point_unit_label_list, Duration_entry_list, Duration_equal_label_list, Duration_label_list, Duration_unit_label_list
    global Flow_label_list, Flow_equal_label_list, Flow_entry_list, Flow_unit_label_list, Flow_Duration_label_list, Flow_Duration_equal_label_list, Flow_Duration_entry_list, Flow_Duration_unit_label_list
    global Mode
    """
    Creates the GUI
    """
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # check functions of the concentration mode
    ## check total flow value
    def check_total_flow(text):
        global Mode
        text = total_flow_entry.get()
        if Mode == "conc":
            if text: #if there is text input
                try:
                    value = float(text) #try converting text into a float
                    if 0 < value <= 60: #restrict value range
                        total_flow_entry.configure(border_color = "white") #configure border color of the corresponding entry cell
                        check_val_total_flow[0]=True #stores True/False value at the corresponding index along the list
                    else: #if the value is out of range
                        total_flow_entry.configure(border_color = "red")
                        check_val_total_flow[0]=False
                except ValueError: #if the entry is not a number
                    total_flow_entry.configure(border_color = "red")
                    check_val_total_flow[0]=False
            else: #if the entry is submitted without an input
                check_val_total_flow[0]=False
        #hide error message only if all entries for total flow rate, concentratoin setpoints, and durations are accepted 
        if sum(check_val_total_flow) == len(check_val_total_flow) and sum(check_val_point) == len(check_val_point) and sum(check_val_duration) == len(check_val_duration):
            if Mode == "conc":
                app.input_alert_label.configure(text="")
        else:
            if Mode == "conc":
                app.input_alert_label.configure(text="Input error")
    
    ##check function for concentration setpoint
    def check_point(text):
        global Mode
        for pos,i in enumerate(Point_entry_list): #checks all concentration setpoint entries everytime a binidng event occurs in one of them
            text = i.get()
            if text:
                try:
                    value = float(text)
                    if 0 <= value <= 30:
                        print(value)
                        try:
                            check_val_point[pos] = True
                        except IndexError: #append instead,if the index does not exist in the check list yet
                            check_val_point.append(True)
                    else:
                        try:
                            check_val_point[pos] = False
                        except IndexError:
                            check_val_point.append(False)
                except ValueError:
                    try:
                        check_val_point[pos] = False
                    except IndexError:
                        check_val_point.append(False)
            else:
                try:
                    check_val_point[pos] = False
                except IndexError:
                    check_val_point.append(False)

        for i,val in enumerate(check_val_point): #go through the check list and configure the entry cell's border colour correspondingly
            if check_val_point[i]==True:
                Point_entry_list[i].configure(border_color="white")
            elif check_val_point[i]==False:
                Point_entry_list[i].configure(border_color="red")
        if sum(check_val_total_flow) == len(check_val_total_flow) and sum(check_val_point) == len(check_val_point) and sum(check_val_duration) == len(check_val_duration):
            if Mode == "conc":
                app.input_alert_label.configure(text="")
        else:
            if Mode == "conc":
                app.input_alert_label.configure(text="Input error")
        return

    ##check function for duration
    def check_duration(text):
        global Mode
        for pos,i in enumerate(Duration_entry_list):
            text = i.get()
            if text:
                try:
                    value = float(text)
                    if value > 0:
                        try:
                            check_val_duration[pos] = True
                        except IndexError:
                            check_val_duration.append(True)
                    elif value == None:
                        try:
                            check_val_duration[pos] = False
                        except IndexError:
                            check_val_duration.append(False)
                    else:
                        try:
                            check_val_duration[pos] = False
                        except IndexError:
                            check_val_duration.append(False)
                except ValueError:
                    try:
                        check_val_duration[pos] = False
                    except IndexError:
                        check_val_duration.append(False)
            else:
                try:
                    check_val_duration[pos] = False
                except IndexError:
                    check_val_duration.append(False)

        for i,val in enumerate(check_val_duration):
            if check_val_duration[i]==True:
                Duration_entry_list[i].configure(border_color="white")
            elif check_val_duration[i]==False:
                Duration_entry_list[i].configure(border_color="red")
        if sum(check_val_total_flow) == len(check_val_total_flow) and sum(check_val_point) == len(check_val_point) and sum(check_val_duration) == len(check_val_duration):
            if Mode == "conc":
                app.input_alert_label.configure(text="")
        else:
            if Mode == "conc":
                app.input_alert_label.configure(text="Input error")
        return
    
    # check functions of the flow rate mode
    ## check total flow value in the flow rate mode
    def check_total_flow_flow(text):
        global Mode
        text = flow_total_flow_entry.get()
        if Mode == "conc":
            if text: #if there is text input
                try:
                    value = float(text) #try converting text into a float
                    if 0 < value <= 60: #restrict value range
                        flow_total_flow_entry.configure(border_color = "white") #configure border color of the corresponding entry cell
                        check_val_flow_total_flow[0]=True #stores True/False value at the corresponding index along the list
                    else: #if the value is out of range
                        flow_total_flow_entry.configure(border_color = "red")
                        check_val_flow_total_flow[0]=False
                except ValueError: #if the entry is not a number
                    flow_total_flow_entry.configure(border_color = "red")
                    check_val_flow_total_flow[0]=False
            else: #if the entry is submitted without an input
                check_val_flow_total_flow[0]=False
        #hide error message only if all entries for total flow rate, concentratoin setpoints, and durations are accepted 
        if sum(check_val_flow_total_flow) == len(check_val_flow_total_flow) and sum(check_val_flow) == len(check_val_flow) and sum(check_val_flow_duration) == len(check_val_flow_duration):
            if Mode == "conc":
                app.input_alert_label.configure(text="")
        else:
            if Mode == "conc":
                app.input_alert_label.configure(text="Input error")
    ## check function for flow rate
    def check_flow(text):
        global Mode
        for pos,i in enumerate(Flow_entry_list):
            text = i.get()
            if text:
                try:
                    value = float(text)
                    if 0 <= value <= float(flow_total_flow_entry.get()):
                        try:
                            check_val_flow[pos] = True
                        except IndexError:
                            check_val_flow.append(True)
                    else:
                        try:
                            check_val_flow[pos] = False
                        except IndexError:
                            check_val_flow.append(False)
                except ValueError:
                    try:
                        check_val_flow[pos] = False
                    except IndexError:
                        check_val_flow.append(False)
            else:
                try:
                    check_val_flow[pos] = False
                except IndexError:
                    check_val_flow.append(False)

        for i,val in enumerate(check_val_flow):
            if check_val_flow[i]==True:
                Flow_entry_list[i].configure(border_color="white")
            elif check_val_flow[i]==False:
                Flow_entry_list[i].configure(border_color="red")
        if sum(check_val_flow_total_flow) == len(check_val_flow_total_flow) and sum(check_val_flow) == len(check_val_flow) and sum(check_val_flow_duration) == len(check_val_flow_duration):
            if Mode == "flow":
                app.input_alert_label.configure(text="")
        else:
            if Mode == "flow":
                app.input_alert_label.configure(text="Input error")
        return

    ##check function for duration (in flow rate mode)
    def check_flow_duration(text):
        global Mode
        for pos,i in enumerate(Flow_Duration_entry_list):
            text = i.get()
            if text:
                try:
                    value = float(text)
                    if value > 0:
                        try:
                            check_val_flow_duration[pos] = True
                        except IndexError:
                            check_val_flow_duration.append(True)
                    else:
                        try:
                            check_val_flow_duration[pos] = False
                        except IndexError:
                            check_val_flow_duration.append(False)
                except ValueError:
                    try:
                        check_val_flow_duration[pos] = False
                    except IndexError:
                        check_val_flow_duration.append(False)
            else:
                try:
                    check_val_flow_duration[pos] = False
                except IndexError:
                    check_val_flow_duration.append(False)

        for i,val in enumerate(check_val_flow_duration):
            if check_val_flow_duration[i]==True:
                Flow_Duration_entry_list[i].configure(border_color="white")
            elif check_val_flow_duration[i]==False:
                Flow_Duration_entry_list[i].configure(border_color="red")
        if sum(check_val_flow_total_flow) == len(check_val_flow_total_flow) and sum(check_val_flow) == len(check_val_flow) and sum(check_val_flow_duration) == len(check_val_flow_duration):
            if Mode == "flow":
                app.input_alert_label.configure(text="")
        else:
            if Mode == "flow":
                app.input_alert_label.configure(text="Input error")
        return
        
    # master app setup
    app = ctk.CTk()
    app.geometry("1350x900")
    app.title("Oxygen Control")
    app.rowconfigure(0,weight=1)
    app.columnconfigure(0,weight=3)
    app.columnconfigure(1,weight=4)
    GUIfont = ctk.CTkFont(family="Arial", size=12, weight="normal")

    # set frames
    ## frame for concentration mode
    FrameConc = ctk.CTkScrollableFrame(app)
    FrameConc.grid(row=0, column=0, ipadx=28, sticky="news")
    FrameConc.grid_columnconfigure(0,weight=1)
    FrameConc.grid_columnconfigure(1,weight=1)
    FrameConc.grid_columnconfigure(2,weight=1)
    FrameConc.grid_columnconfigure(3,weight=1)
    FrameConc.grid(row=0, column=0, ipadx=28, sticky="news")
    
    ## frame for flow rate mode
    FrameFlowRate = ctk.CTkScrollableFrame(app)
    FrameFlowRate.grid_columnconfigure(0,weight=1)
    FrameFlowRate.grid_columnconfigure(1,weight=1)
    FrameFlowRate.grid_columnconfigure(2,weight=1)
    FrameFlowRate.grid_columnconfigure(3,weight=1)
    

    # Set up the first variables in the concentraton mode frame
    ## row for total flow rate input
    total_flow_label = ctk.CTkLabel(FrameConc,text="Total flow", font = GUIfont)
    total_flow_label.grid(row=0,column=0,padx=(20, 5), pady=(5,15), sticky="ew")
    total_flow_equal_label = ctk.CTkLabel(FrameConc,text="=", font = GUIfont)
    total_flow_equal_label.grid(row=0,column=1,padx=5, pady=(5,15), sticky="ew")
    total_flow_entry = ctk.CTkEntry(FrameConc, placeholder_text="0 to 60", border_color="white", validate="key")
    total_flow_entry.grid(row=0, column=2, columnspan=1, padx=5, pady=(5,15), sticky="ew")
    total_flow_entry.bind('<FocusOut>', check_total_flow)
    total_flow_entry.bind('<Return>',check_total_flow)
    total_flow_unit_label = ctk.CTkLabel(FrameConc,text="sccm", font = GUIfont)
    total_flow_unit_label.grid(row=0, column=3, padx=(5, 20), pady=(5,15), sticky="ew")

    # row for concentration setpoint
    Point_label = ctk.CTkLabel(FrameConc, text="Point 1", font=GUIfont)
    Point_label.grid(row=1, column=0, padx=(20, 5), pady=(15,5), sticky="ew")
    Point_label_list.append(Point_label)
    Point_equal_label = ctk.CTkLabel(FrameConc, text="=", font=GUIfont)
    Point_equal_label.grid(row=1, column=1, padx=5, pady=(15,5), sticky="ew")
    Point_equal_label_list.append(Point_equal_label)
    Point_entry = ctk.CTkEntry(FrameConc, placeholder_text="0 to 30", border_color="white", validate="key")
    Point_entry.grid(row=1, column=2, columnspan=1, padx=5, pady=(15,5), sticky="ew")
    Point_entry.bind('<FocusOut>', check_point)
    Point_entry.bind('<Return>', check_point)
    Point_entry_list.append(Point_entry)
    Point_unit_label = ctk.CTkLabel(FrameConc, text="%", font=GUIfont)
    Point_unit_label.grid(row=1, column=3, padx=(5, 20), pady=(15,5), sticky="ew")
    Point_unit_label_list.append(Point_unit_label)

    # row for duration time setting 
    Duration_label = ctk.CTkLabel(FrameConc, text="Duration", font=GUIfont)
    Duration_label.grid(row=2, column=0, padx=(20, 5), pady=(5,15), sticky="ew")
    Duration_label_list.append(Duration_label)
    Duration_equal_label = ctk.CTkLabel(FrameConc, text="=", font=GUIfont)
    Duration_equal_label.grid(row=2, column=1, padx=5, pady=(5,15), sticky="ew")
    Duration_equal_label_list.append(Duration_equal_label)
    Duration_entry = ctk.CTkEntry(FrameConc, placeholder_text="any + value", border_color="white", validate="key")
    Duration_entry.grid(row=2, column=2, columnspan=1, padx=5, pady=(5,15), sticky="ew")
    Duration_entry_list.append(Duration_entry)
    Duration_entry.bind('<FocusOut>', check_duration)
    Duration_entry.bind('<Return>', check_duration)
    Duration_unit_label = ctk.CTkLabel(FrameConc, text="min", font=GUIfont)
    Duration_unit_label.grid(row=2, column=3, padx=(5, 20), pady=(5,15), sticky="ew")
    Duration_unit_label_list.append(Duration_unit_label)

    # add subscripts
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    O2_string = "O2 Concentration"
    O2_flow_string = "O2 Flow Rate"

    # function for adding a new row of setpoint and duration time everytime its button is pressed
    def addpoint():
        global Number_of_point
        global Point_entry_list, Point_equal_label_list, Point_label_list, Point_unit_label_list, Duration_entry_list, Duration_equal_label_list, Duration_label_list, Duration_unit_label_list
        Number_of_point += 1 #increment the total number of setpoints by 1
        
        if Number_of_point >= 1: #almost a repeat of what it is above
            Point_label_new = ctk.CTkLabel(FrameConc, text="Point {}".format(Number_of_point), font=GUIfont)
            Point_label_new.grid(row=Number_of_point*2+1, column=0, padx=(20, 5), pady=(15,5), sticky="ew")
            Point_label_list.append(Point_label_new)
            Point_equal_label_new = ctk.CTkLabel(FrameConc, text="=", font=GUIfont)
            Point_equal_label_new.grid(row=Number_of_point*2+1, column=1, padx=5, pady=(15,5), sticky="ew")
            Point_equal_label_list.append(Point_equal_label_new)
            Point_entry_new = ctk.CTkEntry(FrameConc, placeholder_text="0 to 30", border_color="white", validate="key")
            Point_entry_new.grid(row=Number_of_point*2+1, column=2, columnspan=1, padx=5, pady=(15,5), sticky="ew")
            Point_entry_new.bind('<FocusOut>', check_point)
            Point_entry_new.bind('<Return>', check_point)
            Point_entry_list.append(Point_entry_new)
            Point_unit_label_new = ctk.CTkLabel(FrameConc, text="%", font=GUIfont)
            Point_unit_label_new.grid(row=Number_of_point*2+1, column=3, padx=(5, 20), pady=(15,5), sticky="ew")
            Point_unit_label_list.append(Point_unit_label_new)

            Duration_label_new = ctk.CTkLabel(FrameConc, text="Duration", font=GUIfont)
            Duration_label_new.grid(row=Number_of_point*2+2, column=0, padx=(20, 5), pady=(5,15), sticky="ew")
            Duration_label_list.append(Duration_label_new)
            Duration_equal_label_new = ctk.CTkLabel(FrameConc, text="=", font=GUIfont)
            Duration_equal_label_new.grid(row=Number_of_point*2+2, column=1, padx=5, pady=(5,15), sticky="ew")
            Duration_equal_label_list.append(Duration_equal_label_new)
            Duration_entry_new = ctk.CTkEntry(FrameConc, placeholder_text="any + value", border_color="white", validate="key")
            Duration_entry_new.grid(row=Number_of_point*2+2, column=2, columnspan=1, padx=5, pady=(5,15), sticky="ew")
            Duration_entry_list.append(Duration_entry_new)
            Duration_entry_new.bind('<FocusOut>', check_duration)
            Duration_entry_new.bind('<Return>', check_duration)
            Duration_unit_label_new = ctk.CTkLabel(FrameConc, text="min", font=GUIfont)
            Duration_unit_label_new.grid(row=Number_of_point*2+2, column=3, padx=(5, 20), pady=(5,15), sticky="ew")
            Duration_unit_label_list.append(Duration_unit_label_new)
        
        return Number_of_point
    
    # fuction for removing the last row of setpoint and duration time
    def RemovePoint():
        global Number_of_point
        if Number_of_point > 1: #permit removal only if the number of points is greater than 1
            Number_of_point -= 1 #decrease the total number of point by 1

            #destroy all widgets in this row and delete them from their storing lists and checking lists
            Point_label_list[-1].destroy() 
            del Point_label_list[-1]
            Point_equal_label_list[-1].destroy()
            del Point_equal_label_list[-1]
            Point_entry_list[-1].destroy()
            del Point_entry_list[-1]
            Point_unit_label_list[-1].destroy()
            del Point_unit_label_list[-1]
            Duration_label_list[-1].destroy()
            del Duration_label_list[-1]
            Duration_equal_label_list[-1].destroy()
            del Duration_equal_label_list[-1]
            Duration_entry_list[-1].destroy()
            del Duration_entry_list[-1]
            Duration_unit_label_list[-1].destroy()
            del Duration_unit_label_list[-1]
            try:
                del check_val_point[-1]
            except IndexError:
                pass
            try:
                del check_val_duration[-1]
            except IndexError:
                pass
            check_point(Point_entry)
            check_duration(Duration_entry)
        return Number_of_point
    
    # Variables and functions in the Flow Rate Mode, everything is the same as in the concentration mode,
    # just different variable names and text
    ## row for total flow rate input
    flow_total_flow_label = ctk.CTkLabel(FrameFlowRate,text="Total flow", font = GUIfont)
    flow_total_flow_label.grid(row=0,column=0,padx=(20, 5), pady=(5,15), sticky="ew")
    flow_total_flow_equal_label = ctk.CTkLabel(FrameFlowRate,text="=", font = GUIfont)
    flow_total_flow_equal_label.grid(row=0,column=1,padx=5, pady=(5,15), sticky="ew")
    flow_total_flow_entry = ctk.CTkEntry(FrameFlowRate, placeholder_text="0 to 60", border_color="white", validate="key")
    flow_total_flow_entry.grid(row=0, column=2, columnspan=1, padx=5, pady=(5,15), sticky="ew")
    flow_total_flow_entry.bind('<FocusOut>', check_total_flow_flow)
    flow_total_flow_entry.bind('<Return>',check_total_flow_flow)
    flow_total_flow_unit_label = ctk.CTkLabel(FrameFlowRate,text="sccm", font = GUIfont)
    flow_total_flow_unit_label.grid(row=0, column=3, padx=(5, 20), pady=(5,15), sticky="ew")
    
    Flow_label = ctk.CTkLabel(FrameFlowRate, text=O2_flow_string.translate(SUB)+" 1", font=GUIfont)
    Flow_label.grid(row=1, column=0, padx=(20, 5), pady=(15, 5), sticky="ew")
    Flow_label_list.append(Flow_label)
    Flow_equal_label = ctk.CTkLabel(FrameFlowRate, text="=", font=GUIfont)
    Flow_equal_label.grid(row=1, column=1, padx=5, pady=(15, 5), sticky="ew")
    Flow_equal_label_list.append(Flow_equal_label)
    Flow_entry = ctk.CTkEntry(FrameFlowRate, placeholder_text="less than total flow rate", border_color="white", validate="key")
    Flow_entry.grid(row=1, column=2, columnspan=1, padx=5, pady=(15, 5), sticky="ew")
    Flow_entry.bind('<FocusOut>', check_flow)
    Flow_entry.bind('<Return>', check_flow)
    Flow_entry_list.append(Flow_entry)
    Flow_unit_label = ctk.CTkLabel(FrameFlowRate, text="sccm", font=GUIfont)
    Flow_unit_label.grid(row=1, column=3, padx=(5, 20), pady=(15, 5), sticky="ew")
    Flow_unit_label_list.append(Flow_unit_label)

    # Duration
    Flow_Duration_label = ctk.CTkLabel(FrameFlowRate, text="Duration", font=GUIfont)
    Flow_Duration_label.grid(row=2, column=0, padx=(20, 5), pady=(5,15), sticky="ew")
    Flow_Duration_label_list.append(Flow_Duration_label)
    Flow_Duration_equal_label = ctk.CTkLabel(FrameFlowRate, text="=", font=GUIfont)
    Flow_Duration_equal_label.grid(row=2, column=1, padx=5, pady=(5,15), sticky="ew")
    Flow_Duration_equal_label_list.append(Flow_Duration_equal_label)
    Flow_Duration_entry = ctk.CTkEntry(FrameFlowRate, placeholder_text="any + value", border_color="white", validate="key")
    Flow_Duration_entry.grid(row=2, column=2, columnspan=1, padx=5, pady=(5,15), sticky="ew")
    Flow_Duration_entry_list.append(Flow_Duration_entry)
    Flow_Duration_entry.bind('<FocusOut>', check_flow_duration)
    Flow_Duration_entry.bind('<Return>', check_flow_duration)
    Flow_Duration_unit_label = ctk.CTkLabel(FrameFlowRate, text="min", font=GUIfont)
    Flow_Duration_unit_label.grid(row=2, column=3, padx=(5, 20), pady=(5,15), sticky="ew")
    Flow_Duration_unit_label_list.append(Flow_Duration_unit_label)

    def addflow():
        global Number_of_flow
        global Flow_entry_list, Flow_equal_label_list, Flow_label_list, Flow_unit_label_list, Flow_Duration_entry_list, Flow_Duration_equal_label_list, Flow_Duration_label_list, Flow_Duration_unit_label_list
        Number_of_flow += 1
        
        if Number_of_flow >= 1:
            #for Number_of_point in Number_of_widgets:
            #Number_of_widgets.append(Number_of_point)
            Flow_label_new = ctk.CTkLabel(FrameFlowRate, text= O2_flow_string.translate(SUB) +" {}".format(Number_of_flow), font=GUIfont)
            Flow_label_new.grid(row=Number_of_flow*2+1, column=0, padx=(20, 5), pady=(15,5), sticky="ew")
            Flow_label_list.append(Flow_label_new)
            Flow_equal_label_new = ctk.CTkLabel(FrameFlowRate, text="=", font=GUIfont)
            Flow_equal_label_new.grid(row=Number_of_flow*2+1, column=1, padx=5, pady=(15,5), sticky="ew")
            Flow_equal_label_list.append(Flow_equal_label_new)
            Flow_entry_new = ctk.CTkEntry(FrameFlowRate, placeholder_text="less than total flow rate", border_color="white", validate="key")
            Flow_entry_new.grid(row=Number_of_flow*2+1, column=2, columnspan=1, padx=5, pady=(15,5), sticky="ew")
            Flow_entry_new.bind('<FocusOut>', check_flow)
            Flow_entry_new.bind('<Return>', check_flow)
            Flow_entry_list.append(Flow_entry_new)
            Flow_unit_label_new = ctk.CTkLabel(FrameFlowRate, text="sccm", font=GUIfont)
            Flow_unit_label_new.grid(row=Number_of_flow*2+1, column=3, padx=(5, 20), pady=(15,5), sticky="ew")
            Flow_unit_label_list.append(Flow_unit_label_new)

            # Duration
            Flow_Duration_label_new = ctk.CTkLabel(FrameFlowRate, text="Duration", font=GUIfont)
            Flow_Duration_label_new.grid(row=Number_of_flow*2+2, column=0, padx=(20, 5), pady=(5,15), sticky="ew")
            Flow_Duration_label_list.append(Flow_Duration_label_new)
            Flow_Duration_equal_label_new = ctk.CTkLabel(FrameFlowRate, text="=", font=GUIfont)
            Flow_Duration_equal_label_new.grid(row=Number_of_flow*2+2, column=1, padx=5, pady=(5,15), sticky="ew")
            Flow_Duration_equal_label_list.append(Flow_Duration_equal_label_new)
            Flow_Duration_entry_new = ctk.CTkEntry(FrameFlowRate, placeholder_text="any + value", border_color="white", validate="key")
            Flow_Duration_entry_new.grid(row=Number_of_flow*2+2, column=2, columnspan=1, padx=5, pady=(5,15), sticky="ew")
            Flow_Duration_entry_list.append(Flow_Duration_entry_new)
            Flow_Duration_entry_new.bind('<FocusOut>', check_flow_duration)
            Flow_Duration_entry_new.bind('<Return>', check_flow_duration)
            Flow_Duration_unit_label_new = ctk.CTkLabel(FrameFlowRate, text="min", font=GUIfont)
            Flow_Duration_unit_label_new.grid(row=Number_of_flow*2+2, column=3, padx=(5, 20), pady=(5,15), sticky="ew")
            Flow_Duration_unit_label_list.append(Flow_Duration_unit_label_new)
        return Number_of_flow
     
    def RemoveFlow():
        global Number_of_flow
        if Number_of_flow > 1:
            Number_of_flow -= 1

            Flow_label_list[-1].destroy()
            del Flow_label_list[-1] 
            Flow_equal_label_list[-1].destroy()
            del Flow_equal_label_list[-1]
            Flow_entry_list[-1].destroy()
            del Flow_entry_list[-1]
            Flow_unit_label_list[-1].destroy()
            del Flow_unit_label_list[-1]
            Flow_Duration_label_list[-1].destroy()
            del Flow_Duration_label_list[-1]
            Flow_Duration_equal_label_list[-1].destroy()
            del Flow_Duration_equal_label_list[-1]
            Flow_Duration_entry_list[-1].destroy()
            del Flow_Duration_entry_list[-1]
            Flow_Duration_unit_label_list[-1].destroy()
            del Flow_Duration_unit_label_list[-1]
            try:
                del check_val_flow[-1]
            except IndexError:
                pass
            try:
                del check_val_flow_duration[-1]
            except IndexError:
                pass
            check_flow(Flow_entry)
            check_flow(Flow_Duration_entry)
        return Number_of_flow
    
    # function for changing from concentration mode to flow rate mode
    def change_to_flow():
        global Mode
        FrameConc.grid_forget() #hide the concentration mode frame
        FrameFlowRate.grid(row=0, column=0, ipadx=28, sticky="news") #show the flow rate mode frame
        add_conc_button.grid_forget() #hide the button for adding concentration setpoints
        add_flow_button.grid(row=1,column=0,columnspan=1,padx=20,pady=5) #show the button for adding flow rate setpoints
        remove_conc_button.grid_forget() #hide the button for removing concentration setpoints
        remove_flow_button.grid(row=2,column=0,columnspan=1,padx=20,pady=5) #show the button for removing flow rate setpoints
        change_to_flow_button.grid_forget() #hide the button for this change function 
        change_to_conc_button.grid(row=3,column=0,columnspan=1,padx=20,pady=5) #show the button for changing from flow rate to concentration mode
        app.input_alert_label.configure(text="") #re-initialise the error message for the new mode
        if sum(check_val_flow) == len(check_val_flow) and sum(check_val_flow_duration) == len(check_val_flow_duration):
            app.input_alert_label.configure(text="")
        else:
            app.input_alert_label.configure(text="Input error")
        Mode = "flow"
        return Mode

    #vice versa of the change_to_flow function
    def change_to_conc():
        global Mode
        FrameFlowRate.grid_forget()
        FrameConc.grid(row=0, column=0, ipadx=28, sticky="news")
        add_flow_button.grid_forget()
        add_conc_button.grid(row=1,column=0,columnspan=1,padx=20,pady=5)
        remove_flow_button.grid_forget()
        remove_conc_button.grid(row=2,column=0,columnspan=1,padx=20,pady=5)
        change_to_conc_button.grid_forget()
        change_to_flow_button.grid(row=3,column=0,columnspan=1,padx=20,pady=5)
        app.input_alert_label.configure(text="")
        if sum(check_val_point) == len(check_val_point) and sum(check_val_duration) == len(check_val_duration):
            app.input_alert_label.configure(text="")
        else:
            app.input_alert_label.configure(text="Input error")
        Mode = "conc"
        return Mode

    # add subscripts
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    O2_string = "O2 Concentration"

    #widgets locating in the master app frame
    ## buttons 
    add_conc_button = ctk.CTkButton(app, text="Add Point",border_color="dark-blue", command=lambda:addpoint()) #button to add concentration setpoint
    add_conc_button.grid(row=1,column=0,columnspan=1,padx=20,pady=5) #show the add_conc_button as the mode is defaulted as concentration mode
    add_flow_button = ctk.CTkButton(app, text="Add Point",border_color="dark-blue", command=lambda:addflow()) #button to add flow rate setpoint, not shown until the app is in flow rate mode
    remove_conc_button = ctk.CTkButton(app, text="Remove Point",border_color="dark-blue", command=lambda:RemovePoint()) #button to remove concentration setpoint
    remove_conc_button.grid(row=Number_of_point+1,column=0,columnspan=1,padx=20,pady=5)
    remove_flow_button = ctk.CTkButton(app, text="Remove Point",border_color="dark-blue", command=lambda:RemoveFlow()) #button to remove flow rate setpoint, not shown yet
    change_to_flow_button = ctk.CTkButton(app, text="Flow Rate",border_color="dark-blue", command=lambda:change_to_flow()) #button to change concentration mode into flow rate mode
    change_to_flow_button.grid(row=3,column=0,columnspan=1,padx=20,pady=5)
    change_to_conc_button = ctk.CTkButton(app, text=O2_string.translate(SUB),border_color="dark-blue", command=lambda:change_to_conc()) #button to change flow rate mode into concentration mode, not shown yet

    # error message
    app.input_alert_label = ctk.CTkLabel(app, text="", font=GUIfont, text_color=("red"))
    app.input_alert_label.grid(row=4, column=0, columnspan=1, padx=10, pady=(0, 5), sticky="ew")
    # function to submit all input variables
    # incorporate command line scheduling and flow control here
    def runGUI():
        print(Mode)
        keyboard.press(Key.enter) #simulate pressing and release of the enter key in case the user didn't bind the last entry they made before pressing run
        keyboard.release(Key.enter)
        if Mode == "conc": #detect mode and submit the corresponding entries
            check_point(Point_entry) #run the check functions again, assuming the user didn't trigger them before submitting for some reason
            check_duration(Duration_entry)
            check_total_flow(total_flow_entry)
            if sum(check_val_total_flow) == len(check_val_total_flow) and sum(check_val_point) == len(check_val_point) and sum(check_val_duration) == len(check_val_duration): #allow variable inputs only if there's no error in all inputs
                print("run")
                for pos,i in enumerate(Point_entry_list): #checks all concentration setpoint entries everytime a binidng event occurs in one of them
                    print(i.get())
                    setpoint.set(float(i.get())) #set the setpoint to the value in the entry
                    start_time_of_point_entry = time.time()
                    pid = PID(1,0.02,0, sample_time = 1, output_limits = (0,100), setpoint = float(i.get()), starting_output= float(i.get())) #PID controller with the setpoint being the concentration setpoint
                    def controlled_system(total_flow, O2_set_point, current_O2_percent):
                        flow_controller_O2.set_flow_rate(total_flow*O2_set_point/100)
                        flow_controller_Ar.set_flow_rate(total_flow-(total_flow*O2_set_point/100))
                        # print(current_O2_percent)
                        return current_O2_percent
                    while time.time()< start_time_of_point_entry + float(Duration_entry_list[pos].get())*60:
                        oxygen_percent = float(read_O2_sensor())*10e-5
                        print(oxygen_percent, float(i.get()))
                        if abs(oxygen_percent-float(i.get())) < 4:
                            PID_setpoint = pid(oxygen_percent) #this is the setpoint required the PID controller
                            #we need to get current value and feed back into the PID controller
                            print(PID_setpoint)
                            controlled_system(float(total_flow_entry.get()),PID_setpoint,oxygen_percent)
                        else:
                            controlled_system(float(total_flow_entry.get()),float(i.get()),oxygen_percent)
                        oxygen_plotting()  
                        time.sleep(0.5)

            elif sum(check_val_total_flow) != len(check_val_total_flow) or sum(check_val_point) != len(check_val_point) or sum(check_val_duration) != len(check_val_duration):
                print("NO WAY")
            
        elif Mode == "flow":
            check_flow(Flow_entry)
            check_flow_duration(Flow_Duration_entry)
            if sum(check_val_flow_total_flow) == len(check_val_flow_total_flow) and sum(check_val_flow) == len(check_val_flow) and sum(check_val_flow_duration) == len(check_val_flow_duration):
                print("run")
                for pos,i in enumerate(Flow_entry_list): #checks all concentration setpoint entries everytime a binidng event occurs in one of them
                    print(i.get())
                    flow_control_basic(float(flow_total_flow_entry.get()),float(i.get()))
                    start_time_of_point_entry = time.time()
                    while time.time()< start_time_of_point_entry + float(Flow_Duration_entry_list[pos].get())*60:
                        oxygen_plotting()  
                        time.sleep(0.5)
            else:
                print("Bruh")
            


    #add run button
    run_button = ctk.CTkButton(app, text="Run",border_color="dark-blue", command=lambda: runGUI())
    run_button.grid(row=5,column=0,columnspan=1,padx=20,pady=(5,20))


    #liveplot (some .grid positioning variables are changed to fit things into the same GUI )
    bv1=ctk.BooleanVar(value=False)
    setpoint=ctk.StringVar(value='0')
    def stopplotting():
        bv1.set(0)
        print(bv1.get())
    def plotting():
        bv1.set(1)
        oxygen_plotting()
        print(bv1.get())
    
    start_plot_button=ctk.CTkButton(app, text="Start Plotting",border_color="dark-blue", command=plotting)
    start_plot_button.grid(row=1,column=1, columnspan=1, padx=20, pady=5)
    stop_plot_button=ctk.CTkButton(app, text="Stop Plotting",border_color="dark-blue", command=stopplotting)
    stop_plot_button.grid(row=2,column=1, columnspan=1, padx=20, pady=5)
    
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
    line2, = ax.plot([],[])
    canvas = FigureCanvasTkAgg(fig,master=app)
    canvas.get_tk_widget().grid(row=0, column=1, columnspan=4, sticky="nsew")

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
            xdata2, ydata2 = line2.get_xdata(),line2.get_ydata()
            xdata2 = np.append(xdata2,current_time)
            ydata2 = np.append(ydata2,float(setpoint.get()))
            line.set_data(xdata,ydata)
            line2.set_data(xdata2,ydata2)
            line2.set_linestyle('--')
            ax.relim()
            ax.autoscale_view()

            fig.canvas.flush_events()
            canvas = FigureCanvasTkAgg(fig,master=app)
            canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew")
            
            f.write(data_line)
            f.write('\n')

            # if bv1.get() == True:
            #     plottingqueue = app.after(oxygen_plotting())
            # else:
            #     app.after_cancel(plottingqueue)
    
    
    def on_closing():
        global loop
        if messagebox.askokcancel("Oxygen Control", "Do you want to quit?"):
            loop == False
            app.destroy()
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()


if __name__ == "__main__":
    create_gui() #creates the gui for testing when run