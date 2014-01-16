################################################################################
#
# This module automates WAN's AT commands test cases. 
# Company: Sierra Wireless
# Date: Oct 3, 2013
# Author: Airlink
# 
################################################################################

import unittest
import sys
import os

airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")
sys.path.append(".")

import basic_airlink
basic_airlink.append_sys_path()
import at_utilities
import connectivity

tbd_config_map, wan_config_map = basic_airlink.get_config_data("WAN","")          
   
class TsWanAtCommands(unittest.TestCase):
    ''' This test suite automates WAN testcases by AT commands.
    Please make sure testbed (DUT,X-card, connection, configuration) ready 
    before run any test.
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
        ''' the test runner will invoke that method after each test
        Args: None
        Returns: None
        '''        
        self.assertEqual([], self.verificationErrors) 
        self.connect_instance.close()
        
        basic_airlink.slog(" Testcase complete")

    def tc_cdma_autoprl_and_autoprlfreq(self):
        ''' In ApTest test case Feature/WAN_Celluar/AT_Commands/AUTOPRL_and_AUTPPRLFREQ
        this is for CDMA serial device only
        '''
        if tbd_config_map[self.device_name]["RM_TYPE"] in ["MC7750","MC5728","SL5011"]:

            temp =self.at_ins.get_auto_prl_flag(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1  
    
            ret = self.at_ins.set_auto_prl_flag(self.connect_instance,"0")
            if not ret:
                self.fail_flag +=1
    
            ret = self.at_ins.set_auto_prl_flag(self.connect_instance,"1")
            if not ret:
                self.fail_flag +=1
                                        
            volt =self.at_ins.get_auto_prl_frequency(self.connect_instance) 
            if volt == basic_airlink.ERR:
                self.fail_flag +=1  
     
            ret = self.at_ins.set_auto_prl_frequency(self.connect_instance,"10")
            if not ret:
                self.fail_flag +=1  
     
            volt =self.at_ins.get_auto_prl_frequency(self.connect_instance) 
            if volt == basic_airlink.ERR:
                self.fail_flag +=1  
        else:
            basic_airlink.slog("this is for CDMA serial device only!")
                                              
        self.assertEqual(self.fail_flag, 0)  
 
    def tc_gsm_band(self):
        ''' In ApTest test case Feature/WAN_Celluar/AT_Commands/BAND
        this is for GSM serial device only
        '''
        
        if tbd_config_map[self.device_name]["RM_TYPE"] in ["MC7710","MC7700","MC8705", "SL8090", "SL8091"]:

            temp =self.at_ins.get_band(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1  
    
            ret = self.at_ins.set_for_band(self.connect_instance,"02")
            if not ret:
                self.fail_flag +=1
    
            temp =self.at_ins.get_for_band(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1 

        else:
            basic_airlink.slog("this is for GSM serial device only!")
                                                                  
        self.assertEqual(self.fail_flag, 0) 

    def tc_diversity_commands(self):
        ''' In ApTest test case Feature/WAN_Celluar/AT_Commands/diversity_commands
        '''
        if tbd_config_map[self.device_name]["RM_TYPE"] in ["MC7750","MC5728","SL5011"]:
            temp =self.at_ins.get_evdo_diversity(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1  
    
            ret = self.at_ins.set_evdo_diversity(self.connect_instance,"0")
            if not ret:
                self.fail_flag +=1
    
            temp =self.at_ins.get_evdo_diversity(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1 

            ret = self.at_ins.set_evdo_diversity(self.connect_instance,"1")
            if not ret:
                self.fail_flag +=1
    
            temp =self.at_ins.get_evdo_diversity(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1 
                
        elif tbd_config_map[self.device_name]["RM_TYPE"] in ["MC7710","MC7700","MC8705", "SL8090", "SL8091"]:
            temp =self.at_ins.get_hspa_diversity(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1  
    
            ret = self.at_ins.set_hspa_diversity(self.connect_instance,"0")
            if not ret:
                self.fail_flag +=1
    
            temp =self.at_ins.get_hspa_diversity(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1 

            ret = self.at_ins.set_hspa_diversity(self.connect_instance,"1")
            if not ret:
                self.fail_flag +=1
    
            temp =self.at_ins.get_hspa_diversity(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1 

        else:
            basic_airlink.slog("this Radio module type is incorrect!")
                                                                                                 
        self.assertEqual(self.fail_flag, 0) 

    def tc_evdo_data_service(self):
        ''' In ApTest test case Feature/WAN_Celluar/AT_Commands/evdodataserv
        this is for CDMA serial device only
        '''
        
        basic_airlink.slog("this is for CDMA device only!")
       
        if tbd_config_map[self.device_name]["RM_TYPE"] in ["MC7750","MC5728","SL5011"]:

            temp =self.at_ins.get_evdo_data_service(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1  
    
            ret = self.at_ins.set_evdo_data_service(self.connect_instance,"0")
            if not ret:
                self.fail_flag +=1
 
            temp =self.at_ins.get_evdo_data_service(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1  

        if tbd_config_map[self.device_name]["RM_TYPE"] in ["MC5728","SL5011"]:

            temp =self.at_ins.get_evdo_data_service(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1  
    
            ret = self.at_ins.set_evdo_data_service(self.connect_instance,"1")
            if not ret:
                self.fail_flag +=1
 
            temp =self.at_ins.get_evdo_data_service(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1  
                                   
            ret = self.at_ins.set_evdo_data_service(self.connect_instance,"2")
            if not ret:
                self.fail_flag +=1
 
            temp =self.at_ins.get_evdo_data_service(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1  

        if tbd_config_map[self.device_name]["RM_TYPE"] in ["MC7750"]:

            temp =self.at_ins.get_evdo_data_service(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1  
    
            ret = self.at_ins.set_evdo_data_service(self.connect_instance,"3")
            if not ret:
                self.fail_flag +=1
 
            temp =self.at_ins.get_evdo_data_service(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1  
                                   
            ret = self.at_ins.set_evdo_data_service(self.connect_instance,"4")
            if not ret:
                self.fail_flag +=1
 
            temp =self.at_ins.get_evdo_data_service(self.connect_instance) 
            if temp == basic_airlink.ERR:
                self.fail_flag +=1                                                         
                                              
        self.assertEqual(self.fail_flag, 0)  
                                        
    def tc_evdo_roam_pref(self):
        '''TODO '''
                    
        self.assertEqual(self.fail_flag, 0)
        
    def tc_lte_signal_commands(self):
        '''TODO '''
                    
        self.assertEqual(self.fail_flag, 0)
        
    def tc_net_allow_zero_ip(self):
        '''TODO '''
                    
        self.assertEqual(self.fail_flag, 0)
        
    def tc_net_apn(self):
        '''TODO '''
                    
        self.assertEqual(self.fail_flag, 0)

    def tc_net_watch_dog(self):
        '''TODO '''
                    
        self.assertEqual(self.fail_flag, 0)
        
    def tc_username_password(self):
        '''TODO '''
                    
        self.assertEqual(self.fail_flag, 0)