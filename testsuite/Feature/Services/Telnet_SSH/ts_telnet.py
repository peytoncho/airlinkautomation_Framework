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
import ssh_airlink
import telnetSsh_airlink
import at_utilities

test_area = "Services"
test_sub_area="TELNET_SSH"
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_FRAMEWORK'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")

ba.append_sys_path()
tbd_config_map, telnetssh_config_map = ba.get_config_data(test_area,test_sub_area)

class TsTelnet(unittest.TestCase):
    def setUp(self):
        #Pick info from config file        
        self.device = tbd_config_map["DUTS"][0]
        connectivity_ins = connectivity.Connectivity(device_name = self.device)
        conn_ins = connectivity_ins.connection_types()
        self.ip_addr = connectivity_ins.address()
        self.url = connectivity_ins.get_url()       
        self.username = tbd_config_map[self.device]["USERNAME"]
        self.password = tbd_config_map[self.device]["PASSWORD"]
        #Ping device
        ret = os.system('ping '+self.ip_addr)
        if ret == 0:
            ba.cslog("DUT ready", "GREEN") 
        else:
            ba.cslog("DUT not ready", "RED")
            self.fail("DUT not ready")

        #init and login
        self.telnetssh_ins = telnetSsh_airlink.TelnetSshAirlink()
#        self.driver = self.telnetssh_ins.login(self.url, self.username, self.password)
           
    def tearDown(self):
        try:
            self.driver.close()
        except:
            pass
        pass
             
    def tc_telnet_login_attempt_wrong_password(self):
        '''Change the value of Maximum login attempt to other number, to see if the wrong login attempt 
        can match the number set in the ACEManager 
        '''
        #self.telnetssh_ins.get_remote_login_server_mode(driver)
        #1, Navigate to services->telnet/ssh page, change the Maximum login attempt time, apply, reboot
        #2, Login with Telnet, try incorrect password for the times which was set in the previous step
        #3, verify the time after trying login
               
        attempt_times = 3
        wrong_password = "12345"
#        self.telnetssh_ins.set_maximum_login_attempts(self.driver, attempt_times)
#        self.telnetssh_ins.apply_reboot(self.driver)
#        time.sleep(tbd_config_map[self.device]["REBOOT_TIMEOUT"]) 
        telnet_ins = telnet_airlink.TelnetAirlink(password = wrong_password)
        at_ins = at_utilities.AtCommands()
        for i in range(attempt_times+1): 
            ret = telnet_ins.connect_test()
        time.sleep(15)
        str1 = at_ins.get_device_id(telnet_ins)
        ba.cslog(str1)        
        pass
    
    def tc_telnet_login_attempt_wrong_username(self):
        '''Change the value of Maximum login attempt to other number, to see if the wrong login attempt 
        can match the number set in the ACEManager 
        '''        
        #1, Navigate to services->telnet/ssh page, change the Maximum login attempt time, apply, reboot
        #2, Login with Telnet, try incorrect password for the times which was set in the previous step
        #3, verify the time after trying login
        pass
    
    def tc_local_ssh_as_root(self):
        ssh_ins = ssh_airlink.SshAirlink(username="root", password="v3r1fym3")
        attempt_time = 10
        while not ssh_ins.connect():
            ba.cslog("Connection failed", "RED")
        cmd = "ls"
        ret = ssh_ins.command(cmd)
        self.assertIn("aleos", ret[1], "Verify failed")
        ba.cslog("Verify: Pass", "GREEN")
        
#===============================================================================
# Local, UI
#===============================================================================
    
    def tc_local_ui_telnet_change_ssh(self):
        '''Change the value of Maximum login attempt to other number, to see if the wrong login attempt 
        can match the number set in the ACEManager 
        '''
        #1, Navigate to services->telnet/ssh page, change to SSH mode, apply, reboot
        self.driver = self.telnetssh_ins.login(self.url, self.username, self.password)
        self.telnetssh_ins.set_remote_login_server_mode(self.driver, "SSH")
        self.telnetssh_ins.apply_reboot(self.driver)
        
        time.sleep(tbd_config_map[self.device]["REBOOT_TIMEOUT"])
        
        #2, Try telnet to device, ssh to device
        telnet_ins = telnet_airlink.TelnetAirlink()
        ssh_ins = ssh_airlink.SshAirlink(port=2332)
        
        telnet_flag = True
        ssh_flag = True
        
        if not telnet_ins.connect():
            ba.cslog("Telnet access failed..", "RED")
            telnet_flag = False
        else:
            ba.cslog("Telnet access success..", "GREEN")
        
        if not ssh_ins.connect():
            ba.cslog("SSH access failed", "RED")       
            ssh_flag = False
        else:
            ba.cslog("SSH access success..", "GREEN")
               
        if not (telnet_flag == False and ssh_flag == True):
            ba.cslog("Verify: Failed", "RED")
            self.fail("Verify: Failed")
        else:
            ba.cslog("Verify: Pass")
        #3, Change back to Telnet mode
        ba.cslog("Change back to Telnet mode")
        self.telnetssh_ins.set_remote_login_server_mode(self.driver, "Telnet")
        self.telnetssh_ins.apply_reboot(self.driver)
        self.driver.close()
    
    def tc_local_ui_telnet_change_diff_port(self):
        '''Change the value of port, to see if the connection with new port is working 
        '''
        #1, Navigate to services->telnet/ssh page, change to SSH mode, apply, reboot
        self.driver = self.telnetssh_ins.login(self.url, self.username, self.password)
        port = telnetssh_config_map["CONFIG_PORT"]
        origin_port = tbd_config_map[self.device]["CONNECTION_PORT"]
        ba.cslog("Change to port: "+str(port))
        self.telnetssh_ins.set_remote_login_server_port(self.driver, port)
        self.telnetssh_ins.apply_reboot(self.driver)
        time.sleep(tbd_config_map[self.device]["REBOOT_TIMEOUT"])
        ret = os.system('ping '+self.ip_addr)
        while ret!=0:
            ret = os.system('ping '+self.ip_addr)     
        
        ba.cslog("Device up...")
        
        #2, Try telnet to device with the new port
        telnet_ins = telnet_airlink.TelnetAirlink(port=int(port))
        if not telnet_ins.connect():
            ba.cslog("Telnet access failed..", "RED")
            self.fail("Telnet access failed..")
        else:
            ba.cslog("Telnet access success", "GREEN")
        
        ba.cslog("Change back to original port: "+str(origin_port))
        self.driver = self.telnetssh_ins.login(self.url, self.username, self.password)
        self.telnetssh_ins.set_remote_login_server_port(self.driver, origin_port)
        self.telnetssh_ins.apply_reboot(self.driver)
        time.sleep(tbd_config_map[self.device]["REBOOT_TIMEOUT"])
        self.driver.close()
        ba.cslog("Test case Done", "BLUE")                 
                
    def tc_local_ui_ssh_change_diff_port(self):
        '''Change the value of port, to see if the connection with new port is working 
        '''
        #1, Navigate to services->telnet/ssh page, change to SSH mode, apply, reboot
        
        port = telnetssh_config_map["CONFIG_PORT"]
        origin_port = tbd_config_map[self.device]["CONNECTION_PORT"]
        self.driver = self.telnetssh_ins.login(self.url, self.username, self.password)
        self.telnetssh_ins.set_remote_login_server_mode(self.driver, "SSH")
        ba.cslog("Change to port: "+str(port))
        self.telnetssh_ins.set_remote_login_server_port(self.driver, port)
        self.telnetssh_ins.apply_reboot(self.driver)
        self.driver.close()
        time.sleep(tbd_config_map[self.device]["REBOOT_TIMEOUT"])
        
        ret = os.system('ping '+self.ip_addr)
        while ret!=0:
            ret = os.system('ping '+self.ip_addr)
        ba.cslog("Device up...")
        
        #2, Try telnet to device with the new port
        telnet_ins = telnet_airlink.TelnetAirlink(port=int(port))
        if not telnet_ins.connect():
            ba.cslog("SSH access failed..", "RED")
            self.fail("Telnet access failed..")
        else:
            ba.cslog("SSH access success", "GREEN")
        
        ba.cslog("Change back to original port"+str(origin_port))
        self.driver = self.telnetssh_ins.login(self.url, self.username, self.password)
        self.telnetssh_ins.set_remote_login_server_port(self.driver, origin_port)
        self.telnetssh_ins.apply_reboot(self.driver)
        self.driver.close()
        time.sleep(tbd_config_map[self.device]["REBOOT_TIMEOUT"])
        self.driver.close()
        ba.cslog("Test case Done", "BLUE")
        
    def tc_local_ui_ssh_make_new_key(self):
        ssh_ins = ssh_airlink.SshAirlink(port = 2332)
        self.telnetssh_ins.click_make_ssh_key(driver, value)
        pass
    
    def tc_local_ui_telnet_echo_disable(self):
        pass

    def tc_local_ui_ssh_echo_disable(self):
        ssh_ins = ssh_airlink.SshAirlink(port=22)
        if not ssh_ins.connect():
            ba.cslog("Connection fail", "RED")
        
        ba.cslog(str(ssh_ins.command("ati")))
        
        pass
    
    def tc_local_ui_ssh_check_state(self):
        remote_svr_mode = self.telnetssh_ins.get_remote_login_server_mode(self.driver)
        ba.cslog(remote_svr_mode, "BLUE")
        if remote_svr_mode != "SSH":
            ba.cslog("Remote server mode is not SSH, change to SSH now...", "RED")
            self.telnetssh_ins.set_remote_login_server_mode(self.driver, "SSH")
            self.telnetssh_ins.apply_reboot(self.driver)
            time.sleep(tbd_config_map[self.device]["REBOOT_TIMEOUT"])
        
        ssh_ins = ssh_airlink.SshAirlink(port = 2332)
        status = self.telnetssh_ins.get_ssh_status(self.driver)
        self.telnetssh_ins.refresh(self.driver)
        while status == "" or "not" in status:
            self.telnetssh_ins.refresh(self.driver)
            status = self.telnetssh_ins.get_ssh_status(self.driver)
            
        ba.cslog(status, "BLUE")
    
    
#===============================================================================
# Local, AT Command
#===============================================================================    
    def tc_local_at_telnet_change_ssh(self):
        pass
    
    def tc_local_at_telnet_change_diff_port(self):
        pass
    
    def tc_local_at_ssh_change_diff_port(self):
        pass
    
#===============================================================================
# OTA, AT Command
#===============================================================================    
    def tc_ota_at_ssh_change_diff_port(self):
        pass
    
    def tc_ota_at_telnet_change_diff_port(self):
        pass
    
    def tc_ota_at_telnet_change_ssh(self):
        pass    

#===============================================================================
# OTA, UI
#=============================================================================== 
    def tc_ota_ui_ssh_change_diff_port(self):
        pass
    
    def tc_ota_ui_telnet_change_diff_port(self):
        pass
    
    def tc_ota_ui_telnet_change_ssh(self):
        pass
    
    