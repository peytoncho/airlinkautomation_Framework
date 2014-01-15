from __future__ import print_function
import csv

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
    dics = readcsv()
    key1 = "LinALEOS/ACEmanager_functions/FF_XP/LAN_Access_by_Interface/Ethernet_in_Public_mode"
    key2 = "LinALEOS/ACEmanager_functions/FF_XP/ACEmanager_local_access-IPv6"
    key3 = "LinALEOS/ACEmanager_functions/FF_XP/Templates/Download_a_comprehensive_Template"
    val1 = "pass"
    val2 = "pass"
    val3 = "pass"
     
    changeResult(dics,key1,val1)
    changeResult(dics,key2,val2)
    changeResult(dics,key3,val3)
     
    writecsv(dics)
    

    
    
    
    
    
    
    