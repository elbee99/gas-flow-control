import tkinter as tk
import customtkinter as ctk

# system settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# check errors
def check(text):
    if text:
        try:
            value = float(text)
            if 0 <= value <= 30 or value is None:
                app.input_alert_label.config(text="")
                return True
            else:
                app.input_alert_label.config(text="Input must be a value between 0 and 30")
                return False
        except ValueError:
            app.input_alert_label.config(text="Input must be a number")
            return False
    else:
        app.input_alert_label.config(text="")
    return True

# error for start point
def on_validate_start(*args):
    if not check(app.O2Start_entry.get()):
        app.input_alert_label.config(fg="red", bg=app.cget("bg"))
        app.input_alert_label.grid(row=1, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="ew")
    else:
        app.input_alert_label.grid_forget()

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
app.geometry("310x400")
app.title("Oxygen Control")
GUIfont = ctk.CTkFont(family="Arial", size=12, weight="normal")

# error update
app.input_alert_label = tk.Label(app, font=GUIfont, fg="red", bg=app.cget("bg"))
#app.input_alert_label.grid(row=1, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="ew")

# start point
app.O2Start_label = ctk.CTkLabel(app, text="Start Point", font=GUIfont)
app.O2Start_label.grid(row=0, column=0, padx=(20, 5), pady=(100, 5), sticky="ew")
app.O2Start_equal_label = ctk.CTkLabel(app, text="=", font=GUIfont)
app.O2Start_equal_label.grid(row=0, column=1, padx=5, pady=(100, 5), sticky="ew")
app.O2Start_entry = ctk.CTkEntry(app, placeholder_text="value between 0 to 30", border_color="white", validate="key")
app.O2Start_entry.grid(row=0, column=2, columnspan=1, padx=5, pady=(100, 5), sticky="ew")
app.O2Start_entry.bind('<FocusOut>', on_validate_start)
app.O2Start_entry.bind('<Return>', on_validate_start)
app.O2Start_unit_label = ctk.CTkLabel(app, text="%", font=GUIfont)
app.O2Start_unit_label.grid(row=0, column=3, padx=(5, 20), pady=(100, 5), sticky="ew")


# end point
app.O2End_label = ctk.CTkLabel(app, text="End Point", font=GUIfont)
app.O2End_label.grid(row=2, column=0, padx=(20, 5), pady=5, sticky="ew")
app.O2End_equal_label = ctk.CTkLabel(app, text="=", font=GUIfont)
app.O2End_equal_label.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
app.O2End_entry = ctk.CTkEntry(app, placeholder_text="value between 0 to 30", border_color="white", validate="key")
app.O2End_entry.grid(row=2, column=2, columnspan=1, padx=5, sticky="ew")
app.O2End_entry.bind('<FocusOut>', on_validate_end)
app.O2End_entry.bind('<Return>', on_validate_end)
app.O2End_unit_label = ctk.CTkLabel(app, text="%", font=GUIfont)
app.O2End_unit_label.grid(row=2, column=3, padx=(5, 20), pady=(10, 5), sticky="ew")

# ramp rate
app.ramp_label = ctk.CTkLabel(app, text="Ramp Rate", font=GUIfont)
app.ramp_label.grid(row=5, column=0, padx=(20, 5), pady=5, sticky="ew")
app.ramp_equal_label = ctk.CTkLabel(app, text="=", font=GUIfont)
app.ramp_equal_label.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
app.ramp_entry = ctk.CTkEntry(app, placeholder_text="any +/- value", border_color="white", validate="key")
app.ramp_entry.grid(row=5, column=2, columnspan=1, padx=5, sticky="ew")
app.ramp_entry.bind('<FocusOut>', on_validate_ramp)
app.ramp_entry.bind('<Return>', on_validate_ramp)
app.ramp_unit_label = ctk.CTkLabel(app, text="%/min", font=GUIfont)
app.ramp_unit_label.grid(row=5, column=3, padx=(5, 20), pady=(10, 5), sticky="ew")

#run button
app.run_button = ctk.CTkButton(app, text="Run",border_color="dark-blue")
app.run_button.grid(row=7,column=0,columnspan=4,padx=20,pady=5)

app.resizable(False,False)
app.mainloop()