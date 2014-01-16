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


import ts_fwupdate_ui
import ts_fwupdate_at_commands

test_area = "Fwupdate"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME']
basic_airlink.append_sys_path()
tbd_config_map, fwupdate_config_map = basic_airlink.get_config_data(test_area,"")

tc_ts_map={
    1:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_single",0],  
    2:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_roundtrip",0],
    3:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_sp_LS300",0],
    4:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_sp_GX400",0],
    5:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_432a010_432a010I",0],
    6:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_432a010I_434009",0],
    7:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_432009_433014",0],
    8:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_432009_433a014",0],
    9:   [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_432a010_433014",0],
    10:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_432a010_433a014",0],
    11:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_432a010_434009",0],
    12:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_433a014_434009",0],
    13:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_433014_434009",0],   
    14:  [ts_fwupdate_ui.TsFwupdateUi,"tc_fwupdate_local_434008_434009",0],
    15:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_local_single",0],
    16:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_local_roundtrip",0],
    17:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_rm_update_local",0],
    18:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fw_rm_update_local",0],
    19:  [ts_fwupdate_at_commands.TsFwupdateAtCommands,"tc_fwupdate_local_434008_434009",0],             
}

####################################################
#  Firmware Update test automation main
####################################################

if __name__ == "__main__":
  
    log_filename=basic_airlink.get_log_filename(tbd_config_map, test_area,"")
    FORMAT ='%(asctime)-15s => %(levelname)-8s => %(message)s'
    if tbd_config_map["LOG_LEVEL"]=="DEBUG":
        LEVEL = logging.DEBUG
    else: 
        LEVEL = logging.INFO 
    logging.basicConfig(level = LEVEL,filename = log_filename, format=FORMAT,  filemode='w')    
    time_stamp = time.strftime("%b-%d-%Y_%H-%M")
    report_filename=basic_airlink.get_report_filename(tbd_config_map, test_area,"")
    report_file_name = report_filename.split('/')[-1]
    fpp = file(report_filename, 'wb')   
    description_text= r""" ***"""+ "log file name " +log_filename
          
    runner = htmlreport.HTMLTestRunner(
                stream = fpp,
                title = 'Firmware Update Test Report', 
                description = description_text
                )       

    
    mySuite = basic_airlink.setup_suite(tbd_config_map, fwupdate_config_map, tc_ts_map)    
    test_cases = mySuite.countTestCases()
    basic_airlink.slog("\x1b[0mTotal test cases: %d" % test_cases)
     
    test_result=runner.run(mySuite)
    basic_airlink.slog("\x1b[0mTotal %d test cases PASS." % test_result.success_count )
    basic_airlink.slog("Total %d test cases FAILED." % test_result.failure_count )
    basic_airlink.slog("Total %d test cases has ERROR." % test_result.error_count )
    fpp.close()
#    shutil.copyfile('C:'+report_filename, 'C:/jenkins/workspace/Firmware_update_test/reports/'+report_file_name)
#    sys.stdout.write("\nFor details of the results please check \n http://carmd-ev-aptest:8080/job/Firmware_update_test/ws/reports/%s\n\n For details of the log please check \n http://carmd-ev-aptest:8080/job/Firmware_update_test/ws/logs/%s\n\n"  % ( report_file_name,log_filename))    
    
    if (test_result.error_count + test_result.failure_count): 
        sys.exit(1)
    else:
        sys.exit(0)
