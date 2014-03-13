################################################################################
#
# This module provides LAN UI operation using Selenium lib, handle three subtab
#pages: Status/LAN, WAN/WAN, WAN/RSR.
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
#ele_config_map = basic_airlink.get_element_config_data()


class LanAirlink(selenium_utilities.SeleniumAcemanager):
    ''' This class implements Selenium UI operation methods by ACEmanager Web, 
    if methods don't include tab/subtab parameters, that needs to 
    call navigate_subtab() first to navigate the specified page.
    
    ''' 
    
    def __init__(self):
        ''' TODO
        '''
 
        selenium_utilities.SeleniumAcemanager.__init__(self)
   
##########LAN tab page #########################################################
    def get_config(self):
        pass    
    
    def set_config(self):
        pass 

    def verify_config(self):
        pass 
        
    def set_eth_port(self, driver, ethernet_port_val):
        ''' Enable/Disable Ethernet port from ACEmanager LAN/Ethernet page
        e.g. set_eth_port(self, driver, "Enable")
        Args:
            driver: FF/IE web driver 
        Returns:
            True/False
        
        '''
        basic_airlink.slog("step: Enable/Disable Ethernet port from ACEmanager LAN/Ethernet page ")
        if ethernet_port_val in ["Disable","Enable"]:
            Select(driver.find_element_by_name(msciids.MSCIID_CFG_CMN_ETH_DEVICE)).select_by_visible_text(ethernet_port_val)   
        else:
            basic_airlink.slog("Wrong parameter")
              
        time.sleep(2)

 
    def set_ethernet_device_ip(self, driver, device_ip):
        ''' Set device IP from ACEmanager LAN/Ethernet page
        
        Args:
            driver: FF/IE web driver 
        
        '''
        basic_airlink.slog("step: set device IP from ACEmanager LAN/Ethernet page ")
        driver.find_element_by_name("1084").clear()
        driver.find_element_by_name("1084").send_keys(device_ip)   
              
        time.sleep(2)
                                                     
    def set_ethernet_starting_ip(self, driver, staring_ip):
        ''' Set starting IP from ACEmanager LAN/Ethernet page
        
        Args:
            driver: FF/IE web driver 
        
        '''
        basic_airlink.slog("step: set starting IP from ACEmanager LAN/Ethernet page ")  
        driver.find_element_by_name("1137").clear()
        driver.find_element_by_name("1137").send_keys(staring_ip)
                  
        time.sleep(2)


    def set_ethernet_ending_ip(self, driver, ending_ip):
        ''' Set ending IP from ACEmanager LAN/Ethernet page
        
        Args:
            driver: FF/IE web driver 
        
        '''
        basic_airlink.slog("step: set ending IP from ACEmanager LAN/Ethernet page ")  
        
        driver.find_element_by_name("1138").clear()
        driver.find_element_by_name("1138").send_keys(ending_ip)
        time.sleep(2)


    def set_ethernet_dhcp_network_mask(self, driver, dhcp_network_mask):
        ''' Set DHCP network mask from ACEmanager LAN/Ethernet page
        
        Args:
            driver: FF/IE web driver 
        
        '''
        basic_airlink.slog("step: set DHCP network mask from ACEmanager LAN/Ethernet page ")  
        
        driver.find_element_by_name("1135").clear()
        driver.find_element_by_name("1135").send_keys(dhcp_network_mask)
        time.sleep(2)


    def set_ethernet_dhcp_server_mode(self, driver, dhcp_server_mode):
        ''' Set DHCP server mode from ACEmanager LAN/Ethernet page
        
        Args:
            driver: FF/IE web driver 
        
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
            driver: FF/IE web driver 
        
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
            driver: FF/IE web driver 
            radio link_relay: Radio LInk Delay (unit: sec)
        
        '''
        basic_airlink.slog("step: set radio link_relay from ACEmanager LAN/Ethernet page ")  
        
        driver.find_element_by_name("2724").clear()
        driver.find_element_by_name("2724").send_keys(radio_link_relay)
        time.sleep(2)
 
 
    def set_ethernet_interface_disabled_duration(self, driver, interface_disabled_duration):
        ''' Set interface disabled duration from ACEmanager LAN/Ethernet page
        
        Args:
            driver: FF/IE web driver 
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
            driver: FF/IE web driver 
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
            driver      : FF/IE web driver 
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
             

    def set_host_connection_mode(self, driver, host_connection_mode): 
        ''' set host connection mode by ACEmanager LAN/DHCP page
        Args: 
        
            diver : FF/IE web driver
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
            diver : FF/IE web driver
        Returns: 
            Host conenction mode 
        '''

        msciid_str = str(msciids.MSCIID_CFG_CMN_HOST_IP_MODE)
        ret = self.get_element_by_name(driver,msciid_str)     
        return ret     
    

    def get_dhcp_lease_timer(self, driver): 
        ''' get DHCP lease timer
        Args: 
            diver : FF/IE web driver
        Returns: 
             DHCP lease timer 
        '''

        msciid_str = str(msciids.DHCP_LEASE_TIME)
        ret = self.get_element_by_name(driver,msciid_str)     
        return ret  


    def get_dhcp_domain(self, driver): 
        ''' get DHCP domain
        Args: 
            diver : FF/IE web driver
        Returns: 
             DHCP domain
        '''

        msciid_str = str(msciids.MSCIID_CFG_DHCP_DOMAIN)
        ret = self.get_element_by_name(driver,msciid_str)     
        return ret 


    def get_dhcp_mtu_size(self, driver): 
        ''' get DHCP MTU size
        Args: 
            diver : FF/IE web driver
        Returns: 
             DHCP MTU size
        '''

        msciid_str = str(msciids.MSCIID_CFG_DHCP_MTU_SIZE)
        ret = self.get_element_by_name(driver,msciid_str)     
        return ret 
            
    def get_bridge_wifi_to_ethernet_d2(self, driver): 
        ''' get Bridge Wifi to Ethernet in LAN/DHCP_ADDRESSING page
        Args: 
            diver : FF/IE web driver
        Returns: 
             Enable/Disable
        '''

        msciid_str = str(msciids.MSCIID_CFG_WIFI_BRIDGE_EN)
        ret = self.get_element_by_name(driver,msciid_str+"-d2")     
        return ret
 
    def get_wifi_mode_d1(self, driver): 
        ''' get wifi mode in LAN/DHCP_ADDRESSING page
        Args: 
            diver : FF/IE web driver
        Returns: 
             Enable/Disable
        '''

        msciid_str = str(msciids.MSCIID_WIFI_MODE)
        ret = self.get_element_by_name(driver,msciid_str+"-d1")     
        return ret     

    def get_wifi_mode(self, driver): 
        ''' get wifi mode in LAN/WIFI page
        Args: 
            diver : FF/IE web driver
        Returns: 
             Enable/Disable
        '''

        msciid_str = str(msciids.MSCIID_WIFI_MODE)
        ret = self.get_element_by_name(driver,msciid_str)     
        return ret  

    def get_usb_device_mode(self, driver): 
        ''' get USB device mode in LAN/USB page
        Args: 
            diver : FF/IE web driver
        Returns: 
             0/1/2 (USB serial/USBNET/Disabled)
        '''

        msciid_str = str(msciids.MSCIID_CFG_CMN_USB_DEVICE)
        ret = self.get_element_by_name(driver,msciid_str)     
        return ret                        

    def set_usb_device_mode(self, driver, mode): 
        ''' get USB device mode in LAN/USB page
        Args: 
            diver : FF/IE web driver
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
            basic_airlink.cslog("-- Connecting to remote AP")
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
                    available_ap = self.get_element_by_id(driver, str(msciids.MSCIID_WIFI_AVAILABLE_AP))
                    connect_status = self.get_element_by_id(driver, str(msciids.MSCIID_WIFI_REMOTE_AP_CONNECT_STATE))
                    logging.debug(available_ap + " ... " + connect_status)
                    wait -= 1
                else: return False
                
            basic_airlink.cslog("-- Successfully " + connect_status + " to remote AP: " + available_ap + " using WiFi")   
            return True
        
        except WebDriverException:
            logging.debug("Unable to establish the Connection")  
            return False
        
##########Status/LAN subtab page ###############################################

    def get_eth_status(self, driver, eth_port=1):
        ''' get speed and duplex status of the connection on Ethernet port 1/2/3 
        by ACEmanager Web UI Status/LAN page
        Args: 
            driver FF/IE web driver 
            eth_port: 1 Ethernet port on device, 
                      2/3 Ethernet port on the dual-ethernet card

        Returns: 
            speed and duplex status of the connection on Ethernet port 1/2/3
        '''

        if eth_port == 1: 
            msciid_str = str(msciids.MSCIID_STS_ETH_NET )
        elif eth_port == 2: 
            msciid_str = str(msciids.MSCIID_STS_ETH_NET2 )
        elif eth_port == 3: 
            msciid_str = str(msciids.MSCIID_STS_ETH_NET3)
                        
        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret  

    def get_eth_port(self, driver, eth_port=1):
        ''' get speed and duplex status of the connection on Ethernet port 1/2
        by ACEmanager Web UI Status/LAN page
        Args: 
            driver FF/IE web driver 
            eth_port: 1 Ethernet port on device, 
                      2 Ethernet port on the dual-ethernet card

        Returns: 
            speed and duplex status of the connection on Ethernet port 1/2
        '''

        if eth_port == 1: 
            msciid_str = str(msciids.STS_ETHERNET_PORT_1 )
        elif eth_port == 2: 
            msciid_str = str(msciids.STS_ETHERNET_PORT_1 )
                        
        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret
    
    def get_usb_mode(self, driver):
        ''' get USB port mode by ACEmanager Web UI Status/LAN page
        Args: 
            driver FF/IE web driver 
        Returns: 
            USB mode (USBnet/USBserial)
        '''

        msciid_str = str(msciids.MSCIID_CFG_CMN_USB_DEVICE ) + '-d1'
            
        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret  
    
    def get_connected_clients(self, driver):
        ''' get #of connected clients by ACEmanager Web UI Status/LAN page
        Args: 
            driver FF/IE web driver 
        Returns: 
            number of connected clients
        '''

        msciid_str = str(msciids.STS_CONNECTED_CLIENTS)
            
        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret 

    def get_lan_packets_sent(self, driver):
        ''' get number of IP packets sent to the host interface since the system 
        startup by ACEmanager Web UI Status/LAN page
        Args: 
            driver FF/IE web driver 
        Returns: 
            Number of IP packets sent to the host interface since the system 
           startup
        '''

        msciid_str = str(msciids.MSCIID_STS_HOST_IP_SENT )
            
        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret
    
    def get_lan_packets_received(self, driver):
        ''' get number of IP packets received to the host interface since the 
        system startup by ACEmanager Web UI Status/LAN page
        Args: 
            driver FF/IE web driver 
        Returns: 
            Number of IP packets received to the host interface since the system 
           startup
        '''

        msciid_str = str(msciids.MSCIID_STS_HOST_IP_RECV )
            
        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret  
    
    def get_ip_mac_table(self, driver):
        ''' get the local IP Address and the MAC Address of connected hosts by 
        ACEmanager Web UI Status/LAN page. 
        TODO: to debug 
        Args: 
            driver - FF/IE web driver 
        Returns: 
            the local IP Address and the MAC Address of connected hosts
        '''

        # Creates a list containing lists initialized to 0
        ip_mac_table = [["" for j in range(4)] for i in range(6)]  
        
        #step: check IP, MAC
        for i in range(3,6): 
            for j in range(2,4):           #column  2, 3
                mylist = self.driver.find_elements_by_xpath("//*[@id='110621']/tr["+str(i)+"]/td["+str(j)+"]")   
                for  k in mylist: 
                    ip_mac_table[i][j]=k.text    
                ip_mac_table.slog(str(i)+" " +str(j)+" "+ip_mac_table[i][j]) 
                
        
        return ip_mac_table  

    def get_vrrp_mode(self, driver):
        ''' get indicator of the configuration of the VRRP feature by ACEmanager 
        Web UI Status/LAN page
        Args: 
            driver FF/IE web driver 
        Returns: 
            indicator of the configuration of the VRRP feature(enabled/disabled)
        '''

        msciid_str = str(msciids.MSCIID_VRRP_ENABLED )+'-d1'
            
        ret=self.get_element_by_id(driver, msciid_str)
        
        return ret 

    def get_vlan_table(self, driver):
        ''' get the the identities (Interface name and ID) of the configured 
        VLANs by ACEmanager Web UI Status/LAN page
        TODO: to verify code
        Args: 
            driver FF/IE web driver 
        Returns: 
            list as VLAN table
        '''
        # Creates a list containing 5 lists initialized to 0
        vlan_table = [["" for j in range(9)] for i in range(6)]  
        
        #step: check Ethernet IP, USBNET IP 
        for i in range(3,6): 
            for j in range(1,3):        #colume 1, 2     
                mylist = self.driver.find_elements_by_xpath("//*[@id='110601']/tr["+str(i)+"]/td["+str(j)+"]")   
                for  k in mylist: 
                    vlan_table[i][j]=k.text    
                vlan_table.slog(str(i)+" " +str(j)+" "+vlan_table[i][j]) 
        
        return vlan_table 
        
    def set_vrrp_mode(self, driver, enable):
        try:
            Select(driver.find_element_by_name("9001")).select_by_visible_text(enable)   
            return True
        except WebDriverException:
            logging.debug("Unable to enable VRRP")
            return False

    def verify_vrrp_mode_enabled(self, driver, enable):
        try:
            text = Select(driver.find_element_by_name("9001")).first_selected_option.text
            return text == (enable)
        except WebDriverException:
            logging.debug("Unable to enable VRRP")
            return False
        
    def set_vrrp_ethernet_group_id(self, driver, group_id):
        try: 
            driver.find_element_by_xpath('//*[@id="9010"]/tbody/tr[3]/td[3]/input').clear()
            driver.find_element_by_xpath('//*[@id="9010"]/tbody/tr[3]/td[3]/input').send_keys(group_id)
            time.sleep(1)
            return True
        except WebDriverException:
            logging.debug("Unable to set VRRP Group ID for Ethernet")  
            return False

    def verify_vrrp_ethernet_group_id(self, driver, group_id):
        try: 
            text = driver.find_element_by_xpath('//*[@id="9010"]/tbody/tr[3]/td[3]').get_attribute("title")
            return text == group_id
        except WebDriverException as e:
            logging.debug("Unable to set VRRP Group ID for Ethernet")  
            return False

    def set_vrrp_ethernet_priority(self, driver, priority):
        try: 
            driver.find_element_by_xpath('//*[@id="9010"]/tbody/tr[3]/td[4]/input').clear()
            driver.find_element_by_xpath('//*[@id="9010"]/tbody/tr[3]/td[4]/input').send_keys(priority)
            time.sleep(1)
            return True
        except WebDriverException:
            logging.debug("Unable to set VRRP Priority for Ethernet")  
            return False

    def verify_vrrp_ethernet_priority(self, driver, priority):
        try: 
            text = driver.find_element_by_xpath('//*[@id="9010"]/tbody/tr[3]/td[4]').get_attribute("title")
            return text == priority 
        except WebDriverException:
            logging.debug("Unable to set VRRP Priority for Ethernet")  
            return False

    def set_vrrp_ethernet_virtual_ip(self, driver, virtual_ip):
        try: 
            driver.find_element_by_xpath('//*[@id="9010"]/tbody/tr[3]/td[5]/input').clear()
            driver.find_element_by_xpath('//*[@id="9010"]/tbody/tr[3]/td[5]/input').send_keys(virtual_ip)
            time.sleep(1)
            return True
        except WebDriverException:
            logging.debug("Unable to set VRRP Virtual IP for Ethernet")  
            return False

    def verify_vrrp_ethernet_virtual_ip(self, driver, virtual_ip):
        try: 
            text = driver.find_element_by_xpath('//*[@id="9010"]/tbody/tr[3]/td[5]').get_attribute("title")
            return text == virtual_ip
        except WebDriverException:
            logging.debug("Unable to set VRRP Virtual IP for Ethernet")  
            return False

    def set_vrrp_ethernet_interval(self, driver, interval):
        try: 
            driver.find_element_by_xpath('//*[@id="9010"]/tbody/tr[3]/td[7]/input').clear()
            driver.find_element_by_xpath('//*[@id="9010"]/tbody/tr[3]/td[7]/input').send_keys(interval)
            time.sleep(1)
            return True
        except WebDriverException:
            logging.debug("Unable to set VRRP interval for Ethernet")  
            return False

    def verify_vrrp_ethernet_interval(self, driver, interval):
        try: 
            text = driver.find_element_by_xpath('//*[@id="9010"]/tbody/tr[3]/td[7]').get_attribute("title")
            return text == interval
        except WebDriverException:
            logging.debug("Unable to set VRRP interval for Ethernet")  
            return False
