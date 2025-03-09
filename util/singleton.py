# https://github.com/tiangolo/fastapi/issues/504#issuecomment-586766559
# https://stackoverflow.com/a/6798042/2098800
class Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
