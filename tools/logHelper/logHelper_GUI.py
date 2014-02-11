import wx

class LogHelperApp(wx.App):
    def OnInit(self):    
        frame = MainFrame("Log Helper V1.0", (50, 60), (300, 400))
        frame.Show()
        self.SetTopWindow(frame)
        return True
    
class MainFrame(wx.Frame):
    def __init__(self, title, pos, size):
        wx.Frame.__init__(self, None, -1, title, pos, size)
        panel = wx.Panel(self, -1)
        self.dumpOptionBox = wx.StaticBox(panel, -1, "Dump Option", (12,20),(260,90))
        self.settingBox = wx.StaticBox(panel, -1, "Setting", (12,110),(260,150))
        
        self.dumpFromDeviceRadio = wx.RadioButton(self.dumpOptionBox, -1, "Dump From Device ", (20, 25))
        self.dumpFromLogTxtRadio = wx.RadioButton(self.dumpOptionBox, -1, "Dump From Log Txt ", (20, 50))
        
        self.dumpAllCheckBox = wx.CheckBox(self.settingBox, -1, "Dump All", (19, 25))
        
        
        self.timeCheckBox = wx.CheckBox(self.settingBox, -1, "Time: ", (19, 52))
        self.wordCheckBox = wx.CheckBox(self.settingBox, -1, "Word: ", (19, 80))
        self.timeTextCtrl = wx.TextCtrl(self.settingBox, -1, "20", (77, 52), (40,20))
        self.wordTextCtrl = wx.TextCtrl(self.settingBox, -1, "", (77, 80), (150,20))
        
        self.dumpButton = wx.Button(panel, -1, "Dump!", (100,280), (80,50))
#         timeCheckBoxLabel = wx.StaticText(self.panel, -1, "Word: ", (60, 40))
#         dumpAllCheckBoxLabel = wx.StaticText(self.panel, -1, "Dump All ", (60, 80))
        


if __name__ == "__main__":
    app = LogHelperApp(False)
    app.MainLoop()