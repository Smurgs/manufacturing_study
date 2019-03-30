class Component(object):
    def __init__(self, time, component_type):
        self.active = True
        self.start_time = time
        self.type = component_type
        self.system_time = None

    def completed(self, time):
        self.system_time = time - self.start_time
        self.active = False
