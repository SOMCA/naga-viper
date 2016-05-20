from abc import ABC, abstractmethod

class PATTERNExport(ABC):
    def __init__(self, filename, format_data):
        super(PATTERNExport, self).__init__()
        self._filename = filename if format_data in filename else ".".join([filename, format_data])

    @staticmethod
    def decor(func):
        def wrapper(*args):
            print(str(args[0]))
            return func(*args)
        return wrapper

    @abstractmethod
    def export_data(self, data):
        return

    def __repr__(self):
        return "%r" % self.__class__.__name__

    def __str__(self):
        return "--- EXPORT TO %s FORMAT: %s! ---" % (repr(self), self._filename)
