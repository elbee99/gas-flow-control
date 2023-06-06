import tkinter as tk
import customtkinter as ctk
import tkinter.font as tkFont
import os

#system settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def check(text):
    if text:
        try:
            value=float(text)
            if 0 <= value <= 30 or value==None:
                return True
                app.input_alert_label.config(text="")
            else:
                return False
                app.input_alert_label.config(text="Input must be a value between 0 and 30")
        except ValueError:
            return False 
            app.O2Start_alert_label.config(text="Input must be a number")
    else:
        app.O2Start_alert_label.config(text="")
    return True

def on_validate(*args):
    if not check(app.O2Start_entry.get()):
        app.input_alert_label.config(fg="red")
        app.input_alert_label.grid(row=1,column=0,columnspan=4, padx=10,pady=(0,5),sticky="ew")
    else:
        app.input_alert_label.grid_forget()

#app frame
app = ctk.CTk()
app.geometry("285x400")
#ctk.CTkFrame(app,width=200, height=200)
app.title("Oxygen Control")
GUIfont=ctk.CTkFont(family="Arial", size=12, weight="normal")

#form row 0
app.O2Start_label=ctk.CTkLabel(app,text="Start Point", font=GUIfont)
app.O2Start_label.grid(row=0,column=0,padx=(20,5),pady=(10,5),sticky="ew")
app.O2Start_equal_label=ctk.CTkLabel(app,text="=", font=GUIfont)
app.O2Start_equal_label.grid(row=0,column=1,padx=5,pady=(10,5),sticky="ew")
app.O2Start_entry=ctk.CTkEntry(app, placeholder_text="0 to 30", border_color="white",validate="key")
#app.O2Start_entry["validatecommand"]=(app.register(check),'%P')
app.O2Start_entry.grid(row=0, column=2, columnspan=1, padx=5, pady=(10,5), sticky="ew")
app.O2Start_entry.bind('<FocusOut>', on_validate)
app.O2Start_entry.bind('<Return>', on_validate)
app.O2Start_unit_label=ctk.CTkLabel(app,text="%", font=GUIfont)
app.O2Start_unit_label.grid(row=0,column=3,padx=(5,20),pady=(10,5),sticky="ew")

#form row 1
app.input_alert_label=tk.Label(app, font=GUIfont, fg="white")
#app.input_alert_label.grid(row=1,column=0,columnspan=4, padx=10,pady=(0,5),sticky="ew")

#form row 2
app.O2End_label=ctk.CTkLabel(app,text="End Point", font=GUIfont)
app.O2End_label.grid(row=2,column=0,padx=(20,5),pady=5,sticky="ew")
app.O2End_equal_label=ctk.CTkLabel(app,text="=", font=GUIfont)
app.O2End_equal_label.grid(row=2,column=1,padx=5,pady=5,sticky="ew")
app.O2End_entry=ctk.CTkEntry(app, placeholder_text="0 to 30", border_color="white",validate="key")
app.O2End_entry["validatecommand"]=(app.register(check),'%P')
app.O2End_entry.grid(row=2, column=2, columnspan=1, padx=5, pady=5, sticky="ew")
app.O2End_unit_label=ctk.CTkLabel(app,text="%", font=GUIfont)
app.O2End_unit_label.grid(row=2,column=3,padx=(5,20),pady=5,sticky="ew")



#Run app
app.mainloop()