################################################################################
#
# This module automates VPN AT commands test cases. 
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
#import ping_airlink

tbd_config_map, vpn_config_map = basic_airlink.get_config_data("VPN","")


class TsVpnAtCommands(unittest.TestCase):
    ''' This test suite automates VPN testcases by AT Commands.
        Please make sure testbed ready before execution.
    '''     
                     
    def setUp(self):
        ''' the test runner will run that method prior to each test

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
        ''' the test runner will invoke that method after each test.
        '''        
        self.assertEqual([], self.verificationErrors) 
        self.connect_instance.close()
        
        basic_airlink.slog(" Testcase complete")
        
    def set_ipsec_at(self,vpn_no):
        ''' set VPN IPSec parameters by AT commands
        Args: 
            vpn_no: integer,VPN number (1-5)
        '''
        ret = self.at_ins.set_ipsec_auth(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["IPSEC_AUTH"]["VALUE"][vpn_no-1])  #SHA1
        self.assertEqual(ret, True)
        ret = self.at_ins.set_ipsec_dh(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["IPSEC_KEY_GROUP"]["VALUE"][vpn_no-1])  # DH2
        self.assertEqual(ret, True)
        ret = self.at_ins.set_ipsec_encrypt(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["IPSEC_ENCRYPT"]["VALUE"][vpn_no-1])  #AES128
        self.assertEqual(ret, True)        
        ret = self.at_ins.set_ipsec_gateway(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["VPN_GATEWAY"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True)        
        ret = self.at_ins.set_ipsec_lifetime(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["IPSEC_SA_TIME"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True)        
        ret = self.at_ins.set_ipsec_ike_auth(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["IKE_AUTH"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True)        
        ret = self.at_ins.set_ipsec_ike_dh(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["IKE_KEY_GROUP"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True) 
        ret = self.at_ins.set_ipsec_ike_encrypt(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["IKE_ENCRYPT"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True) 
        ret = self.at_ins.set_ipsec_ike_lifetime(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["IKE_SA_TIME"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True) 
        ret = self.at_ins.set_ipsec_local_addr(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDR"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True) 
        ret = self.at_ins.set_ipsec_local_addr_mask(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDR_MASK"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True) 
        ret = self.at_ins.set_ipsec_local_addr_type(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDR_TYPE"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True) 
        # don't need to set my_id
        ret = self.at_ins.set_ipsec_local_id_type(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["MY_ID_TYPE"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True) 
        ret = self.at_ins.set_ipsec_neg_mode(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["NEG_MODE"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True) 
        ret = self.at_ins.set_ipsec_pfs(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["PFS"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True) 
        ret = self.at_ins.set_ipsec_remote_addr(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDR"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True) 
        ret = self.at_ins.set_ipsec_remote_addr_mask(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDR_MASK"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True) 
        ret = self.at_ins.set_ipsec_remote_addr_type(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDR_TYPE"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True) 
        # don't need set remote id
        ret = self.at_ins.set_ipsec_remote_id_type(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["PEER_ID_TYPE"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True) 
        ret = self.at_ins.set_ipsec_shared_key1(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["PSK1"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True)      
           
    def verify_ipsec_at(self,vpn_no):
        ''' verify VPN IPSec setting by AT commands.
        Args: 
            vpn_no: integer, VPN number (1-5)
        '''
        ret = self.at_ins.get_ipsec_tunnel_type(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["VPN_TYPE"]["VALUE"][vpn_no-1])
    
        ret = self.at_ins.get_ipsec_auth(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["IPSEC_AUTH"]["VALUE"][vpn_no-1])

        ret = self.at_ins.get_ipsec_dh(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["IPSEC_KEY_GROUP"]["VALUE"][vpn_no-1])

        ret = self.at_ins.get_ipsec_encrypt(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["IPSEC_ENCRYPT"]["VALUE"][vpn_no-1])
        
        ret = self.at_ins.get_ipsec_gateway(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["VPN_GATEWAY"]["VALUE"][vpn_no-1])
        
        ret = self.at_ins.get_ipsec_lifetime(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["IPSEC_SA_TIME"]["VALUE"][vpn_no-1])
        
        ret = self.at_ins.get_ipsec_ike_auth(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["IKE_AUTH"]["VALUE"][vpn_no-1])
        
        ret = self.at_ins.get_ipsec_ike_dh(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["IKE_KEY_GROUP"]["VALUE"][vpn_no-1])
        
        ret = self.at_ins.get_ipsec_ike_encrypt(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["IKE_ENCRYPT"]["VALUE"][vpn_no-1])
        
        ret = self.at_ins.get_ipsec_ike_lifetime(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["IKE_SA_TIME"]["VALUE"][vpn_no-1])

        ret = self.at_ins.get_ipsec_local_addr(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDR"]["VALUE"][vpn_no-1])
        
        ret = self.at_ins.get_ipsec_local_addr_mask(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDR_MASK"]["VALUE"][vpn_no-1])
        
        ret = self.at_ins.get_ipsec_local_addr_type(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDR_TYPE"]["VALUE"][vpn_no-1])
        #ALLX-4110 AT command AT*IPSEC1_LOCAL_ID and AT*REMOTE_ID not working
        my_id = self.at_ins.get_ipsec_local_id(self.connect_instance,str(vpn_no))
        net_ip= self.at_ins.get_net_ip(self.connect_instance)
        #self.assertEqual(my_id, net_ip)   
        
        ret = self.at_ins.get_ipsec_local_id_type(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["MY_ID_TYPE"]["VALUE"][vpn_no-1])
        
        ret = self.at_ins.get_ipsec_neg_mode(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["NEG_MODE"]["VALUE"][vpn_no-1])
        
        ret = self.at_ins.get_ipsec_pfs(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["PFS"]["VALUE"][vpn_no-1])
        
        ret = self.at_ins.get_ipsec_remote_addr(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDR"]["VALUE"][vpn_no-1])
        
        ret = self.at_ins.get_ipsec_remote_addr_mask(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDR_MASK"]["VALUE"][vpn_no-1])
        
        ret = self.at_ins.get_ipsec_remote_addr_type(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDR_TYPE"]["VALUE"][vpn_no-1])
        #ALLX-4110
        ret = self.at_ins.get_ipsec_remote_id(self.connect_instance,str(vpn_no))
        #self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["PEER_ID"]["VALUE"][vpn_no-1])  
        
        ret = self.at_ins.get_ipsec_remote_id_type(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["PEER_ID_TYPE"]["VALUE"][vpn_no-1])
        
        ret = self.at_ins.get_ipsec_shared_key1(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["PSK1"]["VALUE"][vpn_no-1])
        
        ret = self.at_ins.get_ipsec_status(self.connect_instance,str(vpn_no))
        self.assertEqual(ret, vpn_config_map["IPSEC_TUNNEL"]["VPN_STATUS"]["VALUE"][vpn_no-1])  

    def tc_ipsec_vpn1_commands(self):
        ''' to test VPN1 IPSec AT commands 
        '''
        
        vpn_no = 1
        #step: set VPN IPSEC parameters
        ret = self.at_ins.set_ipsec_tunnel_type(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["VPN_TYPE"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True)
        
        #step: set VPN IPSEC parameters
        self.set_ipsec_at(vpn_no)
                          
        #Step: apply and reboot
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
        
        #step: read and check VPN IPSEC parameters
        self.verify_ipsec_at(vpn_no)

        ret = self.at_ins.at_ping(self.connect_instance,"10.11.12.13")
        self.assertEqual(ret, True)  
                                                                                                         
    def tc_ipsec_vpn2_commands(self):
        ''' VPN2 ipsec AT commands 
        '''
 
        vpn_no = 2
        #step: set VPN IPSEC parameters
        ret = self.at_ins.set_ipsec_tunnel_type(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["VPN_TYPE"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True)
     
        #Step: apply and reboot
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
        
        #step: read and check VPN IPSEC parameters
        self.verify_ipsec_at(vpn_no)
        
        ret = self.at_ins.at_ping(self.connect_instance,"10.11.13.13")
        self.assertEqual(ret, True)  
        
    def tc_ipsec_vpn3_commands(self):
        ''' VPN3 IPSec AT commands 
        '''
        vpn_no = 3
        #step: set VPN IPSEC parameters
        ret = self.at_ins.set_ipsec_tunnel_type(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["VPN_TYPE"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True)
     
        #Step: apply and reboot
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
        
        #step: read and check VPN IPSEC parameters
        self.verify_ipsec_at(vpn_no)

        ret = self.at_ins.at_ping(self.connect_instance,"10.11.14.13")
        self.assertEqual(ret, True)  
        
    def tc_ipsec_vpn4_commands(self):
        ''' VPN4 IPSec AT commands 
        '''
            
        vpn_no = 4
        #step: set VPN IPSEC parameters
        ret = self.at_ins.set_ipsec_tunnel_type(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["VPN_TYPE"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True)
     
        #Step: apply and reboot
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
        
        #step: read and check VPN IPSEC parameters
        self.verify_ipsec_at(vpn_no)

        ret = self.at_ins.at_ping(self.connect_instance,"10.11.15.13")
        self.assertEqual(ret, True)  
        
    def tc_ipsec_vpn5_commands(self):
        ''' VPN5 IPSec AT commands 
        '''
            
        vpn_no = 5
        #step: set VPN IPSEC parameters
        ret = self.at_ins.set_ipsec_tunnel_type(self.connect_instance,str(vpn_no),vpn_config_map["IPSEC_TUNNEL"]["VPN_TYPE"]["VALUE"][vpn_no-1])
        self.assertEqual(ret, True)
     
        #Step: apply and reboot
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
        
        #step: read and check VPN IPSEC parameters
        self.verify_ipsec_at(vpn_no)
        
        ret = self.at_ins.at_ping(self.connect_instance,"10.11.16.13")
        self.assertEqual(ret, True)  
            
    def tc_dummy(self):
        pass                                                          