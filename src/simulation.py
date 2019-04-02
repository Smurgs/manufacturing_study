import numpy as np
import scipy.stats as stats


from numpy import *
import math
import matplotlib.pyplot as plt
#from matplotlib import interactive
#interactive(True)


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
REPLICATIONS = 6
INTERVAL = 5
product_count = 0
throughput = []
total_idle_time = 0
idle_probability = []


def main():
    global event_queue
    global time

    # Start inspectors
    inspector1.start(time)
    inspector2.start(time)

    # Insert interval elapsed event into queue
    event_queue.append((time + INTERVAL, elapsed_interval))

    while time < 100000:
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

        # print("Previous time: " + str(previous_time) + " Current time: " + str(time))

        # Record completed products every given interval
        # JOE's genius time logic
        # if ((time + previous_time) > INTERVAL * i):
        #     previous_time = (time + previous_time) - (INTERVAL * i)
        #     event_time_1.append(time)
        #     event_time_2.append(time)
        #     event_time_3.append(time)
        #
        #     total_list_product_1.append(len(ws1.completed_components) - previous_entry_1)
        #     total_list_product_2.append(len(ws2.completed_components) - previous_entry_2)
        #     total_list_product_3.append(len(ws3.completed_components) - previous_entry_3)
        #
        #     event_time_4.append(time)
        #     buffer_sizes_11.append(b11.size())
        #     buffer_sizes_22.append(b22.size())
        #     buffer_sizes_33.append(b33.size())
        #     buffer_sizes_21.append(b21.size())
        #     buffer_sizes_31.append(b31.size())
        #
        #     previous_entry_1 = sum(total_list_product_1)
        #     previous_entry_2 = sum(total_list_product_2)
        #     previous_entry_3 = sum(total_list_product_3)
        #
        #     # previous_entry_4 = sum(buffer_sizes_11)
        #     i += 1
        # else:
        #     previous_time += time
        #
        # plt.axvline
        # previous_time = time

    print('\nSimulation complete')
    for insp in [inspector1, inspector2]:
        insp.close(time)
        print('%s spent %.2f time units blocked' % (insp.name, insp.time_blocked))
    for ws in [ws1, ws2, ws3]:
        print('%s completed %d products' % (ws.name, ws.components_completed))
    print('\nThroughput')
    print(throughput)
    print('Confidence')
    print(confidence_interval(throughput))

    print('\nIdle Probability')
    print(idle_probability)
    print('Confidence')
    print(confidence_interval(idle_probability))

    # Plot throughput
    plt.plot(throughput)
    plt.show()

    # Plot throughput
    plt.plot(idle_probability)
    plt.show()

    avg_sys_time = np.mean([x.system_time for x in ws1.completed_components])
    avg_arrival_time = np.mean([x for x in b11.inter_arrival_times])
    print('Average system time for components in workstation1: %.2f' % avg_sys_time)
    print('Average arrival time for buffer_1_1: %.2f' % avg_arrival_time)
    print(avg_sys_time * avg_arrival_time)


def elapsed_interval(t):
    global product_count
    global throughput
    global total_idle_time
    global idle_probability
    global event_queue

    # Get throughput
    product_count = len(ws1.completed_components) + len(ws2.completed_components) + len(ws3.completed_components)
    throughput.append(product_count / t)

    # Get idle time probability
    total_idle_time = inspector1.time_blocked + inspector2.time_blocked
    idle_probability.append(total_idle_time / t)

    # Set next data collection event
    event_queue.append((t + INTERVAL, elapsed_interval))


def confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), stats.sem(a)
    h = se * stats.t.ppf((1 + confidence) / 2., n - 1)
    return m, m-h, m+h


if __name__ == '__main__':
    main()
