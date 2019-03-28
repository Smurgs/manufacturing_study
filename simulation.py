from collections import deque
import random

import scipy.stats as stats


class Inspector(object):
    def __init__(self, name, rv):
        self.name = name
        self.rv = rv
        self.time_blocked = 0
        self.start_of_block = 0
        self.component_type = 0
        self.idle = True

    def start(self):
        self.idle = False
        self.time_blocked = self.time_blocked + (time - self.start_of_block)
        if self.name == 'insp1':
            self.component_type = 1
            event_queue.append((time + self.rv[0].rvs(), self.complete))
        else:
            if random.randint(0, 1) == 0:
                self.component_type = 2
                event_queue.append((time + self.rv[0].rvs(), self.complete))
            else:
                self.component_type = 3
                event_queue.append((time + self.rv[1].rvs(), self.complete))
        print('%.3f\t%s starting to inspect component %d' % (time, self.name, self.component_type))

    def complete(self):
        self.idle = True
        print('%.3f\t%s finished inspecting component %d' % (time, self.name, self.component_type))
        self.start_of_block = time
        if self.name == 'insp1':
            if buffer_ws1_c1.size() <= buffer_ws2_c1.size() and buffer_ws1_c1.size() <= buffer_ws3_c1.size():
                buffer_ws1_c1.add(1)
                if buffer_ws1_c1.size() > 2:
                    buffer_ws1_c1.blockingFlag = True
                    buffer_ws1_c1.blockingEvent = self.start
                else:
                    event_queue.append((time, self.start))

            elif buffer_ws2_c1.size() <= buffer_ws3_c1.size():
                buffer_ws2_c1.add(1)
                if buffer_ws2_c1.size() > 2:
                    buffer_ws2_c1.blockingFlag = True
                    buffer_ws2_c1.blockingEvent = self.start
                else:
                    event_queue.append((time, self.start))

            else:
                buffer_ws3_c1.add(1)
                if buffer_ws3_c1.size() > 2:
                    buffer_ws3_c1.blockingFlag = True
                    buffer_ws3_c1.blockingEvent = self.start
                else:
                    event_queue.append((time, self.start))

        elif self.component_type == 2:
            buffer_ws2_c2.add(2)
            if buffer_ws2_c2.size() > 2:
                buffer_ws2_c2.blockingFlag = True
                buffer_ws2_c2.blockingEvent = self.start
            else:
                event_queue.append((time, self.start))

        else:
            buffer_ws3_c3.add(3)
            if buffer_ws3_c3.size() > 2:
                buffer_ws3_c3.blockingFlag = True
                buffer_ws3_c3.blockingEvent = self.start
            else:
                event_queue.append((time, self.start))

    def close(self):
        if self.idle:
            self.time_blocked = self.time_blocked + (time - self.start_of_block)



class Buffer(object):
    def __init__(self, name):
        self.name = name
        self.queue = deque()
        self.blockingFlag = False
        self.blockingEvent = None

    def size(self):
        return len(self.queue)

    def add(self, item):
        self.queue.append(item)
        print('%.3f\t%s item added, size: %d' % (time, self.name, self.size()))

    def remove(self):
        self.queue.popleft()
        print('%.3f\t%s item removed, size: %d' % (time, self.name, self.size()))
        if self.blockingFlag:
            self.blockingEvent()
            self.blockingFlag = False


class WorkStation(object):
    def __init__(self, name, rv, components):
        self.name = name
        self.rv = rv
        self.components = components
        self.idle = True
        self.components_completed = 0

    def is_idle(self):
        return self.idle

    def components_ready(self):
        for componentBuffer in self.components:
            if componentBuffer.size() == 0:
                return False
        return True

    def start_work(self):
        global event_queue
        global time
        for componentBuffer in self.components:
            componentBuffer.remove()
        event_queue.append((time + self.rv.rvs(), self.complete))
        self.idle = False
        print('%.3f\t%s starting' % (time, self.name))

    def complete(self):
        self.idle = True
        self.components_completed += 1
        print('%.3f\t%s completed' % (time, self.name))


# Initialization
time = 0.0
event_queue = []
inspector1 = Inspector('insp1', [stats.expon(loc=0.09, scale=10.27)])
inspector2 = Inspector('insp2', [stats.expon(loc=0.13, scale=15.41), stats.expon(loc=0.03, scale=20.60)])
buffer_ws1_c1 = Buffer('ws1_c1')
buffer_ws2_c1 = Buffer('ws2_c1')
buffer_ws2_c2 = Buffer('ws2_c2')
buffer_ws3_c1 = Buffer('ws3_c1')
buffer_ws3_c3 = Buffer('ws3_c3')
ws1 = WorkStation('ws1', stats.expon(loc=0.01, scale=4.60), [buffer_ws1_c1])
ws2 = WorkStation('ws2', stats.expon(loc=0.09, scale=11.00), [buffer_ws2_c1, buffer_ws2_c2])
ws3 = WorkStation('ws3', stats.expon(loc=0.10, scale=8.69), [buffer_ws3_c1, buffer_ws3_c3])


def main():
    global event_queue
    global time

    # Start inspectors
    inspector1.start()
    inspector2.start()

    while time < 100:
        # Sort event list
        event_queue = sorted(event_queue)

        # Get next
        event = event_queue[0]
        event_queue = event_queue[1:]

        # Advance clock
        time = event[0]

        # Execute event
        event[1]()

        # Start workstations if they are not idle and the components are ready
        for ws in [ws1, ws2, ws3]:
            if ws.is_idle() and ws.components_ready():
                ws.start_work()

    print('\nSimulation complete')
    for insp in [inspector1, inspector2]:
        insp.close()
        print('%s spent %.2f time units blocked' % (insp.name, insp.time_blocked))
    for ws in [ws1, ws2, ws3]:
        print('%s completed %d products' % (ws.name, ws.components_completed))


if __name__ == '__main__':
    main()
