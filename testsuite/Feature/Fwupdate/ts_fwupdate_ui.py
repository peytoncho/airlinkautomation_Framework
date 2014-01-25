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

ip_postfix = 1
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
        
        if fwupdate_config_map["MDT"] == "YES":
            
            testing_combo = fwupdate_config_map["TESTING_COMBO"]
            dut_name = fwupdate_config_map[testing_combo][ip_postfix-1]
            basic_airlink.cslog(dut_name, "RED")
                        
            self.dut_ip = "192.168.13."+str(ip_postfix)
            self.fw_ins = fwupdate_airlink.FwupdateAirlink(dut_name,self.dut_ip)
            self.conn_ins = connectivity.Connectivity(dut_name)
            basic_airlink.cslog("Ping to "+self.dut_ip, "BLUE")
            self.assertTrue(self.conn_ins.dut_ready(self.dut_ip), self.dut_ip+" DUT not Ready")
                               
        else:
            dut_name =  tbd_config_map["DUTS"][0]
            self.fw_ins = fwupdate_airlink.FwupdateAirlink(dut_name)
            self.conn_ins = connectivity.Connectivity(dut_name)
            #        check the connection between host and dut
#            try:
            self.assertTrue(self.conn_ins.testbed_ready(), "DUT not Ready")
            self.assertTrue(self.fw_ins._device_check(), "Device does not match the one set in config file")
    
    def tearDown(self):
        ''' the test runner will invoke that method after each test
        
        Args: None
        
        Returns: None
        '''
        if fwupdate_config_map["MDT"] == "YES":
            global ip_postfix
            ip_postfix+=1
        return

#===========================================================================
# Test Cases
#===========================================================================
    def tc_fwupdate_local_single(self):
        ''' This method will run the single update
        
        Args: None
        
        Returns: None
        '''        
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case:  ACEManager Firmware single upgrade ", "BLUE")        
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        result = self.fw_ins.fwupdate_ui(fw1) 
        if not "True" in result :
            self.fail("Test failed. Reason: "+result)
        else:
            basic_airlink.clog(time.ctime(time.time())+" ===>> "+result, "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE")            

    
    def tc_fwupdate_local_roundtrip(self):
        '''  This method will run the round trip update
        
        Args: None
        
        Returns: None
        '''
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
        
    
    def tc_fwupdate_GX400_MC8705_BEL(self):
        basic_airlink.cslog(self.dut_ip, "BLUE")
        basic_airlink.cslog("tc_fwupdate_GX400_MC8705_BEL", "BLUE")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
    
    def tc_fwupdate_GX400_MC8705_TLS(self):
        basic_airlink.cslog(self.dut_ip, "YELLOW")
        basic_airlink.cslog("tc_fwupdate_GX400_MC8705_TLS", "YELLOW")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
    
    def tc_fwupdate_GX410_MC8705_OSM(self):
        basic_airlink.cslog(self.dut_ip)
        basic_airlink.cslog("tc_fwupdate_GX410_MC8705_OSM")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
       
    def tc_fwupdate_GX400_MC5728_VZW(self):
        basic_airlink.cslog(self.dut_ip)
        basic_airlink.cslog("tc_fwupdate_GX400_MC5728_VZW", "RED")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
    
    def tc_fwupdate_GX440_MC7750_VZW(self):
        basic_airlink.cslog(self.dut_ip)
        basic_airlink.cslog("tc_fwupdate_GX440_MC7750_VZW", "RED")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
    
    def tc_fwupdate_GX440_MC7700_ATT(self):
        basic_airlink.cslog(self.dut_ip, "RED")
        basic_airlink.cslog("tc_fwupdate_GX440_MC7700_ATT", "RED")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
    
    def tc_fwupdate_GX400_MC5728_SPT(self):
        basic_airlink.cslog(self.dut_ip, "RED")
        basic_airlink.cslog("tc_fwupdate_GX400_MC5728_SPT", "RED")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")

    def tc_fwupdate_GX440_MC7700_OSM(self):
        basic_airlink.cslog(self.dut_ip, "RED")
        basic_airlink.cslog("tc_fwupdate_GX440_MC7700_OSM", "RED")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")

    def tc_fwupdate_ES440_MC7750_VZW(self):
        basic_airlink.cslog(self.dut_ip, "RED")
        basic_airlink.cslog("tc_fwupdate_ES440_MC7750_VZW", "RED")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
    
    def tc_fwupdate_ES440_MC7700_ATT(self):
        basic_airlink.cslog(self.dut_ip, "RED")
        basic_airlink.cslog("tc_fwupdate_ES440_MC7700_ATT", "RED")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")

    def tc_fwupdate_ES440_MC7710_EMEA(self):
        basic_airlink.cslog(self.dut_ip, "RED")
        basic_airlink.cslog("tc_fwupdate_ES440_MC7710_EMEA", "RED")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")

    def tc_fwupdate_ES440_MC7700_OSM(self):
        basic_airlink.cslog(self.dut_ip, "RED")
        basic_airlink.cslog("tc_fwupdate_ES440_MC7700_OSM", "RED")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")   

    def tc_fwupdate_LS300_SL5011_VZW(self):
        basic_airlink.cslog(self.dut_ip, "RED")
        basic_airlink.cslog("tc_fwupdate_LS300_SL5011_VZW", "RED")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")

    def tc_fwupdate_LS300_SL5011_SPT(self):
        basic_airlink.cslog(self.dut_ip, "RED")
        basic_airlink.cslog("tc_fwupdate_LS300_SL5011_SPT", "RED")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")

    def tc_fwupdate_LS300_SL8090_ATT(self):
        basic_airlink.cslog(self.dut_ip, "RED")
        basic_airlink.cslog("tc_fwupdate_LS300_SL8090_ATT", "RED")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")

    def tc_fwupdate_LS300_SL8090_BEL(self):
        basic_airlink.cslog(self.dut_ip, "RED")
        basic_airlink.cslog("tc_fwupdate_LS300_SL8090_BEL", "RED")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
 

    def tc_fwupdate_LS300_SL8092_OSM(self):
        basic_airlink.cslog(self.dut_ip, "RED")
        basic_airlink.cslog("tc_fwupdate_LS300_SL8092_OSM", "RED")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case: ACEManager Firmware Roundtrip upgrade ", "BLUE", "YELLOW")      
       
        self.fw_ins.fwrmupdate_ui_roundtrip(self.fw_from, self.fw_to)
                              
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")

        pass 