#################################################################################
#
# This module is main part of WAN test automation, and run the specified 
# testcases.
# Company: Sierra Wireless
# Time: Oct 3, 2013
# 
#################################################################################

import time
import sys
import os
import logging
import unittest

test_area="WAN"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")

import basic_airlink
basic_airlink.append_sys_path()
tbd_config_map, wan_config_map = basic_airlink.get_config_data(test_area,"")

import htmlreport
import ts_wan_at_commands
import ts_wan_ui_basic
import ts_wan_pt_rssi

# mapping info about test case/test module/testsuite class/selection
#          test module . test class       test case          flag of  test case selected 
tc_ts_map = {
    1:     [ts_wan_at_commands.TsWanAtCommands,"tc_cdma_autoprl_and_autoprlfreq",0],
    2:     [ts_wan_at_commands.TsWanAtCommands,"tc_gsm_band",0],
    3:     [ts_wan_at_commands.TsWanAtCommands,"tc_diversity_commands",0],     
    4:     [ts_wan_at_commands.TsWanAtCommands,"tc_evdo_data_service",0],     
    5:     [ts_wan_at_commands.TsWanAtCommands,"tc_evdo_roam_pref",0],     
    6:     [ts_wan_at_commands.TsWanAtCommands,"tc_lte_signal_commands",0],     
    7:     [ts_wan_at_commands.TsWanAtCommands,"tc_net_allow_zero_ip",0],     
    8:     [ts_wan_at_commands.TsWanAtCommands,"tc_net_apn",0],     
    9:     [ts_wan_at_commands.TsWanAtCommands,"tc_net_watchog",0],     
    10:    [ts_wan_at_commands.TsWanAtCommands,"tc_username_password",0],     
    11:    [ts_wan_ui_basic.TsWanUiBasic,"tc_user_entered_apn",0],     
    12:    [ts_wan_ui_basic.TsWanUiBasic,"tc_user_entered_apn",0],     
    13:    [ts_wan_ui_basic.TsWanUiBasic,"tc_user_entered_apn",0],     
    14:    [ts_wan_ui_basic.TsWanUiBasic,"tc_user_entered_apn",0],     
    15:    [ts_wan_ui_basic.TsWanUiBasic,"tc_user_entered_apn",0],     
    16:    [ts_wan_ui_basic.TsWanUiBasic,"tc_user_entered_apn",0],     
    17:    [ts_wan_ui_basic.TsWanUiBasic,"tc_user_entered_apn",0], 
    18:    [ts_wan_pt_rssi.TsWanPtRssi, "tc_rssi_change",0],    
}
                     
     
####################################################
#  WAN test automation main
####################################################
if __name__ == "__main__":
    
    log_filename=basic_airlink.get_log_filename(tbd_config_map, test_area,test_sub_area)
    FORMAT ='%(asctime)-15s => %(levelname)-8s => %(message)s'
    if tbd_config_map["LOG_LEVEL"]=="DEBUG":
        LEVEL = logging.DEBUG
    else: 
        LEVEL = logging.INFO 
    logging.basicConfig(level = LEVEL,filename = log_filename, format=FORMAT,  filemode='w') 

    time_stamp = time.strftime("%b-%d-%Y_%H-%M")

    report_filename=basic_airlink.get_report_filename(tbd_config_map, test_area,test_sub_area)

    fpp = file(report_filename, 'wb')
    
    description_text= r""" ***"""+ "log file name " +log_filename 
    
    runner = htmlreport.HTMLTestRunner(
                stream = fpp,
                title = 'WAN Automation Test Report', 
                description = description_text
                )    
    
    result = None
    #result = unittest.TestResult()

    mySuite=basic_airlink.setup_suite(wan_config_map, tc_ts_map) 
    
    test_cases = mySuite.countTestCases()
    
    basic_airlink.slog("Total test cases: %d" % test_cases)
    #mySuite.run(result)
    test_result=runner.run(mySuite, True, result)
 
    basic_airlink.slog("Total %d test cases PASS." % test_result.success_count )
    basic_airlink.slog("Total %d test cases FAILED." % test_result.failure_count )
    basic_airlink.slog("Total %d test cases has ERROR." % test_result.error_count )    
     
    if (test_result.error_count + test_result.failure_count): 
        sys.exit(1)
    else:
        sys.exit(0)
