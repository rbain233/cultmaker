import wx
from mvc import *
from laborpool import * 
from person import * 
from cult import *

#Assuming the LaborPool class counts as the model....
#This is sort of a combination view/controller.  DEAL WITH IT.
class LaborPoolViewRankSubsection:
	def __init__(self, frame, sizer, labor_pool, cult, rank):
		self.labor_pool = labor_pool
		self.cult = cult
		self.rank = rank
		self.sizer = sizer
		self.labor_pool.addCallback(self.callbackPoolChange)
		tmp_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.label = wx.StaticText(frame, label=rank)
		tmp_sizer.Add(self.label, 0, wx.EXPAND | wx.ALL)
		self.btn_zero = wx.Button(frame, label="0", style=wx.BU_EXACTFIT)
		tmp_sizer.Add(self.btn_zero, 0, wx.EXPAND | wx.ALL)
		self.btn_minus_ten = wx.Button(frame, label="-10", style=wx.BU_EXACTFIT)
		tmp_sizer.Add(self.btn_minus_ten, 0, wx.EXPAND | wx.ALL)
		self.btn_minus_one = wx.Button(frame, label="-1", style=wx.BU_EXACTFIT)
		tmp_sizer.Add(self.btn_minus_one, 0, wx.EXPAND | wx.ALL)
		self.txt_people_count_view = wx.TextCtrl(frame, 0, size=(60,-1), style=wx.TE_RIGHT)
		self.txt_people_count_view.SetEditable(False)
		tmp_sizer.Add(self.txt_people_count_view, 0, wx.EXPAND | wx.ALL)
		self.btn_plus_one = wx.Button(frame, label="+1", style=wx.BU_EXACTFIT)
		tmp_sizer.Add(self.btn_plus_one, 0, wx.EXPAND | wx.ALL)
		self.btn_plus_ten = wx.Button(frame, label="+10", style=wx.BU_EXACTFIT)
		tmp_sizer.Add(self.btn_plus_ten, 0, wx.EXPAND | wx.ALL)
		self.btn_max = wx.Button(frame, label="All", style=wx.BU_EXACTFIT)
		tmp_sizer.Add(self.btn_max, 0, wx.EXPAND | wx.ALL)
		#now bind 'em.
		self.btn_zero.Bind(wx.EVT_BUTTON, self.zeroPeople)
		self.btn_minus_ten.Bind(wx.EVT_BUTTON, self.minusTenPeople)
		self.btn_minus_one.Bind(wx.EVT_BUTTON, self.minusOnePeople)
		#Bind txt_people_count_view ... later.
		self.btn_plus_one.Bind(wx.EVT_BUTTON, self.plusOnePeople)
		self.btn_plus_ten.Bind(wx.EVT_BUTTON, self.plusTenPeople)
		self.btn_max.Bind(wx.EVT_BUTTON, self.maxPeople)
		self.sizer.Add(tmp_sizer, 0, wx.ALL) #This all needs to be one 'chunk' for the sizer.
		
	def zeroPeople(self, evt):
		#Remove all people of (rank)
		list = self.labor_pool.getPeopleList(self.rank)
		#for p in list:
		#	self.labor_pool.removePerson(p)
		self.cult.removeLabor(self.labor_pool.name, list)

	def minusTenPeople(self, evt):
		#remove first ten (rank)
		list = self.labor_pool.getPeopleList(self.rank)
		list = list[0:10]
		#for p in list:
		#	self.labor_pool.removePerson(p)
		self.cult.removeLabor(self.labor_pool.name, list)
		
	def minusOnePeople(self, evt):
		#remove first one person of (rank)
		list = self.labor_pool.getPeopleList(self.rank)
		list = list[0:1]
		#for p in list:
		#	self.labor_pool.removePerson(p)
		self.cult.removeLabor(self.labor_pool.name, list)
		
	def plusOnePeople(self, evt):
		#add one person of (rank)
		list = self.cult.getUnassignedLaborByRank(self.rank)
		list = list[0:1]
		#for p in list:
		#	self.labor_pool.addPerson(p)
		self.cult.assignLabor(self.labor_pool.name, list)
		
	def plusTenPeople(self, evt):
		list = self.cult.getUnassignedLaborByRank(self.rank)
		list = list[0:10]
		#for p in list:
		#	self.labor_pool.addPerson(p)
		self.cult.assignLabor(self.labor_pool.name, list)
		
	def maxPeople(self, evt):
		list = self.cult.getUnassignedLaborByRank(self.rank)
		#for p in list:
		#	self.labor_pool.addPerson(p)
		self.cult.assignLabor(self.labor_pool.name, list)
		
	def callbackPoolChange(self, labor_pool):
		list = self.labor_pool.getPeopleList(self.rank)
		assigned = len(list)
		self.txt_people_count_view.ChangeValue(str(assigned)) 
		unassigned = len(self.cult.getUnassignedLaborByRank(self.rank))
		"""
		max_people = assigned + unassigned
		if self.labor_pool.getMaxPeople() != "unlimited":
			max_people = max(max_people, self.labor_pool.getMaxPeople())
		self.btn_max.SetLabel(str(max_people)) 
		"""
		#This could stand to be more efficient.
	
	def destroy(self):
		self.labor_pool.delCallback(self.callbackPoolChange)

class LaborPoolView:
	def __init__(self, frame, sizer, labor_pool, cult):
		self.labor_pool = labor_pool
		self.sizer = sizer
		self.cult = cult
		self.frame = frame
		rank_order = (Person.RANK_RECRUIT, Person.RANK_OUTER_CIRCLE, Person.RANK_INNER_CIRCLE)
		self.label = wx.StaticText(frame, label=labor_pool.short_name)
		self.sizer.Add(self.label, 0, wx.ALL)
		self.subsections = []
		
		for rank in rank_order:
			if self.labor_pool.rankOK(rank):
				lp = LaborPoolViewRankSubsection(self.frame, self.sizer, self.labor_pool, self.cult, rank)
				self.subsections += [lp]
				#self.sizer.Add(lp.sizer, 0, wx.ALL)
			else:
				self.sizer.Add(wx.StaticText(frame, label="X"), 0, wx.ALL)
		self.sizer.Add(wx.StaticText(frame, label="Leader"), 0, wx.ALL)

		if labor_pool.rankOK(Person.RANK_LEADER):
			pass #This one might just be a checkbox?

	def destroy(self):
		#This is being removed, so delete all the internal parts, too.
		for lp in self.subsections:
			lp.destroy()

class UnassignedCultistsView:
	rank_order = (Person.RANK_RECRUIT, Person.RANK_OUTER_CIRCLE, Person.RANK_INNER_CIRCLE, Person.RANK_LEADER)
	
	def __init__(self, parent, sizer, cult):
		self.cult = cult
		self.cult.addCallback(self.update)
		self.sizer = sizer
		self.label = wx.StaticText(parent, label="Unassigned Cultists ")
		self.sizer.Add(self.label, 0, wx.ALL)
		self.ranked_labels = {}
		self.ranked_fields = {}
		for rank in self.rank_order:
			tmp_sizer = wx.BoxSizer(wx.HORIZONTAL)
			self.ranked_labels[rank] = wx.StaticText(parent, label= " " + rank + ": ")
			self.ranked_fields[rank] = wx.TextCtrl(parent, -1, size=(60,-1), style=wx.TE_RIGHT)
			self.ranked_fields[rank].SetEditable(False)
			tmp_sizer.Add(self.ranked_labels[rank], 0, wx.ALL)
			tmp_sizer.Add(self.ranked_fields[rank], 0, wx.ALL)
			sizer.Add(tmp_sizer, 0,  wx.ALL)
			
		self.update(self.cult)
		
	def update(self, cult):
		for rank in self.rank_order:
			list = cult.getUnassignedLaborByRank(rank)
			self.ranked_fields[rank].ChangeValue(str(len(list)))

class AllLaborPoolsView(wx.Panel):
	"""This page is supposed to show all the cult's labor pools.
	When pools are added/lost, update this."""
	def __init__(self, parent, cult):
		wx.Panel.__init__(self, parent)
		self.cult = cult
		self.parent = parent
		self.cult.addCallback(self.update)
		#self.sizer = wx.BoxSizer(wx.VERTICAL)
		pool_count = len(cult.departments) + 1
		self.sizer = wx.FlexGridSizer(0, 5, 9, 25)
		self.labor_pool_watchers = {}
		"""Create one view row for unassigned cultists, and one for each labor pool."""
		self.unassigned_cultists_view = UnassignedCultistsView(self.parent, self.sizer, cult)
		#self.sizer.Add(self.unassigned_cultists_view.sizer, 0, wx.ALL)
		self.update(cult)
	
	def update(self, cult):
		"""Check if any pools have been added/removed. If so, add/remove them here."""
		"""Add any new pools"""
		for dept_name in cult.departments:
			if cult.departments[dept_name] not in self.labor_pool_watchers.keys():
				#print "making new", dept_name
				#add a new labor_pool watcher.
				self.labor_pool_watchers[cult.departments[dept_name]] = LaborPoolView(self.parent, self.sizer, cult.departments[dept_name], cult) #Adds itself to the window.
				self.sizer.Layout() #THAT fixed the 'form in the corner' problem.
				
				
		"""remove any removed pools."""
		for lp in self.labor_pool_watchers:
			if lp not in cult.departments.values():
				#Remove missing labor_pool's watcher.
				#self.sizer.Remove(self.labor_pool_watchers[dept_name].sizer)
				#TODO
				#Need a way to delete this...
				self.labor_pool_watchers[lp].destroy()
				self.labor_pool_watchers.pop(dept_name, None) #dereference it.
		"""TODO: the other views will need to remove their callbacks when deleted?"""
		
if __name__ == "__main__":
	#test_pool = LaborPool("foo")
	cult = Cult()
	#cult.departments["foo"] = test_pool
	for ii in range(25):
		cult.membership.append(Person())
	for ii in range(25):
		p = Person()
		p.rank = Person.RANK_OUTER_CIRCLE
		cult.membership.append(p)
	app = wx.App(False)
	frame = wx.Frame(None, wx.ID_ANY, "Main View", (200,200), (1400,800))
	sizer = wx.BoxSizer(wx.VERTICAL)
	#ucv = UnassignedCultistsView(frame, cult)
	#sizer.Add(ucv.sizer, 0, wx.ALL)
	controller = AllLaborPoolsView(frame, cult)
	#controller = LaborPoolView(frame, test_pool, cult)
	sizer.Add(controller.sizer, 0, wx.ALL)
	frame.SetSizer(sizer)
	frame.Show()
	app.MainLoop()
	