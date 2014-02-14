from __future__ import print_function
import csv
import at_utilities
import telnet_airlink
import time


def retrive_global_ip():
    
    at_ins = at_utilities.AtCommands()
    globalid_lst = []
    
    while len(globalid_lst)<5:
        result = ""
        curr_ip = "192.168.13.31"
        telnet_ins = telnet_airlink.TelnetAirlink(hostname = curr_ip)
        while True:
            try:
                while not telnet_ins.connect():
                    print('connection fail')
                 
                global_id = at_ins.get_global_id(telnet_ins)
                if not global_id in globalid_lst: 
                    globalid_lst.append(global_id)
                 
                lst_index = globalid_lst.index(global_id)
                change_ip = '192.168.13.'+str(lst_index+1)
                     
                at_ins.set_ethernet_device_ip(telnet_ins, change_ip)
                at_ins.atz_reboot(telnet_ins)
                 
#                telnet_ins.close()
                time.sleep(15)
            except:               
                continue
             
            break

        print(globalid_lst)
        
def repeat_reboot():
    at_ins = at_utilities.AtCommands()
    i=20
    while i>0:
        curr_ip = "192.168.13.31"
        telnet_ins = telnet_airlink.TelnetAirlink(hostname = curr_ip)
        i=i-1
        while True:
            try:
                while not telnet_ins.connect():
                    print('connection fail')
                time.sleep(20)
                at_ins.atz_reboot(telnet_ins)
                
                time.sleep(30)
                
            except:               
                continue
            break        
        

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
        
        
        
        
        
        

def getcsvHeader(csvfile):
    header = ""
    fp = open(csvfile)
    for i, line in enumerate(fp):
        if i < 12:
            header = header+str(line)
    fp.close()
    return header

def readcsv():
    with open('test.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter = ",")
        flag = False
        mydict = dict()
        for row in reader:
            if len(row)>=10:
                for i in range(0,len(row)-1):
                    if row[i] == 'Test Case':
                        flag = True
                if flag == True:
                    mydict[row[0]] = row[1:]

    return mydict


def changeResult(dics,key,value):
    dics[key][0] = value
    return dics




def writecsv(dics):
    csv1file = open('test1.csv','wb')
    header = getcsvHeader('test.csv')
    print(header, file=csv1file)
    content = ""
    item_lst = dics.items()
    for i in range(0,len(item_lst)):
        nextline = ''
        content = content+'"'+item_lst[i][0]+'"'
        for j in range(0,len(item_lst[i][1])):
            if j == 8:
                nextline = '\n'
            content = content+','+'"'+item_lst[i][1][j]+'"'+nextline
    
    print(content, file=csv1file)
     
    csv1file.close()

if __name__ == "__main__":
#     get_device_ip_list()
#    retrive_global_ip()
#   repeat_reboot()  
    get_device_ip_list()
    
    
    
    
    