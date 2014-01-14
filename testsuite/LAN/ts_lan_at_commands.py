################################################################################
#
# This module automates LAN's AT commands test cases. 
# Company: Sierra Wireless
# Date: Jul 5, 2013
# Author: Airlink
# 
################################################################################

import os
import sys
import time
import unittest

import at_utilities
import basic_airlink
import connectivity


airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")
sys.path.append(".")

basic_airlink.append_sys_path()

tbd_config_map, lan_config_map = basic_airlink.get_config_data("LAN","")
        
class TsLanAtCommands(unittest.TestCase):
    ''' This test suite automates LAN testcases by AT commands.
    Please make sure testbed (DUT,X-card, connection, configuration) is ready 
    before run any test.
    '''     
                     
    def setUp(self):
        ''' the test runner will run that method prior to each test
        Args: None
        Returns: None
        '''
           
        self.conn_ins = connectivity.Connectivity()     
        self.at_ins   = at_utilities.AtCommands()   
         
        # step: check if devices ready    
        basic_airlink.slog("step: check if testbed is ready")
        self.conn_ins.testbed_ready() 
        self.device_name = tbd_config_map["DUTS"][0]
               
        basic_airlink.slog("Step:  connect to DUT and generate connection instance")
        
        self.connect_instance = self.conn_ins.connection_types()
        
        if not self.connect_instance.connect(): 
            basic_airlink.slog("Problem: testbed not ready yet")
                    
        self.fail_flag = 0
           
        self.verificationErrors = []
        self.accept_next_alert = True                
        
          
    def tearDown(self):
        ''' the test runner will invoke that method after each test
        Args: None
        Returns: None
        '''        
        self.assertEqual([], self.verificationErrors) 
        self.connect_instance.close()
        
        basic_airlink.slog(" Testcase complete")
        
            
    def tc_ethernet_dhcp_commands(self):
        ''' LAN test case Ethernet_DHCP_commands in ApTest
        '''
        connect_instance = self.connect_instance
        
        #step: get/set DHCP server mode by AT command
        ret = self.at_ins.get_ethernet_dhcp_server_mode(connect_instance)
        self.assertNotEqual(ret, basic_airlink.ERR)                      
        
        ret=self.at_ins.set_ethernet_dhcp_server_mode(connect_instance,lan_config_map["DHCP_SERVER_MODE"])
        self.assertEqual(ret, True)
        
        ret = self.at_ins.get_ethernet_dhcp_server_mode(connect_instance)
        if  ret.find(lan_config_map["DHCP_SERVER_MODE"],0) == -1 or ret == basic_airlink.ERR: 
            self.fail_flag +=1     
            
        #step: get/set Ethernet device IP 
        ret = self.at_ins.get_ethernet_device_ip(connect_instance)
        self.assertNotEqual(ret, basic_airlink.ERR)                    
            
        ret = self.at_ins.set_ethernet_device_ip(connect_instance,lan_config_map["ETH_DEVICE_IP"])                         
        self.assertEqual(ret,True)
        ret = self.at_ins.get_ethernet_device_ip(connect_instance)                            
        if  ret.find(lan_config_map["ETH_DEVICE_IP"],0) == -1 or ret == basic_airlink.ERR: 
            self.fail_flag +=1                                  
                        
        #step: get/set starting IP by AT command
        ret = self.at_ins.get_ethernet_starting_ip(connect_instance)
        self.assertNotEqual(ret, basic_airlink.ERR)                    
                                   
        ret = self.at_ins.set_ethernet_starting_ip(connect_instance,lan_config_map["ETH_STARTING_IP"])
        self.assertEqual(ret, True)                      
        ret = self.at_ins.get_ethernet_starting_ip(connect_instance)                            
        if  ret.find(lan_config_map["ETH_STARTING_IP"],0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1        
            
        #step: get/set ending IP by AT command
        ret = self.at_ins.get_ethernet_ending_ip(connect_instance) 
        self.assertNotEqual(ret, basic_airlink.ERR)                       
                           
        ret =   self.at_ins.set_ethernet_ending_ip(connect_instance,lan_config_map["ETH_ENDING_IP"])
        self.assertEqual(ret, True)     
                         
        ret = self.at_ins.get_ethernet_ending_ip(connect_instance)                            
        if  ret.find(lan_config_map["ETH_ENDING_IP"],0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1                               

        #step: get/set DHCP network mask
        ret =  self.at_ins.get_ethernet_dhcp_network_mask(connect_instance)
        self.assertNotEqual(ret , basic_airlink.ERR)                    
                          
        ret = self.at_ins.set_ethernet_dhcp_network_mask(connect_instance,lan_config_map["DHCP_NETWORK_MASK"])
        self.assertEqual(ret,True)
        
        ret = self.at_ins.get_ethernet_dhcp_network_mask(connect_instance)
        if  ret.find(lan_config_map["DHCP_NETWORK_MASK"],0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1  
            
        self.assertEqual(self.fail_flag, 0)
                                                                                                 
    def tc_ethernet_state(self):
        ''' LAN test case Ethernet state. Don't need DualEthernet card.
        '''
        #step: get Ethernet state by AT command
        ret = self.at_ins.get_ethernet_state(self.connect_instance,"")
        self.assertNotEqual(ret , basic_airlink.ERR)                    

        ret = self.at_ins.get_ethernet_state(self.connect_instance,"1")
        self.assertNotEqual(ret , basic_airlink.ERR)                                       
   
        #self.assertEqual(self.fail_flag, 0) 

    def tc_dual_eth_state(self):
        ''' LAN test case Ethernet state. Please insert 
            DualEthernet card.
        '''
        #step: get Ethernet state by AT command
        ret = self.at_ins.get_ethernet_state(self.connect_instance,"")
        self.assertNotEqual(ret , basic_airlink.ERR)                    

        ret = self.at_ins.get_ethernet_state(self.connect_instance,"1")
        self.assertNotEqual(ret , basic_airlink.ERR)                    
       
        ret = self.at_ins.get_ethernet_state(self.connect_instance,"2")
        self.assertNotEqual(ret , basic_airlink.ERR)                    

        ret = self.at_ins.get_ethernet_state(self.connect_instance,"3")
        self.assertNotEqual(ret , basic_airlink.ERR)                    
   


        
    def tc_ethernet_mac(self):
        ''' LAN test case Ethernet state and Ethernet MAC. Don't insert 
            DualEthernet card.
        '''
        #step: get Ethernet MAC by AT command

        ret = self.at_ins.get_ethernet_mac(self.connect_instance,"")
        self.assertNotEqual(ret, basic_airlink.ERR)  

  
        ret = self.at_ins.get_ethernet_mac(self.connect_instance,"1")
        self.assertNotEqual(ret, basic_airlink.ERR)     
         

    def tc_dual_eth_mac(self):
        ''' LAN test case Ethernet state and Ethernet MAC. Please insert 
            DualEthernet card.
        '''
        #step: get Ethernet MAC by AT command
#        ret = self.at_ins.get_ethernet_state(self.connect_instance,"")
#        if ret=="100Mb/s Full Duplex":  
        ret = self.at_ins.get_ethernet_mac(self.connect_instance,"")
        self.assertNotEqual(ret, basic_airlink.ERR)  

#        ret = self.at_ins.get_ethernet_state(self.connect_instance,"1")
#        if ret=="100Mb/s Full Duplex":          
        ret = self.at_ins.get_ethernet_mac(self.connect_instance,"1")
        self.assertNotEqual(ret, basic_airlink.ERR)  
        
#        ret = self.at_ins.get_ethernet_state(self.connect_instance,"2")
#        if ret =="100Mb/s Full Duplex":                                 
        ret = self.at_ins.get_ethernet_mac(self.connect_instance,"2")
        self.assertNotEqual(ret, basic_airlink.ERR) 

#        ret = self.at_ins.get_ethernet_state(self.connect_instance,"3")
#        if ret=="100Mb/s Full Duplex":           
        ret = self.at_ins.get_ethernet_mac(self.connect_instance,"3")
        self.assertNotEqual(ret, basic_airlink.ERR)   
         
#        self.assertEqual(self.fail_flag, 0)
        
    def tc_global_dns(self):
        ''' LAN test case Global DNS. 
        '''
        #step: get Ethernet MAC by AT command
        ret = self.at_ins.get_dns_state(self.connect_instance,"1")
        self.assertNotEqual(ret, basic_airlink.ERR) 
          
        ret = self.at_ins.get_dns_state(self.connect_instance,"2")
        self.assertNotEqual(ret, basic_airlink.ERR) 
        
        ret = self.at_ins.get_dns_user(self.connect_instance)
        self.assertNotEqual(ret, basic_airlink.ERR)  

        ret = self.at_ins.set_dns_user(self.connect_instance,"172.26.38.3")
        self.assertNotEqual(ret, basic_airlink.ERR) 

        ret = self.at_ins.get_dns_user(self.connect_instance)
        self.assertEqual(ret, "172.26.38.3") 
                         
        #self.assertEqual(self.fail_flag, 0)

    def tc_ppoe_commands(self):
        ''' LAN test case PPoE_commands in ApTest
        '''
        connect_instance = self.connect_instance
        
        #step: get/set DHCP server mode by AT command
        ret = self.at_ins.get_host_auth(connect_instance)
        self.assertNotEqual(ret, basic_airlink.ERR)                      
        
        ret=self.at_ins.set_host_auth(connect_instance,"0")
        self.assertEqual(ret, True)
        
        ret = self.at_ins.get_host_auth(connect_instance)
        if  ret.find("0",0) == -1 or ret == basic_airlink.ERR: 
            self.fail_flag +=1     
            
        ret=self.at_ins.set_host_auth(connect_instance,"1")
        self.assertEqual(ret, True)
        
        ret = self.at_ins.get_host_auth(connect_instance)
        if  ret.find("1",0) == -1 or ret == basic_airlink.ERR: 
            self.fail_flag +=1                                 
                        
        ret=self.at_ins.set_host_auth(connect_instance,"2")
        self.assertEqual(ret, True)
        
        ret = self.at_ins.get_host_auth(connect_instance)
        if  ret.find("2",0) == -1 or ret == basic_airlink.ERR: 
            self.fail_flag +=1    

        ret = self.at_ins.get_host_password(connect_instance)
        if ret == basic_airlink.ERR: 
            self.fail_flag +=1     
            
        ret=self.at_ins.set_host_passsord(connect_instance,"12345")
        self.assertEqual(ret, True)            

        ret = self.at_ins.get_host_password(connect_instance)
        if ret != "12345": 
            self.fail_flag +=1    

        ret = self.at_ins.get_host_username(connect_instance)
        if ret == basic_airlink.ERR: 
            self.fail_flag +=1     
            
        ret=self.at_ins.set_host_username(connect_instance,"user")
        self.assertEqual(ret, True)            

        ret = self.at_ins.get_host_username(connect_instance)
        if ret != "user": 
            self.fail_flag +=1    
                                    
        self.assertEqual(self.fail_flag, 0)
                                   
    def tc_wifi_apbridged(self):
        ''' LAN test case WiFi_APBRIDGED in ApTest. 
        '''

        connect_instance = self.connect_instance

        #step: get/set WIFI AP Bridged by AT command
        ret = self.at_ins.get_wifi_ap_bridged(connect_instance)
        self.assertNotEqual(ret, basic_airlink.ERR)  
                                          
        self.assertEqual(self.at_ins.set_wifi_ap_bridged(connect_instance,"1"), True)
        ret = self.at_ins.get_wifi_ap_bridged(connect_instance)
        if  ret.find("1",0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1    
            
        self.assertEqual(self.at_ins.set_wifi_ap_bridged(connect_instance,"0"), True)
        ret = self.at_ins.get_wifi_ap_bridged(connect_instance)
        if  ret.find("0",0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1 
            
        self.assertEqual(self.fail_flag, 0)                                                          
        
    def tc_wifi_apchannel(self):
        ''' LAN test case WiFi_APCHANNEL in ApTest
        '''

        connect_instance = self.connect_instance

        #step: get/set WIFI AP channel by AT command
        ret = self.at_ins.get_wifi_ap_channel(connect_instance)
        self.assertNotEqual(ret, basic_airlink.ERR)                      
           
        self.assertEqual(self.at_ins.set_wifi_ap_channel(connect_instance,"0"),True)
        ret = self.at_ins.get_wifi_ap_channel(connect_instance)
        if  ret.find("0",0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1 
            
        self.assertEqual(self.at_ins.set_wifi_ap_channel(connect_instance,"1"),True)
        ret = self.at_ins.get_wifi_ap_channel(connect_instance)
        if  ret.find("1",0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1 

        self.assertEqual(self.at_ins.set_wifi_ap_channel(connect_instance,"2"),True)
        ret = self.at_ins.get_wifi_ap_channel(connect_instance)
        if  ret.find("2",0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1 
            
        self.assertEqual(self.at_ins.set_wifi_ap_channel(connect_instance,"3"),True)
        ret = self.at_ins.get_wifi_ap_channel(connect_instance)
        if  ret.find("3",0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1 
            
        self.assertEqual(self.at_ins.set_wifi_ap_channel(connect_instance,"4"),True)
        ret = self.at_ins.get_wifi_ap_channel(connect_instance)
        if  ret.find("4",0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1 
            
        self.assertEqual(self.at_ins.set_wifi_ap_channel(connect_instance,"5"),True)
        ret = self.at_ins.get_wifi_ap_channel(connect_instance)
        if  ret.find("5",0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1 
            
        self.assertEqual(self.at_ins.set_wifi_ap_channel(connect_instance,"6"),True)
        ret = self.at_ins.get_wifi_ap_channel(connect_instance)
        if  ret.find("6",0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1 
            
        self.assertEqual(self.at_ins.set_wifi_ap_channel(connect_instance,"7"),True)
        ret = self.at_ins.get_wifi_ap_channel(connect_instance)
        if  ret.find("7",0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1 
    
        self.assertEqual(self.at_ins.set_wifi_ap_channel(connect_instance,"8"),True)
        ret = self.at_ins.get_wifi_ap_channel(connect_instance)
        if  ret.find("8",0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1 

        self.assertEqual(self.at_ins.set_wifi_ap_channel(connect_instance,"9"),True)
        ret = self.at_ins.get_wifi_ap_channel(connect_instance)
        if  ret.find("9",0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1 
            
        self.assertEqual(self.at_ins.set_wifi_ap_channel(connect_instance,"10"),True)
        ret = self.at_ins.get_wifi_ap_channel(connect_instance)
        if  ret.find("10",0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1  
            
        self.assertEqual(self.at_ins.set_wifi_ap_channel(connect_instance,"11"),True)
        ret = self.at_ins.get_wifi_ap_channel(connect_instance)
        if  ret.find("11",0) == -1 or ret == basic_airlink.ERR:
            self.fail_flag +=1 
                       
        self.assertEqual(self.fail_flag, 0)

    def tc_wifi_apen(self):
        ''' LAN test case WiFi_APEN in ApTest, requires WiFi x-card
        '''

        connect_instance = self.connect_instance

        #step: get/set WIFI AP Enable by AT command
        self.assertNotEqual(self.at_ins.get_wifi_ap_enable(connect_instance), basic_airlink.ERR)           
                                  
        self.assertEqual(self.at_ins.set_wifi_ap_enable(connect_instance,"2"), True)    
        ret = self.at_ins.get_wifi_ap_enable(connect_instance)
        if  ret.find("2",0) == -1 or ret == basic_airlink.ERR: 
            self.fail_flag +=1             
            
        self.assertEqual(self.at_ins.set_wifi_ap_enable(connect_instance,"3"), True) 
        ret = self.at_ins.get_wifi_ap_enable(connect_instance)
        if  ret.find("3",0) == -1 or ret == basic_airlink.ERR: 
            self.fail_flag +=1 
 
        self.assertEqual(self.fail_flag, 0)

    def tc_wifi_mode(self):
        ''' LAN test case wifi mode in ApTest, requires WiFi x-card
        '''
        connect_instance = self.connect_instance

        #step: get/set WIFI AP Enable by AT command
        self.assertNotEqual(self.at_ins.get_wifi_mode(connect_instance), basic_airlink.ERR)           
                                  
        self.assertEqual(self.at_ins.set_wifi_mode(connect_instance,"2"), True)    
        ret = self.at_ins.get_wifi_mode(connect_instance)
        if  ret.find("2",0) == -1 or ret == basic_airlink.ERR: 
            self.fail_flag +=1             
            basic_airlink.slog("Problem: wifimode 2 !!!")
            
        self.assertEqual(self.at_ins.set_wifi_mode(connect_instance,"3"), True) 
        ret = self.at_ins.get_wifi_mode(connect_instance)
        if  ret.find("3",0) == -1 or ret == basic_airlink.ERR: 
            self.fail_flag +=1 
            basic_airlink.slog("Problem: wifimode 3 !!!")
 
        self.assertEqual(self.fail_flag, 0)
 
    def tc_wifi_mac(self):
        ''' LAN test case wifi MAC in ApTest, requires WiFi x-card
        '''
        #step: get/set WIFI AP Enable by AT command
        ret=self.at_ins.get_wifi_mode(self.connect_instance)
        self.assertNotEqual(ret, basic_airlink.ERR)                       
            
        self.assertEqual(self.at_ins.set_wifi_mode(self.connect_instance,"3"), True) 
        ret = self.at_ins.get_wifi_mode(self.connect_instance)
        if  ret.find("3",0) == -1 or ret == basic_airlink.ERR: 
            self.fail_flag +=1 

        ret=self.at_ins.get_datz(self.connect_instance) 
        if ret == basic_airlink.ERR:
            self.fail_flag +=1     
        if ret == "1":
            self.at_ins.set_datz(self.connect_instance,"0") 
            
        ret = self.at_ins.atz_reboot(self.connect_instance)
            
        time.sleep(tbd_config_map[self.device_name]["REBOOT_TIMEOUT"])
        
        basic_airlink.slog("Step:  connect to DUT and generate connection instance")
        self.connect_instance = self.conn_ins.connection_types()
        if not self.connect_instance.connect(): 
            basic_airlink.slog("Problem: testbed not ready yet")
 
        self.assertNotEqual(self.at_ins.get_wifi_mac(self.connect_instance), basic_airlink.ERR)                       
            
        self.assertEqual(self.fail_flag, 0)
 
    def tc_wifi_ap_max_client(self):
        ''' LAN test case wifi AP maximum clients in ApTest, 
            requires WiFi x-card installed.
        '''                      
                  
        original_max_client = self.at_ins.get_wifi_ap_max_client(self.connect_instance)
        self.assertNotEqual(original_max_client, basic_airlink.ERR)                       

        ret=self.at_ins.set_wifi_ap_max_client(self.connect_instance,"1") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_max_client(self.connect_instance)
        self.assertEqual(ret, "1")                       
                     
        ret=self.at_ins.set_wifi_ap_max_client(self.connect_instance,"2") 
        self.assertEqual(ret, True)   
               
        ret = self.at_ins.get_wifi_ap_max_client(self.connect_instance)
        self.assertEqual(ret, "2")                       

        ret=self.at_ins.set_wifi_ap_max_client(self.connect_instance,"3") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_max_client(self.connect_instance)
        self.assertEqual(ret, "3")                       

        ret=self.at_ins.set_wifi_ap_max_client(self.connect_instance,"4") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_max_client(self.connect_instance)
        self.assertEqual(ret, "4")                        
            
        ret=self.at_ins.set_wifi_ap_max_client(self.connect_instance,"5") 
        self.assertEqual(ret, True)                        
               
        ret = self.at_ins.get_wifi_ap_max_client(self.connect_instance)
        self.assertEqual(ret, "5")                       

        ret=self.at_ins.set_wifi_ap_max_client(self.connect_instance,"6") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_max_client(self.connect_instance)
        self.assertEqual(ret, "6") 

        ret=self.at_ins.set_wifi_ap_max_client(self.connect_instance,"7") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_max_client(self.connect_instance)
        self.assertEqual(ret, "7")                       

        ret=self.at_ins.set_wifi_ap_max_client(self.connect_instance,"8") 
        self.assertEqual(ret, True)                         
               
        ret = self.at_ins.get_wifi_ap_max_client(self.connect_instance)
        self.assertEqual(ret, "8")    
 
        ret=self.at_ins.set_wifi_ap_max_client(self.connect_instance,original_max_client) 
        self.assertEqual(ret, True)                       
                                             
        #self.assertEqual(self.fail_flag, 0)

    def tc_wifi_ap_security_type(self):
        ''' LAN test case wifi AP security type in ApTest, 
            requires WiFi x-card installed. ALLX2440/ALLX-4629
        '''                       
                  
        original_security_type = self.at_ins.get_wifi_ap_security_type(self.connect_instance)
        self.assertNotEqual(original_security_type, basic_airlink.ERR)                       

        # ALLX-2440 not allow AT command to set security 
#        ret=self.at_ins.set_wifi_ap_security_type(self.connect_instance,"0") 
#        self.assertEqual(ret, True)                       
               
#        ret = self.at_ins.get_wifi_ap_security_type(self.connect_instance)
#        self.assertEqual(ret, "0")                       

#        ret=self.at_ins.set_wifi_ap_security_type(self.connect_instance,"3") 
#        self.assertEqual(ret, True)                       
               
#        ret = self.at_ins.get_wifi_ap_security_type(self.connect_instance)
#        self.assertEqual(ret, "3")  
#        
#        ret=self.at_ins.set_wifi_ap_security_type(self.connect_instance,"5") 
#        self.assertEqual(ret, True)                       
#               
#        ret = self.at_ins.get_wifi_ap_security_type(self.connect_instance)
#        self.assertEqual(ret, "5")                       
# 
#        ret=self.at_ins.set_wifi_ap_security_type(self.connect_instance,original_security_type) 
#        self.assertEqual(ret, True)                       
                                             
        #self.assertEqual(self.fail_flag, 0)  
        
    def tc_wifi_ap_tx_power(self):
        ''' LAN test case wifi AP Trasmit power in ApTest, 
            requires WiFi x-card installed.
        '''                      
                  
        original_ap_tx_power = self.at_ins.get_wifi_ap_tx_power(self.connect_instance)
        self.assertNotEqual(original_ap_tx_power, basic_airlink.ERR)                       

        ret=self.at_ins.set_wifi_ap_tx_power(self.connect_instance,"1") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_tx_power(self.connect_instance)
        self.assertEqual(ret, "1")                       

        ret=self.at_ins.set_wifi_ap_tx_power(self.connect_instance,"0") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_tx_power(self.connect_instance)
        self.assertEqual(ret, "0")                       
 
        ret=self.at_ins.set_wifi_ap_tx_power(self.connect_instance,original_ap_tx_power) 
        self.assertEqual(ret, True)                       
                                             
        #self.assertEqual(self.fail_flag, 0)       
 
    def tc_wifi_ap_dhcp_commands(self):
        ''' LAN test case wifi AP DHCP commands in ApTest, 
            requires WiFi x-card installed, and wifi mode set.
        '''        
        # step : test WIFI AP Host IP          
        original_ap_host_ip = self.at_ins.get_wifi_ap_host_ip(self.connect_instance)
        self.assertNotEqual(original_ap_host_ip, basic_airlink.ERR)                       

        ret=self.at_ins.set_wifi_ap_host_ip(self.connect_instance,"192.168.17.31") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_host_ip(self.connect_instance)
        self.assertEqual(ret, "192.168.17.31")                       

        ret=self.at_ins.set_wifi_ap_host_ip(self.connect_instance,original_ap_host_ip) 
        self.assertEqual(ret, True)                       
               
        # step : test WIFI AP starting  IP          
        original_ap_start_ip = self.at_ins.get_wifi_ap_starting_ip(self.connect_instance)
        self.assertNotEqual(original_ap_start_ip, basic_airlink.ERR)                       

        ret=self.at_ins.set_wifi_ap_starting_ip(self.connect_instance,"192.168.17.100") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_starting_ip(self.connect_instance)
        self.assertEqual(ret, "192.168.17.100")                       

        ret=self.at_ins.set_wifi_ap_starting_ip(self.connect_instance,original_ap_start_ip) 
        self.assertEqual(ret, True)                      

        # step : test WIFI AP ending IP          
        original_ap_end_ip = self.at_ins.get_wifi_ap_ending_ip(self.connect_instance)
        self.assertNotEqual(original_ap_end_ip, basic_airlink.ERR)                       

        ret=self.at_ins.set_wifi_ap_ending_ip(self.connect_instance,"192.168.17.150") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_ending_ip(self.connect_instance)
        self.assertEqual(ret, "192.168.17.150")                       

        ret=self.at_ins.set_wifi_ap_ending_ip(self.connect_instance,original_ap_end_ip) 
        self.assertEqual(ret, True)   

        # step : test WIFI AP network mask          
        original_ap_net_mask = self.at_ins.get_wifi_ap_net_mask(self.connect_instance)
        self.assertNotEqual(original_ap_net_mask, basic_airlink.ERR)                       

        ret=self.at_ins.set_wifi_ap_net_mask(self.connect_instance,"255.255.255.0") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_net_mask(self.connect_instance)
        self.assertEqual(ret, "255.255.255.0")                       

        ret=self.at_ins.set_wifi_ap_net_mask(self.connect_instance,original_ap_net_mask) 
        self.assertEqual(ret, True)   
                                                     
        #self.assertEqual(self.fail_flag, 0)   

    def tc_wifi_ap_ssid_commands(self):
        ''' LAN test case WIFI AP SSID commands in ApTest, 
            requires WiFi x-card installed, and wifi mode set.
        '''        
        # step : test WIFI AP SSID BCAST          
        original_ssid_bcast = self.at_ins.get_wifi_ap_ssid_broadcast(self.connect_instance)
        self.assertNotEqual(original_ssid_bcast, basic_airlink.ERR)                       

        ret=self.at_ins.set_wifi_ap_ssid_broadcast(self.connect_instance,"1") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_ssid_broadcast(self.connect_instance)
        self.assertEqual(ret, "1")                       

        ret=self.at_ins.set_wifi_ap_ssid_broadcast(self.connect_instance,"0") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_ssid_broadcast(self.connect_instance)
        self.assertEqual(ret, "0") 
        
        ret=self.at_ins.set_wifi_ap_ssid_broadcast(self.connect_instance,original_ssid_bcast) 
        self.assertEqual(ret, True)                       

        # step : test WIFI AP SSID Value/ modem name        
        original_ssid_value = self.at_ins.get_wifi_ap_ssid_val(self.connect_instance)
        self.assertNotEqual(original_ssid_value, basic_airlink.ERR)                       

        modem_name = self.at_ins.get_modem_name(self.connect_instance)

        ret=self.at_ins.set_wifi_ap_ssid_val(self.connect_instance,modem_name) 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_ssid_val(self.connect_instance)
        self.assertEqual(ret, modem_name)                       
        
        ret=self.at_ins.set_wifi_ap_ssid_val(self.connect_instance,original_ssid_value) 
        self.assertEqual(ret, True)                                                        

    def tc_wifi_ap_wep_commands(self):
        ''' LAN test case wifi AP Wep commands in ApTest, 
            requires WiFi x-card installed, and wifi mode set.
            User manual: Wep not recommended for Wifi security.
            Ignore this testcase.
        '''        

        # step : test WIFI AP Wep Encryption type         
        original_wep_enc_type = self.at_ins.get_wifi_ap_wep_enc_type(self.connect_instance)
        self.assertNotEqual(original_wep_enc_type, basic_airlink.ERR)                       

        ret=self.at_ins.set_wifi_ap_wep_enc_type(self.connect_instance,"0") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_wep_enc_type(self.connect_instance)
        self.assertEqual(ret, "0")                       

        ret=self.at_ins.set_wifi_ap_wep_enc_type(self.connect_instance,"1") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_wep_enc_type(self.connect_instance)
        self.assertEqual(ret, "1") 
        
        ret=self.at_ins.set_wifi_ap_wep_enc_type(self.connect_instance,original_wep_enc_type) 
        self.assertEqual(ret, True)  

        # step : test WIFI AP Wep key       
        original_wep_key = self.at_ins.get_wifi_ap_wep_key(self.connect_instance)
        self.assertNotEqual(original_wep_key, basic_airlink.ERR)  
                 
        # step : test WIFI AP Wep key length        
        original_wep_key_len = self.at_ins.get_wifi_ap_wep_key_len(self.connect_instance)
        self.assertNotEqual(original_wep_key_len, basic_airlink.ERR)                       

        ret=self.at_ins.set_wifi_ap_wep_key_len(self.connect_instance,"0") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_wep_key_len(self.connect_instance)
        self.assertEqual(ret, "0")                       

        ret=self.at_ins.set_wifi_ap_wep_key_len(self.connect_instance,"1") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_wep_key_len(self.connect_instance)
        self.assertEqual(ret, "1") 

        ret=self.at_ins.set_wifi_ap_wep_key_len(self.connect_instance,"2") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_wep_key_len(self.connect_instance)
        self.assertEqual(ret, "2") 
                
        ret=self.at_ins.set_wifi_ap_wep_key_len(self.connect_instance,original_wep_key_len) 
        self.assertEqual(ret, True) 
                                                             
        self.assertEqual(self.fail_flag, 0)   

    def tc_wifi_ap_wpa_commands(self):
        ''' LAN test case wifi AP WPA commands in ApTest, 
            requires WiFi x-card installed, and wifi mode set.
        '''        
        # step : test WIFI AP WPA encryption        
        original_wpa_enc_type = self.at_ins.get_wifi_ap_wpa_crypt(self.connect_instance)
        self.assertNotEqual(original_wpa_enc_type, basic_airlink.ERR)                       

        ret=self.at_ins.set_wifi_ap_wpa_crypt(self.connect_instance,"0") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_wpa_crypt(self.connect_instance)
        self.assertEqual(ret, "0")                       

        ret=self.at_ins.set_wifi_ap_wpa_crypt(self.connect_instance,"1") 
        self.assertEqual(ret, True)                       
               
        ret = self.at_ins.get_wifi_ap_wpa_crypt(self.connect_instance)
        self.assertEqual(ret, "1") 
        
        ret=self.at_ins.get_wifi_ap_wpa_crypt(self.connect_instance,original_wpa_enc_type) 
        self.assertEqual(ret, True)  
                                                     
        self.assertEqual(self.fail_flag, 0)    
                                     
    def tc_dummy(self):
        self.assertEqual(self.fail_flag, 0)
                                                          