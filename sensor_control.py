import serial

serial_output = ""

# opens the COM3 port which is what the O2 sensor was when I plugged it in
# check to see if it is COM3 before running
# Will try optimise so it selects automatically soon
with serial.Serial('COM3', 576000, timeout=1) as ser:
    print(ser.name)

    while True:
        # according to manual send D to get response
        ser.write('D'.encode('ASCII')) 
        if(ser.in_waiting > 0): #checks if there is bytes to be read
            serial_output = ser.readline() #reads to newline character
            try: 
                serial_output_ascii = serial_output.decode('ascii')
            except: 
                print('Data communication was not successful)')

            oxygen_ppm = serial_output_ascii.split(',')[0]
            oxygen_ppm = oxygen_ppm.replace('d','')
            print(oxygen_ppm)
            