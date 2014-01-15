################################################################################
#
# This module automates LAN's AT commands test cases. 
# Company: Sierra Wireless
# Date: Aug 13, 2013
# Author: Airlink
# 
################################################################################

import logging
import os
import sys
import time
import unittest

import at_utilities
import basic_airlink
import connectivity
import serial_airlink
import telnet_airlink


airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")
sys.path.append(".")

basic_airlink.append_sys_path()

tbd_config_map, admin_config_map = basic_airlink.get_config_data("Admin","")          
   
        
class TsAdminAtCommands(unittest.TestCase):
    ''' This test suite automates Admin testcases by AT commands.
    Please make sure testbed (DUT,X-card, connection, configuration) is ready 
    before run any test.
    '''     
                     
    def setUp(self):
        ''' the test runner will run that method prior to each test
        '''
           
        self.conn_ins = connectivity.Connectivity()     
        self.at_ins   = at_utilities.AtCommands()   
        # step: check if devices ready    
        basic_airlink.slog("step: check if testbed is ready")
        self.conn_ins.testbed_ready() 
        self.device_name = tbd_config_map["DUTS"][0]
                   
        basic_airlink.slog("Step:  connect to DUT and generate connection instance")
        self.connect_instance = self.conn_ins.connection_types()
        if not self.connect_instance.connect(): 
            basic_airlink.slog("Problem: testbed not ready yet")
                    
        self.fail_flag = 0
           
        self.verificationErrors = []
        self.accept_next_alert = True                
        
          
    def tearDown(self):
        ''' the test runner will invoke that method after each test
        Args: None
        Returns: None
        '''        
        self.assertEqual([], self.verificationErrors) 
        self.connect_instance.close()
        
        basic_airlink.slog(" Testcase complete")
        
            
    def tc_reset_to_factory_default(self):
        ''' 
        '''
        ret = self.at_ins.factory_reset(self.connect_instance)
        if not ret:
            self.fail_flag +=1  
            
        time.sleep(tbd_config_map[self.device_name]["REBOOT_TIMEOUT"])
        
        basic_airlink.slog("Step:  connect to DUT and generate connection instance")
        self.connect_instance = self.conn_ins.connection_types()
        if not self.connect_instance.connect(): 
            basic_airlink.slog("Problem: testbed not ready yet")
        else:    
            ret=self.at_ins.get_system_reset_number(self.connect_instance)     
            self.assertEqual(int(ret), 1)
            
        self.assertEqual(self.fail_flag, 0)

    def tc_atz_reboot(self):
        ''' test AT command ATZ and DATZ
        '''
        num1 =self.at_ins.get_system_reset_number(self.connect_instance) 
        
        ret=self.at_ins.get_datz(self.connect_instance) 
        if ret == basic_airlink.ERR:
            self.fail_flag +=1     
        if ret == "1":
            self.at_ins.set_datz(self.connect_instance,"0") 
            
        ret = self.at_ins.atz_reboot(self.connect_instance)
            
        time.sleep(tbd_config_map[self.device_name]["REBOOT_TIMEOUT"])
        
        basic_airlink.slog("Step:  connect to DUT and generate connection instance")
        self.connect_instance = self.conn_ins.connection_types()
        if not self.connect_instance.connect(): 
            basic_airlink.slog("Problem: testbed not ready yet")
        else:    
            num2=self.at_ins.get_system_reset_number(self.connect_instance)     
            self.assertEqual(int(num2)-int(num1), 1)
            
        self.assertEqual(self.fail_flag, 0)  
                                                                                                         
    def tc_block_reset_config(self):
        ''' 
        '''
        cfg1 =self.at_ins.get_block_reset_config(self.connect_instance) 
            
        ret = self.at_ins.set_block_reset_config(self.connect_instance,"1")
        if not ret:
            self.fail_flag +=1  
            
        cfg2 =self.at_ins.get_block_reset_config(self.connect_instance) 
        
        self.assertEqual(cfg2, "1")  
        self.assertEqual(self.fail_flag, 0)  

    def tc_boardtemp_and_powerinput(self):
        ''' 
        '''
        temp =self.at_ins.get_board_temp(self.connect_instance) 
        if temp == basic_airlink.ERR:
            self.fail_flag +=1  
            
        volt =self.at_ins.get_power_input_voltage(self.connect_instance) 
        if volt == basic_airlink.ERR:
            self.fail_flag +=1  
                    
        self.assertEqual(self.fail_flag, 0)  

    def tc_at_ping(self):
        ''' 
        '''
        ret =self.at_ins.at_ping(self.connect_instance, "google.com") 
        if not ret:
            self.fail_flag +=1  
            
        ret =self.at_ins.at_ping(self.connect_instance, "8.8.8.8") 
        if not ret:
            self.fail_flag +=1  
                    
        self.assertEqual(self.fail_flag, 0) 
                        
    def tc_date_time(self):
        ''' 
        '''
        ret =self.at_ins.get_date(self.connect_instance) 
        if ret == basic_airlink.ERR:
            self.fail_flag +=1  
            
        ret =self.at_ins.set_date(self.connect_instance, "08/14/2013,23:40:11") 
        if not ret:
            self.fail_flag +=1  
                    
        self.assertEqual(self.fail_flag, 0) 
 
    def tc_status_update_commands(self):
        ''' 
        '''
        # step: get and set status update address by at command
        ret =self.at_ins.get_status_update_address(self.connect_instance) 
        if ret == basic_airlink.ERR:
            self.fail_flag +=1  
            
        ret =self.at_ins.set_status_update_address(self.connect_instance, 
                                                   admin_config_map["STATUS_UPDATE_ADDRESS"],
                                                   admin_config_map["STATUS_UPDATE_PORT"]) 
        if not ret:
            self.fail_flag +=1  
            
        ret =self.at_ins.get_status_update_address(self.connect_instance) 
        if ret == basic_airlink.ERR:
            self.fail_flag +=1 
        self.assertEqual(ret, admin_config_map["STATUS_UPDATE_ADDRESS"]+"/"+admin_config_map["STATUS_UPDATE_PORT"])
        
        # step: get and set status update interval by at command
        ret =self.at_ins.get_status_update_interval(self.connect_instance) 
        if ret == basic_airlink.ERR:
            self.fail_flag +=1  
            
        ret =self.at_ins.set_status_update_interval(self.connect_instance, "0") 
        if not ret:
            self.fail_flag +=1  

        ret =self.at_ins.get_status_update_interval(self.connect_instance) 
        if ret == basic_airlink.ERR:
            self.fail_flag +=1  
        self.assertEqual(ret, "0")
        #    
        ret =self.at_ins.set_status_update_interval(self.connect_instance, "15")
        if not ret:
            self.fail_flag +=1  
        ret =self.at_ins.get_status_update_interval(self.connect_instance) 
        if ret == basic_airlink.ERR:
            self.fail_flag +=1  
        self.assertEqual(ret, "15")
        #            
        ret =self.at_ins.set_status_update_interval(self.connect_instance, "255") 
        if not ret:
            self.fail_flag +=1                
        ret =self.at_ins.get_status_update_interval(self.connect_instance) 
        if ret == basic_airlink.ERR:
            self.fail_flag +=1  
        self.assertEqual(ret, "255")
        #                                      
        self.assertEqual(self.fail_flag, 0)
                               
        

    def tc_memory_cpu_root_user(self):
        '''
        to check the memory  and CPU usage in DUT as root user
        
        '''
        tc_id = "tc_memory_check_root_user"
        logging.info(tc_id+' : '+'begins\n')
        
        # step: check if devices ready    
#        logging.debug("step: check if Testbed is ready")
#        if not self.conn_ins.testbed_ready() :         
#            basic_airlink.test_report(tbd_config_map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
#            self.tc_fail_counter +=1
#            basic_airlink.cleanup()
#            return  
        
        # step: Telnet to device            
        _device   = tbd_config_map["DUTS"][0]
        _hostname = tbd_config_map[_device]["ETH_DEVICE_IP"] 
        print _hostname        
        connect_instance = telnet_airlink.TelnetAirlink( hostname=_hostname, port = "2332", username = "root", password = "v3r1fym3",debug_mode= True)
        if not (connect_instance.connect()):
            #basic_airlink.test_report(tbd_config_map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.fail_flag +=1
            #basic_airlink.cleanup()
            #return  
        
        else:
            #step: get memory status 
            logging.debug("Step:  get memory status")
            
            ret = connect_instance.command("free -m")
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)
            
            ret = connect_instance.command("top -n3")
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("\n")

            ret = connect_instance.command("cat /proc/meminfo")
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)
                                      
            #basic_airlink.test_report(tbd_config_map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
            #self.tc_pass_counter +=1
            #basic_airlink.cleanup()
        self.assertEqual(self.fail_flag,0)                
                                                 
 
    def tc_log_reset_check_root_user(self):
        '''
        to check the rebooting by AT command and log
        
        '''
        tc_id = "tc_log_reset_check_root_user"
        logging.info(tc_id+' : '+'begins\n')
        
        # step: Telnet to device            
        _device   = tbd_config_map["DUTS"][0]
        _hostname = tbd_config_map[_device]["ETH_DEVICE_IP"] 
            
            #step: get the number of reset since last reset to default
        logging.debug("Step:  get the number of reset since last reset to default")
        ret =self.at_ins.get_system_reset_number(self.connect_instance) 
   
                    
        connect_instance = telnet_airlink.TelnetAirlink( hostname=_hostname, port = "2332", username = "root", password = "v3r1fym3",debug_mode= True)
        if not (connect_instance.connect()):
            #basic_airlink.test_report(tbd_config_map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.fail_flag +=1
            #basic_airlink.cleanup()
            return  
        
        else:
            
            #step: get reset timestamp from logs
            logging.debug("Step:  get reset timestamp from the latest fives logs")
            
            if tbd_config_map[self.device_name]["RM_TYPE"] == "MC7750":
                reset_substring = 'alert ALEOS_SYSTEM_SCR_rc.syslog:   Version: ' 

            else:
                reset_substring = 'alert ALEOS_SYSTEM_SCR_rc.syslog:   Version:'  
                #reset_substring = 'alert ALEOS_SYSTEM_SCR_aleosreboot: Rebooting...'  

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages | grep -E \'%s\'" %(reset_substring))
            ret_str = ''.join(ret)                             
            basic_airlink.slog(ret_str)
            
            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.0 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.1 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)
 
            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.2 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.3 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.4 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)
                                                             
            #basic_airlink.test_report(tbd_config_map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
            #self.tc_pass_counter +=1
            #basic_airlink.cleanup()
        self.assertEqual(self.fail_flag,0)                
            
      
    def tc_check_network_state_root_user(self):
        '''
        to check the network state by AT command and log
        
        '''
        tc_id = "tc_check_network_state_root_user"
        logging.info(tc_id+' : '+'begins\n')
        
        # step: check if devices ready    
#        logging.debug("step: check if testbed is ready")
#        if not self.conn_ins.testbed_ready() : 
#            basic_airlink.test_report(tbd_config_map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
#            self.tc_fail_counter +=1
#            #basic_airlink.cleanup()
#            return  
        
        # step: Telnet to device            
        _device   = tbd_config_map["DUTS"][0]
        _hostname = tbd_config_map[_device]["ETH_DEVICE_IP"] 
        
        connect_instance = self.conn_ins.connection_types()    
        if not (connect_instance.connect()):
            #basic_airlink.test_report(tbd_config_map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.fail_flag +=1
            #basic_airlink.cleanup()
            return 
  
        else:
            
            #step: get the number of reset since last reset to default
            logging.debug("Step:  get the number of reset since last reset to default")
            ret = connect_instance.command("at*netstate?")
            ret_str = ''.join(ret)                             
            basic_airlink.slog(ret_str)     
                    
        connect_instance = telnet_airlink.TelnetAirlink( hostname=_hostname, port = "2332", username = "root", password = "v3r1fym3",debug_mode= True)
        if not (connect_instance.connect()):
            #basic_airlink.test_report(tbd_config_map["TEST_REPORT_FILE"],'FAILED : '+tc_id)
            self.fail_flag+=1
            #basic_airlink.cleanup()
            return  
        
        else:
            
            #step: get reset timestamp from logs
            logging.debug("Step:  get the network state from the latest fives logs")
            
            reset_substring = 'Network State'  

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages | grep -E \'%s\'" %(reset_substring))
            ret_str = ''.join(ret)                             
            basic_airlink.slog(ret_str)
            
            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.0 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.1 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)
 
            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.2 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.3 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)

            ret = connect_instance.command("cat /mnt/hda1/junxion/log/messages.4 | grep \"%s\"" %(reset_substring))
            ret_str = ''.join(ret)                             
            logging.debug(ret_str)
                                                             
            #basic_airlink.test_report(tbd_config_map["TEST_REPORT_FILE"],'PASSED : '+tc_id)
            #self.tc_pass_counter +=1
            #basic_airlink.cleanup()
        self.assertEqual(self.fail_flag,0)                

    def tc_dummy(self):
        pass