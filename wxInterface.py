import wx
import wx.html
from mvc import *
import SetupPage
from datetime import date, timedelta
import wxLaborPoolControls
import cult
import person
#include <wx/html/htmlwin.h>

"""Trying to use wxPython to set up a UI for this game."""

"""Overall 'keep everything straight' object for the game."""
class GameObject(CrudeObservable):
	def __init__(self):
		CrudeObservable.__init__(self)
		self.cult = None
		self.leader = None
		self.date = None
		
	def test(self):
		print "testing..."
		
	def advanceMonth(self):
		#Do all the things necessary to move the game ahead one month.
		#Do functions in here - cult activities, enemies, govenment, media, random stuff....
		#And advance to next month.
		
		next_month = self.date + timedelta(days=32)
		next_month.replace(day=1)
		self.date = next_month
		self._docallbacks()

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
	def __init__(self, parent, game):
		wx.Panel.__init__(self, parent)
		self.game = game
		self.cult = game.cult
		cult = game.cult
		
		self.last_month_funds = 0
		self.last_month_membership = 0
		self.last_month_morale = 0
		
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
		self.update()
	
	#Gets called at the start of the month, never any other time?
	def update(self):
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
		#Cult activities log
		for ii in range(1, 20):
			self.log_text_field.WriteText("%d: Activities log (Under construction)\n" % ii) 
			
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
		self.loss_field.SetLabel(str(self.loss))
		self.loss_field.Show(self.loss != 0)
		self.right_sizer.Layout()
		self.parent.sizer.Layout()
		self.parent.updateTotal()
		
	def update(self, watchee):
		self.name = watchee.name
		self.gain = watchee.getGain()  #Hm... this will always be 'projected' gain?
		self.loss = watchee.getLoss()
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
	
#This one is static - same layout, but it's getting info from a file or text?
class PastFinancePanel(wx.Panel):
	def __init__(self, parent, game):
		wx.Panel.__init__(self, parent)

class FinancePanel(wx.Panel):
	def __init__(self, parent, game):
		wx.Panel.__init__(self, parent)
		self.game = game
		self.game.cult.addCallback(self.cultUpdate)
		self.sizer = wx.BoxSizer(wx.VERTICAL or wx.ALIGN_CENTER)
		self.header = wx.BoxSizer(wx.HORIZONTAL or wx.ALIGN_CENTER)
		self.header.Add(wx.StaticText(self, label="Select month: "))
		self.date_selector = SetupPage.InlineCalendar(self, show_day=False)
		self.header.Add(self.date_selector)
		self.btn_load_month = wx.Button(self, label="View", style=wx.BU_EXACTFIT)
		self.header.Add(self.btn_load_month)
		#The button needs to be bound.
		
		self.btn_this_month = wx.Button(self, label="Now: " + game.date.strftime("%B %Y"), style=wx.BU_EXACTFIT)
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
		
		self.past_panel = wx.Panel(self)
		self.past_panel_sizer = wx.BoxSizer(wx.VERTICAL)
		self.past_panel_sizer.Add(wx.StaticText(self.past_panel, label="Past month"))
		self.past_panel.SetSizer(self.past_panel_sizer)
		self.sizer.Add(self.past_panel)
		
		self.SetSizer(self.sizer)
		self.sizer.Layout()
		
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
		
	def monthUpdate(self, new_month):
		#snapshot the current month's financial data, save it to disk.
		#advance to the new month.
		#Calculate the month's expenses.
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
		#self.game.test()
		
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
		self.game.leader.name = 'J.R. "Bob" Dobbs'
		self.game.leader.gender = 'm'
		self.game.leader.morale = 55
		self.game.leader.birthday = date(1959,4,1)
		self.game.leader.rank= person.Person.RANK_LEADER
		self.game.cult.leader = self.game.leader
		self.game.cult.membership.append(self.game.leader)
		self.game.date = date.today()
		for ii in range(25):
			self.game.cult.membership.append(person.Person())
		for ii in range(25):
			p = person.Person()
			p.rank = person.Person.RANK_OUTER_CIRCLE
			self.game.cult.membership.append(p)
		self.GameStartedPages()

	
	def GameStartedPages(self):
		#Game has been started/loaded, and it underway.
		#Put in all the appropriate pages.
		if self.game.cult:
			nb = self.nb
			self.nb.DeleteAllPages()
			panel_main = MainCultPanel(nb, self.game)
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
			panel_inventory = ExamplePanel(nb, "Inventory")
			self.nb.AddPage(panel_inventory, "Inventory")
			panel_beliefs = ExamplePanel(nb, "Beliefs")
			self.nb.AddPage(panel_beliefs, "Beliefs")
			panel_enemies = ExamplePanel(nb, "Enemies")
			self.nb.AddPage(panel_enemies, "Enemies")
			self.game.advanceMonth() #Start 1st of next month.
			self.game_update(self.game)
		else:
			#Something went wrong, the cult's not initialized.
			self.addStartPages()
		
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
	game = GameObject()
	ca = CultApp(game)