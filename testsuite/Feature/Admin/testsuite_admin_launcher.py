#################################################################################
#
# This module is main part of Admin test automation, and run the specified 
# testcases.
# Company: Sierra Wireless
# Time: Aug 13, 2013
# 
#################################################################################

import logging
import os
import sys
import time

import htmlreport
import yaml

import basic_airlink
import ts_admin_advanced
import ts_admin_at_commands
import ts_admin_change_password
import ts_admin_logging


test_area="Admin"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")

basic_airlink.append_sys_path()
tbd_config_map, admin_config_map = basic_airlink.get_config_data(test_area,"")


# mapping info about test case/test module/testsuite class/selection
#          test module . test class       test case          flag of  test case selected 
tc_ts_map = {
    1:     [ts_admin_at_commands.TsAdminAtCommands,"tc_reset_to_factory_default",0],     
    2:     [ts_admin_at_commands.TsAdminAtCommands,"tc_atz_reboot",0],
    3:     [ts_admin_at_commands.TsAdminAtCommands,"tc_block_reset_config",0],
    4:     [ts_admin_at_commands.TsAdminAtCommands,"tc_boardtemp_and_powerinput",0],     
    5:     [ts_admin_at_commands.TsAdminAtCommands,"tc_at_ping",0],     
    6:     [ts_admin_at_commands.TsAdminAtCommands,"tc_date_time",0],     
    7:     [ts_admin_at_commands.TsAdminAtCommands,"tc_status_update_commands",0], 
    8:     [ts_admin_at_commands.TsAdminAtCommands,"tc_dummy",0],
    9:     [ts_admin_at_commands.TsAdminAtCommands,"tc_dummy",0],     
    10:    [ts_admin_at_commands.TsAdminAtCommands,"tc_dummy",0],      
    11:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_logging_wan_celluar_debug_display_yes",0],
    12:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_logging_wan_celluar_debug_display_no",0],
    13:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_logging_wan_celluar_info_display_yes",0],
    14:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_logging_wan_celluar_info_display_no",0], 
    15:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_logging_wan_celluar_error_display_yes",0],
    16:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_logging_wan_celluar_error_display_no",0],
    17:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_logging_wan_celluar_critical_display_yes",0],
    18:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_logging_wan_celluar_critical_display_no",0],
    19:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_logging_lan_debug_display_yes",0],
    20:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_logging_lan_debug_display_no",0], 
    21:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_logging_lan_info_display_yes", 0],
    22:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_logging_lan_info_display_no",0],
    23:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_logging_lan_error_display_yes",0],
    24:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_logging_lan_error_display_no",0],
    25:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_logging_lan_critical_display_yes",0],
    26:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_logging_lan_critical_display_no",0],
    27:     [ts_admin_logging.TsAdminLogging,"tc_ui_logging_all_critical_display_yes",0],  
    28:     [ts_admin_logging.TsAdminLogging,"tc_ui_logging_all_critical_display_no",0],  
    29:     [ts_admin_logging.TsAdminLogging,"tc_ui_logging_all_error_display_yes",0],    
    30:     [ts_admin_logging.TsAdminLogging,"tc_ui_logging_all_error_display_no",0], 
    31:     [ts_admin_logging.TsAdminLogging,"tc_ui_logging_all_info_display_yes",0],    
    32:     [ts_admin_logging.TsAdminLogging,"tc_ui_logging_all_info_display_no",0], 
    33:     [ts_admin_logging.TsAdminLogging,"tc_ui_logging_all_debug_display_yes",0],    
    34:     [ts_admin_logging.TsAdminLogging,"tc_ui_logging_all_debug_display_no",0], 
    35:     [ts_admin_logging.TsAdminLogging,"tc_ui_config_linux_sys_log",0],
    35:     [ts_admin_logging.TsAdminLogging,"tc_dummy",0],   #TODO
    36:     [ts_admin_logging.TsAdminLogging,"tc_dummy",0],
    37:     [ts_admin_logging.TsAdminLogging,"tc_dummy",0],
    38:     [ts_admin_logging.TsAdminLogging,"tc_dummy",0],
    39:     [ts_admin_logging.TsAdminLogging,"tc_dummy",0],
    40:     [ts_admin_logging.TsAdminLogging,"tc_dummy",0],
    41:     [ts_admin_advanced.TsAdminAdvanced,"tc_ui_factory_reset",0],
    42:     [ts_admin_advanced.TsAdminAdvanced,"tc_dummy",0],
    43:     [ts_admin_advanced.TsAdminAdvanced,"tc_dummy",0],
    44:     [ts_admin_advanced.TsAdminAdvanced,"tc_dummy",0],
    45:     [ts_admin_advanced.TsAdminAdvanced,"tc_dummy",0],
    46:     [ts_admin_advanced.TsAdminAdvanced,"tc_dummy",0],
    47:     [ts_admin_advanced.TsAdminAdvanced,"tc_dummy",0],
    48:     [ts_admin_advanced.TsAdminAdvanced,"tc_dummy",0],
    49:     [ts_admin_advanced.TsAdminAdvanced,"tc_dummy",0],
    50:     [ts_admin_advanced.TsAdminAdvanced,"tc_dummy",0],
    51:     [ts_admin_change_password.TsAdminChangePassword,"tc_ui_viewer_change_password",0],
    52:     [ts_admin_change_password.TsAdminChangePassword,"tc_ui_user_change_password",0],            

}
                     
     
####################################################
#  LAN test automation main
####################################################
if __name__ == "__main__":
    

    airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 

    stream = open(airlinkautomation_home_dirname+'/config/testbed2Conf.yml', 'r')
    tbd_config_map = yaml.load(stream)
    stream.close()
    
    log_filename=basic_airlink.get_log_filename(tbd_config_map, "Admin","")
    FORMAT ='%(asctime)-15s => %(levelname)-8s => %(message)s'
    if tbd_config_map["LOG_LEVEL"]=="DEBUG":
        LEVEL = logging.DEBUG
    else: 
        LEVEL = logging.INFO 
    logging.basicConfig(level = LEVEL,filename = log_filename, format=FORMAT,  filemode='w') 
        
    fo=open(airlinkautomation_home_dirname+'/testsuite/Feature/Admin/admin_test_conf.yml','r')
    admin_config_map = yaml.load(fo)
    fo.close()

    time_stamp = time.strftime("%b-%d-%Y_%H-%M")

    report_filename=basic_airlink.get_report_filename(tbd_config_map, "Admin","")

    fpp = file(report_filename, 'wb')
    
    description_text= r""" ***"""+ "log file name " +log_filename 
    
    runner = htmlreport.HTMLTestRunner(
                stream = fpp,
                title = 'Admin Automation Test Report', 
                description = description_text
                )    
    
    result = None

    mySuite=basic_airlink.setup_suite(admin_config_map, tc_ts_map) 
    
    test_cases = mySuite.countTestCases()
    
    basic_airlink.slog("Total test cases: %d" % test_cases)
    
    test_result=runner.run(mySuite, True, result)

    basic_airlink.slog("Total %d test cases PASS." % test_result.success_count )
    basic_airlink.slog("Total %d test cases FAILED." % test_result.failure_count )
    basic_airlink.slog("Total %d test cases has ERROR." % test_result.error_count )    
    
    if (test_result.error_count + test_result.failure_count): 
        sys.exit(1)
    else:
        sys.exit(0)