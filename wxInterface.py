import wx
import wx.html
from mvc import *
import SetupPage
from datetime import date, timedelta
import wxLaborPoolControls
import cult
import person
import merch
import Belief
#include <wx/html/htmlwin.h>

"""Trying to use wxPython to set up a UI for this game."""

"""Overall 'keep everything straight' object for the game."""
class GameObject(CrudeObservable):
	def __init__(self):
		CrudeObservable.__init__(self)
		self.cult = None
		self.leader = None
		self.date = None
		self.event_log = ""  #Just save a string?
		
	def advanceMonth(self):
		#Do all the things necessary to move the game ahead one month.
		#Do functions in here - cult activities, enemies, government, media, random stuff....
		#And advance to next month.
		
		#Enemy stuff
		#Check if cult gets attention.
		#The higher your fame, the more chance media will pay attention.
		#Fame is the main factor if the government will pay attention, but so are criminal members, militiant, pacifist, muslim, political, or psychedelic beliefs.
		#enemies always pay attention, but can't always do much.
		
		#Buy stuff.
		self.event_log += self.cult.doMonth(self.date)
		
		next_month = self.date.month + 1
		if next_month == 13: #Next year.
			self.date = date(self.date.year + 1, 1, 1)
		else:
			self.date = date(self.date.year, next_month, 1)
		
		self.event_log += self.date.strftime("%B %Y") + "\n"
		
		self._docallbacks() #This takes care of updating the frame header.

class ExamplePanel(wx.Panel):
	def __init__(self, parent, name):
		wx.Panel.__init__(self, parent)
		self.name = name
		
class GameStartPanel(wx.Panel):
	def __init__(self, main_frame):
		wx.Panel.__init__(self, main_frame.nb)
		
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add((40,40), 0, wx.CENTRE)
		self.sizer.Add(wx.StaticText(self, label="Cult Maker"), 0, wx.CENTRE)
		self.sizer.Add((10,10), 0, wx.CENTRE)
		
		self.btn_new_game = wx.Button(self, label="New Cult")
		self.sizer.Add(self.btn_new_game, 0, wx.CENTRE)
		self.Bind(wx.EVT_BUTTON, main_frame.OnNew, self.btn_new_game)
		self.sizer.Add((10,10), 0, wx.CENTRE)
		
		self.btn_sg_game = wx.Button(self, label="SubGenius")
		self.sizer.Add(self.btn_sg_game, 0, wx.CENTRE)
		self.Bind(wx.EVT_BUTTON, main_frame.OnSubgenius, self.btn_sg_game)
		self.sizer.Add((10,10), 0, wx.CENTRE)
		
		self.btn_load_game = wx.Button(self, label="Load Cult")
		self.sizer.Add(self.btn_load_game, 0, wx.CENTRE)
		self.Bind(wx.EVT_BUTTON, main_frame.OnLoad, self.btn_load_game)
		self.sizer.Add((10,10), 0, wx.CENTRE)
		
		self.btn_quit = wx.Button(self, label="Quit")
		self.sizer.Add(self.btn_quit, 0, wx.CENTRE)
		self.Bind(wx.EVT_BUTTON, main_frame.OnExit, self.btn_quit)
		self.sizer.Add((10,10), 0, wx.CENTRE)
		
		self.SetSizer(self.sizer)
		
class MainCultPanel(wx.Panel):
	def __init__(self, parent, game, main_window):
		wx.Panel.__init__(self, parent)
		self.game = game
		self.cult = game.cult
		cult = game.cult
		self.main_window = main_window
		
		cult.addCallback(self.update)
		self.game.addCallback(self.gameUpdate)
		
		self.last_month_funds = 0
		self.last_month_membership = 0
		self.last_month_morale = 0
		
		self.month_started_here = True #Used to keep advanceMonth from starting an infinite loop.
		
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		#Running cult: Has general cult info page.
		#What-all needs to be here?
		#Cult name, obv.
		self.cult_name_field = wx.StaticText(self, label=cult.name, style=wx.ALIGN_CENTRE_HORIZONTAL)
		
		self.sizer.Add(self.cult_name_field, 0, wx.ALIGN_CENTER)
		#TODO: Way to change cult's name - causes a fame hit?
		self.sizer.Add((20,20))
		sides_sizer = wx.BoxSizer(wx.HORIZONTAL)
		right_side_sizer = wx.BoxSizer(wx.VERTICAL)
		
		#Cult fame and reputation
		self.cult_fame_field = wx.StaticText(self, label="")
		right_side_sizer.Add(self.cult_fame_field)
		
		#Cult membership
		self.cult_membership_field = wx.StaticText(self, label="")
		right_side_sizer.Add(self.cult_membership_field)
		#Cult $$$
		self.cult_money_field = wx.StaticText(self, label="")
		right_side_sizer.Add(self.cult_money_field)
		#TODO: -/+ money from last month.
		self.cult_money_diff_field = wx.StaticText(self, label="")
		right_side_sizer.Add(self.cult_money_diff_field)
		#TODO: Overall membership mood?
		self.cult_mood_field = wx.StaticText(self, label="")
		right_side_sizer.Add(self.cult_mood_field)
		#Cult activities log? (Needs a scrollbar.)
		self.log_text_field = wx.TextCtrl(self, size = (600,500), style = wx.TE_MULTILINE + wx.TE_READONLY) 
		sides_sizer.Add(self.log_text_field, 1, wx.ALIGN_LEFT)
		sides_sizer.Add((20,20))
		sides_sizer.Add(right_side_sizer)
		self.sizer.Add(sides_sizer)
		self.SetSizer(self.sizer)
		self.next_month_button = wx.Button(self, label="Next Month >>")
		self.sizer.Add(self.next_month_button,1,wx.ALIGN_RIGHT)
		self.next_month_button.Bind(wx.EVT_BUTTON, self.advanceMonth)
		self.update(self.cult)
	
	#Gets called at the start of the month, never any other time?
	def update(self, cult):
		self.cult_name_field.SetLabel(self.cult.name)
		#Cult fame and reputation
		popularity_string = "Your cult is " + self.cult.getFameTitle()
		if self.cult.fame > 10:
			popularity_string +=  " and is " + self.cult.getPopularityTitle()
			if self.cult.fame < 50:
				popularity_string += " by those who know of it."
		self.cult_fame_field.SetLabel(popularity_string)
		#Cult membership
		#Add changes from last month?
		membership = len(self.cult.membership)
		if membership > self.cult.last_month_membership_count:
			adj_string = "(+" + str(membership - self.cult.last_month_membership_count) + ")"
		elif membership < self.cult.last_month_membership_count:
			adj_string = "(-" + str(self.cult.last_month_membership_count - membership) + ")"
		else:
			adj_string = ""
		self.cult_membership_field.SetLabel("Membership: " + str(membership) + " " + adj_string)
		#Cult $$$
		if self.cult.funds > self.cult.last_month_funds:
			adj_string = "(+" + str(self.cult.funds - self.cult.last_month_funds) + ")"
		elif self.cult.funds < self.cult.last_month_funds:
			adj_string = "(-" + str(self.cult.last_month_funds - self.cult.funds) + ")"
		else:
			adj_string = ""
		self.cult_money_field.SetLabel("Cult treasury: $" + str(self.cult.funds) + " "  + adj_string)
		
		morale = self.cult.calculateAverageMorale(accurate=False) #We want it subjective.
		diff = morale - self.cult.last_month_morale
		if diff < -20: 
			adj_string = "---"
		elif diff < -10:
			adj_string = "--"
		elif diff < 0:
			adj_string = "-"
		elif diff == 0:
			adj_string = ""
		elif diff > 20:
			adj_string = "+++"
		elif diff > 10:
			adj_string = "++"
		elif diff > 0:
			adj_string = "+"
			
		if morale < 20:
			mood_str = "disintegrating"
		if morale >= 30:
			mood_str = "miserable"
		if morale >= 40:
			mood_str = "unhappy"
		if morale >= 50:
			mood_str = "ok"
		if morale >= 60:
			mood_str = "happy"
		if morale >= 60:
			mood_str = "joyous"
		if morale >= 80:
			mood_str = "blissful"
		if morale >= 90:
			mood_str = "ecstatic"
		
		#TODO: Take out raw value, it's for debugging.
		self.cult_mood_field.SetLabel("Cult morale: " + mood_str + " (" + str(morale) + ") " + adj_string)
		
	
	def gameUpdate(self, game):
		#Cult activities log
		self.log_text_field.Clear()
		self.log_text_field.WriteText(self.game.event_log) 
		
	def advanceMonth(self, evt):
		#TODO: Add some logic to prompt user if they have a lot of unallocated meeples or similar.
		print "Next month!"
		self.main_window.advanceMonth()

#One line, with name, mouseover desc, and a -/#/+ control
class InventoryBuyControl(wx.Panel):
	def __init__(self, parent, cult, merch):
		wx.Panel.__init__(self, parent)
		self.cult = cult
		self.merch = merch
		self.parent = parent
		#self.SetToolTip(wx.ToolTip(self.merch.desc))
		#self.SetHelpText("YYY" + self.merch.desc)
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		top_sizer = wx.BoxSizer(wx.HORIZONTAL)
		top_sizer.Add(wx.StaticText(self, label=self.merch.name))
		top_sizer.Add((10,10))
		self.inventory_field = wx.StaticText(self, label=str(cult.getSupplies(merch.internal_name)) + " in stock")
		top_sizer.Add(self.inventory_field)
		top_sizer.Add((10,10))
		self.buy_field = wx.StaticText(self, label="buy 0")
		self.buy_amount = 0
		top_sizer.Add(self.buy_field)
		top_sizer.Add((20,10))
		top_sizer.Add(wx.StaticText(self, label="@ $" + str(self.merch.unit_cost) + " each"))
		top_sizer.Add((10,10))
		
		self.btn_buy_more = wx.Button(self, label="+", style=wx.BU_EXACTFIT)
		top_sizer.Add(self.btn_buy_more, 0, wx.CENTRE)
		self.btn_buy_more.Bind(wx.EVT_BUTTON, self.buyMore)
		self.btn_buy_less = wx.Button(self, label="-", style=wx.BU_EXACTFIT)
		top_sizer.Add(self.btn_buy_less, 0, wx.CENTRE)
		self.btn_buy_less.Bind(wx.EVT_BUTTON, self.buyLess)
		self.checkbox_monthly = wx.CheckBox(self, label = 'Repeat purchase every month') 
		top_sizer.Add((10,10))
		top_sizer.Add(self.checkbox_monthly)
		
		self.sizer.Add(top_sizer)
		desc = wx.StaticText(self, label=self.merch.desc)
		desc.SetFont(wx.Font(8, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL ))
		self.sizer.Add(desc)
		self.SetSizer(self.sizer)
	
	def clearBuyField(self):
		self.buy_amount = 0
		self.buy_field.SetLabel("buy " + str(self.buy_amount))
		#Update inventoryPanel
		self.parent.btnUpdate()
		
	def setBuyField(self):
		self.buy_field.SetLabel("buy " + str(self.buy_amount))
		#Update inventoryPanel
		self.parent.btnUpdate()
		
	def buyMore(self, evt):
		self.buy_amount += 1
		self.setBuyField()
	
	def buyLess(self, evt):
		self.buy_amount -= 1
		if self.buy_amount < 0:
			self.buy_amount = 0
		self.setBuyField()
	
	def getBuyAmount(self):
		return self.buy_amount
	
	def setInventory(self, n):
		self.inventory_field.SetLabel(str(n) + " in stock")
	
class InventoryPanel(wx.Panel):
	def __init__(self, parent, game):
		wx.Panel.__init__(self, parent)
		self.cult = game.cult
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.sizer)
		game.cult.addCallback(self.monthlyUpdate)
		self.buy_controls = {}
		self.monthlyUpdate(self.cult)
		
		#TODO: Needs to sum these all up, show how much money will be left after purchase?
		#Or just 'current funds' and 'spending' lines, and a line on the finance page.
		
	#This should only be updated when doing a new month - do we need this?
	def monthlyUpdate(self, cult):
		#self.sizer.Clear()
		for m in merch.merch_list:
			if m.meetsPrereq(cult):
				if m not in self.buy_controls:
					ibc = InventoryBuyControl(self, self.cult, m)
					self.buy_controls[m] = ibc
					self.sizer.Add(ibc)
		for item in cult.supplies:
			m = merch.findMerch(item)
			#It shouldn't be possible to have an inventory of items you can't make...
			self.buy_controls[m].setInventory(cult.getSupplies(item))
		for m in self.buy_controls:
			if not self.buy_controls[m].checkbox_monthly.GetValue():
				self.buy_controls[m].clearBuyField() #If it's not monthly, reset to 0 every month.
		self.sizer.Layout()
		#Should keep a count of available money.
	
	"""Call this before doing the game's monthly method."""
	def advanceMonth(self):
		#Empty cult shopping list.
		self.cult.shopping_list = {}
		for m in self.buy_controls:
			qty = self.buy_controls[m].getBuyAmount()
			if qty > 0:
				self.cult.shopping_list[m] = qty
		
	def btnUpdate(self):
		pass
		
		
class PropertyPanel(wx.Panel):
	def __init__(self, parent, game):
		wx.Panel.__init__(self, parent)
		self.game = game
		self.cult = game.cult
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		
		self.owned_sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(wx.StaticText(self, label="Cult Properties"), 0, wx.ALIGN_CENTER)
		self.sizer.Add(self.owned_sizer)
		self.sizer.Add(wx.StaticLine(self))
		self.for_sale_sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(wx.StaticText(self, label="Properties Available"), 0, wx.ALIGN_CENTER)
		self.sizer.Add(self.for_sale_sizer)
		self.SetSizer(self.sizer)
		self.listProperties()
	
	def listProperties(self):
		self.for_sale_sizer.Clear()
		self.owned_sizer.Clear() #Gets rid of existing fields.
		
		#add all cult properties to owned_sizer, and all available properties to for_sale_sizer.
		#What-all needs to be shown for a property?
		#If for sale, price &/or Monthly rent.
		#Monthly upkeep (If owned)
		#Name, description, people capacity (max), infrastructure needs.
		#"Buy" or "Sell" button.
		#Change name button?  (To keep different buildings separate.)
		#Buying or selling a building should take effect next month?
		#If you buy a property, 'clone' it so you can buy more than one?
		pass

#line items can be for:
#Lump sums of money
#labor pool costs/returns (both?)
#Property costs(/returns?)
#Ok, should this handle both profit and loss, or just one? For now, do both.
class FinanceLineItem:
	def __init__(self, parent, watchee = None, name="", gain=0, loss=0):
		
		#sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.parent = parent
		self.name_field = wx.StaticText(parent)
		#sizer.Add(self.name_field, 1, wx.ALIGN_LEFT)
		self.right_sizer = wx.BoxSizer(wx.VERTICAL)
		self.gain_field = wx.StaticText(parent)
		self.loss_field = wx.StaticText(parent)
		self.right_sizer.Add(self.gain_field, 1, wx.ALIGN_RIGHT)
		self.right_sizer.Add(self.loss_field, 1, wx.ALIGN_RIGHT)
		#sizer.Add(sizer2)
		#self.SetSizer(sizer)
		
		if watchee:
			#Get name and (current) amount from watchee, 
			self.watchee = watchee
			watchee.addCallback(self.update)
			self.update(watchee)
		else:
			#Use name and amount(s).
			self.watchee = None
			self.name = name
			self.gain = gain 
			self.loss = loss
			print self.name, self.gain, self.loss
			self.setFields()
	
	def getLeftElement(self):
		return self.name_field
		
	def getRightElement(self):
		return self.right_sizer
		
	def setFields(self):
		self.name_field.SetLabel(self.name)
		self.gain_field.SetLabel(str(self.gain))
		self.gain_field.Show(self.gain != 0)
		self.loss_field.SetLabel(str(-self.loss))
		self.loss_field.Show(self.loss != 0)
		self.right_sizer.Layout()
		self.parent.sizer.Layout()
		self.parent.updateTotal()
		
	def update(self, watchee):
		self.name = watchee.name
		self.gain = watchee.guessGain()  #Hm... this will always be 'projected' gain?
		self.loss = watchee.guessLoss()
		self.setFields()

#This one is a bit less complex, as it only is there to passively get the sum up the results.
class FinanceLineItemTotal(FinanceLineItem):
	def __init__(self, parent, name=""):
		FinanceLineItem.__init__(self, parent, None, name, 0, 0)
		
	def setFields(self):
		self.name_field.SetLabel(self.name)
		self.gain_field.SetLabel(str(self.gain))
		self.gain_field.Show(self.gain != 0)
		self.loss_field.SetLabel(str(self.loss))
		self.loss_field.Show(self.loss != 0)
		self.right_sizer.Layout()
		self.parent.sizer.Layout()
		#Does not call update, to avoid an infinite regress.
	
	def setTotal(self, amount):
		self.gain = amount
		self.loss = 0
		self.setFields()
	
#This one needs to be updated in real time with changes from assigning/removing minions & buying/selling stuff.
class PresentFinancePanel(wx.Panel):
	def __init__(self, parent, game):
		wx.Panel.__init__(self, parent)
		#When first created, this needs to create 'displayers' for all the labor pools?
		self.game = game
		self.cult = game.cult
		self.list = {}
		#Or are we just summing them up?
		#self.sizer = wx.BoxSizer(wx.VERTICAL) #TODO: Use a wx.FlexGridSizer? Each line-item would take 2 or 4 cells...
		self.sizer = wx.FlexGridSizer(0, 2, 9, 25)
		self.SetSizer(self.sizer)
		
		self.end_total_line = FinanceLineItemTotal(self, name = "Projected end-of-month total:")
		self.start_total_line = FinanceLineItem(self, name = "Cult treasury, start of month:", gain = self.cult.funds)
		
		self.sizer.Add(self.start_total_line.getLeftElement())
		self.sizer.Add(self.start_total_line.getRightElement())
		
		self.sizer.Add(self.end_total_line.getLeftElement())
		self.sizer.Add(self.end_total_line.getRightElement())
		
		self.update(self.cult)
	
	def update(self, cult):
		#add any labor-pools that aren't on the list.
		for lp_name in cult.departments:
			lp = cult.departments[lp_name]
			if lp not in self.list:
				item = FinanceLineItem(self, watchee = lp)
				self.list[lp] = item
				ii = self.sizer.GetItemCount()
				#self.sizer.Insert(ii - 1, self.list[lp], 1, wx.EXPAND)
				self.sizer.Insert(ii - 2, item.getLeftElement(), 1, wx.EXPAND)
				self.sizer.Insert(ii - 1, item.getRightElement(), 1, wx.EXPAND)
				#self.sizer.Add(self.end_total_line.getLeftElement())
				#self.sizer.Add(self.end_total_line.getRightElement())
		#Remove any line-items that don't have corresponding labor-pools.
		for lp in self.list: 
			cult_lps = cult.departments.values()
			if lp not in cult_lps:
				self.sizer.Remove(self.list[lp].getLeftElement())
				self.sizer.Remove(self.list[lp].getRightElement())
				del(self.list[lp])
		self.updateTotal()
		self.sizer.Layout()
		#add up all totals, and make that the end-of-month total.
	
	def updateTotal(self):
		total = 0
		#I have to do these 'if's, or this will get called before the total_lines exist yet.
		if "start_total_line" in dir(self):  
			total = self.start_total_line.gain + self.start_total_line.loss
		for lp in self.list:
			total += self.list[lp].gain + self.list[lp].loss
		if "end_total_line" in dir(self):
			self.end_total_line.setTotal(total)

"""Page for adding and removing
Cult beliefs
Edicts
"""
class BeliefsPanel(wx.ScrolledWindow):
	def __init__(self, parent, game):
		wx.ScrolledWindow.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.VSCROLL)
		self.SetScrollRate( 5, 5 )
		self.game = game
		self.cult = game.cult
		game.cult.addCallback(self.update)
		#How's this going to work?
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.sizer)
		self.update(self.cult)
		
	def update(self, cult):
		self.sizer.Clear()
		self.sizer.Add(wx.StaticText(self, label="Current Beliefs:"))
		#Existing beliefs:
		for b in cult.doctrines:
			bb = Belief.belief_master_list.getBelief(b)
			if bb:
				self.sizer.Add(wx.StaticText(self, label=bb.name))
		
		#Available beliefs.
		self.sizer.Add(wx.StaticText(self, label="Available Beliefs:"))
		for bb in Belief.belief_master_list.getAvailableBeliefs(cult):
			if bb.internal_name in cult.doctrines:
				#print "Nope.", bb.internal_name
				continue
			self.sizer.Add(wx.StaticText(self, label=bb.name))
		
		self.sizer.Add(wx.StaticText(self, label="Available Edicts:"))
		for name in Belief.edict_master_list.list:
			edict = Belief.edict_master_list.list[name]
			self.sizer.Add(wx.StaticText(self, label=edict.name))
		#Mostly, check to see if you have enough 'unspent' dogma to add new beliefs/edicts.
		#Should some edicts have higher costs?
		#Adding new edicts can cause cultists to make tests of faith.
		#So can radical changes in beliefs?
		#How about removing edicts?
		pass
	
	#Don't think it needs one of these.
	"""
	def advanceMonth(self):
		pass
	"""
#This one is static - same layout, but it's getting info from a file or text?
class PastFinancePanel(wx.Panel):
	def __init__(self, parent, game):
		wx.Panel.__init__(self, parent)
		self.game = game
		self.sizer = wx.FlexGridSizer(0, 2, 9, 25)
		self.SetSizer(self.sizer)
	
	def loadMonth(self, date):
		self.sizer.Clear()
		if date in self.game.cult.financial_log:
			month_financial_log = self.game.cult.financial_log[date]
			for entry in month_financial_log:
				(name, gain, loss) = entry
				name_field = wx.StaticText(self, label = name)
				self.sizer.Add(name_field)
				
				right_sizer = wx.BoxSizer(wx.VERTICAL)
				if int(gain) > 0:
					gain_field = wx.StaticText(self, label = str(gain))
					right_sizer.Add(gain_field, 1, wx.ALIGN_RIGHT)
				if int(loss) < 0:
					loss_field = wx.StaticText(self, label = str(loss))
					right_sizer.Add(loss_field, 1, wx.ALIGN_RIGHT)
				self.sizer.Add(right_sizer, 1, wx.ALIGN_RIGHT)
		else:
			#No entries for this month.
			self.sizer.Add(wx.StaticText(self, label = "No financial log for this month."))
			
		self.sizer.Layout()

class FinancePanel(wx.Panel):
	def __init__(self, parent, game):
		wx.Panel.__init__(self, parent)
		self.game = game
		self.game.cult.addCallback(self.cultUpdate)
		self.sizer = wx.BoxSizer(wx.VERTICAL or wx.ALIGN_CENTER)
		self.header = wx.BoxSizer(wx.HORIZONTAL or wx.ALIGN_CENTER)
		select_sizer = wx.BoxSizer(wx.HORIZONTAL)
		select_sizer.Add(wx.StaticText(self, label="Select month: "))
		self.date_selector = SetupPage.InlineCalendar(self, show_day=False)
		select_sizer.Add(self.date_selector)
		self.btn_load_month = wx.Button(self, label="View", style=wx.BU_EXACTFIT)
		select_sizer.Add(self.btn_load_month)
		self.header.Add(select_sizer)
		#The button needs to be bound.
		self.game.addCallback(self.gameMonthlyUpdate)
		
		self.btn_last_month = wx.Button(self, style=wx.BU_EXACTFIT)
		self.header.Add(self.btn_last_month)
		
		self.btn_this_month = wx.Button(self, style=wx.BU_EXACTFIT)
		self.header.Add(self.btn_this_month)
		#The button needs to be bound.
		
		self.header.Layout()
		self.sizer.Add(self.header)
		
		#needs (at least) two subpanels - this month(projected) and previous month
		#No it doesn't, it just needs to render the page correctly.
		#self.present_panel = wx.html.HtmlWindow(self) #This isn't showing up....
		#self.present_panel.SetPage("<i>HTML PANEL</i>")
		self.present_panel = PresentFinancePanel(self, self.game)
		self.sizer.Add(self.present_panel, 1, wx.EXPAND) #EXPAND here is a bit too much, but without it, it's got no room to grow at all.
		
		self.past_panel = PastFinancePanel(self, self.game)
		self.sizer.Add(self.past_panel, 1, wx.EXPAND)
		
		self.past_panel.loadMonth(date(1998,4,1))
		
		self.SetSizer(self.sizer)
		self.sizer.Layout()
		self.gameMonthlyUpdate(self.game)
		#looks like you can't put a notebook inside another notebook, though?
		#So, a radio button or a dropdown?
		#Finance panel.
		#Track projected money gains/losses for the month.
		#Donations and sales: Average all previous months, add wishful thinking? 
		#(oooh, Fanaticism can skew them higher!)
		#TODO: Ability to check past months?
		#Total treasury
		
		
	def cultUpdate(self, cult):
		#Update when a new month starts? No, different callback for that.
		
		#Or when the user incurs expenses.
		#If the window is looking at the current month, this does something.
		#Otherwise, disconnect it?
		#Or have it look at last month?
		pass
	
	def gameMonthLabelsUpdate(self):
		self.btn_last_month.SetLabel("Last Month: " + self.last_month_date.strftime("%B %Y"))
		self.btn_this_month.SetLabel("Projected: " + self.this_month_date.strftime("%B %Y"))
		
	
	def gameMonthlyUpdate(self, game):
		self.this_month_date = game.date
		self.last_month_date = game.date - timedelta(days=1)
		self.last_month_date = self.last_month_date.replace(day=1)
		#snapshot the current month's financial data, save it to disk.
		#advance to the new month.
		#Calculate the month's expenses.
		self.gameMonthLabelsUpdate()
		pass
	
	#Previous Months:
	def assemblePageFromFile(self):
		pass
	
	#Current Month:
	def assemblePageFromCult(self):
		#Blank the fields
		#Fill it in:
		#Income:  Donations (Projected), selling crap (projected), dues (ditto), crimes, lawsuits?
		#Outgo: Labor pool costs, rent, buying stuff, fees.
		#And the total.
		pass
	
class MainWindow(wx.Frame):
	def __init__(self, parent, game_obj, title):
		wx.Frame.__init__(self, parent, wx.ID_ANY, title, (200,200), (1400,800))
		self.CreateStatusBar() # A Statusbar in the bottom of the window
		self.SetFont(wx.Font(14, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL ))
		self.SetBackgroundColour(wx.LIGHT_GREY)
		
		self.game = game_obj
		self.game.addCallback(self.game_update)
		
		#Pages that can directly (or indirectly) effect the game or the cult.
		self.game_control_pages = []
		
		# Setting up the menu.
		filemenu= wx.Menu()

		# wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
		menu_item = filemenu.Append(wx.ID_NEW, "&New Game"," Start a new game")
		self.Bind(wx.EVT_MENU, self.OnNew, menu_item)
		menu_item = filemenu.Append(wx.ID_OPEN, "&Load Game"," Load an existing game")
		self.Bind(wx.EVT_MENU, self.OnLoad, menu_item)
		menu_item = filemenu.Append(wx.ID_SAVE, "&Save Game"," Save game")
		self.Bind(wx.EVT_MENU, self.OnSave, menu_item)
		filemenu.AppendSeparator()
		menu_item = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
		self.Bind(wx.EVT_MENU, self.OnExit, menu_item)
		
		help_menu = wx.Menu()
		menu_item = help_menu.Append(wx.ID_HELP_INDEX, "&Cultopedia", " Information about cults and the game")
		self.Bind(wx.EVT_MENU, self.OnCultopedia, menu_item)
		menu_item = help_menu.Append(wx.ID_ABOUT, "&About"," Information about this program")
		self.Bind(wx.EVT_MENU, self.OnAbout, menu_item)

		# Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
		menuBar.Append(help_menu,"&Help")
		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
		
		self.sizer = wx.BoxSizer(wx.VERTICAL)
				
		#anel1 = wx.Panel(self)
		nb = wx.Notebook(self)
		self.nb = nb
		
		self.addStartPages()
		
		self.sizer.Add(self.nb, 1, wx.EXPAND)
		#For some reason, trying to add a button here makes nothing show up, so I'll have to add it on individual pages?  Blargh.
		self.sizer.Layout()
		wx.CallAfter(nb.Refresh) #Gets rid of black square that was appearing on the topmost page.
		self.game_update(self.game)
		self.Show(True)
		

	def OnAbout(self,e):
		# A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
		dlg = wx.MessageDialog( self, "CULT LEADER", "CULT LEADER", wx.OK)
		dlg.ShowModal() # Show it
		dlg.Destroy() # finally destroy it when finished.	
		
	def OnNew(self, e):
		#hide the notebook
		#self.sizer.Hide(self.nb_sizer)
		self.nb.DeleteAllPages()
		panel_main = SetupPage.SetupPage(self.nb, self.game, self.addStartPages, self.GameStartedPages)
		self.nb.AddPage(panel_main, "New Cult")
		self.game.cult = None
		self.game_update(self.game)
		#This needs better sizing, but it works!
	
	def OnLoad(self, e):
		dlg = wx.MessageDialog( self, "Under Construction", "Load Game", wx.OK)
		dlg.ShowModal() # Show it
		dlg.Destroy() # finally destroy it when finished.	
	
	def OnSave(self, e):
		dlg = wx.MessageDialog( self, "Under Construction", "Save Game",  wx.OK)
		dlg.ShowModal() # Show it
		dlg.Destroy() # finally destroy it when finished.	
		
	def OnCultopedia(self, e):
		dlg = wx.MessageDialog( self, "All you need to know about cults!", "Cultopedia", wx.OK)
		dlg.ShowModal() # Show it
		dlg.Destroy() # finally destroy it when finished.	

	def OnExit(self,e):
		self.Close(True)
		
	def addInitPages(self):
		#Put in the new/load/exit page.
		pass
		
	def addStartPages(self):
		#Put in all the game-startup tabs. (Just one, right now.)
		self.nb.DeleteAllPages()
		self.game_control_pages = []
		self.panel_inventory = None #Got to clear this.
		self.nb.AddPage(GameStartPanel(self), "Start")
		#And initialize them.
		pass
	
	def OnSubgenius(self, e):
		self.game.cult = cult.Cult()
		self.game.leader = person.Person()
		self.game.cult.name = "Church of the SubGenius"
		self.game.cult.short_name = "SubGenius"
		self.game.cult.members_name = "SubGenii"
		self.game.cult.founding_date = date(1998,07,05)
		self.game.cult.doctrines= ["ufo", "apocalyptic", "funny"]
		self.game.leader.name = 'J.R. "Bob" Dobbs'
		self.game.leader.gender = 'm'
		self.game.leader.morale = 55
		self.game.leader.birthday = date(1959,4,1)
		self.game.leader.rank= person.Person.RANK_LEADER
		self.game.cult.leader = self.game.leader
		self.game.cult.membership.append(self.game.leader)
		self.game.date = date.today() + timedelta(days=32) 
		self.game.date = self.game.date.replace(day=1)
		for ii in range(25):
			self.game.cult.membership.append(person.Person())
		for ii in range(25):
			p = person.Person()
			p.rank = person.Person.RANK_OUTER_CIRCLE
			p.morale = 75
			p.fanaticism = 40
			self.game.cult.membership.append(p)
		self.GameStartedPages()

	
	def GameStartedPages(self):
		#Game has been started/loaded, and it underway.
		#Put in all the appropriate pages.
		if self.game.cult:
			nb = self.nb
			self.nb.DeleteAllPages()
			panel_main = MainCultPanel(nb, self.game, self)
			self.nb.AddPage(panel_main, "Main")
			panel_leader = ExamplePanel(nb, "Leader")
			self.nb.AddPage(panel_leader, "Leader")
			panel_people = ExamplePanel(nb, "Membership")
			self.nb.AddPage(panel_people, "Membership")
			panel_work = wxLaborPoolControls.AllLaborPoolsView(nb, self.game.cult) #IT WORKS!  But it needs a smaller font size...
			self.nb.AddPage(panel_work, "Jobs")
			panel_money = FinancePanel(nb, self.game)
			self.nb.AddPage(panel_money, "Finance")
			panel_property = PropertyPanel(nb, self.game)
			self.nb.AddPage(panel_property, "Property")
			self.panel_inventory = InventoryPanel(nb, self.game)
			self.nb.AddPage(self.panel_inventory, "Inventory")
			panel_beliefs = BeliefsPanel(nb, self.game)
			self.nb.AddPage(panel_beliefs, "Beliefs")
			panel_enemies = ExamplePanel(nb, "Enemies")
			self.nb.AddPage(panel_enemies, "Enemies")

			self.game.date.replace(day=1)
			
			self.game_control_pages = [panel_main,
				panel_leader,
				panel_people,
				panel_work,
				panel_money,
				panel_property,
				self.panel_inventory,
				panel_beliefs,
				panel_enemies]
			
			self.game_update(self.game)
		else:
			#Something went wrong, the cult's not initialized.
			self.addStartPages()
	
	def advanceMonth(self):
		for page in self.game_control_pages:
			if hasattr(page,"advanceMonth"):
				if not hasattr(page,"month_started_here"): #Avoid infinite recursion
					page.advanceMonth()
		self.game.advanceMonth()
			
			
	def game_update(self, game):
		if game and game.cult:
			self.SetTitle("CULT MAKER: " + game.cult.name + " " + game.date.strftime("%B %Y"))
		else:
			self.SetTitle("CULT MAKER")
	
class CultApp(wx.App):
	def __init__(self, game_obj):
		wx.App.__init__(self)
		frame = MainWindow(None, game_obj, "Cult Leader")
		self.game = game_obj
		self.MainLoop()
		
if __name__ == "__main__":
	#wx.ToolTip.Enable(True)  #Huh, adding this made it crash?
	game = GameObject()
	ca = CultApp(game)