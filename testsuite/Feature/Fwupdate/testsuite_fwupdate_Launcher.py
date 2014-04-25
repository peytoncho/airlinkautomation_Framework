#################################################################################
#
# This module is main part of Firmware update test automation, 
# and run the specified testcases.
# Company: Sierra Wireless
# Time: Apr 25, 2014
# Author: Airlink
# 
#################################################################################

import logging
import os
import sys
import time
import shutil
import htmlreport
import basic_airlink
import mdt_airlink
import yaml
import datetime

import ts_fwupdate_ui
import ts_fwupdate_at_commands

test_area = "Fwupdate"
test_sub_area=""
tbd_config_map, fwupdate_config_map = basic_airlink.get_config_data(test_area,"")


def dump_tc_list(combo_list,processing_index):
    combo_map = {'COMBO_LIST' : combo_list,
                 'PROCESSING_INDEX': processing_index}  
    stream = open('temp_fwupdate_tc_info.yml','w')
    yaml.dump(combo_map, stream, default_flow_style=True)
    stream.close()

####################################################
#  Firmware Update test automation main
####################################################
class Runner(object):
    def __init__(self,device = tbd_config_map["DUTS"][0], test_type = None):
        self.device_name = device
        self.test_type = test_type
        if tbd_config_map["LOG_LEVEL"]=="DEBUG":
            self.LEVEL = logging.DEBUG
        else: 
            self.LEVEL = logging.INFO
        
        self.FORMAT ='%(asctime)-15s => %(levelname)-8s => %(message)s'
        self.tc_ts_map={
                        #Local test cases for UI and AT Command
                        1:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_single_aleos",0],
                        2:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_roundtrip_aleos",0],
                        3:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_single_rm_customize",0], 
                        4:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_roundtrip_rm_customize",0],
                        5:   [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_local_single_aleos",0],
                        6:   [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_local_roundtrip_aleos",0],
                        7:   [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_local_single_rm",0],
                        8:   [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_local_roundtrip_rm",0],
                        9:   [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_local_single_aleos_rm",0],                       
                        10:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_local_roundtrip_aleos_rm",0],                        
                        
                        #OTA test cases for UI and AT Command
                        11:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_ota_single_aleos",0],
                        12:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_ota_roundtrip_aleos",0],                       
                        13:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_ota_single_rm",0],
                        14:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_ota_roundtrip_rm",0],                       
                        15:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_ota_single_aleos",0],
                        16:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_ota_roundtrip_aleos",0],
                        17:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_ota_single_rm",0],
                        18:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_ota_roundtrip_rm",0],
                        19:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_ota_single_aleos_rm",0],                       
                        20:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_ota_roundtrip_aleos_rm",0],                       

                        #Additional test cases
                        21:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_single_aleos_skip_rm",0],
                        22:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_roundtrip_aleos_skip_rm",0],
#                        23:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_single_rm_designate",0], 
#                        24:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_roundtrip_rm_designate",0],                                         
                        }
    
    def create_log_name(self):
        log_filename=basic_airlink.get_log_filename(tbd_config_map, test_area,"")          
        return log_filename
    
    def create_report_name(self):
        time_stamp = time.strftime("%b-%d-%Y_%H-%M")
        current_date_str = str(datetime.datetime.now().date())
        current_time_str = str(datetime.datetime.now().time()).replace(":","-")
        airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME']
        slash = "\\" if sys.platform == 'win32' else "/"
        device_name = self.device_name
                
        report_filename = airlinkautomation_home_dirname+slash+"results"+slash+current_date_str+"_"+ \
                            current_time_str+"_"+ device_name +"_" + \
                            tbd_config_map[device_name]["ALEOS_FW_VER"]+ "_"+ \
                            "Fwupdate_testsuite.html"
        return report_filename
    
    def run(self):
        log_filename = self.create_log_name()
        report_filename = self.create_report_name()
        fpp = file(report_filename, 'wb')
        logging.basicConfig(level = self.LEVEL,filename = log_filename, format=self.FORMAT,  filemode='w')
#        description_text= r""" ***"""+ "log file name " +log_filename
        description_text=""
        runner = htmlreport.HTMLTestRunner(
                stream = fpp,
                title = 'Firmware Update Test Report', 
                description = description_text
                )
        if self.test_type == "mdt":
            tbd_config_map["DUTS"][0] = self.device_name
            mySuite = basic_airlink.setup_suite(tbd_config_map,fwupdate_config_map, self.tc_ts_map)
        else:
            mySuite = basic_airlink.setup_suite(tbd_config_map,fwupdate_config_map, self.tc_ts_map)
           
        test_cases = mySuite.countTestCases()   
        basic_airlink.slog("\x1b[0mTotal test cases: %d" % test_cases)
        test_result=runner.run(mySuite,fail_flag=tbd_config_map["TERMINATE_ON_FAIL"])
        fpp.close()
        basic_airlink.slog("\x1b[0mTotal %d test cases PASS." % test_result.success_count )
        basic_airlink.slog("Total %d test cases FAILED." % test_result.failure_count )
        basic_airlink.slog("Total %d test cases has ERROR." % test_result.error_count )
        
        airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME']
        csv_file_path = airlinkautomation_home_dirname+'/results/csv/'
        basic_airlink.make_csv(csv_file_path, test_result, fwupdate_config_map, self.tc_ts_map, note=self.device_name)   

class Launcher(object):
    def __init__(self,test_type):
        self.test_type = test_type
        if self.test_type == "mdt":
            self.mdt_ins = mdt_airlink.MdtAirlink(fwupdate_config_map["DEVICE_NUMBER"])
    
    def run(self):
        if self.test_type == "mdt":
        
            #1, change all connected devices IP
            self.mdt_ins.change_all_device_ip()
            print "IP changed Waiting..."
            time.sleep(110)
         
            #2, form the devices list            
            combo_list = self.mdt_ins.form_device_fullname()
                
            #3,write the list to yml             
            for device in combo_list:
                i = combo_list.index(device)
                dump_tc_list(combo_list,str(i+1))              
                Runner(device = device, test_type = self.test_type).run()
            self.mdt_ins.restore_device_ip()           
        else:
             Runner(test_type = self.test_type).run()      
         
if __name__ == "__main__":
     if fwupdate_config_map["MDT_LOCAL"] == "YES" :
         test_type = "mdt"
     else:
         test_type = "single"
     Launcher(test_type).run()
