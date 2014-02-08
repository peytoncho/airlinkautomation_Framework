################################################################################
#
# This module automates VPN IPsec test cases. 
# Company: Sierra Wireless
# Date: Oct 1, 2013
# Author: Airlink
# 
################################################################################

import unittest
import basic_airlink
import connectivity
import cisco_config
from cisco_asa_config import *
import time
import datetime
import copy
import ping_airlink
import os
import yaml, proxy_airlink
from selenium_vpn import VpnSeleniumProcess
from cisco_vpn import VpnCiscoProcess
import types
import telnet_airlink
import at_utilities
import random
import re
import ipsec_vpn_tc_manager
from known_vpn_bugs import KnownVpnBugs
from ipv4 import Ipv4
import vpn_tc_wrappers

tbd_config_map = basic_airlink.get_tbd_config_data()

class TsVpn(unittest.TestCase, vpn_tc_wrappers.VpnTcWrappers):
    ''' This test suite automates VPN IPsec test cases.
        Please make sure testbed ready before execution.
    '''               
    def setUp(self):
        '''
        the test runner will run that method prior to each test
        '''

        basic_airlink.cslog(time.strftime("%b-%d-%Y %H:%M", time.localtime()))
        self.test_start_time = datetime.datetime.now()

        self.TEST_CONFIG = {}

        self.tc_name = self.id().split('.')[-1]
        
        self.skip_teardown = False
        self.fail_due_to_known_bug = False

        if ipsec_vpn_tc_manager.Combo.base_name in self.tc_name: # main ipsec vpn test cases
            # Some combinations are known to fail due to bugs, we do not skip them but fail them immediately so a failure is marked in the reports
            # refer to known_vpn_bugs.py 
            tc_number = ipsec_vpn_tc_manager.Combo.get_combo_number_from_name(self.tc_name)

            expect_to_pass, reasons = ipsec_vpn_tc_manager.Combo.from_number(tc_number).do_we_expect_this_combo_to_pass()

            if not expect_to_pass:
                self.skip_teardown = True
                message = "%s: TEST FAIL: " %self.tc_name
                for string in reasons:
                    message += "%s, " %string
                basic_airlink.cslog(message, "RED")
                # self.fail(message) # Don't fail in setup() because unittest marks them as 'error', fail in actual test so it gets marked 'fail'
                self.fail_due_to_known_bug = True
                self.fail_due_to_known_bug_msg = message 


        self.TEST_CONFIG['VPN_NO'] = random.choice(["1", "2", "3", "4", "5"])

        self.TEST_CONFIG['GATEWAY_ADDRESS'] = tbd_config_map["PUBLIC_IP"]["VPN_CISCO_ROUTER"]
        self.TEST_CONFIG['AIRLINK_SIM_STATIC'] = tbd_config_map["VPN"]["AIRLINK_SIM_STATIC"]
        self.TEST_CONFIG['AIRLINK_WAN_IP'] = tbd_config_map["VPN"]["AIRLINK_WAN_IP"]

        self.TEST_CONFIG['LOCAL_ADDRESS'] = tbd_config_map["VPN"]["AIRLINK_SUBNET"]
        self.TEST_CONFIG['LOCAL_ADDRESS_MASK'] = tbd_config_map["VPN"]["AIRLINK_SUBNET_MASK"]

        # cisco subnet mask 
        if self.tc_name.startswith("tc_ipsec_vpn_cisco_subnet_"):
            # These test cases varies the subnet mask of the cisco subnet
            # first we get the bitmask length from tc_name
            for length in self.tc_name.split("_"):
                try:
                    self.TEST_CONFIG['REMOTE_ADDRESS_MASK_LENGTH'] = int(length)
                    break
                except ValueError:
                    pass
        else:
            self.TEST_CONFIG['REMOTE_ADDRESS_MASK_LENGTH'] =  24
        cisco_subnet_mask_in_decimal = Ipv4.get_netmask(self.TEST_CONFIG['REMOTE_ADDRESS_MASK_LENGTH']) 
        self.TEST_CONFIG['REMOTE_ADDRESS_MASK'] = Ipv4.to_dotted_notation(cisco_subnet_mask_in_decimal) # in dotted notation

        # cisco subnet
        cisco_subnet = "172.20.20.0" # This may get truncated if the specified mask len is small
        self.TEST_CONFIG['REMOTE_ADDRESS'] = Ipv4.to_dotted_notation(Ipv4.to_decimal_notation(cisco_subnet) & cisco_subnet_mask_in_decimal)

        # cisco host ip address: always address 1 of the subnet - we calculate the ip address here.
        # address 2 of the subnet will be the inside interface on the cisco router 
        # address 3 and onward are excluded from the dhcp pool
        cisco_host_ip_in_decimal = Ipv4.to_decimal_notation(self.TEST_CONFIG['REMOTE_ADDRESS']) + 1
        self.TEST_CONFIG['CISCO_HOST'] = Ipv4.to_dotted_notation(cisco_host_ip_in_decimal)

        self.TEST_CONFIG['ACEMANAGER_URL'] = tbd_config_map[tbd_config_map["DUTS"][0]]["ACE_URL"]
        self.TEST_CONFIG['ACEMANAGER_USER'] = tbd_config_map[tbd_config_map["DUTS"][0]]["USERNAME"]
        self.TEST_CONFIG['ACEMANAGER_PASSWORD'] = tbd_config_map[tbd_config_map["DUTS"][0]]["PASSWORD"]

        self.TEST_CONFIG['AIRLINK_HOST'] = tbd_config_map["VPN"]["AIRLINK_HOST"]

        self.TEST_CONFIG['CISCO_TYPE'] = tbd_config_map["VPN"]["CISCO_TYPE"]

        if self.TEST_CONFIG['CISCO_TYPE'] == "IOS":
            self.TEST_CONFIG["TELNET_PORT"] = tbd_config_map["VPN"]["TELNET_PORT"]
            self.TEST_CONFIG["TELNET_USER"] = tbd_config_map["VPN"]["TELNET_USER"]
            self.TEST_CONFIG["TELNET_PASSWORD"] = tbd_config_map["VPN"]["TELNET_PASSWORD"]
            self.TEST_CONFIG["TELNET_HOSTNAME"] = tbd_config_map["VPN"]["TELNET_HOSTNAME"]
            debug_telnet = False
            self.TEST_CONFIG["TELNET_DEBUG"] = debug_telnet
            self.TEST_CONFIG["TELNET_VERBOSE"] = debug_telnet 
            self.TEST_CONFIG["CISCO_ENABLE_PASSWORD"] = tbd_config_map["VPN"]["IOS_ENABLE_PASSWORD"]
        elif self.TEST_CONFIG['CISCO_TYPE'] == "ASA":
            self.TEST_CONFIG["SSH_PORT"] = tbd_config_map["VPN"]["SSH_PORT"]
            self.TEST_CONFIG["SSH_USER"] = tbd_config_map["VPN"]["SSH_USERNAME"]
            self.TEST_CONFIG["SSH_PASSWORD"] = tbd_config_map["VPN"]["SSH_PASSWORD"]
            self.TEST_CONFIG["ASA_NAME"] = tbd_config_map["VPN"]["ASA_NAME"]
            self.TEST_CONFIG["ASA_ENABLE_PASSWORD"] = tbd_config_map["VPN"]["ASA_ENABLE_PASSWORD"]

        self.TEST_CONFIG["BROWSER"] = tbd_config_map["BROWSER"]

        if not self.tc_name == "tc_dummy":
            self.TEST_CONFIG["VPN_TYPE"] = self.get_tunnel_type_from_tc_name()


    def tearDown(self):
        ''' the test runner will invoke that method after each test.
        '''        
        if not self.skip_teardown:
            cleanup_cisco = True
            if cleanup_cisco:
                basic_airlink.cslog("-> clean up Cisco %s router" %self.TEST_CONFIG["CISCO_TYPE"])
                VpnCiscoProcess.create_and_execute(VpnCiscoProcess.CLEANUP_GATEWAY, self.TEST_CONFIG, 60, 5)
            else:
                basic_airlink.cslog("-> NOT clean up Cisco %s router" %self.TEST_CONFIG["CISCO_TYPE"], 'RED')
    
            self.disable_all_tunnels_on_airlink_device_settings()
            
            # kill any lingering browser (needed?)
            basic_airlink.cslog("-> closing all %s browser windows still open" %self.TEST_CONFIG["BROWSER"])
    
            if self.TEST_CONFIG["BROWSER"] == "FF":
                os.system("taskkill /im firefox.exe /t /f >nul 2>&1")
            elif self.TEST_CONFIG["BROWSER"] == "IE":
                os.system("taskkill /im IEDriverServer.exe /t /f >nul 2>&1")
                os.system("taskkill /im iexplore.exe /t /f >nul 2>&1")
            else:
                basic_airlink.cslog("Warning: Browser configuration is neither IE nor FF.", "BLUE")
        else:
            basic_airlink.cslog("-> Skipping tearDown()")

        message = time.strftime("%b-%d-%Y %H:%M", time.localtime()) + "\n"
        message += "Time elapsed: %s\n" %(datetime.datetime.now() - self.test_start_time)
        message += " Testcase complete\n"
        basic_airlink.cslog(message)

    def tc_vpn_default(self):
        """This function is called to perform the default IPsec and GRE test case.

        returns: None
        """

        if self.fail_due_to_known_bug:
            self.fail(self.fail_due_to_known_bug_msg)

        #######################################################################################################
        # Add the appropriate keys in the test config dictionary that will be used based on the type of test
        # - settings that are common to all types of test cases are done in self.setUp()
        #######################################################################################################
        if self.tc_name == "tc_gre_vpn_default_case":
            basic_airlink.cslog("Test Case: Default GRE VPN", "WHITE", "BLUE") 
            self.TEST_CONFIG["REMOTE_ADDRESS_TYPE"] = "Subnet Address"
            self.TEST_CONFIG["GRE_TTL"] = "255"
        elif ipsec_vpn_tc_manager.Combo.base_name in self.tc_name: # main ipsec vpn test cases
            tc_number = ipsec_vpn_tc_manager.Combo.get_combo_number_from_name(self.tc_name)
            basic_airlink.cslog("Test Case: Default IPsec VPN - combo number %d" %tc_number, "WHITE", "BLUE")

            combo = ipsec_vpn_tc_manager.Combo.from_number(tc_number)
            self.TEST_CONFIG = dict(combo.parameters.items() + self.TEST_CONFIG.items())
            basic_airlink.slog(str(combo))
        elif self.tc_name.startswith("tc_ipsec_vpn_cisco_subnet_"): # varying cisco subnet mask length
            # randomly pick a set of working parameters
            tc_number = None
            total_combos_available = ipsec_vpn_tc_manager.IpsecVpnTestCaseManager().num_tcs()

            while tc_number is None:
                temp_tc_number = random.randint(1,total_combos_available)
                combo = ipsec_vpn_tc_manager.Combo.from_number(temp_tc_number)
                if combo.do_we_expect_this_combo_to_pass()[0]:
                    tc_number = temp_tc_number

            self.TEST_CONFIG = dict(combo.parameters.items() + self.TEST_CONFIG.items())
            basic_airlink.cslog("Test Case: %s (%d)" %(self.tc_name, tc_number), "WHITE", "BLUE")
            basic_airlink.slog(str(combo))

        
        basic_airlink.cslog("-> begin test. vpn gateway @ %s" %self.TEST_CONFIG["GATEWAY_ADDRESS"])

        #=======================================================================
        # Set up and verify IPsec on Cisco Router
        #=======================================================================
        self.configure_and_verify_cisco_gateway_settings()

        #=======================================================================
        # Set up and reboot GX400
        #=======================================================================
        self.configure_and_verify_airlink_device_settings()

        self.reboot_device()

        #=======================================================================
        # Verify VPN settings in ACEmanager
        #=======================================================================
        self.configure_and_verify_airlink_device_settings(verify_only = True)

        test_failed = False 
        # checks past this point deals with the functionalities of the tunnel, 
        # we will perform all the tests and only fail at the very end of the script

        #=======================================================================
        # Verify that tunnel is up using ACEmanager before proceeding
        #=======================================================================
        timeout = 600
        if not self.check_acemanager_tunnel_status_connected(timeout):
            message = "TEST FAIL: Tunnel status on ACEmanager does not say \'Connected\' after %d seconds of being on back on the cellular network" %timeout
            basic_airlink.cslog(message, "RED")
            test_failed = True
     
        #=======================================================================
        # Verify if tunnel is up by pinging
        #=======================================================================            
        if not self.airlink_host_pings_cisco_host()[0]:
            message = "TEST FAIL: Cisco host could not ping Airlink host over the tunnel"
            basic_airlink.cslog(message, "RED")
            test_failed = True

        #=======================================================================
        # Verify tunnel on Cisco 
        #=======================================================================
        if not self.verify_tunnel_on_cisco_gateway():
            message = "TEST FAIL: Could not verify %s VPN tunnel on Cisco %s" %(self.TEST_CONFIG["VPN_TYPE"],self.TEST_CONFIG["CISCO_TYPE"])
            basic_airlink.cslog(message, "RED")
            test_failed = True

        #=======================================================================
        # Verify tunnel status on ACEmanager - with proxy
        #=======================================================================
        if not self.check_acemanager_tunnel_status_connected(proxy = True):
            message = "TEST FAIL: Tunnel status on ACEmanager does not say 'Connected'"
            basic_airlink.cslog(message, "RED")
            test_failed = True
            
        #=======================================================================
        # ping host behind DUT from host behind cisco    
        #=======================================================================
        if not self.airlink_host_pings_cisco_host(reverse_ping = True)[0]:
            message = "TEST FAIL: Cisco host could not ping Airlink host over the tunnel"
            basic_airlink.cslog(message, "RED")
            test_failed = True

        if test_failed:
            basic_airlink.cslog("** TEST FAILED **", "RED")
            self.fail("** TEST FAILED **")
        else:
            basic_airlink.cslog("** TEST PASS **", "GREEN")

    def tc_ipsec_vpn_mismatch(self, bad_parameter):
        """
        This test case tests that the tunnel does not come up
        when there is a mismatch in the settings between the DUT
        and the Cisco router.
        """
        basic_airlink.cslog("Test Case: IPsec VPN Mismatched Setting: %s" %bad_parameter, "WHITE", "BLUE") 

        # the other parameters and what the mismatched setting is changed to is chosen at random
        # set a seed for reproducibility 
        seed = random.randint(0,0xFFFFFFFF)

        random.seed(seed)
        basic_airlink.cslog("Seed used to pick base set up and mismatched setting: 0x%X" %seed)

        #=======================================================================
        # Prepare Test Configurations 
        #=======================================================================
        # generate a set of parameters 
        manager = ipsec_vpn_tc_manager.IpsecVpnTestCaseManager()
        while True:
            combo_number = random.randint(1, manager.num_tcs())
            combo = ipsec_vpn_tc_manager.Combo.from_number(combo_number)

            expect_to_pass, reason = combo.do_we_expect_this_combo_to_pass()
            if expect_to_pass and not combo.parameters["IPSEC_DH_GROUP"] == "DH1": 
                # can't use DH1 for phase 2 on cisco because it will accept DH2 and DH5 also
                break

        self.TEST_CONFIG = dict(combo.parameters.items() + self.TEST_CONFIG.items())

        # make a copy of the test config, modify it, then use it to configure the cisco
        temp_list = copy.deepcopy(manager.CONFIG_OPTIONS[bad_parameter]) # make a list of possible options that we can use for that setting on DUT that will screw up the test
        temp_list.remove(self.TEST_CONFIG[bad_parameter]) # remove the option that we are using on the DUT

        if bad_parameter in KnownVpnBugs.ipsec.keys(): 
            # The parameter we are testing has an option that is bugged, remove the bugged options
            for bugged_option in KnownVpnBugs.ipsec[bad_parameter]:
                try:
                    temp_list.remove(bugged_option)
                except ValueError:
                    pass

        # for phase 2 dh group, cisco IOS will accept proposal as long as the proposed value is higher than what it is configured to accept
        # thus we make sure that we only pick something that is lower so the tunnel will not come up
        if bad_parameter == "IPSEC_DH_GROUP":
            level = ["None", "DH1", "DH2", "DH5"] # higher index means higher security
            for lvl in level:
                if level.index(lvl) > level.index(self.TEST_CONFIG["IPSEC_DH_GROUP"]):
                    #           ^-DUT                            ^- Cisco
                    try:
                        temp_list.remove(lvl)
                    except ValueError:
                        pass

        new_setting = random.choice(temp_list) # pick the new setting

        basic_airlink.cslog("** Using IPsec VPN Default combination %d as a base: using %s on Cisco router and %s on DUT for %s" %(combo_number,self.TEST_CONFIG[bad_parameter],new_setting,bad_parameter))

        #=======================================================================
        # Set up and verify IPsec on Cisco Router - The cisco router will use
        # the original setting from the default test case
        #=======================================================================
        self.configure_and_verify_cisco_gateway_settings()

        #=======================================================================
        # Set up and reboot GX400 - the DUT will use the test config that
        # has one of its setting changed
        #=======================================================================
        # Change the appropriate setting in self.TEST_CONFIG
        self.TEST_CONFIG[bad_parameter] = new_setting

        self.configure_and_verify_airlink_device_settings()

        self.reboot_device()

        #=======================================================================
        # Verify VPN settings in ACEmanager
        #=======================================================================
        self.configure_and_verify_airlink_device_settings(verify_only = True)

        test_failed = False

        #=======================================================================
        # Look for error message on cisco router
        #=======================================================================
        if not self.wait_error_message_on_cisco(bad_parameter):
            message = "TEST FAIL: Error message never showed up in Cisco debug log."
            basic_airlink.cslog(message, "RED")
            test_failed = True


        #=======================================================================
        # Check ACEmanager to make sure that it does not say 'Connected'
        #=======================================================================
        if self.check_acemanager_tunnel_status_connected():
            message = "TEST FAIL: Tunnel status on ACEmanager says \'Connected\'"
            basic_airlink.cslog(message, "RED")
            test_failed = True

        #=======================================================================
        # verify that airlink host cannot ping cisco host
        #=======================================================================            
        pinged, delivered = self.airlink_host_pings_cisco_host(ping_attempts = 3)
        if not delivered:
            message = "Test fail: Could not deliver PyRC object!"
            basic_airlink.cslog(message, "RED")
            test_failed = True
        elif pinged:
            message = "Test fail: Airlink host should not be able to ping the Cisco host for this test"
            basic_airlink.cslog(message, "RED")
            test_failed = True

        #=======================================================================
        # verify that cisco host cannot ping airlink host
        #=======================================================================            
        if not tbd_config_map["MANAGEMENT_IP"]["HOST2"] == "0.0.0.0":
            pinged, delivered = self.airlink_host_pings_cisco_host(reverse_ping = True, ping_attempts = 3)
            if not delivered:
                message = "Test fail: Could not deliver PyRC object!"
                basic_airlink.cslog(message, "RED")
                test_failed = True
            elif pinged:
                message = "Test fail: Airlink host should not be able to ping the Cisco host for this test"
                basic_airlink.cslog(message, "RED")
                test_failed = True
        else:
            basic_airlink.cslog("Skipping ping test from Cisco Host to Airlink Host due to the absence of a management switch")

        if test_failed:
            basic_airlink.cslog("** TEST FAILED **", "RED")
            self.fail("** TEST FAILED **")
        else:
            basic_airlink.cslog("** TEST PASS **", "GREEN")

    def tc_dummy(self):
#        tc_number = random.randint(0, 8000)
#        basic_airlink.cslog("Test Case: Dummy (%d)" %tc_number, "WHITE", "RED")
#
#        combo = ipsec_vpn_tc_manager.Combo.from_number(tc_number)
#        self.TEST_CONFIG = dict(combo.parameters.items() + self.TEST_CONFIG.items())
#        basic_airlink.slog(str(combo))
#
#        self.TEST_CONFIG["VPN_TYPE"] = "IPSEC"
#
#        if not VpnSeleniumProcess.create_and_execute(VpnSeleniumProcess.VERIFY_TUNNEL, self.TEST_CONFIG, 60, 5):
#        #if not VpnSeleniumProcess.create_and_execute(VpnSeleniumProcess.VERIFY_TUNNEL, self.TEST_CONFIG, 60, 5, "192.168.13.100"):
#            message = "TEST FAIL: Tunnel status on ACEmanager does not say \'Connected\'"
#            basic_airlink.cslog(message, "RED")
#            test_failed = True

        basic_airlink.cslog("** TEST PASS **", "GREEN")

    def configure_and_verify_cisco_gateway_settings(self, attempts = 5):
        for attempts_remaining in range(attempts-1,-1,-1):
            basic_airlink.cslog("-> clearing cisco %s settings" %self.TEST_CONFIG["CISCO_TYPE"])
            VpnCiscoProcess.create_and_execute(VpnCiscoProcess.CLEANUP_GATEWAY, self.TEST_CONFIG, 60, 5)
            if self.TEST_CONFIG["VPN_TYPE"] == "IPSEC":
                basic_airlink.cslog("-> configuring cisco %s ipsec vpn settings" %self.TEST_CONFIG["CISCO_TYPE"])
                VpnCiscoProcess.create_and_execute(VpnCiscoProcess.CONFIG_GATEWAY, self.TEST_CONFIG, 60, 5)
                basic_airlink.cslog("-> verifying cisco %s ipsec vpn settings" %self.TEST_CONFIG["CISCO_TYPE"])
    
                if VpnCiscoProcess.create_and_execute(VpnCiscoProcess.VERIFY_GATEWAY, self.TEST_CONFIG, 60, 5):
                    return
            elif self.TEST_CONFIG["VPN_TYPE"] == "GRE":
                basic_airlink.cslog("-> configuring and verifying cisco router GRE vpn settings")
                if VpnCiscoProcess.create_and_execute(VpnCiscoProcess.CONFIG_AND_VERIFY_GRE_GATEWAY, self.TEST_CONFIG, 60, 5):
                    return

            basic_airlink.cslog("-> Cisco %s not set up correctly, retrying... %d attempts remaining" %(self.TEST_CONFIG["CISCO_TYPE"], attempts_remaining))

        message = "TEST FAIL: Cannot configure Cisco %s after %d attempts" %(self.TEST_CONFIG["CISCO_TYPE"], attempts)
        basic_airlink.cslog(message, "RED")
        self.fail(message)

    def configure_and_verify_airlink_device_settings(self, verify_only = False, attempts = 5):
        for attempts_remaining in range(attempts-1,-1,-1):
            if not verify_only:
                basic_airlink.cslog("-> Configuring Airlink device")
                if self.TEST_CONFIG["VPN_TYPE"] == "IPSEC":
                    VpnSeleniumProcess.create_and_execute(VpnSeleniumProcess.CONFIG_VPN, self.TEST_CONFIG, 60, 1)
                elif self.TEST_CONFIG["VPN_TYPE"] == "GRE":
                    VpnSeleniumProcess.create_and_execute(VpnSeleniumProcess.CONFIG_GRE_VPN, self.TEST_CONFIG, 60, 1)

            basic_airlink.cslog("-> Verifying Airlink device settings")
            if self.TEST_CONFIG["VPN_TYPE"] == "IPSEC":
                if VpnSeleniumProcess.create_and_execute(VpnSeleniumProcess.VERIFY_VPN, self.TEST_CONFIG, 60, 1):
                    return # settings verified
            elif self.TEST_CONFIG["VPN_TYPE"] == "GRE":
                if VpnSeleniumProcess.create_and_execute(VpnSeleniumProcess.VERIFY_GRE_VPN, self.TEST_CONFIG, 60, 1):
                    return # settings verified

            basic_airlink.cslog("-> Airlink device not set up correctly, retrying... %d attempts remaining" %attempts_remaining)

        message = "TEST FAIL: Could not %s Airlink device after %d attempts" %("verify" if verify_only else "configure/verify", attempts)
        basic_airlink.cslog(message, "RED")
        self.fail(message)

    def reboot_device(self, attempts = 10, sleep_time = 60):
        basic_airlink.cslog("-> rebooting DUT")

        for attempts_remaining in range(attempts-1,-1,-1):
            if not self.at_reboot(): # Reboot the device
                basic_airlink.cslog("** AT command to reboot failed **")
                time.sleep(10) # Try sending the AT command again after 10 seconds if not successful 
            else:
                # AT command is successful, wait for reboot to finish
                start_time = time.time() # keep track of how long we have to wait for device to go back on air
                time.sleep(sleep_time)

                if VpnSeleniumProcess.create_and_execute(VpnSeleniumProcess.WAIT_NETWORK_READY, self.TEST_CONFIG, 60, 30):
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
                    return False
                at_cmd_ins.atz_reboot(tn_instance) # atz_reboot never returns True because the connection shuts off immediately when the device reboots
            else:
                return False
        except Exception as e:
            return False

        return True

    def check_acemanager_tunnel_status_connected(self, timeout = 300, proxy = False):
        proxy_ip = self.get_proxy_ip("AIRLINK_HOST") if proxy else None

        basic_airlink.cslog("-> Checking tunnel status on ACEmanager")
        start_time = time.time()
        while not VpnSeleniumProcess.create_and_execute(VpnSeleniumProcess.VERIFY_TUNNEL, self.TEST_CONFIG, 60, 1, proxy_ip):
            # Sometimes the tunnel does not come up until traffic is passed through it.
            self.airlink_host_pings_cisco_host(ping_attempts = 1, verbose = False)

            if time.time() - start_time > timeout:
                return False
        return True

    def get_tunnel_type_from_tc_name(self):
        for part in self.tc_name.upper().split("_"):
            if part in ["IPSEC", "GRE", "SSL"]:
                return part

        raise ValueError # All VPN test case names shall have its tunnel type in it

    def get_proxy_ip(self, host):
        ip = {"AIRLINK_HOST": tbd_config_map["MANAGEMENT_IP"]["HOST1"],
              "CISCO_HOST": tbd_config_map["MANAGEMENT_IP"]["HOST2"]}[host]

        if ip == "0.0.0.0": # no management switch in test bed, return actual IP address through DUT or tunnel
            ip = self.TEST_CONFIG[host]

        return ip

    def airlink_host_pings_cisco_host(self, reverse_ping = False, pyrc_deliver_attempts = 10, ping_attempts = 10, verbose = True):
        # if reverse_ping is True then the cisco host pings the airlink host instead

        # Set ip addresses
        # pinger_ip: ip address of pinger 
        # pingee_ip: ip address of pingee
        # pyrc_ip: ip address to deliver proxy ping object to (possibly same as pinger_ip if there's no management switch set up)
        pyrc_ip = self.get_proxy_ip("AIRLINK_HOST" if not reverse_ping else "CISCO_HOST")

        if not reverse_ping: # airlink host pings cisco host
            pingee_ip = self.TEST_CONFIG["CISCO_HOST"]
            pinger_ip = self.TEST_CONFIG["AIRLINK_HOST"]
        else: # cisco host pings airlink host
            pinger_ip = self.TEST_CONFIG["CISCO_HOST"]
            pingee_ip = self.TEST_CONFIG["AIRLINK_HOST"]

        if verbose:
            basic_airlink.cslog("-> Ping test: %s => %s, management ip = %s" %(pinger_ip, pingee_ip, pyrc_ip))

        for attempts_remaining in range(pyrc_deliver_attempts-1,-1,-1): # deliver PyRC object
            self.proxy=proxy_airlink.ProxyAirlink(pyrc_ip)
            self.conn = self.proxy.connect()
    
            ping = ping_airlink.PingAirlink()
            remote_ping = self.proxy.deliver(ping)

            if type(remote_ping) is not types.BooleanType:
                break
            elif not attempts_remaining: 
                if verbose: 
                    basic_airlink.cslog("** Failed to deliver PyRC object! **")
                return False, False # Ping not successful, PyRC not delivered

            time.sleep(10)

        for attempts_remaining in range(ping_attempts-1,-1,-1): # perform ping
            if remote_ping.ping_test(pingee_ip):
                return True, True # Ping successful, PyRC delivered

        return False, True # Ping not successful, PyRC delivered

    def verify_tunnel_on_cisco_gateway(self):
        if self.TEST_CONFIG["VPN_TYPE"] == "IPSEC":
            basic_airlink.cslog("-> checking SA on Cisco %s" %self.TEST_CONFIG["CISCO_TYPE"])
            if not VpnCiscoProcess.create_and_execute(VpnCiscoProcess.CHECK_SA, self.TEST_CONFIG, 60, 5):
                return False
        elif self.TEST_CONFIG["VPN_TYPE"] == "GRE":
            basic_airlink.cslog("-> checking GRE tunnel on Cisco router")
            if not VpnCiscoProcess.create_and_execute(VpnCiscoProcess.CHECK_GRE_TUNNEL, self.TEST_CONFIG, 60, 5):
                return False
        return True

    def wait_error_message_on_cisco(self, bad_parameter):
        basic_airlink.cslog("-> Looking for error message on Cisco router")

        # Set what error message to look for for different test
        # cisco router doesn't tell exactly which phase 2 setting is wrong
        if self.TEST_CONFIG["CISCO_TYPE"] == "IOS":
            self.TEST_CONFIG["CISCO_WAIT_MESSAGE"] = {"IKE_ENCRYPTION":re.escape('Encryption algorithm offered does not match policy!'),
                                                      "IKE_AUTHENTICATION":re.escape('Hash algorithm offered does not match policy!'),
                                                      "IKE_DH_GROUP":re.escape('Diffie-Hellman group offered does not match policy!'),
                                                      "IPSEC_ENCRYPTION":re.escape('phase 2 SA policy not acceptable!'),
                                                      "IPSEC_AUTHENTICATION":re.escape('phase 2 SA policy not acceptable!'),
                                                      "IPSEC_DH_GROUP":re.escape('phase 2 SA policy not acceptable!')}[bad_parameter]
        else: # ASA
            self.TEST_CONFIG["CISCO_WAIT_MESSAGE"] = {"IKE_ENCRYPTION":'All SA proposals found unacceptable',
                                                      "IKE_AUTHENTICATION":'All SA proposals found unacceptable',
                                                      "IKE_DH_GROUP":'All SA proposals found unacceptable',
                                                      "IPSEC_ENCRYPTION":'All IPSec SA proposals found unacceptable',
                                                      "IPSEC_AUTHENTICATION":'All IPSec SA proposals found unacceptable',
                                                      "IPSEC_DH_GROUP":'All IPSec SA proposals found unacceptable'}[bad_parameter]
                                   
        # we need a timeout because the negotiation log doesn't appear right away after turning on debug
        self.TEST_CONFIG["CISCO_WAIT_MESSAGE_TIMEOUT"] = 2*60

        return VpnCiscoProcess.create_and_execute(VpnCiscoProcess.WATCH_ERROR_MESSAGE, self.TEST_CONFIG, 2*self.TEST_CONFIG["CISCO_WAIT_MESSAGE_TIMEOUT"], 2)

    def disable_all_tunnels_on_airlink_device_settings(self, attempts = 5):
        for attempts_remaining in range(attempts-1,-1,-1):
            basic_airlink.cslog("-> Disabling all tunnels on Airlink Device")
            VpnSeleniumProcess.create_and_execute(VpnSeleniumProcess.DISABLE_ALL_TUNNELS, self.TEST_CONFIG, 60, 1)

            basic_airlink.cslog("-> Verifying all tunnels disabled on Airlink device")
            if VpnSeleniumProcess.create_and_execute(VpnSeleniumProcess.VERIFY_ALL_TUNNELS_DISABLED, self.TEST_CONFIG, 60, 1):
                return # settings verified

            basic_airlink.cslog("-> Tunnels not disabled on Airlink device, retrying... %d attempts remaining" %attempts_remaining)

        message = "TEST FAIL: Could not turn off all tunnels on Airlink device"
        basic_airlink.cslog(message, "RED")
        self.fail(message)
