#!C:\Python27\python.exe

import cgi, cgitb
import string
import random
import types
import itertools, operator
import common_funcs

class SubmitTestToJenkins():
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
                            <h2 class="title">Batch Commands</h2>
                            <div class="entry">
"""
        batch_commands = ""
        tc_list = []
        if form.getvalue("action") == "FromList":
            for selected_range in common_funcs.get_cgi_multiple_select(form, "tc_multiple_select"):
                tc_list += range(int(selected_range.split("-")[0]), int(selected_range.split("-")[-1]) + 1)

        elif form.getvalue("action") == "Random":
            num_tcs = int(form.getvalue("num_tcs"))
            tc = common_funcs.extract_number_list(form.getvalue("tc"))["RESULT"]
            while num_tcs:
                try:
                    tc_list += random.sample(tc, num_tcs)
                    break
                except ValueError:
                    random.shuffle(tc)
                    tc_list += tc
                    num_tcs = num_tcs - len(tc)
        elif form.getvalue("action") == "Manual":
            tc_list += common_funcs.extract_number_list(form.getvalue("tc"))["RESULT"]
            

        dispenser = self.tc_dispenser(tc_list, int(form.getvalue("report_size")))
        for i in dispenser:
            batch_commands += "<PREFIX> %s\n" %common_funcs.pack_tc_list(i)
        batch_commands = batch_commands.replace("<PREFIX>", "C:\\airlinkautomation\\testsuite\Feature\VPN\\testsuite_vpn_ipsec_default_launcher.py -n")
        print "<textarea rows=\"%d\">%s</textarea>" %(20, batch_commands)
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

    def tc_dispenser(self, tc_list, n):
        index = 0
        while True:
            try:
                tc_list[index+n]
                yield tc_list[index:index+n]
                index += n
            except IndexError:
                yield tc_list[index:]
                break


if __name__ == "__main__":
    html = SubmitTestToJenkins()
    html.write_html()
