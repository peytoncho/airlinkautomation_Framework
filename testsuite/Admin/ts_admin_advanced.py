################################################################################
#
# This test suite implements automation of Admin test cases.
# Company: Sierra Wireless
# Time: Apr 2nd, 2013
# Author: Airlink
# 
################################################################################

import logging
import os
import sys
import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.remote.webdriver
from selenium.webdriver.support.ui import Select
import yaml

import basic_airlink
import connectivity
import selenium_utilities
import telnet_airlink


airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")
  
class TsAdminAdvanced(unittest.TestCase):
    ''' This test suite implements automation of Admin test cases.
    
    '''
       
    def setUp(self):
        ''' the test runner will run that method prior to each test
        '''
        airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
    
        stream = open(airlinkautomation_home_dirname+'/config/testbed2Conf.yml', 'r')
        tbd_config_map = yaml.load(stream)
        stream.close()
        
        self.tbd_config_map =tbd_config_map       
        
        self.conn_ins = connectivity.Connectivity()       
        
        # step: check if devices ready    
        basic_airlink.slog("step: check if testbed is ready")
        self.conn_ins.testbed_ready()
        self.device_name = self.tbd_config_map["DUTS"][0]
        
        self.se_ins = selenium_utilities.SeleniumAcemanager()              
        
        # step: login to Ace Manager 
        basic_airlink.slog("step: login to ACEmanager")
        ace_manager_url = self.conn_ins.get_url()
        self.driver = self.se_ins.login(ace_manager_url, 
                                        tbd_config_map[self.device_name]["USERNAME"], 
                                        tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])   
        
        self.fail_flag = 0
           
        self.verificationErrors = []
        self.accept_next_alert = True  
                                             
#    def is_element_present(self, how, what):
#        try: self.driver.find_element(by=how, value=what)
#        except NoSuchElementException, e: return False
#        return True
    
    
#    def close_alert_and_get_its_text(self):
#        try:
#            alert = self.driver.switch_to_alert()
#            if self.accept_next_alert:
#                alert.accept()
#            else:
#                alert.dismiss()
#            return alert.text
#        finally: self.accept_next_alert = True
         
    def tearDown(self):
        ''' the test runner will invoke that method after each test
        Args: None
        Returns: None
        '''        
        # Step: close the AceManager web
        basic_airlink.slog("step: close Firefox")  
        self.driver.quit()         
        self.assertEqual([], self.verificationErrors) 

        basic_airlink.slog(" Testcase complete")      
               
    def tc_ui_factory_reset(self):
        '''
        to test factory resetby selenium/AceManager
        
        '''
        tc_id = "tc_ui_factory_reset"
        logging.info(tc_id+' : '+'begins\n')
        
        # step: check if devices ready    
#        logging.debug("step: check if testbed is ready")
#        if not self.conn_ins.testbed_ready() : 
#            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
#            self.tc_fail_counter +=1
#            basic_airlink.cleanup()
#            return  
        
        # step: login to Ace Manager 
#        logging.debug("step: login to Ace Manager")
#        #device_name = self.tbd_config_map["DUTS"][0]
#        driver = self.se_ins.login(self.tbd_config_map[self.device_name]["ACE_URL"], self.tbd_config_map[self.device_name]["USERNAME"], self.tbd_config_map[self.device_name]["PASSWORD"])
#
#        time.sleep(self.tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])   
                
        # step: factory reste 
        if not self.se_ins.factory_reset(self.driver) : 
            #basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.fail_flag +=1
            #basic_airlink.cleanup()
            return  
        
        # step: close Firefox 
        self.se_ins.quit(self.driver)   
                
        #basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
        #self.tc_pass_counter +=1
        #basic_airlink.cleanup() 
        self.assertEqual(self.fail_flag,0)                
             
        