import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from simple_pid import PID
from alicat import FlowController

flow_controller_O2 = FlowController(port='COM3')
flow_controller_Ar = FlowController(port='COM5')

print(flow_controller_O2.get())
print(flow_controller_Ar.get())

flow_controller_O2.set_gas('O2')
flow_controller_Ar.set_gas('Ar')

flow_controller_O2.set_flow_rate(20)
flow_controller_Ar.set_flow_rate(80)
total_flow = 100 # set the total flowrate 
setpoint = 0
def printtext():
    global e, setpoint
    string = e.get() 
    print(string) 
    setpoint = float(string)

from tkinter import *
root = Tk()

root.title('Name')

e = Entry(root)
e.pack()
e.focus_set()

b = Button(root,text='okay',command=printtext)
b.pack(side='bottom')
root.mainloop()

pid = PID(1,0.02,0, sample_time = 1, setpoint=setpoint, output_limits=(12,24), starting_output=setpoint)
serial_output = ""
def controlled_system(flow_rate,oxygen_percent):
    flow_controller_O2.set_flow_rate(flow_rate)
    flow_controller_Ar.set_flow_rate(total_flow-flow_rate)
    print(oxygen_percent)
    return oxygen_percent
oxygen_ppm_stored = np.array([])
o2 = 20 # setpoint 
# opens the COM3 port which is what the O2 sensor was when I plugged it in
# check to see if it is COM3 before running
# Will try optimise so it selects automatically soon
with open('oxygen_sensor.txt', 'w') as f:
    f.write('Time (s)\tO2 conc. (ppm)\n')
    for port in range(1,17):

        try:
            # with serial.Serial('COM{}'.format(port), 57600, timeout=1) as ser: 
            with serial.Serial('COM4', 57600, timeout=1) as ser: 
                print(ser.name)
                start_time = time.time()
                
                fig, ax = plt.subplots()
                ax.set_xlabel('Time (s)')
                ax.set_ylabel('O$_2$ conc. (%)')
                line, = ax.plot([],[])
                
                # while time.time()-start_time < 20: 
                while True:
                    ser.write('D'.encode('ascii'))
                    
                    if(ser.in_waiting > 0):
                            serial_output = ser.readline() 
                            #print(serial_output)
                            
                            try: 
                                serial_output_ascii = serial_output.decode('ascii')
                            except Exception: 
                                print('Data communication was not successful)')
                                pass
                            oxygen_ppm = serial_output_ascii.split(',')[0]
                            #print(oxygen_ppm)
                            oxygen_ppm = oxygen_ppm.replace('d','')
                            #print(serial_output_ascii)
                            oxygen_percent=float(oxygen_ppm)/10e3
                            oxygen_ppm_stored = np.append(oxygen_ppm_stored,oxygen_percent)
                            #print(oxygen_ppm_stored)
                            current_time = time.time()-start_time 
                            data_line = str("{:.2f}".format(current_time))+'\t'+oxygen_ppm

                            xdata, ydata = line.get_xdata(),line.get_ydata()
                            xdata = np.append(xdata,current_time)
                            ydata = np.append(ydata,oxygen_percent)

                            line.set_data(xdata,ydata)
                            ax.relim()
                            ax.autoscale_view()

                            fig.canvas.draw()
                            fig.canvas.flush_events()
                            plt.pause(0.1)

                            f.write(data_line)
                            f.write('\n')
                            
                            if abs(oxygen_percent-setpoint) < 1:
                                new_flow = pid(o2)
                                o2 = controlled_system(new_flow,oxygen_percent)
                            else:
                                controlled_system(setpoint,oxygen_percent)
                            # if(len(oxygen_ppm_stored)>1):
                            #     v = controlled_system(control,oxygen_ppm_stored[len(oxygen_ppm_stored)-1])
                            #     print(oxygen_ppm_stored[len(oxygen_ppm_stored)-1])

            #plt.show()
        except serial.serialutil.SerialException:
            pass


# 

                        # plt.plot(time_list,oxygen_ppm_list)
                        # plt.ylim(0,)
            #fig = plt.figure()
            #ax1 = fig.add_subplot(1,1,1)

            #def animate(i,xar,yar):
                #ax1.clear()
                #ax1.plot(xar,yar)
            #ani = animation.FuncAnimation(fig, animate, interval=1000, fargs=(time_list,oxygen_ppm_list))
            #plt.show()   
