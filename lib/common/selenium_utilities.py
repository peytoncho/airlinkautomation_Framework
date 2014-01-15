################################################################################
#
# This module provides UI operation using Selenium lib. 
# Company: Sierra Wireless
# Time: Feb 19, 2013
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
import os

airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")

basic_airlink.append_sys_path()
tbd_config_map = basic_airlink.get_tbd_config_data()

class SeleniumAcemanager(unittest.TestCase):
    ''' Selenium UI operation functions by ACEmanager   
    ''' 
    
    def __init__(self):
        ''' TODO
        '''
        self.error_flag = 0
    
        
    def get_element_by_id(self, driver, id_str):
        '''
        find item by id and get its text 
        Args:        
            driver - Firefox/IE web driver
            id_str - id string 
        returns: 
            the text that read from web
            
        '''
        
        txt = ""
        try:
            txt= driver.find_element_by_id(id_str).text
            basic_airlink.slog("MSCIID_"+id_str+ " : "+ txt)
        
        except NoSuchElementException:
            
            basic_airlink.slog("get_element_by_id: cannot find " +id_str)
            self.error_flag+=1
        
        finally: 
            return txt   
  
    def get_element_by_name(self, driver, name, attribute="value"):
        '''
        find item by name and get its value 
        Args:        
            driver - Firefox/IE web driver
            name -  string element name
            attribute - element attribute ("value"/"title")
        returns: 
            the value that read from web
            
        '''
        
        val = ""
        try:
            if attribute == "value"  or  attribute == "title":
                val= driver.find_element_by_name(name).get_attribute(attribute)
                basic_airlink.slog(name+"="+val)
            else:
                basic_airlink.slog("wrong attribute of element")
            
        except NoSuchElementException:
            
            basic_airlink.slog("get_element_by_id: cannot find " + name)
            self.error_flag+=1
        
        finally: 
            logging.debug("\n " +name +" return value = " + val)          
            return val
                 
    def get_element_by_xpath(self, driver, x_path, get_text_flag=False):
        '''
        find item by xpath
        Args:        
            driver - Firefox/IE web driver
            x_path -  string, xpath of the item
            get_text_flag  Flase  find element by xpath 
                           True  find element by xpath and get text
        returns: 
            the value that read from web page
            
        '''
        
        val = ""
        try:
            if not get_text_flag: 
                val= driver.find_element_by_xpath(x_path)
            else: 
                val= driver.find_element_by_xpath(x_path).text
            
        except NoSuchElementException:
            
            basic_airlink.slog("get_element_by_xpath: cannot find " + x_path)
            self.error_flag+=1
        
        finally: 
            basic_airlink.slog(x_path)          
            return val

    def select_box_by_xpath(self, driver, x_path):
        '''
        find item by xpath
        Args:        
            driver - Firefox/IE web driver
            x_path -  string, xpath of the item
        returns: 
            the value that read from web
            
        '''
        
        val = True
        try:
            driver.find_element_by_xpath(x_path).click()
            print x_path,"\n"
            
        except:
            
            basic_airlink.slog("select box failed at " + x_path)
            val = False
            self.error_flag+=1
            
        finally: 
            basic_airlink.slog(x_path)          
            return val

    def select_element_by_css_selector(self, driver, css_selector):
        '''
        find item by css selector
        Args:        
            driver - Firefox/IE web driver
            css_selector -  string, css_selector of the item
        returns: 
            the value that read from web
            
        '''
        
        val = True
        try:
            driver.find_element_by_css_selector(css_selector).click()
            print css_selector,"\n"
            
        except:
            
            basic_airlink.slog("select element failed at " + css_selector)
            val = False
            self.error_flag+=1
            
        finally: 
            basic_airlink.slog(css_selector)          
            return val
                           
    def set_element_by_id(self, driver, id_str, val_str):
        '''
        find item by id and set the value
        '''
        try:
            driver.find_element_by_id(id_str).clear()
            driver.find_element_by_id(id_str).send_keys(val_str)
        
        except NoSuchElementException:
            basic_airlink.slog("set_element_by_id: cannot find " + id_str)
            self.error_flag+=1
            return False
        
        return True
         
        
    def set_element_by_name(self, driver, name_str, val_str):
        '''
        find item by name and set the value
        '''        
        try:
            driver.find_element_by_name(name_str).clear()
            driver.find_element_by_name(name_str).send_keys(val_str)
        
        except NoSuchElementException:
            basic_airlink.slog("set_element_by_name: cannot find " + name_str)
            self.error_flag+=1
            return False
                
        return True    
        
    def select_item_by_visible_text(self, driver, name_str, select_str):
        '''
        select item by visible text
        
        '''        
        basic_airlink.slog("select_item_by_text: name="+name_str+",select="+select_str+"\n")
        try: 
            Select(driver.find_element_by_name(name_str)).select_by_visible_text(select_str)
        except NoSuchElementException:
            basic_airlink.slog("select_item_by_text: cannot find " + name_str)
            self.error_flag+=1
            return False
                
        return True

    def se_close_alert_and_get_its_text(self, driver):
        '''
        TODO
        
        '''
        try:
            alert = self.driver.switch_to_alert()
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert.text
        finally: self.accept_next_alert = True        
 
 
    def apply_reboot(self, driver):
        ''' ACEmanager UI: apply and reboot DUT   
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            True  - successful 
            False - exception appears
        ''' 
        try: 
            driver.find_element_by_id("btn_Apply").click()
            time.sleep(5)
            driver.switch_to_alert().accept()
                 
            driver.find_element_by_id("btn_Reset").click()
            time.sleep(5)
    
            driver.switch_to_alert().accept() 
            
        except WebDriverException: 
            
            logging.debug(" apply and reboot: pop up exception \n")
            return False
        
        return True
 
 
    def apply_refresh(self, driver):
        ''' Acemanager UI: apply and refresh DUT   
        args: 
            driver - Firefox/IE web driver
        returns: 
            True  - successful 
            False - exception appears  (TODO)
        ''' 
        
        driver.find_element_by_id("btn_Apply").click()
        time.sleep(5)
        driver.switch_to_alert().accept()
             
        driver.find_element_by_id("btn_Refresh").click()
        time.sleep(5)

        #driver.switch_to_alert().accept()        

        return True
       
       
    def apply(self, driver):
        ''' Acemanager UI: apply DUT   
        args: 
            driver - Firefox/IE web driver
        returns: 
            None
        '''
        try: 
            driver.find_element_by_id("btn_Apply").click()
            time.sleep(2)    
            driver.switch_to_alert().accept()
            
        except WebDriverException:
            
            logging.debug(" apply: failed, and pop up exception\n")
            return False
        
        return True           

    def refresh(self, driver):
        ''' Acemanager UI: refresh   
        args: 
            driver - Firefox/IE web driver
        returns: 
            None

        '''
        driver.find_element_by_id("btn_Refresh").click()
        time.sleep(2)
 
    def refresh_all(self, driver):
        ''' Acemanager UI: refresh all
        args: 
            driver - Firefox/IE web driver
        returns: 
            None

        '''

        driver.find_element_by_id("btn_All").click()
        time.sleep(2)
        
        driver.switch_to_alert().accept()    
         
        
    def reboot(self, driver):
        ''' Acemanager UI: reboot   
        args: 
            driver - Firefox/IE web driver
        returns: 
            None

        ''' 
        try: 
            
            driver.find_element_by_id("btn_Reset").click()
            driver.switch_to_alert().accept()
            
        except WebDriverException:
            
            logging.debug(" reboot: failed, and pop up exception\n")
            return False
        
        return True           
        

    def login(self, url, username, password):
        ''' ACEmanager UI: login   
        
        Args: 
                 url         web url
                 username    username 
                 password    password
        
        Returns: 
                driver - Firefox/IE web driver
        Global: 
                error_flag  not 0 if error exist

        '''
        logging.debug("\n"+url+" "+username+" "+password)
        try: 
            if tbd_config_map["BROWSER"] == "FF":
                driver = webdriver.Firefox()                # Get local session of firefox
            else:
                driver = webdriver.Ie()                     # Get local session of IE

            driver.get(url)    # Load page
            # assert "ACEmanager" in driver.title
        
            time.sleep(1)     
            driver.find_element_by_id("username").clear()
            driver.find_element_by_id("username").send_keys(username)
            driver.find_element_by_id("password").clear()
            driver.find_element_by_id("password").send_keys(password)
            driver.find_element_by_name("Login").click()

        except WebDriverException:
          
            logging.debug(" login: failed, and pop up web driver exception\n")
            self.error_flag += 1
        
        finally:
            return driver  

         
    
    def logout(self, driver):
        ''' Acemanager UI: logout   
        args: 
            driver - Firefox/IE web driver
        returns: 
            none
        '''
        driver.find_element_by_css_selector("span.DMenuCont").click()
 
 
    def quit(self, driver):
        ''' Acemanager UI: quit Firefox browser   
        args: 
            driver - Firefox/IE web driver
        returns: 
            none
        '''
        try: 
            
            driver.quit()
            
        except WebDriverException:
          
            logging.debug(" Web quit: failed, and pop up exception\n")
            self.error_flag+=1
        
        finally:
            return 
      
    def factory_reset(self, driver):        
        '''  reset to factory default by AceManager/Selenium
        Args:
            driver: Firefox browser 
        Returns:
            True: successful
            False: failed 
        
        '''
        basic_airlink.slog("Web UI factory reset")
        try: 
            
            driver.find_element_by_css_selector("#AdminM1 > a > span").click()
            
            driver.find_element_by_css_selector("#SM1_Admin_AdvancedM1 > a > span").click()
            
            driver.find_element_by_id("b5108").click()
            time.sleep(5)
            driver.switch_to_alert().accept()  
            
        except WebDriverException: 
            
            basic_airlink.slog("Pop up exception")
            return False
        
        return True  
    
    
    def get_net_ip(self, driver):
        ''' get NET IP by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            phone number
        '''
        msciid_str = str(msciids.MSCIID_STS_NETWORK_IP)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret
    

    def get_phone_num(self, driver):
        ''' get phone number by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            phone number
        '''

        msciid_str = str(msciids.MSCIID_INF_PHONE_NUM)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret
    
 
    def get_network_ip(self, driver):
        ''' get network IP by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            network IP
        '''

        msciid_str = str(msciids.MSCIID_STS_NETWORK_IP)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret     

    def get_network_state(self, driver):
        ''' get network state by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            network state
        '''

        msciid_str = str(msciids.MSCIID_STS_NETWORK_STATE)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret  
    
    def get_network_rssi(self, driver):
        ''' get network RSSI by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            network RSSI
        '''

        msciid_str = str(msciids.MSCIID_STS_NETWORK_RSSI)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret  
    
    def get_gprs_cell_info(self, driver):
        ''' get GPRS cell info by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            GPRS cell info
        '''

        msciid_str = str(msciids.MSCIID_STS_GPRS_CELL_INFO)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret  
    
    def get_network_service(self, driver):
        ''' get network service by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            network service
        '''

        msciid_str = str(msciids.MSCIID_STS_NETWORK_SERVICE)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret  
    
    def get_aleos_sw_ver(self, driver):
        ''' get ALEOS SW version by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            ALEOS SW version
        '''

        msciid_str = str(msciids.MSCIID_INF_ALEOS_SW_VER)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret  
    
    
    def get_cdma_1xecio(self, driver):
        ''' get CDMA 1x ECIO by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            CDMA 1x ECIO
        '''

        msciid_str = str(msciids.MSCIID_STS_CDMA_1XECIO)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret  
    
    def get_gprs_ecio(self, driver):
        ''' get GPRS ECIO by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            GPRS ECIO
        '''

        msciid_str = str(msciids.MSCIID_STS_GPRS_ECIO)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret  
    
    def get_network_channel(self, driver):
        ''' get network channel by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            network IP
        '''

        msciid_str = str(msciids.MSCIID_STS_NETWORK_CHANNEL)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret  
    
    def get_modem_sent(self, driver):
        ''' get network IP by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            Bytes sent
        '''

        msciid_str = str(msciids.MSCIID_STS_MODEM_SENT)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret  
    
    def get_modem_received(self, driver):
        ''' get bytes received by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            bytes received
        '''

        msciid_str = str(msciids.MSCIID_STS_MODEM_RECV)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret     
 
    def get_modem_name(self, driver):
        ''' get modem name by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            modem name
        '''

        msciid_str = str(msciids.MSCIID_CFG_CMN_MDM_NAME)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret   
 
    def get_xcard_type(self, driver):
        ''' get X card type by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            X card type
        '''

        msciid_str = str(msciids.MSCIID_X_CARD_TYPE)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret  
 
    def get_xcard_state(self, driver):
        ''' get X card state by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            X card state
        '''

        msciid_str = str(msciids.MSCIID_STS_X_CARD_STATE)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret 


    def get_modem_sw_ver(self, driver):
        ''' get modem SW version by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            modem SW version
        '''

        msciid_str = str(msciids.MSCIID_INF_MODEM_SW_VER)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret 

    def get_lte_rsrp(self, driver):
        ''' get LTE RSRP by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            LTE RSRP
        '''

        msciid_str = str(msciids.MSCIID_STS_LTE_RSRP)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret


    def get_lte_rsrq(self, driver):
        ''' get LTE RSRQ by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
            LTE RSRQ
        '''

        msciid_str = str(msciids.MSCIID_STS_LTE_RSRQ)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret


    def get_modem_id(self, driver):
        ''' get modem ID by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
         MOdem ID
        '''

        msciid_str = str(msciids.MSCIID_INF_MODEM_ID)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret
 
 
 
    def get_gprs_simid(self, driver):
        ''' get GPRS SIMID by ACEmanager Web UI Status-> WAN/Cellular page
        Args: 
            driver FF web driver 
        Returns: 
            GPRS SIM ID
        '''

        msciid_str = str(msciids.MSCIID_STS_GPRS_SIMID)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret
    
    
    def get_apn_current(self, driver):
        ''' get current APN by ACEmanager Web UI Status -> WAN/Cellular page
        Args: 
            driver FF web driver 
        Returns: 
            current APN
        '''

        msciid_str = str(msciids.MSCIID_STS_CMN_APN_CURRENT)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret
    
    
    def get_gprs_imsi(self, driver):
        ''' get GPRS IMSI by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
           GPRS IMSI
        '''

        msciid_str = str(msciids.MSCIID_STS_GPRS_IMSI)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret    
    
    
    def get_gprs_cell_id(self, driver):
        ''' get GPRS CEll ID by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
           GPRS Cell ID
        '''

        msciid_str = str(msciids.MSCIID_STS_GPRS_CELL_ID)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret    
    
        
    def get_gprs_lac(self, driver):
        ''' get GPRS LAC by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
           GPRS LAC
        '''

        msciid_str = str(msciids.MSCIID_STS_GPRS_LAC)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret    
    
        
    def get_gprs_bsic(self, driver):
        ''' get GPRS BSIC by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
           GPRS BSIC
        '''

        msciid_str = str(msciids.MSCIID_STS_GPRS_BSIC)

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret    
    
        
    def get_keepalive_ip(self, driver):
        ''' get Keepalive IP Address by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
           Keepalive IP Address
        '''

        msciid_str = str(msciids.MSCIID_CFG_CMN_IPPING_ADDR)+"-d1"

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret    
    
        
    def get_keepalive_ping_time(self, driver):
        ''' get eepalive Ping Time (min) by ACEmanager Web UI Status/Home page
        Args: 
            driver FF web driver 
        Returns: 
           Keepalive Ping Time (min)
        '''

        msciid_str = str(msciids.MSCIID_CFG_CMN_IPPING_PERIOD ) +'-d1'

        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret    
      
                                     
    def config_one_subsystem_logging(self, driver, verbosity_name, verbosity_value, display_in_log_name, display_in_log_value):
        '''  configure subsystem logging 
         args: 
             driver         - Firefox driver 
             sub_system     - WAN/LAN/VPN/...
             verbosity      - Critical/Error/Info/Debug
             display_in_log - yes or no 
         
         returns: 
              1 - changed 
              0 - no change
      
         '''    
        changed = 0 
        
        # read the existing verbosity value 
        val = int(driver.find_element_by_name(verbosity_name).get_attribute("value"))   
        
        # compare the existing value to the value to set
        if val != basic_airlink.verbosity_map[verbosity_value]:    
            
            # the existing value is different from the value to set            
            self.select_item_by_visible_text(driver, verbosity_name, verbosity_value)        
            logging.debug("  Config:: verbosity changed !! the existing: " + str(val) + ", the value to set: " +str(basic_airlink.verbosity_map[verbosity_value]))
            changed = 1
            
        else: 

            # the existing value is identical to the value to set, no need to set again           
            logging.debug("  Config:: verbosity no change")
       
        time.sleep(1)   
        
        val = int(driver.find_element_by_name(display_in_log_name).get_attribute("value")) 
         
        if val != basic_airlink.yes_no_map[display_in_log_value]:  
             
            # the existing value is different from the value to set            
            self.select_item_by_visible_text(driver, display_in_log_name, display_in_log_value)   
            logging.debug(" Config:: display_in_log changed !! the existing: " + str(val) + ", the value to set: " +str(basic_airlink.yes_no_map[display_in_log_value]))
            changed = 1
            
        else: 
            # the existing value is identical to the value to set, no need to set again           
            logging.debug(" Config:: display_in_log no change")
             
        return changed      

        
    def verify_one_subsystem_logging(self, driver, verbosity_name, verbosity_value, display_in_log_name, display_in_log_value):
        '''  verify one subsystem logging setting
         args: 
             driver         - Firefox driver 
             sub_system     - WAN/LAN/VPN/...
             verbosity      - Critical/Error/Info/Debug
             display_in_log - yes or no 
         
         returns: 
              0 - identical
             -1 - different 
      
         '''    
        ret = 0 

        val = int(driver.find_element_by_name(verbosity_name).get_attribute("value"))
        
        if val != basic_airlink.verbosity_map[verbosity_value]:                
            logging.debug(" verify:: verbosity is different")
            ret = -1
        else: 
            logging.debug(" verify:: verbosity is identical")

        time.sleep(1)   
        
        val = int(driver.find_element_by_name(display_in_log_name).get_attribute("value"))           
        if val != basic_airlink.yes_no_map[display_in_log_value]:   
            logging.debug(" verify:: display_in_log is different")
            ret = -1
        else: 
            logging.debug(" verify:: display_in_log is identical")
            
        return ret       
 

    def config_linux_syslog(self, driver, display_flag_value): 
        ''' config the linux system log display to "Display" /"No Display"
        
        '''
        
        changed = 0 
        display_flag_name = str(msciids.MSCIID_CFG_SYSLOG_LOGFILTER)
        val = int(driver.find_element_by_name(display_flag_name).get_attribute("value"))

        if val != basic_airlink.display_map[display_flag_value]:                
            self.select_item_by_visible_text(driver, display_flag_name, display_flag_value)        
            logging.debug(" Config:: Linux syslog display changed! ")
            changed = 1
        else: 
            logging.debug(" Config:: Linux syslog display no change ")
             
        return changed      
 
 
    def verify_linux_syslog(self, driver, display_flag_value): 
        '''verify if the linux system log display"Display" /"No Display"  
        
        '''
         
        ret = 1
        display_flag_name = str(msciids.MSCIID_CFG_SYSLOG_LOGFILTER)
        val = int(driver.find_element_by_name(display_flag_name).get_attribute("value"))

        if val != basic_airlink.display_map[display_flag_value]:                
            logging.debug(" Verify:: Linux syslog display changed! ")
            ret = -1
        else: 
            logging.debug(" Verify:: Linux syslog display no change")
             
        return ret   

 
    def status_page(self, driver):
        ''' ACEmanager comes to status page
        
        '''
        basic_airlink.slog("step: from Ace Manager come to status page: ")
        #driver.find_element_by_id("StatusM1").click()
        #driver.find_element_by_css_selector("#SM1_Status_HomeM1 > a > span").click()
        #if (device_name == "GX400_MC8705_ROW"):
        driver.find_element_by_css_selector("#StatusM1 > a > span").click()
        time.sleep(1)     
        

    def status_wan_page(self, driver):
        ''' ACEmanager comes to Status/WAN page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            None
        '''
        basic_airlink.slog("step: from Ace Manager come to Status/WAN page: ")
        driver.find_element_by_xpath("//li[@id='SM1_Status_WAN/CellularM1']/a/span").click()
        time.sleep(2) 
 
 
    def status_lan_page(self, driver):
        ''' ACEmanager comes to Status/LAN page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            None
        '''
        basic_airlink.slog("step: from Ace Manager come to Status/LAN page: ")
        driver.find_element_by_id("S_SM1_Status_LANM1").click()
        time.sleep(2) 
        
 
    def status_vpn_page(self, driver):
        ''' ACEmanager comes to Status/VPN page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            None
        '''
        basic_airlink.slog("step: from Ace Manager come to Status/VPN page: ")
        driver.find_element_by_css_selector("#SM1_Status_VPNM1 > a > span").click()
        time.sleep(2) 
 
  
    def status_security_page(self, driver):
        ''' ACEmanager comes to Status/Security page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            None
        '''
        basic_airlink.slog("step: from Ace Manager come to Status/Security page: ")
        driver.find_element_by_css_selector("#SM1_Status_SecurityM1 > a > span").click()
        time.sleep(2) 
        
 
    def status_services_page(self, driver):
        ''' ACEmanager comes to Status/Services page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            None
        '''
        basic_airlink.slog("step: from Ace Manager come to Status/Services page: ")
        driver.find_element_by_css_selector("#SM1_Status_ServicesM1 > a > span").click()
        time.sleep(2) 
        
    def status_gps_page(self, driver):
        ''' ACEmanager comes to Status/GPS page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            None
        '''
        basic_airlink.slog("step: from Ace Manager come to Status/GPS page: ")
        driver.find_element_by_css_selector("#SM1_Status_GPSM1 > a > span").click()
        time.sleep(2) 
        
    def status_serial_page(self, driver):
        ''' ACEmanager comes to Status/Serial page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            None
        '''
        basic_airlink.slog("step: from Ace Manager come to Status/Serial page: ")
        driver.find_element_by_css_selector("#SM1_Status_SerialM1 > a > span").click()
        time.sleep(2) 
        
    def status_applications_page(self, driver):
        ''' ACEmanager comes to Status/Applications page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            None
        '''
        basic_airlink.slog("step: from Ace Manager come to Status/Applications page: ")
        driver.find_element_by_css_selector("#SM1_Status_ApplicationsM1 > a > span").click()
        time.sleep(2) 
        
    def status_about_page(self, driver):
        ''' ACEmanager comes to Status/SAbout page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            None
        '''
        basic_airlink.slog("step: from Ace Manager come to Status/About page: ")
        driver.find_element_by_css_selector("#SM1_Status_AboutM1 > a > span").click()
        time.sleep(2) 
                                    
    def wan_page(self, driver):
        ''' ACEmanager comes to WAN page
        
        '''
        basic_airlink.slog("step: from Ace Manager come to WAN page: ")
        #driver.find_element_by_id("WAN/CellularM1").click()
        driver.find_element_by_xpath("//li[@id='WAN/CellularM1']/a/span").click()
        time.sleep(2)     

    def lan_page(self, driver):
        ''' ACEmanager comes to LAN page
        
        Args:
            driver FF web driver 
        
        '''
        basic_airlink.slog("step: from ACEmanager come to LAN page ")
        driver.find_element_by_id("S_LANM1").click()
        time.sleep(2)     

    def lan_dhcp_addressing_page(self, driver):
        ''' ACEmanager comes to LAN/DHCP addressing web page
        
        Args:
            driver: FF web driver 
        
        '''
        basic_airlink.slog("step: from ACEmanager come to LAN/Ethernet page ")
        driver.find_element_by_xpath("//li[@id='SM1_LAN_DHCP/AddressingM1']/a/span").click()
        time.sleep(2)  
        
    def lan_ethernet_page(self, driver):
        ''' ACEmanager comes to LAN/Ethernet web page
        
        Args:
            driver: FF web driver 
        
        '''
        basic_airlink.slog("step: from ACEmanager come to LAN/Ethernet page ")
        driver.find_element_by_css_selector("#SM1_LAN_EthernetM1 > a > span").click()
        time.sleep(2)  

    def lan_usb_page(self, driver):
        ''' ACEmanager comes to LAN/USB web page
        
        Args:
            driver: FF web driver 
        
        '''
        basic_airlink.slog("step: from ACEmanager come to LAN/USB page ")
        driver.find_element_by_css_selector("#SM1_LAN_USBM1 > a > span").click()
        time.sleep(2) 

    def lan_host_port_routing_page(self, driver):
        ''' ACEmanager comes to LAN/Host Port Routing web page
        
        Args:
            driver: FF web driver 
        
        '''
        basic_airlink.slog("step: from ACEmanager come to LAN/Host Port Routing page ")
        driver.find_element_by_xpath("//li[@id='SM1_LAN_Host Port RoutingM1']/a/span").click()
        time.sleep(2) 
 
    def lan_global_dns_page(self, driver):
        ''' ACEmanager comes to LAN/Global DNS web page
        
        Args:
            driver: FF web driver 
        
        '''
        basic_airlink.slog("step: from ACEmanager come to LAN/Global DNS page ")        
        driver.find_element_by_xpath("//li[@id='SM1_LAN_Global DNSM1']/a/span").click()
        
        time.sleep(2)

    def lan_pppoe_page(self, driver):
        ''' ACEmanager comes to LAN/PPPoE web page
        
        Args:
            driver: FF web driver 
        
        '''
        basic_airlink.slog("step: from ACEmanager come to LAN/PPPoE page ")
        driver.find_element_by_css_selector("#SM1_LAN_PPPoEM1 > a > span").click()
        time.sleep(2)
        
    def lan_vlan_page(self, driver):
        ''' ACEmanager comes to LAN/VLAN web page
        
        Args:
            driver: FF web driver 
        
        '''
        basic_airlink.slog("step: from ACEmanager come to LAN/VLAN page ")
        driver.find_element_by_css_selector("#SM1_LAN_VLANM1 > a > span").click()
        time.sleep(2)

    def lan_vrrp_page(self, driver):
        ''' ACEmanager comes to LAN/VRRP web page
        
        Args:
            driver: FF web driver 
        
        '''
        basic_airlink.slog("step: from ACEmanager come to LAN/VRRP page ")
        driver.find_element_by_css_selector("#SM1_LAN_VRRPM1 > a > span").click()
        time.sleep(2)
        
    def lan_host_interface_watchdog_page(self, driver):
        ''' ACEmanager comes to LAN/Host interface watchdog web page
        
        Args:
            driver: FF web driver 
        
        '''
        basic_airlink.slog("step: from ACEmanager come to LAN/Host inrerface watchdog page ")
        driver.find_element_by_xpath("//li[@id='SM1_LAN_Host Interface WatchdogM1']/a/span").click()
        time.sleep(2)
 
    def set_ethernet_port(self, driver, ethernet_port_val):
        ''' Enable/Disable Ethernet port from ACEmanager LAN/Ethernet page
        
        Args:
            driver: FF web driver 
            
        
        '''
        basic_airlink.slog("step: Enable/Disable Ethernet port from ACEmanager LAN/Ethernet page ")
        if ethernet_port_val in ["Disable","Enable"]:
            Select(driver.find_element_by_name("10066")).select_by_visible_text(ethernet_port_val)   
        else:
            basic_airlink.slog("Wrong parameter")
              
        time.sleep(2)

 
    def set_ethernet_device_ip(self, driver, device_ip):
        ''' Set device IP from ACEmanager LAN/Ethernet page
        
        Args:
            driver: FF web driver 
        
        '''
        basic_airlink.slog("step: set device IP from ACEmanager LAN/Ethernet page ")
        driver.find_element_by_name("1084").clear()
        driver.find_element_by_name("1084").send_keys(device_ip)   
              
        time.sleep(2)
                                                     
    def set_ethernet_starting_ip(self, driver, staring_ip):
        ''' Set starting IP from ACEmanager LAN/Ethernet page
        
        Args:
            driver: FF web driver 
        
        '''
        basic_airlink.slog("step: set starting IP from ACEmanager LAN/Ethernet page ")  
        driver.find_element_by_name("1137").clear()
        driver.find_element_by_name("1137").send_keys(staring_ip)
                  
        time.sleep(2)


    def set_ethernet_ending_ip(self, driver, ending_ip):
        ''' Set ending IP from ACEmanager LAN/Ethernet page
        
        Args:
            driver: FF web driver 
        
        '''
        basic_airlink.slog("step: set ending IP from ACEmanager LAN/Ethernet page ")  
        
        driver.find_element_by_name("1138").clear()
        driver.find_element_by_name("1138").send_keys(ending_ip)
        time.sleep(2)


    def set_ethernet_dhcp_network_mask(self, driver, dhcp_network_mask):
        ''' Set DHCP network mask from ACEmanager LAN/Ethernet page
        
        Args:
            driver: FF web driver 
        
        '''
        basic_airlink.slog("step: set DHCP network mask from ACEmanager LAN/Ethernet page ")  
        
        driver.find_element_by_name("1135").clear()
        driver.find_element_by_name("1135").send_keys(dhcp_network_mask)
        time.sleep(2)


    def set_ethernet_dhcp_server_mode(self, driver, dhcp_server_mode):
        ''' Set DHCP server mode from ACEmanager LAN/Ethernet page
        
        Args:
            driver: FF web driver 
        
        '''
        basic_airlink.slog("step: set DHCP server mode from ACEmanager LAN/Ethernet page ")  
        
        if dhcp_server_mode in ["Disable","Enable"]:
            Select(driver.find_element_by_name("2722")).select_by_visible_text(dhcp_server_mode)
        else:
            basic_airlink.slog("Wrong parameter")
        time.sleep(2)
  
  
    def set_ethernet_link_radio_coverage_to_interface(self, driver, link_radio_coverage_to_interface):
        ''' Set DHCP server mode from ACEmanager LAN/Ethernet page
        
        Args:
            driver: FF web driver 
        
        '''
        basic_airlink.slog("step: set DHCP server mode from ACEmanager LAN/Ethernet page ")  
        
        if link_radio_coverage_to_interface in ["Disable","Ethernet", "USB"]:
            Select(driver.find_element_by_name("2723")).select_by_visible_text(link_radio_coverage_to_interface)
        else:
            basic_airlink.slog("Wrong parameter")
        time.sleep(2)


    def set_ethernet_radio_link_relay(self, driver, radio_link_relay):
        ''' Set radio link_relay from ACEmanager LAN/Ethernet page
        
        Args:
            driver: FF web driver 
            radio link_relay: Radio LInk Delay (unit: sec)
        
        '''
        basic_airlink.slog("step: set radio link_relay from ACEmanager LAN/Ethernet page ")  
        
        driver.find_element_by_name("2724").clear()
        driver.find_element_by_name("2724").send_keys(radio_link_relay)
        time.sleep(2)
 
 
    def set_ethernet_interface_disabled_duration(self, driver, interface_disabled_duration):
        ''' Set interface disabled duration from ACEmanager LAN/Ethernet page
        
        Args:
            driver: FF web driver 
            interface_disabled_duration: interface disabled duration
                0 - "Interface Disabled when Radio is disconnected"
                1 -"5 sec"
                2 -"10 sec"
                3 -"15sec"
                4 -"20 sec"
                5 -"25 sec"
                6 -"30 sec"      
        '''
        basic_airlink.slog("step: set interface disabled duration from ACEmanager LAN/Ethernet page ")  
        if interface_disabled_duration == 0:
            Select(driver.find_element_by_name("2763")).select_by_visible_text("Interface Disabled when Radio is disconnected")
        elif interface_disabled_duration == 1:
            Select(driver.find_element_by_name("2763")).select_by_visible_text("5 sec")
        elif interface_disabled_duration == 2:
            Select(driver.find_element_by_name("2763")).select_by_visible_text("10 sec")
        elif interface_disabled_duration == 3:
            Select(driver.find_element_by_name("2763")).select_by_visible_text("15 sec")
        elif interface_disabled_duration == 4:
            Select(driver.find_element_by_name("2763")).select_by_visible_text("20 sec")
        elif interface_disabled_duration == 5:
            Select(driver.find_element_by_name("2763")).select_by_visible_text("25 sec")
        elif interface_disabled_duration == 6:
            Select(driver.find_element_by_name("2763")).select_by_visible_text("30 sec")
        else:
            basic_airlink.slog("Wrong parameter")         
              
        time.sleep(2)


    def set_ethernet_turn_off_nat(self, driver, turn_off_nat):
        ''' Set turn_off_nat from ACEmanager LAN/Ethernet page
        
        Args:
            driver: FF web driver 
            turn_off_nat: Disabled/Enabled
        
        '''
        basic_airlink.slog("step: set turn_off_nat from ACEmanager LAN/Ethernet page ")  
        if turn_off_nat in ["Disabled","Enabled"]:
            Select(driver.find_element_by_name("1179")).select_by_visible_text(turn_off_nat)
        else:
            basic_airlink.slog("Wrong parameter")       

        time.sleep(2)
        
 
    def set_ethernet_1_link(self, driver, link_setting):
        ''' Ethernet 1 link setting from ACEmanager LAN/Ethernet page
        
        Args:
            driver      : FF web driver 
            link_setting: 
        
        '''
        basic_airlink.slog("step: Ethernet 1 link setting from ACEmanager LAN/Ethernet page ")  
        if   link_setting == 0:
            Select(driver.find_element_by_name("2760")).select_by_visible_text("Auto 10Mb only")
        elif link_setting == 1:
            Select(driver.find_element_by_name("2760")).select_by_visible_text("Auto 100/10")
        elif link_setting == 2:
            Select(driver.find_element_by_name("2760")).select_by_visible_text("100 Mb Full Duplex")
        elif link_setting == 3:
            Select(driver.find_element_by_name("2760")).select_by_visible_text("100 Mb Half Duplex")
        elif link_setting == 4:
            Select(driver.find_element_by_name("2760")).select_by_visible_text("10 Mb Full Duplex")
        elif link_setting == 5:
            Select(driver.find_element_by_name("2760")).select_by_visible_text("10 Mb Half Duplex")
        else:
            basic_airlink.slog("Wrong parameter")       

        time.sleep(2)
 
    def vpn_page(self, driver):
        ''' ACEmanager comes to VPN tab
        
        '''
        basic_airlink.slog("step: from Ace Manager come to VPN tab ")
        #driver.find_element_by_id("SM1_VPN").click()   #FF local nok 
        driver.find_element_by_css_selector("#VPNM1 > a > span").click() #FF  ok, IE nok
        time.sleep(2)  
                                                                          
    def vpn_sub_page(self, driver, vpn_no):
        ''' ACEmanager comes to VPN# sub tab page
        
        '''
        basic_airlink.slog("step: from Ace Manager come to VPN: " + str(vpn_no))

        if   vpn_no == 1: 
            driver.find_element_by_id("SM1_VPN_VPN 1M1").click()
        elif vpn_no == 2: 
            driver.find_element_by_id("SM1_VPN_VPN 1M2").click()
        elif vpn_no == 3: 
            driver.find_element_by_id("SM1_VPN_VPN 1M3").click()
        elif vpn_no == 4: 
            driver.find_element_by_id("SM1_VPN_VPN 1M4").click()
        elif vpn_no == 5: 
            driver.find_element_by_id("SM1_VPN_VPN 1M5").click()
            
        time.sleep(1)     
            
    def security_page(self, driver):
        ''' ACEmanager comes to Security page
        
        '''
        basic_airlink.slog("step: from Ace Manager come to Security page: ")
        #driver.find_element_by_css_selector("#SecurityM1 > a > span").click()
        driver.find_element_by_id("SecurityM1").click()
        time.sleep(1)     

        
    def services_page(self, driver):
        ''' ACEmanager comes to Services page
        
        '''
        basic_airlink.slog("step: from Ace Manager come to Services page: ")
        driver.find_element_by_css_selector("#ServicesM1 > a > span").click()

        #driver.find_element_by_id("ServicesM1").click()
        time.sleep(1)     
       

    def gps_page(self, driver):
        ''' ACEmanager comes to Gps page
        
        '''
        basic_airlink.slog("step: from Ace Manager come to GPS page: ")
        driver.find_element_by_id("S_GPSM1").click()
        time.sleep(1)     


    def er_page(self, driver):
        ''' ACEmanager comes to Events Reporting page
        
        '''
        basic_airlink.slog("step: Ace Manager comes to Events Reporting page: ")
        #driver.find_element_by_id("Events ReportingM1").click()     #FF ok , IE nok
        driver.find_element_by_xpath("//li[@id='Events ReportingM1']/a/span").click() #FF ok, IE nok
        time.sleep(1)     

    def serial_page(self, driver):
        ''' ACEmanager comes to Serial page
        
        '''
        basic_airlink.slog("step: from Ace Manager come to Serial page: ")
        driver.find_element_by_id("SerialM1").click()
        time.sleep(1)     

        
    def applications_page(self, driver):
        ''' ACEmanager comes to Applications page
        
        '''
        basic_airlink.slog("step: from Ace Manager come to Application page: ")
        driver.find_element_by_id("ApplicationsM1").click()
        time.sleep(1)     

        
    def io_page(self, driver):
        ''' ACEmanager comes to I/O page
        
        '''
        basic_airlink.slog("step: from Ace Manager come to I/O page: ")
        driver.find_element_by_id("I/OM1").click()
        time.sleep(1)     
 
            
    def admin_page(self, driver):
        ''' ACEmanager comes to Admin page  
        args:
        driver  - Firefox/IE web driver 
        
        returns:
            none
            
        ''' 
                     
        basic_airlink.slog("step: come from ACEmanager to Admin page: ")
        #driver.find_element_by_id("AdminM1").click()
        driver.find_element_by_css_selector("#AdminM1 > a > span").click()
        time.sleep(1)  
           

    def create_action(self, driver, elem_id, item_id, action_name, action_type):
        '''
        To create a new action by ACEmanager UI
        Args: 
            action_name string specify the action name 
            action_type string one of action types "Email", "SMS","Relay Link","SNMP Trap", etc
        
        '''
                       
        
        driver.find_element_by_xpath("//li[@id='SM1_Events Reporting_Actions_Add NewM1']/a/span").click()
        self.set_element_by_name(driver, elem_id, action_name)
        self.select_item_by_visible_text(driver, item_id, action_type)
        
        self.apply_reboot(driver)

    def create_event(self, driver):
        '''
        TODO
        '''
        
        pass
    

    def set_apn(self, driver): 
        ''' user enter the APN by ACEmanager WAN/Celluar web page.
        Args: 
            diver : FF web driver
            tbd_config_map: testbed configuration data 
        Returns: 
            True/False 
        '''

        basic_airlink.slog("Step: User entered APN")  
 
        device_name = tbd_config_map["DUTS"][0]
        apn = tbd_config_map[device_name]["APN"]
        ret = self.get_element_by_name(driver,"2151") 
        
        if (ret != apn):
            
            basic_airlink.slog("Need change APN " + ret + "to " + apn)  
            return self.set_element_by_name(driver, "2151", apn)
        
        else:
            
            basic_airlink.slog("No need change APN " + ret)  
            return True
                  

    def set_host_connection_mode(self, driver, host_connection_mode): 
        ''' set host connection mode by ACEmanager LAN/DHCP page
        Args: 
        
            diver : FF web driver
            host_connection_mode:   string  "0" - "Ethernet Uses Public IP"
                                    string  "1" - "All Hosts Use Private IPs"
                                    string  "2" - "USB Uses Public IP"
                                    string  "3" - "RS232 Uses Public IP"
                                    string  "4" - "First Host gets Public IP"
        Returns: 0 - successful, -1 - failed 
        '''
 
        basic_airlink.slog("driver=" + str(driver))  
        basic_airlink.slog("host connection mode=" + host_connection_mode)  
        
        if   (host_connection_mode == "0"):       
            ret = self.select_item_by_visible_text(driver, "1139", "Ethernet Uses Public IP")        
        elif (host_connection_mode == "1"):       
            ret = self.select_item_by_visible_text(driver, "1139", "All Hosts Use Private IPs") 
        elif (host_connection_mode == "2"):       
            ret = self.select_item_by_visible_text(driver, "1139", "USB Uses Public IP") 
        elif (host_connection_mode == "3"):       
            ret = self.select_item_by_visible_text(driver, "1139", "RS232 Uses Public IP") 
        elif (host_connection_mode == "4"):       
            ret = self.select_item_by_visible_text(driver, "1139", "First Host gets Public IP")            

        basic_airlink.slog("ret= " + str(ret))  
            
        return ret
    
        
    def get_host_connection_mode(self, driver): 
        ''' get host connection mode
        Args: 
            diver : FF web driver
        Returns: 
            Host conenction mode 
        '''

        msciid_str = str(msciids.MSCIID_CFG_CMN_HOST_IP_MODE)
        ret = self.get_element_by_name(driver,msciid_str)     
        return ret     
    

    def get_dhcp_lease_timer(self, driver): 
        ''' get DHCP lease timer
        Args: 
            diver : FF web driver
        Returns: 
             DHCP lease timer 
        '''

        msciid_str = str(msciids.DHCP_LEASE_TIME)
        ret = self.get_element_by_name(driver,msciid_str)     
        return ret  


    def get_dhcp_domain(self, driver): 
        ''' get DHCP domain
        Args: 
            diver : FF web driver
        Returns: 
             DHCP domain
        '''

        msciid_str = str(msciids.MSCIID_CFG_DHCP_DOMAIN)
        ret = self.get_element_by_name(driver,msciid_str)     
        return ret 


    def get_dhcp_mtu_size(self, driver): 
        ''' get DHCP MTU size
        Args: 
            diver : FF web driver
        Returns: 
             DHCP MTU size
        '''

        msciid_str = str(msciids.MSCIID_CFG_DHCP_MTU_SIZE)
        ret = self.get_element_by_name(driver,msciid_str)     
        return ret 
            
    def get_bridge_wifi_to_ethernet_d2(self, driver): 
        ''' get Bridge Wifi to Ethernet in LAN/DHCP_ADDRESSING page
        Args: 
            diver : FF web driver
        Returns: 
             Enable/Disable
        '''

        msciid_str = str(msciids.MSCIID_CFG_WIFI_BRIDGE_EN)
        ret = self.get_element_by_name(driver,msciid_str+"-d2")     
        return ret
 
    def get_wifi_mode_d1(self, driver): 
        ''' get wifi mode in LAN/DHCP_ADDRESSING page
        Args: 
            diver : FF web driver
        Returns: 
             Enable/Disable
        '''

        msciid_str = str(msciids.MSCIID_WIFI_MODE)
        ret = self.get_element_by_name(driver,msciid_str+"-d1")     
        return ret     

    def get_wifi_mode(self, driver): 
        ''' get wifi mode in LAN/WIFI page
        Args: 
            diver : FF web driver
        Returns: 
             Enable/Disable
        '''

        msciid_str = str(msciids.MSCIID_WIFI_MODE)
        ret = self.get_element_by_name(driver,msciid_str)     
        return ret  

    def get_usb_device_mode(self, driver): 
        ''' get USB device mode in LAN/USB page
        Args: 
            diver : FF web driver
        Returns: 
             0/1/2 (USB serial/USBNET/Disabled)
        '''

        msciid_str = str(msciids.MSCIID_CFG_CMN_USB_DEVICE)
        ret = self.get_element_by_name(driver,msciid_str)     
        return ret                        

    def set_usb_device_mode(self, driver, mode): 
        ''' get USB device mode in LAN/USB page
        Args: 
            diver : FF web driver
            mode: 
             USB serial/USBNET/Disabled
        '''

        msciid_str = str(msciids.MSCIID_CFG_CMN_USB_DEVICE)
        basic_airlink.slog("step: set USB device mode from ACEmanager LAN/USB page ")  
        if mode in ["Disabled","USBNet","USB Serial"]:
            Select(driver.find_element_by_name("1130")).select_by_visible_text("Disabled")
        else:
            basic_airlink.slog("Wrong parameter")  
            return False     

        time.sleep(2)
        return True
    
    def get_apn_in_use(self, driver):
        ''' get APN in use in WAN/Celluar page
        Args: 
            diver : FF web driver
        Returns: 
             APN in use
        '''

        msciid_str = str(msciids.MSCIID_STS_CMN_APN_CURRENT)+"-d1"
        ret = self.get_element_by_id(driver,msciid_str)     
        return ret 

    def get_apn_type(self, driver):
        ''' get APN type in WAN/Celluar page, Apply for GX400 ROW
        Args: 
            diver : FF web driver
        Returns: 
             APN type
        '''

        msciid_str = str(msciids.MSCIID_CFG_CMN_APN_TYPE)
        ret = self.get_element_by_id(driver,msciid_str)     
        return ret     

    def get_gprs_diversity(self, driver):
        ''' get RX diversity in WAN/Celluar page
        Args: 
            diver : FF web driver
        Returns: 
             RX diversity
        '''

        msciid_str = str(msciids.MSCIID_CFG_GPRS_DIVERSITY)
        ret = self.get_element_by_id(driver,msciid_str)     
        return ret 
    
    def get_evdo_diversity(self, driver):
        ''' get EVDO diversity in WAN/Celluar page
        Args: 
            diver : FF web driver
        Returns: 
             EVDO diversity
        '''

        msciid_str = str(msciids.MSCIID_CFG_EVDO_DIVERSITY)
        ret = self.get_element_by_id(driver,msciid_str)     

        return ret
	
    def retry_match_state(self, driver, state, fail_refresh_count, restart_count, refresh_delta_time, url, username, password):
        ''' retry to get the correct state in UI, refresh the page if the state is not match, 
            restart the browser after refreshing does not work 
        Args: 
            diver : FF web driver
            state: The state needed match
            fail_refresh_count: refresh count
            restart_count: restart the browser count
            refresh_delta_time: Time interval of refresh
            url: device AceManager url
            username: AceManager username
            password: AceManager password
        Returns: 
             True: match the state sucessfully
             FalseL: fail to match state
        '''              
        ret = True
        flag = 0
        var = ""
        func_lst = []
        
        #If the network state is not Network Ready, keep refreshing until times up, then restart the Firefox
        if state == "Network Ready":
            time.sleep(2)        
            var = self.get_network_state(driver)
            func_lst = [self.get_network_state(driver)]
        elif state == "4.3.4":
            time.sleep(2)
            var = self.get_aleos_sw_ver(driver)
            func_lst = [self.get_aleos_sw_ver(driver)]
#        Add the states need to be checked
#        elif state == 
        
        else:
            flag = 1
            ret = False
                
        try_restart_count = 0
        while try_restart_count != restart_count and var != state and flag == 0:
            if try_restart_count > 0:
                driver = self.login(url, username, password)                      
            fail_get_state_count = 0
            while var != state and fail_get_state_count != fail_refresh_count:
                logging.info("Logging:state: "+ var)
                basic_airlink.slog("Logging:state: "+ var)
                time.sleep(refresh_delta_time)
                fail_get_state_count+=1
                basic_airlink.slog("Get try refresh count: "+ str(fail_get_state_count))
                self.refresh(driver)
                var = func_lst[0]           
                        
            if fail_get_state_count == fail_refresh_count and var != state:               
                try_restart_count+=1
                basic_airlink.slog("Get try restart count: "+ str(try_restart_count))
                driver.close()
                
                basic_airlink.slog("can not get right state, restart...")
            
        if try_restart_count == restart_count and restart_count != 0:
            ret = False
        return ret
    
    def verify_ap_connection(self, driver, config_ap):
        '''  verify remote AP connection 
        assumes at LAN/WiFi page
         args: 
             driver        - web driver
             config_ap     - the configured AP's name
         
         returns: 
              True - able to connect
              False - unable to connect
         '''  
        try: 
            # Connect button
            driver.find_element_by_id("b"+str(msciids.MSCIID_WIFI_AVAILABLE_AP_CONNECT)).click()
            time.sleep(1)
            driver.switch_to_alert().accept()
            basic_airlink.cslog("-- Connecting to remote AP...")
            time.sleep(10)   
            
            self.refresh(driver)
            
            available_ap = self.get_element_by_id(driver, str(msciids.MSCIID_WIFI_AVAILABLE_AP))
            connect_status = self.get_element_by_id(driver, str(msciids.MSCIID_WIFI_REMOTE_AP_CONNECT_STATE))
            
            basic_airlink.cslog("-- Checking Available AP and Connect Status")
                    
            wait = 5
            # 5 waits for AP to get connected
            while connect_status == "Connecting..." or connect_status == "Not connected" or available_ap != config_ap:
                if wait > 0:
                    self.refresh(driver)
                    time.sleep(10) 
                    available_AP = self.get_element_by_id(driver, str(msciids.MSCIID_WIFI_AVAILABLE_AP))
                    connect_status = self.get_element_by_id(driver, str(msciids.MSCIID_WIFI_REMOTE_AP_CONNECT_STATE))
                    logging.debug(available_AP + " ... " + connect_status)
                    wait -= 1
                else: return False
                
            basic_airlink.cslog("-- Successfully " + connect_status + " to remote AP: " + available_AP + " using WiFi")   
            return True
        
        except WebDriverException:
            logging.debug("Unable to establish the Connection")  
            return False
        
    def get_current_page(self, driver):
        
        return driver.find_element_by_class_name("current").text

