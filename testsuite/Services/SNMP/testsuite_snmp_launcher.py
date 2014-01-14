#################################################################################
#
# This module is main part of SNMP test automation, and run the specified testcases.
# Company: Sierra Wireless
# Time: Sept 5, 2013
# Author: Airlink
# 
#################################################################################

import logging
import os
import sys
import time

import htmlreport

import basic_airlink
import ts_snmp_at_commands


test_area = "Services"
test_sub_area="SNMP"
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")

basic_airlink.append_sys_path()
tbd_config_map, snmp_config_map = basic_airlink.get_config_data(test_area,test_sub_area)

#import ts_snmp_trap
#import ts_snmp_version_2
#import ts_snmp_version_3
#import ts_snmp_ui_check_up

# mapping info about test case/test module/testsuite class/selection
#             test module . test class       test case          flag of  test case selected 
tc_ts_map = {
    1:      [ts_snmp_at_commands.TsSnmpAtCommands,"tc_snmp_v2_enable",0],
    2:      [ts_snmp_at_commands.TsSnmpAtCommands,"tc_snmp_v3_enable",0],
    3:      [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],
    4:      [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0], 
    5:      [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],
    6:      [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],
    7:      [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],
    8:      [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],
    9:      [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],
    10:     [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],     
    11:     [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],           
    12:     [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],                
    13:     [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],           
    14:     [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],           
    15:     [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],           
    16:     [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],         
    17:     [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],          
    18:     [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],           
    19:     [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],           
    20:     [ts_snmp_at_commands.TsSnmpAtCommands,"tc_dummy",0],           
#    21:     [ts_snmp_trap.TsSnmpTrap,"tc_dummy", 0],
#    22:     [ts_snmp_version_2.TsSnmpVersion2,"tc_dummy",0],
#    23:     [ts_snmp_version_3.TsSnmpVersion3,"tc_dummy",0],
#    24:     [ts_snmp_ui_check_up.TsSnmpUiCheckUp,"tc_dummy",0],
}
                   
####################################################
#  LAN test automation main
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
                title = test_area+' '+test_sub_area+' Automation Test Report', 
                description = description_text
                )    
    
    result = None

    mySuite=basic_airlink.setup_suite(snmp_config_map, tc_ts_map) 
    
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