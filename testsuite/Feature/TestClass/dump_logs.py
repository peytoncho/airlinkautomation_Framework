from ssh_airlink import SshAirlink 
import io
import time
import sys, getopt

def dump_log_file():
    time_range = 0
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
        elif opt == '-a':
            all_flag = True       
        elif opt == '-w':
            word_flag = True
            word = arg
    
    while True:
        i+=1
        print "Start to dump logs: "+str(i)
        time.sleep(float(time_range)*60)
        if all_flag is True:
            write_logs()
        elif word_flag is True and not word is None:
            write_logs(word=word)
        print "Done"

def write_logs(word=None):
    ssh = SshAirlink(hostname='192.168.13.4')
    messages = ['messages','messages.0','messages.1','messages.2','messages.3','messages.4']
    if not ssh.connect():
        return None
    fp = file(time_stamp()+'logmsg.txt','a')
    fp.flush()
    for filename in messages:
        output = ssh.command("cat ../mnt/hda1/junxion/log/%s"%filename)
        if not output is None:
            for line in output:
                if (not word is None) and (word in line): 
                    fp.write(filename+" :"+line)  
                elif word==None:
                    fp.write(filename+" :"+line)
        else:
            return None
    fp.close()
    ssh.close()
    return "Done"

def time_stamp():
    time_stamp = time_stamp = time.strftime("%Y-%b-%d_%H-%M-%S_")
    return time_stamp

if __name__ == "__main__":
    dump_log_file()