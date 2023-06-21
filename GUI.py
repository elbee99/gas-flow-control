import tkinter as tk
import customtkinter as ctk
#from oxygen_sensor import read_O2_sensor
#put () behind read_O2_sensor and take out global read_O2_sensor
from oxygen_plotting import oxygen_plotting
read_O2_sensor=300
Number_of_point = 1
Point_label_list = []
Point_equal_label_list = []
Point_entry_list = []
Point_unit_label_list = []
Duration_label_list = []
Duration_equal_label_list = []
Duration_entry_list = []
Duration_unit_label_list =[]

Number_of_flow = 1
Flow_label_list = []
Flow_equal_label_list = []
Flow_entry_list = []
Flow_unit_label_list = []
Flow_Duration_label_list = []
Flow_Duration_equal_label_list = []
Flow_Duration_entry_list = []
Flow_Duration_unit_label_list =[]
# system settings
def create_gui():
    global read_O2_sensor
    global Number_of_point
    global Point_entry_list, Point_equal_label_list, Point_label_list, Point_unit_label_list, Duration_entry_list, Duration_equal_label_list, Duration_label_list, Duration_unit_label_list
    global Flow_label_list, Flow_equal_label_list, Flow_entry_list, Flow_unit_label_list, Flow_Duration_label_list, Flow_Duration_equal_label_list, Flow_Duration_entry_list, Flow_Duration_unit_label_list
    """
    Creates the GUI (made a function for multithreading)
    """
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # check errors
    def check_point(text):
        check_val=[]
        for i in Point_entry_list:
            text = i.get()
            if text:
                try:
                    value = float(text)
                    if 0 <= value <= 30 or value is None:
                        #app.input_alert_label.config(text="")
                        check_val.append(True)
                    else:
                        #app.input_alert_label.config(text="Input must be a value between 0 and 30")
                        check_val.append(False)
                except ValueError:
                    #app.input_alert_label.config(text="Input must be a number")
                    check_val.append(False)
            else:
                app.input_alert_label.configure(text="")
                check_val.append(True)

        for i,val in enumerate(check_val):
            if check_val[i]==True:
                Point_entry_list[i].configure(border_color="white")
            elif check_val[i]==False:
                Point_entry_list[i].configure(border_color="red")
        if sum(check_val) == len(check_val):
            return True
        else:
            app.input_alert_label.configure(text="Input error")
            app.input_alert_label.grid(row=6, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="ew")
            return False

    # # error for start point
    # def on_validate_point(*args):
    #         if not check_point(Point_entry_list.get()):
    #             app.input_alert_label.config(fg="red", bg=app.cget("bg"))
    #             app.input_alert_label.grid(row=6, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="ew")
    #         else:
    #             pass
    #             #app.input_alert_label.grid_forget()

    def check_duration(text):
        check_val=[]
        for i in Duration_entry_list:
            text = i.get()
            if text:
                try:
                    value = float(text)
                    if value > 0 or value is None:
                        #app.input_alert_label.config(text="")
                        check_val.append(True)
                    else:
                        #app.input_alert_label.config(text="Input must be a value between 0 and 30")
                        check_val.append(False)
                except ValueError:
                    #app.input_alert_label.config(text="Input must be a number")
                    check_val.append(False)
            else:
                app.input_alert_label.configure(text="")
                check_val.append(True)

        for i,val in enumerate(check_val):
            if check_val[i]==True:
                Duration_entry_list[i].configure(border_color="white")
            elif check_val[i]==False:
                Duration_entry_list[i].configure(border_color="red")
        if sum(check_val) == len(check_val):
            return True
        else:
            app.input_alert_label.configure(text="Input error")
            app.input_alert_label.grid(row=6, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="ew")
            return False
    
     # check errors
    def check_flow(text):
        check_val=[]
        for i in Flow_entry_list:
            text = i.get()
            if text:
                try:
                    value = float(text)
                    if 0 <= value <= 100 or value is None:
                        #app.input_alert_label.config(text="")
                        check_val.append(True)
                    else:
                        #app.input_alert_label.config(text="Input must be a value between 0 and 30")
                        check_val.append(False)
                except ValueError:
                    #app.input_alert_label.config(text="Input must be a number")
                    check_val.append(False)
            else:
                app.input_alert_label.configure(text="")
                check_val.append(True)

        for i,val in enumerate(check_val):
            if check_val[i]==True:
                Flow_entry_list[i].configure(border_color="white")
            elif check_val[i]==False:
                Flow_entry_list[i].configure(border_color="red")
        if sum(check_val) == len(check_val):
            return True
        else:
            app.input_alert_label.configure(text="Input error")
            app.input_alert_label.grid(row=6, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="ew")
            return False

    def check_flow_duration(text):
        check_val=[]
        for i in Flow_Duration_entry_list:
            text = i.get()
            if text:
                try:
                    value = float(text)
                    if value > 0 or value is None:
                        #app.input_alert_label.config(text="")
                        check_val.append(True)
                    else:
                        #app.input_alert_label.config(text="Input must be a value between 0 and 30")
                        check_val.append(False)
                except ValueError:
                    #app.input_alert_label.config(text="Input must be a number")
                    check_val.append(False)
            else:
                app.input_alert_label.config(text="")
                check_val.append(True)

        for i,val in enumerate(check_val):
            if check_val[i]==True:
                Flow_Duration_entry_list[i].configure(border_color="white")
            elif check_val[i]==False:
                Flow_Duration_entry_list[i].configure(border_color="red")
        if sum(check_val) == len(check_val):
            return True
        else:
            app.input_alert_label.configure(text="Input error", fg="red", bg=app.cget("bg"))
            app.input_alert_label.grid(row=6, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="ew")
            return False
        
    # error for start point
    # def on_validate_duration(*args):
    #         if not check_duration(Duration_entry_list.get()):
    #             app.input_alert_label.config(fg="red", bg=app.cget("bg"))
    #             app.input_alert_label.grid(row=6, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="ew")
    #         else:
    #             pass
                #app.input_alert_label.grid_forget()

    # # error for end point
    # def on_validate_end(*args):
    #     if not check(app.O2End_entry.get()):
    #         app.input_alert_label.config(fg="red", bg=app.cget("bg"))
    #         app.input_alert_label.grid(row=4, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="ew")
    #     else:
    #         app.input_alert_label.grid_forget()

    # error for ramp
    # def check_ramp(text):
    #     if text:
    #         try:
    #             value = float(text)
    #             return True
    #         except ValueError:
    #             app.input_alert_label.config(text="Input must be a number")
    #             return False
    #     else:
    #         app.input_alert_label.config(text="")
    #     return True

    # def on_validate_ramp(*args):
    #     if not check_ramp(app.ramp_entry.get()):
    #         app.input_alert_label.config(fg="red", bg=app.cget("bg"))
    #         app.input_alert_label.grid(row=6, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="ew")
    #     else:
    #         app.input_alert_label.grid_forget()

    # app frame
    app = ctk.CTk()
    app.geometry("350x400")
    app.title("Oxygen Control")
    GUIfont = ctk.CTkFont(family="Arial", size=12, weight="normal")

    # error update
    app.input_alert_label = ctk.CTkLabel(app, text="", font=GUIfont, text_color=("red"))
    app.input_alert_label.grid(row=6, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="ew")

    # set frames
    FrameConc = ctk.CTkFrame(app)
    FrameFlowRate = ctk.CTkFrame(app)
    FrameConc.grid(row=0, column=0, ipadx=28)  
    
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
    Point_entry = ctk.CTkEntry(FrameConc, placeholder_text="value between 0 to 30", border_color="white", validate="key")
    Point_entry.grid(row=0, column=2, columnspan=1, padx=5, pady=5, sticky="ew")
    Point_entry.bind('<FocusOut>', check_point)
    Point_entry.bind('<Return>', check_point)
    Point_entry_list.append(Point_entry)
    Point_unit_label = ctk.CTkLabel(FrameConc, text="%", font=GUIfont)
    Point_unit_label.grid(row=0, column=3, padx=(5, 20), pady=5, sticky="ew")
    Point_unit_label_list.append(Point_unit_label)

    # Duration
    Duration_label = ctk.CTkLabel(FrameConc, text="Duration", font=GUIfont)
    Duration_label.grid(row=0, column=4, padx=(20, 5), pady=5, sticky="ew")
    Duration_label_list.append(Duration_label)
    Duration_equal_label = ctk.CTkLabel(FrameConc, text="=", font=GUIfont)
    Duration_equal_label.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
    Duration_equal_label_list.append(Duration_equal_label)
    Duration_entry = ctk.CTkEntry(FrameConc, placeholder_text="any +/- value", border_color="white", validate="key")
    Duration_entry.grid(row=0, column=6, columnspan=1, padx=5, sticky="ew")
    Duration_entry_list.append(Duration_entry)
    Duration_entry.bind('<FocusOut>', check_duration)
    Duration_entry.bind('<Return>', check_duration)
    Duration_unit_label = ctk.CTkLabel(FrameConc, text="min", font=GUIfont)
    Duration_unit_label.grid(row=0, column=7, padx=(5, 20), pady=(10, 5), sticky="ew")
    Duration_unit_label_list.append(Duration_unit_label)

    def addpoint():
        global Number_of_point
        global Point_entry_list, Point_equal_label_list, Point_label_list, Point_unit_label_list, Duration_entry_list, Duration_equal_label_list, Duration_label_list, Duration_unit_label_list
        Number_of_point += 1
        
        if Number_of_point >= 1:
            #for Number_of_point in Number_of_widgets:
            #Number_of_widgets.append(Number_of_point)
            Point_label_new = ctk.CTkLabel(FrameConc, text="Point {}".format(Number_of_point), font=GUIfont)
            Point_label_new.grid(row=Number_of_point-1, column=0, padx=(20, 5), pady=5, sticky="ew")
            Point_label_list.append(Point_label_new)
            Point_equal_label_new = ctk.CTkLabel(FrameConc, text="=", font=GUIfont)
            Point_equal_label_new.grid(row=Number_of_point-1, column=1, padx=5, pady=5, sticky="ew")
            Point_equal_label_list.append(Point_equal_label_new)
            Point_entry_new = ctk.CTkEntry(FrameConc, placeholder_text="value between 0 to 30", border_color="white", validate="key")
            Point_entry_new.grid(row=Number_of_point-1, column=2, columnspan=1, padx=5, pady=5, sticky="ew")
            Point_entry_new.bind('<FocusOut>', check_point)
            Point_entry_new.bind('<Return>', check_point)
            Point_entry_list.append(Point_entry_new)
            Point_unit_label_new = ctk.CTkLabel(FrameConc, text="%", font=GUIfont)
            Point_unit_label_new.grid(row=Number_of_point-1, column=3, padx=(5, 20), pady=5, sticky="ew")
            Point_unit_label_list.append(Point_unit_label_new)

            # Duration
            Duration_label_new = ctk.CTkLabel(FrameConc, text="Duration", font=GUIfont)
            Duration_label_new.grid(row=Number_of_point-1, column=4, padx=(20, 5), pady=5, sticky="ew")
            Duration_label_list.append(Duration_label_new)
            Duration_equal_label_new = ctk.CTkLabel(FrameConc, text="=", font=GUIfont)
            Duration_equal_label_new.grid(row=Number_of_point-1, column=5, padx=5, pady=5, sticky="ew")
            Duration_equal_label_list.append(Duration_equal_label_new)
            Duration_entry_new = ctk.CTkEntry(FrameConc, placeholder_text="any +/- value", border_color="white", validate="key")
            Duration_entry_new.grid(row=Number_of_point-1, column=6, columnspan=1, padx=5, sticky="ew")
            Duration_entry_list.append(Duration_entry_new)
            Duration_entry_new.bind('<FocusOut>', check_duration)
            Duration_entry_new.bind('<Return>', check_duration)
            Duration_unit_label_new = ctk.CTkLabel(FrameConc, text="min", font=GUIfont)
            Duration_unit_label_new.grid(row=Number_of_point-1, column=7, padx=(5, 20), pady=(10, 5), sticky="ew")
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
    Flow_Duration_label.grid(row=0, column=4, padx=(20, 5), pady=5, sticky="ew")
    Flow_Duration_label_list.append(Flow_Duration_label)
    Flow_Duration_equal_label = ctk.CTkLabel(FrameFlowRate, text="=", font=GUIfont)
    Flow_Duration_equal_label.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
    Flow_Duration_equal_label_list.append(Flow_Duration_equal_label)
    Flow_Duration_entry = ctk.CTkEntry(FrameFlowRate, placeholder_text="any + value", border_color="white", validate="key")
    Flow_Duration_entry.grid(row=0, column=6, columnspan=1, padx=5, sticky="ew")
    Flow_Duration_entry_list.append(Flow_Duration_entry)
    Flow_Duration_entry.bind('<FocusOut>', check_flow_duration)
    Flow_Duration_entry.bind('<Return>', check_flow_duration)
    Flow_Duration_unit_label = ctk.CTkLabel(FrameFlowRate, text="min", font=GUIfont)
    Flow_Duration_unit_label.grid(row=0, column=7, padx=(5, 20), pady=(10, 5), sticky="ew")
    Flow_Duration_unit_label_list.append(Flow_Duration_unit_label)

    def addflow():
        global Number_of_flow
        global Flow_entry_list, Flow_equal_label_list, Flow_label_list, Flow_unit_label_list, Flow_Duration_entry_list, Flow_Duration_equal_label_list, Flow_Duration_label_list, Flow_Duration_unit_label_list
        Number_of_flow += 1
        
        if Number_of_flow >= 1:
            #for Number_of_point in Number_of_widgets:
            #Number_of_widgets.append(Number_of_point)
            Flow_label_new = ctk.CTkLabel(FrameFlowRate, text="Flow Rate {}".format(Number_of_flow), font=GUIfont)
            Flow_label_new.grid(row=Number_of_flow-1, column=0, padx=(20, 5), pady=5, sticky="ew")
            Flow_label_list.append(Flow_label_new)
            Flow_equal_label_new = ctk.CTkLabel(FrameFlowRate, text="=", font=GUIfont)
            Flow_equal_label_new.grid(row=Number_of_flow-1, column=1, padx=5, pady=5, sticky="ew")
            Flow_equal_label_list.append(Flow_equal_label_new)
            Flow_entry_new = ctk.CTkEntry(FrameFlowRate, placeholder_text="value between 0 to 100", border_color="white", validate="key")
            Flow_entry_new.grid(row=Number_of_flow-1, column=2, columnspan=1, padx=5, pady=5, sticky="ew")
            Flow_entry_new.bind('<FocusOut>', check_flow)
            Flow_entry_new.bind('<Return>', check_flow)
            Flow_entry_list.append(Flow_entry_new)
            Flow_unit_label_new = ctk.CTkLabel(FrameFlowRate, text="sccm", font=GUIfont)
            Flow_unit_label_new.grid(row=Number_of_flow-1, column=3, padx=(5, 20), pady=5, sticky="ew")
            Flow_unit_label_list.append(Flow_unit_label_new)

            # Duration
            Flow_Duration_label_new = ctk.CTkLabel(FrameFlowRate, text="Duration", font=GUIfont)
            Flow_Duration_label_new.grid(row=Number_of_flow-1, column=4, padx=(20, 5), pady=5, sticky="ew")
            Flow_Duration_label_list.append(Flow_Duration_label_new)
            Flow_Duration_equal_label_new = ctk.CTkLabel(FrameFlowRate, text="=", font=GUIfont)
            Flow_Duration_equal_label_new.grid(row=Number_of_flow-1, column=5, padx=5, pady=5, sticky="ew")
            Flow_Duration_equal_label_list.append(Flow_Duration_equal_label_new)
            Flow_Duration_entry_new = ctk.CTkEntry(FrameFlowRate, placeholder_text="any + value", border_color="white", validate="key")
            Flow_Duration_entry_new.grid(row=Number_of_flow-1, column=6, columnspan=1, padx=5, sticky="ew")
            Flow_Duration_entry_list.append(Flow_Duration_entry_new)
            Flow_Duration_entry_new.bind('<FocusOut>', check_flow_duration)
            Flow_Duration_entry_new.bind('<Return>', check_flow_duration)
            Flow_Duration_unit_label_new = ctk.CTkLabel(FrameFlowRate, text="min", font=GUIfont)
            Flow_Duration_unit_label_new.grid(row=Number_of_flow-1, column=7, padx=(5, 20), pady=(10, 5), sticky="ew")
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
        return Number_of_flow
    
    def change_to_flow():
        FrameConc.grid_forget()
        FrameFlowRate.grid(row=0, column=0, ipadx=28)
        add_conc_button.grid_forget()
        add_flow_button.grid(row=1,column=0,columnspan=7,padx=20,pady=5)
        remove_conc_button.grid_forget()
        remove_flow_button.grid(row=2,column=0,columnspan=7,padx=20,pady=5)
        change_to_flow_button.grid_forget()
        change_to_conc_button.grid(row=3,column=0,columnspan=7,padx=20,pady=5)

    def change_to_conc():
        FrameFlowRate.grid_forget()
        FrameConc.grid(row=0, column=0, ipadx=28)
        add_flow_button.grid_forget()
        add_conc_button.grid(row=1,column=0,columnspan=7,padx=20,pady=5)
        remove_flow_button.grid_forget()
        remove_conc_button.grid(row=2,column=0,columnspan=7,padx=20,pady=5)
        change_to_conc_button.grid_forget()
        change_to_flow_button.grid(row=3,column=0,columnspan=7,padx=20,pady=5)

    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    O2_string = "O2 Concentration"

    add_conc_button = ctk.CTkButton(app, text="Add Point",border_color="dark-blue", command=lambda:addpoint() and print(Point_entry_list))
    add_conc_button.grid(row=1,column=0,columnspan=7,padx=20,pady=5)
    add_flow_button = ctk.CTkButton(app, text="Add Point",border_color="dark-blue", command=lambda:addflow() and print(Number_of_flow))
    remove_conc_button = ctk.CTkButton(app, text="Remove Point",border_color="dark-blue", command=lambda:RemovePoint() and print(Point_entry_list))
    remove_conc_button.grid(row=Number_of_point+1,column=0,columnspan=7,padx=20,pady=5)
    remove_flow_button = ctk.CTkButton(app, text="Remove Point",border_color="dark-blue", command=lambda:RemoveFlow() and print(Flow_entry_list))
    change_to_flow_button = ctk.CTkButton(app, text="Flow Rate Mode",border_color="dark-blue", command=lambda:change_to_flow())
    change_to_flow_button.grid(row=3,column=0,columnspan=7,padx=20,pady=5)
    change_to_conc_button = ctk.CTkButton(app, text=O2_string.translate(SUB),border_color="dark-blue", command=lambda:change_to_conc())

    #run button
    app.run_button = ctk.CTkButton(app, text="Run",border_color="dark-blue")
    app.run_button.grid(row=4,column=0,columnspan=7,padx=20,pady=5)

    # text displaying value of read_O2_sensor function
    app.O2_value_label = ctk.CTkLabel(app, font=GUIfont)
    app.O2_value_label.grid(row=8, column=0, padx=(20, 5), pady=5, sticky="ew")
    def update_O2_value():
        """
        Updates the O2 value label every 200ms
        """
        app.O2_value_label.configure(text="O2 value = " + str(float(read_O2_sensor)/10E3) + "%")
        app.after(200, update_O2_value)

    update_O2_value()
    #app.resizable(False,False)
    app.mainloop()

def create_gui_test():
    app = tk.Tk()
    app.geometry("310x500")
    app.title("Oxygen Control")
    GUIfont = ("Arial", 12, "normal")
    app.O2_value_label = tk.Label(app, font=GUIfont)
    app.O2_value_label.grid(row=8, column=0, padx=(20, 5), pady=5, sticky="ew")

    def update_O2_value():
        """
        Updates the O2 value label every 200ms
        """
        app.O2_value_label.configure(text="O2 value = " + str(float(read_O2_sensor) / 10E3) + "%")
        app.after(200, update_O2_value)

    update_O2_value()
    app.resizable(False, False)
    app.mainloop()

if __name__ == "__main__":
    create_gui() #creates the gui for testing when run