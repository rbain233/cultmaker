import wx
from mvc import *
import SetupPage
from datetime import date, timedelta
import wxLaborPoolControls
import cult
import person

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
		#Do functuions in here - cult activities, enemies, govenment, media, random stuff....
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
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		#Running cult: Has general cult info page.
		#What-all needs to be here?
		#Cult name, obv.
		#Current date - or should that go in the title bar?  Yes.

		
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
		#Individual pages go here.
		"""
		panel_main = SetupPage.SetupPage(nb)
		nb.AddPage(panel_main, "Main")
		panel_leader = ExamplePanel(nb, "Leader")
		nb.AddPage(panel_leader, "Leader")
		panel_people = ExamplePanel(nb, "Membership")
		nb.AddPage(panel_people, "Membership")
		panel_work = ExamplePanel(nb, "Jobs")
		nb.AddPage(panel_work, "Jobs")
		panel_money = ExamplePanel(nb, "Money")
		nb.AddPage(panel_money, "Money")
		panel_property = ExamplePanel(nb, "Property")
		nb.AddPage(panel_property, "Property")
		panel_inventory = ExamplePanel(nb, "Inventory")
		nb.AddPage(panel_inventory, "Inventory")
		panel_beliefs = ExamplePanel(nb, "Beliefs")
		nb.AddPage(panel_beliefs, "Beliefs")
		panel_enemies = ExamplePanel(nb, "Enemies")
		nb.AddPage(panel_enemies, "Enemies")
		"""
		
		self.sizer.Add(self.nb, 1, wx.EXPAND)
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
			panel_main = ExamplePanel(nb, "Main")
			self.nb.AddPage(panel_main, "Main")
			panel_leader = ExamplePanel(nb, "Leader")
			self.nb.AddPage(panel_leader, "Leader")
			panel_people = ExamplePanel(nb, "Membership")
			self.nb.AddPage(panel_people, "Membership")
			panel_work = wxLaborPoolControls.AllLaborPoolsView(nb, self.game.cult) #IT WORKS!  But it needs a smaller font size...
			self.nb.AddPage(panel_work, "Jobs")
			panel_money = ExamplePanel(nb, "Money")
			self.nb.AddPage(panel_money, "Money")
			panel_property = ExamplePanel(nb, "Property")
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