#################################################################################
#
# This module is main part of LAN test automation, and run the specified testcases.
# Company: Sierra Wireless
# Time: Jun 26, 2013
# Author: Airlink
# 
#################################################################################

import logging
import os
import sys
import time

import htmlreport

import basic_airlink
import ts_lan_at_commands
import ts_lan_dhcp_addressing


test_area = "LAN"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")

basic_airlink.append_sys_path()
tbd_config_map, lan_config_map = basic_airlink.get_config_data(test_area,"")


# mapping info about test case/test module/testsuite class/selection
#             test module . test class       test case          flag of  test case selected 
tc_ts_map = {
    1:      [ts_lan_at_commands.TsLanAtCommands,"tc_ethernet_dhcp_commands",0],
    2:      [ts_lan_at_commands.TsLanAtCommands,"tc_ethernet_state",0],
    3:      [ts_lan_at_commands.TsLanAtCommands,"tc_ethernet_mac",0],
    4:      [ts_lan_at_commands.TsLanAtCommands,"tc_global_dns",0], 
    5:      [ts_lan_at_commands.TsLanAtCommands,"tc_ppoe_commands",0],
    6:      [ts_lan_at_commands.TsLanAtCommands,"tc_dual_eth_state",0],
    7:      [ts_lan_at_commands.TsLanAtCommands,"tc_dual_eth_mac",0],
    8:      [ts_lan_at_commands.TsLanAtCommands,"tc_dummy",0],
    9:      [ts_lan_at_commands.TsLanAtCommands,"tc_dummy",0],
    10:     [ts_lan_at_commands.TsLanAtCommands,"tc_dummy",0],     
    11:     [ts_lan_at_commands.TsLanAtCommands,"tc_wifi_mode",0],           
    12:     [ts_lan_at_commands.TsLanAtCommands,"tc_wifi_mac",0],                
    13:     [ts_lan_at_commands.TsLanAtCommands,"tc_wifi_apbridged",0],           
    14:     [ts_lan_at_commands.TsLanAtCommands,"tc_wifi_apchannel",0],           
    15:     [ts_lan_at_commands.TsLanAtCommands,"tc_wifi_apen",0],           
    16:     [ts_lan_at_commands.TsLanAtCommands,"tc_wifi_ap_max_client",0],         
    17:     [ts_lan_at_commands.TsLanAtCommands,"tc_wifi_ap_security_type",0],          
    18:     [ts_lan_at_commands.TsLanAtCommands,"tc_wifi_ap_tx_power",0],           
    19:     [ts_lan_at_commands.TsLanAtCommands,"tc_wifi_ap_dhcp_commands",0],           
    20:     [ts_lan_at_commands.TsLanAtCommands,"tc_wifi_ap_ssid_commands",0],           
    21:     [ts_lan_dhcp_addressing.TsLanDhcpAddressing,"tc_all_hosts_use_private_ips_default", 0],
    22:     [ts_lan_dhcp_addressing.TsLanDhcpAddressing,"tc_ethernet_uses_public_ip",0],
    23:     [ts_lan_dhcp_addressing.TsLanDhcpAddressing,"tc_usb_uses_public_ip",0],
    24:     [ts_lan_dhcp_addressing.TsLanDhcpAddressing,"tc_ethernet_display_disable",0],
    25:     [ts_lan_dhcp_addressing.TsLanDhcpAddressing,"tc_dummy",0],

}
                   
####################################################
#  LAN test automation main
####################################################
if __name__ == "__main__":
    
    log_filename=basic_airlink.get_log_filename(tbd_config_map, "LAN","")
    FORMAT ='%(asctime)-15s => %(levelname)-8s => %(message)s'
    if tbd_config_map["LOG_LEVEL"]=="DEBUG":
        LEVEL = logging.DEBUG
    else: 
        LEVEL = logging.INFO 
    logging.basicConfig(level = LEVEL,filename = log_filename, format=FORMAT,  filemode='w') 

    time_stamp = time.strftime("%b-%d-%Y_%H-%M")

    report_filename=basic_airlink.get_report_filename(tbd_config_map, "LAN","")

    fpp = file(report_filename, 'wb')
    
    description_text= r""" ***"""+ "log file name " +log_filename 
    
    runner = htmlreport.HTMLTestRunner(
                stream = fpp,
                title = 'LAN Automation Test Report', 
                description = description_text
                )    
    
    result = None

    mySuite=basic_airlink.setup_suite(lan_config_map, tc_ts_map) 
    
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