'''
Created on Oct 25, 2013

@author: Henry
'''
import time
import sys
import os
import logging

test_area="VPN"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")
sys.path.append(airlinkautomation_home_dirname+"/lib/site-packages")
sys.dont_write_bytecode = True

import yaml
import basic_airlink
import htmlreport

import ts_vpn

tc_ts_map = {
    0:[ts_vpn.TsVpn,"tc_dummy",0],
    1:[ts_vpn.TsVpn,"tc_gre_vpn_default_case",0],
    2:[ts_vpn.TsVpn,"tc_ipsec_vpn_ike_encryption_mismatch",0],
    3:[ts_vpn.TsVpn,"tc_ipsec_vpn_ike_authentication_mismatch",0],
    4:[ts_vpn.TsVpn,"tc_ipsec_vpn_ike_dh_group_mismatch",0],
    5:[ts_vpn.TsVpn,"tc_ipsec_vpn_ipsec_encryption_mismatch",0],
    6:[ts_vpn.TsVpn,"tc_ipsec_vpn_ipsec_authentication_mismatch",0],
    7:[ts_vpn.TsVpn,"tc_ipsec_vpn_ipsec_dh_group_mismatch",0],
    10:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_30_bit_netmask",0],
    11:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_29_bit_netmask",0],
    12:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_28_bit_netmask",0],
    13:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_27_bit_netmask",0],
    14:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_26_bit_netmask",0],
    15:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_25_bit_netmask",0],
    16:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_24_bit_netmask",0],
    17:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_23_bit_netmask",0],
    18:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_22_bit_netmask",0],
    19:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_21_bit_netmask",0],
    20:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_20_bit_netmask",0],
    21:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_19_bit_netmask",0],
    22:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_18_bit_netmask",0],
    23:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_17_bit_netmask",0],
    24:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_16_bit_netmask",0],
    25:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_15_bit_netmask",0],
    26:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_14_bit_netmask",0],
    27:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_13_bit_netmask",0],
    28:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_12_bit_netmask",0],
    29:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_11_bit_netmask",0],
    30:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_10_bit_netmask",0],
    31:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_9_bit_netmask",0],
    32:[ts_vpn.TsVpn,"tc_ipsec_vpn_cisco_subnet_8_bit_netmask",0],
}
####################################################
#  VPN test automation main
####################################################
if __name__ == "__main__":

    tbd_config_map, vpn_config_map = basic_airlink.get_config_data("VPN", "")
    
    log_filename=basic_airlink.get_log_filename(tbd_config_map, "VPN","")
    FORMAT ='%(asctime)-15s => %(levelname)-8s => %(message)s'
    if tbd_config_map["LOG_LEVEL"]=="DEBUG":
        LEVEL = logging.DEBUG
    else: 
        LEVEL = logging.INFO 
    logging.basicConfig(level = LEVEL,filename = log_filename, format=FORMAT,  filemode='w') 
           
    time_stamp = time.strftime("%b-%d-%Y_%H-%M")

    report_filename=basic_airlink.get_report_filename(tbd_config_map, "VPN","")

    fpp = file(report_filename, 'wb')
    
    description_text= r""" ***"""+ "log file name " + log_filename 
    
    runner = htmlreport.HTMLTestRunner(
                stream = fpp,
                title = 'VPN Test Report', 
                description = description_text
                )    
    
    result = None
    
    mySuite=basic_airlink.setup_suite(tbd_config_map, vpn_config_map, tc_ts_map) 
    
    test_cases = mySuite.countTestCases()
    
    basic_airlink.slog("Total test cases: %d" % test_cases)
    
    test_result=runner.run(mySuite, True, result)

    basic_airlink.slog("Total %d test cases PASS." % test_result.success_count )
    basic_airlink.slog("Total %d test cases FAILED." % test_result.failure_count )
    basic_airlink.slog("Total %d test cases has ERROR." % test_result.error_count )    

    if tbd_config_map["VPN"]["AUTO_UPLOAD_RESULTS_TO_TEMP"] == "YES":
        # Upload html report to jenkins server
        if basic_airlink.upload_report(tbd_config_map, test_area, report_filename):
            print "Report: %s" %basic_airlink.get_report_url(tbd_config_map, test_area, report_filename.split('\\')[-1])
        else:
            print "Could not upload report to Jenkins"

       # Upload log file to jenkins server
        if basic_airlink.upload_report(tbd_config_map, test_area, log_filename):
            print "Log: %s" %basic_airlink.get_report_url(tbd_config_map, test_area, log_filename.split('\\')[-1])
        else:
            print "Could not upload log to Jenkins"
    else:
        print "AUTO_UPLOAD_RESULTS_TO_TEMP is set to \"NO\", not copying html/log files."

    if (test_result.error_count + test_result.failure_count): 
        sys.exit(1)
    else:
        sys.exit(0)
