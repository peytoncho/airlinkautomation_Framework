from ssh_airlink import SshAirlink 
import io
import glob, os
import time
import sys, getopt

def dump_log_file():
    
    time_range = 0
    time_flag = False
    all_flag  = False
    word_flag = False
    word = None
    i = 0
    msg = "Done"
    try:
      opts, args = getopt.getopt(sys.argv[1:],"at:w:f",["time=","word="])
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
               
    if time_flag:
        if not cleanup_files():
            return 
        while time_flag:
            i+=1
            sys.stdout.write("Check ALEOS log after: "+time_range+" minute(s)\n")
            time.sleep(float(time_range)*60)
            if word_flag and not word is None:
                write_logs(word=word)
                print "Dump log message contains word :"+word
            else:
                write_logs()
                print "Dump all log message"                
            
    else:
        if all_flag:
            if not cleanup_files():
                return
            write_logs()
            msg = "Dump all log message"
        elif word_flag and not word is None:
            get_info(word=word)
#            msg = "Dump log message contains word :"+word
        else:
            msg = "Help:\n\
            -a: Dump all log message from ACEManager\n\
            -t: Define time range to dump the log (in minute)\n\
            -w: Define keyword when dumping the log or in dumped txt log file"
    print msg

def cleanup_files():
    clean_flag = False
    confirm = raw_input("Continue to clean log file? (Y/N)")
    confirm_lst = ['Y','N','y','n']    
    while not confirm in confirm_lst:
        print "Please input Y or N..."
        confirm = raw_input("Continue to clean log file? (Y/N)")
   
    if confirm is "Y" or confirm is "y":
        os.chdir("./dump_data/dump_log/")
        filelist = glob.glob("*.txt")
        for f in filelist:
            os.remove(f)
        print "Clean up the folder..."
        clean_flag = True
    elif confirm is "N" or confirm is "n":
        print "Cancelled clean up..."
    
    return clean_flag

def write_logs(word=None):    
    ssh = SshAirlink(hostname='192.168.13.31')
#    cleanup_files()
    messages = ['messages','messages.0','messages.1','messages.2','messages.3','messages.4']
    
    
    for i in range(3):
        if ssh.connect():
            break
        else:
            time.sleep(60)
    
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
#                os.chdir("./dump_data/dump_log/")
                fp = file(log_filename,'a')
                file_exist_flag = True
            for line in output:                               
                fp.write(line)
    if file_exist_flag:
        fp.close()
    
    ssh.close()
    return "Done"

def time_stamp():
    time_stamp = time_stamp = time.strftime("%Y-%b-%d_%H-%M-%S")
    return time_stamp

def get_info(word=None):
#    print "Find \""+word+"\" in the dumped log file \""+logfile+"\""
    getinfo_filename = time_stamp()+'_getinfo.txt'
    pick_lst = []
    os.chdir('./dump_data/dump_log/')
    filelist = glob.glob("*.txt")
    for logfile in filelist:
        with open(logfile) as f:
            content = f.readlines()        
        if not word is None: 
            for i in content:
                if word in i:
                    if not i in pick_lst:
                        pick_lst.append(i)
    
    os.chdir('../parsed_logmsg/')   
    if len(pick_lst) == 0:
        msg = "Not found the word in the log file"        
    else:
        with open(getinfo_filename, 'a') as f1:
            f1.writelines(pick_lst)
        msg = "File is created"

    print msg

 
if __name__ == "__main__":
    dump_log_file()
#    get_info('2014-Jan-29_09-54-16_logmsg.txt',"dnsmasq-dhcp")