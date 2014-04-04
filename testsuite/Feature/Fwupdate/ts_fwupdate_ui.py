###############################################################################
#
# This module provides FW Update operations by UI. 
# Company: Sierra Wireless
# Time: October 15th, 2013
# 
#################################################################################
import logging
import os
import time
import unittest
import sys

from selenium.common.exceptions import NoSuchFrameException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import basic_airlink
import connectivity
import selenium_utilities
import at_utilities
import fwupdate_airlink
import ssh_airlink
import telnet_airlink

fail_flag = 0
test_area = "Fwupdate"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME']
basic_airlink.append_sys_path()
tbd_config_map, fwupdate_config_map = basic_airlink.get_config_data(test_area,"")



class TsFwupdateUi(unittest.TestCase):
    """TsFwupdateUi class provides a firmware update automation using Selenium UI test features.
    """
        
    def setUp(self):
        ''' 
        the test runner will run that method prior to each test
        
        Args: None
        
        Returns: None
        '''
        self.fw_from = fwupdate_config_map["ALEOS_BUILD_FROM"]
        self.fw_to = fwupdate_config_map["ALEOS_BUILD_TO"]
        
            
    def tearDown(self):
        ''' the test runner will invoke that method after each test
        
        Args: None
        
        Returns: None
        '''
        return
    
    def testcase_setup(self,test_way):
        if fwupdate_config_map["MDT_LOCAL"] == "YES" and test_way == "Local":
            combo_map = fwupdate_airlink.load_temp_tc_map()                       
            self.ip_postfix = combo_map["PROCESSING_INDEX"]
            dut_name = combo_map["COMBO_LIST"][int(self.ip_postfix)-1]
            basic_airlink.cslog(dut_name, "RED")                       
            self.dut_ip = "192.168.13."+str(self.ip_postfix)
            self.fw_ins = fwupdate_airlink.FwupdateAirlink(dut_name,dut_ip=self.dut_ip)
                               
        elif fwupdate_config_map["MDT_LOCAL"] == "NO" and test_way == "Local":
            self.fw_ins = fwupdate_airlink.FwupdateAirlink()
        elif test_way == "ota":
            self.dut_ip = fwupdate_config_map["OTA_IP"]
            self.fw_ins = fwupdate_airlink.FwupdateAirlink(dut_ip=self.dut_ip)

#===========================================================================
# Test Cases
#===========================================================================
    def tc_fwupdate_local_single_aleos(self):
        ''' This method will run the single update
        
        Args: None
        
        Returns: None
        '''
        self.testcase_setup("Local")       
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case:  ACEManager Firmware single upgrade ", "BLUE")        
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        result = self.fw_ins.fwupdate_ui_aleos(fw1) 
        if not "True" in result :
            self.fail("Test failed. Reason: "+result)
        else:
            basic_airlink.cslog(time.ctime(time.time())+" ===>> "+result, "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE")            
  
    def tc_fwupdate_local_roundtrip_aleos(self):
        '''  This method will run the round trip update
        
        Args: None
        
        Returns: None
        '''
        self.testcase_setup("Local")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
        
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                               
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")


    def tc_fwupdate_local_single_rm(self):
        self.testcase_setup("Local")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case:  ACEManager Firmware single upgrade ", "BLUE")        
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        result = self.fw_ins.fwupdate_ui_aleos(fw1) 
        if not "True" in result :
            self.fail("Test failed. Reason: "+result)
        else:
            basic_airlink.cslog(time.ctime(time.time())+" ===>> "+result, "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE") 
        pass
    
    def tc_fwupdate_local_roundtrip_rm(self):
        self.testcase_setup("Local")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
        
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                               
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
        pass
    
    def tc_fwupdate_ota_single_aleos(self):
        ''' This method will run the single update
        
        Args: None
        
        Returns: None
        '''
        self.testcase_setup("ota")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case:  ACEManager Firmware single upgrade ", "BLUE")        
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        result = self.fw_ins.fwupdate_ui_aleos(fw1) 
        if not "True" in result :
            self.fail("Test failed. Reason: "+result)
        else:
            basic_airlink.cslog(time.ctime(time.time())+" ===>> "+result, "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE") 
    
    def tc_fwupdate_ota_roundtrip_aleos(self):
        '''  This method will run the round trip update
        
        Args: None
        
        Returns: None
        '''
        self.testcase_setup("ota")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
        
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                               
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
  
    def tc_fwupdate_ota_single_rm(self):
        ''' This method will run the single update
        
        Args: None
        
        Returns: None
        '''
        self.testcase_setup("ota")      
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case:  ACEManager Firmware single upgrade ", "BLUE")        
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        result = self.fw_ins.fwupdate_ui_aleos(fw1) 
        if not "True" in result :
            self.fail("Test failed. Reason: "+result)
        else:
            basic_airlink.cslog(time.ctime(time.time())+" ===>> "+result, "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE") 
    
    def tc_fwupdate_ota_roundtrip_rm(self):
        '''  This method will run the round trip update
        
        Args: None
        
        Returns: None
        '''
        self.testcase_setup("ota")
        self.dut_ip = fwupdate_config_map["OTA_IP"]
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
        
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                               
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")

    def tc_fwupdate_local_sp_GX400(self):
        '''  This method will run the round trip update
        
        Args: None
        
        Returns: None
        '''
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        fw2 = fwupdate_config_map["ALEOS_BUILD_TO"]
        rm1 = fwupdate_config_map["RM_VERSION_FROM"]
        rm2 = fwupdate_config_map["RM_VERSION_TO"]      
        times_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        for round in range(times_count):
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Round: "+str(round+1)+" Started", "BLUE")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Upgrade to: "+fw2, "BLUE")
            result = self.fw_ins.fwrmupdate_ui(fw2,rm2)
            if result != "True":
                self.fail("Test failed. Reason: "+result)
            else:
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Downgrade to: "+fw1, "BLUE")
#            result = self.fw_ins.fwupdate_ui(fw1,rm1)
            result = self.fw_ins.fw_rm_update_at_command(fw1, rm1)
            if result != "True":
                self.fail("Test failed. Reason: "+result)
            else:
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Round: "+str(round+1)+" Completed", "BLUE")
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")        

    def tc_fwupdate_local_sp_LS300(self):
        #special internal function for this test case
        def remove_file():
            result = True
            attempt_conn = 1000
            ssh_ins = ssh_airlink.SshAirlink()
            cmd1 = 'cat /mnt/hda1/Altemp/UBOOT_ENV_UPDATED'
            cmd2 = 'rm /mnt/hda1/Altemp/UBOOT_ENV_UPDATED'
            while attempt_conn > 0:
                ret = ssh_ins.connect()
                if ret != True:
                    basic_airlink.cslog(time.ctime(time.time())+" ===>> SSH Connection fail", "RED")
                    attempt_conn-=1
                else:
                    break
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Run Remove file in ssh ")
            ssh_ins.command(cmd2)
            ssh_ins.close()
            return result
        
       # specific path upgrade
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
        
        result = self.fw_ins.fwupdate_ui_aleos('4.3.5.010')
        if not "True" in result :
            self.fail("Test failed. Reason: "+result)
        else:
            basic_airlink.cslog(time.ctime(time.time())+" ===>> "+result, "GREEN")
    
    #This is the template for creating ALEOS path update                  
    def tc_fwupdate_path_example(self):
        #define path in fwupdate yml file, please see fwupdate_test_conf.yml
        fw_path_lst =  fwupdate_config_map["PATH1"]     
        times_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
         
        for round in range(times_count):
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Round: "+str(round+1)+" Started", "BLUE")
            #Upgrade path
            for fw_ver in fw_path_lst:                   
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Upgrade to: "+fw_ver, "BLUE")
                result = self.fw_ins.fwupdate_ui_aleos(fw_ver)
                if not "True" in result:
                    self.fail(result)
                else:
                    basic_airlink.cslog(time.ctime(time.time())+" ===>>"+result, "GREEN")
            
            #Downgrade path, built by tester, it depense on the downgrade process
            
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Round: "+str(round+1)+" Completed", "BLUE")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE")
    
    def tc_fwupdate_custom_path_example(self):
        #This example is simulating the path:
        #4.3.4.009 -> delete UBOOT file in ALEOS linux 
        #-> do RM update only -> do ALEOS update only(4.3.5.010)
        
        #internal method for this test case
        def remove_file():
            pass
               
        #define the version, file which the test case needed.
        times_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        fw1 = "4.3.4.009"
        rm1 = "SL5011_VZW003_11301"
        fw2 = "4.3.5.010"
        
        for round in range(times_count):
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Round: "+str(round+1)+" Started", "BLUE")
            #Upgrade path
            #Step 1:
            #for this case step 1 is the downgrade step                   
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Upgrade to: "+fw1, "BLUE")
            result = self.fw_ins.fwupdate_ui_aleos(fw1)
            if not "True" in result:
                self.fail(result)
            else:
                basic_airlink.cslog(time.ctime(time.time())+" ===>>"+result, "GREEN")
            
            #Step 2:
            remove_file()

            #Step 3:
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Upgrade to: "+rm1, "BLUE")                
            result = self.fw_ins.fwupdate_ui_rm(rm1)
            if not "True" in result:
                self.fail(result)
            else:
                basic_airlink.cslog(time.ctime(time.time())+" ===>>"+result, "GREEN")
            
            #Step 4:
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Upgrade to: "+rm1, "BLUE")                
            result = self.fw_ins.fwupdate_ui_rm(rm1)
            if not "True" in result:
                self.fail(result)
            else:
                basic_airlink.cslog(time.ctime(time.time())+" ===>>"+result, "GREEN")            
            
            
            #Downgrade path, built by tester, it depense on the downgrade process
                       
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Round: "+str(round+1)+" Completed", "BLUE")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE")
        pass       
    
        
    def tc_fwupdate_GX400_MC8705_OSM(self):
        basic_airlink.cslog(self.dut_ip, "GREEN")
        basic_airlink.cslog("tc_fwupdate_GX400_MC8705_OSM", "RED")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
            
    def tc_fwupdate_GX400_MC8705_ATT(self):
        basic_airlink.cslog(self.dut_ip, "GREEN")
        basic_airlink.cslog("tc_fwupdate_GX400_MC8705_ATT", "GREEN")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
        
 