import subprocess
import logging
import platform, socket

class PingAirlink(object):
    '''
    This class provides the basic ping functions on Windows and Linux platform
    
    '''
    def __init__(self):
        
        return

    def ping_test(self, address):
        ''' ping a device
        Args:
             address: IP address
        Returns: 
            True - ping ok, False - ping failed        
        '''
        if platform.system().find("Linux")<0: 
            count_flag="-n"
        else:    
            count_flag="-c"    
        p = subprocess.Popen(['ping', count_flag, '5', address], stdout=subprocess.PIPE)
        out, err = p.communicate()

        logging.debug(out)

        if out.find(" from %s" %address) > 0:
            print "Ping to %s succeed from %s with its %s OS" % (address, socket.gethostname(), platform.system())
            return True
        else:
            print "Ping to %s fail from %s with its %s OS" % (address, socket.gethostname(), platform.system())
            return False  
 
        
    def ping_test_linux(self, address='192.168.13.31'):
        '''ping a device
        Args:
             url: IP to DUT
        Returns: 
            True - ping ok, False - ping failed
            
        '''

        ret = subprocess.call(['ping', '-c', '3', address])
        print address, ret
        if ret == 0:
            logging.debug("ping to " + address + " :OK")
            return True
        elif ret == 2:
            logging.debug("no response from " + address)
        else: 
            logging.debug("Ping to " + address + " failed!")            
        return False 
    
