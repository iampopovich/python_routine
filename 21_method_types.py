class toyClass:
    def __init__(self, name):
        self.name = None

    def instance_method(self):
        return 'instance method called', self

    @classmethod
    def class_method(cls):
        return 'class method called', cls

    @staticmethod
    def static_method():
        return 'static method called'


toy = toyClass('heher')

print(toy.instance_method())
print(toyClass.class_method())
print(toyClass.static_method())
