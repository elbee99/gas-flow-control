from alicat_flowmeter_control import flow_control
from alicat import FlowController

flow_controller_O2 = FlowController(port='COM3')
flow_controller_Ar = FlowController(port='COM5')

flow_controller_O2.set_gas('O2')
flow_controller_Ar.set_gas('Ar')


import tkinter as tk
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
plt.ioff()
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import datetime
from oxygen_sensor import read_O2_sensor
from oxygen_plotting import oxygen_plotting
from pynput.keyboard import Key, Controller

keyboard = Controller()

Number_of_point = 1
Point_label_list = []
Point_equal_label_list = []
Point_entry_list = []
Point_unit_label_list = []


Duration_label_list = []
Duration_equal_label_list = []
Duration_entry_list = []
Duration_unit_label_list =[]

check_val_point = [1]
check_val_duration=[1]

Number_of_flow = 1
Flow_label_list = []
Flow_equal_label_list = []
Flow_entry_list = []
Flow_unit_label_list = []
Flow_Duration_label_list = []
Flow_Duration_equal_label_list = []
Flow_Duration_entry_list = []
Flow_Duration_unit_label_list =[]

check_val_flow = [1]
check_val_flow_duration=[1]

Mode="conc"
Conc_error=None
Flow_error=None
# system settings
def create_gui():
    global Number_of_point
    global Point_entry_list, Point_equal_label_list, Point_label_list, Point_unit_label_list, Duration_entry_list, Duration_equal_label_list, Duration_label_list, Duration_unit_label_list
    global Flow_label_list, Flow_equal_label_list, Flow_entry_list, Flow_unit_label_list, Flow_Duration_label_list, Flow_Duration_equal_label_list, Flow_Duration_entry_list, Flow_Duration_unit_label_list
    global Mode, Conc_error, Flow_error
    """
    Creates the GUI (made a function for multithreading)
    """
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # check errors
    def check_point(text):
        global Mode
        for pos,i in enumerate(Point_entry_list):
            text = i.get()
            if text:
                try:
                    value = float(text)
                    if 0 <= value <= 30:
                        #app.input_alert_label.config(text="")
                        print(value)
                        try:
                            check_val_point[pos] = True
                        except IndexError:
                            check_val_point.append(True)
                    else:
                        #app.input_alert_label.config(text="Input must be a value between 0 and 30")
                        try:
                            check_val_point[pos] = False
                        except IndexError:
                            check_val_point.append(False)
                except ValueError:
                    #app.input_alert_label.config(text="Input must be a number")
                    try:
                        check_val_point[pos] = False
                    except IndexError:
                        check_val_point.append(False)
            else:
                #app.input_alert_label.configure(text="")
                try:
                    check_val_point[pos] = False
                except IndexError:
                    check_val_point.append(False)

        for i,val in enumerate(check_val_point):
            if check_val_point[i]==True:
                Point_entry_list[i].configure(border_color="white")
            elif check_val_point[i]==False:
                Point_entry_list[i].configure(border_color="red")
        if sum(check_val_point) == len(check_val_point) and sum(check_val_duration) == len(check_val_duration):
            if Mode == "conc":
                app.input_alert_label.configure(text="")
        else:
            if Mode == "conc":
                app.input_alert_label.configure(text="Input error")
        return

    def check_duration(text):
        global Mode
        for pos,i in enumerate(Duration_entry_list):
            text = i.get()
            if text:
                try:
                    value = float(text)
                    if value > 0:
                        #app.input_alert_label.config(text="")
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
                        #app.input_alert_label.config(text="Input must be a value between 0 and 30")
                        try:
                            check_val_duration[pos] = False
                        except IndexError:
                            check_val_duration.append(False)
                except ValueError:
                    #app.input_alert_label.config(text="Input must be a number")
                    try:
                        check_val_duration[pos] = False
                    except IndexError:
                        check_val_duration.append(False)
            else:
                #app.input_alert_label.configure(text="")
                try:
                    check_val_duration[pos] = False
                except IndexError:
                    check_val_duration.append(False)

        for i,val in enumerate(check_val_duration):
            if check_val_duration[i]==True:
                Duration_entry_list[i].configure(border_color="white")
            elif check_val_duration[i]==False:
                Duration_entry_list[i].configure(border_color="red")
        if sum(check_val_point) == len(check_val_point) and sum(check_val_duration) == len(check_val_duration):
            if Mode == "conc":
                app.input_alert_label.configure(text="")
            #return Conc_error == False
        else:
            if Mode == "conc":
                app.input_alert_label.configure(text="Input error")
            #return Conc_error == True
        return
    
     # check errors
    def check_flow(text):
        global Mode
        for pos,i in enumerate(Flow_entry_list):
            text = i.get()
            if text:
                try:
                    value = float(text)
                    if 0 <= value <= 100:
                        #app.input_alert_label.config(text="")
                        try:
                            check_val_flow[pos] = True
                        except IndexError:
                            check_val_flow.append(True)
                    else:
                        #app.input_alert_label.config(text="Input must be a value between 0 and 30")
                        try:
                            check_val_flow[pos] = False
                        except IndexError:
                            check_val_flow.append(False)
                except ValueError:
                    #app.input_alert_label.config(text="Input must be a number")
                    try:
                        check_val_flow[pos] = False
                    except IndexError:
                        check_val_flow.append(False)
            else:
                #app.input_alert_label.configure(text="")
                try:
                    check_val_flow[pos] = False
                except IndexError:
                    check_val_flow.append(False)

        for i,val in enumerate(check_val_flow):
            if check_val_flow[i]==True:
                Flow_entry_list[i].configure(border_color="white")
            elif check_val_flow[i]==False:
                Flow_entry_list[i].configure(border_color="red")
        if sum(check_val_flow) == len(check_val_flow) and sum(check_val_flow_duration) == len(check_val_flow_duration):
            if Mode == "flow":
                app.input_alert_label.configure(text="")
        else:
            if Mode == "flow":
                app.input_alert_label.configure(text="Input error")
        return

    def check_flow_duration(text):
        global Mode
        for pos,i in enumerate(Flow_Duration_entry_list):
            text = i.get()
            if text:
                try:
                    value = float(text)
                    if value > 0:
                        #app.input_alert_label.config(text="")
                        try:
                            check_val_flow_duration[pos] = True
                        except IndexError:
                            check_val_flow_duration.append(True)
                    else:
                        #app.input_alert_label.config(text="Input must be a value between 0 and 30")
                        try:
                            check_val_flow_duration[pos] = False
                        except IndexError:
                            check_val_flow_duration.append(False)
                except ValueError:
                    #app.input_alert_label.config(text="Input must be a number")
                    try:
                        check_val_flow_duration[pos] = False
                    except IndexError:
                        check_val_flow_duration.append(False)
            else:
                #app.input_alert_label.config(text="")
                try:
                    check_val_flow_duration[pos] = False
                except IndexError:
                    check_val_flow_duration.append(False)

        for i,val in enumerate(check_val_flow_duration):
            if check_val_flow_duration[i]==True:
                Flow_Duration_entry_list[i].configure(border_color="white")
            elif check_val_flow_duration[i]==False:
                Flow_Duration_entry_list[i].configure(border_color="red")
        if sum(check_val_flow) == len(check_val_flow) and sum(check_val_flow_duration) == len(check_val_flow_duration):
            if Mode == "flow":
                app.input_alert_label.configure(text="")
        else:
            Flow_error == True
            if Mode == "flow":
                app.input_alert_label.configure(text="Input error")
        return
        
    # app frame
    app = ctk.CTk()
    app.geometry("800x600")
    app.title("Oxygen Control")
    app.rowconfigure(0,weight=1)
    app.columnconfigure(0,weight=1)
    app.columnconfigure(1,weight=1)
    GUIfont = ctk.CTkFont(family="Arial", size=12, weight="normal")

    # error update
    app.input_alert_label = ctk.CTkLabel(app, text="", font=GUIfont, text_color=("red"))
    app.input_alert_label.grid(row=4, column=0, columnspan=1, padx=10, pady=(0, 5), sticky="ew")

    # set frames
    FrameConc = ctk.CTkScrollableFrame(app)
    FrameConc.grid(row=0, column=0, ipadx=28, sticky="news")
    FrameConc.grid_columnconfigure(0,weight=1)
    FrameConc.grid_columnconfigure(1,weight=1)
    FrameConc.grid_columnconfigure(2,weight=1)
    FrameConc.grid_columnconfigure(3,weight=1)
    FrameConc.grid(row=0, column=0, ipadx=28, sticky="news")
    
    FrameFlowRate = ctk.CTkScrollableFrame(app)
    FrameFlowRate.grid_columnconfigure(0,weight=1)
    FrameFlowRate.grid_columnconfigure(1,weight=1)
    FrameFlowRate.grid_columnconfigure(2,weight=1)
    FrameFlowRate.grid_columnconfigure(3,weight=1)

    # FramePlot = ctk.CTkFrame(app)
    # FramePlot.grid(row=0, column=1, sticky="news")
    # FramePlot.columnconfigure(0,weight=4)
    # FramePlot.rowconfigure(0,weight=3)
    
    #Choose Mode
    #app.conc_button = ctk.CTkButton(app, text="Run",border_color="dark-blue")
    #app.conc_button.grid(row=0,column=0,columnspan=4,padx=20,pady=5)

    # Point Frame
    Number_of_widgets = []
    Number_of_widgets.append(Number_of_point)

    Point_label = ctk.CTkLabel(FrameConc, text="Point 1", font=GUIfont)
    Point_label.grid(row=0, column=0, padx=(20, 5), pady=5, sticky="ew")
    Point_label_list.append(Point_label)
    Point_equal_label = ctk.CTkLabel(FrameConc, text="=", font=GUIfont)
    Point_equal_label.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    Point_equal_label_list.append(Point_equal_label)
    Point_entry = ctk.CTkEntry(FrameConc, placeholder_text="0 to 30", border_color="white", validate="key")
    Point_entry.grid(row=0, column=2, columnspan=1, padx=5, pady=5, sticky="ew")
    Point_entry.bind('<FocusOut>', check_point)
    Point_entry.bind('<Return>', check_point)
    Point_entry_list.append(Point_entry)
    Point_unit_label = ctk.CTkLabel(FrameConc, text="%", font=GUIfont)
    Point_unit_label.grid(row=0, column=3, padx=(5, 20), pady=5, sticky="ew")
    Point_unit_label_list.append(Point_unit_label)

    # Duration
    Duration_label = ctk.CTkLabel(FrameConc, text="Duration", font=GUIfont)
    Duration_label.grid(row=1, column=0, padx=(20, 5), pady=5, sticky="ew")
    Duration_label_list.append(Duration_label)
    Duration_equal_label = ctk.CTkLabel(FrameConc, text="=", font=GUIfont)
    Duration_equal_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    Duration_equal_label_list.append(Duration_equal_label)
    Duration_entry = ctk.CTkEntry(FrameConc, placeholder_text="any + value", border_color="white", validate="key")
    Duration_entry.grid(row=1, column=2, columnspan=1, padx=5, sticky="ew")
    Duration_entry_list.append(Duration_entry)
    Duration_entry.bind('<FocusOut>', check_duration)
    Duration_entry.bind('<Return>', check_duration)
    Duration_unit_label = ctk.CTkLabel(FrameConc, text="min", font=GUIfont)
    Duration_unit_label.grid(row=1, column=3, padx=(5, 20), pady=(10, 5), sticky="ew")
    Duration_unit_label_list.append(Duration_unit_label)

    def addpoint():
        global Number_of_point
        global Point_entry_list, Point_equal_label_list, Point_label_list, Point_unit_label_list, Duration_entry_list, Duration_equal_label_list, Duration_label_list, Duration_unit_label_list
        Number_of_point += 1
        
        if Number_of_point >= 1:
            #for Number_of_point in Number_of_widgets:
            #Number_of_widgets.append(Number_of_point)
            Point_label_new = ctk.CTkLabel(FrameConc, text="Point {}".format(Number_of_point), font=GUIfont)
            Point_label_new.grid(row=Number_of_point*2, column=0, padx=(20, 5), pady=5, sticky="ew")
            Point_label_list.append(Point_label_new)
            Point_equal_label_new = ctk.CTkLabel(FrameConc, text="=", font=GUIfont)
            Point_equal_label_new.grid(row=Number_of_point*2, column=1, padx=5, pady=5, sticky="ew")
            Point_equal_label_list.append(Point_equal_label_new)
            Point_entry_new = ctk.CTkEntry(FrameConc, placeholder_text="0 to 30", border_color="white", validate="key")
            Point_entry_new.grid(row=Number_of_point*2, column=2, columnspan=1, padx=5, pady=5, sticky="ew")
            Point_entry_new.bind('<FocusOut>', check_point)
            Point_entry_new.bind('<Return>', check_point)
            Point_entry_list.append(Point_entry_new)
            Point_unit_label_new = ctk.CTkLabel(FrameConc, text="%", font=GUIfont)
            Point_unit_label_new.grid(row=Number_of_point*2, column=3, padx=(5, 20), pady=5, sticky="ew")
            Point_unit_label_list.append(Point_unit_label_new)

            # Duration
            Duration_label_new = ctk.CTkLabel(FrameConc, text="Duration", font=GUIfont)
            Duration_label_new.grid(row=Number_of_point*2+1, column=0, padx=(20, 5), pady=5, sticky="ew")
            Duration_label_list.append(Duration_label_new)
            Duration_equal_label_new = ctk.CTkLabel(FrameConc, text="=", font=GUIfont)
            Duration_equal_label_new.grid(row=Number_of_point*2+1, column=1, padx=5, pady=5, sticky="ew")
            Duration_equal_label_list.append(Duration_equal_label_new)
            Duration_entry_new = ctk.CTkEntry(FrameConc, placeholder_text="any + value", border_color="white", validate="key")
            Duration_entry_new.grid(row=Number_of_point*2+1, column=2, columnspan=1, padx=5, sticky="ew")
            Duration_entry_list.append(Duration_entry_new)
            Duration_entry_new.bind('<FocusOut>', check_duration)
            Duration_entry_new.bind('<Return>', check_duration)
            Duration_unit_label_new = ctk.CTkLabel(FrameConc, text="min", font=GUIfont)
            Duration_unit_label_new.grid(row=Number_of_point*2+1, column=3, padx=(5, 20), pady=(10, 5), sticky="ew")
            Duration_unit_label_list.append(Duration_unit_label_new)
        
        
        return Number_of_point
     
    def RemovePoint():
        global Number_of_point
        if Number_of_point > 1:
            Number_of_point -= 1
            #Number_of_widgets.pop()
            #Point_label_list[-1].grid_forget()
            #Point_equal_label_list[-1].grid_forget()
            #Point_unit_label_list[-1].grid_forget()
            #Duration_label_list[-1].grid_forget()
            #Duration_equal_label_list[-1].grid_forget()
            #Duration_entry_list[-1].grid_forget()
            #Duration_unit_label_list[-1].grid_forget()

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
    
     # Duration Frame
    Number_of_duration_widgets = []
    Number_of_duration_widgets.append(Number_of_flow)

    Flow_label = ctk.CTkLabel(FrameFlowRate, text="Flow Rate 1", font=GUIfont)
    Flow_label.grid(row=0, column=0, padx=(20, 5), pady=5, sticky="ew")
    Flow_label_list.append(Flow_label)
    Flow_equal_label = ctk.CTkLabel(FrameFlowRate, text="=", font=GUIfont)
    Flow_equal_label.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    Flow_equal_label_list.append(Flow_equal_label)
    Flow_entry = ctk.CTkEntry(FrameFlowRate, placeholder_text="0 to 100", border_color="white", validate="key")
    Flow_entry.grid(row=0, column=2, columnspan=1, padx=5, pady=5, sticky="ew")
    Flow_entry.bind('<FocusOut>', check_flow)
    Flow_entry.bind('<Return>', check_flow)
    Flow_entry_list.append(Flow_entry)
    Flow_unit_label = ctk.CTkLabel(FrameFlowRate, text="sccm", font=GUIfont)
    Flow_unit_label.grid(row=0, column=3, padx=(5, 20), pady=5, sticky="ew")
    Flow_unit_label_list.append(Flow_unit_label)

    # Duration
    Flow_Duration_label = ctk.CTkLabel(FrameFlowRate, text="Duration", font=GUIfont)
    Flow_Duration_label.grid(row=1, column=0, padx=(20, 5), pady=5, sticky="ew")
    Flow_Duration_label_list.append(Flow_Duration_label)
    Flow_Duration_equal_label = ctk.CTkLabel(FrameFlowRate, text="=", font=GUIfont)
    Flow_Duration_equal_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    Flow_Duration_equal_label_list.append(Flow_Duration_equal_label)
    Flow_Duration_entry = ctk.CTkEntry(FrameFlowRate, placeholder_text="any + value", border_color="white", validate="key")
    Flow_Duration_entry.grid(row=1, column=2, columnspan=1, padx=5, sticky="ew")
    Flow_Duration_entry_list.append(Flow_Duration_entry)
    Flow_Duration_entry.bind('<FocusOut>', check_flow_duration)
    Flow_Duration_entry.bind('<Return>', check_flow_duration)
    Flow_Duration_unit_label = ctk.CTkLabel(FrameFlowRate, text="min", font=GUIfont)
    Flow_Duration_unit_label.grid(row=1, column=3, padx=(5, 20), pady=(10, 5), sticky="ew")
    Flow_Duration_unit_label_list.append(Flow_Duration_unit_label)

    def addflow():
        global Number_of_flow
        global Flow_entry_list, Flow_equal_label_list, Flow_label_list, Flow_unit_label_list, Flow_Duration_entry_list, Flow_Duration_equal_label_list, Flow_Duration_label_list, Flow_Duration_unit_label_list
        Number_of_flow += 1
        
        if Number_of_flow >= 1:
            #for Number_of_point in Number_of_widgets:
            #Number_of_widgets.append(Number_of_point)
            Flow_label_new = ctk.CTkLabel(FrameFlowRate, text="Flow Rate {}".format(Number_of_flow), font=GUIfont)
            Flow_label_new.grid(row=Number_of_flow*2, column=0, padx=(20, 5), pady=5, sticky="ew")
            Flow_label_list.append(Flow_label_new)
            Flow_equal_label_new = ctk.CTkLabel(FrameFlowRate, text="=", font=GUIfont)
            Flow_equal_label_new.grid(row=Number_of_flow*2, column=1, padx=5, pady=5, sticky="ew")
            Flow_equal_label_list.append(Flow_equal_label_new)
            Flow_entry_new = ctk.CTkEntry(FrameFlowRate, placeholder_text="0 to 100", border_color="white", validate="key")
            Flow_entry_new.grid(row=Number_of_flow*2, column=2, columnspan=1, padx=5, pady=5, sticky="ew")
            Flow_entry_new.bind('<FocusOut>', check_flow)
            Flow_entry_new.bind('<Return>', check_flow)
            Flow_entry_list.append(Flow_entry_new)
            Flow_unit_label_new = ctk.CTkLabel(FrameFlowRate, text="sccm", font=GUIfont)
            Flow_unit_label_new.grid(row=Number_of_flow*2, column=3, padx=(5, 20), pady=5, sticky="ew")
            Flow_unit_label_list.append(Flow_unit_label_new)

            # Duration
            Flow_Duration_label_new = ctk.CTkLabel(FrameFlowRate, text="Duration", font=GUIfont)
            Flow_Duration_label_new.grid(row=Number_of_flow*2+1, column=0, padx=(20, 5), pady=5, sticky="ew")
            Flow_Duration_label_list.append(Flow_Duration_label_new)
            Flow_Duration_equal_label_new = ctk.CTkLabel(FrameFlowRate, text="=", font=GUIfont)
            Flow_Duration_equal_label_new.grid(row=Number_of_flow*2+1, column=1, padx=5, pady=5, sticky="ew")
            Flow_Duration_equal_label_list.append(Flow_Duration_equal_label_new)
            Flow_Duration_entry_new = ctk.CTkEntry(FrameFlowRate, placeholder_text="any + value", border_color="white", validate="key")
            Flow_Duration_entry_new.grid(row=Number_of_flow*2+1, column=2, columnspan=1, padx=5, sticky="ew")
            Flow_Duration_entry_list.append(Flow_Duration_entry_new)
            Flow_Duration_entry_new.bind('<FocusOut>', check_flow_duration)
            Flow_Duration_entry_new.bind('<Return>', check_flow_duration)
            Flow_Duration_unit_label_new = ctk.CTkLabel(FrameFlowRate, text="min", font=GUIfont)
            Flow_Duration_unit_label_new.grid(row=Number_of_flow*2+1, column=3, padx=(5, 20), pady=(10, 5), sticky="ew")
            Flow_Duration_unit_label_list.append(Flow_Duration_unit_label_new)
        return Number_of_flow
     
    def RemoveFlow():
        global Number_of_flow
        if Number_of_flow > 1:
            Number_of_flow -= 1
            #Number_of_widgets.pop()
            #Point_label_list[-1].grid_forget()
            #Point_equal_label_list[-1].grid_forget()
            #Point_unit_label_list[-1].grid_forget()
            #Duration_label_list[-1].grid_forget()
            #Duration_equal_label_list[-1].grid_forget()
            #Duration_entry_list[-1].grid_forget()
            #Duration_unit_label_list[-1].grid_forget()

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
    
    def change_to_flow():
        global Mode, Flow_error
        FrameConc.grid_forget()
        FrameFlowRate.grid(row=0, column=0, ipadx=28, sticky="news")
        add_conc_button.grid_forget()
        add_flow_button.grid(row=1,column=0,columnspan=1,padx=20,pady=5)
        remove_conc_button.grid_forget()
        remove_flow_button.grid(row=2,column=0,columnspan=1,padx=20,pady=5)
        change_to_flow_button.grid_forget()
        change_to_conc_button.grid(row=3,column=0,columnspan=1,padx=20,pady=5)
        app.input_alert_label.configure(text="")
        if sum(check_val_flow) == len(check_val_flow) and sum(check_val_flow_duration) == len(check_val_flow_duration):
            app.input_alert_label.configure(text="")
        else:
            app.input_alert_label.configure(text="Input error")
        Mode = "flow"
        return Mode

    def change_to_conc():
        global Mode, Conc_error
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

    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    O2_string = "O2 Concentration"

    add_conc_button = ctk.CTkButton(app, text="Add Point",border_color="dark-blue", command=lambda:addpoint())
    add_conc_button.grid(row=1,column=0,columnspan=1,padx=20,pady=5)
    add_flow_button = ctk.CTkButton(app, text="Add Point",border_color="dark-blue", command=lambda:addflow())
    remove_conc_button = ctk.CTkButton(app, text="Remove Point",border_color="dark-blue", command=lambda:RemovePoint())
    remove_conc_button.grid(row=Number_of_point+1,column=0,columnspan=1,padx=20,pady=5)
    remove_flow_button = ctk.CTkButton(app, text="Remove Point",border_color="dark-blue", command=lambda:RemoveFlow())
    change_to_flow_button = ctk.CTkButton(app, text="Flow Rate",border_color="dark-blue", command=lambda:change_to_flow())
    change_to_flow_button.grid(row=3,column=0,columnspan=1,padx=20,pady=5)
    change_to_conc_button = ctk.CTkButton(app, text=O2_string.translate(SUB),border_color="dark-blue", command=lambda:change_to_conc())

    def runGUI():
        print(Mode)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        if Mode == "conc":
            check_point(Point_entry)
            check_duration(Duration_entry)
            print(sum(check_val_point), len(check_val_point))
            print(sum(check_val_duration), len(check_val_duration))
            if sum(check_val_point) == len(check_val_point) and sum(check_val_duration) == len(check_val_duration):
                print("run")
                print(Point_entry_list[i] for i in Point_entry_list)
            elif sum(check_val_point) != len(check_val_point) or sum(check_val_duration) != len(check_val_duration):
                print("NO WAY")
        elif Mode == "flow":
            check_flow(Flow_entry)
            check_flow_duration(Flow_Duration_entry)
            if sum(check_val_flow) == len(check_val_flow) and sum(check_val_flow_duration) == len(check_val_flow_duration):
                print("run")
            else:
                print("Bruh")


    #run button
    run_button = ctk.CTkButton(app, text="Run",border_color="dark-blue", command=lambda: runGUI())
    run_button.grid(row=5,column=0,columnspan=1,padx=20,pady=(5,20))


    #liveplot
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
            setpointstring=setpoint.get()
            setpoint_line = np.ones(len(xdata))*float(setpointstring)
            ax.plot(xdata,setpoint_line,'r--')
            line.set_data(xdata,ydata)
            ax.relim()
            ax.autoscale_view()

            fig.canvas.flush_events()
            canvas = FigureCanvasTkAgg(fig,master=app)
            canvas.get_tk_widget().grid(row=0, column=1, columnspan=4, sticky="nsew")
            
            f.write(data_line)
            f.write('\n')

            if bv1.get() == True:
                plottingqueue = app.after(100000,oxygen_plotting())
            else:
                app.after_cancel(plottingqueue)

    app.mainloop()


if __name__ == "__main__":
    create_gui() #creates the gui for testing when run