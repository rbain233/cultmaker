import cult
"""Beliefs"""

class Belief:
	def __init__(self, internal_name, name, desc, prereq_beliefs = [], opposed_beliefs = [], other_check_function = None):
		self.name = name
		self.internal_name = internal_name
		self.desc = desc
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
	
	#What sorts of effects can beliefs have?
	#Cause tests of faith.
	#Increase/decrease authoritiarianism, criminality, violence?
	#Increase/decrease government/media attention?
	#make reputation better/worse?
	#Make it easier to sell crapola to cultists/public?

class BeliefMasterList:
	#Singleton?  Bleh, trying to do them in Python looks to be a pain.
	def __init__(self):
		self.list = {}
		
	def addBelief(self, b):
		self.list[b.internal_name] = b

	def getBelief(self, name):
		if name in self.list:
			return self.list[name]
		else:
			return None

belief_master_list = BeliefMasterList()
#Now, load it with beliefs....

#TODO:  Make unit test.
if __name__ == "__main__":
	