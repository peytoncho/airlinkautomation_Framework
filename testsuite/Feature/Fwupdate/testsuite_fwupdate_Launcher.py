#################################################################################
#
# This module is main part of Firmware update test automation, 
# and run the specified testcases.
# Company: Sierra Wireless
# Time: Jun 26, 2013
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

import ts_fwupdate_ui
import ts_fwupdate_at_commands

test_area = "Fwupdate"
test_sub_area=""
tbd_config_map, fwupdate_config_map = basic_airlink.get_config_data(test_area,"")

tc_ts_map={
    1:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_single",0],
    2:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_roundtrip",0],
    3:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_GX400_MC8705_OSM",0],
    4:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_GX400_MC8705_ATT",0],
    5:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_GX400_MC8705_BEL",0],
    6:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_GX400_MC8705_TLS",0],
    7:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_GX410_MC8705_OSM",0],
    8:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_GX400_MC5728_VZW",0],
    9:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_GX440_MC7750_VZW",0],
    10:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_GX440_MC7700_ATT",0],
    11:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_GX400_MC5728_SPT",0],
    12:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_GX440_MC7700_OSM",0],
    13:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_ES440_MC7750_VZW",0],
    14:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_ES440_MC7700_ATT",0],
    15:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_ES440_MC7710_OSM",0],
    16:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_ES440_MC7700_OSM",0],
    17:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_GX440_MC7700_OSM",0],
    18:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_LS300_SL5011_VZW",0],
    19:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_LS300_SL5011_SPT",0],
    20:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_LS300_SL8090_ATT",0],
    21:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_LS300_SL8090_BEL",0],
    22:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_LS300_SL8092_OSM",0],
    23:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_local_single",0],
    24:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_local_roundtrip",0],
    25:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_rm_update_local",0],
    26:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fw_rm_update_local",0],
    27:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_GX400_MC8705_OSM",0],
    28:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_GX400_MC8705_ATT",0],
    29:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_GX400_MC8705_BEL",0],
    30:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_GX400_MC8705_TLS",0],
    31:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_GX410_MC8705_OSM",0],
    32:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_GX400_MC5728_VZW",0],
    33:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_GX440_MC7750_VZW",0],
    34:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_GX440_MC7700_ATT",0],
    35:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_GX400_MC5728_SPT",0],
    36:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_GX440_MC7700_OSM",0],
    37:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_ES440_MC7750_VZW",0],
    38:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_ES440_MC7700_ATT",0],
    39:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_ES440_MC7710_EMEA",0],
    40:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_ES440_MC7700_OSM",0],
    41:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_GX440_MC7700_OSM",0],
    42:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_LS300_SL5011_VZW",0],
    43:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_LS300_SL5011_SPT",0],
    44:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_LS300_SL8090_ATT",0],
    45:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_LS300_SL8090_BEL",0],
    46:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_LS300_SL8092_OSM",0],
    47:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_sp_LS300",0],
    48:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_GX440_MC7700_BEL",0],          
}


def readCombo(testing_combo):
    combo_list = fwupdate_config_map[testing_combo]
    print str(combo_list)
    return combo_list

def pickTestcase(combo_list):
    pick_list = []
    for device in combo_list:
        for keys in tc_ts_map:
            if device[4:] in tc_ts_map[keys][1] and tc_ts_map[keys][0] is ts_fwupdate_ui.TsFwupdateUi:
                pick_list.append(keys)
    print str(pick_list)
    return pick_list

def dump_tc_list(combo_list):
    combo_map = {'COMBO_LIST' : combo_list}  
    stream = open('temp_fwupdate_tc_info.yml','w')
    yaml.dump(combo_map, stream, default_flow_style=True)
    stream.close()

####################################################
#  Firmware Update test automation main
####################################################

class Runner(object):
    def __init__(self,device="",test_type):
        self.device = device
        self.test_type = test_type
        if tbd_config_map["LOG_LEVEL"]=="DEBUG":
            self.LEVEL = logging.DEBUG
        else: 
            self.LEVEL = logging.INFO
        
        self.FORMAT ='%(asctime)-15s => %(levelname)-8s => %(message)s'
    
    def create_log_name(self):
        log_filename=basic_airlink.get_log_filename(tbd_config_map, test_area,"")          
        return log_filename
    
    def create_report_name(self):
        time_stamp = time.strftime("%b-%d-%Y_%H-%M")
        report_filename=basic_airlink.get_report_filename(tbd_config_map, test_area,"")
#        report_file_name = report_filename.split('/')[-1]
        return report_filename
    
    def run(self):
        log_filename = self.create_log_name()
        report_filename = self.create_report_name()
        fpp = file(report_filename, 'wb')
        logging.basicConfig(level = self.LEVEL,filename = log_filename, format=self.FORMAT,  filemode='w')
        description_text= r""" ***"""+ "log file name " +log_filename
        runner = htmlreport.HTMLTestRunner(
                stream = fpp,
                title = 'Firmware Update Test Report', 
                description = description_text
                )
        if self.test_type == "mdt":
            mySuite = basic_airlink.setup_suite_mdt(tc_ts_map, pick_list)
        else:
            mySuite = basic_airlink.setup_suite(tbd_config_map,fwupdate_config_map, tc_ts_map)
        test_cases = mySuite.countTestCases()   
        basic_airlink.slog("\x1b[0mTotal test cases: %d" % test_cases)
        test_result=runner.run(mySuite)
        fpp.close()
        basic_airlink.slog("\x1b[0mTotal %d test cases PASS." % test_result.success_count )
        basic_airlink.slog("Total %d test cases FAILED." % test_result.failure_count )
        basic_airlink.slog("Total %d test cases has ERROR." % test_result.error_count )   



class Launcher(object):
    def __init__(self,test_type):
        self.test_type = test_type
        if self.test_type == "mdt":
            self.mdt_ins = mdt_airlink.MdtAirlink.__init__()
    
    def run(self):
        if self.test_type == "mdt":
        
            #1, change all connected devices IP
            self.mdt_ins.change_global_ip()
            print "IP changed Waiting..."
            time.sleep(90)
         
            #2, check devices connection
            check_connection_flag = self.mdt_ins.ping_devices()
            if not check_connection_flag:
                sys.exit(2)
        
            #3, form the devices list 
            combo_list = mdt_ins.form_device_fullname()
        
            #4, pick the test case
            pick_list = pickTestcase(combo_list)
        
            #5,write the list to yml
            dump_tc_list(combo_list)
            
            device_list = []
                        
            for device in device_list:
                
                dev_runner = Runner(device,self.test_type).run()
        else:
             pass      
         
       

if __name__ == "__main__":
    if fwupdate_config_map["MDT"] == "YES":    
        test_type = "mdt"
    else:
        test_type = "single"
    
    Launcher(test_type).run()
    #mdt_ins.restore_device_ip()
    
