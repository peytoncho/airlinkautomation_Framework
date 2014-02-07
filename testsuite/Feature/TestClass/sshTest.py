import basic_airlink
import ssh_airlink

def dummy():
    ssh = SshAirlink("192.168.13.31","22","user","12345")
    ssh.connect()
    
    shell = ssh.ssh.invoke_shell()
    
    while True:
        if shell.recv_ready():
            buf = shell.recv(0XFFFF)
            basic_airlink.clog(buf)
            shell.send("ATI1\r")
            basic_airlink.clog(shell.recv(0XFFFF))


dummy()