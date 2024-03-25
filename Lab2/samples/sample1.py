class Animal: #superclass
    def __init__(self, name, speed):
        self._name = name
        self._speed = speed

    def __del__(self):
        print(f"An instance of class Animal {self._name} was destroyed")

    def sayHello(self):
        print(f"Hello, I am {self._name}, my speed is {self._speed}")

    def speedUp(self, delta):
        self._speed += delta

    def speedDown(self, delta):
        if self._speed >= delta:
            self._speed -= delta
        else:
            self.__stop()

    def __stop(self):
        self._speed = 0

    def getName(self):
        return self._name


class Rabbit(Animal): #subclass
    def __init__(self, name, speed, jmpPerStep):
        Animal.__init__(self, name, speed)
        self._jmpPerStep = jmpPerStep
        self._jmpCounter = 0

    def __del__(self):
        Animal.__del__(self)
        print(f"An instance of class Rabbit {self._name} was destroyed")
        print(f"Rabbit {self._name} had {self._jmpCounter} jumps")

    def step(self, stepAmount):
        print(f"Rabbit {self._name} jumped {self._jmpPerStep * stepAmount} times")
        self._jmpCounter += self._jmpPerStep * stepAmount

class RunningRabbit(Rabbit): #subclass of Rabbit
    def __init__(self, name, speed, jmpPerStep):
        Rabbit.__init__(self, name, speed, jmpPerStep)

    def __del__(self):
        print(f"An instance of class RunningRabbit {self._name} was destroyed")

    def run(self, distance):
        print(f"RunningRabbit {self._name} started")
        i = 0
        while i < distance:
            print(f"RunningRabbit {self._name} runs {self._speed} km/h")
            if i % 2 == 0:
                self.step(1)
            if i < distance // 2:
                self.speedUp(1)
            else:
                self.speedDown(1)
            i += 1
        print(f"RunningRabbit {self._name} stopped")

an1 = RunningRabbit("Bob", 1, 1)
an1.sayHello()
del an1

an2 = RunningRabbit("Rob", 5, 2)
an2.run(10)
an2.sayHello()
del an2
