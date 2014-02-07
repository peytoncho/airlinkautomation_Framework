import wx
import fwupdate_controller

fwupdate_ctr = fwupdate_controller.FwupdateController()

class FwupdateApp(wx.App):
	def OnInit(self):
		
		frame = MainFrame("Fwupdate Automaiton GUI", (50, 60), (340, 450))
		frame.Show()
		self.SetTopWindow(frame)
		return True
	
class MainFrame(wx.Frame):
	def __init__(self, title, pos, size):
		wx.Frame.__init__(self, None, -1, title, pos, size)
		panel = wx.Panel(self, -1)
		self.box = wx.StaticBox(panel, -1, "Info", (20,20),(280,300))
		self.infoButton = wx.Button(self.box, -1, "MDT", pos=(90, 270))
		self.configButton = wx.Button(panel, -1, "Config", pos=(60, 350))
		self.runButton = wx.Button(panel, -1, "Run", pos=(160, 350))		
		
		#Call function to get all info
		self.fwupdate_map = fwupdate_ctr.loadGuiYmlFile()
		
		#sdt info
		self.deviceNameLabel = wx.StaticText(self.box, -1, "Device Name: ", (20,30))
		self.aleosFromLabel = wx.StaticText(self.box, -1, "ALEOS From: ", (20,60))
		self.aleosToLabel = wx.StaticText(self.box, -1, "ALEOS To: ", (20,90))
		self.testMethodLabel = wx.StaticText(self.box, -1, "Test method: ", (20,120))
		self.updateTypeLabel = wx.StaticText(self.box, -1, "Update Type: ", (20,150))
		
		self.deviceName = wx.StaticText(self.box, -1, self.fwupdate_map['DEVICE_NAME'], (100,30))
		self.aleosFrom  = wx.StaticText(self.box, -1, self.fwupdate_map['ALEOS_FROM'], (100,60))
		self.aleosTo = wx.StaticText(self.box, -1, self.fwupdate_map['ALEOS_TO'], (100,90))
		self.testMethod = wx.StaticText(self.box, -1, self.fwupdate_map['TEST_METHOD'], (100,120))
		self.updateType = wx.StaticText(self.box, -1, self.fwupdate_map['UPDATE_TYPE'], (100,150))		
		
		#mdt info
		self.mdtLabel = wx.StaticText(self.box, -1, "", (20,30))
		self.device1Label = wx.StaticText(self.box, -1, "", (20,60))
		self.device2Label = wx.StaticText(self.box, -1, "", (20,90))
		self.device3Label = wx.StaticText(self.box, -1, "", (20,120))
		self.device4Label = wx.StaticText(self.box, -1, "", (20,150))
		self.device5Label = wx.StaticText(self.box, -1, "", (20,180))
		self.mdt_aleosFromLabel = wx.StaticText(self.box, -1, "", (20,210))
		self.mdt_aleosToLabel = wx.StaticText(self.box, -1, "", (20,240))
		
		self.mdt = wx.StaticText(self.box, -1, "", (100,30))
		self.device1 = wx.StaticText(self.box, -1, "", (100,60))
		self.device2 = wx.StaticText(self.box, -1, "", (100,90))
		self.device3 = wx.StaticText(self.box, -1, "", (100,120))
		self.device4 = wx.StaticText(self.box, -1, "", (100,150))
		self.device5 = wx.StaticText(self.box, -1, "", (100,180))		
		self.mdt_aleosFrom = wx.StaticText(self.box, -1, "", (100,210))
		self.mdt_aleosTo = wx.StaticText(self.box, -1, "", (100,240))
						
		#set events to the components
		self.Bind(wx.EVT_BUTTON, self.onClickConfig, self.configButton)
		self.Bind(wx.EVT_BUTTON, self.onClickInfoChange, self.infoButton)
	
	def onClickRefresh(self,event):
		fwupdate_map = fwupdate_ctr.loadGuiYmlFile()
		
		
		fwupdate_ctr.getMapData(fwupdate_map, key)
	
		
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
			self.aleosFromLabel.SetLabelText("")
			self.aleosToLabel.SetLabelText("")
			self.deviceNameLabel.SetLabelText("")
			self.testMethodLabel.SetLabelText("")
			self.updateTypeLabel.SetLabelText("")
			self.aleosFrom.SetLabelText("")
			self.aleosTo.SetLabelText("")
			
			self.mdtLabel.SetLabelText("MDT: ")
			self.device1Label.SetLabelText("Device 1: ")
			self.device2Label.SetLabelText("Device 2: ")
			self.device3Label.SetLabelText("Device 3: ")
			self.device4Label.SetLabelText("Device 4: ")
			self.device5Label.SetLabelText("Device 5: ")
			self.mdt_aleosFromLabel.SetLabelText("ALEOS From: ")
			self.mdt_aleosToLabel.SetLabelText("ALEOS To: ")
			
			self.mdt.SetLabelText(self.fwupdate_map['MDT'])
			self.device1.SetLabelText(self.fwupdate_map['DEVICE_1'])
			self.device2.SetLabelText(self.fwupdate_map['DEVICE_2'])
			self.device3.SetLabelText(self.fwupdate_map['DEVICE_3'])
			self.device4.SetLabelText(self.fwupdate_map['DEVICE_4'])
			self.device5.SetLabelText(self.fwupdate_map['DEVICE_5'])
			self.mdt_aleosFrom.SetLabelText(self.fwupdate_map['MDT_ALEOS_FROM'])
			self.mdt_aleosTo.SetLabelText(self.fwupdate_map['MDT_ALEOS_TO'])			

		else:
			self.infoButton.SetLabel("MDT")
			self.mdtLabel.SetLabelText("")
			self.device1Label.SetLabelText("")
			self.device2Label.SetLabelText("")
			self.device3Label.SetLabelText("")
			self.device4Label.SetLabelText("")
			self.device5Label.SetLabelText("")
			self.mdt_aleosFromLabel.SetLabelText("")
			self.mdt_aleosToLabel.SetLabelText("")
			self.mdt.SetLabelText("")
			self.device1.SetLabelText("")
			self.device2.SetLabelText("")
			self.device3.SetLabelText("")
			self.device4.SetLabelText("")
			self.device5.SetLabelText("")
			self.mdt_aleosFrom.SetLabelText("")
			self.mdt_aleosTo.SetLabelText("")			
			
			self.deviceNameLabel.SetLabelText("Device Name: ")
			self.testMethodLabel.SetLabelText("Test method: ")
			self.updateTypeLabel.SetLabelText("Update Type: ")
			self.aleosFromLabel.SetLabelText("ALEOS From: ")
			self.aleosToLabel.SetLabelText("ALEOS To: ")
			self.aleosFrom.SetLabelText("")
			self.aleosTo.SetLabelText("")			
			
			self.deviceName.SetLabelText(self.fwupdate_map['DEVICE_NAME'])
			self.aleosFrom.SetLabelText(self.fwupdate_map['ALEOS_FROM'])
			self.aleosTo.SetLabelText(self.fwupdate_map['ALEOS_TO'])
			self.testMethod.SetLabelText(self.fwupdate_map['TEST_METHOD'])
			self.updateType.SetLabelText(self.fwupdate_map['UPDATE_TYPE'])

class ConfigFrame(wx.Frame):
	def __init__(self,title,pos,size):
		self.fwupdate_info_map = fwupdate_ctr.loadInfoYmlFile()
		self.device_list = self.fwupdate_info_map['DEVICE_LIST']
		self.aleos_list = self.fwupdate_info_map['ALEOS_LIST']

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
		self.Bind(wx.EVT_BUTTON,self.onClickCancel, self.cancleButton)
		

		
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
		self.device_choice = wx.Choice(sdtPanel, -1, (110, 27), choices=self.device_list)
		self.device_choice.SetSelection(0)
		
		#Test Method
		method_list = ["Single","Round Trip"]
		self.method_choice = wx.Choice(sdtPanel, -1, (110, 57), choices=method_list)
		self.method_choice.SetSelection(0)
		
		#ALEOS Choices		
		self.aleos_from_choice = wx.Choice(sdtPanel, -1, (110, 87), choices=self.aleos_list)
		self.aleos_to_choice = wx.Choice(sdtPanel, -1, (110, 117), choices=self.aleos_list)
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
		self.Bind(wx.EVT_CHOICE,self.onToggleMdt,self.mdtCheckBox)
		
		#Devices name		
		self.device1_choice = wx.Choice(mdtPanel, -1, (110, 57), choices=self.device_list)
		self.device2_choice = wx.Choice(mdtPanel, -1, (110, 87), choices=self.device_list)
		self.device3_choice = wx.Choice(mdtPanel, -1, (110, 117), choices=self.device_list)
		self.device4_choice = wx.Choice(mdtPanel, -1, (110, 147), choices=self.device_list)
		self.device5_choice = wx.Choice(mdtPanel, -1, (110, 177), choices=self.device_list)
		self.device1_choice.SetSelection(0)
#		self.device1_choice.Enable(False)
		self.device2_choice.SetSelection(0)
		self.device3_choice.SetSelection(0)
		self.device4_choice.SetSelection(0)
		self.device5_choice.SetSelection(0)
		 
		#ALEOS Choices
		self.aleos_from_choice = wx.Choice(mdtPanel, -1, (400, 27), choices=self.aleos_list)
		self.aleos_to_choice = wx.Choice(mdtPanel, -1, (400, 57), choices=self.aleos_list)
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
	
	
	def onToggleMdt(self,event):
		choice = self.mdtCheckBox.GetCurrentSelection()
		if choice is 0:
			self.device1_choice.Enable(False)
			self.device2_choice.Enable(False)
			self.device3_choice.Enable(False)
			self.device4_choice.Enable(False)
			self.device5_choice.Enable(False)
		else:
			self.device1_choice.Enable(True)
			self.device2_choice.Enable(True)
			self.device3_choice.Enable(True)
			self.device4_choice.Enable(True)
			self.device5_choice.Enable(True)			
		
	def onClickOK(self,event):
		fwupdate_map = fwupdate_ctr.loadGuiYmlFile()
		
		for field in self.fwupdate_info_map['GUI_FIELD_LIST']:
			fwupdate_ctr.setMapData(fwupdate_map, field, value)
		
		fwupdate_ctr.dumpYmlFile(fwupdate_map)
#		fwupdate_ctr.setMapData(fwupdate_map, key, value)
		
# 		str1 = self.device_choice.GetStringSelection()
# 		str2 = self.aleos_from_choice.GetStringSelection()
# 		str3 = self.aleos_to_choice.GetStringSelection()		
		self.Close()
	
	def onClickCancel(self,event):
		self.Close()
        
if __name__ == '__main__':
    app = FwupdateApp(False)
    app.MainLoop()
		