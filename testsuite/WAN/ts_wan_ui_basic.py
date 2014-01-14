#################################################################################
#
# This module automates WAN's UI test cases. 
# Company: Sierra Wireless
# Date: Oct 7, 2013
# 
#################################################################################

from selenium import webdriver   
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import selenium.webdriver.remote.webdriver
import time
import unittest
import selenium_utilities
import sys,os

airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")
sys.path.append(".")

import basic_airlink
basic_airlink.append_sys_path()
import connectivity

tbd_config_map, wan_config_map = basic_airlink.get_config_data("WAN","")
    
@classmethod   
def setUpClass(cls):
    ''' a class method called before tests in an individual class run
    '''
    pass            
    
@classmethod   
def tearDownClass(cls):
    ''' a class method called after tests in an individual class have run
    '''
    pass            
   
class TsWanUiBasic(unittest.TestCase):
    ''' This test suite automates WAN testcases by ACEmanager Web UI.
    '''     
                     
    def setUp(self):
        ''' the test runner will run that method prior to each test
        Args: None
        Returns: None
        '''        
        self.conn_ins = connectivity.Connectivity()       
        
        # step: check if devices ready    
        basic_airlink.slog("step: check if testbed is ready")
        self.conn_ins.testbed_ready()
        self.device_name = tbd_config_map["DUTS"][0]
        
        self.se_ins = selenium_utilities.SeleniumAcemanager()              
        
        # step: login to Ace Manager 
        basic_airlink.slog("step: login to ACEmanager")
        ace_manager_url = self.conn_ins.get_url()
        self.driver = self.se_ins.login(ace_manager_url, tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])   
        
        self.fail_flag = 0
           
        self.verificationErrors = []
        self.accept_next_alert = True  
                                             

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert.text
        finally: self.accept_next_alert = True
        
          
    def tearDown(self):
        ''' the test runner will invoke that method after each test
        Args: None
        Returns: None
        '''        
        # Step: close the AceManager web
        basic_airlink.slog("step: close browser")  
        self.driver.quit()         
        self.assertEqual([], self.verificationErrors) 

        basic_airlink.slog(" Testcase complete")
           
    def tc_application_specific_profile_mc7750(self):
        ''' Testcase - Application specific profile MC7750
        '''
        pass

    def tc_user_entered_apn(self):
        ''' Testcase - User entered APN,
            NA for GX400 with MC5728 and LS300 with SL5011
        '''
        
        if tbd_config_map[self.device_name]["RM_TYPE"] in ["MC5728","SL5011"]:
                basic_airlink.slog("This test case is NA for GX400 with MC5728 and LS300 with SL5011!")
        else:
            #step: factory reset
            self.se_ins.factory_reset(self.driver)
            
            # Step: wait till device ready
            basic_airlink.slog("step: wait till device ready" )  
            time.sleep(tbd_config_map[self.device_name ]["REBOOT_TIMEOUT"]) 
            
            # step: login to ACEmanager 
            basic_airlink.slog("step: login to ACEmanager")
            ace_manager_url = self.conn_ins.get_url()
            self.driver = self.se_ins.login(ace_manager_url, tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
            time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])   
                     
            #step: come to WAN page 
            self.se_ins.wan_page(self.driver)

            ret_apn =self.se_ins.get_apn_in_use(self.driver )  
            if tbd_config_map[self.device_name]["RM_TYPE"] in ["MC8705"]:          
                ret_apn_type = self.se_ins.get_apn_type(self.driver )
                  
            if  ret_apn == tbd_config_map[self.device_name]["APN"]:     
                basic_airlink.slog("APN in use is the expected APN, no change required!")
                #step: come to Status page 
                self.se_ins.status_page(self.driver)           
                         
            else:
                # step: user entered APN
                self.se_ins.set_apn(self.driver)
                
                # apply and reboot
                ret=self.se_ins.apply(self.driver)
                self.se_ins.reboot(self.driver)
        
                # Step: wait till device ready
                basic_airlink.slog("step: wait till device ready" )  
                time.sleep(tbd_config_map[self.device_name ]["REBOOT_TIMEOUT"]) 
        
                # step: login to ACEmanager 
                basic_airlink.slog("step: login to ACEmanager")
                ace_manager_url = self.conn_ins.get_url()
                self.driver = self.se_ins.login(ace_manager_url, tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
                time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])
 
           
            # Step:  get net IP from Status/Home page
            ret =self.se_ins.get_network_state(self.driver )            
            self.assertEqual(ret, "Network Ready")  
            
        self.assertEqual(self.fail_flag, 0)  
 
    def tc_rssi(self):
        ''' Testcase - User entered APN,
            NA for GX400 with MC5728 and LS300 with SL5011
        '''
                    
        rssi =self.se_ins.get_network_rssi(self.driver )  
         
        #step: come to Status WAN/Cellular page 
        self.se_ins.status_wan_page(self.driver)

        cur_apn =self.se_ins.get_apn_current(self.driver )  
            
        self.assertEqual(self.fail_flag, 0)  
        
    def tc_upload_prl_mc5728_only(self):
        ''' Testcase - Upload PRL for GX400 with MC5728
        '''
        
        if tbd_config_map[self.device_name]["RM_TYPE"] in ["MC5728"]:
            pass
            
    def tc_dummy(self):
        self.se_ins.wan_page(self.driver)
        self.se_ins.lan_page(self.driver)
        self.se_ins.vpn_page(self.driver)
        self.se_ins.security_page(self.driver)
        self.se_ins.services_page(self.driver)
        self.se_ins.serial_page(self.driver)
        self.se_ins.io_page(self.driver)
        self.se_ins.gps_page(self.driver)
        self.se_ins.eventreporting_page(self.driver)
        self.se_ins.admin_page(self.driver)
        self.se_ins.status_page(self.driver)
