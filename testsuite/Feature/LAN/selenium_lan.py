import time
import os, sys

sys.path.append(os.environ['AIRLINKAUTOMATION_HOME'] + "/lib/common")
sys.path.append(os.environ['AIRLINKAUTOMATION_HOME'] + "/lib/common/UI")
sys.path.append(os.environ['AIRLINKAUTOMATION_HOME'] + "/lib/site-packages")

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import yaml
import basic_airlink
import selenium_process
import proxy_airlink
from lan_airlink import LanAirlink as LanUi
import basic_airlink

class LanSeleniumProcess(selenium_process.SeleniumProcess):
    CONFIG_VRRP = "CONFIG_VRRP"
    VERIFY_VRRP_CONFIGS = "VERIFY_VRRP_CONFIGS"

    def __init__(self, test_config, task, timeout, conn, proxy_ip = None):
        selenium_process.SeleniumProcess.__init__(self, test_config, task, timeout, conn, proxy_ip)

        # add tasks
        self.available_tasks[self.CONFIG_VRRP] = self.config_vrrp
        self.available_tasks[self.VERIFY_VRRP_CONFIGS] = self.verify_vrrp_configs

        self.f = self.available_tasks[self.task]

    def login(self):
        if self.proxy_ip is not None:
            self.proxy = proxy_airlink.ProxyAirlink(self.proxy_ip)
            self.proxy_conn = self.proxy.connect()
            self.local_se_ins = LanUi() #selenium_utilities.SeleniumAcemanager()
            self.se_ins = self.proxy.deliver(self.local_se_ins)
        else:
            self.se_ins = LanUi() #selenium_utilities.SeleniumAcemanager()
        
        self.driver = self.se_ins.login(self.test_config["ACEMANAGER_URL"], self.test_config["ACEMANAGER_USER"], self.test_config["ACEMANAGER_PASSWORD"])
        time.sleep(2)

    def config_vrrp(self):
        # Go to LAN/VRRP page
        self.se_ins.lan_vrrp_page(self.driver)

        # Configure Stuff
        configured = True
        configured = configured and self.se_ins.set_vrrp_mode(self.driver, self.test_config["VRRP_ENABLE"])
        configured = configured and self.se_ins.set_vrrp_ethernet_group_id(self.driver, self.test_config["GROUP_ID"])
        configured = configured and self.se_ins.set_vrrp_ethernet_priority(self.driver, self.test_config["AIRLINK_PRIORITY"])
        configured = configured and self.se_ins.set_vrrp_ethernet_virtual_ip(self.driver, self.test_config["VIRTUAL_DEFAULT_GATEWAY"])
        configured = configured and self.se_ins.set_vrrp_ethernet_interval(self.driver, self.test_config["INTERVAL"])
        time.sleep(1)
        self.se_ins.apply(self.driver)
        return configured 

    def verify_vrrp_configs(self):
        # Go to LAN/VRRP page
        self.se_ins.lan_vrrp_page(self.driver)

        # Verify Settings 
        verified = True
        verified = verified and self.se_ins.verify_vrrp_mode_enabled(self.driver, self.test_config["VRRP_ENABLE"])
        verified = verified and self.se_ins.verify_vrrp_ethernet_group_id(self.driver, self.test_config["GROUP_ID"])
        verified = verified and self.se_ins.verify_vrrp_ethernet_priority(self.driver, self.test_config["AIRLINK_PRIORITY"])
        verified = verified and self.se_ins.verify_vrrp_ethernet_virtual_ip(self.driver, self.test_config["VIRTUAL_DEFAULT_GATEWAY"])
        verified = verified and self.se_ins.verify_vrrp_ethernet_interval(self.driver, self.test_config["INTERVAL"])
        return verified 
