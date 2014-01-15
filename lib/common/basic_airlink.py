################################################################################
# This basic configuration and methods applies for all tests.
#
# Company: Sierra Wireless
# Time: Feb 14, 2013
# Author: Airlink
#
################################################################################

import logging
import yaml
import smtplib
import unittest
import datetime
import os
import sys
import argparse

from multiprocessing import Process
import time
import ftplib

airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 

slash = "\\" if sys.platform == 'win32' else "/"

lib_common_path         = slash+'lib'+slash+'common'
lib_packages_path       = slash+'lib'+slash+'site-packages'
feature_admin_path      = slash+'testsuite'+slash+'Feature'+slash+'Admin' 
feature_status_path     = slash+'testsuite'+slash+'Feature'+slash+'Status'   
feature_lan_path        = slash+'testsuite'+slash+'Feature'+slash+'LAN' 
feature_wan_path        = slash+'testsuite'+slash+'Feature'+slash+'WAN' 
feature_vpn_path        = slash+'testsuite'+slash+'Feature'+slash+'VPN' 
feature_gps_path        = slash+'testsuite'+slash+'Feature'+slash+'GPS' 
feature_er_path         = slash+'testsuite'+slash+'Feature'+slash+'Eventreporting' 
feature_fwupdate_path   = slash+'testsuite'+slash+'Feature'+slash+'Fwupdate' 
feature_template_path   = slash+'testsuite'+slash+'Feature'+slash+'Template' 
feature_serial_path     = slash+'testsuite'+slash+'Feature'+slash+'Serial' 
feature_security_path   = slash+'testsuite'+slash+'Feature'+slash+'Security' 
feature_apps_path       = slash+'testsuite'+slash+'Feature'+slash+'Applications' 
feature_datausage_path  = slash+'testsuite'+slash+'Feature'+slash+'Applications'+slash+'Data_Usage' 
feature_services_path   = slash+'testsuite'+slash+'Feature'+slash+'Services' 
feature_telnet_path     = slash+'testsuite'+slash+'Feature'+slash+'Services'+slash+'Telnet' 
feature_ssh_path        = slash+'testsuite'+slash+'Feature'+slash+'Services'+slash+'SSH' 
feature_snmp_path       = slash+'testsuite'+slash+'Feature'+slash+'Services'+slash+'SNMP' 
feature_sms_path        = slash+'testsuite'+slash+'Feature'+slash+'Services'+slash+'SMS' 
feature_lpm_path        = slash+'testsuite'+slash+'Feature'+slash+'Services'+slash+'LPM' 
testclass_path          = slash+'testsuite'+slash+'Feature'+slash+'TestClass' 
smoke_path              = slash+'testsuite'+slash+'Smoke' 
performance_path        = slash+'testsuite'+slash+'Performance'
throughput_path         = slash+'testsuite'+slash+'Performance'+slash+'Throughput'

def yaml_include(loader,node):
    with file(node.value) as inputfile:
        return yaml.load(inputfile)

OK   = 1
NOK  = -1
PASS = 1
FAIL = -1 
ERR  = "ERROR"

FEATURE_AREA =["WAN","LAN","Security","VPN","GPS","Template","FWupdate","Services","Serial", "Admin"]
FEATUTE_SUB_AREA = ["LPM", "Telnet","SNMP","SMS"]

#Valid WnsRemoteEx Commands to control Anritsu callbox:
WNS_START_SS_APP           = 0   #Starts up SmartStudio application 
WNS_LOAD_SIMU_PARAM_FILE   = 1   #Load SmartStudio Simulation parameter file
WNS_LOAD_CELL_PARAM_FILE   = 2   #Load SmartStudio Cell parameter file 
WNS_START_SS_SIMU          = 3   #Starts SmartStudio simulation (turn on cells and wait for UE, etc.)
WNS_STOP_SS_SIMU           = 4   #Stop SmartStudio simulation (turn off cells, allow cell reconfigurations, etc.)
WNS_CLOSE_SS_APP           = 5   #Close SmartStudio application
WNS_GET_UE_STATUS          = 6   #Get UE Status (and WCDMA RRC Status)
WNS_GET_SS_STATUS          = 7   #Gets the SmartStudio status
WNS_START_IMS_SERVICE      = 8   #Start IMS Service
WNS_STOP_IMS_SERVICE       = 9   #Stop IMS Service
WNS_RESET_SS_SIMU          = 10  #Reset Simulation: Forcibly changes the simulation status of SmartStudio.
WNS_START_MEASURE_EXPORT   = 11  #Start Measurement: Opens the Measure window, and then starts saving the measurement results. 
WNS_STOP_MEASURE_EXPORT    = 12  #Stop Measurement: Stops saving the measurement results
WNS_SET_STATUS_CHANGE      = 13  #Set Status Change Parameter: (During simulation stop or for Non Camping Cell)
WNS_SET_PDN_INFO           = 14  #Set PDN Information: Sets the PDN Information for selected PDN number. Set <ParamString> using the format: parameter=value.
WNS_GET_PDN_INFO           = 15  #Gets the PDN Information for selected PDN number. Set <ParamString> using the format: parameter=value.
WNS_SET_SERVICE_PARAM      = 16  #Sets the Dedicated Service Parameter: Sets Packet filtering, Qos, etc. Set <ParamString> using the format: parameter=value. 
WNS_SET_TRIGGER_MSG        = 17  #Trigger Protocol Events: Accept, Reject (with Cause), and Ignore specific messages. Set <ParamString> using the format: parameter=value. 
WNS_GET_TRIGGER_MSG        = 177 #???  to talk to Serkan
WNS_SELECT_CELL            = 18  #Sets the cell to be used in the simulation for the specified BTS
WNS_SET_SIM_PARAM          = 19  #Set Simulation Param: Set <ParamString> using the format: parameter=value
WNS_SET_CELL_PARAM         = 20  #Set Cell Param: Set <ParamString> using the format: parameter=value.
WNS_GET_CAMPING_CELL       = 21  #Gets the BTS information used by UE
WNS_SET_OOS_ALL_CELL       = 22  #Sets the out-of-service operation ON or OFF.
WNS_SET_OOS_ONE_CELL       = 23  #Sets the out-of-service operation ON or OFF   TODO:
WNS_GET_OOS_ONE_CELL       = 24  #Gets the out-of-service operation ON or OFF
WNS_OPERATE_PACKET         = 25  #Operation commands for the packet connection
WNS_CLOSE_C2K_SESSION      = 26  #C2K session close
WNS_UE_POWER_CONTROL       = 27  #Implements the Power Control of UE
WNS_GET_LEVEL              = 28  #Gets the data of Monitor window of MX847501A control software
WNS_OPERATE_TRAFFIC_VOLUME = 29  #Operates the traffic volume
WNS_LOAD_TC_PARAM_FILE     = 30  #Load SmartStudio TestCase parameter file
WNS_SET_TC_PARAM           = 31  #Sets Test Case parameters
WNS_START_SS_CELL_TEST     = 32  # Starts the SmartStudio cell test. TestCaseParamFilePath is optional
WNS_QUERY_SS_TEST_STATUS   = 33  # Queries the test operation status of SmartStudio
WNS_LOAD_SS_TRACE_FILTER   = 34  #Load SmartStudio Trace Filter file
WNS_SAVE_SS_TRACE_LOG      = 35  # Saves the SmartStudio trace data
WNS_SAVE_SS_SEQ_LOG        = 36  # Saves the sequence log of SmartStudio.
WNS_CLEAR_SS_SEQ_LOG       = 37  # Deletes the retained sequence log
WNS_SAVE_SS_MSG_LOG        = 38  # Saves the message log
WNS_CLEAR_SS_MSG_LOG       = 39  # Deletes the message log
WNS_C2K_SAVE_TRACE_LOG     = 40  # Saves the trace log held by C2K PVT

WNS_IPERF_UDP              = 100 # UDP IPerf command
WNS_IPERF_TCP              = 101 # TCP IPerf command

log_level = {  \
    "CRITICAL" : logging.CRITICAL, \
    "ERROR"    : logging.ERROR, \
    "WARN"     : logging.WARNING, \
    "NOTSET"   : logging.NOTSET, \
    "INFO"     : logging.INFO, \
    "DEBUG"    : logging.DEBUG \
}

fgcolor_map = { \
    "BLACK"   : 30, \
    "RED"     : 31, \
    "GREEN"   : 32, \
    "YELLOW"  : 33, \
    "BLUE"    : 34, \
    "MAGENTA" : 35, \
    "WHITE"   : 37, \
}

bgcolor_map = { \
    "BLACK"   : 40, \
    "RED"     : 41, \
    "GREEN"   : 42, \
    "YELLOW"  : 43, \
    "BLUE"    : 44, \
    "MAGENTA" : 45, \
    "WHITE"   : 47, \
}

verbosity_map ={ \
    "Critical" : 2, \
    "Error"    : 3, \
    "Info"     : 6, \
    "Debug"    : 7 }

yes_no_map  ={"Yes": 1, "No": 0}

display_map ={"Display": 1, "No Display": 0}

 
def slog(msg):
    '''   Print out the debug message on log file and html report    
    Args:
        msg:  message to print out in log file and html report 
    Returns: None
    ''' 
    
    logging.debug('\n'+ msg)   
    print '\n'+ msg  


def _colorlog(msg, fgcolor = None, bgcolor = None):
    '''   Print out the debug message on log file and console   
    Args:
        msg  message to print out in log file and console
        fgcolor: set foreground colour
        bgcolor: set background colour 
    Returns: None
    '''
    
    if fgcolor is not None or bgcolor is not None:
        
        ft_fail_flag = True
        bg_fail_flag = True
        ftcolor_num = "0m"
        bgcolor_num = "0m"


        if fgcolor is None:
            ft_fail_flag = False
        else:        
            for i in range(0, len(fgcolor_map.keys())):
                if fgcolor == fgcolor_map.keys()[i]:
                    ft_fail_flag = False
                    ftcolor_num = str(fgcolor_map[fgcolor])+'m'
        if bgcolor is None:
            bg_fail_flag = False
        else:    
            for i in range(0, len(bgcolor_map.keys())):
                if bgcolor == bgcolor_map.keys()[i]:
                    bg_fail_flag = False
                    bgcolor_num= str(bgcolor_map[bgcolor])+'m'
        
        if ft_fail_flag or bg_fail_flag:
            logging.debug('\n'+ msg)
            slog('\n'+'\x1b[0m'+msg+"   (Please pass the correct color)")
        else:
            if ftcolor_num == "0m":
                ftcolor_num = str(fgcolor_map["BLACK"])+'m'
            logging.debug('\n'+ msg)         
            slog('\n'+'\x1b[' + bgcolor_num + '\x1b[' + ftcolor_num + msg)
    else:
        logging.debug('\n'+ msg)
        slog('\n'+'\x1b[0m'+msg)
    
def clog(msg, fgcolor = None, bgcolor = None):
    '''
    Output colour message by console.
    Args:
        msg    : message to print out 
        fgcolor: foreground colour 
        bgcolor: background colour 
    Returns: 
        None
    
    '''
    p = Process(target = _colorlog, args = (msg, fgcolor, bgcolor,))
    p.start()
    p.join()

def cslog(msg, fgcolor = None, bgcolor = None):
    '''
        Print out colour message by console and html report .
    Args:
        msg:     message to print out 
        fgcolor: foreground color 
        bgcolor: background color 
    Returns: 
        None
    '''    
    slog('\n'+msg)
    p = Process(target = _colorlog, args = (msg, fgcolor, bgcolor,))
    p.start()
    p.join() 
    
def test_report(filename, msg):
    ''' Print out results/messages to test report file  and console
    Args:  
        filename  string, test report file name 
        msg       string, message to print out 
    Returns: None
    '''
    
    print '\n'+msg
    file_handle = open(filename,"a")
    file_handle.write('\n'+msg)
    file_handle.close()
    

def cleanup():
    ''' Test case cleanup    
    Args: none
    Returns: None
    TBD
    '''
    
    logging.debug("step: cleanup")
    
    
def run_testcases(feature_config_map, featrue_testcases):
    ''' run test cases, TO BE REMOVED  
    Args: 
        feature_config_map: array, pointer to test module configuration file
        feature_testcases:  array, pointer to test cases defined in test module 
                            configuration file 
        
    Returns:
        None
    
    '''
    for k in range(feature_config_map["RUN_REPEAT"]):
        
        if feature_config_map["RUN_ALL_TESTCASES"]:
            
            # run all test cases
            for i in range(1,feature_config_map["ALL_TASECASE_NUMBER"]+1):
                print "i="+ str(i)
                logging.debug(feature_config_map["RUN_ALL_TESTCASES"])
                featrue_testcases[feature_config_map["LIST_TESTCASES"][i]]()
                
        else:
            
            # run selective test cases
            for [a,b] in feature_config_map["RUN_SELECTIVE_TESTCASES"] :
                
                for i in range(a,b+1):
                    
                    logging.debug(feature_config_map["LIST_TESTCASES"][i])
                    featrue_testcases[feature_config_map["LIST_TESTCASES"][i]]()


def setup_suite_v1(area_config_map, tc_ts_map):
    """  Gather all the tests from this module in a test suite.    
    
    Args: 
        area_config_map: list, test area configuration
        tc_ts_map: list, test case/testmodule/testsuite mapping info
        
    Returns: 
        test suite, including the selected testcases
        
    """

    test_suite = unittest.TestSuite()

    # run selective test case
    parser = argparse.ArgumentParser(description="testsuite launcher")
    
    parser.add_argument("-n", "--tc_no", dest = "tc_no_range_arg",
        help = "test case number range", default = "")
        
    parser.add_argument("-v", "--prd_ver", dest = "prd_ver_arg",
        help = "Production version", default = "")
        
    parser.add_argument("-t", "--tc_type", dest = "tc_type_arg",
        help = "test cycle type SMOKE/REGERSSION/PERFORMANCE", default = "")
    
    args = parser.parse_args()
    
    if not args.prd_ver_arg and \
       not args.tc_no_range_arg and not args.tc_type_arg: 
        
        # run all default test cases 
        for i in range(1,len(area_config_map["LIST_TESTCASES"])+1):
                             
            if tc_ts_map[i][2]==0:
                    test_suite.addTest(tc_ts_map[i][0](tc_ts_map[i][1])) 
                    tc_ts_map[i][2]=1
                    print i, tc_ts_map[i][1] 
                    
        return test_suite   
                    
    if args.tc_no_range_arg:
        #print args.tc_no_range_arg, "tc_no_range_arg \n"
        ll = len(args.tc_no_range_arg)
        tc_no_range_arg = args.tc_no_range_arg[1:ll-1]
        tc_range_pairs = tc_no_range_arg.split(',')
        for tc_no_pair in tc_range_pairs :
            #print tc_no_pair, "tc_no_pair \n"
            para = tc_no_pair.split('-')
            #print " para =", para
            
            r0 = int(para[0])
            r1 = int(para[1])+1
            for i in range(r0,r1):
                
                product_ver_list  = \
                area_config_map["LIST_TESTCASES"][i]["PRODUCT_VER"]
                tc_type_list      = \
                area_config_map["LIST_TESTCASES"][i]["TEST_TYPE"]         
                           
                if tc_ts_map[i][2]==0 \
                            and (not args.prd_ver_arg or args.prd_ver_arg in product_ver_list) \
                            and (not args.tc_type_arg or args.tc_type_arg in tc_type_list):
                     
                    test_suite.addTest(tc_ts_map[i][0](tc_ts_map[i][1])) 
                    tc_ts_map[i][2]=1
                    print i, tc_ts_map[i][1]

    elif args.prd_ver_arg:
        
        for i in range(1,len(area_config_map["LIST_TESTCASES"])+1):

            product_ver_list=area_config_map["LIST_TESTCASES"][i]["PRODUCT_VER"]
            tc_type_list    =area_config_map["LIST_TESTCASES"][i]["TEST_TYPE"]

            if tc_ts_map[i][2]==0 and args.prd_ver_arg in product_ver_list \
                and (not args.tc_type_arg or args.tc_type_arg in tc_type_list):
            
                test_suite.addTest(tc_ts_map[i][0](tc_ts_map[i][1])) 
                tc_ts_map[i][2]=1
                print i, tc_ts_map[i][1],product_ver_list


    elif args.tc_type_arg:
       
        for i in range(1,len(area_config_map["LIST_TESTCASES"])+1):

            if tc_ts_map[i][2]==0 and args.tc_type_arg in tc_type_list:

                test_suite.addTest(tc_ts_map[i][0](tc_ts_map[i][1])) 
                tc_ts_map[i][2]=1
                print i, tc_ts_map[i][1],tc_type_list

        
    return test_suite    


    
def send_email():
    ''' send notice email by gmail server
    Args   : None
    Returns: None
    '''

    gmail_user = "morganmostafa631@gmail.com"
    gmail_pwd = "sierrawireless"
    FROM = 'morganmostafa631@gmail.com'
    TO = ['mowu@sierrawireless.com'] #must be a list
    SUBJECT = "Test results are in http://208.81.123.2:80"
    TEXT = "Test results are in http://208.81.123.2:80"

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        #server = smtplib.SMTP(SERVER) 
        server = smtplib.SMTP("smtp.gmail.com", 587) 
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        #server.quit()
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"


def get_log_filename(config_map, area_name,sub_area_name):
    ''' generate the log file name 
    Args: 
        config_map   : testbed configuration (array)
        area_name : "status" for staus feature name, "gps" for gps feature name
        sub_area_name: "SNMP" for Services' SNMP, refer to get_config_data()
    Returns: 
        log file name (string)
    '''
                
    current_date_str = str(datetime.datetime.now().date())
    current_time_str = str(datetime.datetime.now().time()).replace(":","-")
    
    device_name  = config_map["DUTS"][0]

    log_filename = airlinkautomation_home_dirname+slash+"logs"+slash+current_date_str+"_"+\
    current_time_str+"_"+ device_name +"_" + \
    config_map[device_name]["ALEOS_FW_VER"]+ "_"+ \
    area_name+"_"+sub_area_name+"_testsuite.log"
        
    return log_filename


def get_report_filename(config_map, area_name,sub_area_name):
    ''' generate the log file name 
    
    Args: 
        config_map   : testbed configuration (array)
        area_name : "status" for staus feature name, "gps" for gps feature name 
        
    Returns: 
        report file name (string)
    '''
            
    current_date_str = str(datetime.datetime.now().date())
    current_time_str = str(datetime.datetime.now().time()).replace(":","-")
    
    device_name  = config_map["DUTS"][0]
    
    report_filename = airlinkautomation_home_dirname+slash+"results"+slash+current_date_str+"_"+ \
    current_time_str+"_"+ device_name +"_" + \
    config_map[device_name]["ALEOS_FW_VER"]+ "_"+ \
    area_name+"_"+sub_area_name+"_testsuite.html"
 
    return report_filename
           
           
def get_config_data(area_name, sub_area_name):
    '''Read the test area configuration yaml files,including area and sub area's
    
    Args: 
        area_name:  test area name, e.g. LA, WAN, Throughput, etc
        sub_area_name: sub area name, Services have a few sub areas SNMP, SNTP, 
                       SMS,etc.
        
    Returns: 
        tbd_config_data : list, main configuration data from testbed yaml file 
        area_config_data: list, configurations of each test area or/and sub area 
    '''
    
    stream = open(airlinkautomation_home_dirname+\
                  slash+'config'+slash+'common_testbed_conf.yml', 'r')
    tbd_config_data = yaml.load(stream)
    stream.close()   
         
    if  area_name == "Throughput":
        fo=open(airlinkautomation_home_dirname+throughput_path+slash+\
            'throughput_test_conf.yml','r')
    elif area_name == "LAN":
        fo=open(airlinkautomation_home_dirname+feature_lan_path+slash+\
                'lan_test_conf.yml','r')
    elif area_name == "WAN":
        fo=open(airlinkautomation_home_dirname+feature_wan_path+slash+\
                'wan_test_conf.yml','r')
    elif area_name == "VPN":
        fo=open(airlinkautomation_home_dirname+feature_vpn_path+slash+\
                'vpn_test_conf.yml','r')
    elif area_name == "GPS":
        fo=open(airlinkautomation_home_dirname+feature_gps_path+slash+\
                'gps_test_conf.yml','r')
    elif area_name == "EventReporting":
        fo=open(airlinkautomation_home_dirname+feature_er_path+slash+\
        'eventreporting_test_conf.yml','r')
    elif area_name == "Applications":
        fo=open(airlinkautomation_home_dirname+feature_apps_path+slash+\
        'applications_test_conf.yml','r')
    elif area_name == "Admin":
        fo=open(airlinkautomation_home_dirname+\
                '/testsuite/Feature/Admin/admin_test_conf.yml','r')
    elif area_name == "Status":
        fo=open(airlinkautomation_home_dirname+feature_status_path+slash+\
                'status_test_conf.yml','r')
    elif area_name == "Fwupdate":
        fo=open(airlinkautomation_home_dirname+feature_fwupdate_path+slash+\
                'fwupdate_test_conf.yml','r')
    elif area_name == "Template":
        fo=open(airlinkautomation_home_dirname+feature_template_path+slash+\
                'template_test_conf.yml','r')
    elif area_name == "Security":
        fo=open(airlinkautomation_home_dirname+feature_security_path+slash+\
                'security_test_conf.yml','r')
    elif area_name == "Serial":
        fo=open(airlinkautomation_home_dirname+feature_serial_path+slash+\
                'serial_test_conf.yml','r')
    elif area_name == "Services" and sub_area_name == "Telnet":
        fo=open(airlinkautomation_home_dirname+feature_telnet_path+slash+\
                'telnet_test_conf.yml','r')
    elif area_name == "Services" and sub_area_name == "SSH":
        fo=open(airlinkautomation_home_dirname+feature_ssh_path+slash+\
                'ssh_test_conf.yml','r')
    elif area_name == "Services" and sub_area_name == "SNMP":
        fo=open(airlinkautomation_home_dirname+feature_snmp_path+slash+\
                'snmp_test_conf.yml','r')
    elif area_name == "Services" and sub_area_name == "SMS":
        fo=open(airlinkautomation_home_dirname+feature_sms_path+slash+\
                'sms_test_conf.yml','r')
    elif area_name == "Services" and sub_area_name == "LPM":
        fo=open(airlinkautomation_home_dirname+feature_lpm_path+slash+\
                'lpm_test_conf.yml','r')
    elif area_name == "TestClass":
        fo=open(airlinkautomation_home_dirname+testclass_path+slash+\
                'testclass_test_conf.yml','r')
                  
    area_config_data = yaml.load(fo)
    fo.close()
    
    return tbd_config_data, area_config_data


def get_tbd_config_data():
    ''' 
    read the test area configuration yaml files, including area and sub area's.
    Args: 
        None
        
    Returns: 
        tbd_config_data : list, main configuration data from testbed yaml file 
    '''
            
    stream = open(airlinkautomation_home_dirname+slash+'config'+slash+\
                  'common_testbed_conf.yml', 'r')
    tbd_config_data = yaml.load(stream)
    stream.close()   
    
    return tbd_config_data


def append_sys_path():
    ''' Append path to system
    '''

    sys.path.append(airlinkautomation_home_dirname+lib_common_path)
    sys.path.append(airlinkautomation_home_dirname+lib_packages_path)
    sys.path.append(airlinkautomation_home_dirname+throughput_path)
    sys.path.append(airlinkautomation_home_dirname+performance_path)
    sys.path.append(airlinkautomation_home_dirname+smoke_path)
    sys.path.append(airlinkautomation_home_dirname+feature_lan_path)
    sys.path.append(airlinkautomation_home_dirname+feature_wan_path)
    sys.path.append(airlinkautomation_home_dirname+feature_vpn_path)
    sys.path.append(airlinkautomation_home_dirname+feature_gps_path)
    sys.path.append(airlinkautomation_home_dirname+feature_er_path)
    sys.path.append(airlinkautomation_home_dirname+feature_apps_path)
    sys.path.append(airlinkautomation_home_dirname+feature_datausage_path)
    sys.path.append(airlinkautomation_home_dirname+feature_admin_path)
    sys.path.append(airlinkautomation_home_dirname+feature_status_path)
    sys.path.append(airlinkautomation_home_dirname+feature_services_path)
    sys.path.append(airlinkautomation_home_dirname+feature_telnet_path)
    sys.path.append(airlinkautomation_home_dirname+feature_ssh_path)
    sys.path.append(airlinkautomation_home_dirname+feature_snmp_path)
    sys.path.append(airlinkautomation_home_dirname+feature_sms_path)
    sys.path.append(airlinkautomation_home_dirname+feature_lpm_path)
    sys.path.append(airlinkautomation_home_dirname+feature_fwupdate_path)
    sys.path.append(airlinkautomation_home_dirname+feature_template_path)
    sys.path.append(airlinkautomation_home_dirname+feature_security_path)
    sys.path.append(airlinkautomation_home_dirname+feature_serial_path)
    

def setup_suite_v2(area_config_map, tc_ts_map):
    """  Gather all the tests from this test module into a test suite.  
    Handle the different arguments from test suite launcher command line:
        -n <test case # range>
        -t <test type>
        -v <product version>
        -d <device type>
        -r <radio module type>
    
    Args: 
        area_config_map: list, test area configuration
        tc_ts_map: list, test case/testmodule/testsuite mapping info
        
    Returns: 
        test suite, including the selected testcases
        
    """
    
    total_tc = len(area_config_map["LIST_TESTCASES"])
    
    test_suite = unittest.TestSuite()

    # run selective test case
    parser = argparse.ArgumentParser(description="testsuite launcher")
    
    parser.add_argument("-n", "--tc_no", dest = "tc_no_range_arg",
        help = "test case number range", default = "")
        
    parser.add_argument("-v", "--prd_ver", dest = "prd_ver_arg",
        help = "Production version", default = "")
        
    parser.add_argument("-t", "--tc_type", dest = "tc_type_arg",
        help = "test cycle type SMOKE/REGERSSION/PERFORMANCE", default = "")

    parser.add_argument("-d", "--dut_type", dest = "dut_type_arg",
        help = "device type GX400/GX440/ES440/LS300", default = "")
    
    parser.add_argument("-r", "--rm_type", dest = "rm_type_arg",
    help = "radio module type MC7750/MC7700/MC8705/SL8090", default = "")
            
    args = parser.parse_args()

    if not (args.prd_ver_arg  or args.tc_no_range_arg or args.tc_type_arg  or args.dut_type_arg or args.rm_type_arg): 
                
        # run all default test cases 
        for i in range(1,total_tc+1):
                             
            if tc_ts_map[i][2]==0:
                    test_suite.addTest(tc_ts_map[i][0](tc_ts_map[i][1])) 
                    tc_ts_map[i][2]=1
                    print i, tc_ts_map[i][1] 
                    
        return test_suite   
                    
    if args.tc_no_range_arg:
        #print args.tc_no_range_arg, "tc_no_range_arg \n"
        ll = len(args.tc_no_range_arg)
        tc_no_range_arg = args.tc_no_range_arg[1:ll-1]
        tc_range_pairs = tc_no_range_arg.split(',')
        for tc_no_pair in tc_range_pairs :
            #print tc_no_pair, "tc_no_pair \n"
            para = tc_no_pair.split('-')
            #print " para =", para
            
            r0 = int(para[0])
            r1 = int(para[1])+1
            for i in range(r0,r1):
                
                prd_ver_list  = area_config_map["LIST_TESTCASES"][i]["PRODUCT_VER"]
                abso_ver_list = area_config_map["LIST_TESTCASES"][i]["OBSOLETE_VER"]
                if args.prd_ver_arg: 
                    if args.prd_ver_arg in abso_ver_list or args.prd_ver_arg < prd_ver_list[0]:
                        tc_ts_map[i][2]=1   #skip flag                        
                
                tc_type_list  = area_config_map["LIST_TESTCASES"][i]["TEST_TYPE"]  
                dut_type_list = area_config_map["LIST_TESTCASES"][i]["DEVICE_TYPE"]     
                rm_type_list  = area_config_map["LIST_TESTCASES"][i]["RM_TYPE"]     
                           
                if tc_ts_map[i][2]==0 \
                            and (not args.tc_type_arg  or args.tc_type_arg  in tc_type_list) \
                            and (not args.dut_type_arg or args.dut_type_arg in dut_type_list)\
                            and (not args.rm_type_arg  or args.rm_type_arg  in rm_type_list):
                     
                    test_suite.addTest(tc_ts_map[i][0](tc_ts_map[i][1])) 
                    tc_ts_map[i][2]=1
                    print i, tc_ts_map[i][1]

    elif args.prd_ver_arg:
        
        for i in range(1,total_tc+1):

            prd_ver_list  = area_config_map["LIST_TESTCASES"][i]["PRODUCT_VER"]
            tc_type_list  = area_config_map["LIST_TESTCASES"][i]["TEST_TYPE"]
            dut_type_list = area_config_map["LIST_TESTCASES"][i]["DEVICE_TYPE"]     
            rm_type_list  = area_config_map["LIST_TESTCASES"][i]["RM_TYPE"]  
            
            if tc_ts_map[i][2]==0 \
                and args.prd_ver_arg in prd_ver_list \
                and (not args.tc_type_arg  or args.tc_type_arg  in tc_type_list)  \
                and (not args.dut_type_arg or args.dut_type_arg in dut_type_list) \
                and (not args.rm_type_arg  or args.rm_type_arg  in rm_type_list) :
            
                test_suite.addTest(tc_ts_map[i][0](tc_ts_map[i][1])) 
                tc_ts_map[i][2]=1
                print i, tc_ts_map[i][1]


    elif args.tc_type_arg:
       
        for i in range(1,total_tc+1):
            
#            prd_ver_list  = area_config_map["LIST_TESTCASES"][i]["PRODUCT_VER"]
            tc_type_list  = area_config_map["LIST_TESTCASES"][i]["TEST_TYPE"]
            dut_type_list = area_config_map["LIST_TESTCASES"][i]["DEVICE_TYPE"]     
            rm_type_list  = area_config_map["LIST_TESTCASES"][i]["RM_TYPE"]  
            
            if tc_ts_map[i][2]==0 \
                and args.tc_type_arg in tc_type_list\
                and (not args.dut_type_arg or args.dut_type_arg in dut_type_list)\
                and (not args.rm_type_arg  or args.rm_type_arg  in rm_type_list) :
#                and (not args.prd_ver_arg  or args.prd_ver_arg  in prd_ver_list) \
                
                test_suite.addTest(tc_ts_map[i][0](tc_ts_map[i][1])) 
                tc_ts_map[i][2]=1
                print i, tc_ts_map[i][1]

    elif args.dut_type_arg:
       
        for i in range(1,total_tc+1):
            
#            prd_ver_list  = area_config_map["LIST_TESTCASES"][i]["PRODUCT_VER"]
#            tc_type_list  = area_config_map["LIST_TESTCASES"][i]["TEST_TYPE"]
            dut_type_list = area_config_map["LIST_TESTCASES"][i]["DEVICE_TYPE"]     
            rm_type_list  = area_config_map["LIST_TESTCASES"][i]["RM_TYPE"]  
            
            if tc_ts_map[i][2]==0 \
                and args.dut_type_arg in dut_type_list\
                and (not args.rm_type_arg  or args.rm_type_arg in rm_type_list) :
#                and (not args.prd_ver_arg  or args.prd_ver_arg in prd_ver_list) \
#                and (not args.tc_type_arg  or args.tc_type_arg in tc_type_list) \
                
                test_suite.addTest(tc_ts_map[i][0](tc_ts_map[i][1])) 
                tc_ts_map[i][2]=1
                print i, tc_ts_map[i][1]
                
    elif args.rm_type_arg:
       
        for i in range(1,total_tc+1):
            
#            prd_ver_list  = area_config_map["LIST_TESTCASES"][i]["PRODUCT_VER"]
#            tc_type_list  = area_config_map["LIST_TESTCASES"][i]["TEST_TYPE"]
#            dut_type_list = area_config_map["LIST_TESTCASES"][i]["DEVICE_TYPE"]     
            rm_type_list  = area_config_map["LIST_TESTCASES"][i]["RM_TYPE"]  
            
            if tc_ts_map[i][2]==0 and args.rm_type_arg in rm_type_list:
#                and (not args.prd_ver_arg  or args.prd_ver_arg  in prd_ver_list) \
#                and (not args.tc_type_arg  or args.tc_type_arg  in tc_type_list) \
#                and (not args.dut_type_arg or args.dut_type_arg in dut_type_list) :
                
                test_suite.addTest(tc_ts_map[i][0](tc_ts_map[i][1])) 
                tc_ts_map[i][2]=1
                print i, tc_ts_map[i][1]
                
        
    return test_suite    

def setup_suite(tbd_config_map, area_config_map, tc_ts_map):
    """  Gather all the tests from this test module into a test suite.  
    Handle the different arguments from test suite launcher command line:
        -n <test case # range>
        -t <test type>
        -v <product version>
        -d <device type>
        -r <radio module type>
    
    Args: 
        tbd_config_map : list, testbed configuration
        area_config_map: list, test area configuration
        tc_ts_map: list, test case/testmodule/testsuite mapping info
        
    Returns: 
        test suite, including the selected testcases
        
    """
    
    device_name = tbd_config_map["DUTS"][0]
    aleos_sw_ver= tbd_config_map[device_name]["ALEOS_FW_VER"][:6]
    if aleos_sw_ver[5]==' ' or aleos_sw_ver[5]=='.': 
        aleos_sw_ver=aleos_sw_ver[:5]
    device_model= tbd_config_map[device_name]["MODEL"]
    
    cslog(device_name +", " +device_model +", " +aleos_sw_ver,"BLUE", "WHITE")
    
    test_suite = unittest.TestSuite()
    
    if not device_model in tbd_config_map["ALEOS_SW_HW"][aleos_sw_ver]:
        cslog("setup_suite(): This DUT is not applying for ALEOS FW version!", "BLUE","WHITE")
        return  test_suite  #empty
  
    total_tc = len(area_config_map["LIST_TESTCASES"])
  
    # run selective test case
    parser = argparse.ArgumentParser(description="testsuite launcher")
    
    parser.add_argument("-n", "--tc_no", dest = "tc_no_range_arg",
        help = "test case number range", default = "")
        
    parser.add_argument("-v", "--prd_ver", dest = "prd_ver_arg",
        help = "Production version", default = "")
        
    parser.add_argument("-t", "--tc_type", dest = "tc_type_arg",
        help = "test cycle type SMOKE/REGERSSION/PERFORMANCE", default = "")

    parser.add_argument("-d", "--dut_type", dest = "dut_type_arg",
        help = "device type GX400/GX440/ES440/LS300", default = "")
    
    parser.add_argument("-r", "--rm_type", dest = "rm_type_arg",
    help = "radio module type MC7750/MC7700/MC8705/SL8090", default = "")
            
    args = parser.parse_args()

    if not (args.prd_ver_arg  or args.tc_no_range_arg or args.tc_type_arg  or args.dut_type_arg or args.rm_type_arg): 
                
        # run all default test cases 
        for i in range(1,total_tc+1):
              
            if tc_ts_map[i][2]==0 \
                and (device_model in area_config_map["LIST_TESTCASES"][i]["DEVICE_TYPE"]) \
                and (not aleos_sw_ver in area_config_map["LIST_TESTCASES"][i]["OBSOLETE_VER"]):
                    test_suite.addTest(tc_ts_map[i][0](tc_ts_map[i][1])) 
                    tc_ts_map[i][2]=1
                    print i, tc_ts_map[i][1] 
                    
        return test_suite   
                    
    if args.tc_no_range_arg:
        #print args.tc_no_range_arg, "tc_no_range_arg \n"
        ll = len(args.tc_no_range_arg)
        tc_no_range_arg = args.tc_no_range_arg[1:ll-1]
        tc_range_pairs = tc_no_range_arg.split(',')
        for tc_no_pair in tc_range_pairs :
            #print tc_no_pair, "tc_no_pair \n"
            para = tc_no_pair.split('-')
            #print " para =", para
            
            r0 = int(para[0])
            r1 = int(para[1])+1
            for i in range(r0,r1):
                
                prd_ver_list  = area_config_map["LIST_TESTCASES"][i]["PRODUCT_VER"]
                abso_ver_list = area_config_map["LIST_TESTCASES"][i]["OBSOLETE_VER"]
                if args.prd_ver_arg: 
                    if args.prd_ver_arg in abso_ver_list or args.prd_ver_arg < prd_ver_list[0]:
                        tc_ts_map[i][2]=1   #skip flag                        
                
                tc_type_list  = area_config_map["LIST_TESTCASES"][i]["TEST_TYPE"]  
                dut_type_list = area_config_map["LIST_TESTCASES"][i]["DEVICE_TYPE"] 
                rm_type_list  = area_config_map["LIST_TESTCASES"][i]["RM_TYPE"]     
                           
                if tc_ts_map[i][2]==0 \
                            and (device_model in area_config_map["LIST_TESTCASES"][i]["DEVICE_TYPE"]) \
                            and (not aleos_sw_ver in area_config_map["LIST_TESTCASES"][i]["OBSOLETE_VER"]) \
                            and (not args.tc_type_arg  or args.tc_type_arg  in tc_type_list) \
                            and (not args.dut_type_arg or args.dut_type_arg in dut_type_list)\
                            and (not args.rm_type_arg  or args.rm_type_arg  in rm_type_list):
                     
                    test_suite.addTest(tc_ts_map[i][0](tc_ts_map[i][1])) 
                    tc_ts_map[i][2]=1
                    print i, tc_ts_map[i][1]

    elif args.prd_ver_arg:
        
        for i in range(1,total_tc+1):

            prd_ver_list  = area_config_map["LIST_TESTCASES"][i]["PRODUCT_VER"]
            tc_type_list  = area_config_map["LIST_TESTCASES"][i]["TEST_TYPE"]
            dut_type_list = area_config_map["LIST_TESTCASES"][i]["DEVICE_TYPE"]     
            rm_type_list  = area_config_map["LIST_TESTCASES"][i]["RM_TYPE"]  
            
            if tc_ts_map[i][2]==0 \
                and (device_model in area_config_map["LIST_TESTCASES"][i]["DEVICE_TYPE"]) \
                and (not aleos_sw_ver in area_config_map["LIST_TESTCASES"][i]["OBSOLETE_VER"])\
                and args.prd_ver_arg in prd_ver_list \
                and (not args.tc_type_arg  or args.tc_type_arg  in tc_type_list)  \
                and (not args.dut_type_arg or args.dut_type_arg in dut_type_list) \
                and (not args.rm_type_arg  or args.rm_type_arg  in rm_type_list) :
            
                test_suite.addTest(tc_ts_map[i][0](tc_ts_map[i][1])) 
                tc_ts_map[i][2]=1
                print i, tc_ts_map[i][1]


    elif args.tc_type_arg:
       
        for i in range(1,total_tc+1):
            
#            prd_ver_list  = area_config_map["LIST_TESTCASES"][i]["PRODUCT_VER"]
            tc_type_list  = area_config_map["LIST_TESTCASES"][i]["TEST_TYPE"]
            dut_type_list = area_config_map["LIST_TESTCASES"][i]["DEVICE_TYPE"]     
            rm_type_list  = area_config_map["LIST_TESTCASES"][i]["RM_TYPE"]  
            
            if tc_ts_map[i][2]==0 \
                and (device_model in area_config_map["LIST_TESTCASES"][i]["DEVICE_TYPE"]) \
                and (not aleos_sw_ver in area_config_map["LIST_TESTCASES"][i]["OBSOLETE_VER"])\
                and args.tc_type_arg in tc_type_list\
                and (not args.dut_type_arg or args.dut_type_arg in dut_type_list)\
                and (not args.rm_type_arg  or args.rm_type_arg  in rm_type_list) :
#                and (not args.prd_ver_arg  or args.prd_ver_arg  in prd_ver_list) \
                
                test_suite.addTest(tc_ts_map[i][0](tc_ts_map[i][1])) 
                tc_ts_map[i][2]=1
                print i, tc_ts_map[i][1]

    elif args.dut_type_arg:
       
        for i in range(1,total_tc+1):
            
#            prd_ver_list  = area_config_map["LIST_TESTCASES"][i]["PRODUCT_VER"]
#            tc_type_list  = area_config_map["LIST_TESTCASES"][i]["TEST_TYPE"]
            dut_type_list = area_config_map["LIST_TESTCASES"][i]["DEVICE_TYPE"]     
            rm_type_list  = area_config_map["LIST_TESTCASES"][i]["RM_TYPE"]  
            
            if tc_ts_map[i][2]==0 \
                and (device_model in area_config_map["LIST_TESTCASES"][i]["DEVICE_TYPE"]) \
                and (not aleos_sw_ver in area_config_map["LIST_TESTCASES"][i]["OBSOLETE_VER"])\
                and args.dut_type_arg in dut_type_list\
                and (not args.rm_type_arg  or args.rm_type_arg in rm_type_list) :
#                and (not args.prd_ver_arg  or args.prd_ver_arg in prd_ver_list) \
#                and (not args.tc_type_arg  or args.tc_type_arg in tc_type_list) \
                
                test_suite.addTest(tc_ts_map[i][0](tc_ts_map[i][1])) 
                tc_ts_map[i][2]=1
                print i, tc_ts_map[i][1]
                
    elif args.rm_type_arg:
       
        for i in range(1,total_tc+1):
            
#            prd_ver_list  = area_config_map["LIST_TESTCASES"][i]["PRODUCT_VER"]
#            tc_type_list  = area_config_map["LIST_TESTCASES"][i]["TEST_TYPE"]
#            dut_type_list = area_config_map["LIST_TESTCASES"][i]["DEVICE_TYPE"]     
            rm_type_list  = area_config_map["LIST_TESTCASES"][i]["RM_TYPE"]  
            
            if tc_ts_map[i][2]==0 \
                and (device_model in area_config_map["LIST_TESTCASES"][i]["DEVICE_TYPE"]) \
                and (not aleos_sw_ver in area_config_map["LIST_TESTCASES"][i]["OBSOLETE_VER"])\
                and args.rm_type_arg in rm_type_list:
#                and (not args.prd_ver_arg  or args.prd_ver_arg  in prd_ver_list) \
#                and (not args.tc_type_arg  or args.tc_type_arg  in tc_type_list) \
#                and (not args.dut_type_arg or args.dut_type_arg in dut_type_list) :
                
                test_suite.addTest(tc_ts_map[i][0](tc_ts_map[i][1])) 
                tc_ts_map[i][2]=1
                print i, tc_ts_map[i][1]
                
        
    return test_suite   

def cmd_stdout(command, argument, timeout=3):
    ''' TODO: can we not use text file?
    ARGS: 
        command  window  execuable or Lunix command
        argument arguments used in command
        timeout  timeout of the command execution 
    RETURNS:
        the output of the command execution 
    '''

    cmd = command +' ' + argument +'>ttt.txt'
    cslog(command +' ' + argument, "BLUE","WHITE")

    os.system(cmd)
    
    time.sleep(timeout)
    
    if os.path.getsize("ttt.txt") == 0: 
        return ""
    
    fh=open('ttt.txt','r')
    input_file = fh.read()
    fh.close()
    cslog(input_file, "BLUE","WHITE")

    return input_file

def cmd_stdout_last_line(command, argument, timeout=3):
    ''' TODO
    ARGS: 
        command  window  execuable or Lunix command
        argument arguments used in command
        timeout  timeout of the command execution 
    RETURNS:
        the last line of output of the command execution 
    '''

    cmd = command +' ' + argument +'>ttt.txt'
    cslog(command +' ' + argument, "BLUE","WHITE")

    os.system(cmd)
    
    time.sleep(timeout)
    
    if os.path.getsize("ttt.txt") == 0: 
        return ""
    
    fh=open('ttt.txt','r')
    for line in fh:
        pass
    fh.close()
    
    cslog(line, "BLUE","WHITE")

    return line


def get_report_url(tbd_config_map, test_area, report_filename):
    '''   Get report url    
    Args:
             tbd_config_map:  test bed configuration list 
             test_area: the feature area of this test
             report_filename  string, report file name 
    Returns: report_url
    '''     
    report_url ="http://"+tbd_config_map["JENKINS"]["MASTER_ADDRESS"]+"/automation/results/temp/"+test_area+'/'+report_filename
    return report_url

def upload_report(tbd_config_map, test_area,report_filename):
    '''   Upload the report file to FTP server    
    Args:
             tbd_config_map:  test bed configuration list 
             test_area: the feature area of this test
             report_filename  string, report file name
    Returns: result: True/False  Upload success or not
    ''' 
    result = True
    ftp_path = '/results/temp/'+test_area+'/'
    
    try:
        
        ftp = ftplib.FTP(tbd_config_map["JENKINS"]["MASTER_ADDRESS"], tbd_config_map["JENKINS"]["USERNAME"], tbd_config_map["JENKINS"]["PASSWORD"])
        fp = open(report_filename,'rb')
        ftp.cwd(ftp_path)
        ftp.storbinary('STOR '+ report_filename, fp)        
        fp.close()
        ftp.close()
    except Exception:
        result = False
    
    return result

def make_csv(csv_file_path, test_result, area_config_map):
    '''   Generating the csv file    
    Args:
             csv_file_path: the feature area of this test
             test_result: result list from completed tests
             area_config_map: 
    Returns: result: True/False  generate csv success or not
    '''
    result = True
    current_date_str = str(datetime.datetime.now().date())
    current_time_str = str(datetime.datetime.now().time()).replace(":","-")
    
    #csv filename format, To be discussed
    csv_filename =csv_file_path+"test_"+current_date_str+"_"+current_time_str+".csv"
    try:
        csvfpp = open(csv_filename,'wb')
        col_string = "ID,RESULT,NOTES,ATM_PRLINK"+'\n'
        csvfpp.writelines(col_string)
        result_lst = test_result.result
        for i in range(0,len(result_lst)):
            if test_result.result[i][0] == 0:
                result_stat = "pass"
            elif test_result.result[i][0] == 1:
                result_stat = "fail"
            else:
                result_stat = "fail"        
            #For the Note, we can modifiy the output depands on the test result
            csvfpp.writelines(area_config_map["LIST_TESTCASES"][i+1]["TC_ID"]+','+result_stat+','+"Note "+str(i)+'\n')
        csvfpp.close()
    except Exception:
        result = False
    
    return result