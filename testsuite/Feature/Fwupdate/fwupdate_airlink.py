###############################################################################
#
# This module provides FW Update operations by UI. 
# Company: Sierra Wireless
# Time: April 10th, 2014
# 
#################################################################################
from selenium.common.exceptions import NoSuchFrameException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import logging
import os,sys
import time
import basic_airlink
import connectivity
import selenium_utilities
import telnet_airlink
import at_utilities
import shutil
import yaml
import re
import gc

test_area = "Fwupdate"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME']
tbd_config_map, fwupdate_config_map = basic_airlink.get_config_data(test_area,"")
basic_airlink.append_sys_path()

def load_temp_tc_map():
    with open('temp_fwupdate_tc_info.yml','r') as stream:
        combo_map = yaml.load(stream)
    return combo_map

class FwupdateAirlink(selenium_utilities.SeleniumAcemanager):
    def __init__(self, dut_name=tbd_config_map["DUTS"][0], dut_ip="192.168.13.31"):
        '''Initialization
        '''
        selenium_utilities.SeleniumAcemanager.__init__(self)
        self.device_name = dut_name
        self.dut_ip = dut_ip
        self.url = "HTTP://"+self.dut_ip+":9191/" 
        self.username = tbd_config_map[self.device_name]['USERNAME']
        self.password = tbd_config_map[self.device_name]['PASSWORD']
        self.ftp_server_ip = fwupdate_config_map["FTP_SERVER_ADDRESS"]
        self.ftp_username = fwupdate_config_map["FTP_USERNAME"]
        self.ftp_password = fwupdate_config_map["FTP_PASSWORD"]
        self.rm_update_flag = False
        
        if fwupdate_config_map["MDT_LOCAL"] == "YES":
            self.conn_ins = telnet_airlink.TelnetAirlink(hostname=self.dut_ip)
        else:
            self.conn_ins = connectivity.Connectivity().connection_types()

    def fwupdate_ui_rm(self, update_rm_version):
        '''This method will update RM with the version in parameter
        
        Args:update_rm_version
        
        Return:result, If there are any issues during the update process, 
        the result will return the error code from the specific point
        
        Notes: Keep the browser closed before calling this function
        '''
        
        result = self._pre_fwupdate_rm(update_rm_version)
        if result == 'completed':
            if self._verify_rm(update_rm_version):
                result = "RM verify: True"
            else:
                result = "RM verify: False"
        return result    
            
        
    def fwupdate_ui_aleos(self,update_fw_version,skip_rm=False):
        '''This method will update ALEOS with the version in parameter
        
        Args:update_fw_version
        
        Return:result, If there are any issues during the update process, 
        the result will return the error code from the specific point
        
        Notes: Keep the browser closed before calling this function
        '''
        
        if skip_rm:
            basic_airlink.cslog("Note: The RM update will be skiped", "RED")
        
        update_rm_version = self._match_rm(update_fw_version)
        result = self._pre_fwupdate_aleos(update_fw_version, update_rm_version, skip_rm)
        if result == "completed":
            if self.rm_update_flag:
                if self._verify_aleos(update_fw_version) and self._verify_rm(update_rm_version):
                    result = "ALEOS and RM verify: True"
                else:
                    result = "ALEOS and RM verify: False"
                    self.rm_update_flag = False
            else: 
                result = "ALEOS verify: "+ str(self._verify_aleos(update_fw_version))               
        return result
    
    def fwrmupdate_ui_aleos_roundtrip(self, fw_from, fw_to, skip_rm=False):
        '''This method will update ALEOS with the version in parameter
        
        Args:fw_version_to, fw_version_from
        
        Return:result, If there are any issues during the update process, 
        the result will return the error code from the specific point
        
        Notes: Keep the browser closed before calling this function
        '''
        if skip_rm:
            basic_airlink.cslog("Note: The RM update will be skiped", "RED")
           
        times_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        for round in range(times_count):
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Round: "+str(round+1)+" Started", "BLUE")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Upgrade to: "+fw_to, "BLUE")
            
            result = self.fwupdate_ui_aleos(fw_to,skip_rm=skip_rm)
            if not result :
                self.fail("Test failed. Reason: "+str(result))
            else:
                basic_airlink.cslog(time.ctime(time.time())+" ===>> "+str(result), "GREEN")
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE") 
            
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Downgrade to: "+fw_from, "BLUE")
            result = self.fwupdate_ui_aleos(fw_from, skip_rm=skip_rm)
            if not result :
                self.fail("Test failed. Reason: "+str(result))
            else:
                basic_airlink.cslog(time.ctime(time.time())+" ===>> "+str(result), "GREEN")
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Round: "+str(round+1)+" Completed", "BLUE")
    
    def fwrmupdate_ui_rm_roundtrip(self, rm_from, rm_to):
        '''This method will update ALEOS with the version in parameter
        
        Args:rm_version_from, rm_version_to
        
        Return:result, If there are any issues during the update process, 
        the result will return the error code from the specific point
        
        Notes: Keep the browser closed before calling this function
        '''
             
        times_count = fwupdate_config_map["ROUNDTRIP_TIMES"]
        for round in range(times_count):
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Round: "+str(round+1)+" Started", "BLUE")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Upgrade to: "+rm_to, "BLUE")
            
            result = self.fwupdate_ui_rm(rm_to)
            if not result :
                self.fail("Test failed. Reason: "+str(result))
            else:
                basic_airlink.cslog(time.ctime(time.time())+" ===>> "+str(result), "GREEN")
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Test case Completed", "BLUE") 
            
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Downgrade to: "+rm_from, "BLUE")
            result = self.fwupdate_ui_rm(rm_from)
            if not result :
                self.fail("Test failed. Reason: "+str(result))
            else:
                basic_airlink.cslog(time.ctime(time.time())+" ===>> "+str(result), "GREEN")
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Round: "+str(round+1)+" Completed", "BLUE")
                   
    def fw_update_at_command(self, update_fw_version):
        '''This method will update ALEOS with the version in parameter
        
        Args: update_fw_version
        
        Return: result, If there are any issues during the update process, 
        the result will return the error code from the specific point
        
        Notes: Keep the browser closed before calling this function
        '''
        ret = self._execute_at_fw_update(update_fw_version)
        result = False
        if ret:
            result = self._verify_aleos(update_fw_version)
        return result
    
    def rm_update_at_command(self, update_rm_version):
        '''This method will update Radio Module with the version in parameter
        
        Args:fw_version
        
        Return:result, If there are any issues during the update process, 
        the result will return the error code from the specific point
        
        Notes: Set FTP server before running this function
        '''
        ret = self._execute_at_rm_update(update_rm_version)
        result = False
        if ret:
            result = self._verify_rm(update_rm_version)
        return result
    
    def fw_rm_update_at_command(self, update_fw_version, update_rm_version):
        '''This method will update ALEOS and Radio Module with the version in parameters
        
        Args:fw_version
        
        Return:result, If there are any issues during the update process, 
        the result will return the error code from the specific point
        
        Notes: Set FTP server before running this function
        '''
        ret = self._execute_at_fw_rm_update(update_fw_version, update_rm_version)
        result = False
        if ret: 
            if self._verify_aleos(update_fw_version) and self._verify_rm(update_rm_version):
                result = True
        return result
    
#===========================================================================
#Helper functions UI
#===========================================================================
    def _startUp(self):
        ''' The test runner will run that method prior to each test
        
        Args: None
        
        Returns: None
        '''                
        # step: login to Ace Manager 
        basic_airlink.cslog("step: login to ACEmanager")
        
        self.driver = self.login(self.url, self.username, self.password)
        

        login_attemp_count = 0               
        while login_attemp_count <= fwupdate_config_map["ATTEMPT_TIME"] and self.error_flag==1:
            self.error_flag = 0
            login_attemp_count+=1
            logging.info("Can not Login, attemp: " + str(login_attemp_count))
            basic_airlink.cslog("Can not Login, attemp: " + str(login_attemp_count), "RED")          
            self.driver.quit()
            self.driver =self.login(self.url, self.username, self.password)
               
    def _verify_aleos(self, fw_version):
        '''Verify the expected version and current version in device
        
        Args: fw_version: expected fw version
        
        return:result str: True/False 
        '''
        basic_airlink.cslog("step: Verify ALEOS version")
        result = True
        attempt_verify_times = fwupdate_config_map["ATTEMPT_VERIFY_TIME"]
        while attempt_verify_times > 0:
            aleos_version = self._aleos_check()
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Current ALEOS version: "+aleos_version)
            if aleos_version != fw_version:
                result = False
                attempt_verify_times=attempt_verify_times-1
                basic_airlink.cslog("fw version does not match", "RED")
            else:
                result = True
                break
        return result
    
    def _aleos_check(self):
        '''To check current aleos firmware version
        
        Args: None
        
        Returns: aleos version
        '''
        aleos_version = ""
        at_ins = at_utilities.AtCommands()
        attempt_count = 1
        basic_airlink.cslog("step: Check current ALEOS version") 
        while not self.conn_ins.connect():
            aleos_version = "connection fail"
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> aleos_check: Connection Failed, retry after 30 seconds")
            time.sleep(30)          
        
        while (aleos_version == "ERROR" or aleos_version =="") and attempt_count>=0:
            aleos_version = at_ins.get_fw_version(self.conn_ins)
            self.conn_ins.close()
        
        return aleos_version
    
    def _device_check(self):
        '''To check whether the device model matches the one configured in testbed yml file or not
        
        Args: device_name
        
        Returns: result: True/False
        '''
        basic_airlink.cslog("step: Check device model") 
        result = True       
        at_ins = at_utilities.AtCommands()
        while not self.conn_ins.connect():
            result = False
            basic_airlink.cslog(time.ctime(time.time())+" ===>> device_check: Connection Failed, retry after 30 seconds")
            time.sleep(30)
        
        current_device_name = at_ins.get_device_model(self.conn_ins)
        current_device_rm = at_ins.get_rm_name(self.conn_ins)
        current_device_str = "DUT_"+current_device_name+"_"+current_device_rm
        basic_airlink.clog(time.ctime(time.time())+" ===>>"+current_device_str)
        if not current_device_str in self.device_name:
            result = False
        self.conn_ins.close()
        return result
    
    def _compare_rm(self,fw_from = None,fw_to = None):
        result = False
        current_fwversion = self._aleos_check()
        if fw_from is None:
            if self._match_rm(fw_to) == self._match_rm(current_fwversion):
                result = True
        else:
            if self._match_rm(fw_from) == self._match_rm(fw_to):
                result = True
        return result
    
    def _match_rm(self, fw_version):
        '''Match the RM according ALEOS version and device
        
        Args: fw_version
        
        Return: rm_name 
        '''
        basic_airlink.cslog("step: Match the RM within ALEOS and device") 
        fw1_version = ""
        fw_lst = fwupdate_config_map["ALEOS_VERSION_LIST"]
        for version in fw_lst:
            if version in fw_version:
                fw1_version = version
        
        rm1_name = fwupdate_config_map[fw1_version][self.device_name]        
        basic_airlink.clog(time.ctime(time.time())+" ===>> rm_version: "+rm1_name)
        
        return rm1_name
        
    def _verify_rm(self, rm_version):
        '''Verify the RM if is expected version in current device
        
        Args: rm_version
        
        Return: result string Ture/False
        '''
        basic_airlink.cslog("step: Verify Radio Module")
        rm_version_rear = rm_version.split("_")[2]
        rm_ver_dict = fwupdate_config_map["RM_VER_NAME_MAP"]
        result = True
        at_ins = at_utilities.AtCommands()
        attempt_count = 1
        
        while (not self.conn_ins.connect()) \
               and (attempt_count<=fwupdate_config_map["ATTEMPT_VERIFY_TIME"]):
            aleos_version = -1
            attempt_count+=1
            basic_airlink.clog(time.ctime(time.time())+\
                               " ===>> _verify_rm: Connection Failed, try again")
        
        current_rm_version = at_ins.get_rm_version(self.conn_ins)
        rm_version_dict = rm_ver_dict[rm_version_rear]
        self.conn_ins.close()
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Current RM version "+current_rm_version)
        if (rm_version_dict == "") or (not rm_version_dict in current_rm_version):
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> rm_version_dict: "+rm_version_dict)
            result = False
        
        return result

    def _get_device_prefix(self):
        '''To get the device model prefix from configure yml file
        
        Args: None
        
        Returns: device_prefix
        '''
        device_prefix = "None"
        if tbd_config_map[self.device_name]["MODEL"][0:2] == "GX" or tbd_config_map[self.device_name]["MODEL"][0:2] == "ES":            
            device_prefix = "GX"
        elif tbd_config_map[self.device_name]["MODEL"][0:2] == "LS":
            device_prefix = "LS"
        
        return device_prefix
   
    def _get_aleos_path(self, device_prefix, fw_version):
        '''To get aleos firmware file path in local PC
        
        Args: device_prefix
              firmwareVersion
        
        Returns: ALEOSBuild: aleos absolute path
        '''
        aleos_build_filename = device_prefix+'_'+fw_version+'.bin'
        aleos_build_path = airlinkautomation_home_dirname + '\\data\\builds\\'+ aleos_build_filename
        return aleos_build_path
    
    def _get_rm_path(self, rm_version):
        '''Get the RM file path on the PC
        
        Args: rm version
        
        Return: the rm path string
        '''
        rm_build_filename = rm_version+'.bin'
        rm_build_path = airlinkautomation_home_dirname + '\\data\\builds\\'+ rm_build_filename
        return rm_build_path

    def _pre_fwupdate_rm(self,rm_version,skip_rm = False):
        '''Pre-actions for update operation
        
        Args: rm_version
        
        Return: update result
        '''
        self.current_fw_version = self._aleos_check()
        basic_airlink.clog(time.ctime(time.time())+" ===>> Current ALEOS Version: "+self.current_fw_version)
        rm_build_path = self._get_rm_path(rm_version)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> RM Build: "+rm_build_path)
        path_list = [rm_build_path]
        
        result = self._fw_update(path_list,skip_rm)

        return result
                
    def _pre_fwupdate_aleos(self, fw_version, rm_version="",skip_rm=False):
        ''' 
        This method will check the ALEOS version and decide 
        which update type should be used, call update execute function
        
        Args: firmware version
        
        Returns: None
        '''       
        device_prefix = self._get_device_prefix()

        self.current_fw_version = self._aleos_check()      #would take some time to access.
        result = "ERROR when getting the current ALEOS version, Please run again..."
        if self.current_fw_version == "ERROR":
            basic_airlink.cslog(result, "RED")
            return result
        
        basic_airlink.cslog(time.ctime(time.time())+" ===>> Current ALEOS Version: "+self.current_fw_version)        
        aleos_build_path = self._get_aleos_path(device_prefix, fw_version)      
        rm_build_path = self._get_rm_path(rm_version)  
        basic_airlink.cslog(time.ctime(time.time())+" ===>> ALEOS Build path: "+aleos_build_path)
        basic_airlink.cslog(time.ctime(time.time())+" ===>> RM Build path: "+rm_build_path)
        path_list = [aleos_build_path,rm_build_path]       
        result = self._fw_update(path_list, skip_rm, fw_version)
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
                
        #Because the update type DOM index is changed after 4.3.5,
        #here is checking the ALEOS version to determine which index should be used.
        result = re.match(r'[4]\.[3]\.[2-4]', self.current_fw_version)
#        basic_airlink.cslog(str(result), "RED")
        if result is None:
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
        '''To click update button in update window
        
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
            
    def _rm_update(self, driver, rm_build_path, skip_rm):
        '''To update radio module
        
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
                
                if skip_rm is True:
                    basic_airlink.cslog(time.ctime(time.time())+"===>> Skip RM update...", "RED")
                    driver.find_element_by_name("gonnot").click()
                    driver.switch_to_alert().accept()                   
                    result = True
                else:               
                    driver.find_element_by_name("image").send_keys(rm_build_path)
                    driver.find_element_by_name("go").click()
                    try:
                        driver.switch_to_alert().accept()
                        basic_airlink.cslog(time.ctime(time.time())+"===>> Warning windows prompt!", "RED")
                    except:
                        pass
                    basic_airlink.cslog(time.ctime(time.time())+" ===>> Applying Firmware ...")
                    self.rm_update_flag = True
                    timer_wait_logout = tbd_config_map[self.device_name]["RM_TIMEOUT"]
                    time.sleep(timer_wait_logout)
                    result = True               
        except:
            result = False
            basic_airlink.cslog(time.ctime(time.time())+" ===>> No RM update required")
        finally:
            return result
        
    def _wait_update_process(self,driver,update_type ,fw_version):
        '''To wait ACEManager log out after update
        
        Args: driver: browser
        
        Returns: result: True/False
        '''
        device_prefix = self._get_device_prefix()
        wait_rm_frame = 45
        if update_type == 'Radio_Module_Firmware':
            timer_wait_logout = fwupdate_config_map["TIMER"]["RM"]
#            timer_wait_logout = tbd_config_map[self.device_name]["RM_TIMEOUT"]
            basic_airlink.cslog("WAIT_PROCESS_RM", "RED")
        
        else:      
            if not "192.168." in self.dut_ip:
                #OTA
                if "I" in fw_version:
                    timer_tag = "WAIT_PROCESS_INCREAMENT_OTA"
                    basic_airlink.cslog("Pick timer for waiting INCREMENT update process", "RED")
                
                else:
                    timer_tag = "WAIT_PROCESS_FULL_OTA"
                    basic_airlink.cslog("Pick timer for waiting FULL update process", "RED")            
          
            else:
                #LOCAL
                if "I" in fw_version:
                    timer_tag = "WAIT_PROCESS_INCREAMENT_LOCAL"
                    basic_airlink.cslog("Pick timer for waiting INCREMENT update process", "RED")
                
                else:
                    timer_tag = "WAIT_PROCESS_FULL_LOCAL"
                    basic_airlink.cslog("Pick timer for waiting FULL update process", "RED")
                 
            timer_wait_logout = fwupdate_config_map["TIMER"][device_prefix][timer_tag]
        
        basic_airlink.cslog("Wait Applyting Step", "BLUE")
        try:
            result = False
            WebDriverWait(driver, timeout=wait_rm_frame).until(EC.visibility_of_element_located((By.ID, "main1")))            
            basic_airlink.cslog(time.ctime(time.time())+" ===>> RM frame shows") 
        except:
            if update_type == 'Radio_Module_Firmware':
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Applying RM...")
                
            else: 
                basic_airlink.cslog(time.ctime(time.time())+" ===>> no RM frame")        
            try:
                result = True          
                WebDriverWait(driver, timeout=int(timer_wait_logout-wait_rm_frame)).\
                until(EC.visibility_of_element_located((By.ID, "aceMasterInn")))
            except:
                basic_airlink.cslog(str(sys.exc_info()))
                basic_airlink.cslog(time.ctime(time.time())+" ===>> Fail on wait log out")
                result = False
         
        finally:
            return result

    def _default_content_switch(self, driver):
        '''To switch to the default content frame
        
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
        '''Get the picture name showing in the update process
        
        Args: driver, step number
        
        Return: picture name
        '''
        try:
            pic_name = ""
            pic_elem = driver.find_element_by_xpath(".//div[@id='file_upload']/center[2]/div/div["+str(step_num)+"]/img")
            pic_name = pic_elem.get_attribute("src").split('/')[-1]
        except:
            basic_airlink.cslog("Can't get the picture", "RED")
        finally:
            return pic_name
        
    def _fw_update(self, path_list, skip_rm, fw_version=""):
        ''' This method will operate the update process in UI
        
        Args: ALEOSBuild
              RMBuild
              UpdateType
        
        Returns: None
        '''
        attempt_time = fwupdate_config_map["ATTEMPT_TIME"]
        step_timer = fwupdate_config_map["STEP_TIMER"]
        #Attempt count if the step is fail
        attemp_count_click_fw_btn = 0
        attemp_count_switch_frame = 0 
        attemp_count_get_type = 0 
        attemp_count_browse_file = 0 
        attemp_count_click_go = 0
        attemp_count_switch_content = 0 
                 
        while True:
            #Step1: Login to ACEManager      
            self._startUp()
            
            #Step2: Click firmware update button
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Clicking firmware update button")
            time.sleep(step_timer)
            if not self._fw_btn_click(self.driver):
                if attemp_count_click_fw_btn >= attempt_time:
                    result = "err_fw_btn_click"
                    break                    
                else:
                    attemp_count_click_fw_btn+=1
                    self.driver.quit()
                    continue
            
            #Step3: Switch to update frame
            time.sleep(step_timer)
            if not self._fw_frame_switch(self.driver):
                if attemp_count_switch_frame >= attempt_time:
                    result = "err_switch_frame"
                    break                    
                else:
                    attemp_count_switch_frame+=1
                    self.driver.quit()
                    continue
            
            #Step4: Get update type
            time.sleep(step_timer)
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Getting update type")
            if len(path_list) == 1:
                update_type = "Radio_Module_Firmware"
            else:
                update_type = "ALEOS_Software"
                 
            type_flag = self._get_update_type(self.driver, update_type)        
            if type_flag == -1:
                if attemp_count_get_type >= attempt_time:
                    result = "err_get_update_type"
                    break
                else:
                    attemp_count_get_type+=1
                    self.driver.quit()
                    continue                    
            
            #Step5: Browse update file from local machine
            time.sleep(step_timer)           
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Browsing update file")
            if not self._browse_fw_file(self.driver, path_list[0]):
                if attemp_count_browse_file >= attempt_time:
                    result = "err_browse_file"
                    break
                else:
                    attemp_count_browse_file+=1
                    self.driver.quit()
                    continue
            
            #Step6: Click "Update" button
            time.sleep(step_timer)           
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Clicking Go")
            if not self._fw_go_click(self.driver):
                if attemp_count_click_go >= attempt_time:
                    result = "err_click_go"
                    break
                else:
                    attemp_count_click_go+=1
                    self.driver.quit()
                    continue
            
            #For RM update sometime it will popup a window to ask you, click OK            
            try:
                self.driver.switch_to_alert().accept()
            except:
                pass
            
            #Step7: Switch to Default content frame
            time.sleep(step_timer)
            basic_airlink.clog(time.ctime(time.time())+" ===>> Waiting for updating process")                       
            if not self._default_content_switch(self.driver):
                if attemp_count_switch_content >= attempt_time:
                    result = "err_switch_content"
                    break
                else:
                    attemp_count_switch_content+=1
                    self.driver.quit()
                    continue
            
            #Step8: Pick the timer according to the update type, and wait for the defined time, if timeout, script will check 
            #the picture showing in each step and return which step has problem. 
            quit_flag = False
            error_flag = False
            error_msg = ""
            if not self._wait_update_process(self.driver, update_type, fw_version):
                if not "check.gif" in self._get_step_pic_name(self.driver, 1):
                    self.driver.quit()
                    continue
                if not "check.gif" in self._get_step_pic_name(self.driver, 2):
                    self.driver.quit()
                    continue
                
                #check Applying step if there is an error, then fail the test case.
                #If the RM update prompt appeared, then select the matched RM file and click update
                #Wait for the RM update, the rainbow chase light can be observed from the device.
                step_3_pic = self._get_step_pic_name(self.driver, 3)
                if not "check.gif" in step_3_pic:
                    
                    #If the RM prompt is showing at the third step. The script will pick the RM file and click "Update"
                    if not self._rm_update(self.driver, path_list[1], skip_rm=skip_rm):
                        if "warning.gif" in step_3_pic:
                            basic_airlink.cslog("Applying Step ===> Warning picture...", "RED")
                            error_element = self.driver.find_element_by_xpath(\
                                            ".//div[@id='file_upload']/center[2]/div/div[3]/div[2]")
                            error_msg = error_element.text
                            basic_airlink.cslog("Applying Step ===> "+error_msg, "RED")
                            error_flag = True
                        self.driver.quit()
                    quit_flag = True
                    break
            break
        
        #Once the date is done, jump back to login page, the reboot timer starts
        if not error_flag:
            time.sleep(step_timer)                   
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Done ALEOS Updating")
            basic_airlink.cslog(time.ctime(time.time())+" ===>> Rebooting ...")
            reboot_time= tbd_config_map[self.device_name]["REBOOT_TIMEOUT"]
            time.sleep(reboot_time)
            result = "completed"
        else:
            basic_airlink.cslog("Error, test case failed...", "RED")
            result = "Error message: "+ error_msg
        if not quit_flag:
            self.driver.quit()     
        return result
    

#===========================================================================
#Helper functions AT Command
#===========================================================================
    def _execute_at_fw_update(self, update_fw_version):
        ''' This method will call the firmware update function in the library
        
        Args: update_fw_version
        
        Returns: None
        '''
        result = False
        at_ins = at_utilities.AtCommands()
        self.current_fw_version = self._aleos_check()
        basic_airlink.clog(time.ctime(time.time())+" ===>> Current ALEOS Version: "+self.current_fw_version)

        fw_filename = self._get_device_prefix()+"_"+update_fw_version+".bin"
        basic_airlink.cslog(time.ctime(time.time())+\
                            " ===>> Step:  Start running the *fwupdate command")
        attempt_count = 1

        while (not self.conn_ins.connect()) and (attempt_count<=5):
            aleos_version = -1
            attempt_count+=1
            basic_airlink.clog(time.ctime(time.time())+\
                               " ===>> _execute_at_fw_update: Connection Failed, try again")
        
        #Check what current ALEOS version is, the command format is different between 4.3.4 and 4.3.5 
        version_match_result = re.match(r'[4]\.[3]\.[2-4]', self.current_fw_version)
        if version_match_result is None:
            basic_airlink.cslog(time.ctime(time.time())+" ===>> filename needed")
            cmd_return = at_ins.fw_update(self.conn_ins, \
                             self.ftp_server_ip, \
                             self.ftp_username, \
                             self.ftp_password, \
                             fw_filename=fw_filename)            
        else:
            basic_airlink.cslog(time.ctime(time.time())+" ===>> filename changed to fw.bin")
            self._change_fw_filename(fw_filename)
            cmd_return = at_ins.fw_update(self.conn_ins, \
                             self.ftp_server_ip, \
                             self.ftp_username, \
                             self.ftp_password)

        if not "failed" in cmd_return:
            result = True
            basic_airlink.cslog("Command result: "+cmd_return)
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> Step:  Finished update, wait reboot...")
            time.sleep(tbd_config_map[self.device_name]["REBOOT_TIMEOUT"])
        return result
          
    def _execute_at_rm_update(self, update_rm_version):
        ''' 
        This method will call the firmware update function in the library
        
        Args: update_rm_version
        
        Returns: None
        '''
        result = False
        at_ins = at_utilities.AtCommands()
        self.current_fw_version = self._aleos_check()
        rm_filename = update_rm_version + ".bin"
        attempt_count = 1

        while (not self.conn_ins.connect()) and (attempt_count<=5):
            aleos_version = -1
            attempt_count+=1
            basic_airlink.clog(time.ctime(time.time())+\
                               " ===>> _execute_at_rm_update: Connection Failed, try again")
                  
        basic_airlink.cslog(time.ctime(time.time())+\
                            " ===>> Step:  Start running the *rmupdate command")
        cmd_return = at_ins.rm_update(self.conn_ins, \
                                  self.ftp_server_ip, \
                                  self.ftp_username, \
                                  self.ftp_password, \
                                  rm_filename)
        
        basic_airlink.cslog("Command Return: "+cmd_return, "BLUE")
        
        if not "failed" in cmd_return:
            result = True
            basic_airlink.cslog("Command result: "+cmd_return)
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> Step:  Finished update, wait reboot...")
            time.sleep(tbd_config_map[self.device_name]["RM_TIMEOUT"])
        return result
    
    def _execute_at_fw_rm_update(self, update_fw_version, update_rm_version):
        ''' 
        This method will call the firmware update function in the library
        
        Args: None
        
        Returns: None
        '''
        result = False        
        at_ins = at_utilities.AtCommands()
        current_aleos_version = self._aleos_check()
        device_prefix = self._get_device_prefix()
        fw_filename = device_prefix +"_"+ update_fw_version + ".bin"
        rm_filename = update_rm_version + ".bin"
        
        basic_airlink.cslog(time.ctime(time.time())+" ===>>fw update to: "+fw_filename)
        basic_airlink.cslog(time.ctime(time.time())+" ===>>rm update to: "+rm_filename)
        
        attempt_count = 1
        while (not self.conn_ins.connect()) and (attempt_count<=5):
            aleos_version = -1
            attempt_count+=1
            basic_airlink.clog(time.ctime(time.time())+\
                               " ===>> _execute_at_fwrm_update: Connection Failed, try again")
        
        basic_airlink.cslog(time.ctime(time.time())+\
                            " ===>> Step:  Start running the *fwrmupdate command")
        cmd_return = at_ins.fw_rm_update(self.conn_ins, \
                                     self.ftp_server_ip, \
                                     self.ftp_username, \
                                     self.ftp_password, \
                                     fw_filename, \
                                     rm_filename)
        
        if not "failed" in cmd_return:
            result = True
            basic_airlink.cslog("Command result: "+cmd_return)
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> Step:  Finished update, wait reboot...")
            time.sleep(tbd_config_map[self.device_name]["RM_TIMEOUT"]+\
                       tbd_config_map[self.device_name]["REBOOT_TIMEOUT"])
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
            basic_airlink.cslog(time.ctime(time.time())+\
                                " ===>> Change file name:"+fw_filename+" to fw.bin")
#            os.remove(airlinkautomation_home_dirname + '\\data\\builds\\RmFwImages\\fw.bin')
            shutil.copyfile(airlinkautomation_home_dirname + '\\data\\builds\\' + fw_filename, 
                            airlinkautomation_home_dirname + '\\data\\builds\\fw.bin')
        except:
            result = False
            basic_airlink.cslog("Fail on change filename", "RED")
        
        return result

