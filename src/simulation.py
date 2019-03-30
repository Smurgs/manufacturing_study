import numpy as np
import scipy.stats as stats

from src.Inspector import Inspector
from src.Buffer import Buffer
from src.WorkStation import WorkStation


# Initialization
time = 0.0
event_queue = []
b11 = Buffer('ws1_c1')
b21 = Buffer('ws2_c1')
b31 = Buffer('ws3_c1')
b22 = Buffer('ws2_c2')
b33 = Buffer('ws3_c3')
inspector1 = Inspector('insp1', [stats.expon(loc=0.09, scale=10.27)], event_queue, b11, b21, b31, b22, b33)
inspector2 = Inspector('insp2', [stats.expon(loc=0.13, scale=15.41), stats.expon(loc=0.03, scale=20.60)], event_queue, b11, b21, b31, b22, b33)
ws1 = WorkStation('ws1', stats.expon(loc=0.01, scale=4.60), [b11], event_queue)
ws2 = WorkStation('ws2', stats.expon(loc=0.09, scale=11.00), [b21, b22], event_queue)
ws3 = WorkStation('ws3', stats.expon(loc=0.10, scale=8.69), [b31, b33], event_queue)


def main():
    global event_queue
    global time

    # Start inspectors
    inspector1.start(time)
    inspector2.start(time)

    while time < 100:
        # Sort event list
        event_queue.sort(key=lambda x: x[0])

        # Get next event
        event = event_queue.pop(0)

        # Advance clock
        time = event[0]

        # Execute event
        event[1](time)

        # Start workstations if they are not idle and the buffers are ready
        for ws in [ws1, ws2, ws3]:
            if ws.is_idle() and ws.components_ready():
                ws.start_work(time)

    print('\nSimulation complete')
    for insp in [inspector1, inspector2]:
        insp.close(time)
        print('%s spent %.2f time units blocked' % (insp.name, insp.time_blocked))
    for ws in [ws1, ws2, ws3]:
        print('%s completed %d products' % (ws.name, ws.components_completed))

    avg_sys_time = np.mean([x.system_time for x in ws1.completed_components])
    avg_arrival_time = np.mean([x for x in b11.inter_arrival_times])
    print('Average system time for components in workstation1: %.2f' % avg_sys_time)
    print('Average arrival time for buffer_1_1: %.2f' % avg_arrival_time)
    print(avg_sys_time * avg_arrival_time)


if __name__ == '__main__':
    main()
