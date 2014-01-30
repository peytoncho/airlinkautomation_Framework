from ssh_airlink import SshAirlink 
import io
import os
import time
import sys, getopt

def dump_log_file():
    time_range = 0
    time_flag = False
    all_flag  = False
    word_flag = False
    file_flag = False
    word = None
    filename = None
    i = 0
    msg = "Done"
    try:
      opts, args = getopt.getopt(sys.argv[1:],"at:w:f:",["time=","word=","file="])
    except getopt.GetoptError:
      print 'get arguments error'
      sys.exit(2)
    
    for opt,arg in opts:
        if opt == '-t':
            time_range = arg
            time_flag = True
        elif opt == '-a':
            all_flag = True       
        elif opt == '-w':
            word = arg
            word_flag = True
        elif opt == '-f':
            filename = arg
            file_flag = True
               
    if time_flag:
        while time_flag:
            i+=1
            sys.stdout.write("Check ALEOS log after: "+time_range+" minute(s)\n")
            time.sleep(float(time_range)*60)
            if all_flag:
                write_logs()
                print "Dump all log message"
            elif word_flag and not word is None:
                write_logs(word=word)
                print "Dump log message contains word :"+word
            
    else:
        if all_flag:
            write_logs()
            msg = "Dump all log message"
        elif word_flag and not word is None and (not file_flag):
            write_logs(word=word)
            msg = "Dump log message contains word :"+word
        elif word_flag and not word is None and file_flag and not filename is None:
            get_info(filename,word=word) 
        elif file_flag and not word_flag:
            msg = "Please pass the key word you want to find in log message"
    print msg

def write_logs(word=None):
    ssh = SshAirlink(hostname='192.168.13.3')
    messages = ['messages','messages.0','messages.1','messages.2','messages.3','messages.4']
    
    if not ssh.connect():
        return None
    
    file_exist_flag = False
        
    for filename in messages:
        if word is None:
            output = ssh.command("cat ../mnt/hda1/junxion/log/%s"%filename)
        else:
            output = ssh.command("cat ../mnt/hda1/junxion/log/"+filename+"| grep \"%s\"" %(word))     
        if len(output)!=0 :
            if not file_exist_flag:
                time_stamp_str = time_stamp()
                log_filename = time_stamp_str+'_logmsg.txt'
                print time_stamp_str+": File created, Please Check"
                os.chdir("./dump_data/dump_log/")
                fp = file(log_filename,'a')
                file_exist_flag = True
            for line in output:                               
                fp.write(filename+" :"+line)
    if file_exist_flag:
        fp.close()
    
    ssh.close()
    return "Done"

def time_stamp():
    time_stamp = time_stamp = time.strftime("%Y-%b-%d_%H-%M-%S")
    return time_stamp

def get_info(logfile, word=None):
    print "Find \""+word+"\" in the dumped log file \""+logfile+"\""
    pick_lst = []
    os.chdir('./dump_data/dump_log/')
    with open(logfile) as f:
        content = f.readlines()
       
    os.chdir('../parsed_logmsg/')
    if not word is None: 
        for i in content:
            if word in i:
                pick_lst.append(i)
        
        if len(pick_lst) == 0:
            msg = "Not found the word in the log file"        
        else:
            with open(time_stamp()+'_getinfo.txt', 'a') as f1:
                f1.writelines(pick_lst)
            msg = "File is created"
    
    print msg

 
if __name__ == "__main__":
    dump_log_file()
#    get_info('2014-Jan-29_09-54-16_logmsg.txt',"dnsmasq-dhcp")