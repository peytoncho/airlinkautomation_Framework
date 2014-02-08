import unittest
import basic_airlink
tbd_config_map = basic_airlink.get_tbd_config_data()

import sys, os
sys.path.append(os.environ['AIRLINKAUTOMATION_HOME'] + "/testsuite/Feature/VPN/auto_generated")
import vpn_ipsec_default_tc_wrappers # Contains wrappers from an auto-generated file

class VpnTcWrappers(vpn_ipsec_default_tc_wrappers.VpnIpsecDefaultTcWrappers):

    # GRE test case
    @unittest.skipIf(tbd_config_map["VPN"]["CISCO_TYPE"] == "ASA", "Cisco ASA does not support GRE tunnels")
    @unittest.skipIf(tbd_config_map["VPN"]["AIRLINK_SIM_STATIC"] == "NO", "GRE tunnels require a static IP address")
    def tc_gre_vpn_default_case(self):
        self.tc_vpn_default()

    # IPsec test cases that tests different subnet mask lengths for the cisco subnet
    def tc_ipsec_vpn_cisco_subnet_8_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_9_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_10_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_11_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_12_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_13_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_14_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_15_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_16_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_17_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_18_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_19_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_20_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_21_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_22_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_23_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_24_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_25_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_26_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_27_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_28_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_29_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_30_bit_netmask(self):
        self.tc_vpn_default()
    def tc_ipsec_vpn_cisco_subnet_31_bit_netmask(self):
        self.tc_vpn_default()

    # Test cases that verifies that the IPsec tunnel does not come up when there is a mismatch in configuration
    def tc_ipsec_vpn_ike_encryption_mismatch(self):
        self.tc_ipsec_vpn_mismatch("IKE_ENCRYPTION")
    def tc_ipsec_vpn_ike_authentication_mismatch(self):
        self.tc_ipsec_vpn_mismatch("IKE_AUTHENTICATION")
    def tc_ipsec_vpn_ike_dh_group_mismatch(self):
        self.tc_ipsec_vpn_mismatch("IKE_DH_GROUP")
    def tc_ipsec_vpn_ipsec_encryption_mismatch(self):
        self.tc_ipsec_vpn_mismatch("IPSEC_ENCRYPTION")
    def tc_ipsec_vpn_ipsec_authentication_mismatch(self):
        self.tc_ipsec_vpn_mismatch("IPSEC_AUTHENTICATION")
    def tc_ipsec_vpn_ipsec_dh_group_mismatch(self):
        self.tc_ipsec_vpn_mismatch("IPSEC_DH_GROUP")
