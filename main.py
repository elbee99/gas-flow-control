from alicat_flowmeter_control import flow_control
from oxygen_plotting import oxygen_plotting
from oxygen_sensor import read_O2_sensor
from threading import Thread

total_flow = 100 
O2_set_point = 15
O2_conc_filepath = 'oxygen_conc.txt'

t1 = Thread(target=flow_control, args=(total_flow,O2_set_point))
t2 = Thread(target=oxygen_plotting, args=(O2_conc_filepath))

t1.start()
t2.start()

