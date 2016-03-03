class Belief:
	def __init__(self, internal_name, name, desc, prereq_beliefs = [], opposed_beliefs = [], other_check_function = None, weirdness = 0, popularity = 0):
		self.name = name
		self.internal_name = internal_name
		self.desc = desc
		self.prereq_beliefs = prereq_beliefs #Other beliefs you need to have first?
		self.opposed_beliefs = opposed_beliefs #List of names, or actual Beliefs?
		self.other_check_function = other_check_function
		self.weirdness = weirdness
		self.popularity = popularity
		#I need to think about how these two are going to affect a cult...
	
	def isBeliefAvailable(self, cult):
		if self.other_check_function:
			if not self.other_check_function(cult):
				return False
		if self.prereq_beliefs:
			if cult:
				for b in self.prereq_beliefs:
					if b not in cult.doctrines:
						return False
			else:
				return false
		if self.opposed_beliefs:
			if cult:
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
	#For now, when recruiting, use the highest abs(popularity) as a modifier.

class BeliefMasterList:
	#Singleton?  Bleh, trying to do them in Python looks to be a pain.
	ALL_BELIEFS = "ALL"
	
	def __init__(self):
		self.list = {}
		self.addBelief(Belief("christian", "Christian", "The most popular faith in America. Well-regarded and mainstream.", popularity = 10))
		self.addBelief(Belief("magik", "Magjiyckk", "You believe in spellcasting, invocations, and myspellynge for power.", weirdness = 10))
		self.addBelief(Belief("new age","New Age","Crystals, dolphins, channeled entities, and boring music.", popularity = 5))
		self.addBelief(Belief("pagan","Pagan","Gimme that Old-Time Religion."))
		self.addBelief(Belief("political","Political","Harder to be tax-exempt with this one.", weirdness = -10))
		self.addBelief(Belief("satanism","Satanism","Bizarro Christianity. Not popular.", popularity = -10))
		self.addBelief(Belief("muslim","Muslim","Currently less popular than Satanism.", popularity = -15))
		self.addBelief(Belief("self help","Self Help","Improve yourself! And your bank account.", popularity = 10, weirdness = -10))
		self.addBelief(Belief("ufo","UFO","Contact the Benevolent Space Brothers, prepare for the Invasion, or both.", weirdness = 5))
		self.addBelief(Belief("buddhism","Buddhism","Zen, meditation, and liberation from attachments. Like your wallet."))
		self.addBelief(Belief("yoga","Yoga","Contortions both physical and logical."))
		self.addBelief(Belief("apocalyptic","Apocalyptic","The End Is Coming!!! Real soon now. Any minute now. Annnny minute....", weirdness = 5, other_check_function = self.isSecondaryBelief))
		self.addBelief(Belief("militant","Militant","You're ready to get violent about your faith, whatever it is.", opposed_beliefs=["pacifist"], other_check_function = self.isSecondaryBelief))
		self.addBelief(Belief("pacifist","Pacifist","Violence is not the answer, whatever the question was.", opposed_beliefs = ["militant"], other_check_function = self.isSecondaryBelief))
		self.addBelief(Belief("psychedelic","Psychedelic","You approve of mind-expanding drugs. The DEA does not approve of you.", weirdness = 5))
		self.addBelief(Belief("pseudoscience","Pseudoscience","You like to make your teachings sound all sciency.", popularity = 5, other_check_function = self.isSecondaryBelief))
		self.addBelief(Belief("paranoid","Paranoid","You think They're out to get you.", weirdness = 10, other_check_function = self.isSecondaryBelief))
		self.addBelief(Belief("secret","Secret","Your cult doesn't advertise or talk about themselves to outsiders.", other_check_function = self.isSecondaryBelief))
		self.addBelief(Belief("racist","Racist","Your ethnic group, whichever it is, is clearly superior to all others.", other_check_function = self.isSecondaryBelief))
		self.addBelief(Belief("funny","Funny","Yes, this cult is a joke. But that doesn't mean it's not True.", weirdness = 5, other_check_function = self.isSecondaryBelief))
		self.addBelief(Belief("communist","Communist","Power to the People!", opposed_beliefs = ["objectivist"]))
		self.addBelief(Belief("objectivist","Objectivist","Money to the Worthy!", opposed_beliefs = ["communist"]))
		self.addBelief(Belief("isolationist","Isolationist","You want to get away from it all.", weirdness = 5, other_check_function = self.isSecondaryBelief, opposed_beliefs=["evangelistic"]))
		self.addBelief(Belief("evangelistic", "Evangelistic", "You want everyone to hear the cult's teachings and join.", other_check_function = self.isSecondaryBelief, opposed_beliefs=["isolationist", "secret"]))
		
		#self.addBelief(Belief("","",""))  #Probably plenty more where this came from...
		
		
	def addBelief(self, b):
		self.list[b.internal_name] = b

	def getBelief(self, name):
		if name in self.list:
			return self.list[name]
		else:
			return None
	
	def isSecondaryBelief(self, cult):
		if cult == BeliefMasterList.ALL_BELIEFS:
			return True
		if cult:
			return (len(cult.doctrines) > 1)
		else:
			return False #If this is called with a 'none' in the make-a-cult screen.
	
	def getAvailableBeliefs(self, cult):
		for n in self.list:
			b = self.list[n]
			if b.isBeliefAvailable(cult):
				yield b
				#look, ma, a generator!
				
belief_master_list = BeliefMasterList()

class Edict:
	#Things the Leader can decree.  Can affect the way a cult operates.
	#Some just cause tests of faith.
	def __init__(self, internal_name, name, desc, excluded_by=[], requires=[], effect=None, check_function = None):
		self.internal_name = internal_name
		self.name = name
		self.desc = desc
		self.excluded_by = excluded_by
		self.requires = requires
		self.effect = effect
		self.check_function = check_function
		pass
	
	def isAvailable(self, cult):
		if not self.check_function(cult):
			return False
		for name in self.excluded_by:
			if name in cult.doctrines:
				return False
		for name in self.requires:
			if name not in cult.doctrines:
				return False
		return True
		
class MasterEdictList:
	def __init__(self):
		self.list = {}
		self.addEdict(Edict("tithing_10", "Tithing 10%", "Members must donate 10% of their income."))
		self.addEdict(Edict("tithing_15", "Tithing 15%", "Members must donate 15% of their income.", requires=["tithing_10"]))
		self.addEdict(Edict("tithing_20", "Tithing 20%", "Members must donate 20% of their income.", requires=["tithing_10", "tithing_15"]))
		self.addEdict(Edict("celibacy","Celibacy","Cultists are forbidden to have sex.", excluded_by=["free_love"]))
		self.addEdict(Edict("free_love","Free Love","Just Say Yes.", excluded_by=["celibacy", "castration"]))
		self.addEdict(Edict("castration","Castration","Sex is not only forbidden to cultists, it's about to be impossible.", requires=["celibacy"], check_function=self.goneCrazy))
		self.addEdict(Edict("vegetarianism","Vegetarianism","No eating meat."))
		self.addEdict(Edict("weird_diet","Weird Diet","Strange dietary requirements."))
		self.addEdict(Edict("no_booze","No Alcohol","Cultists are forbidden booze."))
		self.addEdict(Edict("no_drugs","No Drugs","Cultists are forbidden to take mind-altering substances.", excluded_by=["psychedelic"]))
		self.addEdict(Edict("loyalty_oath","Loyalty Oath","Cultists must swear eternal allegiance to the cult."))
		self.addEdict(Edict("secrecy_oath","Oath of Secrecy","Cultists swear not to reveal cult rituals or teachings to outsiders.", excluded_by = ["evangelistic"]))
		self.addEdict(Edict("poverty_vow", "Vow of Poverty", "Give up all your worldly possessions!"))
		self.addEdict(Edict("quit_job","Quit your job","Members are expected to work for the cult full-time."))
		self.addEdict(Edict("dress_code","Dress Code","Cultists are expected to follow a strict dress code for normal clothing.", excluded_by=["weird_dress_code"]))
		self.addEdict(Edict("weird_dress_code","Weird Dress Code","Cultists are expected to follow a strict dress code that's very unusual.", excluded_by=["dress_code"]))
		self.addEdict(Edict("tattoos","Mandatory Tattoos","Cultists must get a cult symbol or slogan tattooed on them."))
		self.addEdict(Edict("aggressive_donations","Aggressive Donations","Members are constantly exhorted to donate more money."))
		#self.addEdict(Edict("","",""))
		
	def addEdict(self, edict):
		self.list[edict.internal_name] = edict
	
	def goneCrazy(self, cult):
		#TODO: Need to have some way of metering the Total Craziness of the cult - average or sum of Fanaticism, maybe? (Weighted toward craziness at the top...
		#Average of (Leader.fanaticism, average inner circle fantaticism, average outer circle fanaticism)?
		return False

edict_master_list = MasterEdictList()

#TODO:  Make unit test.
if __name__ == "__main__":
	print belief_master_list
	print belief_master_list.getBelief("funny").weirdness
	print belief_master_list.getBelief("fnord")