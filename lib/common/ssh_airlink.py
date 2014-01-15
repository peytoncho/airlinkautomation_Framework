import logging
import paramiko
from paramiko.ssh_exception import SSHException
import inspect

class SshAirlink:
    """SshAirlink provides a SSH connection with default connection parameters.
    
    Attributes:
    hostname: Host ip address. Default ip is 192.168.13.31.
    port: Port connection number. Default port number is 22.
    username: Host username. Default username is root.
    password: Connection password. Default is v3r1fym3.
    """

    def __init__(self, hostname="192.168.13.31", port="22",\
		username="root", password="v3r1fym3"):
        """Initializes the connection parameters.
        
        Args:
        hostname: Host ip address. Default ip is 192.168.13.31.
        port: Port connection number. Default port number is 22.
        username: Host username. Default username is root.
        password: Connection password. Default is v3r1fym3.
        
        Returns:
        No returns.
        """
        self.hostname = hostname
        self.port = int(port)
        self.username = username
        self.password = password
        
    def connect(self):
        """Initiates a SSH connection by using parmiko.SSHClient module.
    
        Args:
        No args. 

        Returns:
        True: If the connection set up successfully.
        False: If the connection set up failed.
        """
        logging.info("connecting")
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=self.hostname, port=self.port,\
				username=self.username, password=self.password)
            
        except Exception, e:
            logging.critical('*** Caught exception: %s: %s' % (e.__class__, e))
            logging.critical("connection failed")
            return False
            
        return True

        
    def command(self, cmd):
        """ Sends a command to the host and returns the response.
        
        Args:
        The cmd is a string without the newline, "\\n", and contains the
        command. 

        Returns:
        It returns None if the command is not correct.
        Otherwise, it returns a list of strings that each string is
		terminated with a newline character.
        """
        logging.info("executing " + cmd)
        try:
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            
        except SSHException:
            logging.debug("unable to execute command")
            return None
        
        except:
            logging.debug("unexpected exception in (" + inspect.stack()[0][3] + ")")
            return None
        
        stdout_list = stdout.readlines()
        stderr_list = stderr.readlines()
        
        if stderr_list:
            logging.warning("bad command:" + "".join(stderr_list))
            return None

        return stdout_list
        
    
    def close(self):
        """Close the SSH connection.
        It is very important to close the connection before exiting the scripts.

        Args:
        No args. 

        Returns:
        No returns.
        """
        logging.info("closing connection")
        self.ssh.close()
