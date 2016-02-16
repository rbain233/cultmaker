#Items the cult can buy that aren't properties and require no staff.
class Merch:
	def __init__(self, internal_name, name, desc, unit_cost, prereq_function = False):
		self.internal_name = internal_name
		self.name = name
		self.desc = desc
		self.unit_cost = unit_cost
		self.prereq_function = prereq_function
	
	def meetsPrereq(self, cult):
		if self.prereq_function:
			return self.prereq_function(self, cult)
		else:
			return True

def pamphletCheck(self, cult):
	return cult.dogma > 10
	
def bookCheck(self, cult):
	return cult.dogma > 40
	
def radioAdCheck(self,cult):
	return cult.dogma > 20
	
merch_list = [Merch("pamphlet_crude", "Crude Pamphlets (100)", "Black and white photocopied introductory pamphlets", 10, pamphletCheck),
			Merch("pamphlet_slick", "Slick Pamphlets (100)", "Nicely printed color introductory pamphlets on glossy paper", 25, pamphletCheck),
			Merch("paraphernalia", "Misc. Paraphernalia", "Prayer cloths, bumper stickers, amulets, posters, t-shirts and other things to sell to believers.", 4),
			Merch("radio_ad", "Radio Ad", "A quick ad for the cult on radio stations", 2000, radioAdCheck),
			Merch("tv_ad", "TV Ad", "A quick ad for the cult on TV stations", 5000, radioAdCheck),
			Merch("book1", "Book of Scriptures, volume 1 (100)", "A book containing some of the cult's doctrines, suitable for new recruits", 500, bookCheck)
			]
			
def findMerch(merch_name):
	for m in merch_list:
		if m.internal_name == merch_name:
			return m
	return False
