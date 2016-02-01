import random
import wx
#import wx.calendar as cal
import datetime
from cult import *
from person import *

bonus_list = ["had a well-paying job", "was independently wealthy", "was a talented artist and writer", "already had attracted several followers", "had a Doctorate degree", "was already somewhat famous"]

class InlineCalendar(wx.BoxSizer):
	month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	def __init__(self, parent, start_date=False, show_day=True):
		day_list = [str(x) for x in range(1,32)]
		wx.BoxSizer.__init__(self, wx.HORIZONTAL)
		self.show_day_field = show_day
		self.month_field = wx.ComboBox(parent, choices=InlineCalendar.month_list, style=wx.CB_READONLY)
		self.Add(self.month_field)
		
		self.day_field = wx.ComboBox(parent, choices=day_list, style=wx.CB_READONLY)
		if not self.show_day_field:
			self.day_field.Hide()
		self.Add(self.day_field)
			
		self.year_field = wx.TextCtrl(parent, 0, size=(100, 30))
		self.year_field.SetMaxLength(4)
		self.Add(self.year_field)
		self.SetValue(start_date)
		
	def SetValue(self, v):
		if v:
			y = v.year
			m = v.month
			d = v.day
		else:
			y = 2000
			m = 1
			d = 1
		self.month_field.SetSelection(m - 1)
		self.day_field.SetSelection(d - 1)
		self.year_field.SetValue(str(y))
		
	def GetValue(self):
		try:
			print self.year_field.GetValue(), self.month_field.GetSelection() + 1, self.day_field.GetSelection() + 1
			d = datetime.date(int(self.year_field.GetValue()), self.month_field.GetSelection() + 1, self.day_field.GetSelection() + 1)
			return d
		except:
			return False
			
	def SetFocus(self):
		self.month_field.SetFocus()
		
"""Take a bunch of fields, use them to create a new cult."""
class SetupPage(wx.Panel):
	def __init__(self, frame, game, back_function, startgame_function):
		wx.Panel.__init__(self, frame)
		
		self.leader = Person()
		self.cult = Cult()
		self.game = game
		self.back_to_startup = back_function
		self.startgame = startgame_function
		
		the_choices = [' ', 'The']
		self.the_select_field = wx.ComboBox(self, choices=the_choices, style=wx.CB_READONLY)
		
		self.cult_name_field = wx.TextCtrl(self, 0, size=(300, 30))
		self.cult_name_field.SetEditable(True)
		self.cult_name_field.SetToolTipString("The name of your cult.")
		
		self.cult_name_short_field = wx.TextCtrl(self, 0, size=(300, 30))
		self.cult_name_short_field.SetEditable(True)
		self.cult_name_short_field.SetToolTipString("A shortened name for your cult.\nFor example, if it's 'the Speleonic Society',\nthis might be 'Society'.")
		
		self.founding_date = datetime.date.today()
		self.founding_date_field = self.founding_date.__str__()
		
		self.leader_name_field = wx.TextCtrl(self, 0, size=(300, 30))
		self.leader_name_field.SetEditable(True)
		self.leader_name_field.SetToolTipString("The cult leader's name.")
		
		gender_choices = ['(male)', '(female)']
		self.gender_select_field = wx.ComboBox(self, choices=gender_choices, style=wx.CB_READONLY)
		
		twentyfive_years = datetime.timedelta(days=(365*random.randint(25,55)) + random.randint(0,354))
		twentyfive_years_ago = datetime.date.today() - twentyfive_years
		self.leader_birthday_date_field = InlineCalendar(self, twentyfive_years_ago) 
		#Should start today minus 20 years?
		
		self.bonus_select_field = wx.ComboBox(self, choices=bonus_list, style=wx.CB_READONLY)
		
		doctrine_choices = [d.name for d in doctrine_list]
		self.doctrine_select_field = wx.ComboBox(self, choices=doctrine_choices, style=wx.CB_READONLY)
		
		sincerity_choices = ['created it as a scam', 'was themselves somewhat doubtful', 'was a fervent believer themselves']
		self.sincerity_select_field = wx.ComboBox(self, choices=sincerity_choices, style=wx.CB_READONLY)
		
		self.cultist_name_field = wx.TextCtrl(self, 0, size=(200, 30))
		self.cultist_name_field.SetEditable(True)
		self.cultist_name_field.SetToolTipString("A nickname for members of your cult.\nFor example, if it's 'the Speleonic Society',\nthis might be 'Speleos'.")
		
		"""
		self.btn_random = wx.Button(self, label="Random choices")
		self.btn_random.Bind(wx.EVT_BUTTON, self.randomChoices)
		"""
		
		self.btn_start = wx.Button(self, label="Start Cult")
		self.btn_start.Bind(wx.EVT_BUTTON, self.setupCultAndLeader)
		
		self.btn_clear = wx.Button(self, label="Clear fields")
		self.btn_clear.Bind(wx.EVT_BUTTON, self.clearFields)
		
		self.btn_cancel = wx.Button(self, label="Cancel")
		self.btn_cancel.Bind(wx.EVT_BUTTON, self.backToStartup)
		
		#TODO: This needs a 'back to main menu' option, and a 'random' option.
		
		
		self.error_name_field = wx.StaticText(self, label="")
		
		self.fields = [self.the_select_field,
					self.cult_name_field,
					'(or "',
					self.cult_name_short_field,
					'" for short)',
					"was founded on ",
					self.founding_date_field,
					" by ",
					self.leader_name_field,
					self.gender_select_field,
					"(Born",
					self.leader_birthday_date_field,
					")"
					"who",
					self.bonus_select_field,
					"It was based on",
					self.doctrine_select_field,
					"beliefs, and it is believed the founder originally",
					self.sincerity_select_field,
					'. Members of the group were called "',
					self.cultist_name_field,
					'".',
					self.btn_start,
					self.btn_clear,
					self.btn_cancel,
					self.error_name_field]
		self.sizer = wx.WrapSizer(wx.HORIZONTAL)
		for f in self.fields:
			if type(f) == str:
				self.sizer.Add(wx.StaticText(self, label=f))
			else:
				self.sizer.Add(f)
			self.sizer.Add((10,10))
		#TODO: This needs better layout.
		self.SetSizer(self.sizer)
		
	def clearFields(self, evt):
		for f in self.fields:
			if type(f) not in (str, wx.Button, wx.StaticText):
				if type(f) == wx.TextCtrl:
					f.SetValue("")
				if type(f) == wx.ComboBox:
					f.SetSelection(wx.NOT_FOUND)
				if type(f) == InlineCalendar:
					f.SetValue(False)
	
	def randomChoices(self, evt):
		#TODO: Need random names & things.
		pass
	
	def backToStartup(self, evt):
		self.back_to_startup()
		pass
	
	def setupCultAndLeader(self, evt):
		#Test all fields.
		for f in self.fields:
			if type(f) not in (str, wx.Button, wx.StaticText, InlineCalendar):
				if not f.GetValue():
					self.error_name_field.SetLabel('error in field' + f.__str__())
					f.SetFocus()
					return False
		#TODO: Check to make sure the founder's birthday isnt absurd - 20 - 100 years, maybe?
		time_diff = self.founding_date - self.leader_birthday_date_field.GetValue()
		birthday = self.leader_birthday_date_field.GetValue()
		if time_diff < datetime.timedelta(days = 0):
			self.error_name_field.SetLabel(birthday.__str__() + "Nice try, but nobody will believe you're a time traveller.")
			self.leader_birthday_date_field.SetFocus()
			return False
		if time_diff <= datetime.timedelta(days = 1):
			self.error_name_field.SetLabel(birthday.__str__() + "You weren't born yesterday.")
			self.leader_birthday_date_field.SetFocus()
			return False
		if time_diff < datetime.timedelta(days = 365 * 20):
			self.error_name_field.SetLabel(birthday.__str__() + "A little young for this, aren't you?")
			self.leader_birthday_date_field.SetFocus()
			return False
		if time_diff > datetime.timedelta(days = 365 * 100):
			self.error_name_field.SetLabel(birthday.__str__() + "A little old for this, aren't you?")
			self.leader_birthday_date_field.SetFocus()
			return False
		#if all the fields have values:
		self.cult.name = self.cult_name_field.GetValue()
		self.cult.short_name = self.cult_name_short_field.GetValue()
		self.cult.members_name = self.cultist_name_field.GetValue()
		self.cult.founding_date = self.founding_date
		
		self.leader.name = self.leader_name_field.GetValue()
		g = self.gender_select_field.GetValue()
		if g == '(male)':
			self.leader.gender = 'm'
		else:
			self.leader.gender = 'f'
		self.leader.birthday = self.leader_birthday_date_field.GetValue()
		#Load the game with them.
		#Go to the main loop.
		self.cult.leader = self.leader
		self.game.cult = self.cult
		self.game.leader = self.leader
		self.game.date = self.cult.founding_date
		
		self.startgame()
		pass
"""
	def growCalendar1(self, evt):
		self.founding_date_field.SetSize((300, 200))
		self.founding_date_field.SetBackgroundColour('Yellow')
		self.founding_date_field.sizer.Fit()
	def shrinkCalendar1(self, evt):
		self.founding_date_field.SetSize((300, 30))
"""
if __name__ == "__main__":
	
	app = wx.App(False)
	frame = wx.Frame(None, wx.ID_ANY, "Main View", (200,200), (1400,800))
	sizer = wx.BoxSizer(wx.VERTICAL)
	frame.SetFont(wx.Font(14, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL ))
	frame.SetBackgroundColour(wx.LIGHT_GREY)
	setup_page = SetupPage(frame, None, None, None)
	
	#controller = LaborPoolView(frame, test_pool, cult)
	sizer.Add(setup_page, 0, wx.ALL)
	frame.SetSizer(sizer)
	frame.Show()
	app.MainLoop()