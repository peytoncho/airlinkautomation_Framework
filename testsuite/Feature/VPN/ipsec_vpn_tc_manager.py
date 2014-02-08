from known_vpn_bugs import KnownVpnBugs
class IpsecVpnTestCaseManager:
    def __init__(self):
        self.CONFIG_OPTIONS = {}
        self.CONFIG_OPTIONS["PRESHARED_KEY"] = ["SierraWireless"]
        self.CONFIG_OPTIONS["NEGOTIATION_MODE"] = ["Main", "Aggressive"]                               
        self.CONFIG_OPTIONS["IKE_ENCRYPTION"] = ["AES-128", "AES-256", "DES", "3DES"]                
        self.CONFIG_OPTIONS["IKE_AUTHENTICATION"] = ["SHA1", "SHA 256", "MD5"]                      
        self.CONFIG_OPTIONS["IKE_DH_GROUP"] = ["DH1", "DH2", "DH5"]                                
        self.CONFIG_OPTIONS["IKE_SA_LIFETIME"] = ["200"]
        self.CONFIG_OPTIONS["IKE_DPD"] = ["Enable", "Disable"]                                    
        self.CONFIG_OPTIONS["IKE_DPD_INTERVAL"] = ["20"]
        self.CONFIG_OPTIONS["LOCAL_ADDRESS_TYPE"] = ["Subnet Address"]
        self.CONFIG_OPTIONS["REMOTE_ADDRESS_TYPE"] = ["Subnet Address"]
        self.CONFIG_OPTIONS["PFS"] = ["Yes", "No"]                                               
        self.CONFIG_OPTIONS["IPSEC_ENCRYPTION"] = ["AES-128", "AES-256", "DES", "3DES", "None"] 
        self.CONFIG_OPTIONS["IPSEC_AUTHENTICATION"] = ["SHA1", "MD5"] # Missing 'None' and 'SHA 256'
        self.CONFIG_OPTIONS["IPSEC_DH_GROUP"] = ["DH1", "DH2", "DH5"] # Missing 'None'             
        self.CONFIG_OPTIONS["IPSEC_SA_LIFETIME"] = ["200"]
        self.CONFIG_OPTIONS["PRESHARED_KEY"] = ["SierraWireless"]

    def num_tcs(self):
        generator = self.tc_generator()
        for tc in generator:
            pass
        return tc["INDEX"] 

    def tc_generator(self):
        # There's two level of generator used here when adding 'None' and 'SHA 256' options to ipsec auth
        # and 'None' to ipsec dh group. At the bottom is original_tc_generator() which creates the original
        # 8640 test cases. We build the top level generator this way so that the first 8640 test cases do not
        # change after adding the new options
        tc_gen = self.original_tc_generator_with_ipsec_dh_none()
        for tc in tc_gen:
            yield tc

        index = tc["INDEX"]

        for added_ipsec_auth in ["SHA 256", "None"]:
            tc_gen = self.original_tc_generator_with_ipsec_dh_none()
            for tc in tc_gen:
                if not tc["IPSEC_AUTHENTICATION"] == "MD5":
                    continue

                index += 1
                tc["IPSEC_AUTHENTICATION"] = added_ipsec_auth
                tc["INDEX"] = index
                yield tc

    def original_tc_generator_with_ipsec_dh_none(self):
        # don't call this generator directly, call tc_generator() to get all the test cases
        # Yield the original 8640 test cases
        original_tc_generator = self.original_tc_generator()
        for tc in original_tc_generator:
            yield tc

        index = tc["INDEX"]

        # add the test cases with ipsec dh 'None'
        original_tc_generator = self.original_tc_generator()
        for tc in original_tc_generator:
            if not tc["IPSEC_DH_GROUP"] == "DH1":
                continue
            index += 1
            tc["INDEX"] = index
            tc["IPSEC_DH_GROUP"] = "None"
            yield tc

    def original_tc_generator(self):
        # don't call this generator directly, call tc_generator() to get all the test cases

        index = 0
        for negotiation_mode in self.CONFIG_OPTIONS["NEGOTIATION_MODE"]:
            for ike_dpd in self.CONFIG_OPTIONS["IKE_DPD"]:
                for ike_encryption in self.CONFIG_OPTIONS["IKE_ENCRYPTION"]:
                    for ike_authentication in self.CONFIG_OPTIONS["IKE_AUTHENTICATION"]:
                        for ike_dh_group in self.CONFIG_OPTIONS["IKE_DH_GROUP"]:
                            for local_address_type in self.CONFIG_OPTIONS["LOCAL_ADDRESS_TYPE"]:
                                for remote_address_type in self.CONFIG_OPTIONS["REMOTE_ADDRESS_TYPE"]:
                                    for pfs in self.CONFIG_OPTIONS["PFS"]:
                                        for ipsec_dh_group in self.CONFIG_OPTIONS["IPSEC_DH_GROUP"]:
                                            for ipsec_encryption in self.CONFIG_OPTIONS["IPSEC_ENCRYPTION"]:
                                                for ipsec_authentication in self.CONFIG_OPTIONS["IPSEC_AUTHENTICATION"]:
                                                    index += 1
                                                    yield {"INDEX": index,
                                                           "PRESHARED_KEY": self.CONFIG_OPTIONS["PRESHARED_KEY"][0],
                                                           "NEGOTIATION_MODE": negotiation_mode,
                                                           "IKE_ENCRYPTION": ike_encryption,
                                                           "IKE_AUTHENTICATION": ike_authentication,
                                                           "IKE_DH_GROUP": ike_dh_group,
                                                           "IKE_SA_LIFETIME": self.CONFIG_OPTIONS["IKE_SA_LIFETIME"][0],
                                                           "IKE_DPD": ike_dpd,
                                                           "IKE_DPD_INTERVAL": self.CONFIG_OPTIONS["IKE_DPD_INTERVAL"][0],
                                                           "LOCAL_ADDRESS_TYPE": local_address_type,
                                                           "REMOTE_ADDRESS_TYPE": remote_address_type,
                                                           "PFS": pfs,
                                                           "IPSEC_ENCRYPTION": ipsec_encryption,
                                                           "IPSEC_AUTHENTICATION": ipsec_authentication,
                                                           "IPSEC_DH_GROUP": ipsec_dh_group,
                                                           "IPSEC_SA_LIFETIME": self.CONFIG_OPTIONS["IPSEC_SA_LIFETIME"][0]}



    def get_tc_list(self):
        generator = self.tc_generator()
        tc_list = []
        for tc in generator:
            tc_list.append(Combo(tc))
        return tc_list

class Combo:
    base_name = "tc_ipsec_vpn_case_"
    def __init__(self, parameters):
        self.parameters = parameters

    @classmethod
    def from_number(cls, number):
        generator = IpsecVpnTestCaseManager().tc_generator()
        for tc in generator:
            if tc["INDEX"] == number:
                return cls(tc)
        return None

    @classmethod
    def get_combo_number_from_name(cls, name):
        for part in name.split('_'):
            try:
                return int(part)
            except ValueError:
                pass
        return -1

    def get_function_name(self):
        function_name = self.__class__.base_name
        function_name += "%d_" %self.parameters["INDEX"]
        for setting in ["IKE_ENCRYPTION", "IKE_AUTHENTICATION", "IKE_DH_GROUP", "IPSEC_ENCRYPTION", "IPSEC_AUTHENTICATION", "PFS", "IPSEC_DH_GROUP"]:
            function_name += "%s_" %self.parameters[setting].replace(" ","").replace("-","").lower()
        return function_name[:-1]

    def __str__(self):
        string = "\n** Ipsec VPN Parameters - number %d **\n" %self.parameters["INDEX"]
        string += "Preshared Key: %s\n" %self.parameters["PRESHARED_KEY"]
        string += "Negotiation Type: %s\n" %self.parameters["NEGOTIATION_MODE"]
        string += "IKE Encryption: %s\n" %self.parameters["IKE_ENCRYPTION"]
        string += "IKE Authentication: %s\n" %self.parameters["IKE_AUTHENTICATION"]
        string += "IKE DH Group: %s\n" %self.parameters["IKE_DH_GROUP"]
        string += "IKE SA Lifetime: %s\n" %self.parameters["IKE_SA_LIFETIME"]
        string += "IKE DPD: %s\n" %self.parameters["IKE_DPD"]
        string += "IKE DPD Interval: %s\n" %self.parameters["IKE_DPD_INTERVAL"]
        string += "Local Address Type: %s\n" %self.parameters["LOCAL_ADDRESS_TYPE"]
        string += "Remote Address Type: %s\n" %self.parameters["REMOTE_ADDRESS_TYPE"]
        string += "Perfect Forward Secrecy: %s\n" %self.parameters["PFS"]
        string += "IPsec Encryption: %s\n" %self.parameters["IPSEC_ENCRYPTION"]
        string += "IPsec Authentication: %s\n" %self.parameters["IPSEC_AUTHENTICATION"]
        string += "IPsec DH Group: %s\n" %self.parameters["IPSEC_DH_GROUP"]
        string += "IPsec SA Lifetime: %s\n\n" %self.parameters["IPSEC_SA_LIFETIME"]
        return string

    def do_we_expect_this_combo_to_pass(self):
        expect_to_pass = True
        reasons = [] # list of string containing reasons why we don't expect this test to pass due to known bugs and issues
        for parameter in KnownVpnBugs.ipsec.keys():
            for option in KnownVpnBugs.ipsec[parameter].keys():
                if self.parameters[parameter] == option:
                    reasons.append(KnownVpnBugs.ipsec[parameter][option])
                    expect_to_pass = False

        return expect_to_pass, reasons
