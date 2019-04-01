import numpy as np
import scipy.stats as stats


from numpy import *
import math
import matplotlib.pyplot as plt
from matplotlib import interactive
interactive(True)


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

    INTERVAL = 100
    total_list_product_1 = []
    total_list_product_2 = []
    total_list_product_3 = []

    event_time_1 = []
    event_time_2 = []
    event_time_3 = []

    previous_entry_1 = 0
    previous_entry_2 = 0
    previous_entry_3 = 0

    previous_time = 0
    i = 1
    difference_value = 0

    while time < 10000:
        # Sort event list
        event_queue.sort(key=lambda x: x[0])

        # Get next event
        event = event_queue.pop(0)

        # Advance clock
        time = event[0]

        # Execute event
        event[1](time)

        print("Previous time: " + str(previous_time) + " Current time: " + str(time))

        # Record completed products every given interval
        # JOE's genius time logic
        if((time + previous_time ) > INTERVAL * i):
            previous_time = (time + previous_time) - (INTERVAL * i)
            event_time_1.append(time)
            event_time_2.append(time)
            event_time_3.append(time)
            total_list_product_1.append(len(ws1.completed_components) - previous_entry_1)
            total_list_product_2.append(len(ws2.completed_components) - previous_entry_2)
            total_list_product_3.append(len(ws3.completed_components) - previous_entry_3)
            previous_entry_1 = sum(total_list_product_1)
            previous_entry_2 = sum(total_list_product_2)
            previous_entry_3 = sum(total_list_product_3)
            i += 1
        else:
            previous_time += time



        # Start workstations if they are not idle and the buffers are ready
        for ws in [ws1, ws2, ws3]:
            if ws.is_idle() and ws.components_ready():
                ws.start_work(time)

        previous_time = time

    print('\nSimulation complete')
    for insp in [inspector1, inspector2]:
        insp.close(time)
        print('%s spent %.2f time units blocked' % (insp.name, insp.time_blocked))
    for ws in [ws1, ws2, ws3]:
        print('%s completed %d products' % (ws.name, ws.components_completed))


    # Plot for buffer_1_1
    event_time_11, buffer_sizes_11 = zip(*b11.change_log)
    event_time_21, buffer_sizes_21 = zip(*b21.change_log)
    event_time_22, buffer_sizes_22 = zip(*b22.change_log)
    # avg_queue_items = sum(buffer_sizes)/(len(buffer_sizes))

    print(total_list_product_1)

    # plt.title("Product 1 Throughput every " + str(INTERVAL) + " minutes plot with respect to time")
    #plt.subplot(2, 2, 1)
    plt.plot(event_time_1, total_list_product_1, 'r')
   # plt.subplot(2, 2, 2)
   # plt.plot(event_time_2, total_list_product_2, 'b')
   # plt.subplot(2, 2, 3)
   # plt.plot(event_time_3, total_list_product_3, 'g')
    plt.xlabel("Time")
    plt.ylabel("Buffer Size")
    plt.ylim([0, 4])
    plt.show()

    avg_sys_time = np.mean([x.system_time for x in ws1.completed_components])
    avg_arrival_time = np.mean([x for x in b11.inter_arrival_times])
    print('Average system time for components in workstation1: %.2f' % avg_sys_time)
    print('Average arrival time for buffer_1_1: %.2f' % avg_arrival_time)
    print(avg_sys_time * avg_arrival_time)


if __name__ == '__main__':
    i = 0
    main()
    # while i < REPLICATIONS:
    #     main()
