import zope.interface

class IRunner(zope.interface.Interface):
    speed = zope.interface.Attribute('The speed attribute')

    def run(self, x):
        pass

    def stop(self):
        pass

    def speed_up(self, x):
        pass

    def slow_down(self, x):
        pass

    def is_running(self):
        pass

@zope.interface.implementer(IRunner)
class RunningEntity:
    def __init__(self):                                                         
        self.speed = 0

    def run(self, x):
        self.speed = x

    def stop(self):
        self.speed = 0

    def speed_up(self, x):                                                  
        self.speed += x
    
    def slow_down(self, x):
        if self.speed > x:
            self.speed -= x
        else:
            self.stop()

    def is_running(self):
        if self.speed > 0:
            return True
        return False

obj = RunningEntity()
