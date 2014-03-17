import datetime
import logging
import telnetlib
import os
import sys
import time
import inspect
import unittest
import connectivity
import basic_airlink as ba
import selenium_utilities
import telnet_airlink
import services_airlink
import at_utilities

test_area = "Services"
test_sub_area="TELNET_SSH"
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_FRAMEWORK'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")

ba.append_sys_path()
tbd_config_map, telnetssh_config_map = ba.get_config_data(test_area,test_sub_area)


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
#        self.driver = self.services_ins.login(url, username, password)
        
        
    
    def tearDown(self):
#        self.driver.close()
        pass
             
    def tc_telnet_login_attempt_wrong_password(self):
        '''Change the value of Maximum login attempt to other number, to see if the wrong login attempt 
        can match the number set in the ACEManager 
        '''
        #self.services_ins.get_remote_login_server_mode(driver)
        #1, Navigate to services->telnet/ssh page, change the Maximum login attempt time, apply, reboot
        #2, Login with Telnet, try incorrect password for the times which was set in the previous step
        #3, verify the time after trying login
        
        
        
#         str1 = self.services_ins.get_remote_login_server_mode(self.driver)
#         str2 = self.services_ins.get_remote_login_server_port(self.driver)
#         str3 = self.services_ins.get_remote_login_server_port_timeout(self.driver)
#         str4 = self.services_ins.get_maximum_login_attempts(self.driver)
#         str5 = self.services_ins.get_telnet_ssh_echo(self.driver)
#         str6 = self.services_ins.get_ssh_status(self.driver)
        
        attempt_times = 3
        wrong_password = "12345"
#        self.services_ins.set_maximum_login_attempts(self.driver, attempt_times)
#        self.services_ins.apply_reboot(self.driver)
#        time.sleep(tbd_config_map[self.device]["REBOOT_TIMEOUT"]) 
        telnet_ins = telnet_airlink.TelnetAirlink(password = wrong_password)
        at_ins = at_utilities.AtCommands()

        

        for i in range(attempt_times+1): 
            ret = telnet_ins.connect_test()
        time.sleep(15)
        str1 = at_ins.get_device_id(telnet_ins)
        ba.cslog(str1)
        
#         ba.cslog(str1)
#         ba.cslog(str2)
#         ba.cslog(str3)
#         ba.cslog(str4)
#         ba.cslog(str5)
#         ba.cslog(str6)
        
        pass
    
    def tc_telnet_login_attempt_wrong_username(self):
        '''Change the value of Maximum login attempt to other number, to see if the wrong login attempt 
        can match the number set in the ACEManager 
        '''        
        #1, Navigate to services->telnet/ssh page, change the Maximum login attempt time, apply, reboot
        #2, Login with Telnet, try incorrect password for the times which was set in the previous step
        #3, verify the time after trying login
        pass
    
    def tc_telnet_change_ssh(self):
        '''Change the value of Maximum login attempt to other number, to see if the wrong login attempt 
        can match the number set in the ACEManager 
        '''
        #1, Navigate to services->telnet/ssh page, change to SSH mode, apply, reboot
        #2, Try telnet to device, ssh to device       
        pass  
    
    def tc_telnet_change_diff_port(self):
        '''Change the value of port, to see if the connection with new port is working 
        '''
        
        #1, Navigate to services->telnet/ssh page, change to SSH mode, apply, reboot
        #2, Try telnet to device with the new port 
        pass        
    
    
    
    
    
    
     