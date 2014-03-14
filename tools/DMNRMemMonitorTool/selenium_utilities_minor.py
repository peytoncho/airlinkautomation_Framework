from selenium import webdriver   
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

import time
import sys


def login(url, username, password):

    try: 
        driver = webdriver.Firefox()                # Get local session of firefox
        driver.get(url)    # Load page
        
        time.sleep(1)     
            
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_name("Login").click()
   
    except WebDriverException:
          print "Fail on Login"
       
    finally:
        return driver
    
def navigate_wan_dmnr(driver):
    wan_tab_xpath = "//li[@id='WAN/CellularM1']/a/span"
    dmnr_tab_xpath = "//li[@id='SM1_WAN/Cellular_DMNR ConfigurationM1']/a/span"
    try:
        driver.find_element_by_xpath(wan_tab_xpath).click()
        driver.find_element_by_xpath(dmnr_tab_xpath).click()
        
    except:
        print "Fail on clicking tab"
    

def apply(driver):
    print "Apply"
    val = True
    try: 
        driver.find_element_by_id("btn_Apply").click()
        time.sleep(2)    
        driver.switch_to_alert().accept()
            
    except WebDriverException:
        print "Failed on apply"
        val = False
        
    finally: 
        return val

def reboot(driver):
    print "reboot"
    val = True
    try:             
        driver.find_element_by_id("btn_Reset").click()
        driver.switch_to_alert().accept()
            
    except WebDriverException:
        print "Failed on reboot"       
        val =  False       
    finally: 
        return val

def enable_dmnr(driver):
    print "Change to Enable"
    drop_list_id = "53000"
    Select(driver.find_element_by_name(drop_list_id)).select_by_visible_text("Enable")


def disable_dmnr(driver):
    print "Change to Disable"
    drop_list_id = "53000"
    Select(driver.find_element_by_name(drop_list_id)).select_by_visible_text("Disable")
