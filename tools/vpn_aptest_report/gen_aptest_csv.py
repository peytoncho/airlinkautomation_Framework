##############################################################################
# This script is used to generate a CSV file that can be uploaded 
# to aptest to report the IPsec VPN default test case results
##############################################################################

import csv
import os, sys
import time 
import ftplib

sys.path.append(os.environ['AIRLINKAUTOMATION_HOME'] + "/lib/common")
sys.path.append(os.environ['AIRLINKAUTOMATION_HOME'] + "/lib/site-packages")
sys.path.append(os.environ['AIRLINKAUTOMATION_HOME'] + "/testsuite/Feature/VPN/webserver/cgi-bin")

from common_funcs import pack_tc_list

import basic_airlink

tbd_config_map = basic_airlink.get_tbd_config_data()

compiled_reports_dir = os.environ['AIRLINKAUTOMATION_HOME'] + '\\tools\\vpn_aptest_report\compiled_reports\\'

class TestCase:
    # Class to hold individual test case results
    def __init__(self, name, result, log):
        self.name = name # test case name - example "tc_ipsec_vpn_case_20_AES.."
        self.result = []
        self.add_result(result, log)

    def get_status(self):
        if self.get_count()["pass"]:
            return True
        else:
            return False 

    def add_result(self, result, log):
        self.result.append({"result": result, "log": log})

    def get_count(self):
        count = {"pass": 0, "fail": 0, "error": 0}
        for run in self.result:
            count[run["result"]] += 1
        return count

    @classmethod
    def combo_number(cls, name):
        # returns the combo number
        for seg in name.split("_"):
            try:
                return int(seg)
            except ValueError:
                pass
        return None

    def __str__(self):
        return "%s\npass: %d, fail: %d, error: %d - %s" %(self.name, 
                                                           self.get_count()["pass"], 
                                                           self.get_count()["fail"], 
                                                           self.get_count()["error"], 
                                                           "Complete" if self.get_status() else "Incomplete")

class ApTestTestCase:
    # Container to hold an ApTest test case
    def __init__(self, combo_number):
        """An object represeting a testcase on ApTest

        args: combo_number - used to determine the group number of the testcase. Multiple indices will map to the same group number.
        """
        self.group_number = (combo_number + 99) / 100
        self.tc_list = [] # the list of combinations that have been run belonging to this testcase_id

    def __str__(self):
        ret = ""
        for tc in self.tc_list:
            ret += str(tc) + "\n"

        return ret

    def get_range(self):
        return range(100*self.group_number - 99, 100*self.group_number + 1)

    def sort_tc_list(self):
        self.tc_list = sorted(self.tc_list, key=lambda tc:tc.name)

    def add_combo(self, name, result, log):
        # loop through the list of combos that have been recorded under this group to see if there's already a recorded result 
        for tc in self.tc_list:
            if tc.name == name: # found existing record
                tc.add_result(result, log) # update existing record
                return

        # count not find existing record -> create a new one
        self.tc_list.append(TestCase(name, result, log))

    def get_result(self): # get a result by ANDing all the results in the list
        final_result = True
        for tc in self.tc_list:
            final_result = final_result and tc.get_status()

        if final_result:
            if len(self.tc_list) == 100: # full pass only if all tc's in the group has finished and passed
                return "pass"
            else:
                return "conditionalpass" # conditional pass if only some have been run
        else:
            return "fail" # fail if anything failed

    def get_summary(self):
        summary = {"pass":[], "not pass":[]}

        for tc in self.tc_list: # loop over everything we have recorded for this test group
            if tc.get_status():
                summary["pass"].append(TestCase.combo_number(tc.name))
            else:
                summary["not pass"].append(TestCase.combo_number(tc.name))

        return summary

    def get_notes(self): # returns the notes that are to be recorded on aptest
        notes = ""
        summary = self.get_summary()
        notes += "Passed [%d]: %s\n" %(len(summary["pass"]), pack_tc_list(summary["pass"]))
        notes += "Failed/Error [%d]: %s\n" %(len(summary["not pass"]), pack_tc_list(summary["not pass"]))
        return notes

    def get_total_count(self):
        total_count = {"pass": 0, "fail": 0, "error": 0}
        for tc in self.tc_list:
            total_count["pass"] += tc.get_count()["pass"]
            total_count["fail"] += tc.get_count()["fail"]
            total_count["error"] += tc.get_count()["error"]
        return total_count

class TestSession:
    def __init__(self):
        self.test_list = [] # a list of ApTestTestCase objects

    def __str__(self):
        ret = ""
        for test in self.test_list:
            ret += str(test)
        return ret

    def add_result(self, test_case, result, log):
        combo_number = TestCase.combo_number(test_case) # extract the combo number

        attc_ref = None
        for aptest_testcase in self.test_list: # loop through the ApTestTestCase objects to find the one that this combo_number belongs to
            if combo_number in aptest_testcase.get_range():
                attc_ref = aptest_testcase
                break
        if attc_ref is None: # if we can't find an already existing group, make it
            self.test_list.append(ApTestTestCase(combo_number))
            attc_ref = self.test_list[-1]

        attc_ref.add_combo(test_case, result, log)

    def parse_html(self, filename):
        # read file
        with open(filename, 'r') as f:
            report = f.read()

        for record in report.split("<div class='testcase'>")[1:]:
            # get test case id
            test_case = record.split("</div>")[0]

            # get test case result
            for temp in record.split(">"):
                if "</a" in temp:
                    result = temp.replace("</a","")
                    break

            # get the log
            log = record[record.find("= \'")+len("= \'"):record.find("\';</script>")]
                
            
            # add result to the session if it has prefix "tc_ipsec_vpn_case" -> reporting of other test cases should not be using this script/method
            if "tc_ipsec_vpn_case" in test_case:
                self.add_result(test_case, result, log)

def main():
    os.system("cls")

    # Check to make sure the compiled reports director is not there because we will create files there and upload anything that is already present there to the server
    # Delete it if there's files there leftover from a previously failed run of this script 
    if os.path.exists(compiled_reports_dir):
        os.system("rmdir %s /S /Q" %compiled_reports_dir)

    # parse the HTML reports 
    print "Parsing source HTML reports...\n\n",
    test_session = TestSession()
    html_source_dir = os.environ['AIRLINKAUTOMATION_HOME'] + '\\tools\\vpn_aptest_report\source_files\\'

    aleos_fw_ver = raw_input("Which firmware version do you want to use?\n(You can say, for example, 4.3.5 to use all builds in the release or 4.3.5.004 to only use that build. Any HTML report without the specified version in the source_files directory is ignored) ")

    for html_file in os.listdir(html_source_dir):
        # ignore file if it's not an html or if its from another FW build
        if not html_file.endswith(".html") or aleos_fw_ver not in html_file: 
            continue

        # parse the html file
        test_session.parse_html(html_source_dir + html_file)

    print "\n\n<Done>\n\n"
    time_stamp = time.strftime("%b-%d-%Y_%H-%M-%S") # time stamp for both csv file and combined html reports created by this script

    # write results to a csv file
    out_filename = "vpn_aptest_upload.csv"
    with open(out_filename, 'w') as csvfile:
        writer = csv.writer(csvfile)

        # top row
        writer.writerow(['ID','RESULT','NOTES']) 

        # each ApTestTestCase object (corresponds to a test case id on aptest) gets a row in the csv
        for attc in test_session.test_list:
            # Create a combined HTML report
            html_filename = create_combined_html(attc, aleos_fw_ver, time_stamp)

            report_link = "http://%s/automation/results/archive/VPN/%s" %(tbd_config_map["JENKINS"]["MASTER_ADDRESS"], html_filename.split('\\')[-1])

            test_case_id = 'Feature/VPN/Automation/VPN_IKE_ESP_Parameters_Grp_%d'%attc.group_number
            test_case_result = attc.get_result()
            test_case_notes = attc.get_notes() + report_link
            writer.writerow([test_case_id,test_case_result,test_case_notes]) 

    # transfer the compiled html reports to the jenkins machine
    print "Uploading compiled HTML reports to Jenkins server...\n\n",
    failed_uploads = []
    for report in os.listdir(compiled_reports_dir):
        path = compiled_reports_dir + report
        if not upload_report(path):
            failed_uploads.append(report)
        else:
            print "File uploaded: %s" %report

    print "\n\n<Done>\n\n"

    if failed_uploads:
        print "\n\nThe following files were not successfully uploaded to Jenkins server:"
        for fails in failed_uploads:
            print "%s\n" %fails
        print "\n"

    print "Cleaning up temporary files...",

    # delete the temp folder after uploading reports
    os.system("rd %s /S /Q" %compiled_reports_dir)
    print "\n\n<Done>\n\nFinished!"

def upload_report(report_filename):
    result = True
    ftp_path = '/results/archive/VPN/'
    
    try:
        
        ftp = ftplib.FTP(tbd_config_map["JENKINS"]["MASTER_ADDRESS"], tbd_config_map["JENKINS"]["USERNAME"], tbd_config_map["JENKINS"]["PASSWORD"])
        fp = open(report_filename,'rb')
        ftp.cwd(ftp_path)
        ftp.storbinary('STOR '+ report_filename.split('\\')[-1], fp)        
        fp.close()
        ftp.close()
    except Exception as e:
        result = False
    
    return result

def create_combined_html(attc, aleos_fw_ver, time_stamp):
    # create a folder for the created reports if it's not already there
    if not os.path.exists(compiled_reports_dir):
        os.makedirs(compiled_reports_dir)

    html_filename = "%s\%s_VPN_ipsec_default_group_%02d_%s.html" %(compiled_reports_dir, aleos_fw_ver, attc.group_number, time_stamp)

    # open the file to be written
    with open(html_filename, 'w') as f:
        
        #===============================================================
        # <head></head>
        #===============================================================
        f.write(r"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>VPN Test Report</title>
    <meta name="generator" content="HTMLTestRunner 0.8.1"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    
<style type="text/css" media="screen">
body        { font-family: verdana, arial, helvetica, sans-serif; font-size: 80%; }
table       { font-size: 100%; }
pre         { }

/* -- heading ---------------------------------------------------------------------- */
h1 {
}
.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}

.heading .attribute {
    margin-top: 1ex;
    margin-bottom: 0;
}

.heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex;
}

/* -- report ------------------------------------------------------------------------ */
#show_detail_line {
    margin-top: 3ex;
    margin-bottom: 1ex;
}
#result_table {
    width: 80%;
    border-collapse: collapse;
    border: medium solid #777;
}
#header_row {
    font-weight: bold;
    color: white;
    background-color: #777;
}
#result_table td {
    border: thin solid #777;
    padding: 2px;
}
#total_row     { font-weight: bold; }
.passClass     { background-color: #6c6; }
.failClass     { background-color: #c60; }
.errorClass    { background-color: #c00; }
.passCase      { color: #6c6; margin-left: 2em;}
.hiddenPassCase   { display: none;}
.notPassCase   { color: #c00; margin-left: 2em;}
.hiddenNotPassCase   { display: none;}
.passSession   { background-color: #6c6; }
.hiddenPassSession   { display: none;}
.failSession   { background-color: #c60; }
.hiddenFailSession   { display: none;}
.errorSession  { background-color: #c00; }
.hiddenErrorSession  { display: none;}
.hiddenRow     { display: none; }
.testcase      { margin-left: 2em; }

/* -- ending ---------------------------------------------------------------------- */
#ending {
}

</style>

</head>""")

        #===============================================================
        # Java script functions
        #===============================================================
        f.write(r"""
<body>
<script language="javascript" type="text/javascript"><!--
output_list = Array();

/* level - 0:Summary; 1:Failed; 2:All */
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        id = tr.id;
        if (id.substr(0,2) == 'ft') {
            if (level < 1) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
        if (id.substr(0,2) == 'pt') {
            if (level > 1) {
                tr.className = '';
            }
            else {
                tr.className = 'hiddenRow';
            }
        }
    }
}

function ToggleTcDetail(tc_name, count) {
    var id_list = Array(count);
    var state = '';
    for (var i = 0; i < count; i++) {
        switch(document.getElementById(tc_name + '_' + i).className)
        {
            case "passSession":
                document.getElementById(tc_name + '_' + i).className = "hiddenPassSession";
                break;
            case "hiddenPassSession":
                document.getElementById(tc_name + '_' + i).className = "passSession";
                break;
            case "failSession":
                document.getElementById(tc_name + '_' + i).className = "hiddenFailSession";
                break;
            case "hiddenFailSession":
                document.getElementById(tc_name + '_' + i).className = "failSession";
                break;
            case "errorSession":
                document.getElementById(tc_name + '_' + i).className = "hiddenErrorSession";
                break;
            case "hiddenErrorSession":
                document.getElementById(tc_name + '_' + i).className = "errorSession";
                break;
            default:
                break;
        }
    }
}

function showClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    for (var i = 0; i < count; i++) {
        tid0 = 't' + cid.substr(1) + '.' + (i+1);
        tid = 'f' + tid0;
        tr = document.getElementById(tid);
        if (!tr) {
            tid = 'p' + tid0;
            tr = document.getElementById(tid);
        }
        id_list[i] = tid;
        if (tr.className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        tid = id_list[i];
        if (toHide) {
            document.getElementById(tid).className = 'hiddenRow';
        }
        else {
            document.getElementById(tid).className = '';
        }
    }
}

function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}

function showOutput(id, name) {
    var w = window.open("", //url
                    "",
                    "resizable,scrollbars,status,width=800,height=450");
    d = w.document;
    d.write("<pre>");
    d.write(html_escape(output_list[id]));
    d.write("\n");
    d.write("<a href='javascript:window.close()'>close</a>\n");
    d.write("</pre>\n");
    d.close();
}
--></script>""")

        #===============================================================
        # Heading
        #===============================================================
        summary = attc.get_summary() 
        f.write(r"""
<div class='heading'>
<h1>VPN Test Report</h1>
<p class='attribute'><strong>Status:</strong> Pass: %d, Fail/Error: %d</p>
</div>""" %(len(summary["pass"]), len(summary["not pass"])))


        #===============================================================
        # Results table header
        #===============================================================
        f.write(r"""
<table id='result_table'>
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row'>
    <td>Test case</td>
    <td>Count</td>
    <td>Pass</td>
    <td>Fail</td>
    <td>Error</td>
    <td>View</td>
</tr>




""")

        #===============================================================
        # create a row for each test combo executed 
        #===============================================================
        attc.sort_tc_list()
        for tc in attc.tc_list:
            count = tc.get_count()

            # summary for a particular combo
            f.write(r"""
<tr id='%s' class='%s'>
    <td class='none'><div class='testcase'>%s</div></td>
    <td>%d</td>
    <td>%d</td>
    <td>%d</td>
    <td>%d</td>
    <td colspan='1' align='center'><a href="javascript:ToggleTcDetail('%s', '%s')">detail</a>
</td>
</tr>

""" %(tc.name, 
      "passCase" if tc.get_status() else "notPassCase", 
      tc.name, 
      count["pass"] + count["fail"] + count["error"], # total 
      count["pass"], # pass
      count["fail"], # fail
      count["error"], #error
      tc.name, 
      count["pass"] + count["fail"] + count["error"])) 

            # a combo could have been executed more than once. we call it 'session'
            for session in range(len(tc.result)):
                classname = {"pass":"hiddenPassSession", "fail":"hiddenFailSession", "error":"hiddenErrorSession"}[tc.result[session]["result"]]
                f.write(r"""
<tr id='%s' class='%s'>
<td></td>
<td colspan='5' align='center'><a href="javascript:showOutput('%s')">%s</a></td>
<script language="javascript" type="text/javascript">output_list['%s'] = '%s';</script>

</tr>

""" %(tc.name+"_"+str(session),
      classname, 
      tc.name+"_"+str(session), 
      tc.result[session]["result"], 
      tc.name+"_"+str(session), 
      tc.result[session]["log"]))

        total_count = attc.get_total_count()
        f.write(r"""
<tr id='total_row'>
    <td>Total</td>
    <td>%d</td>
    <td>%d</td>
    <td>%d</td>
    <td>%d</td>
    <td>&nbsp;</td>
</tr>
</table>""" %(total_count["pass"] + total_count["fail"] + total_count["error"],
              total_count["pass"],
              total_count["fail"],
              total_count["error"]))

        f.write(r"""
<div id='ending'>&nbsp;</div>

</body>
</html>""")


    return html_filename
        
        

if __name__ == "__main__":
    main()
