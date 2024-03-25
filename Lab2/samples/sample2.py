from multipledispatch import dispatch

class Transport: #superclass
    def __init__ (self, name, weight, height, length, loading):
        self._name=name
        self._weight=weight
        self._length=length
        self._height=height
        self._loading=loading
        self._speed=0

    def sayHello(self):
        print("Hello, I am ", self._name)

class Watercraft(Transport):
    def __init__(self, waterSpeedNominal, waterCarryingCapacity, name, weight, height, length, loading):
        Transport.__init__(self, name, weight, height, length, loading)
        self._waterSpeedNom=waterSpeedNominal
        self._waterCarCap=waterCarryingCapacity

    def sailing(self, distance):
        self._speed=self._waterSpeedNom*self._waterCarCap/self._loading
        print(self._name," is sailing, current speed: ", self._speed, ", duration: ", distance/self._speed)
        return distance/self._speed
    
class Vehicle (Transport):
    def __init__(self, landSpeedNominal, landCarryingCapacity, name, weight, height, length, loading) :
        Transport.__init__(self, name, weight, height, length, loading)
        self._landSpeedNom=landSpeedNominal
        self._landCarCap=landCarryingCapacity

    def riding(self, distance):
        self._speed=self._landSpeedNom*self._landCarCap/self._loading
        print (self._name," is riding, current speed: ", self._speed, ", duration: ", distance/self._speed)
        return distance/self._speed
    
class Amfibia (Vehicle, Watercraft): #subclass
    def __init__(self, name, weight, height, length, loading, landSpeedNominal, landCarryingCapacity,
                waterSpeedNominal, waterCarryingCapacity):
        Vehicle.__init__ (self, landSpeedNominal, landCarryingCapacity, name, weight, height, length, loading)
        Watercraft.__init__(self, waterSpeedNominal, waterCarryingCapacity, name, weight, height, length, loading)
    
    def __del__(self):
        print ("An instance of class Amfibia ", self._name, " was destroyed")

    def sayHello(self):
        print("Amfibia method called: Hello, I am ", self._name)

    @dispatch(list)
    def run(self, route):
        print("Amfibia ", self._name," started")
        totalTime=0
        for i in range(len(route)):
            if route[i][0]=="land":
                totalTime=totalTime+super().riding(route[i][1])
            else:
                totalTime=totalTime+super().sailing(route[i][1])
        print("Amfibia ", self._name, " stopped")
        return totalTime
    
    @dispatch(int, int)
    def run(self, landDistance, waterDistance):
        print("Amfibia ", self._name, " started")
        totalTime_riding=0
        totalTime_sailing=0
        totalTime_riding=totalTime_riding+super().riding(landDistance)
        totalTime_sailing=totalTime_sailing+super().sailing(waterDistance)
        print("Amfibia ", self._name, " stopped")
        return totalTime_riding, totalTime_sailing

curRoute=[["land", 100], ["water", 3], ["land", 50], ["water", 2], ["land", 75]]
amf=Amfibia ("Carol", 1500, 1, 3, 500, 100, 2000, 50, 500)
amf.sayHello()
print("Time of trip: ", amf.run(curRoute))
print("Time of trip: ", amf.run(100, 100))
del amf