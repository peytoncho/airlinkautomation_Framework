import time
import sys
import os
import logging

test_area="VPN"
test_sub_area=""
sys.path.append(os.environ['AIRLINKAUTOMATION_HOME'] + "/lib/common")
sys.path.append(os.environ['AIRLINKAUTOMATION_HOME'] + "/lib/site-packages")
sys.path.append(os.environ['AIRLINKAUTOMATION_HOME'] + "/testsuite/Feature/VPN/auto_generated")

sys.dont_write_bytecode = True

import yaml
import basic_airlink
import htmlreport

import argparse

import vpn_default_tc_ts_map

####################################################
#  VPN test automation main
####################################################
def main():
    # Get test bed config
    tbd_config_map = basic_airlink.get_tbd_config_data()

    # Get vpn_config_map - the area_config_map isn't useful with these test cases
    # and it takes nearly up to a minute to read the entire file of useless data
    # This function creates a dummy map so other libraries would continue to work
    vpn_config_map = create_area_config_map() 
    
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
    
    mySuite=basic_airlink.setup_suite(tbd_config_map, vpn_config_map, vpn_default_tc_ts_map.tc_ts_map) 
    
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
        print "\n\n** AUTO_UPLOAD_RESULTS_TO_TEMP is set to \"NO\", not copying html/log files."

    if (test_result.error_count + test_result.failure_count): 
        sys.exit(1)
    else:
        sys.exit(0)

def create_area_config_map():
    area_config_map = {}
    area_config_map["LIST_TESTCASES"] = {}

    # parser command line arguments to get the combo numbers to be tested
    parser = argparse.ArgumentParser(description="testsuite launcher")
    
    parser.add_argument("-n", "--tc_no", dest = "tc_no_range_arg",
        help = "test case number range", default = "")
        
    args = parser.parse_args()

    default_config = {}
    default_config["TC_ID"] = "/Feature/VPN/IPsec/tc_ipsec_vpn"
    default_config["PRODUCT_VER"] = []
    default_config["OBSOLETE_VER"] = []
    default_config["TEST_TYPE"] = []
    default_config["DESCRIPTION"] = ""
    default_config["DEVICE_TYPE"] = ["GX440", "GX400", "LS300", "ES440"]
    default_config["RM_TYPE"] = []
    default_config["PRIORIY"] = "HIGH"
    default_config["TEST_AREA"] = "VPN"

    tc_list = [] # Only add to the dict if the test is selected by the -n argument
    for tc_range in args.tc_no_range_arg.replace("[","").replace("]","").replace(" ","").split(","):
        for tc in range(int(tc_range.split("-")[0]), int(tc_range.split("-")[-1]) + 1):
            area_config_map["LIST_TESTCASES"].setdefault(tc, default_config)

    return area_config_map

if __name__ == "__main__":
    main()
