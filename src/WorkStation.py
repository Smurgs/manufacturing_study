class WorkStation(object):
    def __init__(self, name, rv, buffers, event_queue):
        self.name = name
        self.rv = rv
        self.buffers = buffers
        self.idle = True
        self.components_completed = 0
        self.event_queue = event_queue
        self.active_components = []
        self.completed_components = []

    def is_idle(self):
        return self.idle

    def components_ready(self):
        for componentBuffer in self.buffers:
            if componentBuffer.size() == 0:
                return False
        return True

    def start_work(self, time):
        for componentBuffer in self.buffers:
            self.active_components.append(componentBuffer.remove(time))
        self.event_queue.append((time + self.rv.rvs(), self.complete))
        self.idle = False
        print('%.3f\t%s starting' % (time, self.name))

    def complete(self, time):
        self.idle = True
        self.components_completed += 1
        for component in self.active_components:
            component.completed(time)
            self.completed_components.append(component)
        self.active_components = []
        print('%.3f\t%s completed' % (time, self.name))