################################################################################
#
# This module automates RSSI test case 
# Company: Sierra Wireless
# Time   : Oct 2nd, 2013
# Author : Airlink 
#
################################################################################

from selenium import webdriver   
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import selenium.webdriver.remote.webdriver

import time
import unittest
import sys,os
import proxy_airlink,ping_airlink

airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")
sys.path.append(".")

import basic_airlink
basic_airlink.append_sys_path()

import ftp_airlink
import at_utilities
import selenium_utilities
import callbox_utilities
import datetime
import connectivity
import msciids

tbd_config_map, wan_config_map = basic_airlink.get_config_data("WAN","")
       
class TsWanPtband(unittest.TestCase):
    ''' This test suite automates Band test case 
    '''
                                                              
    def setUp(self):
        ''' the test runner will run that method prior to each test
        '''
        
        self.conn_ins = connectivity.Connectivity() 
        self.fail_flag=0            
        # step: check if devices ready    
        basic_airlink.slog("Step: Check if testbed is READY")
        if not self.conn_ins.testbed_ready(): 
            self.fail_flag += 1
         
        self.device_name = tbd_config_map["DUTS"][0]
              
        # step: check Firefox 
        basic_airlink.slog("Please close Firefox if required \n")
         
        self.se_ins = selenium_utilities.SeleniumAcemanager()
        self.at_ins = at_utilities.AtCommands()   
        self.cb_ins = callbox_utilities.AnritsuMD8475A()
         
        # step: check if callbox/network simulation is ready  
#        if not self.cb_ins.callbox_ready(tbd_config_map, throughput_config_map):
#            self.fail_flag += 1
         
        basic_airlink.slog("Step:  Connect DUT and generate connection instance by Telnet or USB or Serial or WiFi or OTA")
        self.connect_instance=self.conn_ins.connection_types()
        if not self.connect_instance.connect(): 
            basic_airlink.slog("Problem: Testbed not ready yet")
             
        self.fail_flag = 0
         
        # step: login to Ace Manager 
        basic_airlink.slog("Step: Login to ACEmanager")
        ace_manager_url = self.conn_ins.get_url()
        self.driver = self.se_ins.login(ace_manager_url, \
                                        tbd_config_map[self.device_name]["USERNAME"], \
                                        tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"]) 
   
    def tc_2g_only(self):
        '''
        '''
        self.se_ins.wan_page(self.driver)
#         self.se_ins.set_band(self)
#         Equal to 2G only
        self.se_ins.apply(self.driver)
        self.se_ins.apply_reboot(self.driver)
          
        self.cb_ins.launch_smart_studio()   
        
        self.cb_ins.load_sim_param_file("D:\\WnsProxy\\SimParam_att_W1G1.wnssp")
        self.cb_ins.load_cell_param_file("D:\\WnsProxy\\CellParam_2_cells.wnscp")

        self.cb_ins.load_sim_param_file("D:\\WnsProxy\\SimParam_att_L1G1.wnssp")
        self.cb_ins.load_cell_param_file("D:\\WnsProxy\\CellParam_2_cells.wnscp")
        
        self.cb_ins.load_sim_param_file("D:\\WnsProxy\\SimParam_att_L1W1.wnssp")
        self.cb_ins.load_cell_param_file("D:\\WnsProxy\\CellParam_2_cells.wnscp")
        
        self.cb_ins.start_simulator()
        
        self.se_ins.status_page(self.driver)
        time.sleep(20)
        
        self.cb_ins.read_RSSI(self.se_ins,self.driver)
         
        verify_rssi_check = self.verify_RSSI(self.changed_rssi1)
        basic_airlink.slog("Verify: "+ str(verify_rssi_check))
          
        self.cb_ins.change_RSSI(self.changed_rssi2)
          
        self.cb_ins.read_RSSI(self.se_ins,self.driver)  
          
        verify_rssi_check = self.verify_RSSI(self.changed_rssi2)
        basic_airlink.slog("Verify: "+ str(verify_rssi_check))
        
        self.test_remote()
         
        self.cb_ins.stop_simulator()
 
        
    def verify_ecio(self, ):
        error_list = [-5,-4,-3,-2,-1,0,1,2,3,4,5]
        ret = False
        acmgr_rssi = self.se_ins.get_network_rssi(self.driver)
        for i in range(0,len(error_list)):
            if int(acmgr_rssi) == int(changed_rssi) + error_list[i] - 15:
                ret = True
                break
 
        return ret
    
    def test_remote(self):
        self.proxy=proxy_airlink.ProxyAirlink(tbd_config_map["MANAGEMENT_IP"]["HOST1"])
        self.conn = self.proxy.connect()

        ping = ping_airlink.PingAirlink()
        remote_ping = self.proxy.deliver(ping)
        if remote_ping.ping_test('172.20.20.2'):
            basic_airlink.slog("Ping to HOST2 UP")
        
        self.proxy=proxy_airlink.ProxyAirlink(tbd_config_map["MANAGEMENT_IP"]["HOST2"])
        self.conn = self.proxy.connect()

        ping = ping_airlink.PingAirlink()
        remote_ping = self.proxy.deliver(ping)
        if remote_ping.ping_test('192.168.13.102'):
            basic_airlink.slog("Ping to HOST1 UP")
                
        basic_airlink.slog("End-to-end Connection: Verified")
               
    def tearDown(self):
        ''' the test runner will invoke that method after each test
        Args: None
        Returns: None
        '''        
        
        self.cb_ins.close_smart_studio()
        # Step: close the AceManager web
        basic_airlink.slog("Step: Close Firefox")  
        self.driver.quit()         
         
        basic_airlink.slog("Testcase complete")
     
     

    
        
        

        