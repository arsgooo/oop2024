from abc import ABC, abstractmethod
from threading import Thread
import time

class User:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.progress = {}

    def update_progress(self, course_name, lectures_completed, tests_completed):
        if course_name not in self.progress:
            self.progress[course_name] = {"lectures_completed": 0, "tests_completed": 0}
        self.progress[course_name]["lectures_completed"] += lectures_completed
        self.progress[course_name]["tests_completed"] += tests_completed

    def show_progress(self):
        print(f"\n--- PROGRESS FOR {self.name} ---")
        for course_name, progress_data in self.progress.items():
            print(f"Course: {course_name}")
            print(f"Lectures completed: {progress_data['lectures_completed']}")
            print(f"Tests completed: {progress_data['tests_completed']}")
            print()

class Course(ABC):
    def __init__(self, name, cost, lectures_total, tests_total):
        self.name = name
        self.cost = cost
        self.lectures_total = lectures_total
        self.tests_total = tests_total

    def take_course(self, user):
        thread = Thread(target=self._take_course, args=(user,))
        thread.start()

    def _take_course(self, user):
        self.register()
        if self.pay(user):
            print(f"Remaining balance for {user.name}: ${user.balance}")
            lectures_completed, tests_completed = self.complete_course()
            user.update_progress(self.name, lectures_completed, tests_completed)
            self.issue_certificate(user)
            user.show_progress()
        else:
            print("Payment failed. Insufficient funds.")

    def register(self):
        print(f"\nRegistering for {self.name} course...")
    
    @abstractmethod
    def pay(self, user):
        pass

    def complete_course(self):
        print(f"\nWatching {self.lectures_total} lectures...")
        time.sleep(2)
        lectures_completed = self.lectures_total
        print(f"Taking {self.tests_total} tests...")
        time.sleep(1)
        tests_completed = self.tests_total
        return lectures_completed, tests_completed

    def issue_certificate(self, user):
        print(f"Congratulations, {user.name}! You've successfully completed {self.name} course and received a certificate.")

class PayPalCourse(Course):
    def pay(self, user):
        discounted_cost = self.cost * 0.8  # 20% discount for users who pay via PayPal
        print(f"Paying ${discounted_cost} for the {self.name} course using PayPal...")
        if discounted_cost <= user.balance:
            user.balance -= discounted_cost
            return True
        else:
            return False

class CreditCardCourse(Course):
    def pay(self, user):
        print(f"Paying ${self.cost} for the {self.name} course using Credit Card...")
        if self.cost <= user.balance:
            user.balance -= self.cost
            return True
        else:
            return False

def main():
    user = User("John", 100)

    while True:
        print("\nWelcome to the Online Learning Platform!")
        print("Choose a course:")
        print("1. Programming Course")
        print("2. Language Course")
        choice = input("Enter your choice (1 or 2): ")

        if choice == "1":
            print(f"\n{user.name}'s balance: ${user.balance}")
            print("\nChoose a programming course:")
            print("1. Python")
            print("2. Java")
            print("3. C++")
            programming_choice = input("Enter your choice (1, 2, or 3): ")
            payment_choice = input("Choose payment method: 1. PayPal 2. Credit Card: ")

            if programming_choice == "1":
                if payment_choice == "1":
                    course = PayPalCourse("Python", 50, 50, 10)
                elif payment_choice == "2":
                    course = CreditCardCourse("Python", 50, 50, 10)
                else:
                    print("Invalid payment method. Exiting...")
                    return
            elif programming_choice == "2":
                if payment_choice == "1":
                    course = PayPalCourse("Java", 60, 60, 12)
                elif payment_choice == "2":
                    course = CreditCardCourse("Java", 60, 60, 12)
                else:
                    print("Invalid payment method. Exiting...")
                    return
            elif programming_choice == "3":
                if payment_choice == "1":
                    course = PayPalCourse("C++", 70, 70, 15)
                elif payment_choice == "2":
                    course = CreditCardCourse("C++", 70, 70, 15)
                else:
                    print("Invalid payment method. Exiting...")
                    return
            else:
                print("Invalid choice. Exiting...")
                return
        elif choice == "2":
            print(f"\n{user.name}'s balance: ${user.balance}")
            print("Choose a language course:")
            print("1. English")
            print("2. German")
            print("3. Polish")
            language_choice = input("Enter your choice (1, 2, or 3): ")
            payment_choice = input("Choose payment method: 1. PayPal 2. Credit Card: ")

            if language_choice == "1":
                if payment_choice == "1":
                    course = PayPalCourse("English", 40, 40, 8)
                elif payment_choice == "2":
                    course = CreditCardCourse("English", 40, 40, 8)
                else:
                    print("Invalid payment method. Exiting...")
                    return
            elif language_choice == "2":
                if payment_choice == "1":
                    course = PayPalCourse("German", 45, 45, 9)
                elif payment_choice == "2":
                    course = CreditCardCourse("German", 45, 45, 9)
                else:
                    print("Invalid payment method. Exiting...")
                    return
            elif language_choice == "3":
                if payment_choice == "1":
                    course = PayPalCourse("Polish", 35, 35, 7)
                elif payment_choice == "2":
                    course = CreditCardCourse("Polish", 35, 35, 7)
                else:
                    print("Invalid payment method. Exiting...")
                    return
            else:
                print("Invalid choice. Exiting...")
                return
        else:
            print("Invalid choice. Exiting...")
            return

        course.take_course(user)

if __name__ == "__main__":
    main()
