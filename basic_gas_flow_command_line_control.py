from alicat import FlowController
import tkinter as tk
from tkinter import simpledialog
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def main():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # app frame
    app = ctk.CTk()
    app.geometry("350x400")
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
    app.O2End_label = ctk.CTkLabel(app, text="Oxygen Flow Rate", font=GUIfont)
    app.O2End_label.grid(row=2, column=0, padx=(20, 5), pady=5, sticky="ew")
    app.O2End_entry = ctk.CTkEntry(app, placeholder_text="0.00-30.00", border_color="white", validate="key")
    app.O2End_entry.grid(row=2, column=2, columnspan=1, padx=5, sticky="ew")
    app.O2End_unit_label = ctk.CTkLabel(app, text="sccm", font=GUIfont)
    app.O2End_unit_label.grid(row=2, column=3, padx=(5, 20), pady=(10, 5), sticky="ew")
   
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

    #Update Button
    app.run_button = ctk.CTkButton(app, text="Update",border_color="dark-blue")
    app.run_button.grid(row=7,column=0,columnspan=4,padx=20,pady=5)
    # generate random numbers for the plot
    x,y,s,c = np.random.rand(4,100)

    # generate the figure and plot object which will be linked to the root element
    fig, ax = plt.subplots()
    fig.set_size_inches(8,4)
    ax.scatter(x,y,s*50,c)
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
    canvas = FigureCanvasTkAgg(fig,master=app)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=6,  rowspan=7, padx=(20, 5), pady=(100, 5), sticky="ew")

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