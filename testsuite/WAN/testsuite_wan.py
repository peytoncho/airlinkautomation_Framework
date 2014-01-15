from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import sys

sys.path.append("/home/airlink/workspace/airlinkautomation/lib/common")
import yaml
import basic_airlink
import config_airlink
import htmlreport
import unittest, time, re
import sys
import logging
seleniumhandler = None


class Unbuffered:
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

sys.stdout=Unbuffered(sys.stdout)

class TestsuiteWan_public(unittest.TestCase):

    ''' This test suite include all WAN public IP test cases 
    
    '''
    
    def setUp(self):
        global seleniumhandler
        self.base_url = "http://192.168.13.31:9191"
        self.accept_next_alert = True
        print "start selenium"        
        if seleniumhandler == None:
#            profile = webdriver.FirefoxProfile()
#            profile.set_preference("browser.download.folderList","2")
#            self.webdriver = webdriver.Firefox(firefox_profile=profile)
            if int(self.id().split('.')[-1][5:]) not in wan_config_map["RUN_SELECTIVE_TESTCASES"]:
                    self.skipTest(self.id().split('.')[-1]+" been skipped")
            self.driver = webdriver.Firefox()
            self.driver.implicitly_wait(10)            
            self.driver.implicitly_wait(10)
            seleniumhandler = self.driver
            self.verificationErrors = []
            print "Setup is none"
        else:
            print "Setup is skipped"
            self.driver = seleniumhandler
                
    def test_1(self):
       
        print "Test001: Sign in Start"
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.implicitly_wait(10)        
        driver.find_element_by_id("username").clear()
        driver.implicitly_wait(10)
        print "Check login"
        driver.find_element_by_id("username").send_keys("user") 
        driver.find_element_by_id("password").clear()
        driver.implicitly_wait(10)
        print "check password"
        driver.find_element_by_id("password").send_keys("12345")
        driver.find_element_by_name("Login").click()        
        driver.find_element_by_id("WAN/CellularM1").click()
        logging.debug("step: from Ace Manager come to WAN page: ")                
        driver.find_element_by_id("btn_Refresh").click()
        self.driver.implicitly_wait(10)
        print "Test001: Sign in Finish"
 
        print "Test001: setting new configuration"
        print "Test001: rebootting device"
        # Assert example, there are quite a few other assertion methonds,
        # http://docs.python.org/2/library/unittest.html#assert-methods 
        # here's just a simple example
        # This won't affect use whatever archived function, but u could use this simple method as pass/fail flag
        self.assertEqual("e", "e")
    test_1.__doc__="test_wan_celluar_yes"
    
    def test_2(self):
      
        print "Test002: Sign out Start"
        sys.stdout.write("\nTest002: Sign out Start\n\n" )        
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.implicitly_wait(10)        
        driver.find_element_by_id("username").clear()
        driver.implicitly_wait(10)
        print "Check login"
        driver.find_element_by_id("username").send_keys("user") 
        driver.find_element_by_id("password").clear()
        driver.implicitly_wait(10)
        print "check password"
        driver.find_element_by_id("password").send_keys("12345")
        driver.find_element_by_name("Login").click()        
        logging.debug("step: from Ace Manager come to status page: ")            
        driver.find_element_by_id("WAN/CellularM1").click()
        driver.find_element_by_id("btn_Refresh").click()
        print "Test002: Verification started"         
        print "Test002: Verification finished"
    test_2.__doc__="test_wan_celluar_no"


    def test_3(self):
      
        print "Test003: Sign out Start"
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.implicitly_wait(10)        
        driver.find_element_by_id("username").clear()
        driver.implicitly_wait(10)
        print "Check login"
        driver.find_element_by_id("username").send_keys("user") 
        driver.find_element_by_id("password").clear()
        driver.implicitly_wait(10)
        logging.debug("step: from Ace Manager come to status page: ")            
        print "check password"
        driver.find_element_by_id("password").send_keys("12345")
        driver.find_element_by_name("Login").click()        
        driver.find_element_by_id("WAN/CellularM1").click()
        driver.find_element_by_id("btn_Refresh").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectFrame]]
        print "Test003: Sign in Finish"
  #      passed_cases = passed_cases + 1

        print "Test003: setting new configuration"
        print "Test003: rebootting device"        
  
        print "Test003: Verification started"

        elist=["e","a"]  
        self.assertIn("e", elist)          
        print "Test003: Verification finished"
    test_3.__doc__="Utest_wan_celluar_info_yes"
                     
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def tearDown(self):
        print self.id()
        print "Checking the statics"
        global seleniumhandler    
        seleniumhandler = None
        self.driver.quit()            
        self.assertEqual([], self.verificationErrors)
        if self.id().split('.')[-1] == "test_003" :         
  #          self.driver.quit()
            seleniumhandler = None
            self.driver.quit()            
            self.assertEqual([], self.verificationErrors)

class TestsuiteWan_private(unittest.TestCase):

    ''' This test suite include all WAN private IP test cases 
    
    '''
    
    def setUp(self):
        global seleniumhandler
        self.base_url = "http://192.168.13.31:9191"
        self.accept_next_alert = True
        print "start selenium"        
        if seleniumhandler == None:
#            profile = webdriver.FirefoxProfile()
#            profile.set_preference("browser.download.folderList","2")
#            self.webdriver = webdriver.Firefox(firefox_profile=profile)
            if int(self.id().split('.')[-1][5:]) not in wan_config_map["RUN_SELECTIVE_TESTCASES"]:
                    self.skipTest(self.id().split('.')[-1]+"Not suppose to run though")
            self.driver = webdriver.Firefox()
            self.driver.implicitly_wait(10)            
            self.driver.implicitly_wait(10)
            seleniumhandler = self.driver
            self.verificationErrors = []
            print "Setup is none"
        else:
            print "Setup skipped"
            self.driver = seleniumhandler
                
    def test_4(self):
      
        print "Test004: Sign in Start"
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.implicitly_wait(10)        
        driver.find_element_by_id("username").clear()
        driver.implicitly_wait(10)
        print "Check login"
        driver.find_element_by_id("username").send_keys("user") 
        driver.find_element_by_id("password").clear()
        driver.implicitly_wait(10)
        print "check password"
        driver.find_element_by_id("password").send_keys("12345")
        driver.find_element_by_name("Login").click()        
        driver.find_element_by_id("WAN/CellularM1").click()
        logging.debug("step: from Ace Manager come to WAN page: ")                
        driver.find_element_by_id("btn_Refresh").click()
        self.driver.implicitly_wait(10)
        print "Test004: Sign in Finish"
        self.assertEqual("e", "ae")
        print "Test004: setting new configuration"
        print "Test004: rebootting device"
        self.assertEqual("e", "e")
    test_4.__doc__="test_wan_celluar_info_no"

    def test_5(self):
    
        print "Test005: Sign in Start"
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.implicitly_wait(10)        
        driver.find_element_by_id("username").clear()
        driver.implicitly_wait(10)
        print "Check login"
        driver.find_element_by_id("username").send_keys("user") 
        driver.find_element_by_id("password").clear()
        driver.implicitly_wait(10)
        print "check password"
        driver.find_element_by_id("password").send_keys("12345")
        driver.find_element_by_name("Login").click()        
        driver.find_element_by_id("WAN/CellularM1").click()
        logging.debug("step: from Ace Manager come to WAN page: ")                
        driver.find_element_by_id("btn_Refresh").click()
        self.driver.implicitly_wait(10)
        print "Test005: Sign in Finish"
        print "Test005: setting new configuration"
        print "Test005: rebootting device"
        self.assertEqual("e", "e")
    test_5.__doc__="test_wan_celluar_error_yes"    


    def test_6(self):
  #      global passed_cases        
        print "Test001: Sign in Start"
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.implicitly_wait(10)        
        driver.find_element_by_id("username").clear()
        driver.implicitly_wait(10)
        print "Check login"
        driver.find_element_by_id("username").send_keys("suser") 
        driver.find_element_by_id("password").clear()
        driver.implicitly_wait(10)
        print "check password"
        driver.find_element_by_id("password").send_keys("12345")
        driver.find_element_by_name("Login").click()        
        driver.find_element_by_id("WAN/CellularM1").click()
        logging.debug("step: from Ace Manager come to WAN page: ")                
        driver.find_element_by_id("btn_Refresh").click()
        self.driver.implicitly_wait(10)
        print "Test006: Sign in Finish"
  
        print "Test006: setting new configuration"
        print "Test006: rebootting device"
        self.assertEqual("e", "e")
    test_6.__doc__="test_wan_celluar_error_yes" 

    def test_7(self):
  #      global passed_cases        
        print "Test007: Sign in Start"
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.implicitly_wait(10)        
        driver.find_element_by_id("username").clear()
        driver.implicitly_wait(10)
        print "Check login"
        driver.find_element_by_id("username").send_keys("suser") 
        driver.find_element_by_id("password").clear()
        driver.implicitly_wait(10)
        print "check password"
        driver.find_element_by_id("password").send_keys("12345")
        driver.find_element_by_name("Login").click()        
        driver.find_element_by_id("WAN/CellularM1").click()
        logging.debug("step: from Ace Manager come to WAN page: ")                
        driver.find_element_by_id("btn_Refresh").click()
        self.driver.implicitly_wait(10)
        print "Test007: Sign in Finish"
  
        print "Test007: setting new configuration"
        print "Test007: rebootting device"
        self.assertEqual("e", "e")
    test_7.__doc__="test_wan_celluar_critical_yes " 
    
    def test_8(self):
  #      global passed_cases        
        print "Test008: Sign in Start"
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.implicitly_wait(10)        
        driver.find_element_by_id("username").clear()
        driver.implicitly_wait(10)
        print "Check login"
        driver.find_element_by_id("username").send_keys("suser") 
        driver.find_element_by_id("password").clear()
        driver.implicitly_wait(10)
        print "check password"
        driver.find_element_by_id("password").send_keys("12345")
        driver.find_element_by_name("Login").click()        
        driver.find_element_by_id("WAN/CellularM1").click()
        logging.debug("step: from Ace Manager come to WAN page: ")                
        driver.find_element_by_id("btn_Refresh").click()
        self.driver.implicitly_wait(10)
        print "Test008: Sign in Finish"
  
        print "Test008: setting new configuration"
        print "Test008: rebootting device"
        self.assertEqual("e", "e")
    test_8.__doc__="test_wan_celluar_critical_no "     

                     
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def tearDown(self):
        print self.id()
        print "clean up here"
                        
        global seleniumhandler    
        seleniumhandler = None
        self.driver.quit()            
        self.assertEqual([], self.verificationErrors)
        # You may use self.id to do special tear down on specific test case
        if self.id().split('.')[-1] == "Kenny" :         
  #          self.driver.quit()
            seleniumhandler = None
            self.driver.quit()            
            self.assertEqual([], self.verificationErrors)




if __name__ == "__main__":

    print  "Starting test..... "
    time_stamp = time.strftime("%b-%d-%Y_%H-%M")
    
    global wan_config_map
    
    log_file_name = 'WAN_test_log_' + time_stamp + '.txt'
   # folder_log_file_name='../../workspace/TestDrive/'+log_file_name
    folder_log_file_name=log_file_name
    fp_log = open(folder_log_file_name, 'wb')

    FORMAT ='%(asctime)-15s => %(levelname)-8s => %(message)s'
    LEVEL="DEBUG"
    logging.basicConfig(filename = folder_log_file_name, format=FORMAT, level = LEVEL)

    fo=open('wan_test_conf.yml','r')
    wan_config_map = yaml.load(fo)
    fo.close()
    
    report_file_name = 'Airlink_WAN_Test_report_' + time_stamp + '.html'
  #  folder_report_file_name='../../workspace/TestDrive/'+report_file_name
    folder_report_file_name=report_file_name
    fp = file(folder_report_file_name, 'wb')
    
    tbd_config = config_airlink.ConfigParser('../../config/testbed2Conf.yml')    # object instance       
    tbd_config.processing_config("admin")

        
        # step: check if devices ready    
    logging.info("step: check if testbed is ready")
    
    device_name = tbd_config.map["DUTS"][0]
           
        # step: check Firefox 
    
 
        # step: put the curren time, FW version into test report at the beginning of the test results
    description_text= r"""****************"""      
    description_text+=r""" DEVICE MODEL: """ + tbd_config.map[device_name]["MODEL"]
    description_text+=r""" RADIO TYPE  : """ + tbd_config.map[device_name]["RM_TYPE"]
    description_text+=r""" ALEOS FW VER: """ + tbd_config.map[device_name]["ALEOS_FW_VER"]+r"""*********"""    
    
    runner = htmlreport.HTMLTestRunner(# create unitest html testsuite runner
                stream = fp,
                title = 'WAN dryrun demo code test', 
                description = description_text
                )    
    result = None
#    mainsuite = unittest.TestLoader().loadTestsFromTestCase(TestsuiteWan_private)
    def setup_suite():
#    """        Gather all the tests from this module in a test suite.    """
        test_suite = unittest.TestSuite()
        test_suite.addTest(unittest.makeSuite(TestsuiteWan_public))
        test_suite.addTest(unittest.makeSuite(TestsuiteWan_private))        
        return test_suite

    mySuite=setup_suite()
    
#    Otherway to add testcases bases on the selection you may manipulate the "test_"+testcase_number add them one by one
#    suite = unittest.TestSuite()
#    suite.addTest(TestwanSuite('test_1'))
#    suite.addTest(TestwanSuite('test_3'))    
    
    test_cases = mySuite.countTestCases()
    
    sys.stdout.write("\nTotal test cases: %d" % test_cases)
   
    test_result=runner.run(mySuite, True, result)
    print test_result.error_count

    sys.stdout.write("\nFor details of the results please check \n http://carmd-ev-aptest:8080/job/TestDrive/ws/%s\n\n For details of the log please check \n http://carmd-ev-aptest:8080/job/TestDrive/ws/%s\n\n"  % ( report_file_name,log_file_name))
    sys.stdout.write("\nTotal %d test cases PASS." % test_result.success_count )
    sys.stdout.write("\nTotal %d test cases FAILED." % test_result.failure_count )
    sys.stdout.write("\nTotal %d test cases has ERROR." % test_result.error_count )    
    sys.stdout.write("\n" )     
    
    if (test_result.error_count + test_result.failure_count): 
        sys.exit(1)
    else:
        sys.exit(0)