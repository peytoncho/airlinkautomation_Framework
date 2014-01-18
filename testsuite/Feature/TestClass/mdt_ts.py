import os
import time
import unittest
import sys
import basic_airlink
import selenium_utilities

ip_postfix = 1
test_area = "TestClass"
test_sub_area=""
tbd_config_map, testclass_config_map = basic_airlink.get_config_data(test_area,"")
device_name = tbd_config_map["DUTS"][0]

class MultipleDeviceTest(unittest.TestCase):    
    def setUp(self):
        if testclass_config_map["MDT"] == "YES":
            self.url = "HTTP://192.168.13."+str(ip_postfix)+":9191/"           
        else:
            self.url = tbd_config_map[device_name]["ACE_URL"]
        
        self.username = tbd_config_map[device_name]["USERNAME"]
        self.password = tbd_config_map[device_name]["PASSWORD"]
        self.se_ins = selenium_utilities.SeleniumAcemanager()
        
        self.driver = self.se_ins.login(self.url, self.username, self.password)
    
    def tearDown(self):
        if testclass_config_map["MDT"] == "YES":
            global ip_postfix
            ip_postfix+=1          
        
#        self.driver.close()
    
        
        
    def tc_fwupdate_GX400_MC8705_OSM(self):
        basic_airlink.cslog(self.url, "RED")
        basic_airlink.cslog("tc_fwupdate_GX400_MC8705_OSM", "RED")
    
    def tc_fwupdate_GX400_MC8705_ATT(self):
        basic_airlink.cslog(self.url, "GREEN")
        basic_airlink.cslog("tc_fwupdate_GX400_MC8705_ATT", "GREEN")
    
    def tc_fwupdate_GX400_MC8705_BEL(self):
        basic_airlink.cslog(self.url, "BLUE")
        basic_airlink.cslog("tc_fwupdate_GX400_MC8705_BEL", "BLUE")
    
    def tc_fwupdate_GX400_MC8705_TLS(self):
        basic_airlink.cslog(self.url, "YELLOW")
        basic_airlink.cslog("tc_fwupdate_GX400_MC8705_TLS", "YELLOW")
    
    def tc_fwupdate_GX410_MC8705_OSM(self):
        basic_airlink.cslog(self.url)
        basic_airlink.cslog("tc_fwupdate_GX410_MC8705_OSM")
       
    def tc_fwupdate_GX400_MC5728_VZW(self):
        pass
    
    def tc_fwupdate_GX440_MC7750_VZW(self):
        pass
    
    def tc_fwupdate_GX440_MC7700_ATT(self):
        basic_airlink.cslog(self.url, "RED")
        basic_airlink.cslog("tc_fwupdate_GX440_MC7700_ATT", "RED")
        self.se_ins.status_about_page(self.driver)
        pass
    
    def tc_fwupdate_GX400_MC5728_SPT(self):
        pass

    def tc_fwupdate_GX440_MC7700_OSM(self):
        pass

    def tc_fwupdate_ES440_MC7750_VZW(self):
        basic_airlink.cslog(self.url, "RED")
        basic_airlink.cslog("tc_fwupdate_ES440_MC7750_VZW", "RED")
        self.se_ins.status_about_page(self.driver)
        pass
    
    def tc_fwupdate_ES440_MC7700_ATT(self):
        pass

    def tc_fwupdate_ES440_MC7710_EMEA(self):
        basic_airlink.cslog(self.url, "RED")
        basic_airlink.cslog("tc_fwupdate_ES440_MC7710_EMEA", "RED")
        self.se_ins.status_about_page(self.driver)
        pass

    def tc_fwupdate_ES440_MC7700_OSM(self):
        pass   

    def tc_fwupdate_LS300_SL5011_VZW(self):
        basic_airlink.cslog(self.url, "RED")
        basic_airlink.cslog("tc_fwupdate_LS300_SL5011_VZW", "RED")
        self.se_ins.status_about_page(self.driver)
        pass 

    def tc_fwupdate_LS300_SL5011_SPT(self):
        pass 

    def tc_fwupdate_LS300_SL8090_ATT(self):
        pass 

    def tc_fwupdate_LS300_SL8090_BEL(self):
        pass 

    def tc_fwupdate_LS300_SL8092_OSM(self):
        basic_airlink.cslog(self.url, "RED")
        basic_airlink.cslog("tc_fwupdate_LS300_SL8092_OSM", "RED")
        self.se_ins.status_about_page(self.driver)
        pass 

