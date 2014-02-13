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

from selenium.common.exceptions import NoSuchFrameException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import basic_airlink
import connectivity
import selenium_utilities
import at_utilities
import shutil

test_area = "Fwupdate"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME']
basic_airlink.append_sys_path()
tbd_config_map, fwupdate_config_map = basic_airlink.get_config_data(test_area,"")

class FwupdateAirlink(unittest.TestCase):
    def __init__(self, dut_name, dut_ip="192.168.13.31"):
        self.device_name = dut_name
        self.dut_ip = dut_ip
        self.url = "HTTP://"+self.dut_ip+":9191/" 
        self.username = tbd_config_map[self.device_name]["USERNAME"]
        self.password = tbd_config_map[self.device_name]["PASSWORD"]
        self.ftp_server_ip = fwupdate_config_map["FTP_SERVER_ADDRESS"]
        self.ftp_username = fwupdate_config_map["FTP_USERNAME"]
        self.ftp_password = fwupdate_config_map["FTP_PASSWORD"]
        self.rm_update_flag = False


    
    def fwupdate_ui(self, update_fw_version):
        '''
        This method will update ALEOS with the version in parameter
        
        Args:fw_version
        
        Return:result, If there are any issues during the update process, 
        the result will return the error code from the specific point
        
        Notes: Keep the browser closed before calling this function
        '''
        update_rm_version = self._match_rm(update_fw_version)
        result = self._local_fw_update(update_fw_version, update_rm_version)
        
        if result == "completed":
            if self.rm_update_flag:
                if "True" in self._verify_aleos(update_fw_version) and "True" in self._verify_rm(update_rm_version):
                    result = "ALEOS and RM verify: True"
                else:
                    result = "ALEOS and RM verify: False"
                self.rm_update_flag = False
            else: 
                result = "ALEOS verify: "+self._verify_aleos(update_fw_version)
                             
        return result
    
    def fwrmupdate_ui_roundtrip(self, fw_from, fw_to):
        '''
        This method will update ALEOS with the version in parameter
        
        Args:fw_version
        
        Return:result, If there are any issues during the update process, 
        the result will return the error code from the specific point
        
        Notes: Keep the browser closed before calling this function
        '''
             
        times_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        for round in range(times_count):
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Round: "+str(round+1)+" Started", "BLUE")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Upgrade to: "+fw_to, "BLUE")
            
            result = self.fwupdate_ui(fw_to)
            if not "True" in result :
                self.fail("Test failed. Reason: "+result)
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> "+result, "GREEN")
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE") 
            
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Downgrade to: "+fw_from, "BLUE")
            result = self.fwupdate_ui(fw_from)
            if not "True" in result :
                self.fail("Test failed. Reason: "+result)
            else:
                basic_airlink.clog(time.ctime(time.time())+" ===>> "+result, "GREEN")
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Round: "+str(round+1)+" Completed", "BLUE")
                   

    def fw_update_at_command(self, update_fw_version):
        '''
        This method will update ALEOS with the version in parameter
        
        Args: update_fw_version
        
        Return: result, If there are any issues during the update process, 
        the result will return the error code from the specific point
        
        Notes: Keep the browser closed before calling this function
        '''
        self._execute_at_fw_update(update_fw_version)
        result = self._verify_aleos(update_fw_version)
        return result
    
    def rm_update_at_command(self, update_rm_version):
        '''
        This method will update Radio Module with the version in parameter
        
        Args:fw_version
        
        Return:result, If there are any issues during the update process, 
        the result will return the error code from the specific point
        
        Notes: Set FTP server before running this function
        '''
        result = self._execute_at_rm_update(update_rm_version)
        if "pass" in result:
            result = self._verify_rm(update_rm_version)
        return result
    
    def fw_rm_update_at_command(self, update_fw_version, update_rm_version):
        '''
        This method will update ALEOS and Radio Module with the version in parameters
        
        Args:fw_version
        
        Return:result, If there are any issues during the update process, 
        the result will return the error code from the specific point
        
        Notes: Set FTP server before running this function
        '''
        result = self._execute_at_fw_rm_update(update_fw_version, update_rm_version)
        if "pass" in result:
            if "True" in self._verify_aleos(update_fw_version) and "True" in self._verify_rm(update_rm_version):
                result = "True"
            else:
                result = "False"

        return result
    
#===========================================================================
#Helper functions UI
#===========================================================================
    def _startUp(self):
        ''' the test runner will run that method prior to each test
        
        Args: None
        
        Returns: None
        '''
                       
        self.se_ins = selenium_utilities.SeleniumAcemanager()              
                
        # step: login to Ace Manager 
        basic_airlink.cslog("step: login to ACEmanager") 
        self.driver = self.se_ins.login(self.url, self.username, self.password)

        login_attemp_count = 0               
        while self.se_ins.error_flag == 1:
            login_attemp_count+=1
            logging.info("Can not Login, attemp: " + str(login_attemp_count))
            basic_airlink.cslog("Can not Login, attemp: " + str(login_attemp_count), "RED")
            self.se_ins.error_flag = 0
            self.driver.close()
            self.driver = self.se_ins.login(self.url, self.username, self.password)
            
    
    def _verify_aleos(self, fw_version):
        result = True
        attempt_verify_times = 100
        while attempt_verify_times > 0:
            aleos_version = self._aleos_check()
            basic_airlink.cslog("Current fw version: "+aleos_version)
            if aleos_version != fw_version:
                result = False
                attempt_verify_times=attempt_verify_times-1
                basic_airlink.cslog("fw version does not match", "RED")
            else:
                break
        result_str = str(result)
        return result_str
    
    def _aleos_check(self):
        '''
        To check current aleos firmware version
        
        Args: None
        
        Returns: aleos version
        '''
        aleos_version = ""
        at_ins = at_utilities.AtCommands()
        conn_ins = connectivity.Connectivity(self.device_name, self.dut_ip)
        if fwupdate_config_map["MDT"] == "YES":
            connect_instance = conn_ins.connection_types(test_type="mdt")
        else:
            connect_instance = conn_ins.connection_types()
        attempt_count = 1

        while not connect_instance.connect():
            aleos_version = "connection fail"
            basic_airlink.clog(time.ctime(time.time())+" ===>> aleos_check: Connection Failed, retry after 30 seconds")
            time.sleep(30)          
        
        aleos_version = at_ins.get_fw_version(connect_instance)
        connect_instance.close()
        
        return aleos_version
    
    def _device_check(self):
        '''
        To check whether the device model matches the one configured in testbed yml file or not
        
        Args: device_name
        
        Returns: result: True/False
        '''
        result = True       
        at_ins = at_utilities.AtCommands()
        conn_ins = connectivity.Connectivity(self.device_name, self.dut_ip)
        if fwupdate_config_map["MDT"] == "YES":
            connect_instance = conn_ins.connection_types(test_type="mdt")
        else:
            connect_instance = conn_ins.connection_types()
        while not connect_instance.connect():
            result = False
            basic_airlink.clog(time.ctime(time.time())+" ===>> device_check: Connection Failed, retry after 30 seconds")
            time.sleep(30)
        
        current_device_name = at_ins.get_device_model(connect_instance)
        current_device_rm = at_ins.get_rm_name(connect_instance)
        current_device_str = "DUT_"+current_device_name+"_"+current_device_rm
        basic_airlink.clog(time.ctime(time.time())+" ===>>"+current_device_str)
        if not current_device_str in self.device_name:
            result = False
        connect_instance.close()
        return result

    def _get_device_prefix(self):
        '''
        To get the device model prefix from configure yml file
        
        Args: None
        
        Returns: device_prefix
        '''
        device_prefix = "None"
        if tbd_config_map[self.device_name]["MODEL"][0:2] == "GX" or tbd_config_map[self.device_name]["MODEL"][0:2] == "ES":            
            device_prefix = "GX"
        elif tbd_config_map[self.device_name]["MODEL"][0:2] == "LS":
            device_prefix = "LS"
        
        return device_prefix
    
    def _network_state_ckeck(self):
        
        at_ins = at_utilities.AtCommands()
        conn_ins = connectivity.Connectivity()
        connect_instance = conn_ins.connection_types()
        network_state = ""
        while not connect_instance.connect():
            network_state = "Error"
            basic_airlink.clog(time.ctime(time.time())+" ===>> network_ready_ckeck: Connection Failed, retry after 30 seconds")
            time.sleep(30)

        network_state = at_ins.get_net_state(connect_instance)
        basic_airlink.cslog(network_state)
        connect_instance.close()
        return network_state
    
    def _get_aleos_path(self, device_prefix, fw_version):
        '''
        To get aleos firmware file path in local PC
        
        Args: device_prefix
              firmwareVersion
        
        Returns: ALEOSBuild: aleos absolute path
        '''
        aleos_build_filename = device_prefix+'_'+fw_version+'.bin'
        aleos_build_path = airlinkautomation_home_dirname + '\\data\\builds\\RmFwImages\\'+ aleos_build_filename
        return aleos_build_path
    
    def _get_rm_path(self, rm_version):
        rm_build_filename = rm_version+'.bin'
        rm_build_path = airlinkautomation_home_dirname + '\\data\\builds\\RmFwImages\\'+ rm_build_filename
        return rm_build_path

    def _local_fw_update(self, fw_version, rm_version):
        ''' 
        This method will check the ALEOS version and decide 
        which update type should be used, call update execute function
        
        Args: firmware version
        
        Returns: None
        '''       
        device_prefix = self._get_device_prefix()

        self.current_fw_version = self._aleos_check()
        basic_airlink.clog(time.ctime(time.time())+" ===>> Current Firmware Version: "+self.current_fw_version)        
        aleos_build_path = self._get_aleos_path(device_prefix, fw_version)      
        rm_build_path = self._get_rm_path(rm_version)  
        basic_airlink.cslog(time.ctime(time.time())+" ===>> ALEOS Build: "+aleos_build_path)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> RM Build: "+rm_build_path)
                
        if not "4.3.3" in self.current_fw_version:
            update_type = fwupdate_config_map["UPDATE_TYPE"]            
        else:
            update_type = ""
        result = self._fw_update(aleos_build_path, rm_build_path, update_type, fw_version)
        return result

  
    def _fw_btn_click(self, driver):
        '''
        To click firmware update button in ACEManager
        
        Args: driver: browser
        
        Returns: result: True/False
        '''
        try:
            result = True
            driver.find_element_by_id("btn_fw").click()
            xmlFrame =driver.find_element_by_xpath("//*[@id='xmlPage']")
            driver.switch_to_frame(xmlFrame)
        except WebDriverException:
            result = False
            basic_airlink.cslog(time.ctime(time.time())+" ===>> fail on btn_fw click", "RED")
        finally:
            return result

    def _fw_frame_switch(self, driver):
        '''
        To switch the frame to update window in ACEManager
        
        Args: driver: browser
        
        Returns: result: True/False
        '''
        try:
            result = True
            file_frame= self.driver.find_element_by_xpath(".//div[@id='file_upload']/center/div/div/iframe")   
            driver.switch_to_frame(file_frame)
        except WebDriverException:
            result = False
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Fail on fw frame switch", "RED")
        finally:
            return result

    def _get_update_type(self, driver, update_type):
        '''
        To get update type in ACEManager, ALEOS update/ Radio module update
        
        Args: driver: browser
              updateType
        
        Returns: typeFlag
        '''
        type_flag=0
        update_type_element_index = 0
        if "4.3.5" in self.current_fw_version:
            update_type_element_index = 1
        
        try:
            if(update_type == "ALEOS_Software"):
                driver.find_elements_by_name("update_type")[update_type_element_index].click()
                
            elif(update_type == "Radio_Module_Firmware"):
                driver.find_elements_by_name("update_type")[update_type_element_index+1].click()
                type_flag=1
        
        except WebDriverException as e:
            type_flag = -1
            basic_airlink.cslog(time.ctime(time.time())+" ===>>"+ str(e.msg))
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Fail on update type click", "RED")
        
        finally:
            return type_flag
    
    def _browse_fw_file(self, driver, aleos_file):
        '''
        To browse and select firmware file
        
        Args: driver: browser
              updateFile: firmware file
        
        Returns: result: True/False
        '''
        try:
            result = True
            driver.find_element_by_name("image").send_keys(aleos_file)
        except WebDriverException:
            result = False
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Error in send_keys(choose the FW file), Restart....", "RED")
        finally:        
            return result

    def _fw_go_click(self, driver):
        '''
        To click update button in update window
        
        Args: driver: browser
        
        Returns: result: True/False
        '''
        try:
            result = True
            driver.find_element_by_name("go").click()
        except WebDriverException:
            result = False
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Error in go click(click update buttom), Restart....", "RED")
        finally:
            return result
            
    def _rm_update(self, driver, rm_build_path):
        '''
        To update radio module
        
        Args: driver: browser
              RMBuild: RM file
        
        Returns: result: True/False
        '''
        try:
            # wait for frame
            # check if it need to upload RM file when it is in the "Applying stage"
            result = True
            device_prefix = self._get_device_prefix()          
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Applying ...")
            
            logging.info(time.ctime(time.time())+" ===>> Uploading RM Firmware ...")
            try:
                RMFrame= driver.find_element_by_xpath(".//div[@id='file_upload']/center[2]/div/div[3]/div/div/iframe")
                driver.switch_to_frame(RMFrame)
            except NoSuchFrameException:
                result = False
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Frame not found!", "RED")
            else:
                driver.find_element_by_name("image").send_keys(rm_build_path)
                driver.find_element_by_name("go").click()
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Applying Firmware ...")
                self.rm_update_flag = True
                time.sleep(tbd_config_map[self.device_name]["RM_TIMEOUT"])
                
        except:
            result = False
            basic_airlink.cslog(time.ctime(time.time())+" ===>> No RM update required")
        finally:
            return result
        
    def _wait_update_process(self,driver, fw_version):
        '''
        To wait ACEManager log out after update
        
        Args: driver: browser
        
        Returns: result: True/False
        '''
        device_prefix = self._get_device_prefix()
        if "I" in fw_version:
            timer_wait_logout = fwupdate_config_map["TIMER"][device_prefix]["WAIT_PROCESS_I"]
            basic_airlink.clog("WAIT_PROCESS_I", "RED")
        else:
            timer_wait_logout = fwupdate_config_map["TIMER"][device_prefix]["WAIT_PROCESS_F"]
            basic_airlink.clog("WAIT_PROCESS_F", "RED")
        
        try:
            result = True          
            WebDriverWait(driver, timeout=timer_wait_logout).until(EC.visibility_of_element_located((By.ID, "aceMasterInn")))
        except:
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Fail on wait log out")
            result = False
        
        finally:
            return result

    def _default_content_switch(self, driver):
        '''
        To switch to the default content frame
        
        Args: driver: browser
        
        Returns: result: True/False
        '''
        try:
            result = True
            driver.switch_to_default_content()
            xmlFrame =driver.find_element_by_xpath("//*[@id='xmlPage']")
            driver.switch_to_frame(xmlFrame)                                  
        except WebDriverException:
            result = False
            basic_airlink.cslog("Fail on default content switch", "RED")
        finally:
            return result
            
    def _get_step_pic_name(self, driver, step_num):
        pic_elem = driver.find_element_by_xpath(".//div[@id='file_upload']/center[2]/div/div["+str(step_num)+"]/img")
        pic_name = pic_elem.get_attribute("src").split('/')[-1]
        return pic_name
        
    def _fw_update(self, aleos_build_path, rm_build_path, update_type, fw_version):
        ''' 
        This method will operate the update process in UI
        
        Args: ALEOSBuild
              RMBuild
              UpdateType
        
        Returns: None
        '''
        attempt_time = fwupdate_config_map["ATTEMP_TIME"]
        step_timer = fwupdate_config_map["STEP_TIMER"]
        #Attempt count if the step is fail       
        attemp_count_click_fw_btn = 0
        attemp_count_switch_frame = 0 
        attemp_count_get_type = 0 
        attemp_count_browse_file = 0 
        attemp_count_click_go = 0
        attemp_count_switch_content = 0 
                 
        while True:      
            self._startUp()
            
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Clicking firmware update button")
            
            time.sleep(step_timer)
            if self._fw_btn_click(self.driver) != True:
                if attemp_count_click_fw_btn >= attempt_time:
                    result = "err_fw_btn_click"
                    break                    
                else:
                    attemp_count_click_fw_btn+=1
                    self.driver.close()
                    continue
            
            time.sleep(step_timer)
            if self._fw_frame_switch(self.driver) != True:
                if attemp_count_switch_frame >= attempt_time:
                    result = "err_switch_frame"
                    break                    
                else:
                    attemp_count_switch_frame+=1
                    self.driver.close()
                    continue  
                
            time.sleep(step_timer)
            if update_type != "":
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Getting update type") 
            type_flag = self._get_update_type(self.driver, update_type)        
            if type_flag == -1:
                if attemp_count_get_type >= attempt_time:
                    result = "err_get_update_type"
                    break
                else:
                    attemp_count_get_type+=1
                    self.driver.close()
                    continue                    
            
            time.sleep(step_timer)           
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Browsing ALEOS Build file")        
            if self._browse_fw_file(self.driver, aleos_build_path) != True:
                if attemp_count_browse_file >= attempt_time:
                    result = "err_browse_file"
                    break
                else:
                    attemp_count_browse_file+=1
                    self.driver.close()
                    continue 
            
            time.sleep(step_timer)           
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Clicking Go")
            if self._fw_go_click(self.driver) != True:
                if attemp_count_click_go >= attempt_time:
                    result = "err_click_go"
                    break
                else:
                    attemp_count_click_go+=1
                    self.driver.close()
                    continue
            
            time.sleep(step_timer)
            basic_airlink.clog(time.ctime(time.time())+" ===>> Waiting for updating process")                       
            if self._default_content_switch(self.driver) != True:
                if attemp_count_switch_content >= attempt_time:
                    result = "err_switch_content"
                    break
                else:
                    attemp_count_switch_content+=1
                    self.driver.close()
                    continue
            
            #check the update window if is still in the browser
            quit_flag = False
            if not self._wait_update_process(self.driver, fw_version):
                if not "check.gif" in self._get_step_pic_name(self.driver, 1):
                    self.driver.quit()
                    continue
                if not "check.gif" in self._get_step_pic_name(self.driver, 2):
                    self.driver.quit()
                    continue
                
                step_3_pic = self._get_step_pic_name(self.driver, 3)
                if not "check.gif" in step_3_pic:
                    if not self._rm_update(self.driver, rm_build_path):
                        if "warning.gif" in step_3_pic:
                            continue
                        self.driver.quit()
                    quit_flag = True
                    break
            break
        
        time.sleep(step_timer)                   
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Done ALEOS Updating")
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Rebooting ...")
        reboot_time= tbd_config_map[self.device_name]["REBOOT_TIMEOUT"]
        time.sleep(reboot_time)
        if quit_flag != True:
            self.driver.quit()

        result = "completed"
        return result

#===========================================================================
#Helper functions AT Command
#===========================================================================
    def _execute_at_fw_update(self, update_fw_version):
        ''' 
        This method will call the firmware update function in the library
        
        Args: None
        
        Returns: None
        '''
        # future version should added in this list, the version before can not use specified file feature
        version_list = ["4.3.5"]
        at_ins = at_utilities.AtCommands()
        current_aleos_version = self._aleos_check()

        fw_filename = self._get_device_prefix()+"_"+update_fw_version+".bin"
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Step:  Start running the *fwupdate command")
        
        conn_ins = connectivity.Connectivity(self.device_name, self.dut_ip)
        if fwupdate_config_map["MDT"] == "YES":
            connect_instance = conn_ins.connection_types(test_type="mdt")
        else:
            connect_instance = conn_ins.connection_types()
        attempt_count = 1

        while (not connect_instance.connect()) and (attempt_count<=5):
            aleos_version = -1
            attempt_count+=1
            basic_airlink.clog(time.ctime(time.time())+" ===>> _execute_at_fw_update: Connection Failed, try again")
        
        for version in version_list:
            if version in current_aleos_version:
                basic_airlink.cslog(time.ctime(time.time())+" ===>> filename needed")
                at_ins.fw_update(connect_instance, self.ftp_server_ip, self.ftp_username, self.ftp_password, fw_filename)
            else:
                basic_airlink.cslog(time.ctime(time.time())+" ===>> filename changed to fw.bin")
                self._change_fw_filename(fw_filename)
                at_ins.fw_update(connect_instance, self.ftp_server_ip, self.ftp_username, self.ftp_password)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Step:  Finished update, wait reboot...")
        time.sleep(tbd_config_map[self.device_name]["REBOOT_TIMEOUT"])
        
    def _match_rm(self, fw_version):
        fw1_version = ""
        fw_lst = fwupdate_config_map["ALEOS_VERSION_LIST"]
        for version in fw_lst:
            if version in fw_version:
                fw1_version = version
        
        rm1_name = fwupdate_config_map[fw1_version][self.device_name]        
        basic_airlink.clog(time.ctime(time.time())+" ===>> rm1_version: "+rm1_name)
        
        return rm1_name
        
    def _verify_rm(self, rm_version):
       
        rm_version_rear = rm_version.split("_")[2]
#        basic_airlink.clog(time.ctime(time.time())+" ===>> rm_version_rear: "+rm_version_rear)
        rm_ver_dict = {
                "P1008":"P1_0_0_8AP",
                "T1043D":"T1_0_4_3DAP",
                "1032":"T1_0_3_2AP",
                "3552":"T3_5_5_2AP",
                "3553":"T3_5_5_3AP",
                "11301":"p3111301",
                "153":"p3110503",
                "156":"p3110506",                 
            }
        result = True
        at_ins = at_utilities.AtCommands()
        conn_ins = connectivity.Connectivity(self.device_name, self.dut_ip)
        if fwupdate_config_map["MDT"] == "YES":
            connect_instance = conn_ins.connection_types(test_type="mdt")
        else:
            connect_instance = conn_ins.connection_types()
        attempt_count = 1
        
        while (not connect_instance.connect()) and (attempt_count<=100):
            aleos_version = -1
            attempt_count+=1
            basic_airlink.clog(time.ctime(time.time())+" ===>> _verify_rm: Connection Failed, try again")
        
        current_rm_version = at_ins.get_rm_version(connect_instance)
        rm_version_dict = rm_ver_dict[rm_version_rear]
        connect_instance.close()
        basic_airlink.clog(time.ctime(time.time())+" ===>> "+current_rm_version)
        if (rm_version_dict == "") or (not rm_version_dict in current_rm_version):
            basic_airlink.clog(time.ctime(time.time())+" ===>> rm_version_dict: "+rm_version_dict)
            result = False
        return str(result)
           
    def _execute_at_rm_update(self, update_rm_version):
        ''' 
        This method will call the firmware update function in the library
        
        Args: None
        
        Returns: None
        '''
        at_ins = at_utilities.AtCommands()
        current_aleos_version = self._aleos_check()
        
        conn_ins = connectivity.Connectivity(self.device_name, self.dut_ip)
        if fwupdate_config_map["MDT"] == "YES":
            connect_instance = conn_ins.connection_types(test_type="mdt")
        else:
            connect_instance = conn_ins.connection_types()
        rm_filename = update_rm_version + ".bin"
        attempt_count = 1

        while (not connect_instance.connect()) and (attempt_count<=5):
            aleos_version = -1
            attempt_count+=1
            basic_airlink.clog(time.ctime(time.time())+" ===>> _execute_at_rm_update: Connection Failed, try again")
            
        
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Step:  Start running the *rmupdate command")
        result = at_ins.rm_update(connect_instance, self.ftp_server_ip, self.ftp_username, self.ftp_password, rm_filename)
#        basic_airlink.cslog(time.ctime(time.time())+" ===>>Result: "+result)
        if not "failed" in result:
            result = "pass"
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Step:  Finished update, wait reboot...")
            time.sleep(700)
        return result

    
    def _execute_at_fw_rm_update(self, update_fw_version, update_rm_version):
        ''' 
        This method will call the firmware update function in the library
        
        Args: None
        
        Returns: None
        '''        
        at_ins = at_utilities.AtCommands()
        current_aleos_version = self._aleos_check()
        
        conn_ins = connectivity.Connectivity(self.device_name, self.dut_ip)
        if fwupdate_config_map["MDT"] == "YES":
            connect_instance = conn_ins.connection_types(test_type="mdt")
        else:
            connect_instance = conn_ins.connection_types()
        device_prefix = self._get_device_prefix()
        fw_filename = device_prefix +"_"+ update_fw_version + ".bin"
        rm_filename = update_rm_version + ".bin"
        
        basic_airlink.cslog(time.ctime(time.time())+" ===>>fw update to: "+fw_filename)
        basic_airlink.cslog(time.ctime(time.time())+" ===>>rm update to: "+rm_filename)
        
        attempt_count = 1
        while (not connect_instance.connect()) and (attempt_count<=5):
            aleos_version = -1
            attempt_count+=1
            basic_airlink.clog(time.ctime(time.time())+" ===>> _execute_at_fwrm_update: Connection Failed, try again")
        
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Step:  Start running the *fwrmupdate command")
        result = at_ins.fw_rm_update(connect_instance, self.ftp_server_ip, self.ftp_username, self.ftp_password, fw_filename, rm_filename)
        if not "failed" in result:
            result = "pass"
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Step:  Finished update, wait reboot...")
            time.sleep(700)     
        return result
               
    def _change_fw_filename(self,fw_filename):
        ''' 
        This method will change the firmware filename so that the name 
            can match fw.bin
        
        Args: fw_filename: firmware filename
        
        Returns: None
        '''
        result = True
        device_prefix = self._get_device_prefix()
        try:
#            os.remove(airlinkautomation_home_dirname + '\\data\\builds\\RmFwImages\\fw.bin')
            shutil.copyfile(airlinkautomation_home_dirname + '\\data\\builds\\RmFwImages\\' + fw_filename, 
                            airlinkautomation_home_dirname + '\\data\\builds\\RmFwImages\\fw.bin')
        except:
            result = False
            basic_airlink.cslog("Fail on change filename", "RED")
        
        return result
    
    def _at_commands_fwupdate(self,fw_version):
        ''' This method will check which version should be updated and run update function 
        
        Args: fw_version: firmware 1
        
        Returns: None
        '''
        retry_count = 0
        filename_change_check = True
        device_prefix = self.get_device_prefix()
#         current_fw_version = self.at_ins.get_fw_version(self.connect_instance)

        self.assertNotEqual(retry_count, 5, "Firmware update fail")
            
        filename_change_check = self.change_fw_filename(device_prefix+"_"+fw_version+".bin")
        self.assertEqual(filename_change_check, True, "Fail on change filename "+fw_version)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> filename changed"+fw_version)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> at update start...")
        self._execute_at_command_fwupdate()
        
#         if self.aleos_verify(fw1) != True:
#             retry_count+=1
#             continue
#         else:
#             basic_airlink.cslog(time.ctime(time.time())+" ===>> Verify current version: "+fw1+ " Pass", "GREEN")            
#             break
