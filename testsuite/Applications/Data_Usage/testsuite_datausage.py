#################################################################################
#
# This module automates data usage test cases. 
# Company: Sierra Wireless
# Time   : Jul 17, 2013
# Author : Airlink test team
#
#################################################################################

import datetime
import logging
import os
import sys
import time
import unittest

import htmlreport
import yaml

import at_utilities
import basic_airlink
import connectivity
import ftp_airlink
import msciids
import selenium_utilities


class TestsuiteDatausage(unittest.TestCase):
    ''' This class automates data usage test cases.
    
    '''
                                                              
    def setUp(self):
        ''' the test runner will run that method prior to each test
        
        Args: None
        
        Returns: None
        '''
        self.conn_ins = connectivity.Connectivity()       
        
        # step: check if devices ready    
        basic_airlink.slog("step: check if testbed is ready")
        self.conn_ins.testbed_ready()
        self.device_name = tbd_config_map["DUTS"][0]
        
        self.se_ins = selenium_utilities.SeleniumAcemanager()
        self.at_ins = at_utilities.AtCommands()   
        
        basic_airlink.slog("Step:  connect to DUT and generate connection instance by Telnet or USB or Serial or WiFi or OTA")
        self.connect_instance=self.conn_ins.connection_types()
        if not self.connect_instance.connect(): 
            basic_airlink.slog("Problem: testbed not ready yet")
            
        self.fail_flag = 0
        
        # step: login to Ace Manager 
        basic_airlink.slog("step: login to ACEmanager," + tbd_config_map[self.device_name]["ACE_URL"]+","+tbd_config_map[self.device_name]["USERNAME"]+","+tbd_config_map[self.device_name]["PASSWORD"])
        self.driver = self.se_ins.login(tbd_config_map[self.device_name]["ACE_URL"], tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])       
                    
  
    def tearDown(self):
        ''' the test runner will invoke that method after each test
        
        Args: None
        
        Returns: None
        '''        
        # Step: close the AceManager web
        basic_airlink.slog("step: close Firefox")  
        self.driver.quit()         
 
        basic_airlink.slog("Testcase complete")
        
                                 
    def tc_datausage_transfer_large_once(self):
        ''' Upload and download large file only one time, and get the rate of download and upload data
        ''' 
        
        # step: Connect to FTP server 
        basic_airlink.slog("step: Connect to FTP server ")                
        ftp_ins = ftp_airlink.FtpAirlink(1200)   # ftp timeout 20 min
        ret=ftp_ins.login(datausage_config_map["FTP_SERVER"]["ADDRESS"], datausage_config_map["FTP_SERVER"]["USERNAME"], datausage_config_map["FTP_SERVER"]["PASSWORD"])
        self.assertEqual(ret, True)               
                        
        # step: Get the bytes sent and bytes received before transfer data 
        basic_airlink.slog("step: Get the bytes sent and bytes received before transfer data")
        cellular_bytes_sent = self.se_ins.get_element_by_id(self.driver,str(msciids.MSCIID_STS_MODEM_SENT)+"-d1")
        basic_airlink.slog("Bytes Sent: " +cellular_bytes_sent)  
          
        cellular_bytes_received = self.se_ins.get_element_by_id(self.driver,str(msciids.MSCIID_STS_MODEM_RECV)+"-d1")
        basic_airlink.slog("Bytes Received: " +cellular_bytes_received) 
        
        # Step: close the AceManager web
        basic_airlink.slog("step: close Firefox")  
        self.driver.quit()     
        
        # step: transfer data file 
        basic_airlink.slog("step: transfer data file")
        avg_upload_time, avg_download_time= ftp_ins.transfer_file(1,"L")
        self.assertNotEqual(avg_upload_time, 0)               
        self.assertNotEqual(avg_download_time, 0) 
                
        # step: login to Ace Manager 
        basic_airlink.slog("step: login to Ace Manager")
        self.driver = self.se_ins.login(tbd_config_map[self.device_name]["ACE_URL"], tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"]) 
        
        # step: Get the bytes sent and bytes received after transfer data 
        basic_airlink.slog("step: Get the bytes sent and bytes received after transfer data")
        cellular_bytes_sent2 = self.se_ins.get_element_by_id(self.driver,str(msciids.MSCIID_STS_MODEM_SENT)+"-d1")
        basic_airlink.slog("Bytes Sent: " +cellular_bytes_sent2)  
          
        cellular_bytes_received2 = self.se_ins.get_element_by_id(self.driver,str(msciids.MSCIID_STS_MODEM_RECV)+"-d1")
        basic_airlink.slog("Bytes Received: " +cellular_bytes_received2) 
        
        # step: verify the bytes sent and received 
        basic_airlink.slog("step: verify the bytes sent and received ")
        self.assertEqual((int(cellular_bytes_sent2)-int(cellular_bytes_sent))/1048576, 100)
        self.assertEqual((int(cellular_bytes_received2)-int(cellular_bytes_received))/1048576, 100)
        
        ftp_ins.quit()
 
        basic_airlink.slog(str(datetime.datetime.now()))     

        download_rate = 8.0*1024*100/avg_download_time
        upload_rate   = 8.0*1024*100/avg_upload_time		
        basic_airlink.slog(" UL(kbps):" + str(upload_rate))    
        basic_airlink.slog(" DL(kbps):" + str(download_rate))

 
        
        
    def tc_datausage_transfer_medium_once(self):
        ''' Upload and download medium file once '''
       
        #step: Connect to FTP server 
        basic_airlink.slog("step: Connect to FTP server ")
        ftp_ins = ftp_airlink.FtpAirlink()
        ret=ftp_ins.login(datausage_config_map["FTP_SERVER"]["ADDRESS"], datausage_config_map["FTP_SERVER"]["USERNAME"], datausage_config_map["FTP_SERVER"]["PASSWORD"])
        self.assertEqual(ret, True)     
                  
        # step: Get the bytes sent and bytes received before transfer data 
        basic_airlink.slog("step: Get the bytes sent and bytes received before transfer data")
        cellular_bytes_sent = self.se_ins.get_element_by_id(self.driver,str(msciids.MSCIID_STS_MODEM_SENT)+"-d1")
        basic_airlink.slog("Bytes Sent: " +cellular_bytes_sent)  
          
        cellular_bytes_received = self.se_ins.get_element_by_id(self.driver,str(msciids.MSCIID_STS_MODEM_RECV)+"-d1")
        basic_airlink.slog("Bytes Received: " +cellular_bytes_received) 

        # Step: close the AceManager web
        basic_airlink.slog("step: close Firefox")  
        self.driver.quit()     
                
        # step: transfer data file 
        basic_airlink.slog("step: transfer data file")
        avg_upload_time, avg_download_time=ftp_ins.transfer_file(1,"M")
        self.assertNotEqual(avg_upload_time, 0)               
        self.assertNotEqual(avg_download_time, 0) 

        # step: login to Ace Manager 
        basic_airlink.slog("step: login to Ace Manager")
        self.driver = self.se_ins.login(tbd_config_map[self.device_name]["ACE_URL"], tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])  
                       
        # step: Get the bytes sent and bytes received after transfer data 
        basic_airlink.slog("step: Get the bytes sent and bytes received after transfer data")
        cellular_bytes_sent2 = self.se_ins.get_element_by_id(self.driver,str(msciids.MSCIID_STS_MODEM_SENT)+"-d1")
        basic_airlink.slog("Bytes Sent: " +cellular_bytes_sent2)  
          
        cellular_bytes_received2 = self.se_ins.get_element_by_id(self.driver,str(msciids.MSCIID_STS_MODEM_RECV)+"-d1")
        basic_airlink.slog("Bytes Received: " +cellular_bytes_received2) 
        
        # step: verify the bytes sent and received 
        basic_airlink.slog("step: verify the bytes sent and received ")

        self.assertEqual((int(cellular_bytes_sent2)-int(cellular_bytes_sent))/1048576, 10)
        self.assertEqual((int(cellular_bytes_received2)-int(cellular_bytes_received))/1048576, 10)
        
        ftp_ins.quit()
 
        basic_airlink.slog(str(datetime.datetime.now()))     

        download_rate = 8.0*1024*10/avg_download_time
        upload_rate   = 8.0*1024*10/avg_upload_time		
        basic_airlink.slog(" UL(kbps):" + str(upload_rate))    
        basic_airlink.slog(" DL(kbps):" + str(download_rate))
   
                 
        
    def tc_datausage_transfer_small_once(self):
        ''' Upload and download small file once '''
        #step: Connect to FTP server 
        
        basic_airlink.slog("step: Connect to FTP server ")        
        ftp_ins = ftp_airlink.FtpAirlink()
        ret=ftp_ins.login(datausage_config_map["FTP_SERVER"]["ADDRESS"], datausage_config_map["FTP_SERVER"]["USERNAME"], datausage_config_map["FTP_SERVER"]["PASSWORD"])
        self.assertEqual(ret, True)               
        
        # step: Get the bytes sent and bytes received before transfer data 
        basic_airlink.slog("step: Get the bytes sent and bytes received before transfer data")
        cellular_bytes_sent = self.se_ins.get_element_by_id(self.driver,str(msciids.MSCIID_STS_MODEM_SENT)+"-d1")
        basic_airlink.slog("Bytes Sent: " +cellular_bytes_sent)  
          
        cellular_bytes_received = self.se_ins.get_element_by_id(self.driver,str(msciids.MSCIID_STS_MODEM_RECV)+"-d1")
        basic_airlink.slog("Bytes Received: " +cellular_bytes_received) 

        # Step: close the AceManager web
        basic_airlink.slog("step: close Firefox")  
        self.driver.quit()     
                
        # step: transfer data file 
        basic_airlink.slog("step: transfer data file")
        
        avg_upload_time, avg_download_time=ftp_ins.transfer_file(1,"S")
        self.assertNotEqual(avg_upload_time,   0)               
        self.assertNotEqual(avg_download_time, 0)

        # step: login to Ace Manager 
        basic_airlink.slog("step: login to Ace Manager")
        self.driver = self.se_ins.login(tbd_config_map[self.device_name]["ACE_URL"], tbd_config_map[self.device_name]["USERNAME"], tbd_config_map[self.device_name]["PASSWORD"])
        time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])  
                        
        # step: Get the bytes sent and bytes received after transfer data 
        basic_airlink.slog("step: Get the bytes sent and bytes received after transfer data")
        cellular_bytes_sent2 = self.se_ins.get_element_by_id(self.driver,str(msciids.MSCIID_STS_MODEM_SENT)+"-d1")
        basic_airlink.slog("Bytes Sent: " +cellular_bytes_sent2)  
          
        cellular_bytes_received2 = self.se_ins.get_element_by_id(self.driver,str(msciids.MSCIID_STS_MODEM_RECV)+"-d1")
        basic_airlink.slog("Bytes Received: " +cellular_bytes_received2) 
        
        # step: verify the bytes sent and received 
        basic_airlink.slog("step: verify the bytes sent and received ")

        self.assertEqual((int(cellular_bytes_sent2)-int(cellular_bytes_sent))/1048576, 1)
        self.assertEqual((int(cellular_bytes_received2)-int(cellular_bytes_received))/1048576, 1)

        # step: Disconnect FTP server        
        ftp_ins.quit()
 
        basic_airlink.slog(str(datetime.datetime.now()))     
        
        download_rate = 8.0*1024/avg_download_time
        upload_rate   = 8.0*1024/avg_upload_time		
        basic_airlink.slog(" UL(kbps):" + str(upload_rate))    
        basic_airlink.slog(" DL(kbps):" + str(download_rate))


def setup_suite():
    """  Gather all the tests from this module in a test suite.    
    """
    test_suite = unittest.TestSuite()

    for k in range(datausage_config_map["RUN_REPEAT"]):
        
        if datausage_config_map["RUN_ALL_TESTCASES"]:
            
            # run all test cases
            #for i in range(1,datausage_config_map["ALL_TASECASE_NUMBER"]+1):
            for i in range(1,len(datausage_config_map["LIST_TESTCASES"])+1):
                test_suite.addTest(TestsuiteDatausage(datausage_config_map["LIST_TESTCASES"][i]))

        else:
            
            # run selective test cases
            for [a,b] in datausage_config_map["RUN_SELECTIVE_TESTCASES"] :
                
                for i in range(a,b+1):
                    
                    basic_airlink.slog(datausage_config_map["LIST_TESTCASES"][i])
                    
                    test_suite.addTest(TestsuiteDatausage(datausage_config_map["LIST_TESTCASES"][i]))

    return test_suite    

##########################################################################
# main FTP throughput test automation,  please set environment 
# variable AIRLINKAUTOMATION_HOME and PYTHONPATH based on your OS platform 
# and folder, e.g.
# Linux:   export AIRLINKAUTOMATION_HOME = /home/sqa/airlinkautomation
# Windows: AIRLINKAUTOMATION_HOME = C:\airlinkautomation
##########################################################################

if __name__ == "__main__":

    airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 

    stream = open(airlinkautomation_home_dirname+'/config/testbed2Conf.yml', 'r')
    tbd_config_map = yaml.load(stream)
    stream.close()
    
    log_filename=basic_airlink.get_log_filename(tbd_config_map, "datausage")
    FORMAT ='%(asctime)-15s => %(levelname)-8s => %(message)s'
    if tbd_config_map["LOG_LEVEL"]=="DEBUG":
        LEVEL = logging.DEBUG
    else: 
        LEVEL = logging.INFO 
    logging.basicConfig(level = LEVEL,filename = log_filename, format=FORMAT,  filemode='w') 
        
    fo=open(airlinkautomation_home_dirname+'/testsuite/Feature/Applications/Data_Usage/datausage_test_conf.yml','r')
    datausage_config_map = yaml.load(fo)
    fo.close()

    time_stamp = time.strftime("%b-%d-%Y_%H-%M")

    report_filename=basic_airlink.get_report_filename(tbd_config_map, "datausage")

    fpp = file(report_filename, 'wb')
    
    description_text= r""" ***test log file is """ + log_filename
    
    runner = htmlreport.HTMLTestRunner(
                stream = fpp,
                title = 'FTP Test Report', 
                description = description_text
                )    
    
    result = None

    mySuite=setup_suite() 
    
    test_cases = mySuite.countTestCases()
    
    basic_airlink.slog("Total test cases: %d" % test_cases)
   
    test_result=runner.run(mySuite, True, result)

    basic_airlink.slog("For details of the results please check \n http://carmd-ev-aptest:8080/job/TestDrive/ws/%s\n\n For details of the log please check \n http://carmd-ev-aptest:8080/job/TestDrive/ws/%s\n\n"  % ( report_filename,log_filename))
    basic_airlink.slog("Total %d test cases PASS." % test_result.success_count )
    basic_airlink.slog("Total %d test cases FAILED." % test_result.failure_count )
    basic_airlink.slog("Total %d test cases has ERROR." % test_result.error_count )    
    
    if (test_result.error_count + test_result.failure_count): 
        sys.exit(1)
    else:
        sys.exit(0)