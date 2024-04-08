def logPrintingOnSet(cls):
    oldSetAttr = cls.__setattr__
    def newSetAttr(self, key, value):
        print("Setting ", key, "=", value)
        return oldSetAttr(self, key, value)
    cls.__setattr__ = newSetAttr
    return cls

@logPrintingOnSet
class Point:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
    
    def sayHello(self):
        print("Hello, I am", self.name)
    
p1 = Point("A", 1, 2)
p2 = Point("B", 5, 9)
p1.x = 100
p2.y = 50
p2.sayHello()

del p1
del p2