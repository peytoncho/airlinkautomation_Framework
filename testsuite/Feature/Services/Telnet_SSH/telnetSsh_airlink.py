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

tbd_config_map = basic_airlink.get_tbd_config_data()

class TelnetSshAirlink(selenium_utilities.SeleniumAcemanager):
    def __init__(self):
        ''' TODO
        '''        
        selenium_utilities.SeleniumAcemanager.__init__(self)    
    
    def get_remote_login_server_mode(self, driver):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_TELNET_SSH)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret
    
    def get_remote_login_server_port(self,driver):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_CMN_TELNET_PORT)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret

    def get_remote_login_server_port_timeout(self,driver):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_CMN_TNET_TIMEOUT)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret
    
    def get_maximum_login_attempts(self,driver):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_SSH_MAX_LOGIN_TRY)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret
    
    def get_telnet_ssh_echo(self,driver):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_CMN_ECHO_TELNET)
        ret = self.get_element_by_name(driver, msciid_str)
        return ret
    
    def get_ssh_status(self,driver):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_STS_SSH_STATUS)
        ret = self.get_element_by_id(driver, msciid_str)
        return ret
    
    
    
    def set_remote_login_server_mode(self, driver, option):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_TELNET_SSH)
        return self.select_item_by_visible_text(driver, msciid_str, "SSH")
        
    
    def set_remote_login_server_port(self, driver, value):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_CMN_TELNET_PORT)
        return self.set_element_by_name(driver, msciid_str, value)

    def set_remote_login_server_port_timeout(self, driver, value):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_CMN_TNET_TIMEOUT)
        return self.set_element_by_name(driver, msciid_str, value)
    
    def set_maximum_login_attempts(self, driver, value):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_SSH_MAX_LOGIN_TRY)
        return self.set_element_by_name(driver, msciid_str, value)
    
    def set_telnet_ssh_echo(self, driver, value):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_CMN_ECHO_TELNET)
        return self.set_element_by_name(driver, msciid_str, value)
    
    def click_make_ssh_key(self, driver, value):
        msciid_str = str(basic_airlink.MSCIID_ALL[self.aleos_sw_ver].MSCIID_CFG_MAKE_SSH_KEYS)
        return self.set_element_by_name(driver, msciid_str, value)
    