from ssh_airlink import SshAirlink 
import io
import os
import time
import sys, getopt

def dump_log_file():
    time_range = 0
    time_flag = False
    all_flag = False
    word_flag = False
    word = None
    i = 0
    try:
      opts, args = getopt.getopt(sys.argv[1:],"at:w:",["time=","word="])
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
            word_flag = True
            word = arg
   
    if time_flag:
        while time_flag:
            i+=1
            sys.stdout.write("Check ALEOS log after: "+time_range+" minute(s)\n")
            time.sleep(float(time_range)*60)
            if all_flag:
                write_logs()
            elif word_flag and not word is None:
                write_logs(word=word)
            
    else:
        if all_flag:
            write_logs()
        elif word_flag and not word is None:
            write_logs(word=word)
    print "Done"

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

if __name__ == "__main__":
    dump_log_file()