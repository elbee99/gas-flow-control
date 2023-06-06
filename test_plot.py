import time
import datetime
with open('test.txt', 'w') as f:
        start_time = time.time()
        # fig, ax = plt.subplots()
        # ax.set_xlabel('Time (s)')
        # ax.set_ylabel('O$_2$ conc. (%)')
        # line, = ax.plot([],[])
        f.write('Start time=\t{}\n'.format(datetime.datetime.now()))
        f.write('Time (s)\tO2 conc. (ppm)\n')