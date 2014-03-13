################################################################################
#
# This module provides WAN UI operation using Selenium lib. 
# Company: Sierra Wireless
# Time: Jan 9, 2014
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
import sys
import unittest
import logging
import basic_airlink
import msciids
import selenium_utilities

tbd_config_map = basic_airlink.get_tbd_config_data()

class LowpowerAirlink(selenium_utilities.SeleniumAcemanager):
    ''' This class implements Selenium Services UI operation methods by ACEmanager Web, 
    e.g. navigate pages, get/set Web elements. 
    if methods don't include tab/subtab parameters, that needs to 
    call navigate_subtab() first to navigate the specified page.
    
    ''' 
    
    def __init__(self):
        ''' TODO
        '''
        
        selenium_utilities.SeleniumAcemanager.__init__(self)
#        self.error_flag = 0
#        self.device_name = tbd_config_map["DUTS"][0]
#        self.device_model = tbd_config_map[self.device_name]["MODEL"]

    def set_low_power_mode(self, driver, lpm=0): 
        ''' user enter the APN by ACEmanager Services/Low Power web page.
        Args: 
            diver : FF/IE web driver
            lpm: low power mode (0-6), 0 - Diable. 
        Returns: 
            True/False 
        '''

        basic_airlink.slog("Step: Set Low Power Mode")  
        msciid_str = str(msciids.MSCIID_CFG_CMN_LOW_PWR_MODE)

        ret = self.get_element_by_name(driver,msciid_str) 
        
        if (ret != lpm):
            
            basic_airlink.slog("Need change LPM " + ret)  
            return self.set_element_by_name(driver, msciid_str, str(lpm))
        
        else:
            
            basic_airlink.slog("No need change LPM " + ret)  
            return True
                  

    
    def get_low_power_mode(self, driver):
        ''' get APN in use in WAN/Celluar page
        Args: 
            diver : FF/IE web driver
        Returns: 
             APN in use
        '''

        msciid_str = str(msciids.MSCIID_CFG_CMN_LOW_PWR_MODE)
        ret = self.get_element_by_name(driver,msciid_str)     
        return ret
    
class EmailAirlink(selenium_utilities.SeleniumAcemanager):
    def __init__(self):
        ''' TODO
        '''        
        selenium_utilities.SeleniumAcemanager.__init__(self)    
        self.tab = "Services"
        self.subtab = "Email_SMTP"
    def get_smtp_ip_address(self,driver):
        msciid_str = str(msciids.MSCIID_CFG_CMN_SMTP_SERVER)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret
    
    def get_smtp_from_email_address(self, driver):
        msciid_str = str(msciids.MSCIID_CFG_CMN_SMTP_FROM)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret
    
    def get_smtp_username(self,driver):
        msciid_str = str(msciids.MSCIID_CFG_CMN_SMTP_USER)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret
    
    def get_smtp_password(self,driver):
        msciid_str = str(msciids.MSCIID_CFG_CMN_SMTP_PASSWD)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret       
    
    def get_smtp_message_subject(self, driver):
        msciid_str = str(msciids.MSCIID_CFG_CMN_SMTP_SUBJECT)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret
    
    def get_smtp_quick_test_destination(self,driver):
        msciid_str = str(msciids.MSCIID_CFG_CMN_SMTP_TEST_DEST)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret
    
    def get_smtp_test_status(self,driver):
        msciid_str = str(msciids.MSCIID_CFG_CMN_SMTP_TEST_STS)
        ret = self.get_element_by_id(driver, msciid_str)
        return ret
    
    
    def set_smtp_ip_address(self,driver,value):
        pass
    
    def set_smtp_from_email_address(self, driver, value):
        pass
    
    def set_smtp_username(self, driver, value):
        pass
    
    def set_smtp_message_subject(self, driver, value):
        pass
    
    def set_smtp_quick_test_destination(self, driver, value):
        msciid_str = str(msciids.MSCIID_CFG_CMN_SMTP_TEST_DEST)
        return self.set_element_by_name(driver, msciid_str, value)
        
  
    def click_smtp_quick_test(self,driver):
        msciid_str = str(msciids.MSCIID_CFG_CMN_SMTP_QUICK_TEST)
        driver.find_element_by_name(msciid_str).click()
        driver.switch_to_alert().accept()
        driver.switch_to_alert().accept()
    
    
class TelnetSshAirlink(selenium_utilities.SeleniumAcemanager):
    def __init__(self):
        ''' TODO
        '''        
        selenium_utilities.SeleniumAcemanager.__init__(self)    
    
    def get_remote_login_server_mode(self, driver):
        msciid_str = str(msciids.MSCIID_CFG_TELNET_SSH)
        ret = self.get_element_by_id(driver, msciid_str)
        return ret
    
    def get_remote_login_server_port(self,driver):
        msciid_str = str(msciids.MSCIID_CFG_CMN_TELNET_PORT)
        ret = self.get_element_by_id(driver, msciid_str)
        return ret

    def get_remote_login_server_port_timeout(self,driver):
        msciid_str = str(msciids.MSCIID_CFG_CMN_TNET_TIMEOUT)
        ret = self.get_element_by_id(driver, msciid_str)
        return ret
    
    def get_maximum_login_attempts(self,driver):
        msciid_str = str(msciids.MSCIID_CFG_SSH_MAX_LOGIN_TRY)
        ret = self.get_element_by_id(driver, msciid_str)
        return ret
    
    def get_telnet_ssh_echo(self,driver):
        msciid_str = str(msciids.MSCIID_CFG_CMN_ECHO_TELNET)
        ret = self.get_element_by_id(driver, msciid_str)
        return ret
    
    def get_ssh_status(self,driver):
        msciid_str = str(msciids.MSCIID_STS_SSH_STATUS)
        ret = self.get_element_by_id(driver, msciid_str)
        return ret
    
    
    
    def set_remote_login_server_mode(self, driver, option):
        msciid_str = str(msciids.MSCIID_CFG_TELNET_SSH)
        return self.select_item_by_visible_text(driver, msciid_str, "SSH")
        
    
    def set_remote_login_server_port(self, driver, value):
        msciid_str = str(msciids.MSCIID_CFG_CMN_TELNET_PORT)
        return self.set_element_by_name(driver, msciid_str, value)

    def set_remote_login_server_port_timeout(self, driver, value):
        msciid_str = str(msciids.MSCIID_CFG_CMN_TNET_TIMEOUT)
        return self.set_element_by_name(driver, msciid_str, value)
    
    def set_maximum_login_attempts(self, driver, value):
        msciid_str = str(msciids.MSCIID_CFG_SSH_MAX_LOGIN_TRY)
        return self.set_element_by_name(driver, msciid_str, value)
    
    def set_telnet_ssh_echo(self, driver, value):
        msciid_str = str(msciids.MSCIID_CFG_CMN_ECHO_TELNET)
        return self.set_element_by_name(driver, msciid_str, value)
    
    def click_make_ssh_key(self, driver, value):
        msciid_str = str(msciids.MSCIID_CFG_MAKE_SSH_KEYS)
        return self.set_element_by_name(driver, msciid_str, value)
    
    
    
    
    
