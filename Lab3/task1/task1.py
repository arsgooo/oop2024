# Створити абстрактний клас Клієнт, який містить інформацію про рух коштів клієнтів банку. 
# Створити два похідні класи: Приватна_особа, Корпоративний_клієнт. 
# Приватна_особа може покласти кошти собі на рахунок не частіше один раз на 5 днів, 
# а Корпоративний_клієнт отримує заробітку плату не більше 2 разів на місяць. 
# Обидва клієнти можуть знімати кошти з рахунка або перераховувати кошти на інший рахунок. 
# Створити клас-контейнер Клієнти, який містить інформацію про різних клієнтів, вивести інформацію по кожному клієнту.

from abc import ABCMeta, abstractmethod
from collections.abc import MutableSequence
from datetime import datetime, timedelta

class Customer(metaclass=ABCMeta):
    def __init__(self, name, balance):
        self._name = name
        self._balance = balance
        self._last_transaction_date = None

    @abstractmethod
    def topUp(self, amount):
        pass

    def withdraw(self, amount, fee):
        amount_to_be_withdrawn = amount + amount*fee
        self._balance -= amount_to_be_withdrawn
        self._last_transaction_date = datetime.now()
        print(f"Success! {self._name}'s current balance: {self._balance} (-{amount_to_be_withdrawn})\n")
    
    def transfer(self, amount, recipient):
        if self._balance >= amount:
            if (isinstance(self, Corporate) and isinstance(recipient, Individual)) or (isinstance(self, Individual) and isinstance(recipient, Corporate)):
                self._balance -= amount + 5
            elif (isinstance(self, Individual) and isinstance(recipient, Individual)) or (isinstance(self, Corporate) and isinstance(recipient, Corporate)):
                self._balance -= amount
            recipient._balance += amount
            self._last_transaction_date = datetime.now()
            print(f"Success! {self._name}'s balance: {self._balance} (-{amount})")
            print(f"{recipient._name}'s balance: {recipient._balance} (+{amount})\n")
        else:
            print("Not enough money to execute the operation. Please, top up balance and try again.\n")

class Individual(Customer):
    def topUp(self, amount):
        today = datetime.now()
        if self._last_transaction_date is None or today - self._last_transaction_date >= timedelta(days=5):
            self._balance += amount
            self._last_transaction_date = datetime.now()
            print(f"Success! {self._name}'s current balance: {self._balance} (+{amount})\n")
        else:
            print("Unable to top-up balance. Try a bit later.")

class Corporate(Customer):
    def __init__(self, name, balance):
        super().__init__(name, balance)
        self._transactions_this_month = 0
    
    def topUp(self, amount):
        if self._transactions_this_month < 2:
            self._balance += amount
            self._last_transaction_date = datetime.now()
            self._transactions_this_month += 1
            print(f"Success! {self._name}'s current balance: {self._balance} (+{amount})\n")
        else:
            print("Unable to execute the operation. Try a bit later.")

class CustomersContainer(MutableSequence):
    def __init__(self, *clients):
        self._clients = list(clients)

    def __len__(self):
        return len(self._clients)

    def __getitem__(self, index):
        return self._clients[index]

    def __setitem__(self, index, value):
        if not isinstance(value, Customer):
            raise TypeError("Invalid customer type")
        self._clients[index] = value

    def __delitem__(self, index):
        del self._clients[index]

    def insert(self, index, value):
        if not isinstance(value, Customer):
            raise TypeError("Invalid customer type")
        self._clients.insert(index, value)

    def __str__(self):
        return ''.join(
            f"Name: {client._name} \nBalance: ${client._balance} \nLast transaction date: {client._last_transaction_date}\n\n"
            for client in self._clients
        )



individual = Individual("Ryan Gosling", 1300000)
individual.withdraw(300000, 0.01)

corporate = Corporate("Pablo Schreiber", 1200000)
corporate.topUp(50000)
corporate.topUp(1000)
# corporate.topUp(2000) # third top-up will cause an error
corporate.transfer(200000, individual)
# corporate.transfer(10000, "John Newman") # will cause an error

customers = CustomersContainer(individual, corporate)

print("--- Initial list ---")
print(customers)

customers.append(Corporate("Ukrzaliznytsia", 100000))
print("\n--- List after adding a new customer ---")
print(customers)

customers[1] = Individual("Ann Hashlow", 30000)
print("\n--- List after updating a customer ---")
print(customers)

del customers[0]
print("\n--- List after deleting the first customer ---")
print(customers)