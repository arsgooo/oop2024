from dataclasses import dataclass
import json
import random
from typing import List, Protocol
from enum import Enum

class Priority(Enum):
    NONE = 0
    DISABILITY = 1
    INTERNALLY_DISPLACED = 2
    RESIDENCE_IN_SAME_DISTRICT = 3
    LARGE_FAMILY = 4

class PriorityEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Priority):
            return obj.value
        return super().default(obj)

@dataclass
class PrincipalInfo:
    name: str
    surname: str
    phone_number: str
    email: str
    address: str

@dataclass
class ParentInfo:
    name: str
    surname: str
    phone_number: str
    email: str

@dataclass
class ChildInfo:
    name: str
    surname: str
    birth_date: str
    address: str

@dataclass
class Application:
    application_id: int
    priority: Priority
    principalInfo: PrincipalInfo
    parentInfo: ParentInfo
    childInfo: ChildInfo
    educationForm: str
    supportNeeded: bool
    date: str
    status: str

###   INTERFACES   ### 
class IQueue(Protocol):
    def add_application(self, application: Application):
        pass
    
    def remove_application(self) -> Application:
        pass

class IAdmissionAlgorithm(Protocol):
    def admit_children(self, queue: IQueue, class_capacity: int) -> List[Application]:
        pass

class IFileHandler(Protocol):
    def read_data(self, filename: str) -> List[Application]:
        pass
    
    def save_data(self, filename: str, data: List[Application]):
        pass

    def add_application(self, application: Application, filename: str):
        pass

    def remove_application(self, application_id: int, filename: str) -> bool:
        pass

###   IMPLEMENTATION   ###
class Queue:
    def __init__(self):
        self.queue = []

    def add_application(self, application: Application):
        self.queue.append(application)

    def remove_application(self) -> Application:
        if self.queue:
            return self.queue.pop(0)
        else:
            raise IndexError("Queue is empty")

    def __add__(self, other: 'Queue') -> 'Queue':
        new_queue = Queue()
        new_queue.queue = self.queue + other.queue
        return new_queue

    def __str__(self):
        return str(self.queue)

    def __len__(self) -> int:
        return len(self.queue)

class FirstKChildrenAdmissionAlgorithm:
    def admit_children(self, queue: IQueue, class_capacity: int) -> List[Application]:
        admitted_children = []
        while len(queue.queue) > 0 and len(admitted_children) < class_capacity:
            admitted_children.append(queue.remove_application())
        return admitted_children

class ExamAdmissionAlgorithm:
    def admit_children(self, queue: IQueue, class_capacity: int) -> List[Application]:
        admitted_children = []
        
        exam_scores = [random.randint(0, 100) for _ in range(len(queue.queue))]
        max_score = max(exam_scores)
        threshold = max_score * 0.6 # Minimum grade to enter the class
        
        queue.queue.sort(key=lambda app: app.priority.value, reverse=True)
        
        # Admitting prioritized children
        for application in queue.queue:
            if application.priority != Priority.NONE and exam_scores[queue.queue.index(application)] >= threshold:
                admitted_children.append(application)
        
        # Admitting the rest
        non_priority_children = [app for app in queue.queue if app not in admitted_children]
        non_priority_children.sort(key=lambda app: exam_scores[queue.queue.index(app)], reverse=True)
        admitted_children.extend(non_priority_children[:class_capacity - len(admitted_children)])
        
        return admitted_children

class JSONFileHandler:
    def read_data(self, filename: str) -> List[Application]:
        with open(filename, 'r') as file:
            data = json.load(file)
        applications = []
        for app_data in data:
            child_info = ChildInfo(**app_data['childInfo'])
            parent_info = ParentInfo(**app_data['parentInfo'])
            principal_info = PrincipalInfo(**app_data['principalInfo'])
            application = Application(
                application_id=app_data['application_id'],
                priority=Priority(app_data['priority']),
                principalInfo=principal_info,
                parentInfo=parent_info,
                childInfo=child_info,
                educationForm=app_data['educationForm'],
                supportNeeded=app_data['supportNeeded'],
                date=app_data['date'],
                status=app_data['status']
            )
            applications.append(application)
        return applications

    def save_data(self, filename: str, data: List[Application]):
        serialized_data = []
        for app in data:
            app_dict = app.__dict__
            app_dict['principalInfo'] = app.principalInfo.__dict__
            app_dict['parentInfo'] = app.parentInfo.__dict__
            app_dict['childInfo'] = app.childInfo.__dict__
            serialized_data.append(app_dict)
        with open(filename, 'w') as file:
            json.dump(serialized_data, file, indent=4, cls=PriorityEncoder)

    def add_application(self, application: Application, filename: str):
        applications = self.read_data(filename)
        applications.append(application)
        self.save_data(filename, applications)

    def remove_application(self, application_id: int, filename: str) -> bool:
        applications = self.read_data(filename)
        removed = False
        for app in applications:
            if app.application_id == application_id:
                applications.remove(app)
                removed = True
                break
        if removed:
            self.save_data(filename, applications)
        return removed

class School:
    def __init__(self, num_classes: int, max_capacity_per_class):
        self.classes = [Queue() for _ in range(num_classes)]
        self.max_capacity_per_class = max_capacity_per_class
        self.applications_mapping = {}

    def add_application_to_queue(self, class_index: int, application: Application):
        if 0 <= class_index < len(self.classes):
            self.classes[class_index].add_application(application)
            self.applications_mapping[application.application_id] = class_index
        else:
            raise IndexError("Invalid class index")

    def admit_children_to_classes(self, admitted_children: List[Application]):
        for app in admitted_children:
            class_index = self.applications_mapping.get(app.application_id, -1)
            if class_index != -1:
                self.classes[class_index].add_application(app)
            else:
                raise ValueError(f"Application {app.application_id} not found in application mapping")

    def remove_application_from_queue(self, class_index: int) -> Application:
        if 0 <= class_index < len(self.classes):
            return self.classes[class_index].remove_application()
        else:
            raise IndexError("Invalid class index")

    def get_class_index_for_application(self, application_id: int) -> int:
        return self.applications_mapping.get(application_id, -1)

def print_application_info(application: Application):
    print(
        f"Application ID: {application.application_id}\n"
        f"Priority: {application.priority.name}\n"
        f"Principal Info: {application.principalInfo}\n"
        f"Parent Info: {application.parentInfo}\n"
        f"Child Info: {application.childInfo}\n"
        f"Education Form: {application.educationForm}\n"
        f"Support Needed: {'Yes' if application.supportNeeded else 'No'}\n"
        f"Date: {application.date}\n"
        f"Status: {application.status}\n"
    )

def print_class_info(school: School):
    for class_index, queue in enumerate(school.classes):
        print(f"Class {class_index}:")
        print("-" * 12)
        if len(queue) == 0:
            print("No children in Class.\n")
        else:
            printed_ids = set()
            for application in queue.queue:
                child_info = application.childInfo
                child_id = id(child_info)
                if child_id not in printed_ids:
                    print(f"Name: {child_info['name']} {child_info['surname']}, Birth Date: {child_info['birth_date']}, Address: {child_info['address']}")
                    printed_ids.add(child_id)
            print()

def main():
    school = School(num_classes=3, max_capacity_per_class=25)
    print("School created with 3 classes.\n")

    file_handler = JSONFileHandler()
    
    # Creating a new application and adding it to a file
    new_application = Application(
        application_id=random.randint(10, 1000),
        priority=random.choice(list(Priority)),
        principalInfo=PrincipalInfo(
            name="John",
            surname="Doe",
            phone_number="1234567890",
            email="john.doe@example.com",
            address="123 Main St"
        ),
        parentInfo=ParentInfo(
            name="Jane",
            surname="Doe",
            phone_number="0987654321",
            email="jane.doe@example.com"
        ),
        childInfo=ChildInfo(
            name="Alice",
            surname="Doe",
            birth_date="2010-01-01",
            address="123 Main St"
        ),
        educationForm="Full-time",
        supportNeeded=random.choice([True, False]),
        date="2024-05-04",
        status="pending"
    )
    print("New application created: ")
    print_application_info(new_application)
    file_handler.add_application(new_application, "Lab5/task1/applications.json")
    print("New application added to applications.json.")

    applications = file_handler.read_data("Lab5/task1/applications.json")
    print(f"Read {len(applications)} applications from file.")

    print("\n--- ALL APPLICATIONS ---")
    for app in applications:
        print_application_info(app)

    for app in applications:
        # Adding the application to a queue using the selected distribution method
        random_class_index = random.randint(0, 2)
        school.add_application_to_queue(random_class_index, app)
        print(f"Application ID {app.application_id} added to queue of class {random_class_index}.")

    print("\n--- QUEUES FOR EACH CLASS ---")
    for class_index, queue in enumerate(school.classes):
        print(f"Queue for Class {class_index}: {queue.queue}\n")

    ##################################### ADMISSION DEMONSTRATION #####################################
    admission_algorithms = [FirstKChildrenAdmissionAlgorithm(), ExamAdmissionAlgorithm()]
    print("--- ADMISSION PROCESS ---")
    approved_applications = []
    for class_index, queue in enumerate(school.classes):
        algorithm = admission_algorithms[class_index % len(admission_algorithms)]
        admitted_children = algorithm.admit_children(queue, school.max_capacity_per_class)
        approved_applications.extend(admitted_children)
        school.admit_children_to_classes(admitted_children)
        print(f"Admitted {len(admitted_children)} children to class {class_index}.")

    # Updating status of approved applications
    for app in approved_applications:
        app.status = "approved"
    file_handler.save_data("Lab5/task1/approved_applications.json", approved_applications)
    print("\n--- STATUS UPDATE ---")
    print(f"{len(approved_applications)} approved applications saved to file approved_applications.json.")

    print("\n--- APPROVED APPLICATIONS ---")
    for app in approved_applications:
        print_application_info(app)
    
    print("\n--- CLASS INFORMATION ---")
    print_class_info(school)
    ##################################### ADMISSION DEMONSTRATION #####################################

    ##################################### MERGE DEMONSTRATION #####################################
    # # Merge queues of class 0 and class 1
    # print("Number of applications in Class 0 queue:", len(school.classes[0]))
    # print("Number of applications in Class 1 queue:", len(school.classes[1]))

    # merged_queue = school.classes[0] + school.classes[1]
    # print("\n--- MERGED QUEUE (Class 0 + Class 1) ---")
    # print(merged_queue)
    ##################################### MERGE DEMONSTRATION #####################################

    ##################################### REMOVE DEMONSTRATION #####################################
    # # Removing application from the file
    # removed_application_id = 429
    # removed_application = file_handler.remove_application(removed_application_id, "Lab5/task1/applications.json")
    # if removed_application:
    #     print(f"Application with ID {removed_application_id} removed from applications.json.")
    # else:
    #     print(f"Application with ID {removed_application_id} not found in applications.json.")
    ##################################### REMOVE DEMONSTRATION #####################################

if __name__ == "__main__":
    main()
