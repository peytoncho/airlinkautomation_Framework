
from selenium.webdriver.support.ui import Select
import time
import ping_airlink 
import telnet_airlink 
import selenium_utilities
import sys
import basic_airlink 
import yaml
import logging
import cisco_config
import datetime


def yaml_include(loader,node):
    with file(node.value) as inputfile:
        return yaml.load(inputfile)
                
                
class TestsuiteVpn():
    ''' VPN test suite include all VPN test cases tc_
    
    '''
                     
    
    def __init__(self, debug_level = "0", verbose = False):
        ''' check all related items in testbed2 for VPN testing '''

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
        device_name  = self.tbd_config_map["DUTS"][0]
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"], "\nALEOS FW : " + self.tbd_config_map[device_name]["ALEOS_FW_VER"])
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"], "\nRADIO MODULE FW : " + self.tbd_config_map[device_name]["RADIO_FW_VER"]+'\n')       
 
        self.se_ins = selenium_utilities.SeleniumAcemanager()
           
        
    def testbed_ready(self):
        ''' check if the testbed ready 
        
        '''
    
        #ping_ins = ping_airlink.PingAirlink()
        
        # step: check if DUT ready
        for device in self.tbd_config_map["DUTS"]:
            print device
            telnet_instance = telnet_airlink.TelnetAirlink( hostname=self.tbd_config_map[device]["LAN_IP"], port = "2332", username = "user", password = "12345",debug_mode= False)
            if telnet_instance.connect():  
                logging.debug("DUT ready\n")                
            else: 
                logging.debug("DUT not ready yet\n")    
                return False

        #telnet_instance.close()
        
        ping_ins = ping_airlink.PingAirlink()
        
        # step: check if OTA ready
        if ping_ins.ping_test("8.8.8.8"): 
            logging.debug("OTA ready\n")                
        else: 
            logging.debug("OTA not ready yet\n")    
            return False                
          
        # step: check if the cisco router ready 
        if ping_ins.ping_test(self.tbd_config_map["ROUTER"]["WAN_IP"][0]): 
            logging.debug("Cisco router ready\n")                
        else: 
            logging.debug("Cisco router not ready yet\n")    
            return False
         
        #ping_ins.close()
           
        return True
    
    
    def processing_config(self):
        ''' to transfer info from yaml config files to list
        
        
        '''
        sys.path.append("/airlinkautomation/testsuite/GX440/common")
        sys.path.append("/airlinkautomation/testsuiteGX440/VPN")
        sys.path.append("/Python27/DLLs")
        sys.path.append("/Python27/Lib")
        sys.path.append("/Python27/Lib/site-packages")
        sys.path.append("/Python27/Lib/site-packages/selenium")
        sys.path.append("/Python27/Lib/site-packages/yaml")
        
        fo_tbd=open('/airlinkautomation/config/testbed2conf.yml','r')
        self.tbd_config_map = yaml.load(fo_tbd)
        fo_tbd.close()
        
        current_date_str = str(datetime.datetime.now().date())
        current_time_str = str(datetime.datetime.now().time()).replace(":","-")
        log_filename = \
        self.tbd_config_map["LOG_FILE_FOLDER"]+current_date_str+"_"+current_time_str+"_"+"_vpn_testsuite.log"
        FORMAT ='%(asctime)-15s => %(levelname)-8s => %(message)s'
        LEVEL=basic_airlink.log_level[self.tbd_config_map["PYTHON_LOGGING_LEVEL"]]
        print log_filename, FORMAT, LEVEL
        #logging.basicConfig(filename = FILENAME, format=FORMAT, level = logging.DEBUG)
        logging.basicConfig(filename = log_filename, format=FORMAT, level = LEVEL)       
        return                  
 
              
    def cleanup(self):
        ''' test case cleanup '''
        logging.debug("step: cleanup")
    
        return
        
    
    #TODO: this will be implemented in testsuite_snmp.py
    def ipsec_vpn_snmp_setting(self, vpn_no):
        '''IPSEC setting by  SNMP  commands  '''

        return

    def ipsec_vpn_at_setting(self, vpn_no):
        '''IPSEC setting by telnet and AT commands'''
        
        _device   = self.tbd_config_map["DUTS"][0]
        _hostname = self.tbd_config_map[_device]["LAN_IP"] 
        print _hostname        
        telnet_instance = telnet_airlink.TelnetAirlink( hostname=_hostname, port = "2332", username = "user", password = "12345",debug_mode= False)
        if not (telnet_instance.connect()):
            return False

 
        #step: set VPN type
        logging.debug("set VPN type")
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_TUNNEL_TYPE="+str(vpn_config_map["IPSEC_TUNNEL"]["VPN_TYPE"]["VALUE"]))

        ret_str = ''.join(ret)
        if ret_str.find("OK"): 
            logging.debug(' setting VPN type  OK \n')
        else:
            logging.debug(' setting VPN type  not OK   \n')
            return False
        
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_AUTH="+str(vpn_config_map["IPSEC_TUNNEL"]["IPSEC_AUTH"]["VALUE"][vpn_no-1]))
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_DH="+str(vpn_config_map["IPSEC_TUNNEL"]["IPSEC_KEY_GROUP"]["VALUE"][vpn_no-1]))
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_ENCRYPT="+str(vpn_config_map["IPSEC_TUNNEL"]["IPSEC_ENCRYPT"]["VALUE"][vpn_no-1]))

        #step: set VPN gateway 
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_GATEWAY="+str(vpn_config_map["IPSEC_TUNNEL"]["VPN_GATEWAY"]["VALUE"][vpn_no-1]))

        ret_str = ''.join(ret)
        if ret_str.find("OK"): 
            logging.debug(' setting VPN gateway  OK \n')
        else:
            logging.debug(' setting VPN gateway  not OK   \n')
            return False
        
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_IKE_AUTH="+str(vpn_config_map["IPSEC_TUNNEL"]["IKE_AUTH"]["VALUE"][vpn_no-1]))
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_IKE_DH="+str(vpn_config_map["IPSEC_TUNNEL"]["IKE_KEY_GROUP"]["VALUE"][vpn_no-1]))
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_IKE_ENCRYPT="+str(vpn_config_map["IPSEC_TUNNEL"]["IKE_ENCRYPT"]["VALUE"][vpn_no-1]))
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_IKE_LIFETIME="+str(vpn_config_map["IPSEC_TUNNEL"]["IKE_SA_TIME"]["VALUE"][vpn_no-1]))
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_LOCAL_ADDR="+str(vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDRESS"]["VALUE"][vpn_no-1]))
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_LOCAL_ADDR_MASK="+vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDRESS_MASK"]["VALUE"][vpn_no-1])
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_LOCAL_ADDR_TYPE="+str(vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDRESS_TYPE"]["VALUE"][vpn_no-1]))
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_LOCAL_ID="+vpn_config_map["IPSEC_TUNNEL"]["MY_ID"]["VALUE"][vpn_no-1])
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_LOCAL_ID_TYPE="+str(vpn_config_map["IPSEC_TUNNEL"]["MY_ID_TYPE"]["VALUE"][vpn_no-1]))
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_NEG_MODE="+str(vpn_config_map["IPSEC_TUNNEL"]["NEG_MODE"]["VALUE"][vpn_no-1]))
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_PFS="+str(vpn_config_map["IPSEC_TUNNEL"]["PERFECT_FW_SECURITY"]["VALUE"][vpn_no-1]))
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_REMOTE_ADDR="+vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDRESS"]["VALUE"][vpn_no-1])
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_REMOTE_ADDR_MASK="+vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDRESS_MASK"]["VALUE"][vpn_no-1])
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_REMOTE_ADDR_TYPE="+str(vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDRESS_TYPE"]["VALUE"][vpn_no-1]))
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_REMOTE_ID="+vpn_config_map["IPSEC_TUNNEL"]["PEER_ID"]["VALUE"][vpn_no-1])
        ret = telnet_instance.command("at*ipsec"+str(vpn_no)+"_REMOTE_ID_TYPE="+str(vpn_config_map["IPSEC_TUNNEL"]["PEER_ID_TYPE"]["VALUE"][vpn_no-1]))
            
        ret_str = ''.join(ret)
        if ret_str.find("OK"): 
            logging.debug(' setting VPN type  OK \n')
        else:
            logging.debug(' setting VPN type  not OK   \n')
            return False
 
        # Step: apply and reboot DUT
        logging.debug("step: apply and reboot DUT by AT command")
        ret = telnet_instance.command("atz")
        
        # Step: wait till device ready
        logging.debug("step: wait till device ready" +'\n')  
        time.sleep(vpn_config_map["TESTBED2"]["DUT1"]["REBOOT_TIMEOUT"])
        
        return True       

        
       #TODO: temp-hold this part 
    def ipsec_vpn_msciid_setting(self, vpn_no):
        '''IPSEC setting by MSCIIDs'''

        return
        
        
    def set_vpn_type_at(self, vpn_no, vpn_type):
        ''' set vpn type by telnet and at commands '''
        
        _device   = self.tbd_config_map["DUTS"][0]
        _hostname = self.tbd_config_map[_device]["LAN_IP"] 
        telnet_instance = telnet_airlink.TelnetAirlink( hostname=_hostname, port = "2332", username = "user", password = "12345",debug_mode= False)
        
        if not (telnet_instance.connect()): 
            logging.debug("Telnet to " + _hostname +" failed")
            return False
        
        if   vpn_no == 1: 
            ret = telnet_instance.command("at*ipsec1_tunnel_type="+str(vpn_type))
        elif vpn_no == 2: 
            ret = telnet_instance.command("at*ipsec2_tunnel_type="+str(vpn_type)) 
        elif vpn_no == 3: 
            ret = telnet_instance.command("at*ipsec3_tunnel_type="+str(vpn_type)) 
        elif vpn_no == 4: 
            ret = telnet_instance.command("at*ipsec4_tunnel_type="+str(vpn_type)) 
        elif vpn_no == 5: 
            ret = telnet_instance.command("at*ipsec5_tunnel_type="+str(vpn_type)) 
        else: 
            logging.info("wrong VPN number")
            return True
      
        ret_str = ''.join(ret)
        if ret_str.find("OK"): 
            logging.debug(' setting VPN type  OK \n')
        else:
            logging.debug(' setting VPN type  not OK   \n')
            return False
                
       
        return True
  
  
    def ipsec_vpn_ui_setting(self, vpn_no):
        '''VPN IPSEC setting by AceManager UI/Selenium'''

        # step: login to Ace Manager 
        logging.debug("step: login to Ace Manager")
        selenium_instance = selenium_utilities.SeleniumAcemanager()
        _device  = self.tbd_config_map["DUTS"][0]
        driver = selenium_instance.login(self.tbd_config_map[_device]["ACE_URL"], self.tbd_config_map[_device]["USERNAME"], self.tbd_config_map[_device]["PASSWORD"])

        time.sleep(self.tbd_config_map[_device]["ACE_LOGIN_WAIT"])                     
        
        # step: come to VPN page from AceManager
        logging.debug("step: from Ace Manager come to VPN: " + str(vpn_no))
        driver.find_element_by_css_selector("#VPNM1 > a > span").click()

        if   vpn_no == 1: 
            driver.find_element_by_xpath("//li[@id='SM1_VPN_VPN 1M1']/a/span").click()
        elif vpn_no == 2: 
            driver.find_element_by_xpath("//li[@id='SM1_VPN_VPN 2M1']/a/span").click()
        elif vpn_no == 3: 
            driver.find_element_by_xpath("//li[@id='SM1_VPN_VPN 3M1']/a/span").click()
        elif vpn_no == 4: 
            driver.find_element_by_xpath("//li[@id='SM1_VPN_VPN 4M1']/a/span").click()
        elif vpn_no == 5: 
            driver.find_element_by_xpath("//li[@id='SM1_VPN_VPN 5M1']/a/span").click()   
            
        #step: set VPN type
        logging.debug("set VPN type")
        Select(driver.find_element_by_name(vpn_config_map["IPSEC_TUNNEL"]["VPN_TYPE"]["MSCIID"][vpn_no-1])).select_by_visible_text(vpn_config_map["IPSEC_TUNNEL"]["VPN_TYPE"]["VISIBLE_TEXT"])
        
        #step: set VPN gateway 
        logging.debug("set VPN gateway")
        selenium_instance.set_element_by_name(driver,vpn_config_map["IPSEC_TUNNEL"]["VPN_GATEWAY"]["MSCIID"][vpn_no-1],vpn_config_map["IPSEC_TUNNEL"]["VPN_GATEWAY"]["VALUE"])
 
        #step: set PSK1 
        logging.debug("step: set PSK1 ")
        selenium_instance.set_element_by_name(driver,vpn_config_map["IPSEC_TUNNEL"]["PSK1"]["MSCIID"][vpn_no-1],vpn_config_map["IPSEC_TUNNEL"]["PSK1"]["VALUE"])
        
        # step: set My ID type
        logging.debug("step: set My ID type")
        Select(driver.find_element_by_name(vpn_config_map["IPSEC_TUNNEL"]["MY_ID_TYPE"]["MSCIID"][vpn_no-1])).select_by_visible_text(vpn_config_map["IPSEC_TUNNEL"]["MY_ID_TYPE"]["VISIBLE_TEXT"][vpn_no-1])
        
        # step: set Peer ID type
        logging.debug("step: set Peer ID type")
        Select(driver.find_element_by_name(vpn_config_map["IPSEC_TUNNEL"]["PEER_ID_TYPE"]["MSCIID"][vpn_no-1])).select_by_visible_text(vpn_config_map["IPSEC_TUNNEL"]["PEER_ID_TYPE"]["VISIBLE_TEXT"][vpn_no-1])
        
        # step: set Negotiation mode
        logging.debug("step: set Negotiation mode")
        Select(driver.find_element_by_name(vpn_config_map["IPSEC_TUNNEL"]["NEG_MODE"]["MSCIID"][vpn_no-1])).select_by_visible_text(vpn_config_map["IPSEC_TUNNEL"]["NEG_MODE"]["VISIBLE_TEXT"][vpn_no-1])

        # step: set IKE encryption/auth/group/SA Life time
        logging.debug("step: set IKE encryption/auth/group/SA Life time")
        Select(driver.find_element_by_name(vpn_config_map["IPSEC_TUNNEL"]["IKE_ENCRYPT"]["MSCIID"][vpn_no-1])).select_by_visible_text(vpn_config_map["IPSEC_TUNNEL"]["IKE_ENCRYPT"]["VISIBLE_TEXT"][vpn_no-1])
        Select(driver.find_element_by_name(vpn_config_map["IPSEC_TUNNEL"]["IKE_AUTH"]["MSCIID"][vpn_no-1])).select_by_visible_text(vpn_config_map["IPSEC_TUNNEL"]["IKE_AUTH"]["VISIBLE_TEXT"][vpn_no-1])
        Select(driver.find_element_by_name(vpn_config_map["IPSEC_TUNNEL"]["IKE_KEY_GROUP"]["MSCIID"][vpn_no-1])).select_by_visible_text(vpn_config_map["IPSEC_TUNNEL"]["IKE_KEY_GROUP"]["VISIBLE_TEXT"][vpn_no-1])
        selenium_instance.set_element_by_name(driver,vpn_config_map["IPSEC_TUNNEL"]["IKE_SA_TIME"]["MSCIID"][vpn_no-1],vpn_config_map["IPSEC_TUNNEL"]["IKE_SA_TIME"]["VALUE"][vpn_no-1])
        
        # step: set local address type/
        logging.debug("step: set local address type/")
        Select(driver.find_element_by_name(vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDRESS_TYPE"]["MSCIID"][vpn_no-1])).select_by_visible_text(vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDRESS_TYPE"]["VISIBLE_TEXT"][vpn_no-1])
        if  vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDRESS_TYPE"]["VISIBLE_TEXT"][vpn_no-1] == "Single Address": 
            selenium_instance.set_element_by_name(driver,vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDRESS"]["MSCIID"][vpn_no-1],vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDRESS"]["VALUE"])
        elif  vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDRESS_TYPE"]["VISIBLE_TEXT"][vpn_no-1] == "Subnet Address":   
            selenium_instance.set_element_by_name(driver,vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDRESS"]["MSCIID"][vpn_no-1],vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDRESS"]["VALUE"])
            selenium_instance.set_element_by_name(driver,vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDRESS_MASK"]["MSCIID"][vpn_no-1],vpn_config_map["IPSEC_TUNNEL"]["LOCAL_ADDRESS_MASK"]["VALUE"])
        
        # step: set remote address type
        logging.debug("step: set remote address type")
        Select(driver.find_element_by_name(vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDRESS_TYPE"]["MSCIID"][vpn_no-1])).select_by_visible_text(vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDRESS_TYPE"]["VISIBLE_TEXT"][vpn_no-1])
        if  vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDRESS_TYPE"]["VISIBLE_TEXT"][vpn_no-1] == "Single Address": 
            selenium_instance.set_element_by_name(driver,vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDRESS"]["MSCIID"][vpn_no-1],vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDRESS"]["VALUE"])
        elif  vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDRESS_TYPE"]["VISIBLE_TEXT"][vpn_no-1] == "Subnet Address":   
            selenium_instance.set_element_by_name(driver,vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDRESS"]["MSCIID"][vpn_no-1],vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDRESS"]["VALUE"])
            selenium_instance.set_element_by_name(driver,vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDRESS_MASK"]["MSCIID"][vpn_no-1],vpn_config_map["IPSEC_TUNNEL"]["REMOTE_ADDRESS_MASK"]["VALUE"])
 
        # step: set IPSEC encryption/auth/group/SA Life time
        logging.debug("step: set IPSEC encryption/auth/group/SA Life time")
        Select(driver.find_element_by_name(vpn_config_map["IPSEC_TUNNEL"]["IPSEC_ENCRYPT"]["MSCIID"][vpn_no-1])).select_by_visible_text(vpn_config_map["IPSEC_TUNNEL"]["IPSEC_ENCRYPT"]["VISIBLE_TEXT"][vpn_no-1])
        Select(driver.find_element_by_name(vpn_config_map["IPSEC_TUNNEL"]["IPSEC_AUTH"]["MSCIID"][vpn_no-1])).select_by_visible_text(vpn_config_map["IPSEC_TUNNEL"]["IPSEC_AUTH"]["VISIBLE_TEXT"][vpn_no-1])
        Select(driver.find_element_by_name(vpn_config_map["IPSEC_TUNNEL"]["IPSEC_KEY_GROUP"]["MSCIID"][vpn_no-1])).select_by_visible_text(vpn_config_map["IPSEC_TUNNEL"]["IPSEC_KEY_GROUP"]["VISIBLE_TEXT"][vpn_no-1])
        selenium_instance.set_element_by_name(driver,vpn_config_map["IPSEC_TUNNEL"]["IPSEC_SA_TIME"]["MSCIID"][vpn_no-1],vpn_config_map["IPSEC_TUNNEL"]["IPSEC_SA_TIME"]["VALUE"][vpn_no-1])
 
        # Step: apply and reboot DUT
        logging.debug("step: apply and reboot DUT")
        selenium_instance.apply_reboot(driver)
 
        # Step: close the AceManaer web
        driver.close()  
        
        # Step: wait till device ready
        logging.debug("step: wait till device ready" +'\n')  
        time.sleep(vpn_config_map["TESTBED2"]["DUT1"]["REBOOT_TIMEOUT"])
  
  
    def ipsec_vpn_at_verification(self, vpn_no):
        '''VPN IPSEC verification by  AT comamnds'''  
        
        _device   = self.tbd_config_map["DUTS"][0]
        _hostname = self.tbd_config_map[_device]["LAN_IP"] 
        print _hostname        
        telnet_instance = telnet_airlink.TelnetAirlink( hostname=_hostname, port = "2332", username = "user", password = "12345",debug_mode= False)
        telnet_instance.connect()
        #TODO: need to update class TelnetAirlink, __init__ and connect(), need to return error if meet connection fails
        # if telnet_instance not OK:
        # 
        if   vpn_no == 1: 
            ret = telnet_instance.command("at*ipsec1_gateway?")  
        elif vpn_no == 2: 
            ret = telnet_instance.command("at*ipsec2_gateway?")  
        elif vpn_no == 3: 
            ret = telnet_instance.command("at*ipsec3_gateway?")  
        elif vpn_no == 4: 
            ret = telnet_instance.command("at*ipsec4_gateway?")  
        elif vpn_no == 5: 
            ret = telnet_instance.command("at*ipsec5_gateway?")  
        else: 
            logging.info("wrong VPN number")
            return True

        ret_str = ''.join(ret)   
        if ret_str.find(vpn_config_map["IPSEC_TUNNEL"]["VPN_GATEWAY"]["VALUE"]): 
            logging.info(' Found VPN Gateway \n')
        else:
            logging.info(' Cannot find VPN gateway  \n')
            return False
       
        return True
            
    def gre_vpn_at_verification(self, vpn_no):
        '''VPN IPSEC verification by  AT comamnds'''  
        
        return True
 
 
    def ssl_vpn_at_verification(self, vpn_no):
        '''VPN IPSEC verification by  AT comamnds'''  
        
        return True

    def ipsec_vpn_log_verification(self, vpn_no):
        '''VPN IPSEC verification by log file'''  
        
        _device   = self.tbd_config_map["DUTS"][0]
        _hostname = self.tbd_config_map[_device]["LAN_IP"] 
        print _hostname        
        telnet_ins = telnet_airlink.TelnetAirlink( hostname=_hostname, port = "2332", username = "root", password = "v3r1fym3",debug_mode= False, timeout = 3)

        if not (telnet_ins.connect()): 
            logging.debug("telnet disconencted ")
            return False

        ret = telnet_ins.command("cd /mnt/hda1/junxion/log") 
        if not ret:
            logging.debug("cannot go to log folder in device")
            return False           

        ret = telnet_ins.command("cat messages | grep \"ALEOS_VPN: ERROR\"") 
        #ret = telnet_ins.command("cat messages") 
        if not ret:
            logging.debug("cannot find the string ALEOS_VPN in device log file")
            return False  
            
        ret_str = ''.join(ret)
        print ret_str
        if ret_str.find(vpn_config_map["IPSEC_TUNNEL"]["VPN_GATEWAY"]["VALUE"]): 
            logging.info(' Found VPN Gateway \n')
        else:
            logging.info(' Cannot find VPN gateway  \n')
            return False
       
        return True
        
        
    def tc_ipsec_vpn1_ui_setting(self):
        '''test case sets the VPN1 parameters'''
   
        tc_id = "tc_ipsec_vpn1_ui_setting"
        logging.info(tc_id+' : '+'begins'+'\n')
 
        # step: check if devices ready    
        logging.debug("step: check if device ready")
        if not self.testbed_ready() : 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.cleanup()
            self.tc_fail_counter += 1
            return 
        
        #step: disable 5 VPNs
        logging.debug("step: disable 5 VPNs")
        self.set_vpn_type_at(1, 0)
        self.set_vpn_type_at(2, 0)
        self.set_vpn_type_at(3, 0)
        self.set_vpn_type_at(4, 0)
        self.set_vpn_type_at(5, 0)
    
        # set VPN parameters by ACEmanager UI
        self.ipsec_vpn_ui_setting(1)
        
        # step: verify the parameters by AT commands
 
        ret =   self.ipsec_vpn_at_verification(1)
        
        if not ret: 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.tc_fail_counter += 1
            self.cleanup()
            return 
  
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : PASSED\n')
        self.tc_pass_counter += 1
        self.cleanup()


    def tc_ipsec_vpn2_ui_setting(self):
        # test case sets the VPN2 parameters
        
        tc_id = "tc_ipsec_vpn2_ui_setting"
        logging.info(tc_id+' : '+'begins'+'\n')
                 
        # step: check if devices ready    
        logging.debug("step: check if device ready")
        if not self.testbed_ready() : 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.cleanup()
            self.tc_fail_counter += 1
            return 
        
        #step: disable 5 VPNs
        logging.debug("step: disable 5 VPNs")
        self.set_vpn_type_at(1, 0)
        self.set_vpn_type_at(2, 0)
        self.set_vpn_type_at(3, 0)
        self.set_vpn_type_at(4, 0)
        self.set_vpn_type_at(5, 0)
    
        # set VPN parameters by ACEmanager UI
        self.ipsec_vpn_ui_setting(2)
        
        # step: verify the parameters by AT commands
 
        ret =   self.ipsec_vpn_at_verification(2)
        
        if not ret: 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.tc_fail_counter += 1
            self.cleanup()
            return 
  
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : PASSED\n')
        self.tc_pass_counter += 1
        self.cleanup()
        
    
        # test case sets the VPN3 parameters
    def tc_ipsec_vpn3_ui_setting(self):
        
        tc_id = "tc_ipsec_vpn3_ui_setting"
        logging.info(tc_id+' : '+'begins'+'\n')
         
        # step: check if devices ready    
        logging.debug("step: check if device ready")
        if not self.testbed_ready() : 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.cleanup()
            self.tc_fail_counter += 1
            return 
        
        #step: disable 5 VPNs
        logging.debug("step: disable 5 VPNs")
        self.set_vpn_type_at(1, 0)
        self.set_vpn_type_at(2, 0)
        self.set_vpn_type_at(3, 0)
        self.set_vpn_type_at(4, 0)
        self.set_vpn_type_at(5, 0)
    
        # set VPN parameters by ACEmanager UI
        self.ipsec_vpn_ui_setting(3)
        
        # step: verify the parameters by AT commands
 
        ret =   self.ipsec_vpn_at_verification(3)
        
        if not ret: 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.tc_fail_counter += 1
            self.cleanup()
            return 
  
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : PASSED\n')
        self.tc_pass_counter += 1
        self.cleanup()
           
        

        # VPN4 IPSEC setting 
    def tc_ipsec_vpn4_ui_setting(self):
        
        tc_id = "tc_ipsec_vpn4_ui_setting"
        logging.info(tc_id+' : '+'begins'+'\n')
         
        # step: check if devices ready    
        logging.debug("step: check if device ready")
        if not self.testbed_ready() : 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.cleanup()
            self.tc_fail_counter += 1
            return 
        
        #step: disable 5 VPNs
        logging.debug("step: disable 5 VPNs")
        self.set_vpn_type_at(1, 0)
        self.set_vpn_type_at(2, 0)
        self.set_vpn_type_at(3, 0)
        self.set_vpn_type_at(4, 0)
        self.set_vpn_type_at(5, 0)
    
        # set VPN parameters by ACEmanager UI
        self.ipsec_vpn_ui_setting(4)
        
        # step: verify the parameters by AT commands
 
        ret =   self.ipsec_vpn_at_verification(4)
        
        if not ret: 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.tc_fail_counter += 1
            self.cleanup()
            return 
  
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : PASSED\n')
        self.tc_pass_counter += 1
        self.cleanup()
         
    
    
    def tc_ipsec_vpn5_ui_setting(self):
        # VPN5 IPSEC setting by UI

        tc_id = "tc_ipsec_vpn5_ui_setting"
        logging.info(tc_id+' : '+'begins'+'\n')
         
        # step: check if devices ready    
        logging.debug("step: check if device ready")
        if not self.testbed_ready() : 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.cleanup()
            self.tc_fail_counter += 1
            return 
        
        #step: disable 5 VPNs
        logging.debug("step: disable 5 VPNs")
        self.set_vpn_type_at(1, 0)
        self.set_vpn_type_at(2, 0)
        self.set_vpn_type_at(3, 0)
        self.set_vpn_type_at(4, 0)
        self.set_vpn_type_at(5, 0)
    
        # set VPN parameters by ACEmanager UI
        self.ipsec_vpn_ui_setting(5)
        
        # step: verify the parameters by AT commands
 
        ret =   self.ipsec_vpn_at_verification(5)
        
        if not ret: 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.tc_fail_counter += 1
            self.cleanup()
            return 
  
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : PASSED\n')
        self.tc_pass_counter += 1
        self.cleanup()
         
       
    def tc_ipsec_vpn1_at_setting(self):
        '''  VPN1 IPSEC setting by AT command'''
        
        tc_id = "tc_ipsec_vpn1_at_setting"
        logging.info(tc_id+' : '+'begins'+'\n')
 
        # step: check if devices ready    
        logging.debug("step: check if device ready")
        if not self.testbed_ready(): 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.tc_fail_counter += 1
            self.cleanup()
            return 
        
        #step: disable other 4 VPNs
        logging.debug("step: disable other VPNs")
        self.set_vpn_type_at(2, 0)
        self.set_vpn_type_at(3, 0)
        self.set_vpn_type_at(4, 0)
        self.set_vpn_type_at(5, 0)
    
        # set VPN parameters by AT command
        logging.debug("step: set VPN parameters by AT command")

        self.ipsec_vpn_at_setting(1)
        
        # step: verify the parameters by AT commands
        logging.debug("step: verify the parameters by AT commands")

        ret =   self.ipsec_vpn_at_verification(1)       
        if not ret: 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.tc_fail_counter += 1
            self.cleanup()
            return 
  
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : PASSED\n')
        self.tc_pass_counter += 1
        self.cleanup()  
        
        
    def tc_ipsec_vpn2_at_setting(self):
        ''' VPN2 IPSEC setting by AT '''
        
        tc_id = "tc_ipsec_vpn2_at_setting"
        logging.info(tc_id+' : '+'begins'+'\n')
 
        # step: check if devices ready    
        logging.debug("step: check if device ready")
        if not self.testbed_ready(): 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.tc_fail_counter += 1
            self.cleanup()
            return 
        
        #step: disable other 4 VPNs
        logging.debug("step: disable other VPNs")
        self.set_vpn_type_at(1, 0)
        self.set_vpn_type_at(3, 0)
        self.set_vpn_type_at(4, 0)
        self.set_vpn_type_at(5, 0)
    
        # set VPN parameters by AT command
        logging.debug("step: set VPN parameters by AT command")

        self.ipsec_vpn_at_setting(2)
        
        # step: verify the parameters by AT commands
        logging.debug("step: verify the parameters by AT commands")

        ret =   self.ipsec_vpn_at_verification(2)       
        if not ret: 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.tc_fail_counter += 1
            self.cleanup()
            return 
  
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : PASSED\n')
        self.tc_pass_counter += 1
        self.cleanup()  
        
        
    def tc_ipsec_vpn3_at_setting(self):
        ''' VPN3 IPSEC setting by AT '''
        
        tc_id = "tc_ipsec_vpn3_at_setting"
        logging.info(tc_id+' : '+'begins'+'\n')
 
        # step: check if devices ready    
        logging.debug("step: check if device ready")
        if not self.testbed_ready(): 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.tc_fail_counter += 1
            self.cleanup()
            return 
        
        #step: disable other 4 VPNs
        logging.debug("step: disable other VPNs")
        self.set_vpn_type_at(2, 0)
        self.set_vpn_type_at(1, 0)
        self.set_vpn_type_at(4, 0)
        self.set_vpn_type_at(5, 0)
    
        # set VPN parameters by AT command
        logging.debug("step: set VPN parameters by AT command")

        self.ipsec_vpn_at_setting(3)
        
        # step: verify the parameters by AT commands
        logging.debug("step: verify the parameters by AT commands")

        ret =   self.ipsec_vpn_at_verification(3)       
        if not ret: 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.tc_fail_counter += 1
            self.cleanup()
            return 
  
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : PASSED\n')
        self.tc_pass_counter += 1
        self.cleanup()  
        
    def tc_ipsec_vpn4_at_setting(self):
        ''' VPN4 IPSEC setting by AT '''
       
        tc_id = "tc_ipsec_vpn4_at_setting"
        logging.info(tc_id+' : '+'begins'+'\n')
 
        # step: check if devices ready    
        logging.debug("step: check if device ready")
        if not self.testbed_ready(): 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.tc_fail_counter += 1
            self.cleanup()
            return 
        
        #step: disable other 4 VPNs
        logging.debug("step: disable other VPNs")
        self.set_vpn_type_at(2, 0)
        self.set_vpn_type_at(3, 0)
        self.set_vpn_type_at(1, 0)
        self.set_vpn_type_at(5, 0)
    
        # set VPN parameters by AT command
        logging.debug("step: set VPN parameters by AT command")

        self.ipsec_vpn_at_setting(4)
        
        # step: verify the parameters by AT commands
        logging.debug("step: verify the parameters by AT commands")

        ret =   self.ipsec_vpn_at_verification(4)       
        if not ret: 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.tc_fail_counter += 1
            self.cleanup()
            return 
  
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : PASSED\n')
        self.tc_pass_counter += 1
        self.cleanup()  
        

    def tc_ipsec_vpn5_at_setting(self):
        ''' VPN5 IPSEC setting by AT command '''

        tc_id = "tc_ipsec_vpn5_at_setting"
        logging.info(tc_id+' : '+'begins'+'\n')
 
        # step: check if devices ready    
        logging.debug("step: check if device ready")
        if not self.testbed_ready(): 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.tc_fail_counter += 1
            self.cleanup()
            return 
        
        #step: disable other 4 VPNs
        logging.debug("step: disable other VPNs")
        self.set_vpn_type_at(2, 0)
        self.set_vpn_type_at(3, 0)
        self.set_vpn_type_at(4, 0)
        self.set_vpn_type_at(1, 0)
    
        # set VPN parameters by AT command
        logging.debug("step: set VPN parameters by AT command")

        self.ipsec_vpn_at_setting(5)
        
        # step: verify the parameters by AT commands
        logging.debug("step: verify the parameters by AT commands")

        ret =   self.ipsec_vpn_at_verification(5)       
        if not ret: 
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : FAILED\n')
            self.tc_fail_counter += 1
            self.cleanup()
            return 
  
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : PASSED\n')
        self.tc_pass_counter += 1
        self.cleanup()  
        
        
    def tc_ipsec_vpn1_ui_live_router(self):
        '''test case sets the cisco router by Telnet, set VPN1 parameters by AceManager UI'''

        tc_id = "tc_ipsec_vpn_setting010"
        print "tc_ipsec_vpn_setting010 begins"
        #global ipec_vpn_testset
        
        # open the vml config file
        
        yaml.add_constructor("!include", yaml_include)
        
        fo=open('/airlinkautomation/testsuite/GX440/VPN/vpnTestConf.yml','r')
        vpn_config_map = yaml.load(fo)
        fo.close()
        
        print vpn_config_map["IPSEC_TUNNEL"]["VPN_TYPE"]["MSCIID"]
        
        # step: set Cisco router 1811  by telnet        
        
        ppp = cisco_config.CiscoConfig(ip = "172.22.1.254", port = "23", username = "", password = "enable", debug_level = "0", verbose = True)
        #ppp.show_live_router_config()
        ppp.set_access_list() 
        
        # step: set VPN parameters by AceManager UI
        self.ipsec_vpn_ui_setting(1)
        
        # step: verify the parameters by AT commands
 
        _device  = self.tbd_config_map["DUTS"][0]
        hostname = self.tbd_config_map[_device]["LAN_IP"]        
        telnet_instance = telnet_airlink.TelnetAirlink( hostname, port = "2332", username = "user", password = "12345",debug_mode= False)

        ret = telnet_instance.command("at*ipsec1_gateway?")  
        
        ret_str = ''.join(ret)
        if ret_str.find(vpn_config_map["IPSEC_TUNNEL"]["VPN_GATEWAY"]["VALUE"]): 
            logging.debug(tc_id+' : ''PASS'+'\n')
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : ''PASS'+'\n')
        else:
            logging.debug(tc_id+' : ''FAIL'+'\n')
            basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],tc_id+' : ''FAIL'+'\n')
      
      
    def tc_ipsec_vpn2_ui_live_router(self):
        '''test case sets the cisco router by Telnet, set VPN2 parameters by AceManager UI'''

        return

    def tc_ipsec_vpn3_ui_live_router(self):
        '''test case sets the cisco router by Telnet, set VPN3 parameters by AceManager UI'''
        
        return

    def tc_ipsec_vpn4_ui_live_router(self):
        '''test case sets the cisco router by Telnet, set VPN4 parameters by AceManager UI'''
        
        return

    def tc_ipsec_vpn5_ui_live_router(self):
        '''test case sets the cisco router by Telnet, set VPN5 parameters by AceManager UI'''
        
        return

    def tc_ipsec_vpn1_at_live_router(self):
        '''test case sets the cisco router by Telnet, set VPN1 parameters by AT commands '''
        
        return

    def tc_ipsec_vpn2_at_live_router(self):
        '''test case sets the cisco router by Telnet, set VPN2 parameters by AT commands '''
        
        return

    def tc_ipsec_vpn3_at_live_router(self):
        '''test case sets the cisco router by Telnet, set VPN3 parameters by AT commands '''
        
        return

    def tc_ipsec_vpn4_at_live_router(self):
        '''test case sets the cisco router by Telnet, set VPN4 parameters by AT commands '''
        
        return

    def tc_ipsec_vpn5_at_live_router(self):
        '''test case sets the cisco router by Telnet, set VPN5 parameters by AT commands '''
        
        return

        #TODO: SNMP may be here or put into SNMP test suite
    def tc_ipsec_vpn1_snmp_live_router(self):
        '''test case sets the cisco router by Telnet, set VPN1 parameters by AT commands '''
        
        return

    def tc_ipsec_vpn2_snmp_live_router(self):
        '''test case sets the cisco router by Telnet, set VPN2 parameters by AT commands '''
        
        return

    def tc_ipsec_vpn3_snmp_live_router(self):
        '''test case sets the cisco router by Telnet, set VPN3 parameters by AT commands '''
        
        return

    def tc_ipsec_vpn4_snmp_live_router(self):
        '''test case sets the cisco router by Telnet, set VPN4 parameters by AT commands '''
        
        return

    def tc_ipsec_vpn5_snmp_live_router(self):
        '''test case sets the cisco router by Telnet, set VPN5 parameters by AT commands '''
        
        return
        
        
      #############################################
      # VPN GRE mode
      #############################################      
    def tc_gre_vpn1_ui_setting(self, testcase_Id):
        #GRE VPN1
        
        return
      
        # VPN2 GRE setting 
    def tc_gre_vpn2_ui_setting(self, testcase_Id):
        
       return
    
        # VPN3 GRE setting 
    def tc_gre_vpn3_ui_setting(self, testcase_Id):
        
       return

        # VPN4 GRE setting 
    def tc_gre_vpn4_ui_setting(self, testcase_Id):
        
       return
    
            # VPN5 GRE setting 
    def tc_gre_vpn5_ui_setting(self, testcase_Id):
        
       return
    
    def tc_gre_vpn1_at_setting(self, testcase_Id):
        #GRE VPN1
        
        return
      
        # VPN2 GRE setting 
    def tc_gre_vpn2_at_setting(self, testcase_Id):
        
       return
    
        # VPN3 GRE setting 
    def tc_gre_vpn3_at_setting(self, testcase_Id):
        
       return

        # VPN4 GRE setting 
    def tc_gre_vpn4_at_setting(self, testcase_Id):
        
       return
    
            # VPN5 GRE setting 
    def tc_gre_vpn5_at_setting(self, testcase_Id):
        
       return

    def tc_gre_vpn1_ui_live_router(self, testcase_Id):
        #GRE VPN1
        
        return
      
        # VPN2 GRE setting 
    def tc_gre_vpn2_ui_live_router(self, testcase_Id):
        
       return
    
        # VPN3 GRE setting 
    def tc_gre_vpn3_ui_live_router(self, testcase_Id):
        
       return

        # VPN4 GRE setting 
    def tc_gre_vpn4_ui_live_router(self, testcase_Id):
        
       return
    
            # VPN5 GRE setting 
    def tc_gre_vpn5_ui_live_router(self, testcase_Id):
        
       return
    
    def tc_gre_vpn1_at_live_router(self, testcase_Id):
        #GRE VPN1
        
        return
      
        # VPN2 GRE setting 
    def tc_gre_vpn2_at_live_router(self, testcase_Id):
        
       return
    
        # VPN3 GRE setting 
    def tc_gre_vpn3_at_live_router(self, testcase_Id):
        
       return

        # VPN4 GRE setting 
    def tc_gre_vpn4_at_live_router(self, testcase_Id):
        
       return
    
            # VPN5 GRE setting 
    def tc_gre_vpn5_at_live_router(self, testcase_Id):
        
       return

       
       ##############################################
       # use callbox + cisco router 
       ##############################################
       
    def tc_ipsec_vpn1_at_callbox_router(self, testcase_Id):
        #GRE VPN1
        
        return
      
    def tc_ipsec_vpn2_at_callbox_router(self, testcase_Id):
        
       return
    
    def tc_ipsec_vpn3_at_callbox_router(self, testcase_Id):
        
       return

    def tc_ipsec_vpn4_at_callbox_router(self, testcase_Id):
        
       return
    
    def tc_ipsec_vpn5_at_callbox_router(self, testcase_Id):
        
       return
       
    #SSL VPN1
    def tc_ssl_setting_3001(self, testcase_Id):
        
       return
      
        # VPN2 SSL setting 
    def tc_ssl_vpn2_setting_3002(self, testcase_Id):
        
       return
    
        # VPN3 SSL setting 
    def tc_ssl_vpn3_setting_3003(self, testcase_Id):
        
       return

        # VPN4 SSL setting 
    def tc_ssl_vpn4_setting_3004(self, testcase_Id):
        
       return
    
            # VPN5 SSL setting 
    def tc_ssl_vpn5_setting_3005(self, testcase_Id):
        
       return
    


    def finallize(self): 
        '''
        
        '''
        # print test result summary in test report 
        print "\n passed: ", self.tc_pass_counter, " failed:", self.tc_fail_counter
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],"\nPassed : "+ str(self.tc_pass_counter))
        basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"],"\nFailed : "+ str(self.tc_fail_counter))  
              
        return 
    
####################################################
# main  VPN test automation
####################################################

'''
fo_tbd=open('/airlinkautomation/config/testbed2conf.yml','r')
tbd_config_map = yaml.load(fo_tbd)
fo_tbd.close()

current_date_time = datetime.datetime.now()
log_file = self.tbd_config_map["LOG_FILE_FOLDER"]+str(current_date_time)+"_VPN.log"
logging.basicConfig(filename = log_file, level = logging.DEBUG)
'''
myVpn = TestsuiteVpn()

'''
step: put the curren time, FW version into test report at the beginning
current_date_time = datetime.datetime.now()
est_report(self.tbd_config_map["TEST_REPORT_FILE"],"\\n"+str(current_date_time))      
device_name = self.tbd_config_map["DUTS"][0]
hostname = self.tbd_config_map[device_name]["LAN_IP"]   
est_report(self.tbd_config_map["TEST_REPORT_FILE"], "\nALEOS FW : " + self.tbd_config_map[_device]["FW_ALEOS"])
basic_airlink.test_report(self.tbd_config_map["TEST_REPORT_FILE"], "\nRADIO MODULE FW : " + self.tbd_config_map[_device]["FW_RADIO_MODULE"]+'\n')
'''      
VPN_TESTCASES ={  \
           "tc_ipsec_vpn1_ui_setting"  : myVpn.tc_ipsec_vpn1_ui_setting, \
           "tc_ipsec_vpn2_ui_setting"  : myVpn.tc_ipsec_vpn2_ui_setting, \
           "tc_ipsec_vpn3_ui_setting"  : myVpn.tc_ipsec_vpn3_ui_setting, \
           "tc_ipsec_vpn4_ui_setting"  : myVpn.tc_ipsec_vpn4_ui_setting, \
           "tc_ipsec_vpn5_ui_setting"  : myVpn.tc_ipsec_vpn5_ui_setting, \
           "tc_ipsec_vpn1_at_setting"  : myVpn.tc_ipsec_vpn1_at_setting, \
           "tc_ipsec_vpn2_at_setting"  : myVpn.tc_ipsec_vpn2_at_setting, \
           "tc_ipsec_vpn3_at_setting"  : myVpn.tc_ipsec_vpn3_at_setting, \
           "tc_ipsec_vpn4_at_setting"  : myVpn.tc_ipsec_vpn4_at_setting, \
           "tc_ipsec_vpn5_at_setting"  : myVpn.tc_ipsec_vpn5_at_setting,  \
           "tc_ipsec_vpn1_ui_live_router"  : myVpn.tc_ipsec_vpn1_ui_live_router, \
           "tc_ipsec_vpn2_ui_live_router"  : myVpn.tc_ipsec_vpn2_ui_live_router, \
           "tc_ipsec_vpn3_ui_live_router"  : myVpn.tc_ipsec_vpn3_ui_live_router, \
           "tc_ipsec_vpn4_ui_live_router"  : myVpn.tc_ipsec_vpn4_ui_live_router, \
           "tc_ipsec_vpn5_ui_live_router"  : myVpn.tc_ipsec_vpn5_ui_live_router, \
           "tc_ipsec_vpn1_at_live_router"  : myVpn.tc_ipsec_vpn1_at_live_router, \
           "tc_ipsec_vpn2_at_live_router"  : myVpn.tc_ipsec_vpn2_at_live_router, \
           "tc_ipsec_vpn3_at_live_router"  : myVpn.tc_ipsec_vpn3_at_live_router, \
           "tc_ipsec_vpn4_at_live_router"  : myVpn.tc_ipsec_vpn4_at_live_router, \
           "tc_ipsec_vpn5_at_live_router"  : myVpn.tc_ipsec_vpn5_at_live_router, \
           "tc_ipsec_vpn1_at_callbox_router"  : myVpn.tc_ipsec_vpn1_at_callbox_router, \
           "tc_ipsec_vpn2_at_callbox_router"  : myVpn.tc_ipsec_vpn2_at_callbox_router, \
           "tc_ipsec_vpn3_at_callbox_router"  : myVpn.tc_ipsec_vpn3_at_callbox_router, \
           "tc_ipsec_vpn4_at_callbox_router"  : myVpn.tc_ipsec_vpn4_at_callbox_router, \
           "tc_ipsec_vpn5_at_callbox_router"  : myVpn.tc_ipsec_vpn5_at_callbox_router}

# load VPN config and testbed config
yaml.add_constructor("!include", yaml_include)

fo=open('/airlinkautomation/testsuite/GX440/VPN/vpnTestConf.yml','r')
vpn_config_map = yaml.load(fo)
fo.close()

#myVpn.ipsec_vpn_log_verification(1)
#sys.exit(1)

# run all/selective VPN test cases 
for k in range(vpn_config_map["RUN_REPEAT"]):

    #print k
    #print "RUN_ALL_TESTCASES = " 
    #print vpn_config_map["RUN_ALL_TESTCASES"]
    
    if vpn_config_map["RUN_ALL_TESTCASES"]:
        # run all VPN test cases
        for i in range(1,vpn_config_map["ALL_TASECASE_NUMBER"]+1):
            #print i
            logging.debug(vpn_config_map["RUN_ALL_TESTCASES"])
            VPN_TESTCASES[vpn_config_map["VPN_TESTCASES"][i]]()
    else:
        # run selective test cases
        for [a,b] in vpn_config_map["RUN_SELECTIVE_TESTCASES"] :
            #print a,b
            for i in range(a,b+1):
                #print i
                logging.debug(vpn_config_map["VPN_TESTCASES"][i])
                VPN_TESTCASES[vpn_config_map["VPN_TESTCASES"][i]]()

myVpn.finallize()