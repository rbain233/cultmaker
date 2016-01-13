import wx
from mvc import *
from laborpool import * 
from person import * 
from cult import *

# an observable calls callback functions when the data has changed
#o = Observable()
#def func(data):
# print "hello", data
#o.addCallback(func)
#o.set(1)
# --| "hello", 1

class Model:
	def __init__(self):
		self.myMoney = Observable(0)

	def empty(self):
		self.myMoney.set(0)

	def addMoney(self, value):
		self.myMoney.set(self.myMoney.get() + value)

	def removeMoney(self, value):
		self.myMoney.set(self.myMoney.get() - value)
	
	def maxMoney(self):
		self.myMoney.set(75)

class View(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Main View")
        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, label="My Money")
        ctrl = wx.TextCtrl(self)
        sizer.Add(text, 0, wx.EXPAND | wx.ALL)
        sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL)
        ctrl.SetEditable(False)
        self.SetSizer(sizer)
        self.moneyCtrl = ctrl

    def SetMoney(self, money):
        self.moneyCtrl.SetValue(str(money))


class ChangerWidget(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Main View")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.add = wx.Button(self, label="Add Money")
        self.remove = wx.Button(self, label="Remove Money")
        sizer.Add(self.add, 0, wx.EXPAND | wx.ALL)
        sizer.Add(self.remove, 0, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)

class Controller:
    def __init__(self, app):
        self.model = Model()
        self.view1 = View(None)
        self.view2 = ChangerWidget(self.view1)
        self.MoneyChanged(self.model.myMoney.get())
        self.view2.add.Bind(wx.EVT_BUTTON, self.AddMoney)
        self.view2.remove.Bind(wx.EVT_BUTTON, self.RemoveMoney)
        self.model.myMoney.addCallback(self.MoneyChanged)
        self.view1.Show()
        self.view2.Show()

    def AddMoney(self, evt):
        self.model.addMoney(10)

    def RemoveMoney(self, evt):
        self.model.removeMoney(10)

    def MoneyChanged(self, money):
        self.view1.SetMoney(money)


		
class LaborPoolControl:
	def __init__(self, frame, labor_pool, cult):
		self.model = labor_pool
		self.money_view2 = wx.TextCtrl(frame) #For some reason, if this is further down in the code, MoneyChanged() won't acknowledge money_view2 exists.  Very aggravating.
		self.money_view2.SetEditable(False)
		self.money_view2.ChangeValue("XXX")
		sizer = wx.WrapSizer(wx.HORIZONTAL)
		text = wx.StaticText(frame, label="Generic Labor Pool: ")
		sizer.Add(text, 0, wx.EXPAND | wx.ALL)
		self.emptyBtn = wx.Button(frame, label="0", style=wx.BU_EXACTFIT)
		self.maxBtn = wx.Button(frame, label="max", style=wx.BU_EXACTFIT)
		sizer.Add(self.emptyBtn, 0, wx.EXPAND | wx.ALL)
		self.remove = wx.Button(frame, label="-", style=wx.BU_EXACTFIT)
		sizer.Add(self.remove, 0, wx.EXPAND | wx.ALL)
		self.money_view = wx.TextCtrl(frame)
		self.money_view.SetEditable(False)
		sizer.Add(self.money_view, 0, wx.EXPAND | wx.ALL)
		self.add = wx.Button(frame, label="+", style=wx.BU_EXACTFIT)
		sizer.Add(self.add, 0, wx.EXPAND | wx.ALL)
		self.emptyBtn.Bind(wx.EVT_BUTTON, self.setToZero)
		self.add.Bind(wx.EVT_BUTTON, self.AddMoney)
		sizer.Add(self.maxBtn, 0, wx.EXPAND | wx.ALL)
		self.remove.Bind(wx.EVT_BUTTON, self.RemoveMoney)
		self.maxBtn.Bind(wx.EVT_BUTTON, self.MaxMoney)
		self.model.myMoney.addCallback(self.MoneyChanged)
		self.MoneyChanged(self.model.myMoney.get())
		big_sizer  = wx.BoxSizer(wx.VERTICAL)
		sizer2 = wx.WrapSizer(wx.HORIZONTAL)
		text = wx.StaticText(frame, label="Unassigned people: ")
		sizer2.Add(text, 0, wx.EXPAND | wx.ALL)
		sizer2.Add(self.money_view2, 0, wx.EXPAND | wx.ALL)
		big_sizer.Add(sizer, 0)
		big_sizer.Add(sizer2, 0)
		frame.SetSizer(big_sizer)
		frame.Show()
		
	def setToZero(self, evt):
		self.model.empty()

	def AddMoney(self, evt):
		self.model.addMoney(10)
	
	def RemoveMoney(self, evt):
		self.model.removeMoney(10)
	
	def MaxMoney(self, evt):
		self.model.maxMoney()
		
	def MoneyChanged(self, money):
		self.money_view2.ChangeValue(str(75-money))
		self.money_view.ChangeValue(str(money))
		self.maxBtn.SetLabel("75")
		

all_people = []
def countUnassignedPeople():
	c = 0
	for person in all_people:
		if person.department:
			continue
		else:
			c += 1
	return c

if __name__ == "__main__":
	all_people = []
	test_pool = LaborPool()
	cult = Cult()
	for ii in range(25):
		all_people.append(Person())
	
	app = wx.App(False)
	frame = wx.Frame(None, wx.ID_ANY, "Main View", (200,200), (500,400))
	controller = LaborPoolControl(frame, test_pool, cult)
	app.MainLoop()
	