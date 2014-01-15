import os
import sys
import time
import unittest
import htmlreport
import basic_airlink

test_area = "Fwupdate"
test_sub_area=""
tbd_config_map, fwupdate_config_map = basic_airlink.get_config_data(test_area,"")





#===============================================================================
# Launcher section
#===============================================================================
testing_combo = mdt_config_map["TESTING_COMBO"]

testcase_map = {
    1:[MultipleDeviceTest,"tc_fwupdate_GX400_MC8705_OSM",0],
    2:[MultipleDeviceTest,"tc_fwupdate_GX400_MC8705_ATT",0],
    3:[MultipleDeviceTest,"tc_fwupdate_GX400_MC8705_BEL",0],
    4:[MultipleDeviceTest,"tc_fwupdate_GX400_MC8705_TLS",0],
    5:[MultipleDeviceTest,"tc_fwupdate_GX410_MC8705_OSM",0],
    6:[MultipleDeviceTest,"tc_fwupdate_GX400_MC5728_VZW",0],
    7:[MultipleDeviceTest,"tc_fwupdate_GX440_MC7750_VZW",0],
    8:[MultipleDeviceTest,"tc_fwupdate_GX440_MC7700_ATT",0],
    9:[MultipleDeviceTest,"tc_fwupdate_GX400_MC5728_SPT",0],
    10:[MultipleDeviceTest,"tc_fwupdate_GX440_MC7700_OSM",0],
    11:[MultipleDeviceTest,"tc_fwupdate_ES440_MC7750_VZW",0],
    12:[MultipleDeviceTest,"tc_fwupdate_ES440_MC7700_ATT",0],
    13:[MultipleDeviceTest,"tc_fwupdate_ES440_MC7710_EMEA",0],
    14:[MultipleDeviceTest,"tc_fwupdate_ES440_MC7700_OSM",0],
    15:[MultipleDeviceTest,"tc_fwupdate_GX440_MC7700_OSM",0],
    16:[MultipleDeviceTest,"tc_fwupdate_LS300_SL5011_VZW",0],
    17:[MultipleDeviceTest,"tc_fwupdate_LS300_SL5011_SPT",0],
    18:[MultipleDeviceTest,"tc_fwupdate_LS300_SL8090_ATT",0],
    19:[MultipleDeviceTest,"tc_fwupdate_LS300_SL8090_BEL",0],
    20:[MultipleDeviceTest,"tc_fwupdate_LS300_SL8092_OSM",0],
}

if testing_combo == "DEVICE_COMBO1":
    argss = "1-5"    
elif testing_combo == "DEVICE_COMBO2":
    argss = "6-10"
elif testing_combo == "DEVICE_COMBO3":
    argss = "11-15"
else:
    argss = "16-20"
    
IP_map = {
      1: "192.168.13.1",
      2: "192.168.13.2",         
      3: "192.168.13.3",
      4: "192.168.13.4",
      5: "192.168.13.5",      
    }


if __name__ == "__main__":
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
    test_cases = mySuite.countTestCases()
    basic_airlink.slog("\x1b[0mTotal test cases: %d" % test_cases)
    mySuite = basic_airlink.setup_suite(tbd_config_map, fwupdate_config_map, tc_ts_map)    
    test_result=runner.run(mySuite)
    fpp.close()
    basic_airlink.slog("\x1b[0mTotal %d test cases PASS." % test_result.success_count )
    basic_airlink.slog("Total %d test cases FAILED." % test_result.failure_count )
    basic_airlink.slog("Total %d test cases has ERROR." % test_result.error_count )
    
    





    
    
     