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
    
        error_messages = ""
        tc_list = common_funcs.extract_number_list(form.getvalue("analyze_parameters"))
        if tc_list["NONE_INPUT"]:
            error_messages += "No input received!\n"
        elif tc_list["ERROR"]:
            error_messages += "Input not correctly formatted. Example: \'[1-10,13-13,15-20]\'\n"
        else:
    
            tc_manager = ipsec_vpn_tc_manager.IpsecVpnTestCaseManager()
            tc_generator = tc_manager.tc_generator()

            report = {}
            report["NEGOTIATION_MODE"] = {"Main":0,"Aggressive":0}
            report["IPSEC_ENCRYPTION"] = {"None":0,"AES-128":0,"AES-256":0,"DES":0,"3DES":0}
            report["IPSEC_AUTHENTICATION"] = {"None":0,"MD5":0,"SHA1":0,"SHA 256":0}
            report["IPSEC_DH_GROUP"] = {"DH1":0,"DH2":0,"DH5":0}
            report["IKE_ENCRYPTION"] = {"AES-128":0,"AES-256":0,"DES":0,"3DES":0}
            report["IKE_AUTHENTICATION"] = {"MD5":0,"SHA1":0,"SHA 256":0}
            report["IKE_DH_GROUP"] = {"DH1":0,"DH2":0,"DH5":0}
            report["IKE_DPD"] = {"Enable":0,"Disable":0}
            report["PFS"] = {"Yes":0,"No":0}

            for tc_config in tc_generator:
                if tc_config["INDEX"] not in tc_list["RESULT"]:
                    continue

                report["NEGOTIATION_MODE"][tc_config["NEGOTIATION_MODE"]] += 1
                report["IPSEC_ENCRYPTION"][tc_config["IPSEC_ENCRYPTION"]] += 1 
                report["IPSEC_AUTHENTICATION"][tc_config["IPSEC_AUTHENTICATION"]] += 1
                report["IPSEC_DH_GROUP"][tc_config["IPSEC_DH_GROUP"]] += 1
                report["IKE_ENCRYPTION"][tc_config["IKE_ENCRYPTION"]] += 1
                report["IKE_AUTHENTICATION"][tc_config["IKE_AUTHENTICATION"]] += 1
                report["IKE_DH_GROUP"][tc_config["IKE_DH_GROUP"]] += 1
                report["IKE_DPD"][tc_config["IKE_DPD"]] += 1
                report["PFS"][tc_config["PFS"]] += 1

            javascript = ""

            showme = ""
            for key in report:
                rows = ""
                for option in report[key]:
                    showme += "%s<br><br>" %option
                    rows += r"""['%s', %d],""" %(option, report[key][option])
                showme += "******************<br>"
                javascript += r"""
        // Callback that creates and populates a data table,
        // instantiates the pie chart, passes in the data and
        // draws it.
        function draw%sChart() {

            // Create the data table.
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Option');
            data.addColumn('number', 'Count');
            data.addRows([%s]);

            // Set chart options
            var options = {'title':'%s',
                           'pieHole':0.4,
                           'width':400,
                           'height':300,
                           'fontColor':{fill:'white'},
                           'backgroundColor':{fill:'transparent'},
                           'legend':{textStyle:{color:'white'}},
                           'titleTextStyle':{color:'white'},
                           'sliceVisibilityThreshold':0,
                           };

            // Instantiate and draw our chart, passing in some options.
            var chart = new google.visualization.PieChart(document.getElementById('%s_chart'));
            chart.draw(data, options);
        }

        google.setOnLoadCallback(draw%sChart);
""" %(key, rows[:-1], key.replace("_"," "), key, key)

        print "Content-type:text/html\n\n"
        print """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="keywords" content="" />
<meta name="description" content="" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>IPsec VPN Test Case Manager</title>
<link href="/style.css" rel="stylesheet" type="text/css" media="screen" />
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
        // Load the Visualization API and the piechart package.
        google.load('visualization', '1.0', {'packages':['corechart']});
        
        // Set a callback to run when the Google Visualization API is loaded.
%s
    </script>
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
        <div id="page">
            <div id="page-bgtop">
                <div id="page-bgbtm">
                    <div id="content">
                        <div class="post">
                            <h2 class="title">Test Case Analysis</h2>
                            <div class="entry">
""" %(javascript if not error_messages else "")

        if error_messages:
            print error_messages
        else:
            print r"""
                                Test Cases Used: %s
                                <table>
                                <tr>
                                    <td>
                                        <div id="IKE_ENCRYPTION_chart"></div>
                                    </td>
                                    <td>
                                        <div id="IPSEC_ENCRYPTION_chart"></div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <div id="IKE_AUTHENTICATION_chart"></div>
                                    </td>
                                    <td>
                                        <div id="IPSEC_AUTHENTICATION_chart"></div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <div id="IKE_DH_GROUP_chart"></div>
                                    </td>
                                    <td>
                                        <div id="IPSEC_DH_GROUP_chart"></div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <div id="IKE_DPD_chart"></div>
                                    </td>
                                    <td>
                                        <div id="PFS_chart"></div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <div id="NEGOTIATION_MODE_chart"></div>
                                    </td>
                                </tr>
                                </table>
""" %(form.getvalue("analyze_parameters"))

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
