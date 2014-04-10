import at_utilities
import basic_airlink
import telnet_airlink
import sys, getopt
import os
import time
test_area = "Fwupdate"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME']
basic_airlink.append_sys_path()
tbd_config_map, fwupdate_config_map = basic_airlink.get_config_data(test_area,"")

def restore_device_ip(start_point=1, repeat_time=10):
    device_num = fwupdate_config_map["DEVICE_NUMBER"]
    at_ins = at_utilities.AtCommands()
    print "Check IP start from 192.168.13."+str(start_point) +" to 192.168.13."+str(device_num)
    print "Repeat " +str(repeat_time)+" times"
    time.sleep(4)
    for i in range(int(start_point),device_num+1):
        attempt_time = 1
        curr_ip = '192.168.13.'+str(i)
        change_ip = '192.168.13.31'
        telnet_ins = telnet_airlink.TelnetAirlink(hostname = curr_ip)
        print '\n'+curr_ip
        while (not telnet_ins.connect()) and attempt_time<int(repeat_time):
#            print str(attempt_time)
            attempt_time+=1
            
        if attempt_time<int(repeat_time):
            at_ins.set_ethernet_device_ip(telnet_ins, change_ip)
            at_ins.atz_reboot(telnet_ins) 
            time.sleep(15)
            print "IP changed, wait 15 seconds..."   
        else:
            print "No device with IP "+ curr_ip
    
    print("\nDONE! Please wait the device up if it is rebooting ")

def run():
    start_point_flag = False
    repeat_flag = False
    help_flag = False
    try:
      opts, args = getopt.getopt(sys.argv[1:],"s:r:h",["start=","repeat="])
    except getopt.GetoptError:
      print 'get arguments error'
      sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-s':
            start_point = arg
            start_point_flag = True
        elif opt == '-r':
            repeat_time = arg  
            repeat_flag = True
        elif opt == '-h':
            help_flag = True
    
    if not help_flag:
        if start_point_flag and repeat_flag:
            restore_device_ip(start_point = start_point, repeat_time = repeat_time)
        elif (not start_point_flag) and repeat_flag:
            restore_device_ip(repeat_time = repeat_time)
        elif start_point_flag and (not repeat_flag):
            restore_device_ip(start_point = start_point)
        else:
            restore_device_ip()
    else:
        msg = "Help:\n\
        -s: Identify a start point of IP to check which device has changed IP\n\
        -r: Define the repeat time of connection attempt to each IP\n\
        -h: Help info"
        print msg
        
if __name__ == '__main__':
#    mdt_ins = mdt_airlink.MdtAirlink(3)
#    mdt_ins.change_all_device_ip()
    run()
    