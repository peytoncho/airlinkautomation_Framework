###############################################################################
#
# This is ts script template  
# Company: Sierra Wireless
# Time: June 20th, 2099
# 
#################################################################################
import logging
import os
import time
import unittest
import sys
import multiprocessing
import Queue
import re


#import htmlreport
from selenium.common.exceptions import NoSuchFrameException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver


import basic_airlink
import connectivity
import selenium_utilities
import at_utilities
import ssh_airlink
import telnet_airlink
import fwupdate_airlink
import datetime
import ping_airlink

#must define the test area here
test_area = "TestClass"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")
basic_airlink.append_sys_path()
fail_flag = 0
#Change the name here
tbd_config_map, testarea_config_map = basic_airlink.get_config_data(test_area,"")

from multiprocessing import Process

def print_stuff(string):
    print string
def print_to_console(string):
    p = Process(target = print_stuff, args = (string,))
    p.start()
    p.join(5)

def listening_clog(queue):
    while True:
        if not queue.empty():
            m = queue.get()
            sys.stdout.writelines(m) 
        else:
            time.sleep(0.1)
#device_name = tbd_config_map["DUTS"][0]
test_case_num = 0


class TsTestClass1 (unittest.TestCase):
    """TestsuiteTestClass class provides a firmware update automation using Selenium UI test features.
       
    """
        
    def check_fail_flag(self):
        global fail_flag
        if fail_flag == 1:
            self.assertEqual(fail_flag, 0, "Test failed")
    
    def set_fail_flag(self):
        global fail_flag
        fail_flag = 1
    
    def _network_state_ckeck(self):
        
        at_ins = at_utilities.AtCommands()
        conn_ins = connectivity.Connectivity()
        connect_instance = conn_ins.connection_types()
        network_state = ""
        if not connect_instance.connect():
            network_state = "Error"
            basic_airlink.clog(time.ctime(time.time())+" ===>> network_ready_ckeck: Connection Failed")
        else:
           network_state = at_ins.get_net_state(connect_instance)
           basic_airlink.cslog(network_state)
           connect_instance.close()
        return network_state    
   
    def setUp(self):
        ''' the test runner will run that method prior to each test
        
        Args: None
        
        Returns: None
        '''
#         self.q = multiprocessing.Queue(10)   
#         self.p = multiprocessing.Process(target = listening_clog, args=(self.q,))
#         self.p.start()
#         basic_airlink.clog(self.id(), "RED")
#         self.check_fail_flag()
#         global fail_flag
        #self.conn_ins = connectivity.Connectivity()
#         basic_airlink.cslog("TestTESTTEST")               
#         basic_airlink.cslog("step: check if testbed is ready")
#         try:
#             self.assertEqual(self.conn_ins.testbed_ready(), True, "DUT NOT READY")
#         except Exception:
#             self.skipTest("DUT not ready")
                     
        self.se_ins = selenium_utilities.SeleniumAcemanager()
#         self.at_ins = at_utilities.AtCommands()
#         self.ssh_ins = ssh_airlink.SshAirlink()
        
        
#         self.url = tbd_config_map[device_name]["ACE_URL"]
#         self.username = tbd_config_map[device_name]["USERNAME"]
#         self.password = tbd_config_map[device_name]["PASSWORD"]
        self.url = 'http://192.168.13.31:9191'
        self.username = 'user'
        self.password = '12345'
        
#         self.connect_instance = self.conn_ins.connection_types()
#         if not self.connect_instance.connect(): 
#             basic_airlink.slog("Problem: testbed not ready yet")
        self.driver = self.se_ins.login(self.url, self.username, self.password)
        self.device_name = self.se_ins.form_device_name(self.driver)   
        return
    def tearDown(self):
        self.driver.quit()
        return

       
    def test_1(self):
        ping_airlink.PingAirlink().ping_test('192.168.13.31')
        model = tbd_config_map[self.device_name]["MODEL"]
        rm_type = tbd_config_map[self.device_name]["RM_TYPE"]
        
        basic_airlink.cslog("Model: "+model)
        basic_airlink.cslog("RM_TYPE: "+rm_type)
              
    def test_2(self):
        basic_airlink.cslog("This is tc_test 2")
        pass
     
    def test_3(self):              
        basic_airlink.cslog("This is tc_test 3")
        pass
    
    @unittest.skipIf(fail_flag ==1, Exception("tc1"))   
    def test_4(self):
        basic_airlink.cslog("This is tc_test 4")
        self.assertEqual(True, False, "tc4 fail")      
        pass
    
    @unittest.skipIf(fail_flag ==1, Exception("tc1"))
    def test_5(self):
        basic_airlink.cslog("This is tc_test 5")
        pass
    
    @unittest.skipIf(fail_flag ==1, Exception("tc1"))    
    def test_6(self):
        basic_airlink.cslog("This is tc_test 6")
        pass
    
    def test_7(self):
        basic_airlink.cslog("This is tc_test 7")
        pass
    
    def test_8(self):
        basic_airlink.cslog("This is tc_test 8")
        pass
    
    def test_9(self):
        basic_airlink.cslog("This is tc_test 9")
        pass
    
    def test_10(self):
        basic_airlink.cslog("This is tc_test 10")
        pass
    
    def test_11(self):
        basic_airlink.cslog("This is tc_test 11")
        pass
    
    def test_12(self):
        basic_airlink.cslog("This is tc_test 12")
        pass 
    
    
    



class TsTestClass2 (unittest.TestCase):
    def setUp(self):
        return
    
    def test_1(self):
        basic_airlink.slog("This is tc_test 1")
        pass
    
    def test_2(self):
        basic_airlink.slog("This is tc_test 2")
        self.assertEqual(True, False, "class 2 test 2 fail")
        pass
    
    def test_3(self):
        basic_airlink.slog("This is tc_test 3")
        pass


    def retry_at_command(self, state, retry_count, retry_delta_time):
        
        ret = True
        func_lst = []
        var = ""
        flag = 0
        if state == "staticip.apn":
            var = self.at_ins.get_apn(self.connect_instance)
            func_lst = [self.at_ins.get_apn]
        elif state == "Bell":
            var = self.at_ins.get_cell_info(self.connect_instance, "")
            func_lst = [self.at_ins.get_cell_info]
        else:
            flag = 1
            ret = False
        
        retry_to_count = 0
        
        while retry_to_count != retry_count and var != state and flag != 1:
            time.sleep(retry_delta_time)
            func_lst[0](self.connect_instance)           
            retry_to_count+=1
        
        if retry_to_count == retry_count and var != state:
            ret = False
            
        return ret
        

def setup_suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TsTestClass1))
    test_suite.addTest(unittest.makeSuite(TsTestClass2))
    return test_suite



