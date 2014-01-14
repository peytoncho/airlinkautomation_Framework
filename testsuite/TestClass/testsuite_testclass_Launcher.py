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
import datetime

import htmlreport
import basic_airlink
import shutil
import ftp_sender

#Import ts file here
import ts_testClass1


test_area = "TestClass"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")

basic_airlink.append_sys_path()
tbd_config_map, testclass_config_map = basic_airlink.get_config_data(test_area,"")

tc_ts_map={
    1:   [ts_testClass1.TsTestClass1,"test_1",0],
    2:   [ts_testClass1.TsTestClass1,"test_2",0],
    3:   [ts_testClass1.TsTestClass1,"test_3",0],
    4:   [ts_testClass1.TsTestClass1,"test_4",0],
    5:   [ts_testClass1.TsTestClass1,"test_5",0],
    6:   [ts_testClass1.TsTestClass1,"test_6",0],
              
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
    report_file_name = report_filename.split('/')[-1]
    log_file_name = log_filename.split('/')[-1]
    fpp = file(report_filename, 'wb')    
    description_text= r""" ***"""+ "log file name " +log_filename 
     
    
    runner = htmlreport.HTMLTestRunner(
                stream = fpp,
                title = 'TestClass Test Report', 
                description = description_text
                )    
    

    
    mySuite = basic_airlink.setup_suite_v2(testclass_config_map, tc_ts_map)
    #mySuite = ts_testClass1.setup_suite()
    
    
    test_cases = mySuite.countTestCases()
    
    print "\x1b[0mTotal test cases: %d" % test_cases 
    #resultTest1 = mySuite.run(resultTest1)
            
    test_result=runner.run(mySuite)
            
    #print test_result.result  
    print "Total %d test cases PASS." % test_result.success_count
    print "Total %d test cases FAILED." % test_result.failure_count 
    print "Total %d test cases has ERROR." % test_result.error_count
    fpp.close()
#     os.chdir("C:\\airlinkautomation\\results")
#     csv_path = airlinkautomation_home_dirname+'/results/csv/'
#     test_area = 'Fwupdate'
    
#     if not basic_airlink.upload_report(test_area, report_file_name):
#         print "Fail on upload report"
#         sys.exit(0)
#     if not basic_airlink.make_csv(csv_path ,test_result, testclass_config_map):
#         print "Fail on make csvt"
#         sys.exit(0)
    
    

#     sys.stdout.write("\nFor details of the results please check \n"+basic_airlink.get_report_url(test_area, report_file_name)+'\n\n')
    
       
    if (test_result.error_count + test_result.failure_count):
        sys.exit(1)
    else:
        sys.exit(0)

