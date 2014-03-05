import at_utilities
import telnet_airlink
import selenium_utilities
import os
import time

DEVICE_NUMBER = 5
RETRY_TIMES = 20

se_ins = selenium_utilities.SeleniumAcemanager()
globalid_lst = []

def change_global_ip():
    se_ins = selenium_utilities.SeleniumAcemanager()
    at_ins = at_utilities.AtCommands()
    globalid_lst = []
    reboot_fail_lst = []
    retry_counter = 0
        
    while len(globalid_lst)<DEVICE_NUMBER or len(reboot_fail_lst)>0:
        result = ""
        curr_ip = "192.168.13.31"
        telnet_ins = telnet_airlink.TelnetAirlink(hostname = curr_ip)
        while retry_counter<=RETRY_TIMES:
            try:
                while not telnet_ins.connect():
                    print('connection fail')
                global_id = at_ins.get_global_id(telnet_ins)
                if (not global_id in globalid_lst) and (len(global_id)>10): 
                    globalid_lst.append(global_id)
                 
                lst_index = globalid_lst.index(global_id)
                change_ip = '192.168.13.'+str(lst_index+1)
                                     
                at_ins.set_ethernet_device_ip(telnet_ins, change_ip)
            except:
                retry_counter+=1               
                continue
            
            try:    
                if not at_ins.atz_reboot(telnet_ins):
                    if not global_id in reboot_fail_lst:
                        reboot_fail_lst.append(global_id)
                        print("Append "+global_id+" to reboot list")
                else:
                    if global_id in reboot_fail_lst:
                        reboot_fail_lst.remove(global_id)
                        print("Remove "+global_id+" to reboot list")

                
            except:
                if not global_id in reboot_fail_lst:
                        reboot_fail_lst.append(global_id)
                        print("exp:Append "+global_id+" to reboot list")                              
                continue
            retry_counter = 0
            break
        
        if retry_counter > RETRY_TIMES:     
            print "retry done, UI change IP ..... "
            retry_counter = 0
            operated_global_id = ui_change_ip(se_ins,globalid_lst)
            if operated_global_id in reboot_fail_lst:
                reboot_fail_lst.remove(operated_global_id)
        
        print(globalid_lst)
        time.sleep(15)
    print "Change IP Done!!...Wait for device reboot..."
    return len(globalid_lst)


    


def ping_devices():
#    for i in range(device_number):
    device_ip = '192.168.13.31'
    ret = os.system('ping '+device_ip)
    print ret

def restore_device_ip():
    at_ins = at_utilities.AtCommands()
    
    for i in range(DEVICE_NUMBER):
        curr_ip = '192.168.13.'+str(i+1)
        change_ip = '192.168.13.31'
        telnet_ins = telnet_airlink.TelnetAirlink(hostname = curr_ip)
        while not telnet_ins.connect():
            print('connection fail')
        at_ins.set_ethernet_device_ip(telnet_ins, change_ip)
        at_ins.atz_reboot(telnet_ins)
        
        time.sleep(15)
     
    print("DONE!")

def ui_change_ip(selenium_instance,global_id_list):
    retry_counter = 0
    seccess_flag = False
    while retry_counter <= RETRY_TIMES and seccess_flag == False:
       
        driver = selenium_instance.login('http://192.168.13.31:9191','user','12345')
        global_id = selenium_instance.get_global_id(driver)
        
        if global_id == '':
            continue
        
        if not global_id in global_id_list:
            global_id_list.append(global_id)
            global_id_index = global_id_list.index(global_id)
        else:
            global_id_index = global_id_list.index(global_id)
        if not selenium_instance.set_device_ip(driver, "192.168.13."+str(global_id_index+1)):
            retry_counter+=1
            driver.close()
            continue           
    #        selenium_instance.set_device_ip(driver, "192.168.13.31")
        selenium_instance.apply_reboot(driver)
            
        time.sleep(5)
        driver.close()
        seccess_flag = True
    
    return global_id

     
def get_device_ip_list():
    at_ins = at_utilities.AtCommands()
    info_lst = []
    for i in range(DEVICE_NUMBER):
        change_ip = "192.168.13."+str(i+1)
        telnet_ins = telnet_airlink.TelnetAirlink(hostname = change_ip)
        
        while not telnet_ins.connect():
            print("connection fail, retry...")
        device_name = at_ins.get_device_model(telnet_ins)
        device_rm = at_ins.get_rm_name(telnet_ins)
        device_info = device_name+'_'+device_rm
        
        info_lst.append(change_ip+' : '+device_info)
        telnet_ins.close()
           
    for line in info_lst:
        print(line)

#ui_change_ip(se_ins,globalid_lst)
restore_device_ip()
time.sleep(40)
change_global_ip()
time.sleep(40)
get_device_ip_list()
#ping_devices()
