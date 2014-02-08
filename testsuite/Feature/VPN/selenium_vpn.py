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
from vpn_airlink import VpnAirlink as VpnUi
import basic_airlink

class VpnSeleniumProcess(selenium_process.SeleniumProcess):
    CONFIG_VPN = "CONFIG_VPN"
    CONFIG_GRE_VPN = "CONFIG_GRE_VPN"
    VERIFY_VPN = "VERIFY_VPN"
    VERIFY_GRE_VPN = "VERIFY_GRE_VPN"
    VERIFY_TUNNEL = "VERIFY_TUNNEL"

    DISABLE_ALL_TUNNELS = "DISABLE_ALL_TUNNELS"
    VERIFY_ALL_TUNNELS_DISABLED = "VERIFY_ALL_TUNNELS_DISABLED"

    def __init__(self, test_config, task, timeout, conn, proxy_ip = None):
        selenium_process.SeleniumProcess.__init__(self, test_config, task, timeout, conn, proxy_ip)

        # add tasks
        self.available_tasks[self.CONFIG_VPN] = self.config_vpn
        self.available_tasks[self.VERIFY_VPN] = self.verify_vpn
        self.available_tasks[self.VERIFY_GRE_VPN] = self.verify_gre_vpn
        self.available_tasks[self.VERIFY_TUNNEL] = self.verify_tunnel
        self.available_tasks[self.CONFIG_GRE_VPN] = self.config_gre_vpn
        self.available_tasks[self.DISABLE_ALL_TUNNELS] = self.disable_all_tunnels
        self.available_tasks[self.VERIFY_ALL_TUNNELS_DISABLED] = self.verify_all_tunnels_disabled

        self.f = self.available_tasks[self.task]

    def login(self):
        if self.proxy_ip is not None:
            self.proxy = proxy_airlink.ProxyAirlink(self.proxy_ip)
            self.proxy_conn = self.proxy.connect()
            self.local_se_ins = VpnUi() #selenium_utilities.SeleniumAcemanager()
            self.se_ins = self.proxy.deliver(self.local_se_ins)
        else:
            self.se_ins = VpnUi() #selenium_utilities.SeleniumAcemanager()
        
        self.driver = self.se_ins.login(self.test_config["ACEMANAGER_URL"], self.test_config["ACEMANAGER_USER"], self.test_config["ACEMANAGER_PASSWORD"])
        time.sleep(2)

    def config_vpn(self):
        if self.test_config["CISCO_TYPE"] == "ASA" and self.test_config["NEGOTIATION_MODE"] == "Aggressive":
            # Aggressive mode on the ASA requires FQDN instead of IP
            my_identity_type = "FQDN"
        else:
            my_identity_type = "IP"

        ret = self.se_ins.config_ipsec_vpn(driver = self.driver,
                vpn_no = self.test_config["VPN_NO"],
                gateway_address = self.test_config["GATEWAY_ADDRESS"],
                preshared_key = self.test_config["PRESHARED_KEY"],
                my_identity_type = my_identity_type,
                my_fqdn = "AirlinkFQDN", # this string must match what is configured on the ASA with the line 'tunnel-group AirlinkFQDN type ipsec-l2l'
                peer_identity_type = "IP",
                negotiation_mode = self.test_config["NEGOTIATION_MODE"],
                ike_encryption = self.test_config["IKE_ENCRYPTION"],
                ike_authentication = self.test_config["IKE_AUTHENTICATION"],
                ike_key_group = self.test_config["IKE_DH_GROUP"],
                ike_sa_lifetime = self.test_config["IKE_SA_LIFETIME"],
                ike_dpd = self.test_config["IKE_DPD"],
                local_address_type = self.test_config["LOCAL_ADDRESS_TYPE"],
                local_address = self.test_config["LOCAL_ADDRESS"],
                local_address_netmask = self.test_config["LOCAL_ADDRESS_MASK"],
                remote_address = self.test_config["REMOTE_ADDRESS"],
                remote_address_netmask = self.test_config["REMOTE_ADDRESS_MASK"],
                remote_address_type = self.test_config["REMOTE_ADDRESS_TYPE"],
                pfs = self.test_config["PFS"],
                ipsec_encryption = self.test_config["IPSEC_ENCRYPTION"],
                ipsec_authentication = self.test_config["IPSEC_AUTHENTICATION"],
                ipsec_key_group = self.test_config["IPSEC_DH_GROUP"],
                ipsec_sa_lifetime = self.test_config["IPSEC_SA_LIFETIME"])

        return ret 

    def verify_vpn(self):
        if self.test_config["CISCO_TYPE"] == "ASA" and self.test_config["NEGOTIATION_MODE"] == "Aggressive":
            # Aggressive mode on the ASA requires FQDN instead of IP
            my_identity_type = "FQDN"
        else:
            my_identity_type = "IP"

        ret = self.se_ins.verify_ipsec_vpn(driver = self.driver,
                vpn_no = self.test_config["VPN_NO"],
                gateway_address = self.test_config["GATEWAY_ADDRESS"],
                preshared_key = self.test_config["PRESHARED_KEY"],
                my_identity_type = my_identity_type,
                my_fqdn = "AirlinkFQDN", # this string must match what is configured on the ASA with the line 'tunnel-group AirlinkFQDN type ipsec-l2l'
                peer_identity_type = "IP",
                negotiation_mode = self.test_config["NEGOTIATION_MODE"],
                ike_encryption = self.test_config["IKE_ENCRYPTION"],
                ike_authentication = self.test_config["IKE_AUTHENTICATION"],
                ike_key_group = self.test_config["IKE_DH_GROUP"],
                ike_sa_lifetime = self.test_config["IKE_SA_LIFETIME"],
                ike_dpd = self.test_config["IKE_DPD"],
                local_address_type = self.test_config["LOCAL_ADDRESS_TYPE"],
                local_address = self.test_config["LOCAL_ADDRESS"],
                local_address_netmask = self.test_config["LOCAL_ADDRESS_MASK"],
                remote_address = self.test_config["REMOTE_ADDRESS"],
                remote_address_netmask = self.test_config["REMOTE_ADDRESS_MASK"],
                remote_address_type = self.test_config["REMOTE_ADDRESS_TYPE"],
                pfs = self.test_config["PFS"],
                ipsec_encryption = self.test_config["IPSEC_ENCRYPTION"],
                ipsec_authentication = self.test_config["IPSEC_AUTHENTICATION"],
                ipsec_key_group = self.test_config["IPSEC_DH_GROUP"],
                ipsec_sa_lifetime = self.test_config["IPSEC_SA_LIFETIME"])

        return ret 

    def verify_tunnel(self):
        return self.se_ins.verify_vpn_status(self.driver, self.test_config["VPN_NO"], "Connected")

    def config_gre_vpn(self):
        return self.se_ins.config_gre_vpn(self.driver, self.test_config["VPN_NO"], self.test_config["GATEWAY_ADDRESS"], 
                remote_address_type = self.test_config["REMOTE_ADDRESS_TYPE"], 
                remote_address = self.test_config["REMOTE_ADDRESS"],
                remote_address_netmask = self.test_config["REMOTE_ADDRESS_MASK"],
                gre_ttl = "255")

    def verify_gre_vpn(self):
        return self.se_ins.verify_gre_vpn(self.driver, self.test_config["VPN_NO"], self.test_config["GATEWAY_ADDRESS"], 
                remote_address_type = self.test_config["REMOTE_ADDRESS_TYPE"], 
                remote_address = self.test_config["REMOTE_ADDRESS"],
                remote_address_netmask = self.test_config["REMOTE_ADDRESS_MASK"],
                gre_ttl = "255")

    def disable_all_tunnels(self):
        for tunnel in ["1","2","3","4","5"]:
            if not self.se_ins.disable_tunnel(self.driver, tunnel):
                return False
        return True 

    def verify_all_tunnels_disabled(self):
        for tunnel in ["1","2","3","4","5"]:
            if not self.se_ins.verify_disabled_tunnel(self.driver, tunnel):
                return False
        return True 
