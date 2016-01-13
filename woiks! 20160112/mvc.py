#Should this be done on a by-data-field basis, or a by-object basis?  Going with by-object for now.
#Possibly less efficient, but easier to write.
class CrudeObservable:
    def __init__(self):
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callback[func]

    def _docallbacks(self): #needs to call this any time player-visible data is changed.
        for func in self.callbacks:
            func(self) #Yeah, the whole object.
"""
    def set(self, data):
        self.data = data
        self._docallbacks() 

    def get(self):
        return self.data

    def unset(self):
        self.data = None
"""


class Observable:
    def __init__(self, initialValue=None):
        self.data = initialValue
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callback[func]

    def _docallbacks(self): #needs to call this any time player-visible data is changed.
        for func in self.callbacks:
            func(self.data)

    def set(self, data):
        self.data = data
        self._docallbacks() 

    def get(self):
        return self.data

    def unset(self):
        self.data = None

