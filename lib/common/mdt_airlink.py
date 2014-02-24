import at_utilities
import telnet_airlink

DEVICE_NUMBER = 5

def retrive_global_ip():
    
    at_ins = at_utilities.AtCommands()
    globalid_lst = []
    reboot_fail_lst = []
        
    while len(globalid_lst)<DEVICE_NUMBER:
        result = ""
        curr_ip = "192.168.13.31"
        telnet_ins = telnet_airlink.TelnetAirlink(hostname = curr_ip)
        while True:
            try:
                while not telnet_ins.connect():
                    print('connection fail')
                 
                global_id = at_ins.get_global_id(telnet_ins)
                if (not global_id in globalid_lst) and (len(global_id)>10): 
                    globalid_lst.append(global_id)
                 
                lst_index = globalid_lst.index(global_id)
                change_ip = '192.168.13.'+str(lst_index+1)
                     
                at_ins.set_ethernet_device_ip(telnet_ins, change_ip)
                
                if not at_ins.atz_reboot(telnet_ins):
                    if not global_id in reboot_fail_lst:
                        reboot_fail_lst.append(global_id)
                        print("Append "+global_id+" to reboot list")
                else:
                    if global_id in reboot_fail_lst:
                        reboot_fail_lst.remove(global_id)
                        print("Remove "+global_id+" to reboot list")

#                telnet_ins.close()
                time.sleep(15)
            except:               
                continue
             
            break

        print(globalid_lst)



def restore_device_ip():
    at_ins = at_utilities.AtCommands()
    
    for i in range(5):
        curr_ip = '192.168.13.'+str(i+1)
        change_ip = '192.168.13.31'
        telnet_ins = telnet_airlink.TelnetAirlink(hostname = curr_ip)
        while not telnet_ins.connect():
            print('connection fail')
        at_ins.set_ethernet_device_ip(telnet_ins, change_ip)
        at_ins.atz_reboot(telnet_ins)
        
        time.sleep(15)
     
    print("DONE!")
    
    
def get_device_ip_list():
    at_ins = at_utilities.AtCommands()
    info_lst = []
    for i in range(5):
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