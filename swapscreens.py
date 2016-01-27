import wx

class MainFrame ( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        self.SetSizer( bSizer1 )
        self.Layout()

        # self.panelOne = panel_one(self)
        # self.panelTwo = panel_two(self)
        # self.panelTwo.Hide()
        self.Centre( wx.BOTH )
    def __del__( self ):
        pass

class panel_one ( wx.Panel ):
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.TAB_TRAVERSAL )
        bSizer5 = wx.BoxSizer( wx.VERTICAL )
        self.m_button2 = wx.Button( self, wx.ID_ANY, u"panel 1 button", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_button2, 0, wx.ALL, 5 )
        self.SetSizer( bSizer5 )
        self.Layout()
        # Connect Events
        self.m_button2.Bind( wx.EVT_BUTTON, self.changeIntroPanel )
    def __del__( self ):
        pass
    # Virtual event handlers, overide them in your derived class
    def changeIntroPanel( self, event ):
        event.Skip()

class panel_two ( wx.Panel ):
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.TAB_TRAVERSAL )
        bSizer5 = wx.BoxSizer( wx.VERTICAL )
        self.m_button2 = wx.Button( self, wx.ID_ANY, u"panel 2 button ", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_button2, 0, wx.ALL, 5 )
        self.SetBackgroundColour(wx.CYAN)
        self.SetSizer( bSizer5 )
        self.Layout()
        # Connect Events
        self.m_button2.Bind( wx.EVT_BUTTON, self.changeIntroPanel )

    def __del__( self ):
        pass
        # Virtual event handlers, overide them in your derived class
    def changeIntroPanel( self, event ):
        event.Skip()
		
class MainApp(MainFrame):
    def __init__(self, parent):
        MainFrame.__init__(self, parent)

        self.panelOne = Panel1(self)
        self.panelTwo = Panel2(self)
        self.panelTwo.Hide()

class Panel1(panel_one):
    def __init__(self, parent):
        panel_one.__init__(self, parent)
        self.parent = parent

    def changeIntroPanel( self, event ):
        if self.IsShown():
            self.parent.SetTitle("Panel Two Showing")
            self.Hide()
            self.parent.panelTwo.Show()


class Panel2(panel_two):
    def __init__(self, parent):
        panel_two.__init__(self, parent)
        self.parent = parent

    def changeIntroPanel( self, event ):
        if self.IsShown():
            self.parent.SetTitle("Panel One Showing")
            self.parent.panelOne.Show()
            self.Hide()

def main():
    app = wx.App()
    window = MainApp(None)
    window.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()