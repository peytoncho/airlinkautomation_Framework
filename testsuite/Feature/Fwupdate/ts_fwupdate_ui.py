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

fail_flag = 0
test_area = "Fwupdate"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME']
basic_airlink.append_sys_path()
tbd_config_map, fwupdate_config_map = basic_airlink.get_config_data(test_area,"")
device_name = tbd_config_map["DUTS"][0]



class TsFwupdateUi(unittest.TestCase):
    """TsFwupdateUi class provides a firmware update automation using Selenium UI test features.
    """
        
    def setUp(self):
        ''' 
        the test runner will run that method prior to each test
        
        Args: None
        
        Returns: None
        '''
        self.conn_ins = connectivity.Connectivity() 
        
        self.url = tbd_config_map[device_name]["ACE_URL"]
        self.username = tbd_config_map[device_name]["USERNAME"]
        self.password = tbd_config_map[device_name]["PASSWORD"]
        self.se_ins = selenium_utilities.SeleniumAcemanager()
        self.fw_ins = fwupdate_airlink.FwupdateAirlink()
        
#        check the connection between host and dut
        try:
            self.assertTrue(self.conn_ins.testbed_ready(), "DUT not Ready")
        except Exception:
            logging.debug("DUT not ready")
            basic_airlink.cslog("DUT not ready", "RED")           
            self.skipTest("DUT not ready")      
#        check the connected device if match the one set in config file
        try:
            self.assertTrue(self.fw_ins._device_check(device_name), "Device does not match the one set in config file")
        except Exception:
            logging.debug("Device does not match the one set in config file")
            basic_airlink.cslog("Device does not match the one set in config file", "RED")          
            self.skipTest("Device does not match the one set in config file")

    def tearDown(self):
        ''' the test runner will invoke that method after each test
        
        Args: None
        
        Returns: None
        '''
        return

#===========================================================================
# Test Cases
#===========================================================================
    def tc_fwupdate_local_single(self):
        ''' This method will run the single update
        
        Args: None
        
        Returns: None
        '''        
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case:  ACEManager Firmware single upgrade ", "BLUE", "YELLOW")        
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        rm1 = rm1 = fwupdate_config_map["RM_VERSION_FROM"]
        result = self.fw_ins.fwupdate_ui(fw1,rm1) 
        if result != "True":
            self.fail("Test failed. Reason: "+result)
        else:
            basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")            

        
    
    def tc_fwupdate_local_roundtrip(self):
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
            result = self.fw_ins.fwupdate_ui(fw2)
            if result != "True":
                self.fail("Test failed. Reason: "+result)
            else:
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Downgrade to: "+fw1, "BLUE")
            result = self.fw_ins.fwupdate_ui(fw1)
            if result != "True":
                self.fail("Test failed. Reason: "+result)
            else:
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Round: "+str(round+1)+" Completed", "BLUE")
                              
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
        
        
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        fw2 = fwupdate_config_map["ALEOS_BUILD_TO"]       
        times_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        for round in range(times_count):
            
            remove_file()
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Round: "+str(round+1)+" Started", "BLUE")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Upgrade to: "+fw2, "BLUE")
            result = self.fw_ins.fwupdate_ui(fw2)
            if result != "True":
                self.fail("Test failed. Reason: "+result)
            else:
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Downgrade to: "+fw1, "BLUE")
            remove_file()
            result = self.fw_ins.fwupdate_ui(fw1)
            if result != "True":
                self.fail("Test failed. Reason: "+result)
            else:
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Round: "+str(round+1)+" Completed", "BLUE")
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")        
        


    @unittest.skipIf(tbd_config_map[device_name]["MODEL"]=="LS300","Not support this device")
    def tc_fwupdate_local_432009_432a010I(self):
        ''' Update from 4.3.2.009 to 4.3.2a.010-I
        
        Args: None
        
        Returns: None
        '''
        fw1 = '4.3.2.009'
        fw2 = '4.3.2a.010-I'
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware upgrade from "+fw1+" to "+fw2, "BLUE", "YELLOW")      
        self.local_fwupdate_from_to(fw2, fw1)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
    
    @unittest.skipIf(tbd_config_map[device_name]["MODEL"]=="LS300","Not support this device")    
    def tc_fwupdate_local_432a010I_433014(self):
        ''' Update from 4.3.2a.010-I to 4.3.3.014
        
        Args: None
        
        Returns: None
        '''
        fw1 = '4.3.2a.010-I'
        fw2 = '4.3.3.014'
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware upgrade from "+fw1+" to "+fw2, "BLUE", "YELLOW")
        self.local_fw_update(fw2)
        self.assertEqual(self.aleos_verify(self.aleos_check(), fw2), True, "Fw update Failed")
        basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")      
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
    
    @unittest.skipIf(tbd_config_map[device_name]["MODEL"]=="LS300","Not support this device")
    def tc_fwupdate_local_432a010_432a010I(self):
        ''' Update from 4.3.2a.010 to 4.3.2a.010-I
        
        Args: None
        
        Returns: None
        '''
        fw1 = '4.3.2a.010'
        fw2 = '4.3.2a.010-I'
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware upgrade from "+fw1+" to "+fw2, "BLUE", "YELLOW")      
        self.local_fwupdate_from_to(fw2, fw1)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
    
    @unittest.skipIf(tbd_config_map[device_name]["MODEL"]=="LS300","Not support this device")
    def tc_fwupdate_local_432a010I_434009(self):
        ''' Update from 4.3.2a.010-I to 4.3.4.009
        
        Args: None
        
        Returns: None
        '''
        fw1 = '4.3.2a.010-I'
        fw2 = '4.3.4.009'
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware upgrade from "+fw1+" to "+fw2, "BLUE", "YELLOW")
        self.local_fw_update(fw2)
        self.assertEqual(self.aleos_verify(self.aleos_check(), fw2), True, "Fw update Failed")
        basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")      
#         self.local_fwupdate_from_to(fw2, fw1)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
        
    def tc_fwupdate_local_432009_433014(self):
        ''' Update from 4.3.2.009 to 4.3.3.014
        
        Args: None
        
        Returns: None
        '''
        fw1 = '4.3.2.009'
        fw2 = '4.3.3.014'
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware upgrade from "+fw1+" to "+fw2, "BLUE", "YELLOW")       
        self.local_fwupdate_from_to(fw2, fw1)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
    
    def tc_fwupdate_local_432009_433a014(self):
        ''' Update from 4.3.2.009 to 4.3.3a.014
        
        Args: None
        
        Returns: None
        '''
        fw1 = '4.3.2.009'
        fw2 = '4.3.3a.014'
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware upgrade from "+fw1+" to "+fw2, "BLUE", "YELLOW")       
        self.local_fwupdate_from_to(fw2, fw1)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
    
    @unittest.skipIf(tbd_config_map[device_name]["MODEL"]=="LS300","Not support this device")
    def tc_fwupdate_local_432a010_433014(self):
        ''' Update from 4.3.2a.010 to 4.3.3.014
        
        Args: None
        
        Returns: None
        '''
        fw1 = '4.3.2a.010'
        fw2 = '4.3.3.014'
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware upgrade from "+fw1+" to "+fw2, "BLUE", "YELLOW")       
        self.local_fwupdate_from_to(fw2, fw1)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
    
    @unittest.skipIf(tbd_config_map[device_name]["MODEL"]=="LS300","Not support this device")
    def tc_fwupdate_local_432a010_433a014(self):
        ''' Update from 4.3.2a.010 to 4.3.3a.014
        
        Args: None
        
        Returns: None
        '''
        fw1 = '4.3.2a.010'
        fw2 = '4.3.3a.014'
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware upgrade from "+fw1+" to "+fw2, "BLUE", "YELLOW")       
        self.local_fwupdate_from_to(fw2, fw1)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")

    @unittest.skipIf(tbd_config_map[device_name]["MODEL"]=="LS300","Not support this device")
    def tc_fwupdate_local_432a010_434009(self):
        ''' Update from 4.3.2a.010 to 4.3.4.009
        
        Args: None
        
        Returns: None
        '''
        fw1 = '4.3.2a.010'
        fw2 = '4.3.4.009'
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware upgrade from "+fw1+" to "+fw2, "BLUE", "YELLOW")       
        self.local_fwupdate_from_to(fw2, fw1)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")       
                       
    
    def tc_fwupdate_local_433a014_434009(self):
        ''' Update from 4.3.3a.014 to 4.3.4.009
        
        Args: None
        
        Returns: None
        '''
        fw1 = '4.3.3a.014'
        fw2 = '4.3.4.009'
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware upgrade from "+fw1+" to "+fw2, "BLUE", "YELLOW")       
        self.local_fwupdate_from_to(fw2, fw1)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
    
        
    def tc_fwupdate_local_433014_434009(self):
        ''' Update from 4.3.3.014 to 4.3.4.009
        
        Args: None
        
        Returns: None
        '''       
        fw1 = '4.3.3.014'
        fw2 = '4.3.4.009'
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware upgrade from "+fw1+" to "+fw2, "BLUE", "YELLOW")       
        self.local_fwupdate_from_to(fw2, fw1)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
        
    
    def tc_fwupdate_local_434008_434009(self):
        ''' Update from 4.3.4.008 to 4.3.4.009
        
        Args: None
        
        Returns: None
        '''
        fw1 = '4.3.4.008'
        fw2 = '4.3.4.009'
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware upgrade from "+fw1+" to "+fw2, "BLUE", "YELLOW")       
        self.local_fwupdate_from_to(fw2, fw1)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
        
 