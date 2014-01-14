#################################################################################
#
# This module automates status test suite. 
# Company: Sierra Wireless
# Time: Mar 2nd, 2013
# 
#################################################################################

import logging
import os
import re
import sys
import time
import unittest

import htmlreport
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
import msciids
import selenium_utilities


class TestsuiteStatusUi(unittest.TestCase):
    ''' This test suite automates Status test cases by ACEmanager Web UI
    
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
            
        # step: check Firefox 
        basic_airlink.slog("Please close Firefox if required \n")
        
        self.se_ins = selenium_utilities.SeleniumAcemanager()
        
        self.fail_flag = 0
        
        # step: login to Ace Manager 
        basic_airlink.slog("step: login to Ace Manager")

        self.driver = self.se_ins.login(tbd_config_map[self.device_name]["ACE_URL"], tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])

        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])       
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
 

    def tc_status_home_general_ui(self):
        '''
        to test status/home page by Selenium/ACEmanager UI,
        the test case focus on the general items, not LTE related 
        
        '''    
        driver = self.driver     

        if "VZW" not in self.device_name: 
            self.se_ins.wan_user_entry_apn_ui(driver, tbd_config_map)
        
        fail_flag = self.fail_flag              
        
        # step: come to Status page from AceManager          
        self.se_ins.status_page(driver)              
        
        #step: check each item at Status home page 
        basic_airlink.slog("step: check each item at Status home page")

        #step: check phone number 
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_INF_PHONE_NUM))          
        basic_airlink.slog("Phone number correct: " +ret)  
 
        #step: check the current WAN IP address
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_NETWORK_IP))       
        self.assertNotEqual(ret, "0.0.0.0")               
        
        #step: check network state                 
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_NETWORK_STATE))          
        self.assertEqual(ret, "Network Ready")               

        network_service_type_cfg = tbd_config_map[self.device_name]["NET_SERVICE_TYPE"]
        
        # step: check RSSI
        ret = int(self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_NETWORK_RSSI)))
        min_rssi = int(status_config_map["RSSI_RANGE"][0])
        max_rssi = int(status_config_map["RSSI_RANGE"][1])
        if  ret < min_rssi or ret > max_rssi:
                fail_flag += 1  
                basic_airlink.slog("\n Network RSSI not correct range! ")
        else: 
            
                basic_airlink.slog("\n Network RSSI in correct range! ")

        # step: check Cell Info (TCH, RSSI, LAC, Cell ID)
        if network_service_type_cfg in tbd_config_map["CELL_NET"]["LTE"]:
            basic_airlink.slog("\n Cell Info not suitable for LTE! ")
            
        elif network_service_type_cfg in tbd_config_map["CELL_NET"]["GSM"]:
            ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_GPRS_CELL_INFO))
            aaa = ret.split(' ')                        # each item becomes unicode string
            print aaa
            if int(aaa[2]) == 0: 
                fail_flag += 1  
                basic_airlink.slog("\n TCH not correct! ") 
            
            if int(aaa[4]) == 0: 
                fail_flag += 1  
                basic_airlink.slog("\n RSSI not correct! ")                

            if int(aaa[6]) == 0: 
                fail_flag += 1  
                basic_airlink.slog("\n LAC not correct! ") 
            
            if int(aaa[8]) == 0: 
                fail_flag += 1  
                basic_airlink.slog("\n CellID not correct! ") 
                                        
        elif network_service_type_cfg in tbd_config_map["CELL_NET"]["CDMA"]:
            basic_airlink.slog("\n Cell Info not suitable for CDMA! ")

            
        # step: check Network service type    
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_NETWORK_SERVICE))
        aaa = ret.split(',',1)       
        if aaa[0] not in tbd_config_map["NET_SERVICE_TYPES"]: 
            fail_flag += 1 
            basic_airlink.slog(aaa[0]+" not in: " +' '.join(tbd_config_map["NET_SERVICE_TYPES"]))
                  
    
        # step: check ALEOS FW           
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_INF_ALEOS_SW_VER)+"-d1")
        if ret != tbd_config_map[self.device_name]["ALEOS_FW_VER"]: 
            fail_flag += 1 
            basic_airlink.slog(" ALEOS FW version not correct! ")   
                 
        #step: check ECIO
        if   network_service_type_cfg == "EVDO": 
            ret = int(self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_CDMA_1XECIO)))
            if not int(status_config_map["ECIO_RANGE"][0])< ret < int(status_config_map["ECIO_RANGE"][1]):
                fail_flag += 1  
                basic_airlink.slog("\n CDMA_1XECIO not correct! ")
                   
        elif network_service_type_cfg == "UMTS":
            ret = int(self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_GPRS_ECIO)))
            if not int(status_config_map["ECIO_RANGE"][0])< ret < int(status_config_map["ECIO_RANGE"][1]):
                fail_flag += 1  
                basic_airlink.slog("\n GPRS ECIO not correct! ")    
                             
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_NETWORK_CHANNEL))   
        basic_airlink.slog("Network channel: " +ret)  
                        
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_MODEM_SENT)+"-d1")
        basic_airlink.slog("Bytes Sent: " +ret)  
          
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_MODEM_RECV)+"-d1")
        basic_airlink.slog("Bytes Received: " +ret)  

        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_CFG_CMN_MDM_NAME)+"-d1")  #Customer Device Name
        if ret != tbd_config_map[self.device_name]["MODEM_NAME"]: 
            fail_flag += 1 
            basic_airlink.slog(" Customer Device name not correct! ") 
        basic_airlink.slog("Modem name: " +ret)  
                        
        # step: check X-Card
        if tbd_config_map[self.device_name]["MODEL"] == "GX400" or tbd_config_map[self.device_name]["MODEL"] == "GX440" :
            
            x_card_type = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_X_CARD_TYPE))      
            
            if status_config_map["XCARD_ETH"] == "NO":
                self.assertEqual(x_card_type, "X-Card Not Found")
                
            else: 
                x_card_status = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_X_CARD_STATE))
                self.assertEqual(x_card_status, "x-Card Connected")               
                
        self.assertEqual(fail_flag, 0)             
          

    def tc_status_home_specific_ui(self):
        '''
        to test status/home page by Selenium/ACEmanager UI,  see the test case in ApTest or Testlink
        the test case focus on the specific items (LTE), not general items 
        
        '''
        
        driver = self.driver     
        fail_flag = self.fail_flag                             

        #step: check each item at Status home page 
        basic_airlink.slog("step: check each item at Status home page")
                      
        # step: check Radio FW version
        radio_module_type_cfg    = tbd_config_map[self.device_name]["RM_TYPE"]
        network_service_type_cfg = tbd_config_map[self.device_name]["NET_SERVICE_TYPE"]
        
        if  radio_module_type_cfg == "MC7750" or  radio_module_type_cfg == "MC5728" :           
            ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_INF_MODEM_SW_VER)+"-d1")
            print str(msciids.MSCIID_INF_MODEM_SW_VER),ret + "\n"
            if ret != tbd_config_map[self.device_name]["RADIO_FW_VER"]: 
                fail_flag += 1             
                basic_airlink.slog("\n Radio Module FW version not correct! ")

                 
        # Step: check LTE RSRP and RSRQ
        if  network_service_type_cfg == "LTE":            
            ret = int(self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_LTE_RSRP)))
            if not int(status_config_map["RSRP_RANGE"][0])< ret < int(status_config_map["RSRP_RANGE"][1]):
                fail_flag += 1  
                basic_airlink.slog("\n RSRP not correct! ")  
            else: 
                basic_airlink.slog("\n RSRP correct! ")  
         
            # step: check LTE RSRQ   
            ret = int(self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_LTE_RSRQ)))  
            if not int(status_config_map["RSRQ_RANGE"][0])< ret < int(status_config_map["RSRQ_RANGE"][1]):
                fail_flag += 1  
                basic_airlink.slog("\n RSRQ not correct! ")   
            else: 
                basic_airlink.slog("\n RSRQ correct! ")     
                
        self.assertEqual(fail_flag, 0)             
                     
        
    def tc_status_wan_ui(self):
        '''
        to test status/wan page by Selenium/ACEmanager UI
        
        '''
        
        driver = self.driver     
        fail_flag = self.fail_flag                       
        
        # step: come to Status/WAN page from AceManager 
        basic_airlink.slog("step: come to Status/WAN page from ACEManager")
         
        #self.se_ins.status_page(driver)              
        self.se_ins.status_wan_page(driver)  
        
        #step: check each item at Status home page 
        basic_airlink.slog("step: check each item at Status home page")                   
        
        # step: check WAN IP
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_NETWORK_IP)+"-d2")
        basic_airlink.slog(str(msciids.MSCIID_STS_NETWORK_IP)+" => " +ret)
            
        # step: check ESN/EID/IMEI for AT&T
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_INF_MODEM_ID))
        basic_airlink.slog("ESN/EID/IMEI: " + ret)
   
        # step: check SIM ID for AT&T 3G
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_GPRS_SIMID))
        basic_airlink.slog("SIM ID: " + ret)

        # step: check APN for AT&T 3G
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_CMN_APN_CURRENT))
        basic_airlink.slog("APN: " + ret)

        # step: check IMSI for AT&T 3G
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_GPRS_IMSI))
        basic_airlink.slog("IMSI: " + ret)

        # step: check GPRS Cell ID for AT&T 3G
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_GPRS_CELL_ID))
        basic_airlink.slog("GPSR CEll ID: " + ret)

        # step: check GPRS LAC for AT&T 3G
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_GPRS_LAC))
        basic_airlink.slog("GPRS LAC: " + ret)

        # step: check GPRS BSIC for AT&T 3G
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_STS_GPRS_BSIC ))
        basic_airlink.slog("GPRS BSIC: " + ret)

        # step: check Keepalive IP Address for AT&T 3G
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_CFG_CMN_IPPING_ADDR )+'-d1')
        basic_airlink.slog("Keepalive IP Address: " + ret)
        
                # step: check GPRS BSIC for AT&T 3G
        ret = self.se_ins.get_element_by_id(driver,str(msciids.MSCIID_CFG_CMN_IPPING_PERIOD ) +'-d1')
        basic_airlink.slog("Keepalive Ping Time (min): " + ret)
        
                # step: check GPRS BSIC for AT&T 3G
        ret = self.se_ins.get_element_by_id(driver,'10298-d1')
        basic_airlink.slog("DNS Proxy: " + ret)
        
                # step: check GPRS BSIC for AT&T 3G
        ret = self.se_ins.get_element_by_id(driver,"5030-d1")
        basic_airlink.slog("DNS Override: " + ret)
        
                # step: check GPRS BSIC for AT&T 3G
        ret = self.se_ins.get_element_by_id(driver,"1082-d1")
        basic_airlink.slog("DNS Server 1 (IPv4): " + ret)


        ret = self.se_ins.get_element_by_id(driver,"1083-d1")
        basic_airlink.slog("DNS Server 2 (IPv4): " + ret)
                
                # step: check GPRS BSIC for AT&T 3G
        ret = self.se_ins.get_element_by_id(driver,"10701")
        basic_airlink.slog("Number of SIMs present: " + ret)
        
                # step: check GPRS BSIC for AT&T 3G
        ret = self.se_ins.get_element_by_id(driver,"10702")
        basic_airlink.slog("Primary SIM: " + ret)        

        ret = self.se_ins.get_element_by_id(driver,"10703")
        basic_airlink.slog("Active SIM: " + ret)    
        
        ret = self.se_ins.get_element_by_id(driver,"283")
        basic_airlink.slog("Bytes Sent: " + ret)    
        
        ret = self.se_ins.get_element_by_id(driver,"284")
        basic_airlink.slog("Bytes Received: " + ret)    

        ret = self.se_ins.get_element_by_id(driver,"281")
        basic_airlink.slog("Packets Sent: " + ret)    
        
        ret = self.se_ins.get_element_by_id(driver,"282")
        basic_airlink.slog("Packets Received: " + ret)    
                
        self.assertEqual(fail_flag, 0)             
    
    
    def tc_status_lan_ui(self):
        '''
        to test status/lan page by Selenium/ACEmanager UI
        
        '''
            
        driver = self.driver     
        fail_flag = self.fail_flag                           
        
        # step: come to Status page from AceManager          
        #self.se_ins.status_page(driver)              
        self.se_ins.status_lan_page(driver)              

        #step: check each item at Status home page 
        basic_airlink.slog("step: check each item at Status LAN page")
                
        # step: check Ethernet status
        ret = self.se_ins.get_element_by_id(driver,"55001")
        basic_airlink.slog(" Ethernet 1 status: " +ret)

        ret = self.se_ins.get_element_by_id(driver,"55002")
        basic_airlink.slog(" Ethernet 2 status: " +ret)
        
        ret = self.se_ins.get_element_by_id(driver,"55003")
        basic_airlink.slog(" Ethernet 3 status: " +ret)
        
        # step: check USB mode
        ret = self.se_ins.get_element_by_id(driver,'1130-d1')
        basic_airlink.slog("USB mode: " + ret)
        
        # step: check Number of connected clients
        ret = self.se_ins.get_element_by_id(driver,"5006")
        basic_airlink.slog("Number of connected clients: " + ret)
        
        # step: check LAN IP Packets Sent
        ret = self.se_ins.get_element_by_id(driver,"279")
        basic_airlink.slog("LAN IP Packets Sent: " + ret)

        # step: check LAN IP Packets Received
        ret = self.se_ins.get_element_by_id(driver,"280")
        basic_airlink.slog("LAN IP Packets Received: " + ret)
        
        ret = self.se_ins.get_element_by_id(driver,"9001-d1")
        basic_airlink.slog("VRRP: " + ret)  
        
        # TODO: read two tables IP/MAC, VLAN       
                                                                    
        self.assertEqual(fail_flag, 0)             
            
    
    def tc_status_vpn_ui(self):
        '''
        to test status/vpn page by Selenium/ACEmanager UI
        
        '''
            
        driver = self.driver     
        fail_flag = self.fail_flag                        
        
        # step: come to Status/VPN page from AceManager Web UI      
        #self.se_ins.status_page(driver)              
        self.se_ins.status_vpn_page(driver)              
 
        #step: check each item at Status home page 
        basic_airlink.slog("step: check each item at Status VPN page")
        
        # step: Check items from Status/VPN page from AceManager Web UI      
       
        ret = self.se_ins.get_element_by_id(driver,"3177-d1")
        basic_airlink.slog("Incoming out of band: " +ret)           

        ret = self.se_ins.get_element_by_id(driver,"3178-d1")
        basic_airlink.slog("Outgoing out of band: " +ret)      
        
        ret = self.se_ins.get_element_by_id(driver,"3179-d1")
        basic_airlink.slog("Outgoing Host out of band: " +ret)      
        
        ret = self.se_ins.get_element_by_id(driver,"3176-d1")
        basic_airlink.slog("VPN 1 Status: " +ret)      

        ret = self.se_ins.get_element_by_id(driver,"3205-d1")
        basic_airlink.slog("VPN 2 Status: " +ret)  

        ret = self.se_ins.get_element_by_id(driver,"3231-d1")
        basic_airlink.slog("VPN 3 Status: " +ret)  
        
        ret = self.se_ins.get_element_by_id(driver,"3257-d1")
        basic_airlink.slog("VPN 4 Status: " +ret)  
        
        ret = self.se_ins.get_element_by_id(driver,"3283-d1")
        basic_airlink.slog("VPN 5 Status: " +ret)  
                                   
        self.assertEqual(fail_flag, 0) 
        

    def tc_status_security_ui(self):
        '''
        to test status/security page by Selenium/ACEmanager web UI
        
        '''
            
        driver = self.driver     
        
        # step: come to Status/VPN page from AceManager Web UI      
        basic_airlink.slog("step: come to Status Security web page from ACEmanager")
        self.se_ins.status_security_page(driver)              

        #step: check each item at Status/Security page 
        basic_airlink.slog("step: check each item at Status Security page")
                
        ret = self.se_ins.get_element_by_id(driver,"5113-d1")
        basic_airlink.slog("DMZ status: " +ret)           

        ret = self.se_ins.get_element_by_id(driver,"5112-d1")
        basic_airlink.slog("Port Forwarding: " +ret)      
        
        ret = self.se_ins.get_element_by_id(driver,"3505-d1")
        basic_airlink.slog("Port Filtering Inbound: " +ret)      
        
        ret = self.se_ins.get_element_by_id(driver,"3506-d1")
        basic_airlink.slog("Port Filtering Outbounds: " +ret)      

        ret = self.se_ins.get_element_by_id(driver,"1062-d1")
        basic_airlink.slog("Trusted Hosts (Friends): " +ret)  

        ret = self.se_ins.get_element_by_id(driver,"3509-d1")
        basic_airlink.slog("MAC Filtering: " +ret)  
        
        ret = self.se_ins.get_element_by_id(driver,"386")
        basic_airlink.slog("IP Reject Count: " +ret)  
                                   
        self.assertEqual(self.fail_flag, 0) 
        
            
    def tc_status_services_ui(self):
        '''
        to test status/services page by Selenium/ACEmanager UI
        
        '''
        driver = self.driver     
        
        # step: come to Status/services page from AceManager Web UI      
        basic_airlink.slog("step: come to Status services web page from ACEmanager")
        self.se_ins.status_services_page(driver)              

        #step: check each item at Status/services page 
        basic_airlink.slog("step: check each item at Status services page")

        ret = self.se_ins.get_element_by_id(driver,"5026-d1")
        basic_airlink.slog("AVMS status: " +ret)           

        ret = self.se_ins.get_element_by_id(driver,"1149-d1")
        basic_airlink.slog("ACEmanager access method: " +ret)      
        
        ret = self.se_ins.get_element_by_id(driver,"5011-d1")
        basic_airlink.slog("Dynamic DNS Service: " +ret)      
        
        ret = self.se_ins.get_element_by_id(driver,"1107-d1")
        basic_airlink.slog("Enable time update: " +ret)      

        ret = self.se_ins.get_element_by_id(driver,"262")
        basic_airlink.slog("Power state: " +ret)  

        ret = self.se_ins.get_element_by_id(driver,"906-d1")
        basic_airlink.slog("Engine Hours: " +ret)    
                   
        self.assertEqual(self.fail_flag, 0) 
    
    
    def tc_status_gps_ui(self):
        '''
        to test status/gps page by Selenium/ACEmanager UI
        
        '''
        driver = self.driver     
        
        # step: come to Status/gps page from AceManager Web UI      
        basic_airlink.slog("step: come to Status GPS web page from ACEmanager")
        self.se_ins.status_gps_page(driver)              

        #step: check each item at Status/gps page 
        basic_airlink.slog("step: check each item at Status GPS page")

        ret = self.se_ins.get_element_by_id(driver,"10929-d1")
        basic_airlink.slog("Enable GPS: " +ret)           

        ret = self.se_ins.get_element_by_id(driver,"900")
        basic_airlink.slog("GPS fix: " +ret)      
        
        ret = self.se_ins.get_element_by_id(driver,"901")
        basic_airlink.slog("Satellite Count: " +ret)      
        
        ret = self.se_ins.get_element_by_id(driver,"902")
        basic_airlink.slog("Latitude: " +ret)      

        ret = self.se_ins.get_element_by_id(driver,"903")
        basic_airlink.slog("Longitude: " +ret)  

        ret = self.se_ins.get_element_by_id(driver,"904")
        basic_airlink.slog("Heading: " +ret) 

        ret = self.se_ins.get_element_by_id(driver,"905")
        basic_airlink.slog("Speed(km/h): " +ret) 
                           
        self.assertEqual(self.fail_flag, 0) 
                
    
    def tc_status_serial_ui(self):
        '''
        to test status/serial page by Selenium/ACEmanager UI
        
        '''
        driver = self.driver     
        
        # step: come to Status/serial page from AceManager Web UI      
        basic_airlink.slog("step: come to Status serial web page from ACEmanager")
        self.se_ins.status_serial_page(driver)              

        #step: check each item at Status/serial page 
        basic_airlink.slog("step: check each item at Status serial page")
 
        ret = self.se_ins.get_element_by_id(driver,"10120-d1")
        basic_airlink.slog("Serila Reserved by External Application: " +ret)           

        ret = self.se_ins.get_element_by_id(driver,"275")
        basic_airlink.slog("Serial Port Mode: " +ret)      
        
        ret = self.se_ins.get_element_by_id(driver,"1048-d1")
        basic_airlink.slog("TCP Auto Answer: " +ret)      
        
        ret = self.se_ins.get_element_by_id(driver,"1054-d1")
        basic_airlink.slog("UDP Auto Answer: " +ret)      

        ret = self.se_ins.get_element_by_id(driver,"273")
        basic_airlink.slog("Serial bytes sent: " +ret)  

        ret = self.se_ins.get_element_by_id(driver,"274")
        basic_airlink.slog("Serial bytes received: " +ret) 

        ret = self.se_ins.get_element_by_id(driver,"265")
        basic_airlink.slog("Host signal level: " +ret) 
                    
        self.assertEqual(self.fail_flag, 0)  
            
   
    def tc_status_applications_ui(self):
        '''
        to test status/applications page by Selenium/ACEmanager UI
        '''
        driver = self.driver     
        
        # step: come to Status/Applications page from AceManager Web UI      
        basic_airlink.slog("step: come to Status/Applications web page from ACEmanager")
        self.se_ins.status_applications_page(driver)              

        #step: check each item at Status/Applications page 
        basic_airlink.slog("step: check each item at Status/Applications page")

        ret = self.se_ins.get_element_by_id(driver,"1327-d1")
        basic_airlink.slog("Garmin Status: " +ret)      
        
        ret = self.se_ins.get_element_by_id(driver,"25003-d1")
        basic_airlink.slog("Data Services: " +ret)      
        
        ret = self.se_ins.get_element_by_id(driver,"10250-d1")
        basic_airlink.slog("ALEOS Application Framework: " +ret)      

        ret = self.se_ins.get_element_by_id(driver,"10120-d2")
        basic_airlink.slog("Serial Port Received: " +ret)  

        ret = self.se_ins.get_element_by_id(driver,"10125-d1")
        basic_airlink.slog("QCOM DM Port Resource Reserve: " +ret) 
                   
        self.assertEqual(self.fail_flag, 0) 
            
        
    def tc_status_about_ui(self):
        '''
        to test status/About page by Selenium/ACEmanager UI
        '''
        driver = self.driver     
        
        # step: come to Status/VPN page from ACEmanager Web UI      
        basic_airlink.slog("step: come to Status/About web page from ACEmanager")
        self.se_ins.status_about_page(driver)              

        #step: check each item at Status/About page 
        basic_airlink.slog("step: check each item at Status/About web page")

        ret = self.se_ins.get_element_by_id(driver,"7")
        basic_airlink.slog("Device Model: " +ret)
        self.assertEqual(ret, tbd_config_map[self.device_name]["MODEL"])  
                
        ret = self.se_ins.get_element_by_id(driver,"9")
        basic_airlink.slog("Radio Module Type: " +ret)      
        self.assertEqual(ret, tbd_config_map[self.device_name]["RM_TYPE"])  
        
        ret = self.se_ins.get_element_by_id(driver,"8")
        basic_airlink.slog("Radio Firmware Version: " +ret)      
        self.assertEqual(ret, tbd_config_map[self.device_name]["RADIO_FW_VER"])  

        ret = self.se_ins.get_element_by_id(driver,"25")
        basic_airlink.slog("Global ID: " +ret)  
        self.assertEqual(ret, tbd_config_map[self.device_name]["MODEM_NAME"])  

        ret = self.se_ins.get_element_by_id(driver,"10928")
        basic_airlink.slog("GPS/RAP Device ID: " +ret) 
        
        ret = self.se_ins.get_element_by_id(driver,"66")
        basic_airlink.slog("Ethernet Mac Address: " +ret)      
        self.assertEqual(ret, tbd_config_map[self.device_name]["ETH_MAC"])  

        if status_config_map["XCARD_ETH"] == "YES":
            ret = self.se_ins.get_element_by_id(driver,"67")
            basic_airlink.slog("Ethernet2 Mac Address: " +ret)      
            self.assertEqual(ret, tbd_config_map[self.device_name]["ETH2_MAC"])  
            
            ret = self.se_ins.get_element_by_id(driver,"68")
            basic_airlink.slog("Ethernet3 Mac Address: " +ret)      
            self.assertEqual(ret, tbd_config_map[self.device_name]["ETH3_MAC"])  
                
        ret = self.se_ins.get_element_by_id(driver,"4")
        basic_airlink.slog("ALEOS Software Version: " +ret)      
        self.assertEqual(ret, tbd_config_map[self.device_name]["ALEOS_FW_VER"])  
        
        ret = self.se_ins.get_element_by_id(driver,"5")
        basic_airlink.slog("Device Hardware Configuration: " +ret)      

        ret = self.se_ins.get_element_by_id(driver,"6")
        basic_airlink.slog("Boot Version: " +ret)  

        ret = self.se_ins.get_element_by_id(driver,"3")
        basic_airlink.slog("MSCI Version: " +ret) 
                          
        self.assertEqual(self.fail_flag, 0)  
            

class TestsuiteStatusAt(unittest.TestCase):
    ''' This test suite automates Status test cases by AT commands
    
    '''
                     
    def setUp(self):
        ''' the test runner will run that method prior to each test
        '''
        self.conn_ins = connectivity.Connectivity()       
        
        # step: check if devices ready    
        basic_airlink.slog("step: check if testbed is ready")
        self.conn_ins.testbed_ready()
        self.device_name = tbd_config_map["DUTS"][0]
            
  
    def tearDown(self):
        ''' the test runner will invoke that method after each test
        TODO
        '''
        basic_airlink.slog(" After test run")
 
    def tc_status_home_general_at(self):
        '''
        to test status/home page (general) by AT command
        
        '''
        test_id = "tc_status_home_general_at"
        logging.info(test_id+' : '+'begins\n')    
        fail_flag = 0
           
        self.assertEqual(fail_flag, 0)             
    

    def tc_status_home_specific_at(self):
        '''
        to test status/home page (specific) by AT command
        
        '''
        test_id = "tc_status_home_specific_at"
        logging.info(test_id+' : '+'begins\n')    
            
        fail_flag = 0
           
        self.assertEqual(fail_flag, 0)     

    def tc_status_at_lan(self):
        '''
        to test status/lan page by AT command
        
        '''
        test_id = "tc_status_at_lan"
        logging.info(test_id+' : '+'begins\n')    
            
        fail_flag = 0
           
        self.assertEqual(fail_flag, 0) 
        

    def tc_status_at_vpn(self):
        '''
        to test status/vpn page by AT command
        
        '''
        test_id = "tc_status_at_vpn"
        logging.info(test_id+' : '+'begins\n')    
            
        fail_flag = 0
           
        self.assertEqual(fail_flag, 0)                    

    def tc_status_at_about(self):
        '''
        to test status/about page by AT command
        
        '''
        test_id = "tc_status_at_about"
        logging.info(test_id+' : '+'begins\n')    
            
        return     
 
   
    def tc_status_lte_callbox_at_home(self):
        '''
         to test status/home page by AT command, using callbox as network simulator
        
        '''
        test_id = "tc_status_at_about"
        logging.info(test_id+' : '+'begins\n')    
            
        return    


    def tc_status_at_applications(self):
        '''
        to test status/sapplications page by AT command
        
        '''
        test_id = "tc_status_at_applications"
        logging.info(test_id+' : '+'begins\n')    
            
        return 

    def tc_status_at_serial(self):
        '''
        to test status/serial page by AT command
        
        '''
        test_id = "tc_status_at_serial"
        logging.info(test_id+' : '+'begins\n')    
            
        return  
                    
def setup_suite():
    """  Gather all the tests from this module in a test suite.    
    """
    test_suite = unittest.TestSuite()

    for k in range(status_config_map["RUN_REPEAT"]):
        
        if status_config_map["RUN_ALL_TESTCASES"]:
            
            # run all test cases
            #for i in range(1,status_config_map["ALL_TASECASE_NUMBER"]+1):
            for i in range(1,len(status_config_map["LIST_TESTCASES"])+1):
                
                basic_airlink.slog(str(i)+" "+status_config_map["RUN_ALL_TESTCASES"])
                if status_config_map["RUN_UI_AT_TESTCASES"] =="UI": 
                    test_suite.addTest(TestsuiteStatusUi(status_config_map["LIST_TESTCASES"][i]))
                elif status_config_map["RUN_UI_AT_TESTCASES"] =="AT": 
                    test_suite.addTest(TestsuiteStatusAt(status_config_map["LIST_TESTCASES"][i]))
                
        else:
            
            # run selective test cases
            for [a,b] in status_config_map["RUN_SELECTIVE_TESTCASES"] :
                
                for i in range(a,b+1):
                    
                    basic_airlink.slog(status_config_map["LIST_TESTCASES"][i])
                    
                    if status_config_map["RUN_UI_AT_TESTCASES"] =="UI": 
                        test_suite.addTest(TestsuiteStatusUi(status_config_map["LIST_TESTCASES"][i]))
                    elif status_config_map["RUN_UI_AT_TESTCASES"] =="AT": 
                        test_suite.addTest(TestsuiteStatusAt(status_config_map["LIST_TESTCASES"][i]))

    return test_suite      
     
####################################################
# main Status test automation
####################################################
if __name__ == "__main__":

    airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 

    stream = open(airlinkautomation_home_dirname+'/config/testbed2Conf.yml', 'r')
    tbd_config_map = yaml.load(stream)
    stream.close()
    
    log_filename=basic_airlink.get_log_filename(tbd_config_map, "status")
    FORMAT ='%(asctime)-15s => %(levelname)-8s => %(message)s'
    if tbd_config_map["LOG_LEVEL"]=="DEBUG":
        LEVEL = logging.DEBUG
    else: 
        LEVEL = logging.INFO 
    logging.basicConfig(level = LEVEL,filename = log_filename, format=FORMAT,  filemode='w') 
        
    fo=open(airlinkautomation_home_dirname+'/testsuite/Status/status_test_conf.yml','r')
    status_config_map = yaml.load(fo)
    fo.close()

    time_stamp = time.strftime("%b-%d-%Y_%H-%M")

    report_filename=basic_airlink.get_report_filename(tbd_config_map, "status")

    fpp = file(report_filename, 'wb')
    
    description_text= r""" ***"""+ "log file name " +log_filename 
    
    runner = htmlreport.HTMLTestRunner(
                stream = fpp,
                title = 'Status Test Report', 
                description = description_text
                )    
    
    result = None

    mySuite=setup_suite() 
    
    test_cases = mySuite.countTestCases()
    
    basic_airlink.slog("Total test cases: %d" % test_cases)
    
    test_result=runner.run(mySuite, True, result)

    basic_airlink.slog("For details of the results please check \n http://carmd-ev-aptest:8080/job/TestDrive/ws/%s\n\n For details of the log please check \n http://carmd-ev-aptest:8080/job/TestDrive/ws/%s\n\n"  % ( report_filename,log_filename))
    basic_airlink.slog("Total %d test cases PASS." % test_result.success_count )
    basic_airlink.slog("Total %d test cases FAILED." % test_result.failure_count )
    basic_airlink.slog("Total %d test cases has ERROR." % test_result.error_count )    
    
    if (test_result.error_count + test_result.failure_count): 
        sys.exit(1)
    else:
        sys.exit(0)