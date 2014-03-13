################################################################################
#
# This module automates LAN's DHCP/Addressing test cases. 
# Company: Sierra Wireless
# Date: Jul 5, 2013
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
import unittest
import selenium_utilities
import sys
import os

airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 

import basic_airlink
basic_airlink.append_sys_path()
import connectivity
import lan_airlink
import proxy_airlink

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
        self.fail_flag = 0
     
        self.connectivity_ins = connectivity.Connectivity(username="user", password="12345")       
        
        # step: check if devices ready    
        basic_airlink.cslog("step: check if testbed is ready")
        if not self.connectivity_ins.testbed_ready("LAN"):
            basic_airlink.cslog("testbed is not ready")
            sys.exit(0)
            
        self.device_name = tbd_config_map["DUTS"][0]
                  
        self.get_lan_instance()   
        #self.get_lan_instance(proxy_ip = tbd_config_map["MANAGEMENT_IP"]["HOST1"])   # remote by proxy 

#        basic_airlink.cslog("1111111 = "+str(self.lan_ins.error_flag))
        
        # step: login to Ace Manager 
        basic_airlink.cslog("step: login to ACEmanager")
        self.ace_manager_url = self.connectivity_ins.get_url()
        self.driver = self.lan_ins.login(self.ace_manager_url, tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])   

#        self.lan_ins.get_current_tab("LAN")        
#        basic_airlink.cslog("222222222 = "+str(self.lan_ins.error_flag))
#        sys.exit(0)
                
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
        basic_airlink.cslog("step: close Firefox/IE")  
        self.driver.quit()         
        self.assertEqual([], self.verificationErrors) 

        basic_airlink.slog(" Testcase complete")

    def get_lan_instance(self, proxy_ip = None):
        
        if proxy_ip is not None:
            self.proxy = proxy_airlink.ProxyAirlink(proxy_ip)
            self.proxy_conn = self.proxy.connect()
            
            self.local_lan_ins = lan_airlink.LanAirlink()
            
            self.lan_ins = self.proxy.deliver(self.local_lan_ins)
        else:
            self.lan_ins = lan_airlink.LanAirlink()
                                           
    def tc_all_hosts_use_private_ips_default(self):
        ''' Testcase - all hosts use private IPs default
        '''

        # step: come to LAN page from AceManager, and set host connection mode         
        self.lan_ins.lan_page(self.driver )
        self.lan_ins.set_host_connection_mode(self.driver , "1")

        basic_airlink.cslog("step: Apply and reboot" )  
        self.lan_ins.apply_reboot(self.driver )
        self.lan_ins.quit(self.driver )
        
        # Step: wait till device ready
        basic_airlink.cslog("step: wait till device ready" )  
        time.sleep(tbd_config_map[self.device_name ]["REBOOT_TIMEOUT"]) 
        sys.exit()

        # step: login to ACEmanager 
        basic_airlink.cslog("step: login to ACEmanager")
        #self.ace_manager_url = self.conn_ins.get_url()
        self.driver = self.lan_ins.login(self.ace_manager_url, tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])
        
        # Step:  get net IP from Status/Home page
        xcard_type =self.lan_ins.get_xcard_type(self.driver )
        xcard_state=self.lan_ins.get_xcard_state(self.driver )

        # come to LAN page 
        self.lan_ins.lan_page(self.driver )
        
        #step: check each item at LAN home page 
        basic_airlink.cslog("step: check each item at LAN DHCP/Addressing page")
        
        #step: check Host connect mode
        ret = self.lan_ins.get_host_connection_mode(self.driver )          
        basic_airlink.cslog("Host connect mode: " +ret)  
        self.assertEqual(ret, "1")               
 
        #step: check DHCP lease timer
        ret = self.lan_ins.get_dhcp_lease_timer(self.driver )       
        basic_airlink.cslog("DHCP lease timer: " +ret)  
        self.assertNotEqual(ret, "0")               
        
        #step: check DHCP domain               
        ret = self.lan_ins.get_dhcp_domain(self.driver )          
        basic_airlink.cslog("DHCP domain  : " +ret)  

        #step: check MTU             
        ret = self.lan_ins.get_dhcp_mtu_size(self.driver )  
        basic_airlink.cslog("MTU: " +ret)  
        self.assertEqual(ret, "1500")    

        bridge_wifi_to_ethernet_d2="Disabled"
        wifi_mode_d1="WIFI OFF"
                    
        if xcard_type == "WiFi X-Card" and xcard_state == "X-Card Connected":
            bridge_wifi_to_ethernet_d2=self.lan_ins.get_bridge_wifi_to_ethernet_d2(self.driver )
            wifi_mode_d1=self.lan_ins.get_wifi_mode_d1(self.driver )
                    
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
 
        cmd = 'ipconfig > ipconfig_private.txt'
        ret=os.system(cmd)   
        basic_airlink.slog(str(ret))
        self.assertEqual(ret,0)
        self.assertNotEqual(os.path.getsize("ipconfig_private.txt"),0)
        #self.assertTrue(lan_config_map["ETH_STARTING_IP"] in open('ipconfig_out.txt').read())                                                        
          
    def tc_ethernet_uses_public_ip(self):
        '''See testcase - Ethernet uses public IP.
        '''         
        # step: come to WAN page from AceManager, and set APN        
        self.lan_ins.wan_page(self.driver)
        self.lan_ins.set_apn(self.driver, tbd_config_map)
        self.lan_ins.apply(self.driver)
              
        # step: come to LAN page from AceManager, and set host connection mode         
        self.lan_ins.lan_page(self.driver)
        self.lan_ins.set_host_connection_mode(self.driver, "0")
        
        self.lan_ins.apply_reboot(self.driver)
        self.lan_ins.quit(self.driver)
    
        # Step: wait till device ready
        basic_airlink.slog("step: wait till device ready" )  
        time.sleep(tbd_config_map[self.device_name ]["REBOOT_TIMEOUT"]) 

        # step: login to ACEmanager 
        basic_airlink.slog("step: login to ACEmanager")
        ace_manager_url = tbd_config_map["ACE_URL"]["USB"]
        self.driver = self.lan_ins.login(ace_manager_url, tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])           
        
        #step: to get the net IP from Status/Home page
        netip = self.lan_ins.get_net_ip(self.driver)

        #step: come to LAN page 
        self.lan_ins.lan_page(self.driver)
        
        #step: check each item at LAN home page 
        basic_airlink.slog("step: check each item at LAN DHCP/Addressing page")
        
        #step: check Host connect mode 
        ret = self.lan_ins.get_host_connection_mode(self.driver)         
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
        self.lan_ins.wan_page(self.driver)
        self.lan_ins.set_apn(self.driver, tbd_config_map)
        self.lan_ins.apply(self.driver)
               
        # step: come to LAN page from AceManager, and set host connection mode         
        self.lan_ins.lan_page(self.driver )
           
        self.lan_ins.set_host_connection_mode(self.driver , "2")
        
        self.lan_ins.apply_reboot(self.driver )
        self.lan_ins.quit(self.driver )
    
        # Step: wait till device ready
        basic_airlink.slog("step: wait till device ready" )  
        time.sleep(tbd_config_map[self.device_name ]["REBOOT_TIMEOUT"]) 

        # step: login to ACEmanager 
        basic_airlink.slog("step: login to ACEmanager")
        
        ace_manager_url = tbd_config_map["ACE_URL"]["ETH"]
        self.driver = self.lan_ins.login(ace_manager_url, tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])
           
        # come to Status page 
        #self.lan_ins.status_page(driver)
        
        # Step:  get net IP from Status/Home page
        netip = self.lan_ins.get_net_ip(self.driver)

        # come to LAN page 
        self.lan_ins.lan_page(self.driver)
        
        #step: check each item at LAN home page 
        basic_airlink.slog("step: check each item at LAN DHCP/Addressing page")
        
        #step: check Host connect mode
        ret = self.lan_ins.get_host_connection_mode(self.driver)          
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
        '''Ethernet display disabled, please use USB and Ethernet cable between controller and DUT
        '''
        # step: come to LAN page from AceManager, and set host connection mode to 1     
        self.lan_ins.lan_page(self.driver )
           
        self.lan_ins.set_host_connection_mode(self.driver , "1")
        
        self.lan_ins.apply(self.driver )
        #self.lan_ins.quit(self.driver )
        
        #step: come to LAN/Ethernet page, disable Ethernet port   
        self.lan_ins.lan_ethernet_page(self.driver)
        self.lan_ins.set_ethernet_port(self.driver, "Disable")
        
        self.lan_ins.apply_reboot(self.driver)
        self.lan_ins.quit(self.driver)
    
        # Step: wait till device ready
        basic_airlink.slog("step: wait till device ready" )  
        time.sleep(tbd_config_map[self.device_name ]["REBOOT_TIMEOUT"]) 

        # step: login to ACEmanager 
        basic_airlink.slog("step: login to ACEmanager")
        ace_manager_url = self.conn_ins.get_url()
        self.driver = self.lan_ins.login(ace_manager_url, tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])
           
        # come to Status page 
        #self.lan_ins.status_page(driver)

        # come to LAN page 
        self.lan_ins.lan_page(self.driver)
        #self.lan_ins.lan_ethernet_page(self.driver)
        
        #step: check each item at LAN Ethernet page 
        basic_airlink.slog("step: check each item at LAN's DHCP/Addressing page")
        
        #step: check Host connect mode
        ret = self.lan_ins.get_host_connection_mode(self.driver)          
        basic_airlink.slog("Host connect mode: " + str(ret))  
        self.assertEqual(ret, "1")            
        
        # Creates a list containing 9 lists initialized to 0
        matrix_lan_address = [["" for j in range(9)] for i in range(7)] 
        
        #step: check Ethernet IP, USBNET IP 
        for i in range(3,5): 
            for j in range(1,9):             
                mylist = self.driver.find_elements_by_xpath("//*[@id='9060002']/tr["+str(i)+"]/td["+str(j)+"]")   
                for  k in mylist: 
                    matrix_lan_address[i][j]=k.text    
                basic_airlink.slog(str(i)+" " +str(j)+" "+matrix_lan_address[i][j])    
        
        self.assertNotEqual(matrix_lan_address[3][1], "Ethernet")
        self.assertNotEqual(matrix_lan_address[3][3], lan_config_map["ETH_DEVICE_IP"])
        self.assertNotEqual(matrix_lan_address[3][4], lan_config_map["ETH_SUBNET_MASK"])
        self.assertNotEqual(matrix_lan_address[3][5], "Yes")     # Access Internet
        self.assertNotEqual(matrix_lan_address[3][6], "Enable")  # DHCP Server Mode
        self.assertNotEqual(matrix_lan_address[3][7], lan_config_map["ETH_STARTING_IP"]) 
        self.assertNotEqual(matrix_lan_address[3][8], lan_config_map["ETH_ENDING_IP"])                

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
        self.assertTrue(lan_config_map["USB_STARTING_IP"] in open('ipconfig_out.txt').read())                    


    def tc_usb_display(self):
        '''USB display disabled, please use USB and Ethernet cable between controller and DUT
        '''
        # step: come to LAN page from AceManager, and set host connection mode to 1     
        self.lan_ins.lan_page(self.driver )
           
        self.lan_ins.set_host_connection_mode(self.driver , "1")
        
        self.lan_ins.apply(self.driver )
        #self.lan_ins.quit(self.driver )
        
        #step: come to LAN/USB page, set USB device mode to USBNET   
        self.lan_ins.lan_usb_page(self.driver)
        self.lan_ins.set_usb_device_mode(self.driver, "USBNet")
        
        self.lan_ins.apply_reboot(self.driver)
        self.lan_ins.quit(self.driver)
    
        # Step: wait till device ready
        basic_airlink.slog("step: wait till device ready" )  
        time.sleep(tbd_config_map[self.device_name ]["REBOOT_TIMEOUT"]) 

        # step: login to ACEmanager 
        basic_airlink.slog("step: login to ACEmanager")
        ace_manager_url = tbd_config_map[self.device_name]["ACE_URL"]
        self.driver = self.lan_ins.login(ace_manager_url, tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])
           
        # come to Status page 
        #self.lan_ins.status_page(driver)

        # come to LAN page 
        self.lan_ins.lan_page(self.driver)
        
        #step: check each item at LAN Ethernet page 
        basic_airlink.slog("step: check each item at LAN's DHCP/Addressing page")
        
        #step: check Host connect mode
        ret = self.lan_ins.get_host_connection_mode(self.driver)          
        basic_airlink.slog("Host connect mode: " + str(ret))  
        self.assertEqual(ret, "1")            
        
        # Creates a list containing 9 lists initialized to 0
        matrix_lan_address = [["" for j in range(9)] for i in range(7)] 
        
        #step: check Ethernet IP, USBNET IP 
        for i in range(3,5): 
            for j in range(1,9):             
                mylist = self.driver.find_elements_by_xpath("//*[@id='9060002']/tr["+str(i)+"]/td["+str(j)+"]")   
                for  k in mylist: 
                    matrix_lan_address[i][j]=k.text    
                basic_airlink.slog(str(i)+" " +str(j)+" "+matrix_lan_address[i][j])                    

        self.assertEqual(matrix_lan_address[4][1], "USBNET")
        self.assertEqual(matrix_lan_address[4][3], lan_config_map["USB_DEVICE_IP"])
        self.assertEqual(matrix_lan_address[4][4], lan_config_map["USB_SUBNET_MASK"])
        self.assertEqual(matrix_lan_address[4][5], "Yes")     # Access Internet
        self.assertEqual(matrix_lan_address[4][6], "Enable")  # DHCP Server Mode        
        self.assertEqual(matrix_lan_address[4][7], lan_config_map["USB_STARTING_IP"]) #starting IP
        self.assertEqual(matrix_lan_address[4][8], lan_config_map["USB_ENDING_IP"]) #Ending IP
        
        #step: come to LAN/USB page, set USB device mode to USBNET   
        self.lan_ins.lan_usb_page(self.driver)
        self.lan_ins.set_usb_device_mode(self.driver, "USB Serial")
        
        self.lan_ins.apply(self.driver)
           
        # come to Status page 
        #self.lan_ins.status_page(driver)

        # come to LAN page 
        self.lan_ins.lan_page(self.driver)
        self.lan_ins.refresh(self.driver)
        
        #step: check each item at LAN Ethernet page 
        basic_airlink.slog("step: check each item at LAN's DHCP/Addressing page")
        
        #step: check Host connect mode
        ret = self.lan_ins.get_host_connection_mode(self.driver)          
        basic_airlink.slog("Host connect mode: " + str(ret))  
        self.assertEqual(ret, "1")            
        
        # Creates a list containing 9 lists initialized to 0
        matrix_lan_address = [["" for j in range(9)] for i in range(7)] 
        
        #step: check Ethernet IP, USBNET IP 
        for i in range(3,5): 
            for j in range(1,9):             
                mylist = self.driver.find_elements_by_xpath("//*[@id='9060002']/tr["+str(i)+"]/td["+str(j)+"]")   
                for  k in mylist: 
                    matrix_lan_address[i][j]=k.text    
                basic_airlink.cslog(str(i)+" " +str(j)+" "+matrix_lan_address[i][j])                    

        self.assertEqual(matrix_lan_address[4][1], "")
        self.assertEqual(matrix_lan_address[4][3], "")
        self.assertEqual(matrix_lan_address[4][4], "")
        self.assertEqual(matrix_lan_address[4][5], "")     # Access Internet
        self.assertEqual(matrix_lan_address[4][6], "")  # DHCP Server Mode        
        self.assertEqual(matrix_lan_address[4][7], "") #starting IP
        self.assertEqual(matrix_lan_address[4][8], "") #Ending IP
 
    def tc_wifi_display(self):
        pass

    def tc_ip_mac_display(self):

       
        # Creates a list containing lists initialized to ""
        ip_mac_table = [["" for j in range(4)] for i in range(5)] 
        
        self.lan_ins.navigate_subtab(self.driver, "Status","LAN")
        basic_airlink.cslog(self.lan_ins.get_vrrp_mode(self.driver))
        
        ip_mac_table = self.lan_ins.get_ip_mac_table(self.driver)
        self.assertEqual(ip_mac_table[3][2], "192.168.13.101")
        self.assertEqual(ip_mac_table[3][3], "a0:b3:cc:c7:dc:8f")
        self.assertEqual(ip_mac_table[4][2], "192.168.13.100")
        self.assertEqual(ip_mac_table[4][3], "5c:26:0a:75:37:0d")    


    def tc_vlan_display(self):

        # Creates a list containing lists initialized to ""
        matrix_lan_address = [["" for j in range(3)] for i in range(6)] 
        
        self.lan_ins.navigate_subtab(self.driver, "Status","LAN")
        matrix_lan_address = self.lan_ins.get_vlan_table(self.driver)
        
        self.assertEqual(matrix_lan_address[3][1], "3")
        self.assertEqual(matrix_lan_address[3][2], "0")
        self.assertEqual(matrix_lan_address[4][1], "4")
        self.assertEqual(matrix_lan_address[4][2], "0")    
        self.assertEqual(matrix_lan_address[5][1], "5")         
        self.assertEqual(matrix_lan_address[5][2], "0")  
                       
    def tc_dummy(self):
        basic_airlink.cslog(self.lan_ins.error_flag)
        self.lan_ins.error_flag +=1          
        basic_airlink.cslog(self.lan_ins.error_flag)
                