from abc import ABCMeta
from abc import abstractmethod

class Transport(metaclass=ABCMeta):
    def __init__(self, name, weight, height, length, loading):
        self._name = name
        self._weight = weight
        self._height = height
        self._length = length
        self._loading = loading
        self._speed = 0
    
    def sayHello(self):
        print("Hello, I am ", self._name)

    @abstractmethod
    def upgrade(self, x):
        pass

class ModernCar(Transport):
    def upgrade(self, x):
        x += 1

mc = ModernCar("ModernCar_instance", 100, 200, 300, 400)
mc.sayHello()

