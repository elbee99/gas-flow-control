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
# system settings
def create_gui():
    global read_O2_sensor
    global Number_of_point
    global Point_entry_list, Point_equal_label_list, Point_label_list, Point_unit_label_list, Duration_entry_list, Duration_equal_label_list, Duration_label_list, Duration_unit_label_list

    """
    Creates the GUI (made a function for multithreading)
    """
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # check errors
    def check(text):
        check_val=[]
        if text:
            try:
                value = float(text)
                if 0 <= value <= 30 or value is None:
                    app.input_alert_label.config(text="")
                    check_val.append(True)
                else:
                    app.input_alert_label.config(text="Input must be a value between 0 and 30")
                    check_val.append(False)
            except ValueError:
                app.input_alert_label.config(text="Input must be a number")
                check_val.append(False)
        else:
            app.input_alert_label.config(text="")
            check_val.append(True)

        for i,val in enumerate(check_val):
            if i==True:
                pass
            elif i==False:
                app.Point_entry_list[i].config(border_color="red")


    # error for start point
    def on_validate_start(*args):
        global Point_entry_list
        for i in Point_entry_list:
            if not check(i.get()):
                app.input_alert_label.config(fg="red", bg=app.cget("bg"))
                app.input_alert_label.grid(row=6, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="ew")
            else:
                pass
                #app.input_alert_label.grid_forget()

    # error for end point
    def on_validate_end(*args):
        if not check(app.O2End_entry.get()):
            app.input_alert_label.config(fg="red", bg=app.cget("bg"))
            app.input_alert_label.grid(row=4, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="ew")
        else:
            app.input_alert_label.grid_forget()

    # error for ramp
    def check_ramp(text):
        if text:
            try:
                value = float(text)
                return True
            except ValueError:
                app.input_alert_label.config(text="Input must be a number")
                return False
        else:
            app.input_alert_label.config(text="")
        return True

    def on_validate_ramp(*args):
        if not check_ramp(app.ramp_entry.get()):
            app.input_alert_label.config(fg="red", bg=app.cget("bg"))
            app.input_alert_label.grid(row=6, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="ew")
        else:
            app.input_alert_label.grid_forget()

    # app frame
    app = ctk.CTk()
    app.geometry("350x400")
    app.title("Oxygen Control")
    GUIfont = ctk.CTkFont(family="Arial", size=12, weight="normal")

    # error update
    app.input_alert_label = tk.Label(app, font=GUIfont, fg="red", bg=app.cget("bg"))
    app.input_alert_label.grid(row=6, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="ew")

    # set frames
    FrameConc = ctk.CTkFrame(app)
    FrameFlowRate = ctk.CTkFrame(app)
    FrameDuration = ctk.CTkFrame(app)
    FrameConc.grid(row=0, column=0, ipadx=28)  

    #Choose Mode
    #app.conc_button = ctk.CTkButton(app, text="Run",border_color="dark-blue")
    #app.conc_button.grid(row=0,column=0,columnspan=4,padx=20,pady=5)

    # Point and Duration
    # add point

    

    
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
    Point_entry.bind('<FocusOut>', on_validate_start)
    Point_entry.bind('<Return>', on_validate_start)
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
    Duration_entry.bind('<FocusOut>', on_validate_ramp)
    Duration_entry.bind('<Return>', on_validate_ramp)
    Duration_unit_label = ctk.CTkLabel(FrameConc, text="min", font=GUIfont)
    Duration_unit_label.grid(row=0, column=7, padx=(5, 20), pady=(10, 5), sticky="ew")
    Duration_unit_label_list.append(Duration_unit_label)

    def addpoint():
        global Number_of_point
        global Point_entry_list, Point_equal_label_list, Point_label_list, Point_unit_label_list, Duration_entry_list, Duration_equal_label_list, Duration_label_list, Duration_unit_label_list
        Number_of_point += 1
        print(Number_of_point)
        
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
            Point_entry_new.bind('<FocusOut>', on_validate_start)
            Point_entry_new.bind('<Return>', on_validate_start)
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
            Duration_entry_new.bind('<FocusOut>', on_validate_ramp)
            Duration_entry_new.bind('<Return>', on_validate_ramp)
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
        
    app.add_button = ctk.CTkButton(app, text="Add Point",border_color="dark-blue", command=lambda:addpoint() and print(Point_entry_list))
    app.add_button.grid(row=1,column=0,columnspan=7,padx=20,pady=5)
    app.remove_button = ctk.CTkButton(app, text="Remove Point",border_color="dark-blue", command=lambda:RemovePoint() and print(Point_entry_list))
    app.remove_button.grid(row=2,column=0,columnspan=7,padx=20,pady=5)
    app.print_button = ctk.CTkButton(app, text="Print",border_color="dark-blue", command=lambda:print(Point_entry_list[-1].get()))
    app.print_button.grid(row=3,column=0,columnspan=7,padx=20,pady=5)

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