import random

from src.Component import Component


class Inspector(object):
    def __init__(self, name, rv, event_queue, b11, b21, b31, b22, b33):
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
        if self.name == 'insp1':
            if self.b11.size() <= self.b21.size() and self.b11.size() <= self.b31.size():
                if self.b11.size() >= 2:
                    self.b11.blockingFlag = True
                    self.b11.blockingEvent = self.unblocked
                else:
                    self.b11.add(self.component, time)
                    self.event_queue.append((time, self.start))

            elif self.b21.size() <= self.b31.size():
                if self.b21.size() >= 2:
                    self.b21.blockingFlag = True
                    self.b21.blockingEvent = self.unblocked
                else:
                    self.b21.add(self.component, time)
                    self.event_queue.append((time, self.start))

            else:
                if self.b31.size() >= 2:
                    self.b31.blockingFlag = True
                    self.b31.blockingEvent = self.unblocked
                else:
                    self.b31.add(self.component, time)
                    self.event_queue.append((time, self.start))

        elif self.component.type == 2:
            if self.b22.size() >= 2:
                self.b22.blockingFlag = True
                self.b22.blockingEvent = self.unblocked
            else:
                self.b22.add(self.component, time)
                self.event_queue.append((time, self.start))

        else:
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
