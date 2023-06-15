from alicat import FlowController
from simple_pid import PID
from oxygen_sensor import read_O2_sensor
import time


def flow_control(total_flow, O2_set_point=15, control_time = None):
    # for number in range(1,17):
    #     try:
    #         flow_controller = FlowController(port='COM{}'.format(number))
    #         gas = flow_controller.get()['gas']
    #         if gas == 'Ar':
    #             Ar_port = number
    #             # print('Ar port is {}'.format(Ar_port))
    #         elif gas == 'O2':
    #             O2_port = number
    #             # print('O2 port is {}'.format(O2_port))
    #     except Exception:
    #         pass
    # try:
    #     flow_controller_O2 = FlowController(port='COM{}'.format(O2_port))
    #     flow_controller_Ar = FlowController(port='COM{}'.format(Ar_port))
    # except Exception:
    #     print('O2 and Ar flow controllers not found, please set manually')
    # print(read_O2_sensor())
    flow_controller_O2 = FlowController(port='COM{}'.format(3))
    flow_controller_Ar = FlowController(port='COM{}'.format(5))
    pid = PID(1,0.02,0, sample_time = 1, setpoint=O2_set_point, output_limits=(12,24), starting_output=O2_set_point)
    def controlled_system(total_flow=total_flow, O2_set_point=O2_set_point,current_O2_percent = float(read_O2_sensor())/1000):
        flow_controller_O2.set_flow_rate(total_flow*O2_set_point/100)
        flow_controller_Ar.set_flow_rate(total_flow-(total_flow*O2_set_point/100))
        # print(current_O2_percent)
        return current_O2_percent
    start_time = time.time()
    if type(control_time) == float or type(control_time) == int:
        while time.time()-start_time < control_time:
            print('Runtime is {0:.2f} seconds'.format(time.time()-start_time))
            oxygen_percent = float(read_O2_sensor())*10e-5
            if abs(oxygen_percent-O2_set_point) < 1:
                PID_setpoint = pid(oxygen_percent) #this is the setpoint required the PID controller
                #we need to get current value and feed back into the PID controller
                oxygen_percent = controlled_system(total_flow,PID_setpoint,oxygen_percent)
            else:
                controlled_system(total_flow,O2_set_point,oxygen_percent)
    else:
        while True:
            oxygen_percent = float(read_O2_sensor())*10e-3
            if abs(oxygen_percent-O2_set_point) < 1:
                PID_setpoint = pid(oxygen_percent) #this is the setpoint required the PID controller
                #we need to get current value and feed back into the PID controller
                oxygen_percent = controlled_system(total_flow,PID_setpoint,oxygen_percent)
            else:
                controlled_system(total_flow,O2_set_point,oxygen_percent)

    
if __name__ == '__main__':
    flow_control(100,15)