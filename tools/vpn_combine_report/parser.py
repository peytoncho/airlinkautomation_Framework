import os, sys
import datetime
import operator, itertools

source_file_dir = os.getcwd() + '\\source_files\\'
base_name = "tc_ipsec_vpn_case_"

sys.path.append(os.environ['AIRLINKAUTOMATION_HOME'] + "/testsuite/Feature/VPN/")
import ipsec_vpn_tc_manager

def main():
    filelist = []
    for f in os.listdir(source_file_dir):
        if f.startswith(".") or not f.endswith(".html"): 
            continue

        filelist.append(f)

    c_report = CombinedReport()
    c_report.add_to_filelist(filelist)
    for f in filelist:
        c_report.add_tc_list(ParseReport(f).get_summary())

    c_report.sort_tc_list()

    c_report.generate_combined_html_report(".VPN_TESTLOG.html")

class ParseReport():
    def __init__(self, filename):
        f = open(source_file_dir + '\\' + filename, 'r')
        self.report = f.read()
        f.close()

    def get_summary(self):
        tc_list = []

        for tc in self.report.replace('\n','').split("<div class=\'testcase\'>")[1:]:
            tc_list.append({})

            # Get test case name
            tc_list[-1]["NAME"] = tc.split("</div>")[0]

            # Get result
            for temp in tc.split(">"):
                if "</a" in temp:
                    tc_list[-1]["RESULT"] = temp.replace("</a","")
                    break

            # Get log string
            #tc_list[-1]["LOG"] = "LOG for %s" %tc_list[-1]["NAME"]
            tc_list[-1]["LOG"] = tc[tc.find("= \'")+len("= \'"):tc.find("\';</script>")]

        return tc_list

class TcSummary():
    def __init__(self, name, result, log):
        self.name = name
        self.result = [result]
        self.log = [log]

    def __str__(self):
        return "\nTest Case: %s\nPass: %d\nFail: %d\nError: %d\n" %(self.name, self.get_count(["pass"]), self.get_count(["fail"]), self.get_count(["error"]))

    def add_session(self, result, log):
        self.result.append(result)
        self.log.append(log)

    def get_count(self, status):
        ret = 0
        for r in self.result:
            if r in status:
                ret += 1
        return ret

    def get_total_count(self):
        return len(self.result)

class CombinedReport():
    def __init__(self):
        self.tc_list = []
        self.filelist = []

    def add_tc_list(self, tc_list):
        for tc in tc_list:
            self.add_tc(tc)

    def add_tc(self, tc):
        for existing_tc in self.tc_list:
            if tc["NAME"] == existing_tc.name:
                existing_tc.add_session(tc["RESULT"], tc["LOG"])
                return
        self.tc_list.append(TcSummary(tc["NAME"], tc["RESULT"], tc["LOG"]))

    def add_to_filelist(self, filelist):
        self.filelist += filelist

    def sort_tc_list(self):
        self.tc_list = sorted(self.tc_list, key=lambda tc:tc.name)

    def get_passed_list(self):
        self.sort_tc_list()
        pass_list = []
        for tc in self.tc_list:
            if base_name in tc.name and tc.get_count(["pass"]) >= 1:
                pass_list.append(int(tc.name[len(base_name):].split('_')[0]))

        return self.format_output(pass_list)

    def get_not_yet_pass_list(self):
        self.sort_tc_list()
        pass_list = []
        for tc in self.tc_list:
            if base_name in tc.name and tc.get_count(["error", "fail"]) >= 1 and not tc.get_count(["pass"]):
                pass_list.append(int(tc.name[len(base_name):].split('_')[0]))

        return self.format_output(pass_list)

    def get_not_attempted_list(self):
        all_tcs = range(1, ipsec_vpn_tc_manager.IpsecVpnTestCaseManager().num_tcs() + 1)
        for tc in self.tc_list:
            try:
                all_tcs.remove(int(tc.name[len(base_name):].split('_')[0]))
            except ValueError:
                pass
        return self.format_output(all_tcs)

    def format_output(self, number_list):
        number_list.sort()

        ranges = []
        for k, g in itertools.groupby(enumerate(number_list), lambda (i,x):i-x):
            ranges.append(map(operator.itemgetter(1), g))

        total = 0
        output = "["
        for i in ranges:
            output += "%d-%d," %(i[0],i[-1])
            total += i[-1] - i[0] + 1
        output = output[:-1] + "] <Strong>Total: %d</Strong>" %total

        return output 

    def get_total_count(self):
        count = 0
        for tc in self.tc_list:
            count += len(tc.result)

    def get_tc_summary(self, name):
        for tc in self.tc_list:
            if name in tc.name:
                return tc
        return None

    def generate_combined_html_report(self, filename):
        f = open(filename, 'w')

        # a bunch of html bookkeeping stuff
        string = """
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

</head>
<body>
<script language="javascript" type="text/javascript"><!--
output_list = Array();

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

/* level - 0: All, 1: Some Passed, 2: None Passed */
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        switch (level)
        {
            case 0:
                if (trs[i].className == 'hiddenPassCase') {
                    trs[i].className = 'passCase';
                } else if (trs[i].className == 'hiddenNotPassCase') {
                    trs[i].className = 'notPassCase';
                }
                break;
            case 1:
                if (trs[i].className == 'hiddenPassCase') {
                    trs[i].className = 'passCase';
                } else if (trs[i].className == 'notPassCase') {
                    trs[i].className = 'hiddenNotPassCase';
                }
                break;
            case 2:
                if (trs[i].className == 'passCase') {
                    trs[i].className = 'hiddenPassCase';
                } else if (trs[i].className == 'hiddenNotPassCase') {
                    trs[i].className = 'notPassCase';
                }
                break;
            case 3:
                if (trs[i].className == 'passCase') {
                    trs[i].className = 'hiddenPassCase';
                } else if (trs[i].className == 'notPassCase') {
                    trs[i].className = 'hiddenNotPassCase';
                }
                break;
            default:
                break;
        }
    }

    trs = document.getElementsByClassName('passSession');
    for (var i = 0; i < trs.length; i++) {
        trs[i].className = 'hiddenPassSession';
    }

    trs = document.getElementsByClassName('failSession');
    for (var i = 0; i < trs.length; i++) {
        trs[i].className = 'hiddenFailSession';
    }

    trs = document.getElementsByClassName('errorSession');
    for (var i = 0; i < trs.length; i++) {
        trs[i].className = 'hiddenErrorSession';
    }
}

function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}

function showOutput(id) {
    var w = window.open("", //url
                    "",
                    "resizable,scrollbars,status,width=800,height=450");
    d = w.document;
    d.write("<pre>");
    d.write(html_escape(output_list[id]));
    d.write("\\n");
    d.write("<a href='javascript:window.close()'>close</a>\\n");
    d.write("</pre>\\n");
    d.close();
}
--></script>

"""

        f.write(string)
        
        # list of files used to compile this report
        temp = ""
        for log_file in self.filelist:
            temp += log_file + "\\n"

        string = r"""
<div class='heading'>
<h1>Compiled VPN Test Report</h1>
<p><strong>Last Compiled:</strong> %s</p>
<script language="javascript" type="text/javascript">output_list['file_source'] = '%s';</script>
</div>

<td colspan='5' align='center'><a href="javascript:showOutput('file_source')">Log Files Used</a></td>

</body>
</html>
""" %(datetime.datetime.now(), temp)
        f.write(string)

        # show summary of tc
        string = r"""
<p>
<strong> Summary for %s</strong><br>
<strong>Passed: </strong>%s<br><br>
<strong>Attempted but no pass:</strong> %s<br><br>
<strong>Not Attempted:</strong> %s<br><br>
</p>
""" %(base_name[:-1],self.get_passed_list(), self.get_not_yet_pass_list(), self.get_not_attempted_list())
        f.write(string)

        # settings to choose which testcases to display
        string = r"""
<p><strong>Filter:</strong>
<a href='javascript:showCase(0)'>All</a>
<a href='javascript:showCase(1)'>At Least One Session Passed</a>
<a href='javascript:showCase(2)'>No Sessions Passed</a>
<a href='javascript:showCase(3)'>None</a>
</p>
"""
        f.write(string)

        # Results table header
        string = r"""
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

"""
        f.write(string)

        # test cases row
        count = 0
        for tc in self.tc_list:
            count += 1
            string = r"""
<tr id='%s' class='%s'>
    <td class='none'><div class='testcase'>%s</div></td>
    <td>%d</td>
    <td>%d</td>
    <td>%d</td>
    <td>%d</td>
    <td colspan='1' align='center'><a href="javascript:ToggleTcDetail('%s', '%s')">detail</a>
</td>
</tr>

""" %(tc.name, "passCase" if tc.get_count(["pass"]) else "notPassCase", tc.name, tc.get_total_count(), tc.get_count(["pass"]), tc.get_count(["fail"]), tc.get_count(["error"]) ,tc.name, tc.get_total_count())
            f.write(string)

            for session in range(len(tc.result)):
                classname = {"pass":"hiddenPassSession", "fail":"hiddenFailSession", "error":"hiddenErrorSession"}[tc.result[session]]
                string = (r"""
<tr id='%s' class='%s'>
<td></td>
<td colspan='5' align='center'><a href="javascript:showOutput('%s')">%s</a></td>
<script language="javascript" type="text/javascript">output_list['%s'] = '%s';</script>

</tr>

""" %(tc.name+"_"+str(session), classname, tc.name+"_"+str(session), tc.result[session], tc.name+"_"+str(session), tc.log[session]))[1:-1]
                f.write(string)
    








        f.close()

if __name__ == "__main__":
    main()
