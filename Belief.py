import cult
"""Beliefs"""

class Belief:
	def __init__(self, name, prereq_beliefs = [], opposed_beliefs = [], other_check_function = None):
		self.name = name
		self.prereq_beliefs = prereq_beliefs #Other beliefs you need to have first?
		self.opposed_beliefs = opposed_beliefs #List of names, or actual Beliefs?
		self.other_check_function = other_check_function
	
	def isBeliefAvailable(self, cult):
		if self.other_check_function:
			if not self.other_check_function(cult):
				return False
		if self.prereq_beliefs:
			for b in self.prereq_beliefs:
				if b not in cult.doctrines:
					return False
		if self.opposed_beliefs:
			for b in self.opposed_beliefs:
				if b in cult.doctrines:
					return False
		return True
		
#TODO:  Make unit test.