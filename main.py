from alicat_flowmeter_control import flow_control
from oxygen_plotting import oxygen_plotting
from oxygen_sensor import read_O2_sensor
import multiprocessing 
import time
from GUI import create_gui

example_schedule = {'number_of_steps' : 3,
                    'change_time' : 8,
                    'step_lengths' : [20,20,20],
                    'step_total_flow' : [100,100,100],
                    'step_composition' : [1,10,20]
                    }

def main(use_example_schedule = False):
    if  not use_example_schedule:
        schedule = {'number_of_steps' : None,
                    'change_time' : None,
                    'step_lengths' : None,
                    'step_total_flow' : None,
                    'step_composition' : None
                    }
        # get user defined number of steps in their program
        
        while True:
            schedule['number_of_steps'] = input('Enter number of steps: ')
            #checks if input is an integer and if so breaks the loop
            try:
                int(schedule['number_of_steps'])
                break
            #if input is not an integer, prints error message and loops back to start
            # this allows for integer input next time
            except ValueError:
                print('Number of steps must be an integer')

        # get user defined rest time between step changes
        while True:
            schedule['change_time'] = input('Enter amount of rest time between step changes (mins) (rec 5 mins): ')
            try:
                int(schedule['change_time'])
                break
            except ValueError:
                print('Rest time must be an integer')
                
        # get user defined step lengths
        for i in range(schedule['number_of_steps']):
            while True:
                schedule['step_lengths'].append(input('Enter step length for step {} (mins): '.format(i+1)))
                try:
                    int(schedule['step_lengths'][i])
                    break
                except ValueError:
                    print('Step length must be an integer')   

        # get user defined step total flow rates
        for i in range(schedule['number_of_steps']):
            while True:
                schedule['step_total_flow'].append(input('Enter total flow rate for step {} (sccm): '.format(i+1)))
                try:
                    int(schedule['step_total_flow'][i])
                    break
                except ValueError:
                    print('Total flow rate must be an integer')
                    continue
            
        # get user defined step compositions
        for i in range(schedule['number_of_steps']):
            while True:
                schedule['step_composition'].append(input('Enter O2 composition for step {} (percent): '.format(i+1)))
                try:
                    int(schedule['step_composition'][i])
                    break
                except ValueError:
                    print('O2 composition must be an integer')
                        
        # checks the schedule makes sense
        if len(schedule['step_lengths']) != schedule['number_of_steps']:
            raise Exception('Number of steps does not match amount of step lengths defined')
        if len(schedule['step_total_flow']) != schedule['number_of_steps']:
            raise Exception('Number of steps does not match amount of step total flow rates defined')
        if len(schedule['step_composition']) != schedule['number_of_steps']:
            raise Exception('Number of steps does not match amount of step compositions defined')
        
        for i in range(schedule['number_of_steps']):
            print ('Starting step {} of {}'.format(i+1,schedule['number_of_steps']))
            print('Step length: {} mins'.format(schedule['step_lengths'][i]))
            print('Total flow rate: {} sccm'.format(schedule['step_total_flow'][i]))
            print('O2 composition: {} percent'.format(schedule['step_composition'][i]))
            flow_control(schedule['step_total_flow'][i],schedule['step_composition'][i])
            time.sleep(schedule['step_lengths'][i]*60)
            print('Step {} of {} complete'.format(i+1,schedule['number_of_steps']))
            if i != schedule['number_of_steps']-1:
                print('Resting for {} mins'.format(schedule['change_time']))
                time.sleep(schedule['change_time']*60)
    



if __name__ == "__main__":
    process1 = multiprocessing.Process(target=main)
    process2 = multiprocessing.Process(target=oxygen_plotting)

    # Start the processes
    process1.start()
    process2.start()

    # Wait for both processes to finish
    process1.join()
    process2.join()
    