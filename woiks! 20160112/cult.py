import random
from person import Person
from laborpool import LaborPool
from misc import *
import math
from merch import *
from mvc import *

class Doctrine:
	def __init__(self, name, popularity_mod = 0):
		self.name = name
		self.popularity_mod = popularity_mod
	

doctrine_list = [
	Doctrine("Christian", 10),
	Doctrine("Magjickk",0),
	Doctrine("New Age",5),
	Doctrine("Pagan",0),
	Doctrine("Political", 0),
	Doctrine("Satanism", -10),
	Doctrine("Self-Help", 10),
	Doctrine("UFO", 0)
	#add more as needed.
]

def streetPreaching(self, cult):
	if not self.people:
		return #nobody doing this....
	msg = "Street Preaching.\n"
	recruit_count = 0
	for cultist in self.people:
		recruit_chance = cultist.getSkill("recruit")
		fanaticism_bonus = 0
		"""if they've heard of the cult"""
		if (cult.popularity > 20):
			"""If it has a good rep"""
			recruit_chance += 5
		if (cult.popularity > 50):
			"""If it has a GREAT rep"""
			recruit_chance += 10
		if (cult.popularity < -10):
			"""If it has a BAD rep"""
			recruit_chance -= 10
			fanaticism_bonus = 5
		if (cult.popularity < -50):
			"""If the cult is LOATHED"""
			recruit_chance -= 10
			fanaticism_bonus = 10
		#TODO: Add in things like dogma,etc.
		audience_size_min = 10
		audience_size_max = 40
		#Use up the good propaganda first.
		propaganda = ""
		if cult.getSupplies("pamphlet_slick") > 0:
			cult.setSupplies("pamphlet_slick", cult.getSupplies("pamphlet_slick") - 1) #Use up 100 of them...
			audience_size_min *= 3
			audience_size_max *= 3
			propaganda = " passed out slick pamphlets and"
		elif cult.getSupplies("pamphlet_crude") > 0:
			cult.setSupplies("pamphlet_crude", cult.getSupplies("pamphlet_crude") - 1) #Use up 100 of them...
			audience_size_min *= 2
			audience_size_max *= 2
			propaganda = " passed out crude pamphlets and"
		recruit_chance = int(math.sqrt(recruit_chance / 2))
		audience = random.randint(audience_size_min, audience_size_max) 
		new_recruits = cult.proselytize(recruit_chance, audience, fanaticism_bonus)
		msg += "%s%s recruited %d people.\n" % (cultist.name, propaganda, len(new_recruits))  
		cult.membership += new_recruits
		cultist.skillImprovementAttempt("recruit")
		cultist.skillImprovementAttempt("recruit_months", 1, 1, 'auto')
		cultist.sunkCostIncreaseAttempt(1,6) 
		if len(new_recruits) == 0:
			cultist.adjustMorale(-3, 1)
		else:
			cultist.adjustMorale(0, len(new_recruits) * 2)
	return msg

#This one shouldn't even show up if there's no recruits.
#TODO: Possibility of wiseass students who raise stress and/or quit.
#TODO: Ways to vary what they're getting - moral/doctrine/fanaticism...
def indoctrinatingRecruits(self, cult):
	if not self.people:
		return
	msg = "Indoctrinating recruits:\n"
	students = cult.getRecruits()
	if not students:
		#Error - shouldn't be able to educate none students.
		print "Can't try to educate NO students."
		return
	lessons_counter = {}
	for teacher in self.people:
		#How many people can they teach? 1-4 at first, I'll say.
		for ii in range(0, random.randint(1, 4)):
			student = random.choice(students)
			if not lessons_counter.has_key(student):
				lessons_counter[student] = 0
			elif lessons_counter[student] > 3:
				continue #Saturation - they can't learn more this month.
			else:
				#Increase students' fantaticism, morale, sunk_cost, and doctrine skill.
				student.fanaticismIncreaseAttempt(1,6)
				student.sunkCostIncreaseAttempt()
				student.skillImprovementAttempt('doctrine', 0, 10)
				student.adjustMorale(-1, 5)
				lessons_counter[student] += 1
				#DEBUG: print "%s fanaticism: %d. Doctrine: %d.\n" % (student.name, student.fanaticism, student.getSkill('doctrine'))
				#Increase teacher's teaching skill(?) and sunk_cost.
				teacher.sunkCostIncreaseAttempt()
				teacher.skillImprovementAttempt('teaching_months', 1, 1, 'auto')
				teacher.skillImprovementAttempt('doctrine', 1, 2, 'hard')
		msg += "%s indoctrinated %d recruits.\n" % (teacher.name, ii)
	return msg

def writeScripture(self, cult):
	if not self.people:
		return #nobody doing this....
	cult.dogma += 10
	msg = "You set down to write some doctrine for your cult.\n"
	msg += "Your cult now has enough Holy Writ to produce:\n"
	if cult.dogma > 10:
		msg += "introductory pamphlets\n"
	if cult.dogma > 20:
		msg += "a website\n"
		msg += "radio and TV ads\n"
		msg += "magazine ads\n"
	if cult.dogma > 40:
		msg += "a book\n"
		msg += "a movie\n"
	if cult.dogma > 60:
		msg += "a regular radio or TV program\n"
		msg += "a series of books\n"
	return msg
	
labor_pool_street_preaching = LaborPool("Recruiting: Street Preaching", streetPreaching, Person.RANK_OUTER_CIRCLE, 5)
labor_pool_indoctrinating_recruits = LaborPool("Indoctrinating Recruits", indoctrinatingRecruits, Person.RANK_OUTER_CIRCLE, 5) #Gotta be at least outer circle to do this...
labor_pool_write_scripture = LaborPool("Write Scripture", writeScripture, Person.RANK_LEADER, 0) 
	
class Cult(CrudeObservable):
	"""Stats:
	name
	secrecy
	weirdness
	clout
	wealth
	size
	reputation
		fame and popularity are two separate fields
		fame is what %age has heard of the cult,
		popularity is what % of those _like_ it. (If negative, you're actively hated, mostly.)
		
	authoritarianness
	members
	also needs a way to keep track of doctrine, if it affects cult structure"""
	def __init__(self):
		CrudeObservable.__init__(self)
		self.name = "cult"
		self.membership = []
		self.ex_members = []
		self.departments = {"Street Preaching": labor_pool_street_preaching, 
							'Meditating': LaborPool("Transcendental Medication"),
							"Indoctrinating Recruits": labor_pool_indoctrinating_recruits,
							"Write Scripture": labor_pool_write_scripture} 
		self.fame = 0
		self.popularity = 0
		self.funds = 1000 #starting money
		self.doctrines = [] #no starting doctrines?
		self.authoritarianism = 0
		self.recruit_base_morale_min = 40 #need ways to avoid this...
		self.recruit_base_morale_max = 80 #need ways to avoid this...
		self.dogma = 10
		self.supplies = {} #Pamphlets, books and so on.
	
	def proselytize(self, recruit_percent, audience, fanaticism_bonus):
		#I looked up the spelling.
		new_recruits = []
		
		for ii in range(audience):
			if (random.randint(0, 100) <= recruit_percent):
				recruit = Person()
				recruit.fanaticism = fanaticism_bonus
				recruit.morale = random.randint(self.recruit_base_morale_min, self.recruit_base_morale_max)
				new_recruits.append(recruit)
		return new_recruits

	#return a word instead of a number for the 'fame' stat		
	def getFameTitle(self):
		if (self.fame <= 10):
			return "unknown"
		elif (self.fame <= 30):
			return "obscure"
		elif (self.fame <= 50):
			return "minor"
		elif (self.fame <= 75):
			return "major"
		elif (self.fame <= 90):
			return "famous"
		else:
			return "world famous"

	def getPopularityTitle(self):
		if (self.popularity <= -50):
			return "loathed"
		elif (self.popularity <= -25):
			return "hated"
		elif (self.popularity <= -10):
			return "disliked"
		elif (self.popularity <= 15):
			return "tolerated"
		elif (self.popularity <= 25):
			return "liked"
		elif (self.popularity <= 50):
			return "admired"
		elif (self.popularity <= 75):
			return "loved"
		else:
			return "exalted"

	def reportStatus(self):  #NOT CURRENTLY IN USE
		"""Monthly report on cult status.  Return a big string of results?"""
		status = "Membership: %d\n" % len(self.membership)
		status += "The %s is %s" \
				  % (self.name, self.getFameTitle())
		if (self.fame > 10):
			status += " and is %s by those who know of it.\n" % cult.getPopularityTitle()
		else:
			status +=".\n"
		return status
	
	def membershipMonthlyChecks(self):
		msg = ""
		msg += self.loyaltyChecks()
		msg += self.promoteOuterCheck()
		msg += self.promoteRecruitsCheck()
		msg += self.internalSocialStuff()
		msg += self.fundRaising()
		msg += "cult membership:\n"
		m = self.getRecruits()
		if m:
			msg += "%d recruits.\n" % len(m)
		m = self.getOuterCircle()
		if m:
			msg += "%d Outer Circle members.\n" % len(m)
		m = self.getInnerCircle()
		if m:
			msg += "%d Inner Circle members.\n" % len(m)
		msg += "1 leader, %s." % self.leader.name
		return msg
	
	def finances(self):
		msg = "Financial report:\n"
		if self.funds < 0:
			msg += "The cult's debts are mounting!\n"
			self.funds = int(self.funds * 1.05) # 5% interest should be extortionate enough....
		#TODO: Get more financial info each month, archive it.
		for pool_name in self.departments:
			c = self.departments[pool_name].calculateMonthlyExpenses()
			msg += "%s:\t%d\n" % (self.departments[pool_name].name, c)
			self.funds -= c
		msg += "cult treasury: %d.\n" % self.funds
		if self.funds < 0:
			msg += "The cult needs money!\n"
		return msg
		
	def loyaltyChecks(self):
		msg = ""
		loyal_members = []
		quit_count = 0
		enemy_count = 0
		for cultist in self.membership:
			quitter = False
			if cultist.rank == Person.RANK_LEADER or percentCheckEasy(cultist.morale) or percentCheck(cultist.sunk_cost) or percentCheck(cultist.fanaticism):
				loyal_members.append(cultist)
				if not percentCheck(cultist.sunk_cost):
					cultist.sunk_cost += random.randint(1,4) #Sinking more...
			else:
				cultist.rank = Person.RANK_EX
				quit_count += 1
				self.ex_members.append(cultist)
				#TODO: If the cult's turned murderous, now's the chance to kill them before they escape...
				#TODO: If their fanaticism + ambition? is high enough, they may schism!
				#Check to see if quitter because an enemy
				#Now all the things that kept them in go against them...
				if percentCheck(cultist.sunk_cost):
					cultist.morale -= random.randint(1,cultist.sunk_cost)
				if percentCheck(cultist.fanaticism):
					cultist.morale -= random.randint(1,cultist.fanaticism)
				#TODO: If they know any dirt, that can also make them worse.
				if (cultist.morale < 0):
					cultist.rank = Person.RANK_ENEMY
					self.enemies.append(cultist)
					enemy_count += 1
				#if someone quit/gets busted/whatever, they have a bad influence on all the other cultists
				cultist.spreadDiscontent(self)
		self.membership = loyal_members
		if quit_count == 0:
			pass
		elif quit_count == 1:
			msg += "1 member has quit.\n"
		else:
			msg += "%d members have quit.\n" % (quit_count)
			
		if enemy_count == 0:
			pass
		elif enemy_count == 1:
			msg += "1 member is now an enemy of %s!\n" % (self.name)
		else:
			msg += "%d members are now enemies of %s!\n" % (enemy_count, self.name)
			
		return msg  #End of loyaltyCheck()
		
	def promoteRecruitsCheck(self):
		msg = ""
		promotion_count = 0
		for cultist in self.membership:
			if cultist.rank == Person.RANK_RECRUIT and cultist.skillCheck('doctrine', 'easy'):  #TODO: Different possible advancement priorities.
				cultist.rank = Person.RANK_OUTER_CIRCLE
				promotion_count += 1
				if cultist.department:
					self.removeLabor(self, cultist.department, [cultist])
		if promotion_count == 1:
			return "1 recruit has advanced to the Outer Circle!\n"
		if promotion_count > 1:
			return str(promotion_count) + " recruits have advanced to the Outer Circle!\n"
		return msg

	def promoteOuterCheck(self):
		msg = ""
		promotion_count = 0
		for cultist in self.membership:
			if cultist.rank == Person.RANK_OUTER_CIRCLE and cultist.skillCheck('doctrine', 'hard'):  #TODO: Different possible advancement priorities.
				cultist.rank = Person.RANK_INNER_CIRCLE
				promotion_count += 1
				if cultist.department:
					self.removeLabor(self, cultist.department, [cultist])
		if promotion_count == 1:
			return "1 Outer Circle member has advanced to the Inner Circle!\n"
		if promotion_count > 1:
			return str(promotion_count) + " Outer Circle members have advanced to the Inner Circle!\n"
		return msg
	
	def internalSocialStuff(self):
		for cultist in self.membership:
			#Cultists influence each other.
			if cultist.rank == Person.RANK_RECRUIT:
				cultist.influence += random.randint(0,1)
			if cultist.rank == Person.RANK_OUTER_CIRCLE:
				cultist.influence += random.randint(0,3)
			if cultist.rank == Person.RANK_INNER_CIRCLE:
				cultist.influence += random.randint(1, 6)
		return "Social stuff goes here.\n"
	
	def fundRaising(self):
		msg = ""
		total_donations = 0
		for cultist in self.membership:
			if cultist.day_job:
				cultist.wealth += cultist.income #They get mo' money every month... if they have jobs.
			if cultist.rank == Person.RANK_LEADER:
				msg += "You made %d from your day job.\n" % (cultist.income)
				continue #You have to decide what to do with money as leader.
			#Check if they will donate any money.
			#TODO: Mandatory tithing/high-pressure donations?
			#TODO: Buying paraphernalia.
			percent = 0
			individual_donation = 0.0
			while percentCheck(cultist.fanaticism) and percent <= 100:
				percent += 1.0
			individual_donation = int(cultist.wealth * (percent/ 100.0))
			if (individual_donation > 0):
				if individual_donation > 100:
					#TODO: There should be some sort of adjustable threshold for these that goes up as the cult gains $$$ and members.
					msg += "%s donated %d to the cult!\n" % (cultist.name, individual_donation)
				cultist.wealth -= individual_donation
				cultist.money_spent += individual_donation
				self.funds += individual_donation
				total_donations += individual_donation
				cultist.sunkCostIncreaseAttempt(1, percent)
			#Trivial: 1% of their money.
			#significant: 5% of their money.
			#major: 25% of their money.
			#crazy: ALL the money. ALL OF IT.
		if (total_donations > 0):
			msg += "A total of %d in donations this month.\n" % total_donations
		msg += "The cult has a total of $%d.\n" % self.funds
		return msg
	
	def getRecruits(self):
		ret = []
		for cultist in self.membership:
			if cultist.rank == Person.RANK_RECRUIT:
				ret.append(cultist)
		return ret

	def getOuterCircle(self):
		ret = []
		for cultist in self.membership:
			if cultist.rank == Person.RANK_OUTER_CIRCLE:
				ret.append(cultist)
		return ret

	def getInnerCircle(self):
		ret = []
		for cultist in self.membership:
			if cultist.rank == Person.RANK_INNER_CIRCLE:
				ret.append(cultist)
		return ret

	def getLeader(self):  #should just be the one leader...
		ret = []
		for cultist in self.membership:
			if cultist.rank == Person.RANK_LEADER:
				ret.append(cultist)
		return ret
	
	def getUnassignedLaborByRank(self, rank):
		ret = []
		for cultist in self.membership:
			if cultist.rank == rank and cultist.department == False:
				ret.append(cultist)
		return ret
		
	def getUnassignedLabor(self, min_rank_required = Person.RANK_RECRUIT):
		labor = []
		if min_rank_required == Person.RANK_RECRUIT:
			tmp = self.getRecruits()
			for cultist in tmp:
				if cultist.department == "":
					labor.append(cultist)
		if min_rank_required in (Person.RANK_RECRUIT, Person.RANK_OUTER_CIRCLE):
			tmp = self.getOuterCircle()
			for cultist in tmp:
				if cultist.department == "":
					labor.append(cultist)
		if min_rank_required in (Person.RANK_RECRUIT, Person.RANK_OUTER_CIRCLE, Person.RANK_INNER_CIRCLE):
			tmp = self.getInnerCircle()
			for cultist in tmp:
				if cultist.department == "":
					labor.append(cultist)
		return labor
					
	def assignLabor(self, department, cultists):
		#TODO: add permanency, monthly function?
		if not self.departments.has_key(department): #new one.
			d = LaborPool()
			d.name = department
			self.departments[department] = d 
		d = self.departments[department]
		for c in cultists:
			if c.department: #Make sure they're not in two departments at once.
				c.department.removePerson(c) 
			d.addPerson(c)
		self._docallbacks()
		return d #So the user can set the laborpool's attributes, if need be.

	def removeLabor(self, department, cultists):
		if self.departments.has_key(department):
			d = self.departments[department]
			for c in cultists:
				d.removePerson(c)
			self._docallbacks()

	def disbandLabor(self, department):
		if self.departments.has_key(department):
			self.departments[department].disband()
		self._docallbacks()


	def setupDepartmentsInit(self):
		"""Set up cult departments at run-time. Some may not be in use."""
		department_list = ["recruiting", "welcome", "print_propaganda",
						   "panhandling", "praying", "pr",
						   "thought_police", "black_ops"]
		for department_name in department_list:
			self.departments[department_name] = LaborPool(department_name)
	
	def getJobs(self, rank):
		job_list = []
		for department_name in self.departments:
			dept = self.departments[department_name]
			if dept.rankOK(rank):
				if dept.max_people == 'unlimited' or len(dept.people) < dept.max_people:
					job_list.append((department_name, dept.name))
				else:
					job_list.append(("full", department_name))
		job_list.append(("done", "Done"))
		return job_list
		
	def doJobs(self):
		msg = ""
		for department_name in self.departments:
			dept = self.departments[department_name]
			scr = dept.doMonthlyFunction(self)
			if scr:
				msg += scr
		return msg
	
	def getActionList(self):
		action_list = [("review_doctrines", "Review cult doctrines"),
						("review_membership", "Review cult membership"),
						("review_finances", "Review cult finances"),
						("buy_stuff", "Purchase goods"),
						("assign_leader", "Leader activities")]
		#cultist actions
		if (len(self.membership) > 1):
			action_list.append(("assign_cultists", "Assign cultists"))
		action_list.append(("done", "Begin month"))
		return action_list
	
	def getSupplies(self, merch_name):
		if self.supplies.has_key(merch_name):
			return self.supplies[merch_name]
		else:
			return 0
	
	def setSupplies(self, merch_name, qty):
		self.supplies[merch_name] = qty

#Having outer circle members allows:
#Orientation/Welcome/Indoctrination
#Fundraising/panhandling
#Recruiting (that's not by the leader)
#Producing propaganda

"""Assets for the cult to own:
Storefront church
Website (amateur)
Website (Professional)
Wilderness retreat
communal farm
radio station
city lodge building
Newspaper/Magazine/Book printing company
"""

"""Edicts: Things like vegetarianism, free love, tithing, scary initiation rites, and so on.
Can be applies to specific ranks in the group.
When a new member becomes elegible for these, they need to make a Test of Faith.
It can scare them away, or keep them from getting promoted if they fail."""

class Edict:
	def __init__(self, name, applies_to, effect_on, test):
		#(I could use 'isinstance' if it would be clearer.)
		if type(applies_to).__name__ == "function":
			self.applies_to_function = applies_to
			self.applicable_ranks = []
		elif type(applies_to).__name__ in ('tuple', 'list'):
			self.applies_to_function = self.defaultAppliesCheck
			self.applicable_ranks = applies_to
		if effect_on:
			self.effect_on = effect_on
		else:
			self.effect_on = self.defaultEffect
		if test:
			self.test = test
		else:
			self.test = self.defaultTestOfFaith
	
	"""Need a way to standardize these tests"""
	def checkIfApplies(self, cultist):
		if self.applies_to_function:
			return self.applies_to_function(cultist)
		else:
			return False
	
	"""Reason is either 'promotion' or 'new_edict'?"""
	def effectEdictOnCultist(self, cultist, reason):
		if self.effect_on:
			self.effect_on(cultist, reason, self.testFaith(cultist))
			
	def testFaith(self, cultist):
		if self.test:
			return self.test(cultist)
		else:
			return False

	"""Check if they go for it, and if so, how well..."""
	def defaultTestOfFaith(self, cultist):
		return (percentCheck(cultist.fanaticism), percentCheck(cultist.morale), percentCheck(cultist.sunk_cost))

	def defaultEffect(self, cultist, reason, test_results):
		if test_results[0]:
			#they passed with fanaticism. +sunk_cost, +fanaticism.
			cultist.sunkCostIncreaseAttempt(1, 4)
			cultist.fanaticismIncreaseAttempt(1, 4)
			return True
		elif test_results[1]:
			#they passed with happiness. +sunk_cost, +fanaticism.
			cultist.sunkCostIncreaseAttempt(1, 4)
			cultist.fanaticismIncreaseAttempt(1, 4)
			return True
		elif test_results[2]:
			#they passed with just sunk_cost. -morale, +sunk_cost.
			cultist.sunkCostIncreaseAttempt(1, 4)
			cultist.adjustMorale(-20, -1)
			return True
		else:
			#they failed altogether.  Major morale hit, may quit.
			cultist.adjustMorale(-100, -50)
			cultist.fanaticism = cultist.fanaticism / 2
			cultist.sunk_cost / 2
			#TODO: add a 'may quit' check right here, or let it ride 'til the next month?
			return False
			
	def defaultAppliesCheck(self, cultist):
		return (cultist.rank in self.applicable_ranks)
			