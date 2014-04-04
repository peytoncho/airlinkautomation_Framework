import os
import time
import shutil
import unittest
import logging
import at_utilities
import basic_airlink
import connectivity
import fwupdate_airlink

test_area = "Fwupdate"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME']
basic_airlink.append_sys_path()
tbd_config_map, fwupdate_config_map = basic_airlink.get_config_data(test_area,"")
device_name = tbd_config_map["DUTS"][0]

class TsFwupdateAtCommands(unittest.TestCase):
    """TsFwupdateAtCommands class provides a firmware update automation using At Command test features.
    """
        
    def setUp(self):
        ''' the test runner will run that method prior to each test
        
        Args: None
        
        Returns: None
        '''   
        self.at_ins = at_utilities.AtCommands()
        self.fw_ins = fwupdate_airlink.FwupdateAirlink()  
        # step: check if devices ready   
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Step: Check if testbed is ready")
                
    def tearDown(self):
        ''' the test runner will invoke that method after each test
        
        Args: None
        
        Returns: None
        ''' 
        return
    
#===============================================================================
# Test cases
#===============================================================================
    def tc_fwupdate_local_single_aleos(self):        
        ''' This method will run the single update using At Command
        The firmware version to be updated is read from "fwupdate_test_conf.yml" with label "ALEOS_BUILD_TO"  
        
        Args: None
        
        Returns: None
        '''
        update_fw_version = fwupdate_config_map["ALEOS_BUILD_TO"]
        basic_airlink.cslog(time.ctime(time.time())+\
                            " ===>> Test Case: At Command Firmware upgrade to "+\
                            update_fw_version, "BLUE", "YELLOW")
        result = self.fw_ins.fw_update_at_command(update_fw_version)
        if result == "False":
            self.fail("FW update is not successfully")
        else:
            basic_airlink.clog(time.ctime(time.time())+\
                               " ===>> Firmware version Verify: Pass", "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> Test case Completed", "BLUE", "YELLOW")
    
    def tc_fwupdate_local_single_rm(self):
        ''' This method will run the single update using At Command
        The Radio Module version to be updated is read from "fwupdate_test_conf.yml" with label RM_VERSION 
        
        Args: None
        
        Returns: None
        '''
        update_rm_version = fwupdate_config_map["RM_TO"]
        basic_airlink.cslog(time.ctime(time.time())+\
                            " ===>> Test Case: At Command Radio Module upgrade to "+\
                            update_rm_version, "BLUE", "YELLOW")
        result = self.fw_ins.rm_update_at_command(update_rm_version)
        if result == False:
            self.fail("RM update is not successfully")
        elif "failed" in result:
            self.fail(result)
        else:
            basic_airlink.cslog(time.ctime(time.time())+\
                               " ===>> Firmware version Verify: Pass", "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> Test case Completed", "BLUE", "YELLOW")

    def tc_fwupdate_local_single_aleos_rm(self):
        ''' This method will run the single update using At Command
        The firmware and Radio Module version to be updated is read from "fwupdate_test_conf.yml" with label RM_VERSION 
        
        Args: None
        
        Returns: None
        '''
        update_fw_version = fwupdate_config_map["ALEOS_BUILD_TO"]
        update_rm_version = fwupdate_config_map["RM_TO"]
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test Case: At Command Firmware and Radio Module upgrade to "+update_fw_version+" and "+update_rm_version, "BLUE", "YELLOW")
        result = self.fw_ins.fw_rm_update_at_command(update_fw_version, update_rm_version)
        if result == "False":
            self.fail("FW and RM update is not successfully")
        else:
            basic_airlink.clog(time.ctime(time.time())+\
                               " ===>> Firmware and Radio module version Verify: Pass", "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> Test case Completed", "BLUE", "YELLOW")
        pass
        
    
    def tc_fwupdate_local_roundtrip_aleos(self):
        ''' This test case method will repeat the firmware update as round trip. 
        
        Args: None
        
        Returns: None
        '''
        round_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        fw2 = fwupdate_config_map["ALEOS_BUILD_TO"]
        for i in range(1,round_count+1):           
            basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ round trip count:" + str(i)+ " ====================", "BLUE")
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_TO"]
            result = self.fw_ins.fw_update_at_command(update_fw_version)
            if result == "False":
                self.fail("test failed")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_FROM"]
            result = self.fw_ins.fw_update_at_command(update_fw_version)
            if result == "False":
                self.fail("test failed")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")            
            
            basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ round" + str(i)+ " Completed====================", "BLUE")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ Test Completed====================")
    
 
    def tc_fwupdate_local_roundtrip_rm(self):
        ''' This test case method will repeat the firmware update as round trip. 
        
        Args: None
        
        Returns: None
        '''
        round_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        fw2 = fwupdate_config_map["ALEOS_BUILD_TO"]
                      
        for i in range(1,round_count+1):           
            basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ round trip count:" + str(i)+ " ====================", "BLUE")
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_TO"]
            result = self.fw_ins.rm_update_at_command(update_fw_version)
            if result == "False":
                self.fail("test failed")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_FROM"]
            result = self.fw_ins.rm_update_at_command(update_fw_version)
            if result == "False":
                self.fail("test failed")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")            
            
            basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ round" + str(i)+ " Completed====================", "BLUE")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ Test Completed====================")
    
    
    def tc_fwupdate_local_roundtrip_aleos_rm(self):
        ''' This test case method will repeat the firmware update as round trip. 
        
        Args: None
        
        Returns: None
        '''
        round_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        fw2 = fwupdate_config_map["ALEOS_BUILD_TO"]
                      
        for i in range(1,round_count+1):           
            basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ round trip count:" + str(i)+ " ====================", "BLUE")
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_TO"]
            result = self.fw_ins.rm_update_at_command(update_fw_version)
            if result == "False":
                self.fail("test failed")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_FROM"]
            result = self.fw_ins.rm_update_at_command(update_fw_version)
            if result == "False":
                self.fail("test failed")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")            
            
            basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ round" + str(i)+ " Completed====================", "BLUE")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ Test Completed====================")
    
    
    def tc_fwupdate_ota_single_aleos(self):
        ''' This method will run the single update using At Command
        The firmware version to be updated is read from "fwupdate_test_conf.yml" with label "ALEOS_BUILD_TO"  
        
        Args: None
        
        Returns: None
        '''
        update_fw_version = fwupdate_config_map["ALEOS_BUILD_TO"]
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test Case: At Command Firmware upgrade to "+update_fw_version, "BLUE", "YELLOW")
        result = self.fw_ins.fw_update_at_command(update_fw_version)
        if result == "False":
            self.fail("FW update is not successfully")
        else:
            basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
    
    def tc_fwupdate_ota_single_rm(self):
        ''' This method will run the single update using At Command
        The Radio Module version to be updated is read from "fwupdate_test_conf.yml" with label RM_VERSION 
        
        Args: None
        
        Returns: None
        '''
        update_rm_version = fwupdate_config_map["RM_VERSION"]
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test Case: At Command Radio Module upgrade to "+update_rm_version, "BLUE", "YELLOW")
        result = self.fw_ins.rm_update_at_command(update_rm_version)
        if result == False:
            self.fail("RM update is not successfully")
        elif "failed" in result:
            self.fail(result)
        else:
            basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
    
    def tc_fwupdate_ota_single_aleos_rm(self):
        ''' This method will run the single update using At Command
        The Radio Module version to be updated is read from "fwupdate_test_conf.yml" with label RM_VERSION 
        
        Args: None
        
        Returns: None
        '''
        update_rm_version = fwupdate_config_map["RM_VERSION"]
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test Case: At Command Radio Module upgrade to "+update_rm_version, "BLUE", "YELLOW")
        result = self.fw_ins.fw_rm_update_at_command(update_rm_version)
        if result == False:
            self.fail("RM update is not successfully")
        elif "failed" in result:
            self.fail(result)
        else:
            basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE", "YELLOW")
    
    def tc_fwupdate_ota_roundtrip_aleos(self):
        ''' This test case method will repeat the firmware update as round trip. 
        
        Args: None
        
        Returns: None
        '''
        round_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        fw2 = fwupdate_config_map["ALEOS_BUILD_TO"]
                      
        for i in range(1,round_count+1):           
            basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ round trip count:" + str(i)+ " ====================", "BLUE")
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_TO"]
            result = self.fw_ins.fw_update_at_command(update_fw_version)
            if result == "False":
                self.fail("test failed")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_FROM"]
            result = self.fw_ins.fw_update_at_command(update_fw_version)
            if result == "False":
                self.fail("test failed")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")            
            
            basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ round" + str(i)+ " Completed====================", "BLUE")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ Test Completed====================")
    
    
    def tc_fwupdate_ota_roundtrip_rm(self):
        ''' This test case method will repeat the firmware update as round trip. 
        
        Args: None
        
        Returns: None
        '''
        round_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        fw2 = fwupdate_config_map["ALEOS_BUILD_TO"]
                      
        for i in range(1,round_count+1):           
            basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ round trip count:" + str(i)+ " ====================", "BLUE")
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_TO"]
            result = self.fw_ins.fw_update_at_command(update_fw_version)
            if result == "False":
                self.fail("test failed")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_FROM"]
            result = self.fw_ins.fw_update_at_command(update_fw_version)
            if result == "False":
                self.fail("test failed")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")            
            
            basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ round" + str(i)+ " Completed====================", "BLUE")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ Test Completed====================")
    
    
    def tc_fwupdate_ota_roundtrip_aleos_rm(self):
        ''' This test case method will repeat the firmware update as round trip. 
        
        Args: None
        
        Returns: None
        '''
        round_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        fw2 = fwupdate_config_map["ALEOS_BUILD_TO"]
                      
        for i in range(1,round_count+1):           
            basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ round trip count:" + str(i)+ " ====================", "BLUE")
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_TO"]
            result = self.fw_ins.fw_update_at_command(update_fw_version)
            if result == "False":
                self.fail("test failed")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_FROM"]
            result = self.fw_ins.fw_update_at_command(update_fw_version)
            if result == "False":
                self.fail("test failed")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")            
            
            basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ round" + str(i)+ " Completed====================", "BLUE")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ Test Completed====================")
                  

    

        