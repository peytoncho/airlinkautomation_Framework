################################################################################
#
# This file include implementation of AT commands on Radio module
# Company: Sierra Wireless
# Time: Dec  3, 2013
# Author: Airlink
#
################################################################################

import basic_airlink
import msciids
import os
import sys
import datetime
import time

class AtCommandsRadio(object):
    ''' This class includes radio related AT commands implementation.
    
    Precondition: 
                Telnet/SSH/Serial connection instance to DUT
                login as root
                e.g. 
                connect_ins = telnet_airlink.TelnetAirlink( hostname=_hostname, port = "2332", username = "root", password = "v3r1fym3",debug_mode= False)
                if not (connect_ins.connect()):
                ...
        
    '''

    def __init__(self): 
        '''
        '''
        self.error_flag = 0
    

    def get_gstatus(self, instance): 
        ''' use modem_util to get the status, this is radio module's AT command,
        need to login as root first.
        TODO
        Args: 
            instance: Telnet/SSH/Serial connection instance 

        Returns:
            status (string)
        '''
        basic_airlink.slog("Step: get status by radio AT command for root user")
        ret = \
        instance.command("modem_util $ALEOS_ATDEV 115200 \'at!gstatus?\'")
        ret_str = ''.join(ret)                
        basic_airlink.slog( ret_str)         
        if ret_str.find("OK",0) == -1 : 
            basic_airlink.slog(' device reboot not OK   \n')
            return basic_airlink.ERR
        else:    
            return ret_str
        
    def get_gpsstatus(self, instance): 
        ''' use modem_util to get the status, this is radio module's AT command,
        need to login as root first.
        TODO
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            status (string)
        '''
        basic_airlink.slog("Step: get status by radio AT command for root user")
        ret = \
        instance.command("modem_util $ALEOS_ATDEV 38400 \'at!gpsstatus?\'")
        ret_str = ''.join(ret)                
        basic_airlink.slog( ret_str)         
        if ret_str.find("OK",0) == -1 : 
            basic_airlink.slog(' device reboot not OK   \n')
            return basic_airlink.ERR
        else:    
            return ret_str
 
    def get_ecio(self, instance): 
        ''' use modem_util to get the ECIO, this is radio module's AT command,
        need to login as root first.
        TODO
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            status (string)
        '''
        basic_airlink.slog("Step: get ECIO by radio AT command for root user")
        ret = \
        instance.command("modem_util $ALEOS_ATDEV 38400 \'at+ecio?\'")
        ret_str = ''.join(ret)                
        basic_airlink.slog( ret_str)         
        if ret_str.find("OK",0) == -1 : 
            basic_airlink.slog(' device reboot not OK   \n')
            return basic_airlink.ERR
        else:    
            return ret_str       