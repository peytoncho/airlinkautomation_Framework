#################################################################################
#
# This module automates LAN's DHCP/Addressing test cases. 
# Company: Sierra Wireless
# Date: Jul 5, 2013
# 
#################################################################################

from selenium import webdriver   
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import selenium.webdriver.remote.webdriver
from selenium_lan import LanSeleniumProcess
import time
import unittest
import selenium_utilities
import sys,os
import yaml
import rpyc
import StringIO
import subprocess
import threading
import at_utilities

airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")

sys.path.append(airlinkautomation_home_dirname+"/lib/common/UI")
import lan_airlink, wan_airlink

import basic_airlink
import connectivity
from cisco_config import CiscoConfig

tbd_config_map, lan_config_map = basic_airlink.get_config_data("LAN","")
    
@classmethod   
def setUpClass(cls):
    ''' a class method called before tests in an individual class run
    '''
    pass            
    
@classmethod   
def tearDownClass(cls):
    ''' a class method called after tests in an individual class have run
    '''
    pass            
   
class TsLanVrrp(unittest.TestCase):
    ''' This test suite automates LAN testcases by ACEmanager Web UI.
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
        
        
        self.fail_flag = 0
           
        self.verificationErrors = []
        self.accept_next_alert = True  

        self.test_config = {}
        self.test_config['ACEMANAGER_URL'] = tbd_config_map[tbd_config_map["DUTS"][0]]["ACE_URL"]
        self.test_config['ACEMANAGER_USER'] = tbd_config_map[tbd_config_map["DUTS"][0]]["USERNAME"]
        self.test_config['ACEMANAGER_PASSWORD'] = tbd_config_map[tbd_config_map["DUTS"][0]]["PASSWORD"]
        self.test_config["BROWSER"] = tbd_config_map["BROWSER"]
        
                
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert.text
        finally: self.accept_next_alert = True
        
          
    def tearDown(self):
        ''' the test runner will invoke that method after each test
        Args: None
        Returns: None
        '''        
        self.assertEqual([], self.verificationErrors) 

        basic_airlink.slog(" Testcase complete")
           
    def tc_vrrp_basic(self):
        """https://confluence.sierrawireless.com/display/ALENGINEERING/VRRP+Testbed
        """
        # test_config dict is passed around to functions when configuring stuff
        self.test_config["VRRP_ENABLE"] = "Enable"
        self.test_config["GROUP_ID"] = tbd_config_map["VRRP"]["GROUP_ID"]
        self.test_config["AIRLINK_PRIORITY"] = tbd_config_map["VRRP"]["AIRLINK_PRIORITY"]
        self.test_config["VIRTUAL_DEFAULT_GATEWAY"] = tbd_config_map["VRRP"]["VIRTUAL_DEFAULT_GATEWAY"]
        self.test_config["INTERVAL"] = tbd_config_map["VRRP"]["INTERVAL"]

        # change default gateway of Airlink host to 192.168.13.40
        basic_airlink.cslog("-> Changing Airlink host's default gateway to %s" %tbd_config_map["VRRP"]["VIRTUAL_DEFAULT_GATEWAY"])
        conn = rpyc.classic.connect(tbd_config_map["MANAGEMENT_IP"]["HOST1"])
        conn.modules.os.system('netsh interface ip set address name="%s" static %s %s %s' \
                %(tbd_config_map["VRRP"]["ETHERNET_ADAPTER_NAME"],tbd_config_map["PRIVATE_IP"]["HOST1"], tbd_config_map[self.device_name]["ETH_SUBNET_MASK"], \
                    tbd_config_map["VRRP"]["VIRTUAL_DEFAULT_GATEWAY"]))

        # Configure VRRP on Airlink Device
        self.configure_and_verify_airlink_device_settings()

        self.reboot_device()
        basic_airlink.cslog("-> Airlink device back on cellular network")

        basic_airlink.cslog("-> Verifying VRRP settings")
        self.configure_and_verify_airlink_device_settings(verify_only = True)


        for drop_interface in ["fastEthernet 1", "fastEthernet 0"]:
            basic_airlink.cslog(r"""
##############################################################
# Test connection to internet with %s going down #
##############################################################
""" %drop_interface)

            # Depending on which interface we will be dropping, use the other to telnet to the router
            router_ip = {"fastEthernet 0":tbd_config_map["VRRP"]["ROUTER"]["FE1_IP"],
                         "fastEthernet 1":tbd_config_map["VRRP"]["ROUTER"]["FE0_IP"]}[drop_interface]

            # Create Telnet session to Cisco router
            cisco = CiscoConfig(ip = router_ip, 
                    port = tbd_config_map["VRRP"]["ROUTER"]["TELNET_PORT"], 
                    username = tbd_config_map["VRRP"]["ROUTER"]["USERNAME"],
                    password = tbd_config_map["VRRP"]["ROUTER"]["TELNET_PASSWORD"],
                    hostname = tbd_config_map["VRRP"]["ROUTER"]["ROUTER_NAME"],
                    enable_password = tbd_config_map["VRRP"]["ROUTER"]["ENABLE_PASSWORD"],
                    debug_level = False,
                    verbose = False)
    
            # Check that the VRRP state is "Master" for the Cisco router
            vrrp_state = cisco.get_vrrp_state()
            if not vrrp_state == "Master":
                message = "TEST FAIL: VRRP State for Cisco router is not \'Master\'. It is \'%s\'" %vrrp_state
                basic_airlink.cslog(message, "RED")
                cisco.shutdown_interface(drop_interface, no_shutdown = True)
                self.fail(message)
            else:
                basic_airlink.cslog("** Cisco VRRP State: %s" %vrrp_state)
    
            # Have the Airlink host ping 8.8.8.8
            basic_airlink.cslog("-> Starting ping 8.8.8.8 with Airlink Host")
            self.packets_sent = 50
            self.packets_lost = self.packets_sent # This will be updated after the pings are done
            ping_thread = threading.Thread(target = self.get_remote_ping_statistics, args = (conn, "8.8.8.8", self.packets_sent))
            ping_thread.start()

            time.sleep(1)
    
            # take down FE1
            basic_airlink.cslog("-> shutting down %s on Cisco router" %drop_interface)
            cisco.shutdown_interface(drop_interface)

            self.sleep_with_print(2)

            vrrp_state = cisco.get_vrrp_state()
            if vrrp_state not in ["Init", "Backup"]:
                message = "TEST FAIL: VRRP State for Cisco router is not \'Init\' nor \'Backup\'. It is \'%s\'" %vrrp_state
                basic_airlink.cslog(message, "RED")
                cisco.shutdown_interface(drop_interface, no_shutdown = True)
                self.fail(message)
            else:
                basic_airlink.cslog("** Cisco VRRP State: %s" %vrrp_state)
    
            self.sleep_with_print(10)
    
            basic_airlink.cslog("-> Turning on %s on Cisco router" %drop_interface)
    
            cisco.shutdown_interface(drop_interface, no_shutdown = True)
    
            timeout = 60
            basic_airlink.cslog("-> Wait until the Cisco router becomes the Master again")
            start_time = time.time()
    
            while True:
                vrrp_state = cisco.get_vrrp_state()
                elapsed_time = time.time() - start_time
    
                if vrrp_state == "Master": # Master handed back to Cisco
                    basic_airlink.cslog("** Cisco VRRP State: %s. Elapsed time: %d seconds" %(vrrp_state, elapsed_time))
                    break
                elif elapsed_time > timeout: # Master not handed back to Cisco after a long time
                    message = "TEST FAIL: VRRP State for Cisco router did not return to 'Master' after restoring connection for %d seconds." %elapsed_time
                    basic_airlink.cslog(message, "RED")
                    cisco.shutdown_interface(drop_interface, no_shutdown = True)
                    self.fail(message)
    
            ping_thread.join() # wait for all the ping packets to finish
    
            packet_lost_threshold = 10
            basic_airlink.cslog("Total packets sent: %d, Total packets dropped: %d, threshold for not failing test: %d" %(self.packets_sent, self.packets_lost, packet_lost_threshold))
            if self.packets_lost > packet_lost_threshold:
                message = "TEST FAIL: More than %d packets were lost when %s on the Cisco router went down" %drop_interface
                basic_airlink.cslog(message, "RED")
                cisco.shutdown_interface(drop_interface, no_shutdown = True)
                self.fail(message)
        
        basic_airlink.cslog("** TEST PASS **", "GREEN")

        # Change default gateway for Airlink host back to the Airlink device's interface
        basic_airlink.cslog("-> Changing default gateway for Airlink host back to %s" %self.conn_ins.address())
        conn.modules.os.system('netsh interface ip set address name="%s" static %s %s %s' \
                %(tbd_config_map["VRRP"]["ETHERNET_ADAPTER_NAME"],tbd_config_map["PRIVATE_IP"]["HOST1"], tbd_config_map[self.device_name]["ETH_SUBNET_MASK"], \
                    self.conn_ins.address()))

        # Remove VRRP settings from the Airlink Device
        self.test_config["VRRP_ENABLE"] = "Disable"
        self.test_config["GROUP_ID"] = "0"
        self.test_config["AIRLINK_PRIORITY"] = "100"
        self.test_config["VIRTUAL_DEFAULT_GATEWAY"] = "0.0.0.0"
        self.test_config["INTERVAL"] = "1"

        basic_airlink.cslog("-> Turning off VRRP on Airlink Device")
        self.configure_and_verify_airlink_device_settings()

    def get_remote_ping_statistics(self, conn, ip, packets):
        p = conn.modules.subprocess.Popen('ping %s -n %d' %(ip, packets), stdout=conn.modules.subprocess.PIPE)
        output = p.communicate()[0]
        successful_pings = 0
        basic_airlink.slog(output)
        for line in output.split('\n'):
            if ("Reply from %s" %ip) in line:
                successful_pings += 1
        self.packets_lost = self.packets_sent - successful_pings

    def sleep_with_print(self, seconds): # lol
        basic_airlink.cslog("-> Sleep for %d seconds" %seconds)
        time.sleep(seconds)

    def configure_and_verify_airlink_device_settings(self, verify_only = False, attempts = 5):
        for attempts_remaining in range(attempts-1,-1,-1):
            if not verify_only:
                basic_airlink.cslog("-> Configuring Airlink device")
                LanSeleniumProcess.create_and_execute(LanSeleniumProcess.CONFIG_VRRP, self.test_config, 60, 1)

            basic_airlink.cslog("-> Verifying Airlink device settings")
            if LanSeleniumProcess.create_and_execute(LanSeleniumProcess.VERIFY_VRRP_CONFIGS, self.test_config, 60, 1):
                return # settings verified

            basic_airlink.cslog("-> Airlink device not set up correctly, retrying... %d attempts remaining" %attempts_remaining)

        message = "TEST FAIL: Could not %s Airlink device after %d attempts" %("verify" if verify_only else "configure/verify", attempts)
        basic_airlink.cslog(message, "RED")
        self.fail(message)

    def reboot_device(self, attempts = 10, sleep_time = 60):
        basic_airlink.cslog("-> Rebooting Airlink Device")

        for attempts_remaining in range(attempts-1,-1,-1):
            if not self.at_reboot(): # Reboot the device
                basic_airlink.cslog("** AT command to reboot failed **")
                time.sleep(10) # Try sending the AT command again after 10 seconds if not successful 
            else:
                # AT command is successful, wait for reboot to finish
                start_time = time.time() # keep track of how long we have to wait for device to go back on air
                time.sleep(sleep_time)

                if LanSeleniumProcess.create_and_execute(LanSeleniumProcess.WAIT_NETWORK_READY, self.test_config, 60, 30):
                    # back on air
                    reboot_time = time.time() - start_time # time it took to get back on air
                    basic_airlink.cslog("-> Device back on the cellular network after %d seconds." %int(reboot_time))

                    # minimum amount of time it should take to reboot. 
                    # if it takes less than this, then device might not have actually rebooted so we reboot it again
                    min_reboot_time = sleep_time + 20 

                    if reboot_time < min_reboot_time:
                        basic_airlink.cslog("** Reboot time was less than %d, DUT might not have actually rebooted. **" %(min_reboot_time))
                    else:
                        basic_airlink.cslog("-> Continuing with test")
                        return True
                else:
                    # not back on air after a long time
                    basic_airlink.cslog("** DUT could not get back on air. **")

            basic_airlink.cslog("-> rebooting DUT again, %s attempts remaining before failing test case" %attempts_remaining)

        message = "TEST FAIL: DUT reboot not successful"
        basic_airlink.cslog(message, "RED")
        self.fail(message)

    def at_reboot(self):
        try:
            tn_instance = connectivity.Connectivity().telnet_interface()
    
            if tn_instance.connect():
                time.sleep(2)
                at_cmd_ins = at_utilities.AtCommands()
                if not at_cmd_ins.set_datz(tn_instance, '0'):
                    basic_airlink.cslog("tn failed at set_datz()")
                    return False
                at_cmd_ins.atz_reboot(tn_instance) # atz_reboot never returns True because the connection shuts off immediately when the device reboots
            else:
                basic_airlink.cslog("tn failed at connect()")
                return False
        except Exception as e:
            basic_airlink.cslog(str(e))
            return False

        return True
