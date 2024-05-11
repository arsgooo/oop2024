from abc import abstractmethod
from typing import Protocol, runtime_checkable

@runtime_checkable
class SupportsRunningAnimal(Protocol):
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def emit(self):
        pass

class Lion(SupportsRunningAnimal):
    def __init__(self, name):
        self.name = name

    def run(self):
        print(f"Lion {self.name} is running...")

    def emit(self):
        print(f"Lion {self.name} r-r-r-r-r")

class Cat():
    def __init__(self, name):
        self.name = name

    def run(self):
        print(f"Cat {self.name} is running...")

    def emit(self):
        print(f"Cat {self.name} mr-mr-mr-mr-mr")

class Fish():
    def __init__(self, name):
        self.name = name

    def swim(self):
        print(f"Fish {self.name} is swimming...")

def run_all(animals):
    for animal in animals:
        animal.run()

run_all([Lion("King"), Cat("Thomas")])