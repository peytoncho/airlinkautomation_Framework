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
		frame = ConfigFrame("Configuration", (50,50), (700, 400))
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
		panel = wx.Panel(self)
		tabNB = wx.Notebook(panel,-1,size=(680, 320), style=wx.BK_DEFAULT)
		
		sdtPanel = self.makeSdtConfigPage(tabNB)
		mdtPanel = self.makeMdtConfigPage(tabNB)
		ftpPanel = self.makeFtpConfigPage(tabNB)		
		tabNB.AddPage(sdtPanel,"SDT")
		tabNB.AddPage(mdtPanel,"MDT")
		tabNB.AddPage(ftpPanel,"FTP")
		
		self.okButton = wx.Button(panel, -1, "OK", pos=(450, 330))
		self.cancleButton = wx.Button(panel, -1, "Cancel", pos=(550, 330))
		
		self.Bind(wx.EVT_BUTTON, self.onClickOK, self.okButton)
		
	def makeSdtConfigPage(self,parent):
		sdtPanel = wx.Panel(parent)
		
		#Labels
		sdt_deviceName = wx.StaticText(sdtPanel, -1, "Device Name: ", (20,30))
		sdt_testMethod = wx.StaticText(sdtPanel, -1, "Test method: ", (20,60))
		sdt_aleosFrom = wx.StaticText(sdtPanel, -1, "ALEOS From: ", (20,90))
		sdt_aleosTo = wx.StaticText(sdtPanel, -1, "ALEOS To: ", (20,120))		
		sdt_updateType = wx.StaticText(sdtPanel, -1, "Update Type: ", (20,150))
		
		#Control components
		
		#Devices name
		Device_list = ["DUT_GX400_MC8705_OSM",
               "DUT_GX400_MC8705_ATT",
               "DUT_GX400_MC8705_BEL",
               "DUT_GX400_MC8705_TLS",
               "DUT_GX400_MC8705_OSM"]
		self.device_choice = wx.Choice(sdtPanel, -1, (110, 27), choices=Device_list)
		self.device_choice.SetSelection(0)
		
		#Test Method
		method_list = ["Single","Round Trip"]
		self.method_choice = wx.Choice(sdtPanel, -1, (110, 57), choices=method_list)
		self.method_choice.SetSelection(0)
		
		#ALEOS Choices
		ALEOS_list = ["4.3.3a.014","4.3.4.009","4.3.5.008","4.3.5.009","4.3.5.010"]
		self.aleos_from_choice = wx.Choice(sdtPanel, -1, (110, 87), choices=ALEOS_list,)
		self.aleos_to_choice = wx.Choice(sdtPanel, -1, (110, 117), choices=ALEOS_list)
		self.aleos_from_choice.SetSelection(0)
		self.aleos_to_choice.SetSelection(0)
		
		return sdtPanel
	
	def makeMdtConfigPage(self,parent):
		mdtPanel = wx.Panel(parent)
		
		#Labels
		mdt_mdtSwitch = wx.StaticText(mdtPanel, -1, "MDT: ", (20,30))
		mdt_device1 = wx.StaticText(mdtPanel, -1, "Device 1: ", (20,60))
		mdt_device2 = wx.StaticText(mdtPanel, -1, "Device 2: ", (20,90))
		mdt_device3 = wx.StaticText(mdtPanel, -1, "Device 3: ", (20,120))
		mdt_device4 = wx.StaticText(mdtPanel, -1, "Device 4: ", (20,150))
		mdt_device5 = wx.StaticText(mdtPanel, -1, "Device 5: ", (20,180))
		mdt_aleosFrom = wx.StaticText(mdtPanel, -1, "ALEOS From: ", (320,30))
		mdt_aleosTo = wx.StaticText(mdtPanel, -1, "ALEOS To: ", (320,60))
		mdt_roundtripTimes = wx.StaticText(mdtPanel, -1, "RoundTrip Times: ", (320,90))
		
		#MDT Checkbox
		mdt_switch = ["NO","YES"]
		self.mdtCheckBox = wx.Choice(mdtPanel, -1, (110, 27), choices=mdt_switch)
		self.mdtCheckBox.SetSelection(0)
		
		#Devices name
		Device_list = ["DUT_GX400_MC8705_OSM",
               "DUT_GX400_MC8705_ATT",
               "DUT_GX400_MC8705_BEL",
               "DUT_GX400_MC8705_TLS",
               "DUT_GX400_MC8705_OSM"]
		
		self.device1_choice = wx.Choice(mdtPanel, -1, (110, 57), choices=Device_list)
		self.device2_choice = wx.Choice(mdtPanel, -1, (110, 87), choices=Device_list)
		self.device3_choice = wx.Choice(mdtPanel, -1, (110, 117), choices=Device_list)
		self.device4_choice = wx.Choice(mdtPanel, -1, (110, 147), choices=Device_list)
		self.device5_choice = wx.Choice(mdtPanel, -1, (110, 177), choices=Device_list)
		self.device1_choice.SetSelection(0)
#		self.device1_choice.Enable(False)
		self.device2_choice.SetSelection(0)
		self.device3_choice.SetSelection(0)
		self.device4_choice.SetSelection(0)
		self.device5_choice.SetSelection(0)
		 
		#ALEOS Choices
		ALEOS_list = ["4.3.3a.014","4.3.4.009","4.3.5.008","4.3.5.009","4.3.5.010"]
		self.aleos_from_choice = wx.Choice(mdtPanel, -1, (400, 27), choices=ALEOS_list,)
		self.aleos_to_choice = wx.Choice(mdtPanel, -1, (400, 57), choices=ALEOS_list)
		self.aleos_from_choice.SetSelection(0)
		self.aleos_to_choice.SetSelection(0)
		
			
		
		return mdtPanel
	
	def makeFtpConfigPage(self,parent):
		ftpPanel = wx.Panel(parent)
		
		#Labels
		ftp_username = wx.StaticText(ftpPanel, -1, "FTP username: ", (20,30))
		ftp_password = wx.StaticText(ftpPanel, -1, "FTP password: ", (20,60))
		
		#input fields
		self.ftp_username_field = wx.TextCtrl(ftpPanel, -1, "",(110,30),(175, -1))
		self.ftp_password_field = wx.TextCtrl(ftpPanel, -1, "",(110,60),(175, -1),style=wx.TE_PASSWORD)
			
		return ftpPanel
	
	def onClickOK(self,event):
# 		str1 = self.device_choice.GetStringSelection()
# 		str2 = self.aleos_from_choice.GetStringSelection()
# 		str3 = self.aleos_to_choice.GetStringSelection()		
		self.Close()
		pass
	
	def onClickCancel(self,event):
		pass
        
if __name__ == '__main__':
    app = FwupdateApp(False)
    app.MainLoop()
		