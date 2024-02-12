class Animal:
    kind = "warm_blooded"
    counter = 0

    @staticmethod
    def __printAmount(startMess):
        print(startMess, ": now ", Animal.counter, " animals exist")

    def __init__(self, name, speed):
        self.__name = name
        self.speed = speed
        Animal.counter += 1
        self.__printAmount(self.__name)
        
    def __del__(self):
        Animal.counter -= 1
        print("Now ", Animal.counter, " animals left")

    def sayHello(self):
        print("Hello, I am ", self.__name, ", my speed is ", self.speed)

    def speedUp(self, delta):
        self.speed = self.speed + delta

    def speedDown(self, delta):
        if(self.speed >= delta):
            self.speed = self.speed - delta

    def stop(self):
        self.speed = 0

    def getName(self):
        return self.__name

an1 = Animal("Kitty", 1)
an2 = Animal("Puppy", 2)
an3 = Animal("Big dog", 5)

an3.sayHello()
an3.speedUp(20)
an3.speedDown(15)
an3.sayHello()

an2.stop()
an2.sayHello()

print(an1._Animal__name)

print(an1.__dict__)