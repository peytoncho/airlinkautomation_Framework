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
  
class TsAdminLogging(unittest.TestCase):
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
        #logging.debug("step: login to Ace Manager")
        #device_name = self.tbd_config_map["DUTS"][0]
        
        #driver = self.se_ins.login(self.tbd_config_map[self.device_name]["ACE_URL"], self.tbd_config_map[self.device_name]["USERNAME"], self.tbd_config_map[self.device_name]["PASSWORD"])
#        ace_manager_url = self.conn_ins.get_url()
#        self.driver = self.se_ins.login(ace_manager_url, 
#                                        self.tbd_config_map[self.device_name]["USERNAME"], 
#                                        self.tbd_config_map[self.device_name]["PASSWORD"])
#        if self.driver == -1:
#            logging.debug("Login to ACEmanager faield \n")  
#            return -1
#        
#        time.sleep(self.tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])                     
        
        # step: come to Admin page from AceManager          
        self.se_ins.admin_page(self.driver)      
        
        self.driver.find_element_by_xpath("//li[@id='SM1_Admin_Log_Configure LoggingM1']/a/span").click()
        time.sleep(2)  

        # config logging parameters by ACEmanager UI
        changed  = self.se_ins.config_one_subsystem_logging(self.driver,"17001-2-2", verbosity_value, "17001-2-3",  display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(self.driver,"17001-3-2", verbosity_value, "17001-3-3",  display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(self.driver,"17001-4-2", verbosity_value, "17001-4-3",  display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(self.driver,"17001-5-2", verbosity_value, "17001-5-3",  display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(self.driver,"17001-6-2", verbosity_value, "17001-6-3",  display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(self.driver,"17001-7-2", verbosity_value, "17001-7-3",  display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(self.driver,"17001-8-2", verbosity_value, "17001-8-3",  display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(self.driver,"17001-9-2", verbosity_value, "17001-9-3",  display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(self.driver,"17001-10-2",verbosity_value, "17001-10-3", display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(self.driver,"17001-11-2",verbosity_value, "17001-11-3", display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(self.driver,"17001-12-2",verbosity_value, "17001-12-3", display_in_log_value) 
        changed += self.se_ins.config_one_subsystem_logging(self.driver,"17001-13-2",verbosity_value, "17001-13-3", display_in_log_value) 
 
        if changed:
            # Step: apply and reboot DUT
            logging.debug("step: apply and reboot DUT!")
            self.se_ins.apply_reboot(self.driver)
            
            # Step: wait till device ready
            logging.debug("step: wait till device ready ...\n" )  
            time.sleep(self.tbd_config_map[self.device_name ]["REBOOT_TIMEOUT"]) 
            
        else: 
            logging.debug("Step: logout, both verbosity and display_in_log are not changed, no reboot required \n")  
            self.se_ins.logout(self.driver)
                          
        # Step: close the AceManager web
#        logging.debug("step: close Firefox \n")  
#        self.driver.quit()  
        
        if changed:  
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
        logging.debug("step: close Firefox \n")  
        self.driver.quit()  
             
        # step: login to Ace Manager 
        logging.debug("step: login to Ace Manager")
        #device_name = self.tbd_config_map["DUTS"][0]
        #driver = self.se_ins.login(self.tbd_config_map[self.device_name]["ACE_URL"], self.tbd_config_map[self.device_name]["USERNAME"], self.tbd_config_map[self.device_name]["PASSWORD"])
        ace_manager_url = self.conn_ins.get_url()
        self.driver = self.se_ins.login(ace_manager_url, 
                                        self.tbd_config_map[self.device_name]["USERNAME"], 
                                        self.tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(self.tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])                     
        
        # step: come to Admin page from AceManager          
        self.se_ins.admin_page(self.driver)      
        
        self.driver.find_element_by_xpath("//li[@id='SM1_Admin_Log_Configure LoggingM1']/a/span").click()
        time.sleep(2)  

        # config logging parameters by ACEmanager UI
        identical  = self.se_ins.verify_one_subsystem_logging(self.driver,"17001-2-2", verbosity_value, "17001-2-3",  display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(self.driver,"17001-3-2", verbosity_value, "17001-3-3",  display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(self.driver,"17001-4-2", verbosity_value, "17001-4-3",  display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(self.driver,"17001-5-2", verbosity_value, "17001-5-3",  display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(self.driver,"17001-6-2", verbosity_value, "17001-6-3",  display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(self.driver,"17001-7-2", verbosity_value, "17001-7-3",  display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(self.driver,"17001-8-2", verbosity_value, "17001-8-3",  display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(self.driver,"17001-9-2", verbosity_value, "17001-9-3",  display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(self.driver,"17001-10-2",verbosity_value, "17001-10-3", display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(self.driver,"17001-11-2",verbosity_value, "17001-11-3", display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(self.driver,"17001-12-2",verbosity_value, "17001-12-3", display_in_log_value) 
        identical += self.se_ins.verify_one_subsystem_logging(self.driver,"17001-13-2",verbosity_value, "17001-13-3", display_in_log_value) 
                          
        # Step: close the AceManager web
#        logging.debug("step: close Firefox \n")  
#        self.driver.quit()   
        
        if identical < 0 :
            # exist unexpected in the 12 logging settings
            return False
        else:     
            return True 
 
 
    def ui_set_logging_all(self, tc_id, verbosity_value, display_in_log_value):
        '''
        
        '''    
        # step: check if devices ready    
#        logging.debug("step: check if Testbed is ready")
#        if not self.conn_ins.testbed_ready() : 
#            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
#            basic_airlink.cleanup()
#            self.self.tc_fail_counter += 1
#            return 
         
        logging.info(tc_id+' : '+'begins'+'\n')
        
        # step: configure subsystem WAN logging 
        changed = self.ui_config_allsystem_logging(verbosity_value, display_in_log_value)
        
        if changed: 
            # step: verify subsystem WAN logging setting
            indentical = self.ui_verify_allsystem_logging(verbosity_value, display_in_log_value)          
            if not indentical: 
                self.fail_flag +=1
                basic_airlink.slog("UI: verify all system logging failed")
#                basic_airlink.cleanup()
#                self.tc_fail_counter += 1
#                return 
#                     
#        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
#        basic_airlink.cleanup()  
#        self.tc_pass_counter += 1 
   
    def ui_config_subsystem_logging(self, verbosity_name, verbosity_value, display_in_log_name, display_in_log_value):
        '''  configure subsystem logging 
         Args: 
             driver - Firefox driver 
             sub_system - WAN/LAN/VPN/...
             verbosity - Critical/Error/Info/Debug
             display_in_log - yes or no 
         returns: 
             Changed  = 1
             Nochange = 0
             
        '''
                       
        # step: login to Ace Manager 
        #logging.debug("step: login to ACEmanager to config logging")
        #device_name = self.tbd_config_map["DUTS"][0]
        #driver = self.se_ins.login(self.tbd_config_map[self.device_name]["ACE_URL"], self.tbd_config_map[self.device_name]["USERNAME"], self.tbd_config_map[self.device_name]["PASSWORD"])
#        ace_manager_url = self.conn_ins.get_url()
#        self.driver = self.se_ins.login(ace_manager_url, 
#                                        self.tbd_config_map[self.device_name]["USERNAME"], 
#                                        self.tbd_config_map[self.device_name]["PASSWORD"])
#        time.sleep(self.tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])                     
        
        # step: come to Admin page from AceManager          
        self.se_ins.admin_page(self.driver)      
        
        self.driver.find_element_by_xpath("//li[@id='SM1_Admin_Log_Configure LoggingM1']/a/span").click()
        time.sleep(2)  
                    
        # config logging parameters by ACEmanager UI
        changed = self.se_ins.config_one_subsystem_logging(self.driver,
                                                           verbosity_name,
                                                           verbosity_value, 
                                                           display_in_log_name, 
                                                           display_in_log_value) 

        if changed:
            # Step: apply and reboot DUT
            logging.debug("step: apply and reboot DUT!")
            self.se_ins.apply_reboot(self.driver)
            
            # Step: wait till device ready
            logging.debug("step: wait till device ready ...\n" )  
            time.sleep(self.tbd_config_map[self.device_name]["REBOOT_TIMEOUT"]) 
 
#            # Step: close the AceManager web
#            logging.debug("step: quit Firefox \n")  
#            self.driver.quit()  
           
        else: 
            logging.debug("Step: logout, both verbosity and display_in_log are not changed, no reboot required \n")  
            self.se_ins.logout(self.driver)
                          
        # Step: close the AceManager web
#        logging.debug("step: quit Firefox \n")  
#        self.driver.quit()  
        
        if changed :  
            return 1
        else:
            return 0
 
    def ui_verify_subsystem_logging(self,verbosity_name,verbosity_value, display_in_log_name, display_in_log_value):
        ''' go to Admin page, and verify if the subsystem logging setting is expected 
        
        '''
        # Step: close the AceManager web
        logging.debug("step: quit Firefox \n")  
        self.driver.quit()  
                        
        # step: login to Ace Manager 
        logging.debug("step: login to ACEmanager to verify the setting")
        #device_name = self.tbd_config_map["DUTS"][0]
        
        #driver = self.se_ins.login(self.tbd_config_map[self.device_name]["ACE_URL"], self.tbd_config_map[self.device_name]["USERNAME"], self.tbd_config_map[self.device_name]["PASSWORD"])
        ace_manager_url = self.conn_ins.get_url()
        self.driver = self.se_ins.login(ace_manager_url, 
                                        self.tbd_config_map[self.device_name]["USERNAME"], 
                                        self.tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(self.tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])                     
        
        # step: come to Admin page from AceManager
        self.se_ins.admin_page(self.driver)      
        
        self.driver.find_element_by_xpath("//li[@id='SM1_Admin_Log_Configure LoggingM1']/a/span").click()
        time.sleep(2)  

        # step: verify subsystem logging by ACEmanager UI
        ret = self.se_ins.verify_one_subsystem_logging(self.driver,
                                                       verbosity_name,
                                                       verbosity_value, 
                                                       display_in_log_name, 
                                                       display_in_log_value) 
        
        #Step: quit the AceManaer web   
#        logging.debug("step: quit Firefox Acemanager web \n")  
#        self.driver.quit()   
       
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
#        logging.debug("step: check if Testbed is ready")
#        if not self.conn_ins.testbed_ready() : 
#            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
#            basic_airlink.cleanup()
#            self.tc_fail_counter += 1
#            return 
         
        logging.info(tc_id+' : '+'begins'+'\n')
        
        # step: configure subsystem logging 
        changed = self.ui_config_subsystem_logging(verbosity_msciid,verbosity_value, display_msciid,display_value)
        
        if changed: 
            # step: verify subsystem logging setting
            ret = self.ui_verify_subsystem_logging(verbosity_msciid,verbosity_value, display_msciid,display_value)          
            if not ret: 
#                basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
#                basic_airlink.cleanup()
                self.fail_flag += 1
#                return 
                     
#        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
#        basic_airlink.cleanup()  
#        self.tc_pass_counter += 1


#############################################
#    WAN logging tests
#############################################

    def tc_ui_config_logging_wan_celluar_critical_display_yes(self):
        ''' This test case configures logging parameter to Critical for WAN/Celluar subsystem 
        
        '''
        tc_id = "tc_ui_config_logging_wan_celluar_critical_display_yes"
        self.ui_admin_logging(tc_id, "17001-2-2", "Critical","17001-2-3","Yes")
        self.assertEqual(self.fail_flag,0)

    def tc_ui_config_logging_wan_celluar_critical_display_no(self):
        ''' This test case configures logging parameter to Critical for WAN/Celluar subsystem 
        
        '''   
        tc_id = "tc_ui_config_logging_wan_celluar_critical_display_no"
        self.ui_admin_logging(tc_id, "17001-2-2", "Critical","17001-2-3","No")
        self.assertEqual(self.fail_flag,0)
   
    def tc_ui_config_logging_wan_celluar_debug_display_yes(self):
        ''' This test case configures logging parameter to Debug level for WAN/Celluar subsystem 
            display to Yes
        '''
        tc_id = "tc_ui_config_logging_wan_celluar_debug_display_yes"
        self.ui_admin_logging(tc_id, "17001-2-2", "Debug","17001-2-3","Yes")
        self.assertEqual(self.fail_flag,0)
       
    def tc_ui_config_logging_wan_celluar_debug_display_no(self):
        ''' This test case configures logging parameter to debug level for WAN/Celluar subsystem 
            display to No
        '''    
        tc_id = "tc_ui_config_logging_wan_celluar_debug_display_no"    
        self.ui_admin_logging(tc_id, "17001-2-2", "Debug","17001-2-3","No")
        self.assertEqual(self.fail_flag,0)   
        
    def tc_ui_config_logging_wan_celluar_error_display_yes(self):
        ''' test case configure logging parameters for WAN/Celluar 
        '''
        tc_id = "tc_ui_config_logging_wan_celluar_error"
        self.ui_admin_logging(tc_id, "17001-2-2", "Error","17001-2-3","Yes")
        self.assertEqual(self.fail_flag,0)        
 
    def tc_ui_config_logging_wan_celluar_error_display_no(self):
        ''' test case configure logging parameters for WAN/Celluar 
        '''
        tc_id = "tc_ui_config_logging_wan_celluar_error"
        self.ui_admin_logging(tc_id, "17001-2-2", "Error","17001-2-3","No")
        self.assertEqual(self.fail_flag,0)                
        
    def tc_ui_config_logging_wan_celluar_info_display_yes(self):
        '''    
        '''
        # test case configure logging parameters for WAN/Celluar '''
        tc_id = "tc_ui_config_logging_wan_celluar_info_display_yes"
        self.ui_admin_logging(tc_id, "17001-2-2", "Info","17001-2-3","Yes")
        self.assertEqual(self.fail_flag,0)                


    def tc_ui_config_logging_wan_celluar_info_display_no(self):
        '''    ''' 
        
        # test case configure logging parameters for WAN/Celluar '''
        tc_id = "tc_ui_config_logging_wan_celluar_info_display_no"
        self.ui_admin_logging(tc_id, "17001-2-2", "Info","17001-2-3","No")
        self.assertEqual(self.fail_flag,0)                
 
#############################################
#    LAN logging tests
#############################################

    def tc_ui_config_logging_lan_critical_display_yes(self):
        '''
        
        '''
        tc_id = "tc_ui_config_logging_lan_critical_display_yes"
        self.ui_admin_logging(tc_id, "17001-3-2", "Critical","17001-3-3","Yes")
        self.assertEqual(self.fail_flag,0)                


    def tc_ui_config_logging_lan_critical_display_no(self):
        '''
        
        '''
        
        tc_id = "tc_ui_config_logging_lan_critical_display_no"
        self.ui_admin_logging(tc_id, "17001-3-2", "Critical","17001-3-3","No")
        self.assertEqual(self.fail_flag,0)                


    def tc_ui_config_logging_lan_debug_display_yes(self):
        '''
        
        '''
        
        tc_id = "tc_ui_config_logging_lan_debug_display_yes"
        self.ui_admin_logging(tc_id, "17001-3-2", "Debug","17001-3-3","Yes")
        self.assertEqual(self.fail_flag,0)                


    def tc_ui_config_logging_lan_debug_display_no(self):
        '''
        
        '''
        tc_id = "tc_ui_config_logging_lan_debug_display_no"
        self.ui_admin_logging(tc_id, "17001-3-2", "Debug","17001-3-3","No")
        self.assertEqual(self.fail_flag,0)                        
            
    def tc_ui_config_logging_lan_error_display_yes(self):
        '''
       
        '''
        tc_id = "tc_ui_config_logging_lan_error_display_yes"
        self.ui_admin_logging(tc_id, "17001-3-2", "Error","17001-3-3","Yes")
        self.assertEqual(self.fail_flag,0)                

    def tc_ui_config_logging_lan_error_display_no(self):
        '''
        
        
        '''
        tc_id = "tc_ui_config_logging_lan_error_display_no"
        self.ui_admin_logging(tc_id, "17001-3-2", "Error","17001-3-3","No")
        self.assertEqual(self.fail_flag,0)                 
        
    def tc_ui_config_logging_lan_info_display_yes(self):
        '''
             
        '''
        tc_id = "tc_ui_config_logging_lan_info_display_yes"
        self.ui_admin_logging(tc_id, "17001-3-2", "Info","17001-3-3","Yes")
        self.assertEqual(self.fail_flag,0)                

    def tc_ui_config_logging_lan_info_display_no(self):
        '''       
        
        '''
        tc_id = "tc_ui_config_logging_lan_info_display_no"
        self.ui_admin_logging(tc_id, "17001-3-2", "Info","17001-3-3","No")
        self.assertEqual(self.fail_flag,0)                       
        
#############################################
#  set logging all subsystem to same yes or no
#############################################

    def tc_ui_logging_all_critical_display_yes(self):
        '''
        
        '''
        
        tc_id = "tc_ui_logging_all_critcial_display_yes"
 
        self.ui_set_logging_all(tc_id, "Critical", "Yes")
        self.assertEqual(self.fail_flag, 0)     
        
        
    def tc_ui_logging_all_critical_display_no(self):
        '''
        
        '''
        
        tc_id = "tc_ui_logging_all_critical_display_no"
 
        self.ui_set_logging_all(tc_id, "Critical", "No")
        self.assertEqual(self.fail_flag, 0)     
 
        
    def tc_ui_logging_all_error_display_yes(self):
        '''
        
        '''
        
        tc_id = "tc_ui_logging_all_error_display_yes"
 
        self.ui_set_logging_all(tc_id, "Error", "Yes")
        self.assertEqual(self.fail_flag, 0)     
        
        
    def tc_ui_logging_all_error_display_no(self):
        '''
        
        '''
        
        tc_id = "tc_ui_logging_all_error_display_no"
 
        self.ui_set_logging_all(tc_id, "Error", "No")
        self.assertEqual(self.fail_flag, 0)     
        

    def tc_ui_logging_all_info_display_yes(self):
        '''
        '''
        
        tc_id = "tc_ui_logging_all_info_display_yes"
 
        self.ui_set_logging_all(tc_id, "Info", "Yes")
        self.assertEqual(self.fail_flag, 0)     
  
        
    def tc_ui_logging_all_info_display_no(self):
        ''' 
        
        '''
        tc_id = "tc_ui_logging_all_info_display_no"
 
        self.ui_set_logging_all(tc_id, "Info", "No")
        self.assertEqual(self.fail_flag, 0)     
  
        
    def tc_ui_logging_all_debug_display_yes(self):
        '''
        '''
        
        tc_id = "tc_ui_logging_all_debug_display_yes"
 
        self.ui_set_logging_all(tc_id, "Debug", "Yes")
        self.assertEqual(self.fail_flag, 0)     

       
    def tc_ui_logging_all_debug_display_no(self):
        ''' 
        
        '''
        
        tc_id = "tc_ui_logging_all_debug_display_no"
 
        self.ui_set_logging_all(tc_id, "Debug", "No")
        self.assertEqual(self.fail_flag, 0)     
        
        
    def tc_ui_config_linux_sys_log(self):
        '''test case configure linux sys log display, doesn't require reboot
        '''
               
        tc_id = "tc_ui_config_linux_sys_log"
        logging.info(tc_id+' : '+'begins\n')
        
        # step: check if devices ready    
#        logging.debug("step: check if testbed is ready")
#        if not self.conn_ins.testbed_ready() : 
#            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
#            basic_airlink.cleanup()
#            return  
# 
#        # step: login to Ace Manager 
#        logging.debug("step: login to Ace Manager")
#        #device_name = self.tbd_config_map["DUTS"][0]
#        driver = self.se_ins.login(self.tbd_config_map[self.device_name]["ACE_URL"], self.tbd_config_map[self.device_name]["USERNAME"], self.tbd_config_map[self.device_name]["PASSWORD"])
#
#        time.sleep(self.tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])                     
        
        # step: come to Admin page from AceManager          
        self.se_ins.admin_page(self.driver)      
        
        self.driver.find_element_by_xpath("//li[@id='SM1_Admin_Log_Configure LoggingM1']/a/span").click()
        time.sleep(2) 
        
        # step: config linux syslog to "Display"
        changed = self.se_ins.config_linux_syslog(self.driver, "Display")
        
        if changed: 
            #step: refresh 
            self.se_ins.apply_refresh(self.driver)      
        
        # step: verify the linux syslog setting
        indentical=self.se_ins.verify_linux_syslog(self.driver, "Display")
        
        #driver.quit()
        
        if not indentical: 
            #basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.fail_flag +=1
            #basic_airlink.cleanup()
            #return 

        time.sleep(5) 
 
        # step: config linux syslog  to "No Display"
        changed = self.se_ins.config_linux_syslog(self.driver, "No Display")
        
        if changed: 
            #step: refresh 
            self.se_ins.apply_refresh(self.driver)      
        
        # step: verify the linux syslog setting
        indentical=self.se_ins.verify_linux_syslog(self.driver, "No Display")
        
#        driver.quit()
        
        if not indentical: 
            #basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.fail_flag +=1
           
        self.assertEqual(self.fail_flag,0)                
 
    def tc_dummy(self):
        pass          
                               
#    def finallize(self): 
#        '''
#        To print out PASSED/FAILED testcases number in test report
#        '''
#        
#        print "\n passed: ", self.tc_pass_counter, " failed:", self.tc_fail_counter
#        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],"\nPassed : "+ str(self.tc_pass_counter))
#        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],"\nFailed : "+ str(self.tc_fail_counter))  
                
    
####################################################
# main  Admin test automation Aug 13, 2013 deleted Morgan
####################################################
#
#print sys.platform
#
#airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME']
#
#my_admin = TestsuiteAdmin(unittest.TestCase)
#
#        
#ADMIN_TESTCASES ={  \
#   "tc_ui_config_logging_wan_celluar_debug_display_yes"    : my_admin.tc_ui_config_logging_wan_celluar_debug_display_yes, \
#   "tc_ui_config_logging_wan_celluar_debug_display_no"     : my_admin.tc_ui_config_logging_wan_celluar_debug_display_no, \
#   "tc_ui_config_logging_wan_celluar_info_display_yes"     : my_admin.tc_ui_config_logging_wan_celluar_info_display_yes, \
#   "tc_ui_config_logging_wan_celluar_info_display_no"      : my_admin.tc_ui_config_logging_wan_celluar_info_display_no, \
#   "tc_ui_config_logging_wan_celluar_error_display_yes"    : my_admin.tc_ui_config_logging_wan_celluar_error_display_yes, \
#   "tc_ui_config_logging_wan_celluar_error_display_no"     : my_admin.tc_ui_config_logging_wan_celluar_error_display_no, \
#   "tc_ui_config_logging_wan_celluar_critical_display_yes" : my_admin.tc_ui_config_logging_wan_celluar_critical_display_yes, \
#   "tc_ui_config_logging_wan_celluar_critical_display_no"  : my_admin.tc_ui_config_logging_wan_celluar_critical_display_no, \
#   "tc_ui_config_logging_lan_debug_display_yes"            : my_admin.tc_ui_config_logging_lan_debug_display_yes, \
#   "tc_ui_config_logging_lan_debug_display_no"             : my_admin.tc_ui_config_logging_lan_debug_display_no, \
#   "tc_ui_config_logging_lan_info_display_yes"             : my_admin.tc_ui_config_logging_lan_info_display_yes, \
#   "tc_ui_config_logging_lan_info_display_no"              : my_admin.tc_ui_config_logging_lan_info_display_no, \
#   "tc_ui_config_logging_lan_error_display_yes"            : my_admin.tc_ui_config_logging_lan_error_display_yes, \
#   "tc_ui_config_logging_lan_error_display_no"             : my_admin.tc_ui_config_logging_lan_error_display_no, \
#   "tc_ui_config_logging_lan_critical_display_yes"         : my_admin.tc_ui_config_logging_lan_critical_display_yes, \
#   "tc_ui_config_logging_lan_critical_display_no"          : my_admin.tc_ui_config_logging_lan_critical_display_no, \
#   "tc_ui_logging_all_critical_display_yes"                : my_admin.tc_ui_logging_all_critical_display_yes, \
#   "tc_ui_logging_all_critical_display_no"                 : my_admin.tc_ui_logging_all_critical_display_no, \
#   "tc_ui_logging_all_error_display_yes"                   : my_admin.tc_ui_logging_all_error_display_yes, \
#   "tc_ui_logging_all_error_display_no"                    : my_admin.tc_ui_logging_all_error_display_no, \
#   "tc_ui_logging_all_info_display_yes"                    : my_admin.tc_ui_logging_all_info_display_yes, \
#   "tc_ui_logging_all_info_display_no"                     : my_admin.tc_ui_logging_all_info_display_no, \
#   "tc_ui_logging_all_debug_display_yes"                   : my_admin.tc_ui_logging_all_debug_display_yes, \
#   "tc_ui_logging_all_debug_display_no"                    : my_admin.tc_ui_logging_all_debug_display_no, \
#   "tc_ui_config_linux_sys_log"                            : my_admin.tc_ui_config_linux_sys_log, \
#   "tc_ui_viewer_change_password"                          : my_admin.tc_ui_viewer_change_password, \
#   "tc_ui_user_change_password"                            : my_admin.tc_ui_user_change_password, \
#   "tc_ui_factory_reset"                                   : my_admin.tc_ui_factory_reset, \
#   "tc_at_factory_reset"                                   : my_admin.tc_at_factory_reset, \
#   "tc_memory_cpu_root_user"                               : my_admin.tc_memory_cpu_root_user, \
#   "tc_log_reset_check_root_user"                          : my_admin.tc_log_reset_check_root_user,\
#   "tc_check_network_state_root_user"                      : my_admin.tc_check_network_state_root_user,\
#   "tc_check_gps_data_root_user"                           : my_admin.tc_check_gps_data_root_user\
#           }
#    
## load testsuite config and testbed config
#
#fo=open(airlinkautomation_home_dirname+'/testsuite/Admin/admin_test_conf.yml','r')
#admin_config_map = yaml.load(fo)
#fo.close()
#
## run test cases 
#basic_airlink.run_testcases(admin_config_map, ADMIN_TESTCASES)
#
#my_admin.finallize()   