# def log_class_calls(func):
#     def wrapper(*args, **kwargs):
#         if kwargs.get('show_logs', False):
#             class_name = args[0].__class__.__name__
#             print(f"Class '{class_name}' called {func.__name__}")
#         return func(*args, **kwargs)
#     return wrapper

def log_class_calls(func):
    def wrapper(*args, **kwargs):
        if kwargs.get('show_logs', False):
            class_name = args[0].__class__.__name__
            print(f"Class '{class_name}' called {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

class LogClassCallsMeta(type):
    def __new__(cls, name, bases, dct):
        for attr_name, attr_value in dct.items():
            if callable(attr_value):
                dct[attr_name] = log_class_calls(attr_value)
        return super().__new__(cls, name, bases, dct)

class MyClass(metaclass=LogClassCallsMeta):
    def method1(self, x, y, show_logs=False):
        return x + y

    def method2(self, a, b, show_logs=False):
        return a * b

my_instance = MyClass()
my_instance.method1(2, 3, show_logs=True)
my_instance.method2(4, 5, show_logs=True)
