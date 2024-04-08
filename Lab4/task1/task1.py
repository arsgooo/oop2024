# Метаклас, який перевіряє, чи є створюваний клас класом-колекцією

class CollectionMeta(type):
    def __new__(cls, name, bases, attrs_dict):
        required_methods = ('__len__', '__getitem__', '__iter__')
        if all(hasattr(attrs_dict.get(method_name), '__call__') for method_name in required_methods):
            return super().__new__(cls, name, bases, attrs_dict)
        else:
            raise TypeError(f"Class '{name}' must have {', '.join(required_methods)} methods to be a collection class.")
    
class CollectionClass(metaclass=CollectionMeta):
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __iter__(self):
        return iter(self.items)

try:
    class NotCollectionClass(metaclass=CollectionMeta):
        def __init__(self, number):
            self.number = number
except TypeError as e:
    print(e)


# Checkup
collection = CollectionClass([13, 36, 22, 158, 79])
print("The length of collection is:", len(collection))
print("The third element of collection is:", collection[2])

print("All elements of collection: ")
for element in collection:
    print(element)
