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
#import proxy_airlink,ping_airlink

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
import ssh_airlink
import proxy_airlink
import ping_airlink

tbd_config_map, wan_config_map = basic_airlink.get_config_data("WAN","")
       
class TsWanPtEcio(unittest.TestCase):
    ''' This test suite automates RSSI test case 
    '''
                                                              
    def setUp(self):
        ''' the test runner will run that method prior to each test
        '''
        
        #self.conn_ins = connectivity.Connectivity() 
        self.fail_flag=0            
        # step: check if devices ready    
        #basic_airlink.slog("Step: Check if testbed is READY")
        #if not self.conn_ins.testbed_ready(): 
            #self.fail_flag += 1
         
        self.device_name = tbd_config_map["DUTS"][0]
              
        # step: check Firefox 
        #basic_airlink.slog("Please close Firefox if required \n")
         
        #self.se_ins = selenium_utilities.SeleniumAcemanager()
        self.at_ins = at_utilities.AtCommands()   
        #self.cb_ins = callbox_utilities.AnritsuMD8475A()
         
        # step: check if callbox/network simulation is ready  
#        if not self.cb_ins.callbox_ready(tbd_config_map, throughput_config_map):
#            self.fail_flag += 1
         
        #basic_airlink.slog("Step:  Connect DUT and generate connection instance by Telnet or USB or Serial or WiFi or OTA")
        #self.connect_instance=self.conn_ins.connection_types()
        #if not self.connect_instance.connect(): 
            #basic_airlink.slog("Problem: Testbed not ready yet")
             
        #self.fail_flag = 0
         
        # step: login to Ace Manager 
#         basic_airlink.slog("Step: Login to ACEmanager")
        #ace_manager_url = self.conn_ins.get_url()
#         self.driver = self.se_ins.login(ace_manager_url, \
#                                         tbd_config_map[self.device_name]["USERNAME"], \
#                                         tbd_config_map[self.device_name]["PASSWORD"])
#         time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"]) 
   
    def tc_ecio(self):
        '''
        '''
        self.se_ins.wan_page(self.driver)
        time.sleep(2)
        self.driver.find_element_by_xpath("//table[@id='TB_1024_WAN/Cellular_WAN/Cellular_']/tbody/tr[6]/td/p").click()
        time.sleep(2)
        self.se_ins.set_band(self.driver, 'WCDMA ALL')
        self.se_ins.apply_reboot(self.driver)
        basic_airlink.slog("Waitting for rebooting")
        time.sleep(30)  
        self.cb_ins.launch_smart_studio()
        self.driver.close()
        time.sleep(2)
        self.driver = self.se_ins.login(self.conn_ins.get_url(), \
                                        tbd_config_map[self.device_name]["USERNAME"], \
                                        tbd_config_map[self.device_name]["PASSWORD"])   
        ret = self.se_ins.verify_band(self.driver, self.se_ins, "WCDMA ALL")
        self.assertEqual(ret, True, "Verify failed")
        self.se_ins.status_page(self.driver)
        self.se_ins.status_wan_page(self.driver)
        time.sleep(30)
        cr_apn = self.se_ins.get_apn_current(self.driver)
        cur_apn = cr_apn.upper()
        basic_airlink.slog("Current APN: "+cur_apn)
          
        if cur_apn == "BROADBAND":
             
            self.cb_ins.load_sim_param_file("D:\\WnsProxy\\SimParam_att_L1W1.wnssp")
            self.cb_ins.load_cell_param_file("D:\\WnsProxy\\CellParam_2Cells.wnscp")
        else:
            self.assertEqual(cur_apn, "BROADBAND", "Invalid APN")
         
        self.cb_ins.start_simulator()
         
        self.se_ins.status_page(self.driver)
        time.sleep(20)
        self.se_ins.refresh(self.driver)
        time.sleep(2)
         
        ser = self.se_ins.get_network_service(self.driver)      
        self.assertEqual(ser, '3G', "Invalid Band")
           
        self.se_ins.get_gprs_ecio(self.driver)
        basic_airlink.slog("Signal Qaulity (Ec/Io): " +self.se_ins.get_gprs_ecio(self.driver))                    
        
        self.at_ins.gstatus(self.conn_ins)
    
        self.at_ins.get_ecio(self.conn_ins)
        
        ret_ecio = self.verify_ecio(self)
        basic_airlink.slog("Verify: "+str(ret_ecio))

#         self.cb_ins.read_RSSI(self.se_ins,self.driver)
#          
#         self.cb_ins.change_RSSI(self.changed_rssi1)
#  
#         self.cb_ins.read_RSSI(self.se_ins,self.driver)
          
#           
#           
#         verify_rssi_check = self.verify_RSSI(self.changed_rssi1)
#         basic_airlink.slog("Verify: "+ str(verify_rssi_check))
#           
#         self.cb_ins.change_RSSI(self.changed_rssi2)
#           
#         self.cb_ins.read_RSSI(self.se_ins,self.driver)  
#           
#         verify_rssi_check = self.verify_RSSI(self.changed_rssi2)
#         basic_airlink.slog("Verify: "+ str(verify_rssi_check))
        
        self.test_remote()
         
        self.cb_ins.stop_simulator()
 
    def tc_test3(self):
        
        basic_airlink.slog("Test start")
        ssh_ins = ssh_airlink.SshAirlink()
        if not ssh_ins.connect():
            print "Connection failed"

                
        ret1 = ""
        ret2 = ""
        
        ret1 = self.at_ins.gstatus(ssh_ins)
    
#         ret2 = self.at_ins.get_ecio(ssh_ins)
        
        basic_airlink.clog("GSTATUS: "+ ret1+'\n')
        
#         basic_airlink.slog("ECIO: "+ ret2+'\n')
        
        
        
    def verify_ecio(self, ):
        error_list = [-5,-4,-3,-2,-1,0,1,2,3,4,5]
        ret = False
        acmgr_ecio = self.se_ins.get_ecio(self.driver)
        at_ecio = self.at_ins.get_gprs_ecio(self.at_ins)
        for i in range(0,len(error_list)):
            if int(acmgr_ecio) == int(at_ecio) + error_list[i]:
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
        
        #self.cb_ins.close_smart_studio()
        # Step: close the AceManager web
        #basic_airlink.slog("Step: Close Firefox")  
        #self.driver.quit()         
         
        basic_airlink.slog("Testcase complete")
     
     

    
        
        

        