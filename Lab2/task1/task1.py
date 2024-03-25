# Описати ієрархію персоналу організації (три посади з різними посадовими обов'язками). 
# Кожній посаді відповідає певна схема нарахування ЗП, яка їй встановлюється у момент створення 
# і не може бути передана іншому об'єкту.

import datetime

################################    SALARIES    #######################################
class Salary:
    def calculate_salary(self):
        raise NotImplementedError("The method is not implemented")

class SalaryChief(Salary):
    def __init__(self, monthly_rate):
        self._monthly_rate = monthly_rate

    def calculate_salary(self):
        return 1.2*self._monthly_rate
    
class SalaryProjectManager(Salary):
    def __init__(self, hourly_rate, hours_per_month, prize):
        self._hourly_rate = hourly_rate
        self._hours_per_month = hours_per_month
        self._prize = prize

    def calculate_salary(self):
        return self._hourly_rate*self._hours_per_month+self._prize
    
class SalaryDeveloper(Salary):
    def __init__(self, monthly_rate, working_days, present_days):
        self._monthly_rate = monthly_rate
        self._working_days = working_days
        self._present_days = present_days

    def calculate_salary(self):
        return self._monthly_rate/self._working_days*self._present_days

################################    WORKERS    #######################################
class Organization:
    def __init__(self):
        self.staff = []

    def add_worker(self, worker):
        self.staff.append(worker)

class Worker: # superclass
    def __init__(self, name, age, sex, salary, start_date):
        self.name = name
        self.age = age
        self.sex = sex
        self._salary = salary
        self.start_date = start_date

    def total_salary(self): 
        return int(self._salary.calculate_salary())
    
    def __str__(self):
        time_worked = datetime.datetime.now() - self.start_date
        years = time_worked.days // 365
        months = (time_worked.days % 365) // 30
        days = (time_worked.days % 365) % 30
        print("-----------------------------------------------")
        return f"Name: {self.name} \nAge: {self.age} \nSex: {self.sex} \nSalary: ${self.total_salary()} \nBegan to work: {self.start_date.strftime("%d/%m/%Y")} \nAlready works for: {years} years, {months} months, {days} days"

class Chief(Worker):
    def __init__(self, name, age, sex, monthly_rate, start_date):
        super().__init__(name, age, sex, SalaryChief(monthly_rate), start_date)

class ProjectManager(Worker):
    def __init__(self, name, age, sex, hourly_rate, hours_per_month, prize, start_date):
        super().__init__(name, age, sex, SalaryProjectManager(hourly_rate, hours_per_month, prize), start_date)

class Developer(Worker):
    def __init__(self, name, age, sex, monthly_rate, working_days, present_days, start_date):
        super().__init__(name, age, sex, SalaryDeveloper(monthly_rate, working_days, present_days), start_date)

################################    MAIN PROGRAM    #######################################
if __name__ == "__main__":
    org = Organization()

    chief = Chief("Josh", 35, "Male", 3000, datetime.datetime(2020, 5, 7)) # name, age, sex, monthly_rate, start_date
    org.add_worker(chief)

    pm1 = ProjectManager("Ann", 23, "Female", 15, 160, 300, datetime.datetime(2022, 1, 13)) # name, age, sex, hourly_rate, hours_per_month, prize, start_date
    org.add_worker(pm1)

    pm2 = ProjectManager("Ann1", 24, "Female", 16, 170, 400, datetime.datetime(2022, 5, 25)) # name, age, sex, hourly_rate, hours_per_month, prize, start_date
    org.add_worker(pm2)

    developer1 = Developer("Max", 29, "Male", 1500, 20, 17, datetime.datetime(2021, 9, 27)) # name, age, sex, monthly_rate, working_days, present_days, start_date
    org.add_worker(developer1)

    developer2 = Developer("Max1", 35, "Male", 1700, 20, 19, datetime.datetime(2021, 9, 27)) # name, age, sex, monthly_rate, working_days, present_days, start_date
    org.add_worker(developer2)

    developer3 = Developer("Max2", 24, "Male", 1650, 20, 20, datetime.datetime(2021, 9, 27)) # name, age, sex, monthly_rate, working_days, present_days, start_date
    org.add_worker(developer3)

    for worker in org.staff:
        print(worker)