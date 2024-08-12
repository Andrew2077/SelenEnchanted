"""This Module will contain most of the reused MetaClasses that will help in abstracting and creating a better inheritance and instantiation structure for the classes"""


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.

    Example:
        class MyClass(metaclass=SingletonMeta):
            pass

        a = MyClass()
        b = MyClass()
        assert a is b  # This will always be True for classes using SingletonMeta
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
