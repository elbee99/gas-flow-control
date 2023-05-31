from alicat import FlowController
from simple_pid import PID
from oxygen_sensor import read_O2_sensor

for number in range(1,17):
    try:
        flow_controller = FlowController(port='COM{}'.format(number))
        gas = flow_controller.get()['gas']
        if gas == 'Ar':
            Ar_port = number
        elif gas == 'O2':
            O2_port = number
    except Exception:
        pass
try:
    flow_controller_O2 = FlowController(port='COM{}'.format(O2_port))
    flow_controller_Ar = FlowController(port='COM{}'.format(Ar_port))
except Exception:
    print('O2 and Ar flow controllers not found, please set manually')

print(flow_controller_O2.get())
print(flow_controller_Ar.get())


flow_controller_O2.set_flow_rate(0)
flow_controller_Ar.set_flow_rate(0)

def flow_control(total_flow, O2_set_point=15):
    pid = PID(1,0.02,0, sample_time = 1, setpoint=O2_set_point, output_limits=(12,24), starting_output=O2_set_point)
    def controlled_system(total_flow=total_flow, O2_set_point=O2_set_point,current_O2_percent = read_O2_sensor()*1000):
        flow_controller_O2.set_flow_rate(total_flow*O2_set_point/100)
        flow_controller_Ar.set_flow_rate(total_flow-(total_flow*O2_set_point/100))
        print(current_O2_percent)
        return current_O2_percent
    while True:
        oxygen_percent = read_O2_sensor()*10e3
        if abs(oxygen_percent-O2_set_point) < 1:
            PID_setpoint = pid(oxygen_percent) #this is the setpoint required the PID controller
            #we need to get current value and feed back into the PID controller
            oxygen_percent = controlled_system(total_flow,PID_setpoint,oxygen_percent)
        else:
            controlled_system(total_flow,O2_set_point,oxygen_percent)

    
