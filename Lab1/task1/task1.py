# Описати клас «Геометрична прогресія», який представлятиме собою геометричну прогресію 
# із заданими параметрами та реалізуватиме відповідні дії над нею 
# (1-ий елемент, n-ий елемент, послідовність від k-го до m-го елемента, 
# зміна параметрів прогресії, виведення інформації про існуючі екземпляри). 
# На екран має виводитись у форматі & а, b: {перші 7 членів прогресії  ...}. 
# Створіть декілька екземплярів класу, продемонструйте роботу з ними.

class GeometricProgression:
    __counter = 0 # static variable to count the instances
    
    def __init__(self, b, q):
        self.b = b  # first term
        self.q = q  # common ratio
        GeometricProgression.__counter += 1

    def first_element(self):
        return self.b

    def n_element(self, n):
        return self.b * (self.q ** (n - 1))

    def sequence_from_k_to_m(self, k, m):
        return [self.n_element(i) for i in range(k, m + 1)]

    def change_parameters(self, new_b, new_q):
        self.b = new_b
        self.q = new_q

    def __repr__(self):
        sequence = self.sequence_from_k_to_m(1, 7)
        return f"& {self.b}, {self.q}: {{{', '.join(map(str, sequence))} ...}}"

    @staticmethod
    def instances_count():
        return f"There are {GeometricProgression.__counter} instances now."

progression1 = GeometricProgression(1, 4)
print("PROGRESSION1")
print(f"First element of progression1 is {progression1.first_element()}")
print(progression1)  # & 1, 4: {1, 4, 16, 64, 256, 1024, 4096 ...}

progression2 = GeometricProgression(3, 3)
print("\nPROGRESSION2")
print(f"Fifth element of progression2 is {progression2.n_element(5)}")
print(progression2)  # & 3, 3: {3, 9, 27, 81, 243, 729, 2187 ...}

progression2.change_parameters(7, 2)
print("\nUPDATED PROGRESSION2")
print(progression2)  # & 7, 2: {7, 14, 28, 56, 112, 224, 448 ...}

print("\n" + GeometricProgression.instances_count())