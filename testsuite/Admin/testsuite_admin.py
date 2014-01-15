################################################################################
#
# This test suite implements automation of Admin test cases.
# Company: Sierra Wireless
# Time: Apr 2nd, 2013
# 
################################################################################

import datetime
import logging
import os
import random
import re
import subprocess
import sys
import telnetlib
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
import config_airlink
import connectivity
import msciids
import ping_airlink
import selenium_utilities
import ssh_airlink
import telnet_airlink


class TestsuiteAdmin(unittest.TestCase):
    ''' This test suite implements automation of Admin test cases.
    
    '''
                     
    def __init__(self):
        ''' Inits all related items in Testbed for testing '''
       
        self.tc_pass_counter = 0
        self.tc_fail_counter = 0
     
        self.tbd_config = config_airlink.ConfigParser(airlinkautomation_home_dirname+'/config/testbed2conf.yml')        
        self.tbd_config.processing_config("admin")
        self.conn_ins = connectivity.Connectivity()       
        
        # step: check if devices ready    
        logging.info("step: check if testbed is ready")
        self.conn_ins.testbed_ready()
        self.device_name = self.tbd_config.map["DUTS"][0]
           
        # step: check Firefox 
        logging.info("Please close Firefox \n")
 
        current_date_time = datetime.datetime.now()
       
        # step: put the current time, FW version into test report at the beginning of the test results
        basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"], "**************************************************")      
        basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"], "TIME STAMP  : " + str(current_date_time))      
        basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"], "DEVICE MODEL: " + self.tbd_config.map[self.device_name]["MODEL"])
        basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"], "RADIO TYPE  : " + self.tbd_config.map[self.device_name]["RM_TYPE"])
        basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"], "ALEOS FW VER: " + self.tbd_config.map[self.device_name]["ALEOS_FW_VER"])
        basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"], "RADIO FW VER: " + self.tbd_config.map[self.device_name]["RADIO_FW_VER"]+'\n')       
 
        self.se_ins = selenium_utilities.SeleniumAcemanager()
       
      
        
    def ui_config_allsystem_logging(self, verbosity_value, display_in_log_value):
        '''  configure subsystem logging 
         Args: 
             verbosity      - Critical/Error/Info/Debug
             display_in_log - Yes or No 
         Returns: 
             Changed   = 1
             No change = 0    
             Error     = -1       
        '''
                       
        # step: login to Ace Manager 
        logging.debug("step: login to Ace Manager")
        #device_name = self.tbd_config.map["DUTS"][0]
        driver = self.se_ins.login(self.tbd_config.map[self.device_name]["ACE_URL"], self.tbd_config.map[self.device_name]["USERNAME"], self.tbd_config.map[self.device_name]["PASSWORD"])
        if driver == -1:
            logging.debug("Login to ACEmanager faield \n")  
            return -1
        
        time.sleep(self.tbd_config.map[self.device_name]["ACE_LOGIN_WAIT"])                     
        
        # step: come to Admin page from AceManager          
        self.se_ins.admin_page(driver)      
        
        driver.find_element_by_xpath("//li[@id='SM1_Admin_Log_Configure LoggingM1']/a/span").click()
        time.sleep(2)  

        # config logging parameters by ACEmanager UI
        changed  = self.se_ins.config_one_subsystem_logging(driver,"17001-2-2", verbosity_value, "17001-2-3",  display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(driver,"17001-3-2", verbosity_value, "17001-3-3",  display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(driver,"17001-4-2", verbosity_value, "17001-4-3",  display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(driver,"17001-5-2", verbosity_value, "17001-5-3",  display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(driver,"17001-6-2", verbosity_value, "17001-6-3",  display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(driver,"17001-7-2", verbosity_value, "17001-7-3",  display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(driver,"17001-8-2", verbosity_value, "17001-8-3",  display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(driver,"17001-9-2", verbosity_value, "17001-9-3",  display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(driver,"17001-10-2",verbosity_value, "17001-10-3", display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(driver,"17001-11-2",verbosity_value, "17001-11-3", display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(driver,"17001-12-2",verbosity_value, "17001-12-3", display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(driver,"17001-13-2",verbosity_value, "17001-13-3", display_in_log_value) 
 
        if changed:
            # Step: apply and reboot DUT
            logging.debug("step: apply and reboot DUT!")
            self.se_ins.apply_reboot(driver)
            
            # Step: wait till device ready
            logging.debug("step: wait till device ready ...\n" )  
            time.sleep(self.tbd_config.map[self.device_name ]["REBOOT_TIMEOUT"]) 
            
        else: 
            logging.debug("Step: logout, both verbosity and display_in_log are not changed, no reboot required \n")  
            self.se_ins.logout(driver)
                          
        # Step: close the AceManager web
        logging.debug("step: close Firefox \n")  
        driver.quit()  
        
        if changed :  
            return 1
        else:
            return 0        
 
 
    def ui_verify_allsystem_logging(self, verbosity_value, display_in_log_value):
        '''  verify all subsystem logging setting
         Args: 
             verbosity - Critical/Error/Info/Debug
             display_in_log - yes or no 
         Returns: 
             Changed  = 1
             Nochange = 0
             
        '''
                       
        # step: login to Ace Manager 
        logging.debug("step: login to Ace Manager")
        #device_name = self.tbd_config.map["DUTS"][0]
        driver = self.se_ins.login(self.tbd_config.map[self.device_name]["ACE_URL"], self.tbd_config.map[self.device_name]["USERNAME"], self.tbd_config.map[self.device_name]["PASSWORD"])

        time.sleep(self.tbd_config.map[self.device_name]["ACE_LOGIN_WAIT"])                     
        
        # step: come to Admin page from AceManager          
        self.se_ins.admin_page(driver)      
        
        driver.find_element_by_xpath("//li[@id='SM1_Admin_Log_Configure LoggingM1']/a/span").click()
        time.sleep(2)  

        # config logging parameters by ACEmanager UI
        identical  = self.se_ins.verify_one_subsystem_logging(driver,"17001-2-2", verbosity_value, "17001-2-3",  display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(driver,"17001-3-2", verbosity_value, "17001-3-3",  display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(driver,"17001-4-2", verbosity_value, "17001-4-3",  display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(driver,"17001-5-2", verbosity_value, "17001-5-3",  display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(driver,"17001-6-2", verbosity_value, "17001-6-3",  display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(driver,"17001-7-2", verbosity_value, "17001-7-3",  display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(driver,"17001-8-2", verbosity_value, "17001-8-3",  display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(driver,"17001-9-2", verbosity_value, "17001-9-3",  display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(driver,"17001-10-2",verbosity_value, "17001-10-3", display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(driver,"17001-11-2",verbosity_value, "17001-11-3", display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(driver,"17001-12-2",verbosity_value, "17001-12-3", display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(driver,"17001-13-2",verbosity_value, "17001-13-3", display_in_log_value) 
                          
        # Step: close the AceManager web
        logging.debug("step: close Firefox \n")  
        driver.quit()   
        
        if identical < 0 :
            # exist unexpected in the 12 logging settings
            return False
        else:     
            return True 
 
 
    def ui_set_logging_all(self, tc_id, verbosity_value, display_in_log_value):
        '''
        
        '''    
        
                
        # step: check if devices ready    
        logging.debug("step: check if Testbed is ready")
        if not self.conn_ins.testbed_ready() : 
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            basic_airlink.cleanup()
            self.self.tc_fail_counter += 1
            return 
         
        logging.info(tc_id+' : '+'begins'+'\n')
        
        # step: configure subsystem WAN logging 
        changed = self.ui_config_allsystem_logging(verbosity_value, display_in_log_value)
        
        if changed: 
            # step: verify subsystem WAN logging setting
            indentical = self.ui_verify_allsystem_logging(verbosity_value, display_in_log_value)          
            if not indentical: 
                basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
                basic_airlink.cleanup()
                self.tc_fail_counter += 1
                return 
                     
        basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
        basic_airlink.cleanup()  
        self.tc_pass_counter += 1 
   
        
    def ui_config_subsystem_logging(self, verbosity_name, verbosity_value, display_in_log_name, display_in_log_value):
        '''  configure subsystem logging 
         args: 
         driver - Firefox driver 
         sub_system - WAN/LAN/VPN/...
         verbosity - Critical/Error/Info/Debug
         display_in_log - yes or no 
         returns: 
             Changed  = 1
             Nochange = 0
             
        '''
                       
        # step: login to Ace Manager 
        logging.debug("step: login to ACEmanager to config logging")
        #device_name = self.tbd_config.map["DUTS"][0]
        driver = self.se_ins.login(self.tbd_config.map[self.device_name]["ACE_URL"], self.tbd_config.map[self.device_name]["USERNAME"], self.tbd_config.map[self.device_name]["PASSWORD"])

        time.sleep(self.tbd_config.map[self.device_name]["ACE_LOGIN_WAIT"])                     
        
        # step: come to Admin page from AceManager          
        self.se_ins.admin_page(driver)      
        
        driver.find_element_by_xpath("//li[@id='SM1_Admin_Log_Configure LoggingM1']/a/span").click()
        time.sleep(2)  
                    
        # config logging parameters by ACEmanager UI
        changed = self.se_ins.config_one_subsystem_logging(driver,verbosity_name,verbosity_value, display_in_log_name, display_in_log_value) 

        if changed:
            # Step: apply and reboot DUT
            logging.debug("step: apply and reboot DUT!")
            self.se_ins.apply_reboot(driver)
            
            # Step: wait till device ready
            logging.debug("step: wait till device ready ...\n" )  
            time.sleep(self.tbd_config.map[self.device_name]["REBOOT_TIMEOUT"]) 
            
        else: 
            logging.debug("Step: logout, both verbosity and display_in_log are not changed, no reboot required \n")  
            self.se_ins.logout(driver)
                          
        # Step: close the AceManager web
        logging.debug("step: quit Firefox \n")  
        driver.quit()  
        
        if changed :  
            return 1
        else:
            return 0
 
 
    def ui_verify_subsystem_logging(self,verbosity_name,verbosity_value, display_in_log_name, display_in_log_value):
        ''' go to Admin page, and verify if the subsystem logging setting is expected 
        
        '''
                
        # step: login to Ace Manager 
        logging.debug("step: login to ACEmanager to verify the setting")
        #device_name = self.tbd_config.map["DUTS"][0]
        driver = self.se_ins.login(self.tbd_config.map[self.device_name]["ACE_URL"], self.tbd_config.map[self.device_name]["USERNAME"], self.tbd_config.map[self.device_name]["PASSWORD"])

        time.sleep(self.tbd_config.map[self.device_name]["ACE_LOGIN_WAIT"])                     
        
        # step: come to Admin page from AceManager
        self.se_ins.admin_page(driver)      
        
        driver.find_element_by_xpath("//li[@id='SM1_Admin_Log_Configure LoggingM1']/a/span").click()
        time.sleep(2)  

        # step: verify subsystem logging by ACEmanager UI
        ret = self.se_ins.verify_one_subsystem_logging(driver,verbosity_name,verbosity_value, display_in_log_name, display_in_log_value) 
        
        #Step: quit the AceManaer web   
        logging.debug("step: quit Firefox Acemanager web \n")  
        driver.quit()   
       
        if ret == -1:
            
            # the subsystem logging setting is unexpected 
            return False
        
        else:     
            
            # the subsystem logging setting is expected 
            return True
        
        
    def ui_admin_logging(self, tc_id, verbosity_msciid, verbosity_value, display_msciid, display_value):
        ''' This method configures logging parameter subsystem from checking testbed to getting test result
        
        '''
        
        
                
        # step: check if devices ready    
        logging.debug("step: check if Testbed is ready")
        if not self.conn_ins.testbed_ready() : 
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            basic_airlink.cleanup()
            self.tc_fail_counter += 1
            return 
         
        logging.info(tc_id+' : '+'begins'+'\n')
        
        # step: configure subsystem logging 
        changed = self.ui_config_subsystem_logging(verbosity_msciid,verbosity_value, display_msciid,display_value)
        
        if changed: 
            # step: verify subsystem logging setting
            ret = self.ui_verify_subsystem_logging(verbosity_msciid,verbosity_value, display_msciid,display_value)          
            if not ret: 
                basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
                basic_airlink.cleanup()
                self.tc_fail_counter += 1
                return 
                     
        basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
        basic_airlink.cleanup()  
        self.tc_pass_counter += 1


#############################################
#    WAN logging tests
#############################################

    def tc_ui_config_logging_wan_celluar_critical_display_yes(self):
        ''' This test case configures logging parameter to Critical for WAN/Celluar subsystem 
        
        '''
        
        tc_id = "tc_ui_config_logging_wan_celluar_critical_display_yes"
        self.ui_admin_logging(tc_id, "17001-2-2", "Critical","17001-2-3","Yes")
        

        

    def tc_ui_config_logging_wan_celluar_critical_display_no(self):
        ''' This test case configures logging parameter to Critical for WAN/Celluar subsystem 
        
        '''
        
        tc_id = "tc_ui_config_logging_wan_celluar_critical_display_no"
        self.ui_admin_logging(tc_id, "17001-2-2", "Critical","17001-2-3","No")
 
        
 
        
    def tc_ui_config_logging_wan_celluar_debug_display_yes(self):
        ''' This test case configures logging parameter to Debug level for WAN/Celluar subsystem 
            display to Yes
        '''
        
        tc_id = "tc_ui_config_logging_wan_celluar_debug_display_yes"
        self.ui_admin_logging(tc_id, "17001-2-2", "Debug","17001-2-3","Yes")
       

    def tc_ui_config_logging_wan_celluar_debug_display_no(self):
        ''' This test case configures logging parameter to debug level for WAN/Celluar subsystem 
            display to No
        '''
        
        tc_id = "tc_ui_config_logging_wan_celluar_debug_display_no"    
        self.ui_admin_logging(tc_id, "17001-2-2", "Debug","17001-2-3","No")
   
        
    def tc_ui_config_logging_wan_celluar_error_display_yes(self):
        # test case configure logging parameters for WAN/Celluar '''
        tc_id = "tc_ui_config_logging_wan_celluar_error"
        self.ui_admin_logging(tc_id, "17001-2-2", "Error","17001-2-3","Yes")
        
 
    def tc_ui_config_logging_wan_celluar_error_display_no(self):
        # test case configure logging parameters for WAN/Celluar '''
        tc_id = "tc_ui_config_logging_wan_celluar_error"
        self.ui_admin_logging(tc_id, "17001-2-2", "Error","17001-2-3","No")
        
        
    def tc_ui_config_logging_wan_celluar_info_display_yes(self):
        '''    ''' 
        
        # test case configure logging parameters for WAN/Celluar '''
        tc_id = "tc_ui_config_logging_wan_celluar_info_display_yes"
        self.ui_admin_logging(tc_id, "17001-2-2", "Info","17001-2-3","Yes")


    def tc_ui_config_logging_wan_celluar_info_display_no(self):
        '''    ''' 
        
        # test case configure logging parameters for WAN/Celluar '''
        tc_id = "tc_ui_config_logging_wan_celluar_info_display_no"
        self.ui_admin_logging(tc_id, "17001-2-2", "Info","17001-2-3","No")
 
#############################################
#    LAN logging tests
#############################################

    def tc_ui_config_logging_lan_critical_display_yes(self):
        '''
        
        
        '''
        tc_id = "tc_ui_config_logging_lan_critical_display_yes"
        self.ui_admin_logging(tc_id, "17001-3-2", "Critical","17001-3-3","Yes")


    def tc_ui_config_logging_lan_critical_display_no(self):
        '''
        
        
        '''
        
        tc_id = "tc_ui_config_logging_lan_critical_display_no"
        self.ui_admin_logging(tc_id, "17001-3-2", "Critical","17001-3-3","No")


    def tc_ui_config_logging_lan_debug_display_yes(self):
        '''
        
        
        '''
        
        tc_id = "tc_ui_config_logging_lan_debug_display_yes"
        self.ui_admin_logging(tc_id, "17001-3-2", "Debug","17001-3-3","Yes")


    def tc_ui_config_logging_lan_debug_display_no(self):
        '''
        
        
        '''
        
        tc_id = "tc_ui_config_logging_lan_debug_display_no"
        self.ui_admin_logging(tc_id, "17001-3-2", "Debug","17001-3-3","No")
        
            
    def tc_ui_config_logging_lan_error_display_yes(self):
        '''
        
        
        '''
        tc_id = "tc_ui_config_logging_lan_error_display_yes"
        self.ui_admin_logging(tc_id, "17001-3-2", "Error","17001-3-3","Yes")


    def tc_ui_config_logging_lan_error_display_no(self):
        '''
        
        
        '''
        tc_id = "tc_ui_config_logging_lan_error_display_no"
        self.ui_admin_logging(tc_id, "17001-3-2", "Error","17001-3-3","No")
 
        
    def tc_ui_config_logging_lan_info_display_yes(self):
        '''
        
        
        '''
        tc_id = "tc_ui_config_logging_lan_info_display_yes"
        self.ui_admin_logging(tc_id, "17001-3-2", "Info","17001-3-3","Yes")


    def tc_ui_config_logging_lan_info_display_no(self):
        '''
        
        
        '''
        tc_id = "tc_ui_config_logging_lan_info_display_no"
        self.ui_admin_logging(tc_id, "17001-3-2", "Info","17001-3-3","No")
        
        
#############################################
#  set logging all subsystem to same yes or no
#############################################

    def tc_ui_logging_all_critical_display_yes(self):
        '''
        
        '''
        
        tc_id = "tc_ui_logging_all_critcial_display_yes"
 
        self.ui_set_logging_all(tc_id, "Critical", "Yes")
        
        
    def tc_ui_logging_all_critical_display_no(self):
        '''
        
        '''
        
        tc_id = "tc_ui_logging_all_critical_display_no"
 
        self.ui_set_logging_all(tc_id, "Critical", "No")
 
        
    def tc_ui_logging_all_error_display_yes(self):
        '''
        
        '''
        
        tc_id = "tc_ui_logging_all_error_display_yes"
 
        self.ui_set_logging_all(tc_id, "Error", "Yes")
        
        
    def tc_ui_logging_all_error_display_no(self):
        '''
        
        '''
        
        tc_id = "tc_ui_logging_all_error_display_no"
 
        self.ui_set_logging_all(tc_id, "Error", "No")
        

    def tc_ui_logging_all_info_display_yes(self):
        '''
        '''
        
        tc_id = "tc_ui_logging_all_info_display_yes"
 
        self.ui_set_logging_all(tc_id, "Info", "Yes")
  
        
    def tc_ui_logging_all_info_display_no(self):
        ''' 
        
        '''
        tc_id = "tc_ui_logging_all_info_display_no"
 
        self.ui_set_logging_all(tc_id, "Info", "No")
  
        
    def tc_ui_logging_all_debug_display_yes(self):
        '''
        '''
        
        tc_id = "tc_ui_logging_all_debug_display_yes"
 
        self.ui_set_logging_all(tc_id, "Debug", "Yes")

       
    def tc_ui_logging_all_debug_display_no(self):
        ''' 
        
        '''
        
        tc_id = "tc_ui_logging_all_debug_display_no"
 
        self.ui_set_logging_all(tc_id, "Debug", "No")
         
        
    def tc_ui_config_linux_sys_log(self):
        '''test case configure linux sys log display, doesn't require reboot
        '''
 
        
        
               
        tc_id = "tc_ui_config_linux_sys_log"
        logging.info(tc_id+' : '+'begins\n')
        
        # step: check if devices ready    
        logging.debug("step: check if testbed is ready")
        if not self.conn_ins.testbed_ready() : 
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            basic_airlink.cleanup()
            return  
 
        # step: login to Ace Manager 
        logging.debug("step: login to Ace Manager")
        #device_name = self.tbd_config.map["DUTS"][0]
        driver = self.se_ins.login(self.tbd_config.map[self.device_name]["ACE_URL"], self.tbd_config.map[self.device_name]["USERNAME"], self.tbd_config.map[self.device_name]["PASSWORD"])

        time.sleep(self.tbd_config.map[self.device_name]["ACE_LOGIN_WAIT"])                     
        
        # step: come to Admin page from AceManager          
        self.se_ins.admin_page(driver)      
        
        driver.find_element_by_xpath("//li[@id='SM1_Admin_Log_Configure LoggingM1']/a/span").click()
        time.sleep(2) 
        
        # step: config linux syslog to "Display"
        changed = self.se_ins.config_linux_syslog(driver, "Display")
        
        if changed: 
            #step: refresh 
            self.se_ins.apply_refresh(driver)      
        
        # step: verify the linux syslog setting
        indentical=self.se_ins.verify_linux_syslog(driver, "Display")
        
        #driver.quit()
        
        if not indentical: 
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            basic_airlink.cleanup()
            return 

        time.sleep(5) 
 
        # step: config linux syslog  to "No Display"
        changed = self.se_ins.config_linux_syslog(driver, "No Display")
        
        if changed: 
            #step: refresh 
            self.se_ins.apply_refresh(driver)      
        
        # step: verify the linux syslog setting
        indentical=self.se_ins.verify_linux_syslog(driver, "No Display")
        
        driver.quit()
        
        if not indentical: 
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            basic_airlink.cleanup()
            return 
           
        basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
        self.tc_pass_counter +=1
        basic_airlink.cleanup()  
           
               
    def tc_ui_viewer_change_password(self):   
        '''
        to test password change functionality for viewer
        
        '''
        tc_id = "tc_ui_viewer_change_password"
        logging.info(tc_id+' : '+'begins\n')
        
        # step: check if devices ready    
        logging.debug("step: check if testbed is ready")
        if not self.conn_ins.testbed_ready() : 
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            basic_airlink.cleanup()
            return  
        
        # step: login to Ace Manager 
        logging.debug("step: login to Ace Manager")
        #device_name = self.tbd_config.map["DUTS"][0]
        driver = self.se_ins.login(self.tbd_config.map[self.device_name]["ACE_URL"], self.tbd_config.map[self.device_name]["USERNAME"], self.tbd_config.map[self.device_name]["PASSWORD"])

        time.sleep(self.tbd_config.map[self.device_name]["ACE_LOGIN_WAIT"])                     
        
        # step: come to Admin page from AceManager          
        self.se_ins.admin_page(driver)    
                
        if driver == -1:
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            self.se_ins.quit(driver)  
            basic_airlink.cleanup()
            return             
        else:
            driver.find_element_by_xpath("//li[@id='SM1_Admin_Change PasswordM1']/a/span").click()
            Select(driver.find_element_by_id("selectedUsername")).select_by_visible_text("viewer")
            driver.find_element_by_id("Newpassword").clear()
            driver.find_element_by_id("Newpassword").send_keys("54321")
            driver.find_element_by_id("Retypepassword").clear()
            driver.find_element_by_id("Retypepassword").send_keys("54321")
            driver.find_element_by_id("chpwd").click()
            time.sleep(5)
            driver.switch_to_alert().accept()
                    
        self.se_ins.quit(driver)   
 
        # step: login to Ace Manager 
        logging.debug("step: login to Ace Manager")
        #device_name = self.tbd_config.map["DUTS"][0]
        driver = self.se_ins.login(self.tbd_config.map[self.device_name]["ACE_URL"], self.tbd_config.map[self.device_name]["USERNAME"], self.tbd_config.map[self.device_name]["PASSWORD"])

        time.sleep(self.tbd_config.map[self.device_name]["ACE_LOGIN_WAIT"])                     
        
        # step: come to Admin page from AceManager          
        self.se_ins.admin_page(driver)   
                
        if driver == -1:
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            self.se_ins.quit(driver)  
            return             
        else:
            driver.find_element_by_xpath("//li[@id='SM1_Admin_Change PasswordM1']/a/span").click()
            Select(driver.find_element_by_id("selectedUsername")).select_by_visible_text("viewer")
            driver.find_element_by_id("Newpassword").clear()
            driver.find_element_by_id("Newpassword").send_keys("12345")
            driver.find_element_by_id("Retypepassword").clear()
            driver.find_element_by_id("Retypepassword").send_keys("12345")
            driver.find_element_by_id("chpwd").click()
            time.sleep(5)
            driver.switch_to_alert().accept()
                    
        self.se_ins.quit(driver)   
        
        basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
        self.tc_pass_counter +=1
        basic_airlink.cleanup()              
        

        
    def tc_ui_user_change_password(self):   
        '''
        to test password change functionality for user
        
        '''
        tc_id = "tc_ui_user_change_password"
        logging.info(tc_id+' : '+'begins\n')
        
        # step: check if devices ready    
        logging.debug("step: check if testbed is ready")
        if not self.conn_ins.testbed_ready() : 
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            basic_airlink.cleanup()
            return  
        
        # step: login to Ace Manager 
        logging.debug("step: login to Ace Manager")
        #device_name = self.tbd_config.map["DUTS"][0]
        driver = self.se_ins.login(self.tbd_config.map[self.device_name]["ACE_URL"], self.tbd_config.map[self.device_name]["USERNAME"], self.tbd_config.map[self.device_name]["PASSWORD"])

        time.sleep(self.tbd_config.map[self.device_name]["ACE_LOGIN_WAIT"])                     
        
        # step: come to Admin page from AceManager          
        self.se_ins.admin_page(driver)   
                
        if driver == -1:
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            self.se_ins.quit(driver)  
            return  
        else:
            Select(driver.find_element_by_id("selectedUsername")).select_by_visible_text(self.tbd_config.map[self.device_name]["USERNAME"])
            driver.find_element_by_id("password").clear()
            driver.find_element_by_id("password").send_keys(self.tbd_config.map[self.device_name]["PASSWORD"])
            driver.find_element_by_id("Newpassword").clear()
            driver.find_element_by_id("Newpassword").send_keys("54321")
            driver.find_element_by_id("Retypepassword").clear()
            driver.find_element_by_id("Retypepassword").send_keys("54321")
            driver.find_element_by_id("chpwd").click()
            time.sleep(5)
            driver.switch_to_alert().accept()      
        
        self.se_ins.quit(driver)   

        # step: login to Ace Manager 
        logging.debug("step: login to Ace Manager")
        #device_name = self.tbd_config.map["DUTS"][0]
        driver = self.se_ins.login(self.tbd_config.map[self.device_name]["ACE_URL"], username="user", password="54321")

        time.sleep(self.tbd_config.map[self.device_name]["ACE_LOGIN_WAIT"])                     
        
        # step: come to Admin page from AceManager          
        self.se_ins.admin_page(driver)   
                
        if driver == -1:
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            self.se_ins.quit(driver)  
            return  
        
        else:

            Select(driver.find_element_by_id("selectedUsername")).select_by_visible_text(self.tbd_config.map[self.device_name]["USERNAME"])
            driver.find_element_by_id("password").clear()
            driver.find_element_by_id("password").send_keys("54321")
            driver.find_element_by_id("Newpassword").clear()
            driver.find_element_by_id("Newpassword").send_keys(self.tbd_config.map[self.device_name]["PASSWORD"])
            driver.find_element_by_id("Retypepassword").clear()
            driver.find_element_by_id("Retypepassword").send_keys(self.tbd_config.map[self.device_name]["PASSWORD"])
            driver.find_element_by_id("chpwd").click()
            time.sleep(5)
            driver.switch_to_alert().accept()    
                
        self.se_ins.quit(driver)   
                
        basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
        self.tc_pass_counter +=1
        basic_airlink.cleanup()             
        
       
    def tc_ui_factory_reset(self):
        '''
        to test factory resetby selenium/AceManager
        
        '''
        tc_id = "tc_ui_factory_reset"
        logging.info(tc_id+' : '+'begins\n')
        
        # step: check if devices ready    
        logging.debug("step: check if testbed is ready")
        if not self.conn_ins.testbed_ready() : 
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            basic_airlink.cleanup()
            return  
        
        # step: login to Ace Manager 
        logging.debug("step: login to Ace Manager")
        #device_name = self.tbd_config.map["DUTS"][0]
        driver = self.se_ins.login(self.tbd_config.map[self.device_name]["ACE_URL"], self.tbd_config.map[self.device_name]["USERNAME"], self.tbd_config.map[self.device_name]["PASSWORD"])

        time.sleep(self.tbd_config.map[self.device_name]["ACE_LOGIN_WAIT"])   
                
        # step: factory reste 
        if not self.se_ins.factory_reset(driver) : 
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            basic_airlink.cleanup()
            return  
        
        # step: close Firefox 
        self.se_ins.quit(driver)   
                
        basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
        self.tc_pass_counter +=1
        basic_airlink.cleanup() 
  
  
    def tc_at_factory_reset(self):
        '''
        to test factory reset by AT command
        
        '''
        tc_id = "tc_at_factory_reset"
        logging.info(tc_id+' : '+'begins\n')
        temp_count = 2
        
        while temp_count > 0 :
        # step: check if devices ready    
            logging.debug("step: check if testbed is ready")
            if not self.conn_ins.testbed_ready() : 
                basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
                self.tc_fail_counter +=1
                basic_airlink.cleanup()
                return  
            
            # step: Telnet to device            
            _device   = self.tbd_config.map["DUTS"][0]
            _hostname = self.tbd_config.map[_device]["LAN_IP"] 
            print _hostname        
            connect_instance = self.conn_ins.connection_types()    
            if not (connect_instance.connect()):
                basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
                self.tc_fail_counter +=1
                basic_airlink.cleanup()
                return  
            
            if temp_count == 2:    
                #step: get number fo system reset 
                logging.debug("Step:  get number fo system reset by AT command before reset")
                ret = connect_instance.command("at*sysresets?")
                logging.debug(ret)
               
                #step: set host conenction mode 
                logging.debug("Step:  set host conenction mode to 2 by AT command")
                ret = connect_instance.command("at*hostprivmode=2")
                logging.debug(ret)

                ret_str = ''.join(ret)
                if not ret_str.find("OK"): 
                    logging.debug(' factory reset not OK   \n')
                    basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
                    self.tc_fail_counter +=1
                    basic_airlink.cleanup()  
                    return 
                            
                #step:  factory reset
                logging.debug("Step:  factory reset")
                ret = connect_instance.command("at*resetcfg")
                 
                print ret
                ret_str = ''.join(ret)                
                if not ret_str.find("OK"): 
                    logging.debug(' factory reset not OK   \n')
                    basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
                    self.tc_fail_counter +=1
                    basic_airlink.cleanup() 
                    
                time.sleep(self.tbd_config.map[self.device_name ]["REBOOT_TIMEOUT"]) 
                temp_count -=1
                
            elif temp_count ==1: 
                
                #step: get number fo system reset 
                logging.debug("Step:  get number fo system reset by AT command after reset")
                ret = connect_instance.command("at*sysresets?")
                logging.debug(ret)
                
                #step: get host conenction mode 
                logging.debug("Step:  get host conenction mode by AT command")
                ret = connect_instance.command("at*hostprivmode?")
                logging.debug(ret)

                ret_str = ''.join(ret)                             
                if ret_str.find("1"): 
                    logging.debug(' factory reset  OK \n')
                    basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
                    self.tc_pass_counter +=1
                    basic_airlink.cleanup() 
                    return 
                else:
                    logging.debug(' factory reset not OK   \n')
                    basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
                    self.tc_fail_counter +=1
                    basic_airlink.cleanup()  
                    return  
                

    def tc_memory_cpu_root_user(self):
        '''
        to check the memory  and CPU usage in DUT as root user
        
        '''
        tc_id = "tc_memory_check_root_user"
        logging.info(tc_id+' : '+'begins\n')
        
        # step: check if devices ready    
        logging.debug("step: check if Testbed is ready")
        if not self.conn_ins.testbed_ready() :         
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            basic_airlink.cleanup()
            return  
        
        # step: Telnet to device            
        _device   = self.tbd_config.map["DUTS"][0]
        _hostname = self.tbd_config.map[_device]["LAN_IP"] 
        print _hostname        
        connect_instance = telnet_airlink.TelnetAirlink( hostname=_hostname, port = "2332", username = "root", password = "v3r1fym3",debug_mode= True)
        if not (connect_instance.connect()):
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            basic_airlink.cleanup()
            return  
        
        else:
            #step: get memory status 
            logging.debug("Step:  get memory status")
            
            ret = connect_instance.command("free -m")
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)
            
            ret = connect_instance.command("top -n3")
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("\n")

            ret = connect_instance.command("cat /proc/meminfo")
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)
                                      
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
            self.tc_pass_counter +=1
            #basic_airlink.cleanup()
                                                 
 
    def tc_log_reset_check_root_user(self):
        '''
        to check the rebooting by AT command and log
        
        '''
        tc_id = "tc_log_reset_check_root_user"
        logging.info(tc_id+' : '+'begins\n')
        
        # step: check if devices ready    
        logging.debug("step: check if testbed is ready")
        if not self.conn_ins.testbed_ready() : 
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            #basic_airlink.cleanup()
            return  
        
        # step: Telnet to device            
        _device   = self.tbd_config.map["DUTS"][0]
        _hostname = self.tbd_config.map[_device]["LAN_IP"] 
        
        connect_instance = self.conn_ins.connection_types()    
        if not (connect_instance.connect()):
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            #basic_airlink.cleanup()
            return 
  
        else:
            
            #step: get the number of reset since last reset to default
            logging.debug("Step:  get the number of reset since last reset to default")
            ret = connect_instance.command("at*sysresets?")
            ret_str = ''.join(ret)                             
            basic_airlink.slog(ret_str)     
                    
        connect_instance = telnet_airlink.TelnetAirlink( hostname=_hostname, port = "2332", username = "root", password = "v3r1fym3",debug_mode= True)
        if not (connect_instance.connect()):
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            #basic_airlink.cleanup()
            return  
        
        else:
            
            #step: get reset timestamp from logs
            logging.debug("Step:  get reset timestamp from the latest fives logs")
            
            if self.tbd_config.map[self.device_name]["RM_TYPE"] == "MC7750":
                reset_substring = 'alert ALEOS_SYSTEM_SCR_rc.syslog:   Version: ' 

            else:
                reset_substring = 'alert ALEOS_SYSTEM_SCR_rc.syslog:   Version:'  
                #reset_substring = 'alert ALEOS_SYSTEM_SCR_aleosreboot: Rebooting...'  

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages | grep -E \'%s\'" %(reset_substring))
            ret_str = ''.join(ret)                             
            basic_airlink.slog(ret_str)
            
            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.0 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.1 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)
 
            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.2 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.3 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.4 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)
                                                             
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
            self.tc_pass_counter +=1
            #basic_airlink.cleanup()
            
      
    def tc_check_network_state_root_user(self):
        '''
        to check the network state by AT command and log
        
        '''
        tc_id = "tc_check_network_state_root_user"
        logging.info(tc_id+' : '+'begins\n')
        
        # step: check if devices ready    
        logging.debug("step: check if testbed is ready")
        if not self.conn_ins.testbed_ready() : 
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            #basic_airlink.cleanup()
            return  
        
        # step: Telnet to device            
        _device   = self.tbd_config.map["DUTS"][0]
        _hostname = self.tbd_config.map[_device]["LAN_IP"] 
        
        connect_instance = self.conn_ins.connection_types()    
        if not (connect_instance.connect()):
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            #basic_airlink.cleanup()
            return 
  
        else:
            
            #step: get the number of reset since last reset to default
            logging.debug("Step:  get the number of reset since last reset to default")
            ret = connect_instance.command("at*netstate?")
            ret_str = ''.join(ret)                             
            basic_airlink.slog(ret_str)     
                    
        connect_instance = telnet_airlink.TelnetAirlink( hostname=_hostname, port = "2332", username = "root", password = "v3r1fym3",debug_mode= True)
        if not (connect_instance.connect()):
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            #basic_airlink.cleanup()
            return  
        
        else:
            
            #step: get reset timestamp from logs
            logging.debug("Step:  get the network state from the latest fives logs")
            
            reset_substring = 'Network State'  

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages | grep -E \'%s\'" %(reset_substring))
            ret_str = ''.join(ret)                             
            basic_airlink.slog(ret_str)
            
            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.0 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.1 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)
 
            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.2 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.3 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.4 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)
                                                             
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
            self.tc_pass_counter +=1
            #basic_airlink.cleanup()
            
 
    def tc_check_gps_data_root_user(self):
        '''
        to check the GPS data by AT command and log
        
        '''
        tc_id = "tc_check_gps_data_root_user"
        logging.info(tc_id+' : '+'begins\n')
        
        # step: check if devices ready    
        logging.debug("step: check if testbed is ready")
        if not self.conn_ins.testbed_ready() : 
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            #basic_airlink.cleanup()
            return  
        
        # step: Telnet to device            
        _device   = self.tbd_config.map["DUTS"][0]
        _hostname = self.tbd_config.map[_device]["LAN_IP"] 
        
        connect_instance = self.conn_ins.connection_types()    
        if not (connect_instance.connect()):
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            #basic_airlink.cleanup()
            return 
  
        else:
            
            #step: get the number of reset since last reset to default
            logging.debug("Step:  get the number of reset since last reset to default")
            ret = connect_instance.command("at*gpsdata?")
            ret_str = ''.join(ret)                             
            basic_airlink.slog(ret_str)     
                    
        connect_instance = telnet_airlink.TelnetAirlink( hostname=_hostname, port = "2332", username = "root", password = "v3r1fym3",debug_mode= True)
        if not (connect_instance.connect()):
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.tc_fail_counter +=1
            #basic_airlink.cleanup()
            return  
        
        else:
            
            #step: get reset timestamp from logs
            logging.debug("Step:  get the GPS fix from the latest fives logs")
            
            reset_substring = 'GPS '  

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages | grep -E \'%s\'" %(reset_substring))
            ret_str = ''.join(ret)                             
            basic_airlink.slog(ret_str)
            
            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.0 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.1 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)
 
            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.2 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.3 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.4 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)
                                                             
            basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
            self.tc_pass_counter +=1
            #basic_airlink.cleanup()
                               
    def finallize(self): 
        '''
        To print out PASSED/FAILED testcases number in test report
        '''
        
        print "\n passed: ", self.tc_pass_counter, " failed:", self.tc_fail_counter
        basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],"\nPassed : "+ str(self.tc_pass_counter))
        basic_airlink.test_report(self.tbd_config.map["TEST_REPORT_FILE"],"\nFailed : "+ str(self.tc_fail_counter))  
                
    
####################################################
# main  Admin test automation
####################################################

print sys.platform

airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME']

my_admin = TestsuiteAdmin()

        
ADMIN_TESTCASES ={  \
   "tc_ui_config_logging_wan_celluar_debug_display_yes"    : my_admin.tc_ui_config_logging_wan_celluar_debug_display_yes, \
   "tc_ui_config_logging_wan_celluar_debug_display_no"     : my_admin.tc_ui_config_logging_wan_celluar_debug_display_no, \
   "tc_ui_config_logging_wan_celluar_info_display_yes"     : my_admin.tc_ui_config_logging_wan_celluar_info_display_yes, \
   "tc_ui_config_logging_wan_celluar_info_display_no"      : my_admin.tc_ui_config_logging_wan_celluar_info_display_no, \
   "tc_ui_config_logging_wan_celluar_error_display_yes"    : my_admin.tc_ui_config_logging_wan_celluar_error_display_yes, \
   "tc_ui_config_logging_wan_celluar_error_display_no"     : my_admin.tc_ui_config_logging_wan_celluar_error_display_no, \
   "tc_ui_config_logging_wan_celluar_critical_display_yes" : my_admin.tc_ui_config_logging_wan_celluar_critical_display_yes, \
   "tc_ui_config_logging_wan_celluar_critical_display_no"  : my_admin.tc_ui_config_logging_wan_celluar_critical_display_no, \
   "tc_ui_config_logging_lan_debug_display_yes"            : my_admin.tc_ui_config_logging_lan_debug_display_yes, \
   "tc_ui_config_logging_lan_debug_display_no"             : my_admin.tc_ui_config_logging_lan_debug_display_no, \
   "tc_ui_config_logging_lan_info_display_yes"             : my_admin.tc_ui_config_logging_lan_info_display_yes, \
   "tc_ui_config_logging_lan_info_display_no"              : my_admin.tc_ui_config_logging_lan_info_display_no, \
   "tc_ui_config_logging_lan_error_display_yes"            : my_admin.tc_ui_config_logging_lan_error_display_yes, \
   "tc_ui_config_logging_lan_error_display_no"             : my_admin.tc_ui_config_logging_lan_error_display_no, \
   "tc_ui_config_logging_lan_critical_display_yes"         : my_admin.tc_ui_config_logging_lan_critical_display_yes, \
   "tc_ui_config_logging_lan_critical_display_no"          : my_admin.tc_ui_config_logging_lan_critical_display_no, \
   "tc_ui_logging_all_critical_display_yes"                : my_admin.tc_ui_logging_all_critical_display_yes, \
   "tc_ui_logging_all_critical_display_no"                 : my_admin.tc_ui_logging_all_critical_display_no, \
   "tc_ui_logging_all_error_display_yes"                   : my_admin.tc_ui_logging_all_error_display_yes, \
   "tc_ui_logging_all_error_display_no"                    : my_admin.tc_ui_logging_all_error_display_no, \
   "tc_ui_logging_all_info_display_yes"                    : my_admin.tc_ui_logging_all_info_display_yes, \
   "tc_ui_logging_all_info_display_no"                     : my_admin.tc_ui_logging_all_info_display_no, \
   "tc_ui_logging_all_debug_display_yes"                   : my_admin.tc_ui_logging_all_debug_display_yes, \
   "tc_ui_logging_all_debug_display_no"                    : my_admin.tc_ui_logging_all_debug_display_no, \
   "tc_ui_config_linux_sys_log"                            : my_admin.tc_ui_config_linux_sys_log, \
   "tc_ui_viewer_change_password"                          : my_admin.tc_ui_viewer_change_password, \
   "tc_ui_user_change_password"                            : my_admin.tc_ui_user_change_password, \
   "tc_ui_factory_reset"                                   : my_admin.tc_ui_factory_reset, \
   "tc_at_factory_reset"                                   : my_admin.tc_at_factory_reset, \
   "tc_memory_cpu_root_user"                               : my_admin.tc_memory_cpu_root_user, \
   "tc_log_reset_check_root_user"                          : my_admin.tc_log_reset_check_root_user,\
   "tc_check_network_state_root_user"                      : my_admin.tc_check_network_state_root_user,\
   "tc_check_gps_data_root_user"                           : my_admin.tc_check_gps_data_root_user\
           }
    
# load testsuite config and testbed config

fo=open(airlinkautomation_home_dirname+'/testsuite/Admin/admin_test_conf.yml','r')
admin_config_map = yaml.load(fo)
fo.close()

# run test cases 
basic_airlink.run_testcases(admin_config_map, ADMIN_TESTCASES)

my_admin.finallize()   