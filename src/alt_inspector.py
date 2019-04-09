import random

from src.Component import Component


# Insp1 normally sends to C1
# The queue between Inspector 1 and 2
# Insp 1 pops item

# Insp1
# if queue is empty:
#   send to buffer 11
# else:
#   pop number from queue
#   send to that buffer (either 21 or 31)

# Insp2
# add 2 or 3 to queue when placing a component in buffer 22 or 33

class AltInspector(object):


    def __init__(self, name, rv, event_queue, b11, b21, b31, b22, b33, component_queue):
        self.name = name
        self.rv = rv
        self.time_blocked = 0
        self.start_of_block = 0
        self.component = None
        self.idle = True
        self.event_queue = event_queue
        self.b11 = b11
        self.b21 = b21
        self.b31 = b31
        self.b22 = b22
        self.b33 = b33
        self.next_buffer = 0
        self.component_placed = False
        self.component_queue = component_queue

    def start(self, time):
        self.idle = False
        self.time_blocked = self.time_blocked + (time - self.start_of_block)
        if self.name == 'insp1':
            self.component = Component(time, component_type=1)
            self.event_queue.append((time + self.rv[0].rvs(), self.complete))
        else:
            if random.randint(0, 1) == 0:
                self.component = Component(time, component_type=2)
                self.event_queue.append((time + self.rv[0].rvs(), self.complete))
            else:
                self.component = Component(time, component_type=3)
                self.event_queue.append((time + self.rv[1].rvs(), self.complete))
        print('%.3f\t%s starting to inspect component %d' % (time, self.name, self.component.type))

    def complete(self, time):
        self.idle = True
        print('%.3f\t%s finished inspecting component %d' % (time, self.name, self.component.type))
        self.start_of_block = time
        # Routing Algorithm (Round Robin)
        component_placed = False
        if self.name == 'insp1':
            if len(self.component_queue) > 0:
                next_buffer = self.component_queue.pop(0)

                if next_buffer == 2:
                    if self.b21.size() <2:
                        # place in b21
                        self.b21.add(self.component, time)
                        self.event_queue.append((time, self.start))
                        component_placed = True
                    else:
                        self.component_queue.insert(0, 2)
                elif next_buffer == 3:
                    if self.b31.size() <2:
                        # place in b31
                        self.b31.add(self.component, time)
                        self.event_queue.append((time, self.start))
                        component_placed = True
                    else:
                        self.component_queue.insert(0, 3)

            if not component_placed:
                if self.b11.size() >= 2:
                    # Blocking pattern
                    self.b11.blockingFlag = True
                    self.b11.blockingEvent = self.unblocked
                else:
                    # place in b11
                    self.b11.add(self.component, time)
                    self.event_queue.append((time, self.start))


            # self.component_placed = False
            # for _ in range(3):
            #     if self.next_buffer == 0 and not self.b11.size() >= 2:
            #         self.b11.add(self.component, time)
            #         self.event_queue.append((time, self.start))
            #         self.component_placed = True
            #         print('%.3f\tAdded to buffer b11' % time)
            #         break
            #
            #     elif self.next_buffer == 1 and not self.b21.size() >= 2:
            #         self.b21.add(self.component, time)
            #         self.event_queue.append((time, self.start))
            #         self.component_placed = True
            #         print('%.3f\tAdded to buffer b21' % time)
            #         break
            #
            #     elif self.next_buffer == 2 and not self.b31.size() >= 2:
            #         self.b31.add(self.component, time)
            #         self.event_queue.append((time, self.start))
            #         self.component_placed = True
            #         print('%.3f\tAdded to buffer b31' % time)
            #         break
            #
            #     self.next_buffer+=1
            #     self.next_buffer = self.next_buffer % 3
            #
            # if not self.component_placed:
            #     self.b11.blockingFlag = True
            #     self.b11.blockingEvent = self.unblocked
            #     self.next_buffer+=1
            #     self.next_buffer = self.next_buffer % 3
            #     print('%.3f\tWaiting for Buffer 11 to clear' % time)



        elif self.component.type == 2:
            self.component_queue.append(2)
            if self.b22.size() >= 2:
                self.b22.blockingFlag = True
                self.b22.blockingEvent = self.unblocked
            else:
                self.b22.add(self.component, time)
                self.event_queue.append((time, self.start))

        else:
            self.component_queue.append(3)
            if self.b33.size() >= 2:
                self.b33.blockingFlag = True
                self.b33.blockingEvent = self.unblocked
            else:
                self.b33.add(self.component, time)
                self.event_queue.append((time, self.start))

    def close(self, time):
        if self.idle:
            self.time_blocked = self.time_blocked + (time - self.start_of_block)

    def unblocked(self, buffer, time):
        buffer.add(self.component, time)
        self.event_queue.append((time, self.start))
