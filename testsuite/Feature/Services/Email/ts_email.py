import datetime
import logging
import os
import sys
import time
import unittest
import connectivity
import basic_airlink as ba
import selenium_utilities
import telnet_airlink
import services_airlink
import proxy_airlink
import verify_email

test_area = "Services"
test_sub_area="EMAIL"
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_FRAMEWORK'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")

ba.append_sys_path()
tbd_config_map, email_config_map = ba.get_config_data(test_area,test_sub_area)

class TsEmail(unittest.TestCase):
    def setUp(self):
        #Pick info from config file
        self.device = tbd_config_map["DUTS"][0]
        connectivity_ins = connectivity.Connectivity(device_name = self.device)
        self.url = connectivity_ins.get_url()
        ip_addr = connectivity_ins.address()
        self.username = tbd_config_map[self.device]["USERNAME"]
        self.password = tbd_config_map[self.device]["PASSWORD"]
        self.proxy_ip = "208.81.123.51"
        self.proxy = proxy_airlink.ProxyAirlink(ip = self.proxy_ip)
#        self.conn = self.proxy.connect()
        
#        conn_ins = connectivity_ins.connection_types()
        #Ping device
        ret = os.system('ping '+ip_addr)
        if ret == 0:
            ba.cslog("DUT ready", "GREEN") 
        else:
            ba.cslog("DUT not ready", "RED")
            self.fail("DUT not ready")

        #init and login
        self.services_ins = services_airlink.EmailAirlink()
        self.driver = self.services_ins.login(self.url, self.username, self.password)

    
    def tearDown(self):
        self.driver.close()
#        self.conn.close()
    
    def tc_email_1(self):
        ba.cslog("This is test case 1", "RED")
        time.sleep(5)
        smtp_server_ip = self.services_ins.get_smtp_ip_address(self.driver)
        smtp_from_email = self.services_ins.get_smtp_from_email_address(self.driver)
        smtp_username = self.services_ins.get_smtp_username(self.driver)
        smtp_password = self.services_ins.get_smtp_password(self.driver)
        smtp_message_subject = self.services_ins.get_smtp_message_subject(self.driver)
        smtp_quick_test_dest = self.services_ins.get_smtp_quick_test_destination(self.driver)
        ba.cslog("Click quick test button", "BLUE")
        #self.services_ins.click_smtp_quick_test(self.driver)
        
        ba.cslog(smtp_server_ip)
        ba.cslog(smtp_from_email)
        ba.cslog(smtp_username)
        ba.cslog(smtp_password)
        ba.cslog(smtp_message_subject)
#        ba.cslog(smtp_quick_test_dest)
#        ba.cslog(smtp_test_status)
                
    def tc_email_2(self):
        ba.cslog("This is test case 2", "RED")
        test_dest = "airlinksierra@gmail.com"
        self.services_ins.set_smtp_quick_test_destination(self.driver, test_dest)
        self.services_ins.apply(self.driver)
        self.services_ins.click_smtp_quick_test(self.driver)
        time.sleep(10)
        self.services_ins.refresh(self.driver)
        smtp_test_status = self.services_ins.get_smtp_test_status(self.driver)        
        ba.cslog(smtp_test_status)
        

    def tc_email_3(self):
        ba.cslog("This is test case 3", "RED")
        ret = os.system('ping '+self.proxy_ip)
        if ret == 0:
            ba.cslog("DUT ready", "GREEN") 
        else:
            ba.cslog("DUT not ready", "RED")
            self.fail("DUT not ready")
        
        host_se_ins = verify_email.VerifyEmail()
        remote_se_ins = self.proxy.deliver(host_se_ins)
        driver = remote_se_ins.access_email_client()
        txt = remote_se_ins.verify_email_subject(driver,"This")
        ba.cslog(txt, "RED")
        
        
    def tc_email_4(self):
        ba.cslog("This is test case 4", "RED")
    
    def tc_email_5(self):
        ba.cslog("This is test case 5", "RED")
        
    def tc_email_6(self):
        ba.cslog("This is test case 6", "RED")