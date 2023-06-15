from alicat import FlowController
import tkinter as tk
from tkinter import simpledialog
def main():
    flow_controller_O2 = FlowController(port='COM3')
    flow_controller_Ar = FlowController(port='COM5')

    print(flow_controller_O2.get())
    print(flow_controller_Ar.get())

    flow_controller_O2.set_gas('O2')
    flow_controller_Ar.set_gas('Ar')

    def controlled_system(oxygen_flow_rate,argon_flow_rate):
        flow_controller_O2.set_flow_rate(oxygen_flow_rate)
        flow_controller_Ar.set_flow_rate(argon_flow_rate)
    #create gui to take user defined oxygen and argon flow rates and pass them to controlled_system:
    while True:
        root = tk.Tk()


        argon_flow_rate = simpledialog.askfloat("Input", "Enter argon flow rate in sccm",
                                    parent=root,
                                    minvalue=0, maxvalue=100)
        oxygen_flow_rate = simpledialog.askfloat("Input", "Enter oxygen flow rate in sccm",
                                    parent=root,
                                    minvalue=0, maxvalue=100)
        controlled_system(argon_flow_rate,oxygen_flow_rate)
        root.withdraw()

    
    
        # argon_flow_rate = float(input('Enter argon flow rate in sccm: '))
        # oxygen_flow_rate = float(input('Enter oxygen flow rate in sccm: '))
        # controlled_system(argon_flow_rate,oxygen_flow_rate)



if __name__ == "__main__":
    main()