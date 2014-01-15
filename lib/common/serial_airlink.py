import serial
import logging

class SerialAirlink:
    """SerialAirlink provides a serial connection with default connection
    parameters.
    
    Attributes:
    comport: Serial port name. Default port name is "COM3".
    baudrate: Default baudrate is 115200.
    timeout: Default timeout is 3 seconds.
    """

    def __init__(self, comport = "COM1", baudrate = 115200, timeout = 3):
        '''Initializes the connection parameters.
        
        Args:
        comport: Serial port name. Default port name is "COM3".
        baudrate: Default baudrate is 115200.
        timeout: Default timeout is 3 seconds.
        
        Returns:
        No returns.
        '''
    
        
        self.comport = comport
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None

        
    def connect (self):
        """Initiates a serial connection.
    
        Args:
        No args.

        Returns:
        It always returns True
        """        
        logging.info("connecting")
        try:
            self.serial_connection = serial.Serial(port = self.comport,\
                baudrate = self.baudrate, timeout = self.timeout)
            self.serial_connection.open() 
        except:
            logging.error("incorrect hostname or port number")
            return False
            
        return True
        

        
    def read(self):
        """This function reads from the serial port and returns a list of
        received strings.
        """
        logging.info("reading from serial port")
        return self.serial_connection.readlines()
    

    def command(self, cmd):
        """Sends a command to the host and returns the response.
        
        Args:
        The cmd is a string without the newline, "\n", and contains the
        command. 

        Returns:
        It returns None if the command is not correct.
        Otherwise, it returns a list of strings that each string is
        terminated with a newline character".
        """
        
        logging.info("command " + cmd)
        self.serial_connection.write(cmd + "\n")
        rcved_list = self.read()
        return "".join(rcved_list)
        
        
    def close(self):
        """Closes the serial port connection.
        
        Args:
            None
        
        Returns:
            None
        
        """
        self.serial_connection.close()