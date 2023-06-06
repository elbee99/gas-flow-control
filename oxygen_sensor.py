import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
serial_output = ""

def read_O2_sensor():
    """
    Scans through the COM ports to find the one that the oxygen sensor is
    located on. Then reads the oxygen sensor and returns the oxygen 
    concentration in ppm
    Returns:
        oxygen_ppm (float): Oxygen concentration in ppm
    """
    for port in range(1,17):
        try:
            with serial.Serial('COM{}'.format(port), 57600, timeout=1) as ser: 
            # with serial.Serial('COM4', 57600, timeout=1) as ser: 
                # print(ser.name)
                # while time.time()-start_time < 20: 
                ser.write('D'.encode('ascii'))
                time.sleep(0.1) #necessary to allow the sensor to respond
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
                        if oxygen_ppm == None:
                             return str(0.0)
                        return oxygen_ppm
        except Exception:
            pass

if __name__ == '__main__':
     print(read_O2_sensor())