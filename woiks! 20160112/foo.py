class Foo:
    def __init__(self, x):
		self.x = x    
    def bar(self):
        pass
    def __str__(self):
        return "Just a new class! x = " + str(self.x)
#Just to show this works....

f = Foo(23)
print f
