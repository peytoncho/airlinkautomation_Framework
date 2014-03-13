from ssh_airlink import SshAirlink
import selenium_utilities_minor as s
import sys, getopt
import os
import time


def dump_mem_info(times):
    ssh = SshAirlink(hostname="192.168.13.31")
    for i in range(3):
        if ssh.connect():
            break
        else:
            time.sleep(60)
            
    output_1 = ssh.command("ip route")
    output_2 = ssh.command("free -m")
    output_3 = ssh.command("top -n1")
    os.chdir("./logs/")
    time_stamp_str = time_stamp = time.strftime("%Y-%b-%d")
    log_filename = time_stamp_str+'_logmsg.txt'
    print time_stamp_str+": File created, Please Check"
    with open(log_filename,"a") as fp:
        fp.write("\n############################ Time "+times+" ############################\n")
        fp.write("========>$: ip route\n")
        for line in output_1:
            fp.write(line)
        
        fp.write("\n========>$: free -m\n")   
        for line in output_2:
            fp.write(line)
        
        fp.write("\n========>$: top -n1\n") 
        for line in output_3:
            fp.write(line)
    os.chdir("../")

def run():
    try:
      opts, args = getopt.getopt(sys.argv[1:],"n:",["time="])
    except getopt.GetoptError:
      print 'get arguments error'
      sys.exit(2)
      
    #default actions times  
    action_times = 5
    for opt,arg in opts:
        if opt == "-n":
            action_times = arg
    print action_times 
    url = "HTTP://192.168.13.31:9191"
    username = "user"
    password = "12345"
    driver = s.login(url,username,password)
#    driver.close()
    s.navigate_wan_dmnr(driver)
    n=0
    while True:
        print "This is "+str(n)
        if n%2==0:
            s.enable_dmnr(driver)
        else:
            s.disable_dmnr(driver)
        s.apply(driver)
        n+=1
        if n%int(action_times) == 0:
            dump_mem_info(str(n))

    driver.close()
    print "Done!"

if __name__ == '__main__':
    run()

        