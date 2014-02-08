#!C:\Python27\python.exe

import os, sys
import StringIO
import types

# Import modules for CGI handling
import cgi, cgitb

import common_funcs

#sys.path.append(os.environ["AIRLINKAUTOMATION_HOME"] + "\\testsuite\Feature\VPN")
sys.path.append("C:\\airlinkautomation\\testsuite\Feature\VPN")
import ipsec_vpn_tc_manager 

class IpsecLauncher():
    def __init__(self):
        self.dropdowns = ["negotiation_mode",
                          "ike_encryption",
                          "ike_authentication",
                          "ike_dh_group",
                          "ike_dpd",
                          "pfs",
                          "ipsec_encryption",
                          "ipsec_authentication",
                          "ipsec_dh_group"]

    def write_html(self):
        form = cgi.FieldStorage()
    
        print "Content-type:text/html\n\n"
        print """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="keywords" content="" />
<meta name="description" content="" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>IPsec VPN Test Case Manager</title>
<link href="/style.css" rel="stylesheet" type="text/css" media="screen" />
</head>
<body>
<div id="wrapper">
	<div id="wrapper-bgbtm">
		<div id="header">
			<div id="logo">
				<h1><a href="#">IPsec VPN Test Case Manager</a></h1>
			</div>
		</div>
		<!-- end #header -->
<!--
		<div id="menu">
			<ul>
				<li class="current_page_item"><a href="#">Homepage</a></li>
				<li><a href="#">Blog</a></li>
				<li><a href="#">Photos</a></li>
				<li><a href="#">About</a></li>
				<li><a href="#">Links</a></li>
				<li><a href="#">Contact</a></li>
			</ul>
		</div>
-->
		<!-- end #menu -->
		<div id="page">
			<div id="page-bgtop">
				<div id="page-bgbtm">
					<div id="content">
						<div class="post">
							<h2 class="title">Test Parameters</h2>
							<div class="entry">
                            <table width="100%%">
                                <tr><td valign="top">
                                    <table width="80%%">
                                        <tr>
                                            <td valign="top">Negotiation Mode</td>
                                            <td valign="top">%s</td>
                                        </tr>
                                        <tr>
                                            <td valign="top">IKE Encryption</td>
                                            <td valign="top">%s</td>
                                        </tr>
                                        <tr>
                                            <td valign="top">IKE Authentication</td>
                                            <td valign="top">%s</td>
                                        </tr>
                                        <tr>
                                            <td valign="top">IKE DH Group</td>
                                            <td valign="top">%s</td>
                                        </tr>
                                        <tr>
                                            <td valign="top">IKE DPD</td>
                                            <td valign="top">%s</td>
                                        </tr>
                                    </table>
                                </td>
                                <td valign="top">
                                    <table width="80%%">
                                        <tr>
                                            <td valign="top">PFS</td>
                                            <td valign="top">%s</td>
                                        </tr>
                                        <tr>
                                            <td valign="top">IPsec Encryption</td>
                                            <td valign="top">%s </td>
                                        </tr>
                                        <tr>
                                            <td valign="top">IPsec Authentication</td>
                                            <td valign="top">%s</td>
                                        </tr>
                                        <tr>
                                            <td valign="top">IPsec DH Group</td>
                                            <td valign="top">%s</td>
                                        </tr>
                                    </table>
                                </td></tr>
                            </table>
                            """ %(self.list_to_string_with_line_breaks(common_funcs.get_cgi_multiple_select(form, self.dropdowns[0])),
                                  self.list_to_string_with_line_breaks(common_funcs.get_cgi_multiple_select(form, self.dropdowns[1])),
                                  self.list_to_string_with_line_breaks(common_funcs.get_cgi_multiple_select(form, self.dropdowns[2])),
                                  self.list_to_string_with_line_breaks(common_funcs.get_cgi_multiple_select(form, self.dropdowns[3])),
                                  self.list_to_string_with_line_breaks(common_funcs.get_cgi_multiple_select(form, self.dropdowns[4])),
                                  self.list_to_string_with_line_breaks(common_funcs.get_cgi_multiple_select(form, self.dropdowns[5])),
                                  self.list_to_string_with_line_breaks(common_funcs.get_cgi_multiple_select(form, self.dropdowns[6])),
                                  self.list_to_string_with_line_breaks(common_funcs.get_cgi_multiple_select(form, self.dropdowns[7])),
                                  self.list_to_string_with_line_breaks(common_funcs.get_cgi_multiple_select(form, self.dropdowns[8])))

        #==========================================
        # Select tests to run from menu
        #==========================================
        tc_manager = ipsec_vpn_tc_manager.IpsecVpnTestCaseManager()

        # make a dictionary to hold the settings to exclude
        excluded_settings = {}
        for dropdown in self.dropdowns:
            excluded_settings[dropdown] = common_funcs.get_cgi_multiple_select(form, "fl_" + dropdown) # the full list of available settings 
            selected_list = common_funcs.get_cgi_multiple_select(form, dropdown) # the list selected by the user
            for item in selected_list:
                while True:
                    try:
                        excluded_settings[dropdown].remove(item)
                    except ValueError:
                        break

        tc_generator = tc_manager.tc_generator()

        valid_tc_list = []

        manually_excluded_tcs = common_funcs.extract_number_list(form.getvalue("excluded_tc"))["RESULT"] # the list of test cases that have been manually excluded

        for tc in tc_generator:

            # skip the manually excluded tc's
            if tc["INDEX"] in manually_excluded_tcs:
                continue

            # check if the test case has an excluded setting
            skip = False
            for config in self.dropdowns:
                if tc[config.upper()] in excluded_settings[config]:
                    skip = True
                    break
            if not skip:
                valid_tc_list.append(tc["INDEX"])

        tc = common_funcs.pack_tc_list(valid_tc_list)

        temp = ""
        for option in tc.replace("[","").replace("]","").split(","):
            temp += "<option>%s</option>\n                                        " %option

        if manually_excluded_tcs:
            print "Manually excluded test cases: %s<br><br>" %common_funcs.pack_tc_list(sorted(manually_excluded_tcs))
        print r"""<div align="left">Available Test Cases: %s<br><br></div>""" %tc

        print """

                            <table width"100%%"><tr>
                                <td width="25%%">
                                    <h3>Choose Test To Run</h3>
                                    <table><tr>
                                        <form action=\"/cgi-bin/submit_test_to_jenkins.py\" method=\"post\">
                                        <input type="hidden" name="action" value="FromList">
                                        <td>
                                            <select name="tc_multiple_select" multiple="multiple" size="10">
                                                %s
                                        </td>
                                        <td valign="top" align="right" height="100">
                                            <table><tr><td valign="top">
                                                Report Size:<br>
                                                <select name="report_size">
                                                    <option>1</option>
                                                    <option>10</option>
                                                    <option>25</option>
                                                    <option selected="selected">50</option>
                                                    <option>100</option>
                                            </td></tr>
                                            <tr><td valign="bottom" align="right" style="height:120";>
                                            <input type="submit" value="Get Batch File">
                                            </td></tr></table>
                                        </td>
                                        </form>
                                    </tr></table>
                                </td>
                                <td width="5%%"></td>
                                <td width="25%%">
                                    <h3>Randomly Select</h3>
                                    <table><tr>
                                        <form action=\"/cgi-bin/submit_test_to_jenkins.py\" method=\"post\">
                                        <input type="hidden" name="action" value="Random">
                                        <input type="hidden" name="tc" value="%s">
                                        <td valign="top" align="right" height="100">
                                            <table><tr><td valign="top">
                                                How many?<br>
                                                <input type="number" name="num_tcs" style="width:50px;" min="1" max="9999" value="50">
                                                </td>
                                                <td valign="top">
                                                Report Size:<br>
                                                <select name="report_size">
                                                    <option>1</option>
                                                    <option>10</option>
                                                    <option>25</option>
                                                    <option selected="selected">50</option>
                                                    <option>100</option>
                                            </td></tr>
                                            <tr><td valign="bottom" align="right" style="height:120";>
                                            <input type="submit" value="Get Batch File">
                                            </td></tr></table>
                                        </td>
                                        </form>
                                    </tr></table>
                                </td>
                                <td width="5%%"></td>
                                <td width="25%%">
                                    <h3>Manual Selection</h3>
                                    <table><tr>
                                        <form action=\"/cgi-bin/submit_test_to_jenkins.py\" method=\"post\">
                                        <input type="hidden" name="action" value="Manual">
                                        <td valign="top" align="right" height="100">
                                            <table><tr><td valign="top">
                                                Test Cases:<br>
                                                <input type="text" name="tc" style="width:100px;">
                                                </td>
                                                <td valign="top">
                                                Report Size:<br>
                                                <select name="report_size">
                                                    <option>1</option>
                                                    <option>10</option>
                                                    <option>25</option>
                                                    <option selected="selected">50</option>
                                                    <option>100</option>
                                            </td></tr>
                                            <tr><td valign="bottom" align="right" style="height:120";>
                                            <input type="submit" value="Get Batch File">
                                            </td></tr></table>
                                        </td>
                                        </form>
                                    </tr></table>
                                </td>
                            </tr></table>
""" %(temp, tc)

        print """
							</div>
						</div>
					</div>
					<!-- end #content -->
					<div style="clear: both;">&nbsp;</div>
				</div>
			</div>
		</div>
		<!-- end #page -->
	</div>
</div>
<h1>No errors :D</h1>
</body>
</html>
"""

    def list_to_string_with_line_breaks(self, mList, num_breaks = 1):
        ret = "" 
        for item in mList:
            ret += item + num_breaks*"<br>"
        return ret
    
if __name__ == "__main__":
    html = IpsecLauncher()
    html.write_html()
