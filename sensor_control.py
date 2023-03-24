import serial

serial_output = ""

# opens the COM3 port which is what the O2 sensor was when I plugged it in
# check to see if it is COM3 before running
# Will try optimise so it selects automatically soon

for port in range(1,17):
    try:
        with serial.Serial('COM{}'.format(port), 57600, timeout=1) as ser: 
            print(ser.name)

            while True: 
                
                ser.write('D'.encode('ascii'))
                
                if(ser.in_waiting > 0):
                        serial_output = ser.readline() 
                        #print(serial_output)
                        
                        try: 
                            serial_output_ascii = serial_output.decode('ascii')
                        except Exception: 
                            print('Data communication was not successful)')

                        oxygen_ppm = serial_output_ascii.split(',')[0]
                        oxygen_ppm = oxygen_ppm.replace('d','')
                        print(oxygen_ppm)
    except serial.serialutil.SerialException:
        pass
            