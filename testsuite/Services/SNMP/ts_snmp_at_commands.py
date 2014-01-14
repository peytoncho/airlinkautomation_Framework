################################################################################
#
# This module automates SNMP's AT commands test cases. 
# Company: Sierra Wireless
# Date: Sept 5, 2013
# Author: Airlink
# 
################################################################################

import os
import sys
import unittest

import at_utilities
import basic_airlink
import connectivity


airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")
sys.path.append(".")

basic_airlink.append_sys_path()

tbd_config_map, lan_config_map = basic_airlink.get_config_data("Services","SNMP")
        
class TsSnmpAtCommands(unittest.TestCase):
    ''' This test suite automates SNMP testcases by AT commands.
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
        
            
    def tc_snmp_v2_enable(self):
        ''' SNMP test case SNMP_v2_enable in ApTest
        '''
        connect_instance = self.connect_instance
        
        # enable SNMP feature
        ret=self.at_ins.set_snmp_enable(connect_instance,"1")
        self.assertEqual(ret, True)        
        
        #step: get/set SNMP version 2 by AT command
        ret = self.at_ins.get_snmp_version(connect_instance)
        self.assertNotEqual(ret, basic_airlink.ERR)                      
        
        ret=self.at_ins.set_snmp_version(connect_instance,"2")
        self.assertEqual(ret, True)
        
        ret = self.at_ins.get_snmp_version(connect_instance)
        if  ret.find("2",0) == -1 or ret == basic_airlink.ERR: 
            self.fail_flag +=1     
            
        self.assertEqual(self.fail_flag, 0)
 
    def tc_snmp_v3_enable(self):
        ''' SNMP test case SNMP_v3_enable in ApTest
        '''
        connect_instance = self.connect_instance
        
        # enable SNMP feature
        ret=self.at_ins.set_snmp_enable(connect_instance,"1")
        self.assertEqual(ret, True)        
        
        #step: get/set SNMP version 3 by AT command
        ret = self.at_ins.get_snmp_version(connect_instance)
        self.assertNotEqual(ret, basic_airlink.ERR)                      
        
        ret=self.at_ins.set_snmp_version(connect_instance,"3")
        self.assertEqual(ret, True)
        
        ret = self.at_ins.get_snmp_version(connect_instance)
        if  ret.find("3",0) == -1 or ret == basic_airlink.ERR: 
            self.fail_flag +=1     
            
        self.assertEqual(self.fail_flag, 0)
                                                                                                        
    def tc_snmp_v3_config(self):
        ''' SNMP test case SNMP_configuration in ApTest
        '''
        connect_instance = self.connect_instance
        
        # enable SNMP feature
        ret=self.at_ins.set_snmp_enable(connect_instance,"1")
        self.assertEqual(ret, True)        
        
        #step: get/set SNMP version 3 by AT command
        ret = self.at_ins.get_snmp_version(connect_instance)
        self.assertNotEqual(ret, basic_airlink.ERR)                      
        
        ret=self.at_ins.set_snmp_version(connect_instance,"3")
        self.assertEqual(ret, True)
        
        ret = self.at_ins.get_snmp_version(connect_instance)
        if  ret.find("3",0) == -1 or ret == basic_airlink.ERR: 
            self.fail_flag +=1     
            
        self.assertEqual(self.fail_flag, 0)
         
    def tc_dummy(self):
        self.assertEqual(self.fail_flag, 0)
                                                          