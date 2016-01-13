import wx
from cult import *
from person import *

"""Take a bunch of fields, use them to create a new cult."""
class SetupPage(wx.Panel):
	def __init__(self, frame):
		wx.Panel.__init__(self, frame)
		self.leader = Person()
		self.cult = Cult()
		
		the_choices = ['', 'The']
		self.the_select_field = wx.ComboBox(self, choices=the_choices, style=wx.CB_READONLY)
		
		self.cult_name_field = wx.TextCtrl(self)
		self.cult_name_field.SetEditable(True)
		
		self.leader_name_field = wx.TextCtrl(self)
		self.leader_name_field.SetEditable(True)
		
		gender_choices = ['', '(male)', '(female)']
		self.gender_select_field = wx.ComboBox(self, choices=gender_choices, style=wx.CB_READONLY)
		
		doctrine_choices = [d.name for d in doctrine_list]
		self.doctrine_select_field = wx.ComboBox(self, choices=doctrine_choices, style=wx.CB_READONLY)
		
		sincerity_choices = ['created it as a scam', 'was themselves somewhat doubtful', 'was a fervent believer themselves']
		self.sincerity_select_field = wx.ComboBox(self, choices=sincerity_choices, style=wx.CB_READONLY)
		
		fields = [self.the_select_field,
					self.cult_name_field,
					"was established in ",
					"datefield",
					"founded by",
					self.leader_name_field,
					self.gender_select_field,
					"(Born",
					"datefieldselector",
					")"
					"who",
					"bonus starting choices here?",
					"It was based on",
					self.doctrine_select_field,
					"beliefs, and it is believed the founder originally",
					self.sincerity_select_field]
		self.sizer = wx.WrapSizer(wx.HORIZONTAL)
		for f in fields:
			if type(f) == str:
				self.sizer.Add(wx.StaticText(frame, label=f))
			else:
				self.sizer.Add(f)
			self.sizer.Add((10,10))
		
		self.SetSizer(self.sizer)
		
if __name__ == "__main__":
	app = wx.App(False)
	frame = wx.Frame(None, wx.ID_ANY, "Main View", (200,200), (1400,800))
	sizer = wx.BoxSizer(wx.VERTICAL)
	
	setup_page = SetupPage(frame)
	
	#controller = LaborPoolView(frame, test_pool, cult)
	sizer.Add(setup_page, 0, wx.ALL)
	frame.SetSizer(sizer)
	frame.Show()
	app.MainLoop()