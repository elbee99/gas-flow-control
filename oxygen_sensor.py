import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
serial_output = ""

def read_O2_sensor():
    for port in range(1,17):
        try:
            with serial.Serial('COM{}'.format(port), 57600, timeout=1) as ser: 
                print(ser.name)
                # while time.time()-start_time < 20: 
                ser.write('D'.encode('ascii'))
                
                if(ser.in_waiting > 0):
                        serial_output = ser.readline() 
                        #print(serial_output)
                        
                        try: 
                            serial_output_ascii = serial_output.decode('ascii')
                        except Exception: 
                            print('Data communication was not successful')
                            pass
                        oxygen_ppm = serial_output_ascii.split(',')[0]
                        #print(oxygen_ppm)
                        oxygen_ppm = oxygen_ppm.replace('d','')
                        #print(serial_output_ascii)
                        return oxygen_ppm
        except serial.serialutil.SerialException:
            pass

# opens the COM3 port which is what the O2 sensor was when I plugged it in
# check to see if it is COM3 before running
# Will try optimise so it selects automatically soon
# with open('oxygen_sensor.txt', 'w') as f:
#     f.write('Time (s)\tO2 conc. (ppm)\n')
#     for port in range(1,17):

#         try:
#             # with serial.Serial('COM{}'.format(port), 57600, timeout=1) as ser: 
#             with serial.Serial('COM4', 57600, timeout=1) as ser: 
#                 print(ser.name)
#                 start_time = time.time()
                
#                 fig, ax = plt.subplots()
#                 ax.set_xlabel('Time (s)')
#                 ax.set_ylabel('O$_2$ conc. (%)')
#                 line, = ax.plot([],[])
                
#                 # while time.time()-start_time < 20: 
#                 while True:
#                     ser.write('D'.encode('ascii'))
                    
#                     if(ser.in_waiting > 0):
#                             serial_output = ser.readline() 
#                             #print(serial_output)
                            
#                             try: 
#                                 serial_output_ascii = serial_output.decode('ascii')
#                             except Exception: 
#                                 print('Data communication was not successful)')
#                                 pass
#                             oxygen_ppm = serial_output_ascii.split(',')[0]
#                             #print(oxygen_ppm)
#                             oxygen_ppm = oxygen_ppm.replace('d','')
#                             #print(serial_output_ascii)
#                             print(oxygen_ppm)

#                             current_time = time.time()-start_time 
#                             data_line = str("{:.2f}".format(current_time))+'\t'+oxygen_ppm

#                             xdata, ydata = line.get_xdata(),line.get_ydata()
#                             xdata = np.append(xdata,current_time)
#                             ydata = np.append(ydata,float(oxygen_ppm)/10e3)

#                             line.set_data(xdata,ydata)
#                             ax.relim()
#                             ax.autoscale_view()

#                             fig.canvas.draw()
#                             fig.canvas.flush_events()
#                             plt.pause(0.1)

#                             f.write(data_line)
#                             f.write('\n')
#             #plt.show()
#         except serial.serialutil.SerialException:
#             pass