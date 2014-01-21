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


class TsFwupdateUi(unittest.TestCase):
    """TsFwupdateUi class provides a firmware update automation using Selenium UI test features.
    """
        
    def setUp(self):
        ''' 
        the test runner will run that method prior to each test
        
        Args: None
        
        Returns: None
        '''
        
        if fwupdate_config_map["MDT"] == "YES":
            
            testing_combo = fwupdate_config_map["TESTING_COMBO"]
            dut_name = fwupdate_config_map[testing_combo][ip_postfix]
            basic_airlink.cslog(dut_name, "RED")
                        
            dut_ip = "192.168.13."+str(ip_postfix)
            self.fw_ins = fwupdate_airlink.FwupdateAirlink(dut_ip,dut_name)
            self.conn_ins = connectivity.Connectivity(device_name=dut_name)
            
            
                    
        else:
            dut_name =  tbd_config_map["DUTS"][0]
            self.fw_ins = fwupdate_airlink.FwupdateAirlink(dut_name=dut_name)
            self.conn_ins = connectivity.Connectivity(device_name=dut_name)
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
        

    def tc_fwupdate_GX400_MC8705_OSM(self):
        basic_airlink.cslog(self.url, "RED")
        basic_airlink.cslog("tc_fwupdate_GX400_MC8705_OSM", "RED")
            
    def tc_fwupdate_GX400_MC8705_ATT(self):
        basic_airlink.cslog(self.url, "GREEN")
        basic_airlink.cslog("tc_fwupdate_GX400_MC8705_ATT", "GREEN")
    
    def tc_fwupdate_GX400_MC8705_BEL(self):
        basic_airlink.cslog(self.url, "BLUE")
        basic_airlink.cslog("tc_fwupdate_GX400_MC8705_BEL", "BLUE")
    
    def tc_fwupdate_GX400_MC8705_TLS(self):
        basic_airlink.cslog(self.url, "YELLOW")
        basic_airlink.cslog("tc_fwupdate_GX400_MC8705_TLS", "YELLOW")
    
    def tc_fwupdate_GX410_MC8705_OSM(self):
        basic_airlink.cslog(self.url)
        basic_airlink.cslog("tc_fwupdate_GX410_MC8705_OSM")
       
    def tc_fwupdate_GX400_MC5728_VZW(self):
        pass
    
    def tc_fwupdate_GX440_MC7750_VZW(self):
        pass
    
    def tc_fwupdate_GX440_MC7700_ATT(self):
        basic_airlink.cslog(self.url, "RED")
        basic_airlink.cslog("tc_fwupdate_GX440_MC7700_ATT", "RED")
        self.se_ins.status_about_page(self.driver)
        pass
    
    def tc_fwupdate_GX400_MC5728_SPT(self):
        pass

    def tc_fwupdate_GX440_MC7700_OSM(self):
        pass

    def tc_fwupdate_ES440_MC7750_VZW(self):
        basic_airlink.cslog(self.url, "RED")
        basic_airlink.cslog("tc_fwupdate_ES440_MC7750_VZW", "RED")
        self.se_ins.status_about_page(self.driver)
        pass
    
    def tc_fwupdate_ES440_MC7700_ATT(self):
        pass

    def tc_fwupdate_ES440_MC7710_EMEA(self):
        basic_airlink.cslog(self.url, "RED")
        basic_airlink.cslog("tc_fwupdate_ES440_MC7710_EMEA", "RED")
        self.se_ins.status_about_page(self.driver)
        pass

    def tc_fwupdate_ES440_MC7700_OSM(self):
        pass   

    def tc_fwupdate_LS300_SL5011_VZW(self):
        basic_airlink.cslog(self.url, "RED")
        basic_airlink.cslog("tc_fwupdate_LS300_SL5011_VZW", "RED")
        self.se_ins.status_about_page(self.driver)
        pass 

    def tc_fwupdate_LS300_SL5011_SPT(self):
        pass 

    def tc_fwupdate_LS300_SL8090_ATT(self):
        pass 

    def tc_fwupdate_LS300_SL8090_BEL(self):
        pass 

    def tc_fwupdate_LS300_SL8092_OSM(self):
        basic_airlink.cslog(self.url, "RED")
        basic_airlink.cslog("tc_fwupdate_LS300_SL8092_OSM", "RED")
        self.se_ins.status_about_page(self.driver)
        pass 