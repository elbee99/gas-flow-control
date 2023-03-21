import serial

serial_output = ""

# opens the COM3 port which is what the O2 sensor was when I plugged it in
# check to see if it is COM3 before running
# Will try optimise so it selects automatically soon
with serial.Serial('COM3', 576000, timeout=1) as ser:
    print(ser.name)

    while True:
        # according to manual send D to get response
        ser.write('D'.encode('ascii')) 
        if(ser.in_waiting > 0): #checks if there is bytes to be read
            serial_output = ser.readline() #reads to newline character
            # print(type(serial_output))
            print(serial_output.decode('ascii')) 
            # print(serial_output)