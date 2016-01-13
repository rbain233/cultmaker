import wx
from mvc import *

"""Trying to use wxPython to set up a UI for this game."""

class ExamplePanel(wx.Panel):
	def __init__(self, parent, name):
		wx.Panel.__init__(self, parent)
		self.name = name

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, wx.ID_ANY, title, (200,200), (1200,800))
		self.CreateStatusBar() # A Statusbar in the bottom of the window

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
		
		nb = wx.Notebook(self)
		#Individual pages go here.
		panel_main = ExamplePanel(nb, "Main")
		#MVC stuff testing.
		
		
		
		
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

		wx.CallAfter(nb.Refresh) #Gets rid of black square that was appearing on the topmost page.
		self.Show(True)

	def OnAbout(self,e):
		# A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
		dlg = wx.MessageDialog( self, "CULT LEADER", "CULT LEADER", wx.OK)
		dlg.ShowModal() # Show it
		dlg.Destroy() # finally destroy it when finished.	
		
	def OnNew(self, e):
		dlg = wx.MessageDialog( self, "Under Construction", "New Game", wx.OK)
		dlg.ShowModal() # Show it
		dlg.Destroy() # finally destroy it when finished.	
	
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
		
class CultApp(wx.App):
	def __init__(self):
		wx.App.__init__(self)
		frame = MainWindow(None, "Cult Leader")
		self.MainLoop()
		
ca = CultApp()