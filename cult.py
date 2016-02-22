import random
from person import Person
from laborpool import LaborPool
from misc import *
import math
from merch import *
from mvc import *
import datetime

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
	cult._docallbacks()
	return msg
	
labor_pool_street_preaching = LaborPool("street_preaching", "Recruiting: Street Preaching", "Standing around in public hollering at the crowds.", streetPreaching, Person.RANK_OUTER_CIRCLE, 5)
labor_pool_indoctrinating_recruits = LaborPool("indoctrination","Indoctrinating Recruits", "Teaching new members the cult's doctrines.", indoctrinatingRecruits, Person.RANK_OUTER_CIRCLE, 5) #Gotta be at least outer circle to do this...
labor_pool_write_scripture = LaborPool("scripture", "Write Scripture", "Elaborating upon the cult's dogma.", writeScripture, Person.RANK_LEADER, 0) 
	
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
		self.short_name = "cult"
		self.members_name = "cult"
		self.founding_date = None
		self.date = None
		self.membership = []
		self.ex_members = []
		self.enemies = []
		self.departments = {}
		self.addLaborPool(labor_pool_street_preaching) 
		self.addLaborPool(LaborPool("meditation","Transcendental Medication", "Sitting around doing nothing."))
		self.addLaborPool(labor_pool_indoctrinating_recruits)
		max = LaborPool("10max", "10 Max", "Only 10 people at a time.")
		max.setMaxPeople(10)
		self.addLaborPool(max)
		self.addLaborPool(labor_pool_write_scripture)
		self.fame = 0
		self.max_fame = 0
		self.popularity = 0
		self.funds = 1000 #starting money
		self.doctrines = [] #no starting doctrines?
		self.authoritarianism = 0
		self.recruit_base_morale_min = 40 #need ways to avoid this...
		self.recruit_base_morale_max = 80 #need ways to avoid this...
		self.dogma = 10
		self.supplies = {} #Pamphlets, books and so on.
		self.last_month_fame = 0
		self.last_month_popularity = 0
		self.last_month_funds = 0
		self.last_month_morale = 0
		self.financial_log = {datetime.date(1998,4,1): (("starting funds", 999, 0), ("people buying crap", 1, 0),("End of month total", 1000,0))} #Date: (tuple of (name, gain, loss))? Should work....
		self.last_month_membership_count = 1
		self.shopping_list = {}
	
	def doMonth(self, date):
		self.date = date
		if self.fame > self.max_fame:
			self.max_fame = self.fame
		self.last_month_fame = self.fame
		self.last_month_popularity = self.popularity
		self.last_month_funds = self.funds
		self.last_month_membership_count = len(self.membership)
		self.last_month_morale = self.calculateAverageMorale() #(deliberately inaccurate)
		
		msg = ""
		msg += self.buyStuff()
		msg += self.doJobs()
		msg += self.publicity()
		msg += self.monthlyPassiveRecruitment() #Should these be in a different order?
		msg += self.loyaltyChecks()
		msg += self.promoteOuterCheck()
		msg += self.promoteRecruitsCheck()
		msg += self.internalSocialStuff()
		msg += self.fundRaising()
		
		msg +=  self.finances()
		self._docallbacks()
		for pool_name in self.departments:
			self.departments[pool_name]._docallbacks() #Update them all.
			
		return msg
	
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

	def buyStuff(self):
		#buy all the items specified.
		ret = "" #debug
		for m in self.shopping_list:
			qty = self.shopping_list[m]
			cost = qty * m.unit_cost
			self.funds -= cost
			if not self.supplies.has_key(m.internal_name):
				self.supplies[m.internal_name] = qty
			else:
				self.supplies[m.internal_name] += qty 
			ret += " buying %d of %s for %d.\n" % (qty, m.internal_name, cost)
		return ""

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
			status += " and is %s by those who know of it.\n" % self.getPopularityTitle()
		else:
			status +=".\n"
		return status
	
	
	def finances(self):
		temp_log = []
		#TODO: Log all costs and gains per pool, expenditure, etc for the month.
		msg = "Financial report:\n"
		temp_log.append(("Cult treasury, start of month:", self.funds, 0))
		if self.funds < 0:
			msg += "The cult's debts are mounting!\n"
			self.funds = int(self.funds * 1.05) # 5% interest should be extortionate enough....
		#TODO: Get more financial info each month, archive it.
		for pool_name in self.departments:
			c = self.departments[pool_name].getLoss()
			d = self.departments[pool_name].getGain()
			temp_log.append((self.departments[pool_name].name, d, c))
			msg += "%s:\t%d\n" % (self.departments[pool_name].name, c)
			self.funds -= c
		msg += "cult treasury: %d.\n" % self.funds
		if self.funds < 0:
			msg += "The cult needs money!\n"
		temp_log.append(("Projected end-of-month total:", self.funds, 0))
		self.financial_log[self.date] = temp_log
		return msg
	
	"""Calculate changes in publicity for this month."""
	def publicity(self):
		population_levels = [10,25,50,100,200,500,1000,2000,5000]
		fame_from_size = 0
		cult_size = len(self.membership)
		for pop in population_levels:
			if cult_size > pop:
				fame_from_size += 10
			else:
				break #Nope, done here.
		baseline_fame = (fame_from_size + (self.max_fame / 2)) / 2
		self.fame = nudgeTowardsAverage(self.fame, baseline_fame)
		return "baseline: %d Fame: %d.\n" % (baseline_fame, self.fame)
		
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
				self.unassignCultists([cultist]) #Whoops, they still working after quitting!
				cultist.rank = Person.RANK_EX
				quit_count += 1
				self.ex_members.append(cultist)
				#TODO: If the cult's turned murderous, now's the chance to kill them before they escape...
				#TODO: If their fanaticism + ambition? is high enough, they may schism!
				#Check to see if quitter because an enemy
				#Now all the things that kept them in go against them...
				if percentCheck(cultist.sunk_cost):
					cultist.morale -= random.randint(0,min(cultist.sunk_cost,1))
				if percentCheck(cultist.fanaticism):
					cultist.morale -= random.randint(0,min(cultist.fanaticism,1))
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
					self.removeLabor(cultist.department.name, [cultist])
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
					self.removeLabor(cultist.department.name, [cultist])
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
	
	def monthlyPassiveRecruitment(self):
		#use up any purchased ads.
		#ads may attract people, also may raise fame.
		ads = {"magazine_ad" : 1, "internet_ad": 2, "radio_ad": 2, "tv_ad": 5}
		msg = ""
		effective_fame = self.fame
		
		for m_name in ads:
			if self.supplies.has_key(m_name):
				n = self.supplies[m_name]
				if n > 0:
					self.supplies[m_name] = 0 #Use them all up.
					effective_fame += (ads[m_name] * n)
					for ii in range(n):
						if random.randint(1, self.fame) >= ads[m_name]:
							self.fame += 1 #SMALL possibility of an ad improving the cult's fame...
					msg += "Ran %d %s.\n" % (n, findMerch(m_name).name)
				#This should probably have a diminishing returns effect, so you can't just spam your way to universal recognition?
		
		#If the cult's not secretive, random people may hear about it and want to join.
		potential_audience =  effective_fame * effective_fame
		
		fanaticism_mod = 10
		if self.popularity >= 75:
			multiplier = 0.05 
			fanaticism_mod = 20
		elif self.popularity >= 50:
			multiplier = 0.04
		elif self.popularity >= 25:
			multiplier = 0.03
		elif self.popularity >= 0:
			multiplier = 0.02
		else:
			multiplier = 0.01
			fanaticism_mod = 40 #Hated groups get more fanatical recruits.
		
		audience = random.randint(0, int(potential_audience * multiplier))
		new_recruits = []
		for ii in range(audience):
			recruit = Person()
			recruit.fanaticism = fanaticism_mod
			recruit.morale = 50
			new_recruits.append(recruit)
		if len(new_recruits) > 0:
			msg += "%d new members were attracted to join the cult!\n" % len(new_recruits)
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
	
	def addLaborPool(self, lp):
		if lp.name in self.departments:
			print "error: labor pool", lp.name, "already exists in cult."
		else:
			self.departments[lp.name] = lp
	
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
					
	#This uses the department NAME.
	def assignLabor(self, department, cultists):
		#TODO: add permanency, monthly function?
		if department in self.departments: 
			"""		
			d = LaborPool()
			d.name = department
			self.departments[department] = d 
			"""
			d = self.departments[department]
			for c in cultists:
				if c.department: #Make sure they're not in two departments at once.
					c.department.removePerson(c) 
				d.addPerson(c)
			self._docallbacks()
		else:
			print "Error: Effort to assign people to unknown labor pool", department.name

	"""When we don't need to assign them somewhere else yet."""
	def unassignCultists(self, cultists):
		for c in cultists:
			if c.department: #Make sure they're not in two departments at once.
				c.department.removePerson(c) 
		self._docallbacks()
		
	def removeLabor(self, department, cultists):
		if department in self.departments:
			d = self.departments[department]
			for c in cultists:
				d.removePerson(c)
			self._docallbacks()
		else:
			print "Error: Effort to remove people from unknown labor pool", department.name

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
	
	def calculateAverageMorale(self, accurate = False):
		#This number should get distorted, if accurate = false.
		#High-fanaticism people will try to act happier, as will people in an authoritarian cult,
		#and if the Leader is too fanatical, it will skew upwards as well.
		sum = 0
		count = 0
		for cultist in self.membership:
			sum += cultist.morale
			if not accurate:
				if cultist.fanaticism > 50:
					sum += 10
				if cultist.fanaticism > 75:
					sum += 10
				if self.authoritarianism > 50:
					sum += 10
				if self.authoritarianism > 75:
					sum += 10
		average_morale = sum / len(self.membership)
		if not accurate:
			leader = self.getLeader()[0]
			if leader.fanaticism > 50:
				average_morale += 10
			if leader.fanaticism > 75:
				average_morale += 10
		return min(average_morale, 99) #Can't go over 100?  Or will it matter?
		
		
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
			