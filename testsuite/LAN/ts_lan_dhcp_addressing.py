#################################################################################
#
# This module automates LAN's DHCP/Addressing test cases. 
# Company: Sierra Wireless
# Date: Jul 5, 2013
# 
#################################################################################

import os
import sys
import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, \
    WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.remote.webdriver
from selenium.webdriver.support.ui import Select
import yaml

import basic_airlink
import connectivity
import selenium_utilities


airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")
sys.path.append(".")

basic_airlink.append_sys_path()

tbd_config_map, lan_config_map = basic_airlink.get_config_data("LAN","")
    
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
   
class TsLanDhcpAddressing(unittest.TestCase):
    ''' This test suite automates LAN testcases by ACEmanager Web UI.
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
        basic_airlink.slog("step: close Firefox")  
        self.driver.quit()         
        self.assertEqual([], self.verificationErrors) 

        basic_airlink.slog(" Testcase complete")
           
    def tc_all_hosts_use_private_ips_default(self):
        ''' Testcase - all hosts use private IPs default
        '''
        
        # step: come to LAN page from AceManager, and set host connection mode         
        self.se_ins.lan_page(self.driver )
           
        self.se_ins.set_host_connection_mode(self.driver , "1")
        
        self.se_ins.apply_reboot(self.driver )
        self.se_ins.quit(self.driver )
    
        # Step: wait till device ready
        basic_airlink.slog("step: wait till device ready" )  
        time.sleep(tbd_config_map[self.device_name ]["REBOOT_TIMEOUT"]) 

        # step: login to ACEmanager 
        basic_airlink.slog("step: login to ACEmanager")
        ace_manager_url = self.conn_ins.get_url()
        self.driver = self.se_ins.login(ace_manager_url, tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])
        
        # Step:  get net IP from Status/Home page
        xcard_type =self.se_ins.get_xcard_type(self.driver )
        xcard_state=self.se_ins.get_xcard_state(self.driver )

        # come to LAN page 
        self.se_ins.lan_page(self.driver )
        
        #step: check each item at LAN home page 
        basic_airlink.slog("step: check each item at LAN DHCP/Addressing page")
        
        #step: check Host connect mode
        ret = self.se_ins.get_host_connection_mode(self.driver )          
        basic_airlink.slog("Host connect mode: " +ret)  
        self.assertEqual(ret, "1")               
 
        #step: check DHCP lease timer
        ret = self.se_ins.get_dhcp_lease_timer(self.driver )       
        basic_airlink.slog("DHCP lease timer: " +ret)  
        self.assertNotEqual(ret, "0")               
        
        #step: check DHCP domain               
        ret = self.se_ins.get_dhcp_domain(self.driver )          
        basic_airlink.slog("DHCP domain  : " +ret)  

        #step: check MTU             
        ret = self.se_ins.get_dhcp_mtu_size(self.driver )  
        basic_airlink.slog("MTU: " +ret)  
        self.assertEqual(ret, "1500")    

        bridge_wifi_to_ethernet_d2="Disabled"
        wifi_mode_d1="WIFI OFF"
                    
        if xcard_type == "WiFi X-Card" and xcard_state == "X-Card Connected":
            bridge_wifi_to_ethernet_d2=self.se_ins.get_bridge_wifi_to_ethernet_d2(self.driver )
            wifi_mode_d1=self.se_ins.get_wifi_mode_d1(self.driver )
              
        # Creates a list containing 5 lists initialized to 0
        matrix_lan_address = [["" for j in range(9)] for i in range(7)] 
        
        #step: check Ethernet IP, USBNET IP 
        for i in range(3,5): 
            for j in range(1,9):             
                mylist = self.driver .find_elements_by_xpath("//*[@id='9060002']/tr["+str(i)+"]/td["+str(j)+"]")   
                for  k in mylist: 
                    matrix_lan_address[i][j]=k.text    
                basic_airlink.slog(str(i)+" " +str(j)+" "+matrix_lan_address[i][j])    
        
        if bridge_wifi_to_ethernet_d2 == "Enabled" and wifi_mode_d1 != "WIFI OFF":
            self.assertEqual(matrix_lan_address[3][1], "Ethernet/WiFi")
        else:
            self.assertEqual(matrix_lan_address[3][1], "Ethernet")
        self.assertEqual(matrix_lan_address[3][3], lan_config_map["ETH_DEVICE_IP"])
        self.assertEqual(matrix_lan_address[3][4], lan_config_map["ETH_SUBNET_MASK"])
        self.assertEqual(matrix_lan_address[3][5], "Yes")     # Access Internet
        self.assertEqual(matrix_lan_address[3][6], "Enable")  # DHCP Server Mode
        self.assertEqual(matrix_lan_address[3][7], lan_config_map["ETH_STARTING_IP"]) #starting IP
        self.assertEqual(matrix_lan_address[3][8], lan_config_map["ETH_ENDING_IP"])  #Ending IP
                
        self.assertEqual(matrix_lan_address[4][1], "USBNET")
        self.assertEqual(matrix_lan_address[4][3], lan_config_map["USB_DEVICE_IP"])
        self.assertEqual(matrix_lan_address[4][4], lan_config_map["USB_SUBNET_MASK"])
        self.assertEqual(matrix_lan_address[4][5], "Yes")     # Access Internet
        self.assertEqual(matrix_lan_address[4][6], "Enable")  # DHCP Server Mode        
        self.assertEqual(matrix_lan_address[4][7], lan_config_map["USB_STARTING_IP"]) #starting IP
        self.assertEqual(matrix_lan_address[4][8], lan_config_map["USB_ENDING_IP"]) #Ending IP
 
        cmd = 'ipconfig > ipconfig_out.txt'
        ret=os.system(cmd)   
        basic_airlink.slog(str(ret))
        self.assertEqual(ret,0)
        self.assertNotEqual(os.path.getsize("ipconfig_out.txt"),0)
        self.assertTrue(lan_config_map["ETH_STARTING_IP"] in open('ipconfig_out.txt').read())                                                        
          
    def tc_ethernet_uses_public_ip(self):
        '''See testcase - Ethernet uses public IP.
        '''         
        # step: come to WAN page from AceManager, and set APN        
        self.se_ins.wan_page(self.driver)
        self.se_ins.set_apn(self.driver, tbd_config_map)
        self.se_ins.apply(self.driver)
              
        # step: come to LAN page from AceManager, and set host connection mode         
        self.se_ins.lan_page(self.driver)
        self.se_ins.set_host_connection_mode(self.driver, "0")
        
        self.se_ins.apply_reboot(self.driver)
        self.se_ins.quit(self.driver)
    
        # Step: wait till device ready
        basic_airlink.slog("step: wait till device ready" )  
        time.sleep(tbd_config_map[self.device_name ]["REBOOT_TIMEOUT"]) 

        # step: login to ACEmanager 
        basic_airlink.slog("step: login to ACEmanager")
        ace_manager_url = self.conn_ins.get_url()
        self.driver = self.se_ins.login(ace_manager_url, tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])           
        
        #step: to get the net IP from Status/Home page
        netip = self.se_ins.get_net_ip(self.driver)

        #step: come to LAN page 
        self.se_ins.lan_page(self.driver)
        
        #step: check each item at LAN home page 
        basic_airlink.slog("step: check each item at LAN DHCP/Addressing page")
        
        #step: check Host connect mode 
        ret = self.se_ins.get_host_connection_mode(self.driver)         
        basic_airlink.slog("Host connect mode: " + str(ret))  
        self.assertEqual(ret, "0")            
 
        # Creates a list containing 9 lists initialized to 0
        matrix_lan_address = [["" for j in range(9)] for i in range(7)] 
        
        #step: check Ethernet IP, USBNET IP 
        for i in range(3,5): 
            for j in range(1,9):             
                mylist = self.driver.find_elements_by_xpath("//*[@id='9060002']/tr["+str(i)+"]/td["+str(j)+"]")   
                for  k in mylist: 
                    matrix_lan_address[i][j]=k.text    
                basic_airlink.slog(str(i)+" " +str(j)+" "+matrix_lan_address[i][j])    
        
        self.assertEqual(matrix_lan_address[3][1], "Ethernet")
        self.assertEqual(matrix_lan_address[3][3], lan_config_map["ETH_DEVICE_IP"])
        self.assertEqual(matrix_lan_address[3][4], lan_config_map["ETH_SUBNET_MASK"])
        self.assertEqual(matrix_lan_address[3][5], "Yes")     # Access Internet
        self.assertEqual(matrix_lan_address[3][6], "Enable")  # DHCP Server Mode
        self.assertEqual(matrix_lan_address[3][7], netip)     #Starting IP
        self.assertEqual(matrix_lan_address[3][8], netip)     #Ending IP
        
        self.assertEqual(matrix_lan_address[4][1], "USBNET")
        self.assertEqual(matrix_lan_address[4][3], lan_config_map["USB_DEVICE_IP"])
        self.assertEqual(matrix_lan_address[4][4], lan_config_map["USB_SUBNET_MASK"])
        self.assertEqual(matrix_lan_address[4][5], "Yes")     # Access Internet
        self.assertEqual(matrix_lan_address[4][6], "Enable")  # DHCP Server Mode        
        self.assertEqual(matrix_lan_address[4][7], lan_config_map["USB_STARTING_IP"]) #starting IP
        self.assertEqual(matrix_lan_address[4][8], lan_config_map["USB_ENDING_IP"]) #Ending IP
    
        cmd = 'ipconfig > ipconfig_out.txt'
        ret=os.system(cmd)   
        basic_airlink.slog(str(ret))
        self.assertEqual(ret,0)
        self.assertNotEqual(os.path.getsize("ipconfig_out.txt"),0)
        self.assertTrue(netip in open('ipconfig_out.txt').read())              
            
    def tc_usb_uses_public_ip(self):
        '''See testcase - USB uses public IP
        '''          
 
        # step: come to WAN page from AceManager, and set APN        
        self.se_ins.wan_page(self.driver)
        self.se_ins.set_apn(self.driver, tbd_config_map)
        self.se_ins.apply(self.driver)
               
        # step: come to LAN page from AceManager, and set host connection mode         
        self.se_ins.lan_page(self.driver )
           
        self.se_ins.set_host_connection_mode(self.driver , "2")
        
        self.se_ins.apply_reboot(self.driver )
        self.se_ins.quit(self.driver )
    
        # Step: wait till device ready
        basic_airlink.slog("step: wait till device ready" )  
        time.sleep(tbd_config_map[self.device_name ]["REBOOT_TIMEOUT"]) 

        # step: login to ACEmanager 
        basic_airlink.slog("step: login to ACEmanager")
        
        ace_manager_url = self.conn_ins.get_url()
        self.driver = self.se_ins.login(ace_manager_url, tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])
           
        # come to Status page 
        #self.se_ins.status_page(driver)
        
        # Step:  get net IP from Status/Home page
        netip = self.se_ins.get_net_ip(self.driver)

        # come to LAN page 
        self.se_ins.lan_page(self.driver)
        
        #step: check each item at LAN home page 
        basic_airlink.slog("step: check each item at LAN DHCP/Addressing page")
        
        #step: check Host connect mode
        ret = self.se_ins.get_host_connection_mode(self.driver)          
        basic_airlink.slog("Host connect mode: " + str(ret))  
        self.assertEqual(ret, "2")            
        
        # Creates a list containing 9 lists initialized to 0
        matrix_lan_address = [["" for j in range(9)] for i in range(7)] 
        
        #step: check Ethernet IP, USBNET IP 
        for i in range(3,5): 
            for j in range(1,9):             
                mylist = self.driver.find_elements_by_xpath("//*[@id='9060002']/tr["+str(i)+"]/td["+str(j)+"]")   
                for  k in mylist: 
                    matrix_lan_address[i][j]=k.text    
                basic_airlink.slog(str(i)+" " +str(j)+" "+matrix_lan_address[i][j])    
        
        self.assertEqual(matrix_lan_address[3][1], "Ethernet")
        self.assertEqual(matrix_lan_address[3][3], lan_config_map["ETH_DEVICE_IP"])
        self.assertEqual(matrix_lan_address[3][4], lan_config_map["ETH_SUBNET_MASK"])
        self.assertEqual(matrix_lan_address[3][5], "Yes")     # Access Internet
        self.assertEqual(matrix_lan_address[3][6], "Enable")  # DHCP Server Mode
        self.assertEqual(matrix_lan_address[3][7], lan_config_map["ETH_STARTING_IP"]) #starting IP
        self.assertEqual(matrix_lan_address[3][8], lan_config_map["ETH_ENDING_IP"])  #Ending IP
        
        self.assertEqual(matrix_lan_address[4][1], "USBNET")
        self.assertEqual(matrix_lan_address[4][3], lan_config_map["USB_DEVICE_IP"])
        self.assertEqual(matrix_lan_address[4][4], lan_config_map["USB_SUBNET_MASK"])
        self.assertEqual(matrix_lan_address[4][5], "Yes")     # Access Internet
        self.assertEqual(matrix_lan_address[4][6], "Enable")  # DHCP Server Mode        
        self.assertEqual(matrix_lan_address[4][7], netip)     #Starting IP
        self.assertEqual(matrix_lan_address[4][8], netip)     #Ending IP                 

        cmd = 'ipconfig > ipconfig_out.txt'
        ret=os.system(cmd)   
        basic_airlink.slog(str(ret))
        self.assertEqual(ret,0)
        self.assertNotEqual(os.path.getsize("ipconfig_out.txt"),0)
        self.assertTrue(netip in open('ipconfig_out.txt').read())                                                              

    def tc_ethernet_display_disable(self):
        '''See testcase - Ethernet display disabled
        '''
      
        # step: come to LAN page from AceManager, and set host connection mode         
        self.se_ins.lan_page(self.driver )
           
        self.se_ins.set_host_connection_mode(self.driver , "1")
        
        self.se_ins.apply_reboot(self.driver )
        self.se_ins.quit(self.driver )
        
        #step: come to LAN/Ethernet page, disable Ethernet port   
        self.se_ins.lan_ethernet_page(self.driver)
        self.se_ins.set_ethernet_port(self.driver, "Disable")
        
        self.se_ins.apply_reboot(self.driver)
        self.se_ins.quit(self.driver)
    
        # Step: wait till device ready
        basic_airlink.slog("step: wait till device ready" )  
        time.sleep(tbd_config_map[self.device_name ]["REBOOT_TIMEOUT"]) 

        # step: login to ACEmanager 
        basic_airlink.slog("step: login to ACEmanager")
        ace_manager_url = self.conn_ins.get_url()
        self.driver = self.se_ins.login(ace_manager_url, tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])
           
        # come to Status page 
        #self.se_ins.status_page(driver)
        
        # Step:  get net IP from Status/Home page
        netip = self.se_ins.get_net_ip(self.driver)

        # come to LAN page 
        self.se_ins.lan_page(self.driver)
        self.se_ins.lan_ethernet_page(self.driver)
        
        #step: check each item at LAN Ethernet page 
        basic_airlink.slog("step: check each item at LAN/Ethernet page")
                 
        
    def tc_dummy(self):
        pass                          