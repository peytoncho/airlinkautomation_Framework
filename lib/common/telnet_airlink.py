import telnetlib
import logging
import time
import sys
import inspect

class TelnetAirlink:
    """TelnetAirlink class provides a simple telnet connection with default
	connection parameters. In this class all timeout exception are caught to
	prevent termination.
    
    Attributes:
        hostname: Host ip address. Default ip is 192.168.13.31.
        port: Port connection number. Default port number is 2332.
        username: Host username. Default username is user. If the connection is
		username-less, pass an empty string as username.
        password: Connection password. Default is 12345. If the connection is
		password-less, pass an empty string as password.
        debug_mode: Enables the debug mode. Default is True. If it is True, all
		sent and received data are printed out in terminal.
        timeout: The timeout is second. Default timeout is 3 seconds.
    """
    def __init__(self, hostname = "192.168.13.31", port = "2332",\
		username = "user", password = "12345", debug_mode = True, timeout = 3):
        """Initializes the connection parameters.
        
        Args:
            hostname: Host ip address. Default ip is 192.168.13.31.
            port: Port connection number. Default port number is 2332.
            username: Host username. Default username is user. If the connection
			is username-less, pass an empty string as username.
            password: Connection password. Default is 12345. If the connection
			is password-less, pass an empty string as password.
            debug_mode: Enables the debug mode. Default is True. If it is True,
			all sent and received data are printed out in terminal.
            timeout: The timeout is second. Default timeout is 3 seconds.
        
        Returns:
            No returns.
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.debug_mode = debug_mode
        self.timeout = timeout
        
        logging.debug("telnet parameters are initialized")
   
    def connect(self):
        """Initiates a telnet connection by using telnetlib module.
        
        Args:
            No args. 

        Returns:
            True: If the connection set up successfully.
            False: If the connection set up failed.
        """
        logging.info("connecting")
        try:
            self.tn = telnetlib.Telnet(self.hostname, self.port, self.timeout)
            
        except:
            logging.error("incorrect hostname or port number")
            return False

        self.tn.set_debuglevel(self.debug_mode)
        self.tn.msg(logging)
        
        if len(self.username):
            
            if self.read_until_safe("login: "):
                self.tn.write(self.username + "\n")
                
            else:
                logging.error("login time out")
                self.tn.close()
                return False
        
        if len(self.password):

            if self.read_until_safe("Password: "):
                self.tn.write(self.password + "\n")

            else:
                logging.error("password time out")
                self.tn.close()
                return False

        return True

    def command(self, cmd):
        """Sends a command to the device and waits till timeout expires.

        Args:
            The cmd is a string without the newline character and contains the
			command. 

        Returns:
            It returns a list of strings that each string is terminated with a
			newline character.
            If the returned list is empty it most probably means that the device
			is not connected. 
        """
        logging.info("sending command " + cmd)
        self.tn.write(cmd + "\n")

        rcved_list = []
        keep_catching = True
        while keep_catching:

            rcv = self.expect_safe(["\n"])
            if rcv[0] == 0:
                rcved_list.append(rcv[2])
                
            else:
                keep_catching = False

        return rcved_list

    def expect_safe(self, expected_keys):
        """expect_safe is the same as expect method, already implemented in
		telnetlib, with the capability of handling exceptions.

        Args:
            expected_keys: This is a list of expected keys (regular expression).
			For more information refer to expect method in telnetlib. 

        Returns:
            It returns a tuple.
            The first element is the first matched element in the expected_keys.
			In case of timeout (not matched), it returns -1.
            The second element is the matched object (refer to telnetlib module
			document).
            The third element is the received string till expected key.
        """
        try:
            rcv = self.tn.expect(expected_keys)
            return rcv

        except EOFError:
            logging.info("telnet time out in (" + inspect.stack()[0][3] + ")")
            
        except:
            logging.info("unexpected exception in (" + inspect.stack()[0][3] + ")")
        
        return (-1, None, "")

    def read_until_safe(self, expected_key):
        """read_until_safe is the same as read_until method, already implemented
		in telnetlib, with the capability of handling exceptions.

        Args:
            expected_key: This is a string of expected key. For more information
			refer to read_until method in telnetlib. 

        Returns:
            It returns the received string.
            In case of timeout, it most probably return an empty string.
        """
        rcv = ""
        try:
            rcv = self.tn.read_until(expected_key)
            
        except EOFError:
            logging.info("telnet time out in (" + inspect.stack()[0][3] + ")")
            
        except:
            logging.info("unexpected exception in (" + inspect.stack()[0][3] + ")")

        return rcv
        
    def close(self):
        """Closes the telnet connection.
        
        Args:
            None
        
        Returns:
            None
        
        """
        self.tn.close()
