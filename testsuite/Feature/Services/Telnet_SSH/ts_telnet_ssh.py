import datetime
import logging
import os
import sys
import time
import unittest
import connectivity
import basic_airlink as ba
import selenium_utilities
import telnet_airlink
import services_airlink

test_area = "Services"
test_sub_area="EMAIL"
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_FRAMEWORK'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")

ba.append_sys_path()
tbd_config_map, email_config_map = ba.get_config_data(test_area,test_sub_area)


class TsTelnetSsh(unittest.TestCase):
    def setUp(self):
        #Pick info from config file
        self.device = tbd_config_map["DUTS"][0]
        connectivity_ins = connectivity.Connectivity(device_name = self.device)
        url = connectivity_ins.get_url()
        ip_addr = connectivity_ins.address()
        username = tbd_config_map[self.device]["USERNAME"]
        password = tbd_config_map[self.device]["PASSWORD"]
        
        
#        conn_ins = connectivity_ins.connection_types()
        #Ping device
        ret = os.system('ping '+ip_addr)
        if ret == 0:
            ba.cslog("DUT ready", "GREEN") 
        else:
            ba.cslog("DUT not ready", "RED")
            self.fail("DUT not ready")

        #init and login
        self.services_ins = services_airlink.TelnetSshAirlink()
        self.driver = self.services_ins.login(url, username, password)

    
    def tearDown(self):
        self.driver.close()
        
        
    def tc_telnetssh_1(self):
        self.services_ins.get_remote_login_server_mode(driver)
        
        pass
    
    def tc_telnetssh_2(self):
        pass
    
    def tc_telnetssh_3(self):
        pass   