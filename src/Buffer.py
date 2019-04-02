from collections import deque


class Buffer(object):
    def __init__(self, name):
        self.name = name
        self.queue = deque()
        self.blockingFlag = False
        self.blockingEvent = None
        self.last_arrival = 0
        self.inter_arrival_times = []
        self.change_log = []

    def size(self):
        return len(self.queue)

    def add(self, item, time):
        self.queue.append(item)
        self.inter_arrival_times.append(time - self.last_arrival)
        self.last_arrival = time
        self.change_log.append((time, self.size()))
        print('%.3f\t%s item added, size: %d' % (time, self.name, self.size()))

    def remove(self, time):
        component = self.queue.popleft()
        self.change_log.append((time, self.size()))
        print('%.3f\t%s item removed, size: %d' % (time, self.name, self.size()))
        if self.blockingFlag:
            self.blockingEvent(self, time)
            self.blockingFlag = False
        return component
