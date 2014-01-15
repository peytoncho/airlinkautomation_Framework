#################################################################################
#
# This module is main part of Admin test automation, and run the specified 
# testcases.
# Company: Sierra Wireless
# Time: Aug 13, 2013
# Author: Airlink
# 
#################################################################################

import logging
import os
import sys
import time

import htmlreport

import basic_airlink
import ts_vpn_at_commands
import ts_vpn_ipsec


test_area="VPN"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")

basic_airlink.append_sys_path()
tbd_config_map, vpn_config_map = basic_airlink.get_config_data(test_area,"")

#import ts_vpn_gre
#import ts_vpn_dpd
#import ts_vpn_large_packets
#import ts_vpn_ssl
#import ts_vpn_logging



# mapping info about test case/test module/testsuite class/selection
#          test module . test class       test case          flag of  test case selected 
tc_ts_map = {
    1:     [ts_vpn_at_commands.TsVpnAtCommands,"tc_ipsec_vpn1_commands",0],     
    2:     [ts_vpn_at_commands.TsVpnAtCommands,"tc_ipsec_vpn2_commands",0],
    3:     [ts_vpn_at_commands.TsVpnAtCommands,"tc_ipsec_vpn3_commands",0],
    4:     [ts_vpn_at_commands.TsVpnAtCommands,"tc_ipsec_vpn4_commands",0],     
    5:     [ts_vpn_at_commands.TsVpnAtCommands,"tc_ipsec_vpn5_commands",0],     
    6:     [ts_vpn_at_commands.TsVpnAtCommands,"tc_dummy",0],     
    7:     [ts_vpn_at_commands.TsVpnAtCommands,"tc_dummy",0], 
    8:     [ts_vpn_at_commands.TsVpnAtCommands,"tc_dummy",0],
    9:     [ts_vpn_at_commands.TsVpnAtCommands,"tc_dummy",0],     
    10:    [ts_vpn_at_commands.TsVpnAtCommands,"tc_dummy",0],                  
    11:    [ts_vpn_ipsec.TsVpnIpsec,"tc_ipsec_vpn1_ui_setting",0],
    12:    [ts_vpn_ipsec.TsVpnIpsec,"tc_dummy",0],
    13:    [ts_vpn_ipsec.TsVpnIpsec,"tc_dummy",0],
    14:    [ts_vpn_ipsec.TsVpnIpsec,"tc_ipsec_vpn4_ui_setting",0],
    15:    [ts_vpn_ipsec.TsVpnIpsec,"tc_dummy",0],
    16:    [ts_vpn_ipsec.TsVpnIpsec,"tc_dummy",0],
    17:    [ts_vpn_ipsec.TsVpnIpsec,"tc_dummy",0],
    18:    [ts_vpn_ipsec.TsVpnIpsec,"tc_dummy",0],
    19:    [ts_vpn_ipsec.TsVpnIpsec,"tc_dummy",0],
    20:    [ts_vpn_ipsec.TsVpnIpsec,"tc_dummy",0],
    21:    [ts_vpn_gre.TsVpnGre,"tc_dummy",0],

}
                     
     
####################################################
#  LAN test automation main
####################################################
if __name__ == "__main__":
    
#
#    airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
#
#    stream = open(airlinkautomation_home_dirname+'/config/testbed2Conf.yml', 'r')
#    tbd_config_map = yaml.load(stream)
#    stream.close()
    
    log_filename=basic_airlink.get_log_filename(tbd_config_map, "VPN","")
    FORMAT ='%(asctime)-15s => %(levelname)-8s => %(message)s'
    if tbd_config_map["LOG_LEVEL"]=="DEBUG":
        LEVEL = logging.DEBUG
    else: 
        LEVEL = logging.INFO 
    logging.basicConfig(level = LEVEL,filename = log_filename, format=FORMAT,  filemode='w') 
        
#    fo=open(airlinkautomation_home_dirname+'/testsuite/Feature/VPN/vp_test_conf.yml','r')
#    vpn_config_map = yaml.load(fo)
#    fo.close()

    time_stamp = time.strftime("%b-%d-%Y_%H-%M")

    report_filename=basic_airlink.get_report_filename(tbd_config_map, "VPN","")

    fpp = file(report_filename, 'wb')
    
    description_text= r""" ***"""+ "log file name " +log_filename 
    
    runner = htmlreport.HTMLTestRunner(
                stream = fpp,
                title = 'VPN Test Report', 
                description = description_text
                )    
    
    result = None

    mySuite=basic_airlink.setup_suite(vpn_config_map, tc_ts_map) 
    
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