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

#import htmlreport
from selenium.common.exceptions import NoSuchFrameException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import yaml

import basic_airlink
import connectivity
import selenium_utilities

#must define the test area here
test_area = "TestClass"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")
basic_airlink.append_sys_path()

#Change the name here
tbd_config_map, testarea_config_map = basic_airlink.get_config_data(test_area,"")


class TestSuiteTestClass (unittest.TestCase):
    """TestsuiteTestClass class provides a firmware update automation using Selenium UI test features.
       
    """
    
    def setUp(self):
        """
        Desription for setUp function
        
        Returns: None
        
        Args: None
        
        Raises: None       
        """
        return
    
    def tc_test_1(self):
        basic_airlink.slog("This is tc_test 1")
        pass
    
    def tc_test_2(self):
        basic_airlink.slog("This is tc_test 2")
        pass
    
    def tc_test_3(self):
        basic_airlink.slog("This is tc_test 3")
        pass
    
    def tc_test_4(self):
        basic_airlink.slog("This is tc_test 4")
        pass
    
    def tearDown(self):
        """
        Desription for tearDown function
        
        Args: None
        
        Returns: None
         
        Raises: None       
        """
        return








