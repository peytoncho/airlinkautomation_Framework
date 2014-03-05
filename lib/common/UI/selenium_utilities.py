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
import SendKeys
import time
import sys
import unittest
import logging
import basic_airlink
#from msciids import *
import msciids

sys.path.append(basic_airlink.airlinkautomation_home_dirname+basic_airlink.lib_common_path)

basic_airlink.append_sys_path()

tbd_config_map = basic_airlink.get_tbd_config_data()
ace_config_map = basic_airlink.get_ace_config_data()

# This is basic data structure of one parameter/element in ACEmanager UI
ACEelement={
         'tab'   :'Status',  ## refer to tab list in acemanage_pages.yml
         'subtab':'Home',    ## refer to subtab list in acemanage_pages.yml
         'byhow' :'BY_ID',   #BY_ID/BY_NAME/BY_XPATH/BY_CSS_SELECTOR/BY_CLASS_NAME/BY_LINK_TEXT
         'field' :'',        #masciid/name/xpath/css_selector
         'flag'  :1,         #possible post action (e.g. get text, click, get attribute) after find element byhow
         'value' :''         
         }

class SeleniumAcemanager(unittest.TestCase):
    ''' This class implements Selenium UI operation methods by ACEmanager Web, 
    e.g. navigate pages, get/set Web elements. 
    if methods don't include tab/subtab parameters, that needs to 
    call navigate_subtab() first to navigate the specified page.
    User shall manually choose DUT, and set the FW version in 
    common_testbed_conf.yml.
    ''' 
    
    def __init__(self, device_name=tbd_config_map["DUTS"][0]):
        ''' TODO: to think to read these initials from DUT dynamically.
        to think if we really need error_flag variable.
        to think multiple DUTs
        '''
        self.error_flag = 0
        
        self.device_name  = device_name
        self.device_model = tbd_config_map[self.device_name]["MODEL"]
        self.aleos_sw_ver = tbd_config_map[self.device_name]["ALEOS_FW_VER"][:-4]  #long -> short
        self.aleos_sw_ver_format = self.aleos_sw_ver.replace('.','_')
        
        self.ele_config_map = basic_airlink.get_ele_config_data(self.aleos_sw_ver)
        self.short_time = 3
        
    def get_element_by_id(self, driver, msciid, flag=1):
        '''
        find item by id and get its text 
        Args:        
            driver - Firefox/IE web driver
            msciid - id string 
            flag -  1(get text), 2(get title), 0(get element only) 
        returns: 
            the text that read from web
            
        '''
        txt = ""
        tab,subtab = self.get_parents(msciid)
        ret = self.navigate_subtab(driver, tab, subtab)
        
        if not ret:
            txt = ""
        
        try:
            if flag == 1:
                txt= driver.find_element_by_id(msciid).text
                basic_airlink.slog("MSCIID_"+msciid+ " : "+ txt)
            elif flag == 2:
                txt= driver.find_element_by_id(msciid).get_attribute("title")
                basic_airlink.slog("MSCIID_"+msciid+ " : "+ txt)
            else:
                txt= driver.find_element_by_id(msciid)
        
        except NoSuchElementException:
            
            basic_airlink.slog("get_element_by_id: cannot find " +msciid)
            self.error_flag+=1
        
        finally: 
            return txt   
  
    def get_element_by_name(self, driver, name, flag=1):
        '''
        find item by name and get its value
        Args:        
            driver - Firefox/IE web driver
            name -  string element name
            flag -  get value(1) or get title(2) or get element only(0)
        returns: 
            the value that read from web
            
        '''

        tab,subtab = self.get_parents(name)
        self.navigate_subtab(driver, tab, subtab)
                
        val = ""
        try:
            if flag == 1:
                val= driver.find_element_by_name(name).get_attribute("value")
                basic_airlink.slog(name+"="+val)
            elif flag == 2:
                val= driver.find_element_by_name(name).get_attribute("title")
                basic_airlink.slog(name+"="+val)
            else:
                val= driver.find_element_by_name(name)
            
        except NoSuchElementException:
            
            basic_airlink.slog("get_element_by_name: cannot find " + name)
            self.error_flag+=1
        
        finally: 
            return val
                 
    def get_element_by_xpath(self, driver, x_path, flag=1):
        '''
        find item by xpath, and/or get text
        Args:        
            driver - Firefox/IE web driver
            x_path -  string, xpath of the item
            flag  0  find element by xpath 
                  1  find element by xpath and get text
        returns: 
            the value that read from web page
            
        '''
        
        val = ""
        try:
            if flag == 1: 
                val= driver.find_element_by_xpath(x_path).text
            else: 
                val= driver.find_element_by_xpath(x_path)
            
        except NoSuchElementException:
            
            basic_airlink.slog("get_element_by_xpath: cannot find " + x_path)
            self.error_flag+=1
        
        finally: 
            basic_airlink.slog(x_path)          
            return val
 
    def get_element_by_css_selector(self, driver, css_selector_str, flag=1):
        '''
        find item by css selector and/or get its text 
        Args:        
            driver - Firefox/IE web driver
            css_selector_str - string  CSS selector
            flag - 0 (get the element obejct) or 1 (get the text)
        returns: 
            the text that read from web
            
        '''
        
        txt = ""
        try:
            if flag == 1:
                txt= driver.find_element_by_css_selector(css_selector_str).text
                basic_airlink.slog("CSS selector"+css_selector_str+ " : "+ txt)
            else:
                txt = driver.find_element_by_css_selector(css_selector_str)
        
        except NoSuchElementException:
            
            basic_airlink.slog("cannot find " +css_selector_str)
            self.error_flag+=1
        
        finally: 
            return txt              
        
    def get_element_by_class_name(self, driver, name, flag=1):
        ''' TODO
        '''
        ret = driver.find_element_by_class_name(name)
        return ret

    def get_element_by_tag_name(self, driver, name, flag=1):
        ''' TODO
        '''
        ret = driver.find_element_by_tag_name(name)
        return ret
        
    def get_element_by_link_text(self, driver, link_text, flag=1):
        ''' TODO
        find item by link text, and/or get text
        Args:        
            driver - Firefox/IE web driver
            link_text - the text of the element to be found
        
        returns: 
            the text that read from web
            
        '''
        
        txt = ""
        try:
            if flag == 1:
                txt= driver.find_element_by_link_text(link_text).text
                basic_airlink.slog("Link Text"+link_text+ " : "+ txt)
            else:
                txt= driver.find_element_by_link_text(link_text)
                basic_airlink.slog("Link Text "+link_text+ " : "+ txt)
        
        except NoSuchElementException:
            
            basic_airlink.slog("cannot find " +link_text)
            self.error_flag+=1
        
        finally: 
            return txt          

        
    def get_element(self, driver, element):
        ''' generally read one parameter from ACEmanager UI based on the element
         5 parameters 
        
        Args: 
             element: dictionary, including 6 items.
             element["tab"]:  tab name on top of ACEmanager UI 
             element["subtab"]: subtab name under each tab in ACEmanager UI 
             element["byhow"]: BY_ID/BY_NAME/BY_XPATH/BY_CSS_SELECTOR
             element["field"]: id,name, xpath, css_selector, class_name
             element["flag"]:  
             element["value"]: fill this 
             
        Global: 
            self.error_flag +1 if error exists
            
        Returns: 
            element.
            the specified element value if successful, otherwise empty string
            element["value"]
            
        '''

        self.navigate_subtab(driver, element["tab"], element["subtab"])    
         
        if element['byhow'] == 'BY_ID': 
            element['value'] = self.get_element_by_id(driver,element['field'])
            
        elif element['byhow'] =='BY_NAME':
            element['value'] = self.get_element_by_name(driver, element['field'], element['flag'])
        
        elif element['byhow'] =='BY_XPATH':
            element['value'] = self.get_element_by_xpath(driver, element['field'])

        elif element['byhow'] =='BY_CSS_SELECTOR':
            element['value'] = self.get_element_by_css_selector(driver, element['field'])    
        
        else:
            basic_airlink.cslog("wrong by_type parameter")
            self.error_flag+=1
            element['value'] = ""
            
        return element

    def set_element(self, driver, element):
        '''
         generally set one parameter by name by Selenium/ACEmanager UI. 
         Args: 
             driver: FF/IE web driver 
             element: dictionary, including 6 items.
             element["tab"]:  tab name on top of ACEmanager UI 
             element["subtab"]: subtab name under each tab in ACEmanager UI 
             element["byhow"]: BY_ID/BY_NAME/BY_XPATH/BY_CSS_SELECTOR
             element["field"]: id,name, xpath, css_selector, class_name
             element["flag"]:  
             element["value"]:  string, value to set 

         Returns: 
             True/False
             
        '''        

        self.navigate_subtab(driver, element["tab"], element["subtab"])     
           
        if element['byhow'] == 'BY_ID': 
            return self.set_element_by_id(driver, element['field'], element['value'])
            
        elif element['byhow'] =='BY_NAME':
            return self.set_element_by_name(driver, element['field'], element['value'])
        
        elif element['byhow'] =='BY_XPATH':
            return self.set_element_by_xpath(driver, element['field'], element['value'])

        elif element['byhow'] =='BY_CSS_SELECTOR':
            return self.set_element_by_css_selector(driver, element['field'], element['value'])
                
        else:
            basic_airlink.cslog("wrong by_type paramter")
            return False
        
#    def get_subtab_elements(self, driver, tab, subtab):  
#        elems= ""
#                                         
#        try:
#            
#            if ace_config_map[self.aleos_sw_ver][self.device_name][tab][subtab][0] == "BY_CSS_SELECTOR":
#                elems=driver.find_elements_by_css_selector(ace_config_map[self.aleos_sw_ver][self.device_name][tab][subtab][1])
#                
#            elif ace_config_map[self.aleos_sw_ver][self.device_name][tab][subtab][0] == "BY_ID":
#                elems=driver.find_elements_by_id(ace_config_map[self.aleos_sw_ver][self.device_name][tab][subtab][1])
#    
#            elif ace_config_map[self.aleos_sw_ver][self.device_name][tab][subtab][0] == "BY_XPATH":
#                elems=driver.find_elements_by_xpath(ace_config_map[self.aleos_sw_ver][self.device_name][tab][subtab][1])
#            else:
#                basic_airlink.cslog( "Incorrect byhow parameter or NA subtab")
#                        
#            time.sleep(10)               
#            
#        except: 
#            self.error_flag +=1
#            basic_airlink.cslog(" Exception occurred", "RED", "WHITE")
#            
#            ret = ""
#            
#        finally:
#            return elems
#        
#    def get_config(self, driver, tab, subtab):
#        ''' Get all parameters on the specified subtab page, and put onto 
#        config_elements stack.
#         TODO
#        '''
#        config_elements = []       
#        
#        self.navigate_subtab(driver, tab, subtab)
##        xpath = self.get_subtab_xpath(driver, tab, subtab)
##        page_elems = driver.find_elements_by_xpath(xpath)
#        page_elems = self.get_subtab_elements(driver, tab, subtab)
#        print (str(page_elems))
#        
#        for elem in page_elems:
#            id1 = str(elem.get_attribute("id"))
#            
##            byid = self.get_element_by_id(driver, id1)
##            byname = self.get_element_by_name(driver, id1)
#            bytitle = str(elem.get_attribute("title"))
#            text1 = str(elem.text)
#            #config_elements.append({'tab':tab,'subtab':subtab,'byhow':'by_id','field':field,'value':value})
#            
#            basic_airlink.cslog("id="+id1+",title="+bytitle+",text="+text1)
#            
#        return config_elements
    
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
        tab,subtab = self.get_parents(id_str)
        self.navigate_subtab(driver, tab, subtab)
        element = driver.find_element_by_id(id_str)
        val = True

        try:
            element.clear()
            element.send_keys(val_str)
        
        except NoSuchElementException:
            basic_airlink.slog("set_element_by_id: cannot find " + id_str)
            self.error_flag+=1
            val = False
            
        finally: 
            return val
         
        
    def set_element_by_name(self, driver, name_str, val_str):
        '''
        find item by name and set the value
        '''   
        tab,subtab = self.get_parents(name_str)
        val = self.navigate_subtab(driver, tab, subtab)
        
     
        try:
            driver.find_element_by_name(name_str).clear()
            driver.find_element_by_name(name_str).send_keys(val_str)
        
        except:
            basic_airlink.slog("set_element_by_name: cannot find " + name_str)
            self.error_flag+=1
            val = False
                
        finally: 
            return val
                
    def select_item_by_visible_text(self, driver, id_str, option_visible_text):
        '''
        select item by visible text
        
        '''   
        tab,subtab = self.get_parents(id_str)
        self.navigate_subtab(driver, tab,subtab)
        
        val = True
     
        basic_airlink.cslog("select_item_by_visible_text: msciid="+id_str+",option="+option_visible_text+"\n")
        try: 
            Select(driver.find_element_by_name(id_str)).select_by_visible_text(option_visible_text)
            time.sleep(self.short_time)
        except Exception as inst:
            basic_airlink.cslog("select_item_by_visible_text exception: "+str(inst))
            self.error_flag+=1
            val = False
                
        finally: 
            return val

    def select_item_by_value(self, driver, id_str, option_str):
        '''
        select item by value
        
        '''   
        tab,subtab = self.get_parents(id_str)
        self.navigate_subtab(driver, tab, subtab)
        
        val = True
     
        basic_airlink.cslog("select_option_by_value: msciid="+id_str+",option="+option_str+"\n")
        try: 
            Select(driver.find_element_by_name(id_str)).select_by_value(option_str)
            time.sleep(self.short_time)
        except Exception as inst:
            basic_airlink.cslog("select_option_by_value exception: "+str(inst))
            self.error_flag+=1
            val = False
                
        finally: 
            return val
                
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
        ''' ACEmanager UI: apply and reboot DUT whether change parameter
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            True  - successful 
            False - exception appears
        ''' 
        self.apply(driver)
        return self.reboot(driver)
 
    def apply_refresh(self, driver):
        ''' Acemanager UI: apply and refresh DUT   
        args: 
            driver - Firefox/IE web driver
        returns: 
            True  - successful 
            False - exception appears
        ''' 
        self.apply(driver)
        return self.refresh(driver)     
       
    def apply(self, driver):
        ''' Acemanager UI: apply DUT   
        args: 
            driver - Firefox/IE web driver
        returns: 
            None
        '''
        val = True

        try: 
            driver.find_element_by_id("btn_Apply").click()
            time.sleep(2)    
            driver.switch_to_alert().accept()
            
        except WebDriverException:
            
            logging.debug(" apply: failed, and pop up exception\n")
            val = False
        
        finally: 
            return val
        
    def refresh(self, driver):
        ''' Acemanager UI: refresh   
        args: 
            driver - Firefox/IE web driver
        returns: 
            None

        '''
        val = True
        try:
            driver.find_element_by_id("btn_Refresh").click()
            time.sleep(2)
        except:
            val = False
                
        finally: 
            return val
 
    def refresh_all(self, driver):
        ''' Acemanager UI: refresh all
        args: 
            driver - Firefox/IE web driver
        returns: 
            None

        '''
        basic_airlink.cslog("refresh all")

        val = True
        try:
            driver.find_element_by_id("btn_All").click()
            time.sleep(2)           
            driver.switch_to_alert().accept()  
            time.sleep(8)    
            driver.switch_to_alert().accept()  
  
        except:
            val = False
                
        finally: 
            return val       
        
    def reboot(self, driver):
        ''' Acemanager UI: reboot   
        args: 
            driver - Firefox/IE web driver
        returns: 
            None

        ''' 
        basic_airlink.cslog("reboot")
        val = True
        try: 
            
            driver.find_element_by_id("btn_Reset").click()
            driver.switch_to_alert().accept()
            
        except WebDriverException:
            
            logging.debug(" reboot: failed, and pop up exception\n")
            val =  False
        
        finally: 
            return val        

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
        basic_airlink.cslog("login to "+url+" "+username+" "+password)

        try: 
            if tbd_config_map["BROWSER"] == "FF":
                driver = webdriver.Firefox()                # Get local session of firefox
                #driver.set_window_position(200, 200)
                #driver.set_window_size(800, 600)
                #driver.maximize_window()
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
        '''  reset to factory default by AceManager/Admin/Advanced
        Args:
            driver: FF/IE browser 
        Returns:
            True: successful
            False: failed 
        
        '''
        basic_airlink.slog("Web UI factory reset")
        val = True
        try: 
            
            driver.find_element_by_css_selector("#AdminM1 > a > span").click()
            
            driver.find_element_by_css_selector("#SM1_Admin_AdvancedM1 > a > span").click()
            
            driver.find_element_by_id("b5108").click()
            time.sleep(5)
            driver.switch_to_alert().accept()  
            
        except WebDriverException: 
            
            basic_airlink.slog("Pop up exception")
            val = False
        
        return val  

###############Status/Home suntab page read#####################################

    def get_phone_num(self, driver):
        ''' get phone number by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            phone number
        '''
        
        msciid_str = str(msciids.MSCIID_INF_PHONE_NUM)

        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("phone number: "+ret)   
                
        return ret
        
    def get_network_ip(self, driver):
        ''' get network IP by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            network IP
        '''

        msciid_str = str(msciids.MSCIID_STS_NETWORK_IP)

        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("network IP: "+ret)   
        
        return ret     

    def get_network_state(self, driver):
        ''' get network state by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            network state
        '''

        msciid_str = str(msciids.MSCIID_STS_NETWORK_STATE)

        ret=self.get_element_by_id(driver, msciid_str)

        basic_airlink.cslog("network state: "+ret)   
        
        return ret  
    
    def get_network_rssi(self, driver):
        ''' get network RSSI by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            network RSSI
        '''

        msciid_str = str(msciids.MSCIID_STS_NETWORK_RSSI)

        ret=self.get_element_by_id(driver, msciid_str)

        basic_airlink.cslog("network RSSI: "+ret)   
        
        return ret  
 
    def get_network_operator(self, driver):
        ''' get network operator by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            network operator
        '''

        msciid_str = str(msciids.MSCIID_STS_GPRS_OPERATOR)

        ret=self.get_element_by_id(driver, msciid_str)

        basic_airlink.cslog("network operator: "+ret)     
        
        return ret 
       
    def get_gprs_cell_info(self, driver):
        ''' get GPRS cell info by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            GPRS cell info
        '''

        msciid_str = str(msciids.MSCIID_STS_GPRS_CELL_INFO)

        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("GPRS cell info: "+ret)     
        
        return ret  
    
    def get_network_service(self, driver):
        ''' get network service by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            network service
        '''

        msciid_str = str(msciids.MSCIID_STS_NETWORK_SERVICE)

        ret=self.get_element_by_id(driver, msciid_str)

        basic_airlink.cslog("network service: "+ret)     
            
        return ret  
    
    def get_aleos_sw_ver(self, driver, flag = 1):
        ''' get ALEOS SW version by ACEmanager Web UI Status/Home or 
        Status/About page. e.g. 

        Args: 
            driver FF/IE web driver 
            tab    tab of ACEmanager UI
            subtab subtab under tab in ACEmanager
            flag   0  - ALEOS SW version long format for 4.3.4 and older , 
                   1  - ALEOS SW version short format for 4.3.5 and newer.
        Usages:
               get_aleos_sw_ver(driver)
               get_aleos_sw_ver(driver, 0)
               
        Returns: 
            ALEOS SW version -
            short format e.g. 4.3.5 for for 4.3.5 and newer
            long  format e.g. 4.3.4.009 for for 4.3.4 and older

        '''
        ret_subtab = self.get_current_subtab(driver,2)  # get subtab and convert
        
        if flag == 0: 
            if ret_subtab == 'Home':
                msciid_str = str(msciids.MSCIID_INF_ALEOS_SW_VER)
            elif ret_subtab == 'About':
                msciid_str = str(msciids.MSCIID_INF_ALEOS_SW_VER)+'-d1'
    
        elif flag == 1:
            if ret_subtab == 'Home':
                msciid_str = str(msciids.MSCIID_INF_ALEOS_SW_VER_SHORT )
            elif ret_subtab == 'About':
                msciid_str = str(msciids.MSCIID_INF_ALEOS_SW_VER_SHORT )+'-d1'
            
        ret=self.get_element_by_id(driver, msciid_str)

        basic_airlink.cslog("ALEOS SW version: "+ret) 
      
        return ret  
    
    def get_cdma_1xecio(self, driver):
        ''' get CDMA 1x ECIO by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            CDMA 1x ECIO
        '''
        
        msciid_str = str(msciids.MSCIID_STS_CDMA_1XECIO)

        ret=self.get_element_by_id(driver, msciid_str)

        basic_airlink.cslog("CDMA 1x ECIO: "+ret) 
                
        return ret  
    
    def get_gprs_ecio(self, driver):
        ''' get GPRS ECIO by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            GPRS ECIO
        '''

        msciid_str = str(msciids.MSCIID_STS_GPRS_ECIO)

        ret=self.get_element_by_id(driver, msciid_str)

        basic_airlink.cslog("GPRS ECIO: "+ret) 
                
        return ret  
    
    def get_network_channel(self, driver):
        ''' get network channel by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            network channel
        '''

        msciid_str = str(msciids.MSCIID_STS_NETWORK_CHANNEL)

        ret=self.get_element_by_id(driver, msciid_str)

        basic_airlink.cslog("network channel: "+ret) 
        
        return ret  
    
    def get_bytes_sent(self, driver):
        ''' get network IP by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            Bytes sent
        '''

        msciid_str = str(msciids.MSCIID_STS_MODEM_SENT)+'-d1'

        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("WAN Cellular Bytes sent: "+ret) 
        
        return ret  
    
    def get_bytes_received(self, driver):
        ''' get bytes received by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            bytes received
        '''

        msciid_str = str(msciids.MSCIID_STS_MODEM_RECV)+'-d1'

        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("WAN Cellular Bytes received: "+ret) 
        
        return ret     
 
    def get_modem_name(self, driver):
        ''' get modem name by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            modem name
        '''

        msciid_str = str(msciids.MSCIID_CFG_CMN_MDM_NAME)+'-d1'

        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("Modem Name: "+ret)
        
        return ret   
 
    def get_xcard_type(self, driver):
        ''' get X card type by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            X card type
        '''

        msciid_str = str(msciids.MSCIID_X_CARD_TYPE)

        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("X-Card Type : "+ret)
        
        return ret  

    def check_xcard_type(self, driver, xcard_desired=None):
        '''
        Checks X-card type against desired type
        Args: 
            driver
            xcard_desired
        Returns: 
            True/False
            xcard_read: string read from field
        '''                           
        basic_airlink.cslog("-- Checking X-card type")
        xcard_read = ""
        count = 5     
        while self.get_xcard_type(driver) == "Refresh...":
            if count > 0:
                basic_airlink.clog("...X-card information still loading....")
                count -= 1
            else:
                return False, xcard_read
            
        xcard_read = self.get_xcard_type(driver)
        
        if xcard_desired is None:
            return True, xcard_read
        else:        
            if xcard_read != xcard_desired:
                return False, xcard_read
            else: 
                return True, xcard_read
             
    def get_xcard_state(self, driver):
        ''' get X card state by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            X card state
        '''

        msciid_str = str(msciids.MSCIID_STS_X_CARD_STATE)

        ret=self.get_element_by_id(driver, msciid_str)
        basic_airlink.cslog("X-Card State: "+ret)
        
        return ret 

    def get_radio_fw_ver(self, driver):
        ''' get modem SW version by ACEmanager Web UI Status/Home page
        
        Args: 
            driver FF/IE web driver 
        Returns: 
            Radio FW version
        '''

        msciid_str = str(msciids.MSCIID_INF_MODEM_SW_VER)

        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("Radio FW Version: "+ret)
        
        return ret 

    def get_lte_rsrp(self, driver):
        ''' get LTE RSRP by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            LTE RSRP
        '''

        msciid_str = str(msciids.MSCIID_STS_LTE_RSRP)

        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("LTE RSRP: "+ret)


    def get_lte_rsrq(self, driver):
        ''' get LTE RSRQ by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            LTE RSRQ
        '''

        msciid_str = str(msciids.MSCIID_STS_LTE_RSRQ)

        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("LTE RSRQ: "+ret)
        
        return ret


    def get_modem_id(self, driver):
        ''' get modem ID by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
         Modem ID
        '''


        msciid_str = str(msciids.MSCIID_INF_MODEM_ID)

        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("Modem ID: "+ret)
        
        return ret
 
    def get_network_conn_type(self, driver):
        ''' get network connection type indicator by ACEmanager Web UI 
        Status/Home page. Indicates if current connection is IPv4 or IPv6.
        Args: 
            driver FF/IE web driver 
        Returns: 
            network IPv6 or IPv4 conenction type 
        '''

        msciid_str = str(msciids.MSCIID_STS_NETWORK_IPV6_CONN)

        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("network IPv6 or IPv4 conenction type: "+ret)
        
        return ret 
    
    def get_network_ipv6(self, driver):
        ''' get network IP v6 by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            network IPv6
        '''

        msciid_str = str(msciids.MSCIID_STS_NETWORK_IPV6)  

        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("network IPv6: "+ret)
        
        return ret    
 
    def get_network_ipv6_prefix_len(self, driver):
        ''' get network IPv6 prefix length by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            network IPv6 prefix length
        '''

        msciid_str = str(msciids.MSCIID_STS_NETWORK_IPV6PREFIXLEN)

        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("network IPv6 prefix length: "+ret)
        
        return ret 

    def get_network_ipv6_prefix(self, driver):
        ''' get network IPv6 prefix by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            network IPv6 prefix 
        '''

        msciid_str = str(msciids.MSCIID_CFG_NETWORK_IPV6_PREF)

        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("network IPv6 prefix: "+ret)
        
        return ret 
 
    def get_gprs_rscp(self, driver):
        ''' get GPRS RSCP by ACEmanager Web UI Status/Home page
        Args: 
            driver FF/IE web driver 
        Returns: 
            GPRS RSCP
        '''

        msciid_str = str(msciids.MSCIID_STS_GPRS_RSCP)

        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("GPRS RSCP: "+ret)
        
        return ret 
                 
############Status/About subtab page############################################

    def get_device_model(self, driver):
        ''' get device model by ACEmanager Web UI Status/About page
        Args: 
            driver FF/IE web driver 
        Returns: 
            device model
        '''

        msciid_str = str(msciids.MSCIID_INF_PRODUCT_STR )
            
        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("device model: "+ret)
        
        return ret 
    
    def get_radio_module_type(self, driver):
        ''' get Radio Module Type by ACEmanager Web UI Status/About page
        Args: 
            driver FF/IE web driver 
        Returns: 
            radio module type
        '''

        msciid_str = str(msciids.MSCIID_INF_MODEM_HW_VER )
            
        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("radio module type: "+ret)
        
        return ret 

    def get_cmno(self, driver):
        ''' get Certified Mobile Network Operator, e.g. "ATT01" by ACEmanager 
        Web UI Status/About page
        Args: 
            driver FF/IE web driver 
        Returns: 
            Certified Mobile Network Operator, e.g. "ATT01"
        '''

        msciid_str = str(msciids.MSCIID_STS_RMID )
            
        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("Certified Mobile Network Operator: "+ret)
        
        return ret 
    
    def get_global_id(self, driver):
        ''' get Global ID by ACEmanager Web UI Status/About page
        Args: 
            driver FF/IE web driver 
        Returns: 
            Global ID
        '''

        msciid_str = str(msciids.MSCIID_INF_DEVICE_ID )
            
        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("Global ID: "+ret)
        
        return ret 
    
    def get_pri_id(self, driver):
        ''' get PRI ID by ACEmanager Web UI Status/About page
        Args: 
            driver FF/IE web driver 
        Returns: 
            PRI ID
        '''

        msciid_str = str(msciids.MSCIID_STS_PRIID )
            
        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("PRI ID: "+ret)
        
        return ret 

    def get_rap_device_id(self, driver):
        '''get GPS/RAP Device ID by ACEmanager Web UI Status/About page
         Args: 
             driver FF/IE web driver 
         Returns: 
             GPS/RAP Device ID
        '''
        
        msciid_str = str(msciids.MSCIID_STS_RAP_DEVICEID )
            
        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("GPS/RAP Device ID: "+ret) 

        return ret 

    def get_eth_mac_addr(self, driver, eth_port=1):
        ''' get Ethernet Mac Address by ACEmanager Web UI Status/About page
        Args: 
            driver FF/IE web driver 
            eth_port ethernet port 1/2/3. 
                     1 - main ethernet port 
        Returns: 
            Ethernet Mac Address
        '''
        if eth_port == 1:
            msciid_str = str(msciids.MSCIID_INF_MAC_ADDR )
        elif eth_port == 2:
            msciid_str = str(msciids.MSCIID_INF_MAC_ADDR2 )
        elif eth_port == 3:
            msciid_str = str(msciids.MSCIID_INF_MAC_ADDR3 )
                        
        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("Ethernet Mac Address: "+ret) 

        return ret 

    def get_aleos_sw_build(self, driver):
        ''' get ALEOS SW build by ACEmanager Web UI Status/About page
        Args: 
            driver FF/IE web driver 
        Returns: 
            ALEOS SW build
        '''

        msciid_str = str(msciids.MSCIID_INF_ALEOS_SW_BUILD )
            
        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("ALEOS SW build: "+ret) 

        return ret  
    
    def get_device_hw_config(self, driver):
        ''' get Device Hardware Configuration by ACEmanager Web UI Status/About page
        Args: 
            driver FF/IE web driver 
        Returns: 
            Device Hardware Configuration
        '''

        msciid_str = str(msciids.MSCIID_INF_ALEOS_HW_VER )
        
        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("Device Hardware Configuration: "+ret) 
        
        return ret  

    def get_boot_ver(self, driver):
        ''' get Boot Version Version by ACEmanager Web UI Status/About page
        Args: 
            driver FF/IE web driver 
        Returns: 
            Boot Version
        '''

        msciid_str = str(msciids.MSCIID_INF_BOOT_VER )
            
        ret=self.get_element_by_id(driver, msciid_str)
        
        basic_airlink.cslog("Boot Version: "+ret) 
        
        return ret
    
    def get_msci_ver(self, driver):
        ''' get MSCI Version by ACEmanager Web UI Status/About page
        Args: 
            driver FF/IE web driver 
        Returns: 
            MSCI Version
        '''

        msciid_str = str(msciids.MSCIID_INF_VERSION )   
            
        ret=self.get_element_by_id(driver, msciid_str)

        basic_airlink.cslog("MSCI Version: "+ret) 
        
        return ret  
    
    def status_page(self, driver):
        ''' ACEmanager navigates to status page

        Args: 
            driver FF/IE web driver 
            
        Returns: 
            True/False
                    
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to status page: ")
        return self.navigate_tab(driver, "Status")    

    def status_home_page(self, driver):
        ''' ACEmanager navigates to Status/Home page
        Args: 
            driver - FF/IE web driver
        Returns: 
            True/False
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Status/Home page: ")
        return self.navigate_subtab(driver, "Status", "Home")    

    def status_wan_page(self, driver):
        ''' ACEmanager navigates to Status/WAN page
        Args: 
            driver - FF/IE web driver
        Returns: 
            True/False
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Status/WAN page: ")
        return self.navigate_subtab(driver, "Status", "WAN_Cellular")            
 
    def status_lan_page(self, driver, subtab = "LAN"):
        ''' ACEmanager navigates to Status/LAN page
        Args: 
            driver - Firefox/IE web driver
            
            subtab - "LAN" or "LAN_Wi-Fi or "LAN_WiFi"
            
        Returns: 
            True/False
        '''
        
        #basic_airlink.slog("step: from Ace Manager navigate to Status/LAN page: ")
        return self.navigate_subtab(driver, "Status", subtab)        
             
    def status_vpn_page(self, driver):
        ''' ACEmanager navigates to Status/VPN page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            True/False
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Status/VPN page: ")
        return self.navigate_subtab(driver, "Status", "VPN")    
  
    def status_security_page(self, driver):
        ''' ACEmanager navigates to Status/Security page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            True/False
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Status/Security page: ")
        return self.navigate_subtab(driver, "Status", "Security")    
 
    def status_services_page(self, driver):
        ''' ACEmanager navigates to Status/Services page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            True/False
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Status/Services page: ")
        return self.navigate_subtab(driver, "Status", "Services")    
        
    def status_gps_page(self, driver):
        ''' ACEmanager navigates to Status/GPS page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            True/False
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Status/GPS page: ")
        return self.navigate_subtab(driver, "Status", "GPS")    
        
    def status_serial_page(self, driver):
        ''' ACEmanager navigates to Status/Serial page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            True/False
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Status/Serial page: ")
        return self.navigate_subtab(driver, "Status", "Serial")    
        
    def status_applications_page(self, driver):
        ''' ACEmanager navigates to Status/Applications page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            True/False
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Status/Applications page: ")
        return self.navigate_subtab(driver, "Status", "Applications")    
        
    def status_about_page(self, driver):
        ''' ACEmanager navigates to Status/SAbout page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            True/False
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Status/About page: ")
        return self.navigate_subtab(driver, "Status", "About")    
                                    
    def wan_page(self, driver):
        ''' ACEmanager navigates to WAN page

        Args: 
            driver - Firefox/IE web driver
        Returns: 
            True/False
                    
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to WAN page: ")
        return self.navigate_tab(driver, "WAN_Cellular")        

    def wan_wan_page(self, driver):
        ''' ACEmanager navigates to WAN/Cellular page
        
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            True/False
        
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to WAN/Cellular page: ")
        return self.navigate_subtab(driver, "WAN_Cellular", "WAN_Cellular")         

    def wan_rsr_page(self, driver):
        ''' ACEmanager navigates to WAN/Reliable static Route page
        Args: 
            driver - Firefox/IE web driver
        Returns: 
            True/False      
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to WAN/RSR page: ")
        return self.navigate_subtab(driver, "WAN_Cellular", "Reliable_Static_Route_RSR")    
                
    def lan_page(self, driver, tab = "LAN"):
        ''' ACEmanager navigates to LAN page
        
        Args:
            driver FF/IE web driver 
            tab   "LAN","LAN_WiFi","LAN_Wi-Fi"

        Returns: 
            True/False 
                    
        '''
        #basic_airlink.slog("step: from ACEmanager navigate to LAN page ")
        return self.navigate_tab(driver, "LAN")        

    def lan_dhcp_addressing_page(self, driver):
        ''' ACEmanager navigates to LAN/DHCP addressing web page
        
        Args:
            driver: FF/IE web driver 
 
        Returns: 
            True/False 
                   
        '''
        #basic_airlink.slog("step: from ACEmanager navigate to LAN/Ethernet page ")
        return self.navigate_subtab(driver, "LAN", "DHCP_Addressing")    
        
    def lan_ethernet_page(self, driver):
        ''' ACEmanager navigates to LAN/Ethernet web page
        
        Args:
            driver: FF/IE web driver 

        Returns: 
            True/False         
        '''
        #basic_airlink.slog("step: from ACEmanager navigate to LAN/Ethernet page ")
        return self.navigate_subtab(driver, "LAN", "Ethernet")    

    def lan_usb_page(self, driver):
        ''' ACEmanager navigates to LAN/USB web page
        
        Args:
            driver: FF/IE web driver 

        Returns: 
            True/False 
                    
        '''
        #basic_airlink.slog("step: from ACEmanager navigate to LAN/USB page ")
        return self.navigate_subtab(driver, "LAN", "USB")    

    def lan_host_port_routing_page(self, driver):
        ''' ACEmanager navigates to LAN/Host Port Routing web page
        
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
                    
        '''
        #basic_airlink.slog("step: from ACEmanager navigate to LAN/Host Port Routing page ")
        return self.navigate_subtab(driver, "LAN", "Host_Port_Routing")    

    def lan_wifi_page(self, driver):
        ''' ACEmanager navigates to LAN/Wifi subtab
        
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
        
        '''
        return self.navigate_subtab(driver, "LAN", "Wi-Fi")    

                     
    def lan_global_dns_page(self, driver):
        ''' ACEmanager navigates to LAN/Global DNS web page
        
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
        
        '''
        #basic_airlink.slog("step: from ACEmanager navigate to LAN/Global DNS page ")        
        return self.navigate_subtab(driver, "LAN", "Global_DNS")    

    def lan_pppoe_page(self, driver):
        ''' ACEmanager navigates to LAN/PPPoE web page
        
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
        
        '''
        #basic_airlink.slog("step: from ACEmanager navigate to LAN/PPPoE page ")
        return self.navigate_subtab(driver, "LAN", "PPPoE")    
        
    def lan_vlan_page(self, driver):
        ''' ACEmanager navigates to LAN/VLAN web page
        
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
        
        '''
        #basic_airlink.slog("step: from ACEmanager navigate to LAN/VLAN page ")
        return self.navigate_subtab(driver, "LAN", "VLAN")    

    def lan_vrrp_page(self, driver):
        ''' ACEmanager navigates to LAN/VRRP web page
        
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
        
        '''
        #basic_airlink.slog("step: from ACEmanager navigate to LAN/VRRP page ")
        return self.navigate_subtab(driver, "LAN", "VRRP")    
        
    def lan_host_interface_watchdog_page(self, driver):
        ''' ACEmanager navigates to LAN/Host interface watchdog web page
        
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
        
        '''
        #basic_airlink.slog("step: from ACEmanager navigate to LAN/Host inrerface watchdog page ")
        return self.navigate_subtab(driver, "LAN", "Host_Interface_Watchdog")    
 
    def vpn_page(self, driver):
        ''' ACEmanager navigates to VPN tab
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False         
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to VPN tab ")
        return self.navigate_tab(driver, "VPN")    

    def vpn_split_tunnel_page(self, driver):
        ''' ACEmanager navigates to VPN/Split Tunnel subtab

        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False         
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to VPN/Split Tunnel subtab ")
        return self.navigate_subtab(driver, "VPN", "Split_Tunnel")    
                                                                                  
    def vpn_sub_page(self, driver, vpn_no):
        ''' ACEmanager navigates to VPN# sub tab page
        Args:
            driver: FF/IE web driver 
            vpn_no: VPN server number 
            
        Returns: 
            True/False         
        '''
        basic_airlink.slog("step: ACEmanager navigate to VPN subpage: " + str(vpn_no))

        if   vpn_no == 1: 
            driver.find_element_by_xpath("//li[@id='SM1_VPN_VPN 1M1']/a/span").click()
        elif vpn_no == 2: 
            driver.find_element_by_xpath("//li[@id='SM1_VPN_VPN 2M1']/a/span").click()
        elif vpn_no == 3: 
            driver.find_element_by_xpath("//li[@id='SM1_VPN_VPN 3M1']/a/span").click()
        elif vpn_no == 4: 
            driver.find_element_by_xpath("//li[@id='SM1_VPN_VPN 4M1']/a/span").click()
        elif vpn_no == 5: 
            driver.find_element_by_xpath("//li[@id='SM1_VPN_VPN 5M1']/a/span").click()
            
        time.sleep(1)     

    def vpn_1_page(self, driver):
        ''' ACEmanager navigates to VPN1 sub tab page
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False         
        '''
        #basic_airlink.slog("step: ACEmanager navigate to VPN 1 subtab: ")
        return self.navigate_subtab(driver, "VPN", "VPN_1")    

    def vpn_2_page(self, driver):
        ''' ACEmanager navigates to VPN2 sub tab page
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False         
        '''
        #basic_airlink.slog("step: ACEmanager navigate to VPN 2 subtab: ")
        return self.navigate_subtab(driver, "VPN", "VPN_2")    
         
    def vpn_3_page(self, driver):
        ''' ACEmanager navigates to VPN3 sub tab page
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False         
        '''
        #basic_airlink.slog("step: ACEmanager navigate to VPN 3 subtab: ")
        return self.navigate_subtab(driver, "VPN", "VPN_3")    
        
    def vpn_4_page(self, driver):
        ''' ACEmanager navigates to VPN4 sub tab page

        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
                    
        '''
        #basic_airlink.slog("step: ACEmanager navigate to VPN 4 subtab: ")
        return self.navigate_subtab(driver, "VPN", "VPN_4")    
     
    def vpn_5_page(self, driver):
        ''' ACEmanager navigates to VPN5 sub tab page

        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False         
        '''
        #basic_airlink.slog("step: ACEmanager navigate to VPN 5 subtab: ")
        return self.navigate_subtab(driver, "VPN", "VPN_5")    
                        
    def security_page(self, driver):
        ''' ACEmanager navigates to Security page
        
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False   
        
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Security page: ")
        return self.navigate_tab(driver, "Security")    

    def security_port_forwarding_page(self, driver):
        ''' ACEmanager navigates to Security/Port Forwarding page
        
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Security/Port Forwarding page: ")
        return self.navigate_subtab(driver, "Security", "Port_Forwarding")    

    def security_port_filtering_inbound_page(self, driver):
        ''' ACEmanager navigates to Security/Port Filtering inbound page
        
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
        
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Security/Port Filtering inbound page: ")
        return self.navigate_subtab(driver, "Security", "Port_Filtering_Inbound")    
        
    def security_port_filtering_outbound_page(self, driver):
        ''' ACEmanager navigates to Security/Port Filtering Outbound page
        
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False  
        
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Security/Port Filtering Outbound page: ")
        return self.navigate_subtab(driver, "Security", "Port_Filtering_Outbound")     

    def security_trusted_ips_inbound_page(self, driver):
        ''' ACEmanager navigates to Security/Trusted IP Inbound Friends page
        
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
        
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Security/Trusted IP Inbound page: ")
        return self.navigate_subtab(driver, "Security", "Trusted_IPs_Inbound_Friends")    
        
    def security_trusted_ips_outbound_page(self, driver):
        ''' ACEmanager navigates to Security/Trusted IP Outbound page
        
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Security/Trusted IP Outbound page: ")
        return self.navigate_subtab(driver, "Security", "Trusted_IPs_Outbound")    
        
    def security_mac_filtering_page(self, driver):
        ''' ACEmanager navigates to Security/MAC Filtering page
        
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Security/MAC filtering page: ")
        return self.navigate_subtab(driver, "Security", "MAC_Filtering")     
        
    def security_packet_inspection_page(self, driver):
        ''' ACEmanager navigates to Security/Packet Inspection page
        
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
        '''
        #basic_airlink.slog("step: ACEmanager navigates to Security/Packet Inspection page: ")
        return self.navigate_subtab(driver, "Security", "Packet_Inspection")    
                      
    def services_page(self, driver):
        ''' ACEmanager navigates to Services page
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False     
        '''
        #basic_airlink.slog("step: ACEmanager navigates to Services page: ")
        return self.navigate_tab(driver, "Services")       

    def services_avms_page(self, driver):
        ''' ACEmanager navigates to Services/AVMS subtab
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False     
        '''
        #basic_airlink.slog("step: ACEmanager navigates to Services/AVMS subtab: ")
        return self.navigate_subtab(driver, "Services", "AVMS")    
               
    def services_acemanager_page(self, driver):
        ''' ACEmanager navigates to Services/ACEmanager subtab 
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False     
        '''
        #basic_airlink.slog("step: ACEmanager navigates to Services/ACEmanager subtab: ")
        return self.navigate_subtab(driver, "Services", "ACEmanager")    
        
    def services_lpm_page(self, driver):
        ''' ACEmanager navigates to Services/Low Power Mode subtab 
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False    
        '''
        #basic_airlink.slog("step: ACEmanager navigates to Services/LPM subtab: ")
        return self.navigate_subtab(driver, "Services", "Low_Power")    
        
    def services_dynamic_dns_page(self, driver):
        ''' ACEmanager navigates to Services/Dynamic DNS subtab
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False    
        '''
        #basic_airlink.slog("step: ACEmanager navigates to Services/Dynamic DNS subtab: ")
        return self.navigate_subtab(driver, "Services", "Dynamic_DNS")    

    def services_wifi_landing_page(self, driver):
        ''' ACEmanager navigates to Services/Wifi landing subtab
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False                
        '''       
        return self.navigate_subtab(driver, "Services", "Wi-Fi_Landing_Page")    
                
    def services_sms_page(self, driver):
        ''' ACEmanager navigates to Services/SMS subtab
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
        '''
        #basic_airlink.slog("step: ACEmanager navigates to Services/SMS subtab: ")
        return self.navigate_subtab(driver, "Services", "SMS")    
        
    def services_telnet_ssh_page(self, driver):
        ''' ACEmanager navigates to Services/Telnet/ssh subtab 
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
        '''
        #basic_airlink.cslog("step: ACEmanager navigate to Services/Telnet/SSH subtab: ")
        return self.navigate_subtab(driver, "Services", "Telent_SSH")    

    def services_email_smtp_page(self, driver):
        ''' ACEmanager navigates to Services/Email(SMTP) subtab 
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False 
        '''
        #basic_airlink.cslog("step: ACEmanager navigate to Services/Email (SMTP) subtab: ")
        return self.navigate_subtab(driver, "Services", "Email_SMTP")    

    def services_management_snmp_page(self, driver):
        ''' ACEmanager navigates to Services/Management SNMP subtab
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False    
        '''
        #basic_airlink.slog("step: ACEmanager navigate to Services/ Management (SNMP) subtab: ")
        return self.navigate_subtab(driver, "Services", "Management_SNMP")    
        
    def services_time_sntp_page(self, driver):
        ''' ACEmanager navigates to Services/Time (SNTP) subtab
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False      
        '''
        #basic_airlink.slog("step: ACEmanager navigate to Services/Time (SNTP) subtab: ")
        return self.navigate_subtab(driver, "Services", "Time_SNTP")    
 
    def services_device_status_screen_page(self, driver):
        ''' ACEmanager navigates to Services/Device Status Screeen subtab
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False      
        '''
        #basic_airlink.slog("step: ACEmanager navigate to Services/Device Status Screen subtab: ")
        return self.navigate_subtab(driver, "Services", "Device_Status_Screen")    
               
    def gps_page(self, driver):
        ''' ACEmanager navigates to GPS page
        Args:
            driver: FF/IE web driver 
            
        Returns: 
            True/False         
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to GPS page: ")
        return self.navigate_tab(driver, "GPS")         

    def gps_server_page(self, driver, server_no):
        ''' ACEmanager navigates to GPS/Server page
        
        Args: 
            driver: FF/IE web driver 
            server_no: GPS server number(1-4)
        Returns: 
            True/False         
        
        '''
        basic_airlink.slog("step: from Ace Manager navigate to GPS/Server page: ")
        
        if server_no == 1: 
            driver.find_element_by_xpath("//li[@id='SM1_GPS_Server 1M1']/a/span").click()
        elif server_no == 2: 
            driver.find_element_by_xpath("//li[@id='SM1_GPS_Server 2M1']/a/span").click()
        elif server_no == 3: 
            driver.find_element_by_xpath("//li[@id='SM1_GPS_Server 3M1']/a/span").click()
        elif server_no == 4: 
            driver.find_element_by_xpath("//li[@id='SM1_GPS_Server 4M1']/a/span").click()
        else: 
            basic_airlink.slog("wrong server number parameter! ")

        time.sleep(2)

    def gps_server_1_page(self, driver):
        ''' ACEmanager navigates to GPS/Server 1 subtab
        
        Args: 
            driver: FF/IE web driver 
            server_no: GPS server number(1-4)
        Returns: 
            True/False         
        
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to GPS/Server 1 subtab: ")
        return self.navigate_subtab(driver, "GPS", "Server_1")    
        
    def gps_server_2_page(self, driver):
        ''' ACEmanager navigates to GPS/Server 2 subtab
        
        Args: 
            driver: FF/IE web driver 
            server_no: GPS server number(1-4)
        Returns: 
            True/False         
        
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to GPS/Server 2 subtab: ")
        return self.navigate_subtab(driver, "GPS", "Server_2")    
        
    def gps_server_3_page(self, driver):
        ''' ACEmanager navigates to GPS/Server 3 subtab
        
        Args: 
            driver: FF/IE web driver 
            server_no: GPS server number(1-4)
        Returns: 
            True/False         
        
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to GPS/Server 3 subtab: ")
        return self.navigate_subtab(driver, "Admin", "Server_3")    
        
    def gps_server_4_page(self, driver):
        ''' ACEmanager navigates to GPS/Server 4 subtab
        
        Args: 
            driver: FF/IE web driver 
            server_no: GPS server number(1-4)
        Returns: 
            True/False         
        
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to GPS/Server 4 subtab: ")
        return self.navigate_subtab(driver, "GPS", "Server_3")    
  
        
    def gps_local_streaming_page(self, driver):
        ''' ACEmanager navigates to GPS/local streaming page
        
        Args: 
            driver: FF/IE web driver 
        Returns: 
            True/False         
        
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to GPS/Local streaming page: ")        
        return self.navigate_subtab(driver, "GPS", "Local_Streaming")    

    def gps_global_settings_page(self, driver):
        ''' ACEmanager navigates to GPS/Global settings page
        
        Args: 
            driver: FF/IE web driver 
        Returns: 
            True/False         
        
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to GPS/Global settings page: ")
        return self.navigate_subtab(driver, "GPS", "Global_Settings")                  

    def er_page(self, driver):
        ''' ACEmanager navigates to Events Reporting page

        Args: 
            driver: FF/IE web driver 
        Returns: 
            True/False  
                    
        '''
        #basic_airlink.slog("step: Ace Manager navigates to Events Reporting page: ")
        return self.navigate_tab(driver, "Events_Reporting")       

    def er_events_page(self, driver):
        ''' ACEmanager navigates to Events Reporting/Events page
        Args: 
            driver: FF/IE web driver 
        Returns: 
            True/False          
        '''
        #basic_airlink.slog("step: ACEmanager navigates to Events Reporting/Events page: ")
        return self.navigate_subtab(driver, "Events_Reporting","Events")

    def er_actions_page(self, driver):
        ''' ACEmanager navigates to Events Reporting/Actions page

        Args: 
            driver: FF/IE web driver 
        Returns: 
            True/False  
                    
        '''
        #basic_airlink.slog("step: ACEmanager navigates to Events Reporting/Actions page: ")
        return self.navigate_subtab(driver, "Events_Reporting","Actions")
        
    def serial_page(self, driver):
        ''' ACEmanager navigates to Serial page

        Args: 
            driver: FF/IE web driver 
        Returns: 
            True/False          
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Serial page: ")
        return self.navigate_tab(driver, "Serial")        

    def serial_port_configuration_page(self, driver):
        ''' ACEmanager navigates to Serial page/Port_Configuration
         Args: 
            driver: FF/IE web driver 
        Returns: 
            True/False         
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Serial page/Port_Configuration: ")
        return self.navigate_subtab(driver, "Serial","Port_Configuration")  

    def serial_modbus_address_list_page(self, driver):
        ''' ACEmanager navigates to Serial page/MODBUS_Address_List
        Args: 
            driver: FF/IE web driver 
        Returns: 
            True/False          
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Serial page/MODBUS_Address_List: ")
        return self.navigate_subtab(driver, "Serial","MODBUS_Address_List")  
            
                        
    def applications_page(self, driver):
        ''' ACEmanager navigates to Applications page
        Args: 
            driver: FF/IE web driver 
        Returns: 
            True/False          
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Application page: ")
        return self.navigate_tab(driver, "Applications")    

    def applications_data_usage_page(self, driver):
        ''' ACEmanager navigates to Applications/Data_Usage page
        Args: 
            driver: FF/IE web driver 
        Returns: 
            True/False      
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Application/Data_Usage page: ")
        return self.navigate_subtab(driver, "Applications","Data_Usage")  
    
    def applications_garmin_page(self, driver):
        ''' ACEmanager navigates to Applications/Garmin page
        Args: 
            driver: FF/IE web driver 
        Returns: 
            True/False     
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Application/Garmin page: ")
        return self.navigate_subtab(driver, "Applications","Garmin")  
    
    def applications_aleos_applicatio_framework_page(self, driver):
        ''' ACEmanager navigates to Applications/ALEOS_Application_Framework page
        Args: 
            driver: FF/IE web driver 
        Returns: 
            True/False    
        '''
        #basic_airlink.slog("step: from Ace Manager navigate to Application/ALEOS_Application_Framework page: ")
        return self.navigate_subtab(driver, "Applications","ALEOS_Application_Framework")  
            
    def io_page(self, driver):
        ''' ACEmanager navigates to I/O page
        Args: 
            driver: FF/IE web driver 
        Returns: 
            True/False   
        '''
        #basic_airlink.slog("step: ACEmanager navigates to I/O page: ")
        return self.navigate_tab(driver, "IO")
     

    def io_current_state_page(self, driver):
        ''' ACEmanager navigates to IO/Current state subtab
        Args: 
            driver: FF/IE web driver 
        Returns: 
            True/False    
        '''
        #basic_airlink.slog("step: ACEmanager navigates to IO/Current state subtab: ")
        return self.navigate_subtab(driver, "IO", "Current_State")
  
        
    def io_configuration_page(self, driver):
        ''' ACEmanager navigates to IO/Configuration subtab 
        Args: 
            driver: FF/IE web driver 
        Returns: 
            True/False   
        '''
        #basic_airlink.slog("step: ACEmanager navigates to IO/Configuration subtab: ")
        return self.navigate_subtab(driver, "IO", "Configuration")
    
            
    def admin_page(self, driver):
        ''' ACEmanager navigates to Admin page  
        Args:
        driver  - Firefox/IE web driver 
        
        Returns:
            True/False
            
        ''' 
                     
        #basic_airlink.slog("step: navigate from ACEmanager to Admin page: ")
        return self.navigate_tab(driver, "Admin")
 
 
    def admin_change_password_page(self, driver):
        ''' ACEmanager navigates to Admin page  
        args:
        driver  - Firefox/IE web driver 
        
        returns:
            True/False
            
        ''' 
                     
        #basic_airlink.slog("step: navigate from ACEmanager to Admin/Change Password page: ")
        return self.navigate_subtab(driver, "Admin", "Change_Password")


    def admin_advanced_page(self, driver):
        ''' ACEmanager navigates to Admin/Advanced page  
        args:
        driver  - Firefox/IE web driver 
        
        returns:
            True/False
            
        ''' 
                     
        #basic_airlink.slog("step: navigate to Admin/Advanced page: ")
        return self.navigate_subtab(driver, "Admin", "Advanced")
                

    def admin_radio_passthru_page(self, driver):
        ''' ACEmanager navigates to Admin/Radio passthru page  
        args:
        driver  - Firefox/IE web driver 
        
        returns:
            True/False
            
        ''' 
                     
        #basic_airlink.slog("step: navigate to Admin/Radio Passthru page: ")
        return self.navigate_subtab(driver, "Admin", "Radio_Passthru")


    def admin_log_page(self, driver):
        ''' ACEmanager navigates to Admin/Log page  
        args:
        driver  - Firefox/IE web driver 
        
        returns:
            True/False
            
        ''' 
                     
        #basic_airlink.slog("step: navigate to Admin/log page: ")
        return self.navigate_subtab(driver, "Admin", "Log")
 
    def admin_configure_logging_page(self, driver):
        ''' ACEmanager navigates to Admin/Log/Config page  
        args:
        driver  - Firefox/IE web driver 
        
        returns:
            True/False
            
        ''' 
                     
        #basic_airlink.slog("step: navigate to Admin/log page: ")
        return self.navigate_subtab(driver, "Admin", "Log_Configure_Logging")

        
    def admin_view_log_page(self, driver):
        ''' ACEmanager navigates to Admin/Log/view page  
        args:
        driver  - Firefox/IE web driver 
        
        returns:
            True/False
            
        ''' 
                     
        #basic_airlink.slog("step: navigate to Admin/log/View page: ")             
        return self.navigate_subtab(driver, "Admin", "Log_View_Log")
    
    def retry_match_state(self, driver, state, fail_refresh_count, restart_count, refresh_delta_time, url, username, password):
        ''' retry to get the correct state in UI, refresh the page if the state is not match, 
            restart the browser after refreshing does not work 
        Args: 
            diver : FF/IE web driver
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
    
        
    def get_current_tab(self, driver, flag = 1):
        '''
         get the current page (Status/VPN/WAN/etc) 
         Args: 
             flag  1 to get the current tab, don't do any convertion
                   2 to get the current tab, and remove '/' from return string if exist
         Usage:
             get_current_tab(driver)
             get_current_tab(driver,2)
             
         Return: string the current tab page
        '''
        self.error_flag+=1
        
        txt = ""
        try:
            txt= driver.find_element_by_class_name("current").text
            if flag == 1: 
                basic_airlink.slog("current tab : "+ txt)
            elif flag ==2:
                txt = txt.replace('/','_').replace(' ','_')
                basic_airlink.slog("current converted tab : "+ txt)
               
        except NoSuchElementException:
            
            basic_airlink.slog("get_element_by_class_name: cannot find current tab")
            self.error_flag+=1
        
        finally: 
            return txt           

    def get_current_subtab(self, driver, flag=1):
        '''
         get the current subtab page under tab
         Args: 
             flag  1 to get the current subtab, don't do any convertion
                   2 to get the current subtab, and convert '/' or ' ' or '(' or ')' to '_' in string.
         Usage:
             get_current_subtab(driver)
             get_current_subtab(driver,2)
             
         Return: string the current subtab page
         '''        
        txt = ""
        try:
            txt= driver.find_element_by_xpath("//td[@class='fsm']//li[@class='current']").text
            if flag == 1:
                basic_airlink.cslog("current subtab : "+ txt)
            elif flag == 2: # with editing
                txt = txt.replace(')','').replace(' (','_').replace('/','_').replace(' ','_')
                basic_airlink.cslog("current subtab : "+ txt)
            
        
        except NoSuchElementException:
            
            basic_airlink.slog("get_element_by_xpath: cannot find current subtab")
            self.error_flag+=1
        finally:
            return txt  
        
    def navigate_tab(self, driver, tab):
        '''
        This function gets the desired tab and navigates to it.
        Tab is defined as those selectable items on top of each page of the 
        Acemanager for each tab.
        (e.g. Status, VPN,GPS, Services, etc.)
        Args: 
            tab:  tab name in ACEmanager UI ("Status","WAN_Cellular",..."Admin")
        Usage: 
            navigate_tab(driver, "Status")
            navigate_tab(driver, "WAN_Cellular")
            navigate_tab(driver, "LAN_Wi-Fi")
            
        Reurns: True/False
        
        '''
        ret = True
        cur_page = self.get_current_tab(driver,2)
        if cur_page == tab: 
            return ret   
                
        try:
            

            if ace_config_map[self.aleos_sw_ver][self.device_name][tab]["TAB"][0] == "BY_CSS_SELECTOR":
                driver.find_element_by_css_selector(ace_config_map[self.aleos_sw_ver][self.device_name][tab]["TAB"][1]).click()
                
            elif ace_config_map[self.aleos_sw_ver][self.device_name][tab]["TAB"][0] == "BY_ID":
                driver.find_element_by_id(ace_config_map[self.aleos_sw_ver][self.device_name][tab]["TAB"][1]).click()
            
            elif ace_config_map[self.aleos_sw_ver][self.device_name][tab]["TAB"][0] == "BY_XPATH":
                driver.find_element_by_xpath(ace_config_map[self.aleos_sw_ver][self.device_name][tab]["TAB"][1]).click()
            else:
                basic_airlink.cslog( "Incorrect byhow")
                ret = False
                
            time.sleep(1)               
            
            if ace_config_map[self.aleos_sw_ver][self.device_name][tab]["TAB"][2] == 1: 
                self.expand_all(driver) 
            
            self.refresh(driver)
                        

        except: 
            self.error_flag +=1
            basic_airlink.cslog("Navigating tab has Exception occurred", "RED", "WHITE")

            ret = False
            
        finally:
          
            return ret 
        
    def navigate_subtab(self, driver, tab, subtab):
        '''
        This function navigates to the specified Tab/Subtab page in ACEmanager 
        UI.
        
        Args: 
            tab:  Tab is defined as those selectable items on top of each page 
                  of the Acemanager for each tab. 
                  (e.g. Status, VPN,GPS, Services, etc.)
            subtab:  subtab name under tab in ACEmanager UI 
            
        Usage: 
            navigate_subtab(driver, "Status","Home")
            navigate_subtab(driver, "WAN_Cellular","WAN_Cellular")
            navigate_subtab(driver, "LAN_Wi-Fi","Wi-Fi")
            
        Reurns: True/False
        
        '''

        ret = True
        
        cur_subtab = self.get_current_subtab(driver,2)
        if cur_subtab == subtab: 
            return ret              
                
        basic_airlink.cslog( "Begins navigating subtab "+ tab +"/"+subtab)
                 
        try:
            cur_page = self.get_current_tab(driver,2)
            
            if cur_page != tab: 
                self.navigate_tab(driver, tab)
            
            if ace_config_map[self.aleos_sw_ver][self.device_name][tab][subtab][0] == "BY_CSS_SELECTOR":
                driver.find_element_by_css_selector(ace_config_map[self.aleos_sw_ver][self.device_name][tab][subtab][1]).click()
                
            elif ace_config_map[self.aleos_sw_ver][self.device_name][tab][subtab][0] == "BY_ID":
                driver.find_element_by_id(ace_config_map[self.aleos_sw_ver][self.device_name][tab][subtab][1]).click()
    
            elif ace_config_map[self.aleos_sw_ver][self.device_name][tab][subtab][0] == "BY_XPATH":
                driver.find_element_by_xpath(ace_config_map[self.aleos_sw_ver][self.device_name][tab][subtab][1]).click()
            else:
                basic_airlink.cslog( "Incorrect byhow parameter or NA subtab")
                ret = False       
                        
            time.sleep(1)               

            if ace_config_map[self.aleos_sw_ver][self.device_name][tab][subtab][2] == 1: 
                self.expand_all(driver) 
 
            self.refresh(driver)
            
        except: 
            self.error_flag +=1
            basic_airlink.cslog("Navigating subtab has Exception occurred, due to error or NA", "RED", "WHITE")
            
            ret = False
            
        finally:

            return ret 
        
    def expand_all(self,driver):
        '''
        This functions click on the expand-all button in the Acemanager
        '''
        driver.find_element_by_id("btn_Expand").click()
        basic_airlink.slog("Expanded all the tiers")
        
    def verify_config(self, driver, config_elements):
        '''
        This function verifies the UI configurations that were already set by user.
        Args:
        config_elements: is a list of dictionaries that is used for storing the changes in UI.
        
        
        example: We want to set the field:"Device IP" in the tab:"LAN" and sub-tab:"Ethernet"
                 We need to append to the list as follows:
                 config_elements.append({'tab':"LAN",'subtab':"Ethernet",'byhow':'name','field':"1084",'value':"192.168.13.31"})
                 where the entries of this list are as follows:
                 
            
            'tab' : this entry holds the tab that we are intedning to make a change. (e.g. "LAN")
            'subtab': this entry holds the sub-tab that we are intedning to make a change. (e.g. index "Ethernet" in the tab "LAN")
            'byhow' : this entry holds the type of the set function we used for changing. (e.g. set_element_by_name or set_element_by_id)
                     For now only two types of set_ functions are condiered: "BY_NAME" and "BY_ID".
            'field': this entry holds the field that we are intending to change. 
                     (e.g. "1084" which corresponds to the field "Device IP" in Acemanager in the tab "LAN" and sub-tab "Ethernet")
            'flag' :  The default is 1.  when byhow is "BY_ID", flag will be  1(get text), 2(get title), 0(get element only) 
                        when byhow is "by_NAME", flag will be  1(get value) or 2(get title) or 0 (get element only)
            'value': this entry holds the value we want to enter in that field.
                     (e.g. "192.168.13.31")
        Returns: 
            
            True: if the UI configuaration verification is passed successfully.
            False: if the UI configuaration verification is failed.
        '''
        
        basic_airlink.slog("\nVerifying UI configurations\n*****************************\n")
        
        # current contains the current list which is popped out in the current iteration
        current={'tab':'','subtab':'','byhow':'','field':'','flag':1,'value':''}
        
        # prev contains the previous list which was popped out in previous iteration
        prev={'tab':'','subtab':'','byhow':'','field':'','flag':1,'value':''}
        
        # at each iteration one list gets popped out and is stored in current.
        while len(config_elements):
            
            prev=current
            current=config_elements.pop()

            

            if (current['tab']==prev['tab']) and (current['subtab']==prev['subtab']):
                basic_airlink.slog("We're still in the same tab and subtab")
                    
            else:
                self.navigate_subtab(driver, current['tab'], current['subtab'])

            #this condition checks if the element was set using set_element_by_name
            if current['byhow']=='BY_NAME':
                if self.get_element_by_name(driver, current['field'])!=current['value']:
                    #basic_airlink.slog('UI verification is failed')
                    return False
            
            #this condition checks if the element was set using set_element_by_id
            if current['byhow']=='BY_ID':
                if self.get_element_by_id(driver, current['field'])!=current['value']:
                    #basic_airlink.slog('UI verification is failed')
                    return False
            
        return True
    
    def add_config_elements(self,config_elements,tab,subtab,byhow,field,value,flag=1):
        '''
        This function gets the list and the info related to the change and append a dictionary to the list.
        The dictionary to be appeneded is as follows:
        
        {'tab':tab,'subtab':subtab,'byhow':byhow,'field':field,'value':value}
        
        Args:
        config_elements: the list that we want to append to it.
        tab,subtab,byhow,field,value are the keys of the dictionary
        
        Returns:
        The list affter the dictionary is appended to it.
        '''
        config_elements.append({'tab':tab,'subtab':subtab,'byhow':byhow,'field':field,'flag':flag,'value':value})
        return config_elements
    
    def get_parents(self, msciid):
        ''' find TAB/SUBTAB based on msciid and acemanager_msciids_x.y.z.yml
        x.y.x is ALEOS version short format.
        Returns: 
            TAB
            SUBTAB
        '''
        return self.ele_config_map[msciid][0],self.ele_config_map[msciid][1]
    
    def set_device_ip(self, driver, value):
        '''Set device IP in ACEManager
        
        Args: driver
              value
        
        Return: True/False
        
        '''
        id = str(msciids.MSCIID_CFG_CMN_HOST_LOCAL_IP)
        print "deviceIP:"+id
        return self.set_element_by_name(driver, id, value)
          
         
    
    
    