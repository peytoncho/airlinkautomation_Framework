# import paramiko
# 
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect("192.168.13.31", 22, "user", "12345")
# stdin, stdout, stderr = ssh.exec_command('ati1')
# 
# print stdout.readlines()

import pexpect

ssh_new_key = "Are you sure you want to continue connecting"

cmd_connect = "ssh -p22 %s@%s" % ("user", "192.168.13.31")

try:

    p = pexpect.spawn(cmd_connect)
    i = p.expect([ssh_new_key, 'asswor'])

    if i == 0:
        p.send('yes\r')
        i = p.expect([ssh_newkey, 'assword:'])

    if i == 1:
        p.send("12345")

except Exception, exp:  
    print "Could not connect to %s with account %s" % (host, account_name)