import wx

class FwupdateApp(wx.App):
	def OnInit(self):
		frame = MainFrame("Fwupdate Automaiton GUI", (50, 60), (340, 400))
		frame.Show()
		self.SetTopWindow(frame)
		return True
	
class MainFrame(wx.Frame):
	def __init__(self, title, pos, size):
		wx.Frame.__init__(self, None, -1, title, pos, size)
		panel = wx.Panel(self, -1)
		box = wx.StaticBox(panel, -1, "Info", (20,20),(280,250))
		self.infoButton = wx.Button(box, -1, "MDT", pos=(90, 220))
		self.configButton = wx.Button(panel, -1, "Config", pos=(60, 300))
		self.runButton = wx.Button(panel, -1, "Run", pos=(160, 300))		
		
		#sdt info
		self.deviceName = wx.StaticText(box, -1, "Device Name: ", (20,30))
		self.aleosFrom = wx.StaticText(box, -1, "ALEOS From: ", (20,60))
		self.aleosTo = wx.StaticText(box, -1, "ALEOS To: ", (20,90))
		self.testMethod = wx.StaticText(box, -1, "Test method: ", (20,120))
		self.updateType = wx.StaticText(box, -1, "Update Type: ", (20,150))
		
		#mdt info
		self.mdt = wx.StaticText(box, -1, "", (20,30))
		self.device1 = wx.StaticText(box, -1, "", (20,60))
		self.device2 = wx.StaticText(box, -1, "", (20,90))
		self.device3 = wx.StaticText(box, -1, "", (20,120))
		self.device4 = wx.StaticText(box, -1, "", (20,150))
		self.device5 = wx.StaticText(box, -1, "", (20,180))
		
		
		
		
		
		#set events to the components
		self.Bind(wx.EVT_BUTTON, self.onClickConfig, self.configButton)
		self.Bind(wx.EVT_BUTTON, self.onClickInfoChange, self.infoButton)
		
	def onClickConfig(self,event):
		frame = ConfigFrame("Configuration", (50,50), (200, 100))
		frame.Show()
		pass
	
	def onClickInfoChange(self,event):
		if self.infoButton.GetLabel() == "MDT":
			self.infoButton.SetLabel("SDT")
			
			self.deviceName.SetLabelText("")
			self.testMethod.SetLabelText("")
			self.updateType.SetLabelText("")
			
			self.mdt.SetLabelText("MDT: ")
			self.device1.SetLabelText("Device 1: ")
			self.device2.SetLabelText("Device 2: ")
			self.device3.SetLabelText("Device 3: ")
			self.device4.SetLabelText("Device 4: ")
			self.device5.SetLabelText("Device 5: ")
			
			self.aleosFrom.SetPosition((20,210))
			self.aleosTo.SetPosition((20,240))
			
		else:
			self.infoButton.SetLabel("MDT")
			self.mdt.SetLabelText("")
			self.device1.SetLabelText("")
			self.device2.SetLabelText("")
			self.device3.SetLabelText("")
			self.device4.SetLabelText("")
			self.device5.SetLabelText("")
			
			self.deviceName.SetLabelText("Device Name: ")
			self.testMethod.SetLabelText("Test method: ")
			self.updateType.SetLabelText("Update Type: ")

			self.aleosFrom.SetPosition((20,60))
			self.aleosTo.SetPosition((20,90))

class ConfigFrame(wx.Frame):
	def __init__(self,title,pos,size):
		wx.Frame.__init__(self, None, -1, title, pos, size)
		panel = wx.Panel(self,-1)
		
		self.okButton = wx.Button(panel, -1, "Config", pos=(60, 100))
		self.cancleButton = wx.Button(panel, -1, "Config", pos=(60, 150))
		
		
        
		
		
if __name__ == '__main__':
    app = FwupdateApp(False)
    app.MainLoop()
		