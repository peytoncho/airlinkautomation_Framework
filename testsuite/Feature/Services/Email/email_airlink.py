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
import selenium_utilities

class EmailAirlink(selenium_utilities.SeleniumAcemanager):
    def __init__(self):
        ''' TODO
        '''        
        selenium_utilities.SeleniumAcemanager.__init__(self)    
        self.tab = "Services"
        self.subtab = "Email_SMTP"
    def get_smtp_ip_address(self,driver):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_CMN_SMTP_SERVER)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret
    
    def get_smtp_from_email_address(self, driver):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_CMN_SMTP_FROM)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret
    
    def get_smtp_username(self,driver):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_CMN_SMTP_USER)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret
    
    def get_smtp_password(self,driver):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_CMN_SMTP_PASSWD)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret       
    
    def get_smtp_message_subject(self, driver):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_CMN_SMTP_SUBJECT)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret
    
    def get_smtp_quick_test_destination(self,driver):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_CMN_SMTP_TEST_DEST)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret
    
    def get_smtp_test_status(self,driver):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_CMN_SMTP_TEST_STS)
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
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_CMN_SMTP_TEST_DEST)
        return self.set_element_by_name(driver, msciid_str, value)
        
  
    def click_smtp_quick_test(self,driver):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_CMN_SMTP_QUICK_TEST)
        driver.find_element_by_name(msciid_str).click()
        driver.switch_to_alert().accept()
        driver.switch_to_alert().accept()