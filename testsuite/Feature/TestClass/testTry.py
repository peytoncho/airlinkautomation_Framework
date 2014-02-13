from __future__ import print_function
import csv
import at_utilities
import telnet_airlink
import time


def restore_device_ip():
    
    at_ins = at_utilities.AtCommands()
    
    for i in range(5):
        print("Change"+str(i+1)+"device")
        result = ""
        curr_ip = "192.168.13."+str(i+1)
        telnet_ins = telnet_airlink.TelnetAirlink(hostname = curr_ip)
        while not telnet_ins.connect():
            print('connection fail')
        
        print(at_ins.get_device_model(telnet_ins))
        while not result is True:    
            result = at_ins.set_ethernet_device_ip(telnet_ins, "192.168.13.31")
        
        at_ins.atz_reboot(telnet_ins)
        print("Reboot...")
        time.sleep(10)

def change_device_ip(func):
    at_ins = at_utilities.AtCommands()
    
    for i in range(5):
        result = ""
        if func == 'start':
            curr_ip = "192.168.13.31"
            change_ip = "192.168.13."+str(i+1)
        else:
            curr_ip = "192.168.13."+str(i+1)
            change_ip = "192.168.13.31"
        telnet_ins = telnet_airlink.TelnetAirlink(hostname = curr_ip)
        while not telnet_ins.connect():
            print('connection fail')
        
        print(at_ins.get_device_model(telnet_ins))
        while not result is True:    
            result = at_ins.set_ethernet_device_ip(telnet_ins, change_ip)
        
        at_ins.atz_reboot(telnet_ins)
        print("Reboot...")
        time.sleep(10)    
        

def get_device_ip_list():
    at_ins = at_utilities.AtCommands()
    for i in range(5):
        change_ip = "192.168.13."+str(i+1)
        telnet_ins = telnet_airlink.TelnetAirlink(hostname = curr_ip)
        
        
        

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
    restore_device_ip()

    
    
    
    
    
    
    