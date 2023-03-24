import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
serial_output = ""

# opens the COM3 port which is what the O2 sensor was when I plugged it in
# check to see if it is COM3 before running
# Will try optimise so it selects automatically soon



fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
xar = []
yar = []
oxygen_ppm_list = []
time_list = []
start_time = time.time()
def animate(i):
    for port in range(1,17):
        try:
            with serial.Serial('COM{}'.format(port), 57600, timeout=1) as ser: 
                print(ser.name)
                
                
                while len(oxygen_ppm_list)<i: 
                    
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
                            oxygen_ppm = oxygen_ppm.replace('d','')
                            # print(serial_output_ascii)
                            print(oxygen_ppm)
                            oxygen_ppm_list.append(float(oxygen_ppm))
                            time_list.append(time.time()-start_time)
                            # plt.plot(time_list,oxygen_ppm_list)
        except serial.serialutil.SerialException:
            pass

    ax1.clear()
    ax1.set_title("Awesome Oxygen Readings")
    ax1.set_xlabel("time")
    ax1.set_ylabel("oxygen_ppm")
    ax1.plot(time_list,oxygen_ppm_list,color="red")
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()       