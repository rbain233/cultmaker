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
	#For now, when recruiting, use the highest abs(popularity) as a modifier.

class BeliefMasterList:
	#Singleton?  Bleh, trying to do them in Python looks to be a pain.
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
		self.addBelief(Belief("buddhism","buddhism","Zen, meditation, and liberation from attachments. Like your wallet."))
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
		self.addBelief(Belief("isolationist","Isolationist","You want to get away from it all.", weirdness = 5, other_check_function = self.isSecondaryBelief))
		
		#self.addBelief(Belief("","",""))  #Probably plenty more where this came from...
		
		
	def addBelief(self, b):
		self.list[b.internal_name] = b

	def getBelief(self, name):
		if name in self.list:
			return self.list[name]
		else:
			return None
	
	def isSecondaryBelief(self, cult):
		return (len(cult.doctrine) > 1)
		
belief_master_list = BeliefMasterList()

class Edict:
	#Things the Leader can decree.  Can affect the way a cult operates.
	#Some just cause tests of faith.
	def __init__(self, internal_name, name, desc, effect=None):
		pass

#TODO:  Make unit test.
if __name__ == "__main__":
	print belief_master_list
	print belief_master_list.getBelief("funny").weirdness
	print belief_master_list.getBelief("fnord")