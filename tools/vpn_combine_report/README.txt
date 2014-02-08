parser.py is used to combine different HTML reports produced by the framework into a larger report for easier viewing. It will parse the original reports and filter out any test cases with name that does not start with "tc_ipsec_vpn_case_" which indicates that it is part of the main ipsec vpn test cases. 

How to combine individual reports:
1. copy html reports to the 'source_files' directly
2. run parser.py
3. generated compiled report is named ".VPN_TESTLOG.html"