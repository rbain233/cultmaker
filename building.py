from person import * 
from cult import * 
from laborpool import * 

"""Buildings will probably have to be nonstandardized, as they do all sorts of things.
Things they have in common:
they have labor pools of up to X people
They have a cost to buy.
They cost rent to run.
They have 'infrastructure' - a labor pool that needs people assigned to it, or it has a bad effect on morale."""

class GenericBuilding:
	def __init__(self, name, price, rent, labor_pools):
		self.name = name
		self.price = price
		self.rent = rent
		self.labor_pools = labor_pools #{'name': LP,...}
		for pool_name in self.labor_pools:
			self.labor_pools[pool_name].building_backpointer = self
		"""I think this should work, and it gives the building's labor-pools a way to access each other as needed."""
		self.monthly_expenses = 0 #Non-rent cost from users.
	
	def monthlyCheck(self, cult):
		ret = ""
		self.monthly_expenses = 0
		#do infrastructure first.
		ret += self.labor_pools['infrastructure'].doMonthlyFunction(cult)
		for pool_name in self.labor_pools:
			self.monthly_expenses += self.labor_pools[pool_name].calculateMonthlyExpenses()
			if pool_name != 'infrastructure':
				ret += self.labor_pools[pool_name].doMonthlyFunction(cult)
		#TODO: pay rent in 'finance'?
		return ret
		
class BuildingLaborPool(LaborPool):
	def __init__(self, building, name = "labor_pool", f = False, min_rank = Person.RANK_RECRUIT, cost_per_person):
		LaborPool.__init__(name, f, min_rank, cost_per_person)
		self.building_backpointer = building
		self.cost_per_person = cost_per_person
		

class TypicalInfrastructurePool(BuildingLaborPool):
	def __init__(self, building, name = "labor_pool", f = False, min_rank = Person.RANK_RECRUIT, people_needed = 0, cost_per_person = 0):
		BuildingLaborPool.__init__(name, f, min_rank, cost_per_person)
		self.setPeopleNeeded(people_needed)
	
	def setPeopleNeeded(self, n):
		self.people_needed = n
		
	def doMonthlyFunction(self, cult):
		msg = ""
		
		if self.people_needed > count(self.people): #Check if this has enough people.
			#If not, it may cause bad morale among people at this building.
			shortfall = self.people_needed - count(self.people)
			msg = "%s needs more people working on its infrastructure.\n" % self.building_backpointer.name
			people_in_building = []
			for pool_name in self.building_backpointer.labor_pools:
				people_in_building += self.building_backpointer.labor_pools[pool_name].people
			for cultist in people_in_building:
				max_annoyance = min(cultist.morale / 2, shortfall) #Shouldn't be annoying enough to make people quit by itself.
				cultist.adjustMorale(-max_annoyance, 0)
		#Infrastucture work is boring.
		for cultist in self.people:
			cultist.adjust_morale(-3, 0)
			cultist.sunkCostIncreaseAttempt(1,6)
		return msg