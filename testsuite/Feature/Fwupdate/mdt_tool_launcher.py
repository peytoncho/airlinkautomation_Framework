import mdt_airlink
import at_utilities
import basic_airlink
import telnet_airlink
import os
import time
test_area = "Fwupdate"
test_sub_area=""
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME']
basic_airlink.append_sys_path()
tbd_config_map, fwupdate_config_map = basic_airlink.get_config_data(test_area,"")


def restore_device_ip():
    device_num = fwupdate_config_map["DEVICE_NUMBER"]
    at_ins = at_utilities.AtCommands()
        
    for i in range(device_num):
        attempt_time = 0
        curr_ip = '192.168.13.'+str(i+1)
        change_ip = '192.168.13.31'
        telnet_ins = telnet_airlink.TelnetAirlink(hostname = curr_ip)
        print curr_ip
        while (not telnet_ins.connect()) and attempt_time<=20:
            print('connection fail')
            print str(attempt_time)
            attempt_time+=1
            
        if attempt_time<=20:
            at_ins.set_ethernet_device_ip(telnet_ins, change_ip)
            at_ins.atz_reboot(telnet_ins)    
            time.sleep(5)
        else:
            print "No device with IP "+ curr_ip
    print("DONE!")
    
    
if __name__ == '__main__':
#    mdt_ins = mdt_airlink.MdtAirlink(3)
#    mdt_ins.change_all_device_ip()
    restore_device_ip()
    