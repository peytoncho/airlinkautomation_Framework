import os
import time
import unittest
import sys

class MultipleDeviceTest(unittest.TestCase):    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def tc_fwupdate_GX400_MC8705_OSM(self):
        basic_airlink.cslog("tc_fwupdate_GX400_MC8705_OSM", "RED")
    
    def tc_fwupdate_GX400_MC8705_ATT(self):
        basic_airlink.cslog("tc_fwupdate_GX400_MC8705_ATT", "GREEN")
    
    def tc_fwupdate_GX400_MC8705_BEL(self):
        basic_airlink.cslog("tc_fwupdate_GX400_MC8705_BEL", "BLUE")
    
    def tc_fwupdate_GX400_MC8705_TLS(self):
        basic_airlink.cslog("tc_fwupdate_GX400_MC8705_TLS", "YELLOW")
    
    def tc_fwupdate_GX410_MC8705_OSM(self):
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

