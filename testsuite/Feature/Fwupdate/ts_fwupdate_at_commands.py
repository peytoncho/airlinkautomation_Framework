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
        '''   
        self.at_ins = at_utilities.AtCommands()  
                
    def tearDown(self):
        ''' the test runner will invoke that method after each test
        '''
        basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ Test Completed====================")
    
    def testcase_setup(self,test_way):
        #if the MDT is ON, the file, temp_fwupdate_tc_info.yml will record the list of device 
        #and the device index that currently under testing
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
    
#===============================================================================
# Test cases
#===============================================================================
    def tc_fwupdate_local_single_aleos(self):        
        ''' This method will run the single update using At Command
        The firmware version to be updated is read from "fwupdate_test_conf.yml" with label "ALEOS_BUILD_TO"  
        '''
        self.testcase_setup('Local')
        update_fw_version = fwupdate_config_map["ALEOS_BUILD_TO"]
        basic_airlink.cslog(time.ctime(time.time())+\
                            " ===>> Test Case: At Command Firmware upgrade to "+\
                            update_fw_version, "BLUE")
        result = self.fw_ins.fw_update_at_command(update_fw_version)
        if not result:
            self.fail("FW update is not successfully")
        else:
            basic_airlink.clog(time.ctime(time.time())+\
                               " ===>> Firmware version Verify: Pass", "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> Test case Completed", "BLUE")
    
    def tc_fwupdate_local_single_rm(self):
        ''' This method will run the single update using At Command
        The Radio Module version to be updated is read from "fwupdate_test_conf.yml" with label RM_VERSION 
        '''
        self.testcase_setup('Local')
        update_rm_version = fwupdate_config_map["RM_TO"]
        basic_airlink.cslog(time.ctime(time.time())+\
                            " ===>> Test Case: At Command Radio Module upgrade to "+\
                            update_rm_version, "BLUE")
        result = self.fw_ins.rm_update_at_command(update_rm_version)
        if not result:
            self.fail("RM update is not successfully")
        else:
            basic_airlink.cslog(time.ctime(time.time())+\
                               " ===>> Firmware version Verify: Pass", "GREEN")

    def tc_fwupdate_local_single_aleos_rm(self):
        ''' This method will run the single update using At Command
        The firmware and Radio Module version to be updated is read from "fwupdate_test_conf.yml" with label RM_VERSION 
        '''
        self.testcase_setup('Local')
        update_fw_version = fwupdate_config_map["ALEOS_BUILD_TO"]
        update_rm_version = self.fw_ins._match_rm(update_fw_version)
        basic_airlink.cslog(time.ctime(time.time())+\
                            "===>> Test Case: At Command Firmware and Radio Module upgrade to "+update_fw_version+" and "+update_rm_version, "BLUE")
        result = self.fw_ins.fw_rm_update_at_command(update_fw_version, update_rm_version)
        if not result:
            self.fail("FW and RM update is not successfully")
        else:
            basic_airlink.clog(time.ctime(time.time())+\
                               " ===>> Firmware and Radio module version Verify: Pass", "GREEN")
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> Test case Completed", "BLUE")
        
    
    def tc_fwupdate_local_roundtrip_aleos(self):
        ''' This test case method will repeat the firmware update as round trip. 
        '''
        self.testcase_setup('Local')
        round_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        fw2 = fwupdate_config_map["ALEOS_BUILD_TO"]
        for i in range(1,round_count+1):           
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> ============ round trip count:" + str(i)+ " ====================", "BLUE")
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_TO"]
            result = self.fw_ins.fw_update_at_command(update_fw_version)
            if not result:
                self.fail("FW update is not successfully")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_FROM"]
            result = self.fw_ins.fw_update_at_command(update_fw_version)
            if not result:
                self.fail("FW update is not successfully")
            else:
                basic_airlink.clog(time.ctime(time.time())+\
                                   " ===>> Firmware version Verify: Pass", "GREEN")            
            
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> ============ round" + str(i)+ " Completed====================", "BLUE")


    def tc_fwupdate_local_roundtrip_rm(self):
        ''' This test case method will repeat the firmware update as round trip. 
        '''
        self.testcase_setup('Local')
        round_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        rm1 = fwupdate_config_map["RM_FROM"]
        rm2 = fwupdate_config_map["RM_TO"]
                      
        for i in range(1,round_count+1):           
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> ============ round trip count:" + str(i)+ " ====================", "BLUE")

            result = self.fw_ins.rm_update_at_command(rm2)
            if not result:
                self.fail("RM update is not successfully")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            
            result = self.fw_ins.rm_update_at_command(rm1)
            if not result:
                self.fail("RM update is not successfully")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")            
            
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> ============ round" + str(i)+ " Completed====================", "BLUE")
       
    def tc_fwupdate_local_roundtrip_aleos_rm(self):
        ''' This test case method will repeat the firmware update as round trip. 
        '''
        self.testcase_setup('Local')
        round_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"] 
        fw2 = fwupdate_config_map["ALEOS_BUILD_TO"]
        
        rm1 = self.fw_ins._match_rm(fw1)
        rm2 = self.fw_ins._match_rm(fw2)
                      
        for i in range(1,round_count+1):           
            basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ round trip count:" + str(i)+ " ====================", "BLUE")
            result = self.fw_ins.fw_rm_update_at_command(fw2,rm2)
            if not result:
                self.fail("FW and RM update is not successfully")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            
            result = self.fw_ins.fw_rm_update_at_command(fw1,rm1)
            if not result:
                self.fail("FW and RM update is not successfully")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")            
            
            basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ round" + str(i)+ " Completed====================", "BLUE")
       
    def tc_fwupdate_ota_single_aleos(self):
        ''' This method will run the single update using At Command
        The firmware version to be updated is read from "fwupdate_test_conf.yml" with label "ALEOS_BUILD_TO"  
        '''
        self.testcase_setup('ota')
        update_fw_version = fwupdate_config_map["ALEOS_BUILD_TO"]
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test Case: At Command Firmware upgrade to "+update_fw_version, "BLUE", "YELLOW")
        result = self.fw_ins.fw_update_at_command(update_fw_version)
        if not result:
            self.fail("FW update is not successfully")
        else:
            basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
    
    def tc_fwupdate_ota_single_rm(self):
        ''' This method will run the single update using At Command
        The Radio Module version to be updated is read from "fwupdate_test_conf.yml" with label RM_VERSION 
        '''
        self.testcase_setup('ota')
        update_rm_version = fwupdate_config_map["RM_VERSION"]
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test Case: At Command Radio Module upgrade to "+update_rm_version, "BLUE", "YELLOW")
        result = self.fw_ins.rm_update_at_command(update_rm_version)
        if not result:
            self.fail("RM update is not successfully")
        else:
            basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
    
    def tc_fwupdate_ota_single_aleos_rm(self):
        ''' This method will run the single update using At Command
        The Radio Module version to be updated is read from "fwupdate_test_conf.yml" with label RM_VERSION 
        '''
        self.testcase_setup('ota')
        update_rm_version = fwupdate_config_map["RM_VERSION"]
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Test Case: At Command Radio Module upgrade to "+update_rm_version, "BLUE", "YELLOW")
        result = self.fw_ins.fw_rm_update_at_command(update_rm_version)
        if not result:
            self.fail("FW and RM update is not successfully")
        else:
            basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
    
    def tc_fwupdate_ota_roundtrip_aleos(self):
        ''' This test case method will repeat the firmware update as round trip. 
        '''
        self.testcase_setup('ota')
        round_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        fw2 = fwupdate_config_map["ALEOS_BUILD_TO"]
                      
        for i in range(1,round_count+1):           
            basic_airlink.cslog(time.ctime(time.time())+" ===>> ============ round trip count:" + str(i)+ " ====================", "BLUE")
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_TO"]
            result = self.fw_ins.fw_update_at_command(update_fw_version)
            if not result:
                self.fail("test failed")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")
            
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_FROM"]
            result = self.fw_ins.fw_update_at_command(update_fw_version)
            if not result:
                self.fail("FW update is not successfully")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> Firmware version Verify: Pass", "GREEN")            
            
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> ============ round" + str(i)+ " Completed====================", "BLUE")
 
    def tc_fwupdate_ota_roundtrip_rm(self):
        ''' This test case method will repeat the firmware update as round trip. 
        '''
        self.testcase_setup('ota')
        round_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        fw2 = fwupdate_config_map["ALEOS_BUILD_TO"]
                      
        for i in range(1,round_count+1):           
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> ============ round trip count:" + str(i)+ " ====================", "BLUE")
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_TO"]
            result = self.fw_ins.fw_update_at_command(update_fw_version)
            if not result:
                self.fail("RM update is not successfully")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> RM version Verify: Pass", "GREEN")
            
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_FROM"]
            result = self.fw_ins.fw_update_at_command(update_fw_version)
            if not result:
                self.fail("RM update is not successfully")
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> RM version Verify: Pass", "GREEN")            
            
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> ============ round" + str(i)+ " Completed====================", "BLUE")
       
    def tc_fwupdate_ota_roundtrip_aleos_rm(self):
        ''' This test case method will repeat the firmware update as round trip. 
        '''
        self.testcase_setup('ota')
        round_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        fw1 = fwupdate_config_map["ALEOS_BUILD_FROM"]
        fw2 = fwupdate_config_map["ALEOS_BUILD_TO"]
                      
        for i in range(1,round_count+1):           
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> ============ round trip count:" + str(i)+ " ====================", "BLUE")
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_TO"]
            result = self.fw_ins.fw_update_at_command(update_fw_version)
            if not result:
                self.fail("FW and RM update is not successfully")
            else:
                basic_airlink.clog(time.ctime(time.time())+\
                                   " ===>> Firmware and RM version Verify: Pass", "GREEN")
            
            update_fw_version = fwupdate_config_map["ALEOS_BUILD_FROM"]
            result = self.fw_ins.fw_update_at_command(update_fw_version)
            if not result:
                self.fail("FW and RM update is not successfully")
            else:
                basic_airlink.clog(time.ctime(time.time())+\
                                   " ===>> Firmware and RM version Verify: Pass", "GREEN")            
            
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> ============ round" + str(i)+ " Completed====================", "BLUE")
                  

    

        