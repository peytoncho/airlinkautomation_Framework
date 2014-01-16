import os
import time
import unittest
import sys
import basic_airlink

ip_prefix = 1
test_area = "TestClass"
test_sub_area=""
tbd_config_map, testclass_config_map = basic_airlink.get_config_data(test_area,"")
device_name = tbd_config_map["DUTS"][0]

class MultipleDeviceTest(unittest.TestCase):    
    def setUp(self):
        if testclass_config_map["MDT"] == "YES":
            self.url = "192.168.13."+str(ip_prefix)+":9191"
            
        else:
            self.url = tbd_config_map[device_name]["ACE_URL"]
    
    def tearDown(self):
        global ip_prefix
        ip_prefix+=1
        
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
        pass
    
    def tc_fwupdate_GX400_MC5728_SPT(self):
        pass

    def tc_fwupdate_GX440_MC7700_OSM(self):
        pass

    def tc_fwupdate_ES440_MC7750_VZW(self):
        pass
    
    def tc_fwupdate_ES440_MC7700_ATT(self):
        pass

    def tc_fwupdate_ES440_MC7710_EMEA(self):
        pass

    def tc_fwupdate_ES440_MC7700_OSM(self):
        pass   

    def tc_fwupdate_LS300_SL5011_VZW(self):
        pass 

    def tc_fwupdate_LS300_SL5011_SPT(self):
        pass 

    def tc_fwupdate_LS300_SL8090_ATT(self):
        pass 

    def tc_fwupdate_LS300_SL8090_BEL(self):
        pass 

    def tc_fwupdate_LS300_SL8092_OSM(self):
        pass 

