import serial
import time
import matplotlib.pyplot as plt
serial_output = ""


for port in range(1,17):
    try:
        with serial.Serial('COM{}'.format(port), 57600, timeout=1) as ser: 
            print(ser.name)
            start_time = time.time()
            oxygen_ppm_list = []
            time_list = []
            plt.figure()
            # plt.show()
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
                        oxygen_ppm = oxygen_ppm.replace('d','')
                        # print(serial_output_ascii)
                        print(oxygen_ppm)
                        oxygen_ppm_list.append(float(oxygen_ppm))
                        time_list.append(time.time()-start_time)
                        plt.plot(time_list,oxygen_ppm_list)
    except serial.serialutil.SerialException:
        pass
            