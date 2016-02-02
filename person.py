from misc import *

class Person:
	"""Stats:
	name
	gender?
	rank: enemy, ex, outsider, recruit, outer circle, inner circle, leader.
	fanaticism
	charisma - 0-10.
	sunk_cost
	work ethic
	criminality?
	normality
	stress
	persuasiveness
	family
	wealth
	day job (or none)
	department
	dirt (on the organization)
	age?"""
	RANK_RECRUIT = 'recruit'
	RANK_OUTER_CIRCLE = 'outer'
	RANK_OUTER = 'outer'
	RANK_INNER_CIRCLE = 'inner'
	RANK_INNER = 'inner'
	RANK_LEADER = 'leader'
	
	RANK_OUTSIDER = 'outsider'
	RANK_EX_MEMBER = 'ex'
	RANK_EX = 'ex'
	RANK_ENEMY = 'enemy'
	
	def __init__(self):
		#some random schmuck.
		self.name = "Random Name" + str(random.randint(0,9999999))
		self.gender = random.choice(('m','f'))
		self.charisma = random.choice((0,0,0,1,1,2))
		self.sunk_cost = 0
		#self.loyalty = 0
		self.fanaticism = 0
		#self.stress = 0 # Deprecated - using 'morale' instead.
		self.morale = 50
		self.department = False
		self.dirt = []
		self.credibility = 0
		self.birthday = None
		self.rank = Person.RANK_RECRUIT
		self.age = random.randint(16, 68)
		self.day_job = True
		self.family = "" #for now
		self.wealth = 1000 #dollars
		self.income = 50 #probably too low... Obviously, we should have rich/poor/middleclass people.
		self.money_spent = 0
		self.clout = 1 #Just a random citizen
		self.joined_date = '' #TODO: add what day/month/year they joined the cult.
		self.successes = [] #TODO: Keep track of their successes in each cult section?
		self.skills = {'recruit': 15}
		self.influence = 0

	#Assume everyone has a 10% chance to do any skill....
	def getSkill(self, skill_name, default = 10):
		if self.skills.has_key(skill_name):
			return self.skills[skill_name]
		else:
			return default

	def skillCheck(self, skill_name, difficulty):
		skill_percent = self.getSkill(skill_name)
		if skill_percent:
			return percentCheck(skill_percent, difficulty)
		else:
			return False
			
			
	#If you use a skill, see if you improve it.
	def skillImprovementAttempt(self, skill_name, min_imp = 0, max_imp = 5, difficulty = 'normal'):
		current_skill_percent = self.getSkill(skill_name, 0)
		current_skill_experience = self.getSkill(skill_name + "_months", 0)
		check = False
		if difficulty == 'hard':
			check = not self.skillCheck(skill_name, 'easy')
		elif difficulty == 'easy':
			check = not self.skillCheck(skill_name, 'hard')
		elif difficulty == 'auto': 
			check = True
		else: #difficulty == 'normal':
			check = not self.skillCheck(skill_name, 'normal')
		if check:
			new_skill_percent = min(current_skill_percent + random.randint(min_imp, max_imp), 99)
			self.skills[skill_name] = new_skill_percent
		#self.skills[skill_name + "_months"] = current_skill_experience + 1 #Add one month.
	
	def setSunkCost(self, val):
		self.sunk_cost = max(0, min(val, 99))
	
	def sunkCostIncreaseAttempt(self, min_imp = 1, max_imp = 4, difficulty = 'normal'):
		current_sunk_cost = self.sunk_cost
		check = failPercentCheck(current_sunk_cost, difficulty)
		if check:
			self.setSunkCost(current_sunk_cost + random.randint(min_imp, max_imp))
	
	def setFanaticism(self, val):
		self.fanaticism = max(0, min(val, 99))
		
	def fanaticismIncreaseAttempt(self, min_imp = 1, max_imp = 4, difficulty = 'normal'):
		current_fanaticism = self.fanaticism
		check = failPercentCheck(current_fanaticism, difficulty)
		if check:
			self.setFanaticism(current_fanaticism + random.randint(min_imp, max_imp))
	
	def setMorale(self, val):
		self.morale = max(0, min(val, 99))
		
	#Can be used to increase or decrease morale...
	def adjustMorale(self, min_imp, max_imp):
		self.setMorale(self.morale + random.randint(min_imp, max_imp))
		
	"""when a person leaves the cult (voluntarily or not), they make all the people they have influence with unhappier. People who become enemies actually KEEP spreading discontent, unless the cult has Disconnection as a rule."""
	def spreadDiscontent(self,cult):
		damage = 10
		if self.rank == Person.RANK_ENEMY: #If they're mad at the cult, it's worse.
			damage += 10
		#TODO: They do a lot more damage if they have dirt on the cult (that they dare spread)
		for ii in range(self.influence):
			member = random.choice(cult.membership)
			member.adjustMorale(-damage, 0) #Negative numbers - lowest first in the range.
		self.influence = self.influence/2 #Diminishes fairly quickly once they're out?