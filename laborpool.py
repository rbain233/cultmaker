from misc import *
from mvc import *
from person import Person

class LaborPool(CrudeObservable): #Standard labor pool, with no 'use'.
	def __init__(self, name = "labor_pool", short_name = "Generic Labor Pool", desc = "A Labor Pool", f = False, min_rank = Person.RANK_RECRUIT, cost_per_person = 0):
		CrudeObservable.__init__(self)
		self.people = []
		self.permanency = True 
		self.name = name
		self.short_name = short_name
		self.desc = desc
		self.monthly_function = f #Set to make the pool do something every month.
		self.max_people = -1 #If it's non-negative, it's the actual max.
		self.minimum_rank = min_rank
		self.cost_per_person = cost_per_person
	
	#Rank is the rank we're ASKING for.
	def rankOK(self, rank):
		if self.minimum_rank == Person.RANK_RECRUIT:
			return True
		if self.minimum_rank == Person.RANK_OUTER_CIRCLE:
			return rank in (Person.RANK_OUTER_CIRCLE, Person.RANK_INNER_CIRCLE, Person.RANK_LEADER)
		if self.minimum_rank == Person.RANK_INNER_CIRCLE:
			return rank in (Person.RANK_INNER_CIRCLE, Person.RANK_LEADER)
		if self.minimum_rank == Person.RANK_LEADER:
			return rank == Person.RANK_LEADER
			
	def getName(self):
		return self.name
		
	def removePerson(self, person):
		if person in self.people:
			self.people.remove(person)
			person.department = False
		self._docallbacks()

	def addPerson(self, person):
		if self.getMaxPeople() >= 0 and len(self.people) >= self.getMaxPeople():
			return #Don't add more.
		#TODO: This should return some sort of error or message....
		self.people.append(person)
		person.department = self #A person should only be in one labor pool at a time....
		self._docallbacks()
		
	def doMonthlyFunction(self, cult):
		if self.monthly_function:
			ret = self.monthly_function(self, cult)
		else:
			ret = ""
		if not self.permanency:
			self.disband() #Month's up, we're done here.
		return ret
		#cult will houseclean away 'deleted' pools every month.
	
	def calculateMonthlyExpenses(self):  #TODO: Have this get called by the financial stuff.
		return self.cost_per_person * len(self.people)
	
	def disband(self):
		for person in self.people:
			self.removePerson(person)
		self.permanency = False
		self.name = "deleted"
		self.monthly_function = False

	def setPermanence(self, perm):
		self.permanency = perm

	def setMaxPeople(self, m):
		#Better yet, let the player manually remove/add people.
		if (m == 0):
			for person in self.people:
				self.removePerson(person)
			self.max_people = 0	
		elif (m < 0):
			self.max_people = -1
		else:
			self.max_people = m
			if len(self.people) > m:
				too_many = len(self.people) - m
				for p in self.people[1..too_many]:
					self.removePerson(p)
	
	def getMaxPeople(self): #some pools might override this.
		return self.max_people
		
	def getPeopleList(self, rank = False):
		ret = []
		if type(rank).__name__ == 'str':
			rank = [rank]
		if type(rank).__name__ in ('tuple', 'list'):
			for person in self.people:
				if person.rank in rank:
					ret.append(person)
			return ret
		else:
			return self.people
		
	def getIsActive(self):
		#TODO: Check what minimum rank this needs, see if any are in the cult.
		#Check this at start of month.
		#If it can't be active, for whatever reason, de-assign people working on it.
		return True