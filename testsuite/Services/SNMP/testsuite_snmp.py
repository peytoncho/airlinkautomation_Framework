
import datetime
import logging
import os
import time
import unittest

import yaml

import basic_airlink
from pysnmp.entity.rfc3413.oneliner import cmdgen
import selenium_utilities
import telnet_airlink


class TestsuiteSnmp():
    ''' Status test suite include all Status test cases 
    
    '''
                     
    
    def __init__(self, debug_level = "0", verbose = False):
        ''' check all related items in testbed for testing '''
       
        self.tc_pass_counter = 0
        self.tc_fail_counter = 0
        
        self.processing_config()
        
        # step: check if devices ready    
        logging.info("step: check if testbed ready")
        self.testbed_ready()
            
        # step: check Firefox 
        logging.info("Please close Firefox \n")
 
        current_date_time = datetime.datetime.now()
       
        # step: put the curren time, FW version into test report at the beginning
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],"\n "+str(current_date_time))      
        self.device_name  = self.tbd_config_map["DUTS"][0]
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"], "\nALEOS FW VER: " + self.tbd_config_map[self.device_name]["ALEOS_FW_VER"])
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"], "\nRADIO FW VER: " + self.tbd_config_map[self.device_name]["RADIO_FW_VER"]+'\n')       
 
        self.se_ins = selenium_utilities.SeleniumAcemanager()
       
               
    def testbed_ready(self):
        ''' check if the testbed ready 
        
        '''
            
        # step: check if testbed ready
        for device in self.tbd_config_map["DUTS"]:
            print device
            
            telnet_instance = telnet_airlink.TelnetAirlink( hostname=self.tbd_config_map[device]["LAN_IP"], port = "2332", username = "user", password = "12345",debug_mode= False)
            if telnet_instance.connect():                
                logging.debug("DUT ready\n")  
                #telnet_instance.close()    TODO:  wait for implementation
            else: 
                logging.debug("DUT not ready yet\n")  
                #telnet_instance.close()   
                return False
            
        # all devices in testbed are checked ready    
        return True              
                         
   
    def cleanup(self):
        ''' TODO: test case cleanup '''
        
        logging.debug("step: cleanup")
    
        return
        
        
    def processing_config(self):
        ''' TODO
            
        '''
         
        fo_tbd=open( airlinkautomation_home_dirname+'/config/testbed2conf.yml','r')
        self.tbd_config_map = yaml.load(fo_tbd)
        fo_tbd.close()
        
        current_date_str = str(datetime.datetime.now().date())
        current_time_str = str(datetime.datetime.now().time()).replace(":","-")
        
        self.device_name  = self.tbd_config_map["DUTS"][0]


        log_filename = \
        self.tbd_config_map["LOG_FILE_FOLDER"]+current_date_str+"_"+current_time_str+"_"+ \
        self.tbd_config_map[self.device_name]["MODEL"]  +"_" + \
        self.tbd_config_map[self.device_name]["RM_TYPE"]+ "_"+ \
        self.tbd_config_map[self.device_name]["NET_OPERATOR"]+ "_"+ \
        self.tbd_config_map[self.device_name]["ALEOS_FW_VER"]+ "_"+ \
        "snmp_testsuite.log"
        FORMAT ='%(asctime)-15s => %(levelname)-8s => %(message)s'
        LEVEL=basic_airlink.log_level[self.tbd_config_map["PYTHON_LOGGING_LEVEL"]]
        logging.basicConfig(filename = log_filename, format=FORMAT, level = LEVEL)       
        return     
        
       
    def finallize(self): 
        '''
        TODO
        '''
        # print test result summary in test report 
        print "\n passed: ", self.tc_pass_counter, " failed:", self.tc_fail_counter
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],"\nPassed : "+ str(self.tc_pass_counter))
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],"\nFailed : "+ str(self.tc_fail_counter))  
              
 
  
  
    def tc_services_snmp_v2_ui(self):
        '''
        to test status/home page by Selenium/ACEmanager UI,  see the test case in ApTest or Testlink
        the test case focus on the general items, not LTE related 
        
        '''
        tc_id = "tc_status_home_general_ui"
        logging.info(tc_id+' : '+'begins\n')  
        
        fail_flag = 0
        
        # step: login to Ace Manager 
        logging.debug("step: login to Ace Manager")
        #device_name = self.tbd_config_map["DUTS"][0]
        driver = self.se_ins.login(self.tbd_config_map[self.device_name]["ACE_URL"], self.tbd_config_map[self.device_name]["USERNAME"], self.tbd_config_map[self.device_name]["PASSWORD"])

        time.sleep(self.tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])                     
        
        # step: come to Status page from AceManager          
        self.se_ins.services_page(driver)              
        time.sleep(2) 
           
                                 
        # Step: close the AceManager web
        logging.debug("step: close Firefox \n")  
        driver.quit() 
                
        if fail_flag > 0: 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.cleanup()
            self.tc_fail_counter += 1
             
        else:             
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : PASSED\n')
            self.cleanup()  
            self.tc_pass_counter += 1 


    def enable(self, enable_flag):
        '''
        enable/disable SNMP functionality by AT command
        ARGS --
        enable_flag  0 Disable SNMP 
        enable_flag  1 eanble SNMP
        '''
        telnet_instance = telnet_airlink.TelnetAirlink( hostname=self.tbd_config_map[self.device_name]["LAN_IP"], port = "2332", username = "user", password = "12345",debug_mode= True)
        if not (telnet_instance.connect()):
            logging.debug(" Telnet to device failed")
            return  False
        
        #step: set host connection mode 
        logging.debug("Step:  enable/disable SNMP by AT command")
        
        if enable_flag == 1: 
            ret = telnet_instance.command("at*snmp=1")
        else: 
            ret = telnet_instance.command("at*snmp=0")

        logging.debug(ret)

        ret_str = ''.join(ret)
        if not ret_str.find("OK"): 
            logging.debug(' SNMP enable/disable not working  \n')
            return False
        
        
        #step:  rebooting 
        ret = telnet_instance.command("atz")
        basic_airlink.slog("Rebooting...")
        time.sleep(self.tbd_config_map[self.device_name]["REBOOT_TIMEOUT"]) 
 
        # check if the setting is correct 
        telnet_instance = telnet_airlink.TelnetAirlink( hostname=self.tbd_config_map[self.device_name]["LAN_IP"], port = "2332", username = "user", password = "12345",debug_mode= True)
        if not (telnet_instance.connect()):
            logging.debug(" Telnet to device failed")
            return  False
        
        #step: set host connection mode 
        logging.debug("Step: check if SNMP enabled by AT command")
  
        ret = telnet_instance.command("at*snmp?")
        ret_str = ''.join(ret)
        logging.debug(ret_str)

        if   enable_flag == 1 and not ret_str.find("1"): 
                logging.debug(' SNMP enable not working  \n')
                return False
               
        elif enable_flag == 0 and not ret_str.find("0"): 
                logging.debug(' SNMP disable not working  \n')
                return False                  

        logging.debug(' SNMP is working  \n')                          
        return True
   
        
        
    def get(self, community, host, snmp_port, oid):
        '''
        '''
        cmdGen = cmdgen.CommandGenerator()
        
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData(community),
            cmdgen.UdpTransportTarget((host, snmp_port)),
            oid
        )
        
        # Check for errors and print out results
        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1] or '?'
                    )
                )
            else:
                for name, val in varBinds:
                    print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))       
        
 
    def walk(self, community, host, snmp_port, oid):
        '''
        '''
        pass
    
        
    def set(self, comminuty, host, snmp_port, oid, value):   
        
        pass
 
       
    def tc_services_snmp_enable_at(self):
        '''
        '''
        self.enable(0)
        self.enable(1)
        self.get('public','192.168.13.31', 161, 'iso.3.6.1.4.1.20542.9.1.1.2.281.0')       
        self.get('public','192.168.13.31', 161, 'iso.3.6.1.4.1.20542.9.1.1.2.282.0')       
        self.get('public','192.168.13.31', 161, 'iso.3.6.1.4.1.20542.9.1.1.2.283.0')       
        self.get('public','192.168.13.31', 161, 'iso.3.6.1.4.1.20542.9.1.1.2.284.0')       
        
 
    def tc_services_snmp_version_at(self):
        '''
        '''
        self.enable(0)
        self.enable(1)
        
    def tc_services_snmp_contact_at(self):
        '''
        '''
        self.enable(0)
        self.enable(1)       
    

 
    def tc_services_snmp_engine_id_at(self):
        '''
        '''
        self.enable(0)
        self.enable(1)
        
    def tc_services_snmp_location_at(self):
        '''
        '''
        self.enable(0)
        self.enable(1)  
 
    def tc_services_snmp_name_at(self):
        '''
        '''
        self.enable(0)
        self.enable(1)
        
    def tc_services_snmp_port_at(self):
        '''
        '''
        self.enable(0)
        self.enable(1)  
    
     
    def tc_services_snmp_ro_at(self):
        '''
        '''
        self.enable(0)
        self.enable(1)
        
    def tc_services_snmp_rw_at(self):
        '''
        '''
        self.enable(0)
        self.enable(1)  
        
     
    def tc_services_snmp_trap_at(self):
        '''
        '''
        self.enable(0)
        self.enable(1)
        

   
           
##########################################################################
# main SNMP test automation,  please set environment 
# variable AIRLINKAUTOMATION_HOME and PYTHONPATH based on your OS platform 
# and folder, e.g.
# Linux:   export AIRLINKAUTOMATION_HOME = /home/sqa/airlinkautomation
# Windows: AIRLINKAUTOMATION_HOME = C:\airlinkautomation
##########################################################################


   
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME']

my_snmp = TestsuiteSnmp()

SNMP_TESTCASES ={  \
   "tc_services_snmp_enable_at"     : my_snmp.tc_services_snmp_enable_at, \
   "tc_services_snmp_version_at"    : my_snmp.tc_services_snmp_version_at, \
   "tc_services_snmp_contact_at"    : my_snmp.tc_services_snmp_contact_at, \
   "tc_services_snmp_engine_id_at"  : my_snmp.tc_services_snmp_engine_id_at, \
   "tc_services_snmp_location_at"   : my_snmp.tc_services_snmp_location_at, \
   "tc_services_snmp_name_at"       : my_snmp.tc_services_snmp_name_at, \
   "tc_services_snmp_port_at"       : my_snmp.tc_services_snmp_port_at, \
   "tc_services_snmp_ro_at"         : my_snmp.tc_services_snmp_ro_at, \
   "tc_services_snmp_rw_at"         : my_snmp.tc_services_snmp_rw_at, \
   "tc_services_snmp_trap_at"       : my_snmp.tc_services_snmp_trap_at\
   }
    
fo=open(airlinkautomation_home_dirname+'/testsuite/GX440/Services/Snmp/snmp_test_conf.yml','r')
snmp_config_map = yaml.load(fo)
fo.close()

# run test cases 
for k in range(snmp_config_map["RUN_REPEAT"]):
    
    if snmp_config_map["RUN_ALL_TESTCASES"]:
        
        # run all test cases
        for i in range(1,snmp_config_map["ALL_TASECASE_NUMBER"]+1):
            print "i="+ str(i)
            logging.debug(snmp_config_map["RUN_ALL_TESTCASES"])
            SNMP_TESTCASES[snmp_config_map["LIST_TESTCASES"][i]]()           
    else:
        
        # run selective test cases
        for [a,b] in snmp_config_map["RUN_SELECTIVE_TESTCASES"] :
            
            #print a,b
            for i in range(a,b+1):
                
                #print i
                logging.debug(snmp_config_map["LIST_TESTCASES"][i])
                SNMP_TESTCASES[snmp_config_map["LIST_TESTCASES"][i]]()

my_snmp.finallize()