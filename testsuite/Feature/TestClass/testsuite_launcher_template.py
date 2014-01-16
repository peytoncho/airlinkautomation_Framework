#################################################################################
#
# This 
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

#Import ts file here
import ts_template

test_area = "TestClass"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")

basic_airlink.append_sys_path()
tbd_config_map, testclass_config_map = basic_airlink.get_config_data(test_area,"")

tc_ts_map={
    1:   [ts_template.TestSuiteTestClass,"tc_test_1",0],
    2:   [ts_template.TestSuiteTestClass,"tc_test_2",0],
    3:   [ts_template.TestSuiteTestClass,"tc_test_3",0],
    4:   [ts_template.TestSuiteTestClass,"tc_test_4",0],
              
}

####################################################
#  Test Class test automation main
####################################################

if __name__ == "__main__":
  
    log_filename=basic_airlink.get_log_filename(tbd_config_map, "TESTCLASS","")
    FORMAT ='%(asctime)-15s => %(levelname)-8s => %(message)s'
    if tbd_config_map["LOG_LEVEL"]=="DEBUG":
        LEVEL = logging.DEBUG
    else: 
        LEVEL = logging.INFO 
    logging.basicConfig(level = LEVEL,filename = log_filename, format=FORMAT,  filemode='w')     
    time_stamp = time.strftime("%b-%d-%Y_%H-%M")

    report_filename=basic_airlink.get_report_filename(tbd_config_map, "TESTCLASS","")
    fpp = file(report_filename, 'wb')    
    description_text= r""" ***"""+ "log file name " +log_filename 
    
    runner = htmlreport.HTMLTestRunner(
                stream = fpp,
                title = 'TestClass Test Report', 
                description = description_text
                )    
    
    result = None

    mySuite = basic_airlink.setup_suite(tbd_config_map, testclass_config_map, tc_ts_map)
    #mySuite = basic_airlink.setup_suite()
    
    test_cases = mySuite.countTestCases()
    
    basic_airlink.slog("Total test cases: %d" % test_cases)
    
    test_result=runner.run(mySuite, True, result)
    print test_result.result
    basic_airlink.slog("Total %d test cases PASS." % test_result.success_count )
    basic_airlink.slog("Total %d test cases FAILED." % test_result.failure_count )
    basic_airlink.slog("Total %d test cases has ERROR." % test_result.error_count )    
    
    if (test_result.error_count + test_result.failure_count): 
        sys.exit(1)
    else:
        sys.exit(0)        
