from alicat_flowmeter_control import flow_control
from oxygen_plotting import oxygen_plotting
from oxygen_sensor import read_O2_sensor
import multiprocessing 
from GUI import create_gui

if __name__ == "__main__":
    process1 = multiprocessing.Process(target=create_gui)
    process2 = multiprocessing.Process(target=oxygen_plotting)

    # Start the processes
    process1.start()
    process2.start()

    # Wait for both processes to finish
    process1.join()
    process2.join()
    