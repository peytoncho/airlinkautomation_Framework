import sys
sys.dont_write_bytecode = True

class KnownVpnBugs:
    """This class is used to keep track of the known bugs in VPN. 
    Code in the test suite will reference this class to skip test
    cases that have known issues and will fail.
    """

    ipsec = {} # Each type of VPN will have a dictionary whose keys are the parameters that appear in acemanager. Each key maps to a dictionary of options that will cause the script to fail due to a bug/issue.  

    # IMPORTANT NOTE: when filling in the 'reason' fields, do NOT use double quotes " in your string
    # you must run gen_default_vpn_files.py after editing this file to update other files.

    ipsec["IKE_AUTHENTICATION"] = {"SHA 256":"ALLX-3257"}
    #                               ^- option       ^- reason why it fails
    ipsec["IPSEC_AUTHENTICATION"] = {"SHA 256":"ALLX-3257", 
                                     "None":"ALLX-4894"}

    ipsec["IPSEC_DH_GROUP"] = {"None":"ALLX-2531"}
    ipsec["PFS"] = {"No":"ALLX-2531"} # This setting actually doesn't do anything. Combined with "None" not working with IPsec DH Group, you can't turn off PFS ;)

    gre = {} # no known bugs :)
    ssl = {} # no known bugs :)
