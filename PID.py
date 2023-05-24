from simple_pid import PID
pid = PID(1,0.1,0.05, sample_time = 1, setpoint=20, output_limits=(0,50))
start_time = time.time()
with serial.Serial('COM4', 57600, timeout=1) as ser: 
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
                    print(oxygen_ppm)
    return float(oxygen_ppm)/10e3
def controlled_system(flow_rate):
    
v = flow_controller_O2.set_flow_rate(8)

while True:




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
                            print(oxygen_ppm)

                            current_time = time.time()-start_time 
                            data_line = str("{:.2f}".format(current_time))+'\t'+oxygen_ppm

                            xdata, ydata = line.get_xdata(),line.get_ydata()
                            xdata = np.append(xdata,current_time)
                            ydata = np.append(ydata,float(oxygen_ppm)/10e3)

                            line.set_data(xdata,ydata)
                            ax.relim()
                            ax.autoscale_view()

                            fig.canvas.draw()
                            fig.canvas.flush_events()
                            plt.pause(0.1)

                            f.write(data_line)
                            f.write('\n')