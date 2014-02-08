#!C:\Python27\python.exe

import cgi, cgitb
import string
import random
import types
import itertools, operator
import common_funcs
import sys

sys.path.append("C:\\airlinkautomation\\testsuite\Feature\VPN")
import ipsec_vpn_tc_manager

class RetrieveParameters():
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
                            <h2 class="title">Parameters For Each Test Case</h2>
                            <div class="entry">
"""
        tc_list = common_funcs.extract_number_list(form.getvalue("show_parameters"))
        if tc_list["NONE_INPUT"]:
            print "No input received!"
        elif tc_list["ERROR"]:
            print "Input not correctly formatted. Example: \'[1-10,13-13,15-20]\'"
        else:
            tc_manager = ipsec_vpn_tc_manager.IpsecVpnTestCaseManager()
            tc_generator = tc_manager.tc_generator()
            for tc in tc_generator:
                if tc["INDEX"] in tc_list["RESULT"]:
                    print str(ipsec_vpn_tc_manager.Combo(tc)).replace("\n", "<br>")

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
No errors :D
</body>
</html>
"""


if __name__ == "__main__":
    html = RetrieveParameters()
    html.write_html()
