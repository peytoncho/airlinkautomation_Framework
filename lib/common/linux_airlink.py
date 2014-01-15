################################################################################
#
# This file include implementation of Linux commands in ALEOS
# Company: Sierra Wireless
# Time: Nov  14, 2013
# Author: Airlink
#
################################################################################

import basic_airlink
import msciids
import os
import sys
import datetime
import time

class LinuxAirlink(object):
    ''' This class includes linux commands implementation in ALEOS.
    e.g. CSMAccessor, top, ps, ls.
    
    Precondition: 
                Telnet/SSH/Serial connection instance to DUT
                login as root, not user.
                e.g. 
                connect_ins = telnet_airlink.TelnetAirlink( hostname=_hostname, port = "2332", username = "root", password = "v3r1fym3",debug_mode= False)
                if not (connect_ins.connect()):
                ...
        
    '''

    def __init__(self): 
        '''
        '''
        self.error_flag = 0
    

    def get_timestamp_log(self, instance, parma_string): 
       '''step: get timestamp from log at the specified string
            instance: Telnet/SSH/Serial connection instance 
       TODO
       '''
        
       basic_airlink.slog("Step:  get the network state from the latest fives logs")
       
       reset_substring = 'Network State'  

       ret = instance.command("cat /mnt/hda1/junxion/log/messages | grep -E \'%s\'" %(reset_substring))
       ret_str = ''.join(ret)                             
       basic_airlink.slog(ret_str)
       
       ret = instance.command("cat /mnt/hda1/junxion/log/messages.0 | grep \"%s\"" %(reset_substring))
       ret_str = ''.join(ret)                             
       basic_airlink.slog(ret_str)

       ret = instance.command("cat /mnt/hda1/junxion/log/messages.1 | grep \"%s\"" %(reset_substring))
       ret_str = ''.join(ret)                             
       basic_airlink.slog(ret_str)

       ret = instance.command("cat /mnt/hda1/junxion/log/messages.2 | grep \"%s\"" %(reset_substring))
       ret_str = ''.join(ret)                             
       basic_airlink.slog(ret_str)

       ret = instance.command("cat /mnt/hda1/junxion/log/messages.3 | grep \"%s\"" %(reset_substring))
       ret_str = ''.join(ret)                             
       basic_airlink.slog(ret_str)

       ret = instance.command("cat /mnt/hda1/junxion/log/messages.4 | grep \"%s\"" %(reset_substring))
       ret_str = ''.join(ret)                             
       basic_airlink.slog(ret_str)
       
    def get_route_table(self, instance): 
        ''' get the route table from DUT
            instance: Telnet/SSH/Serial connection instance 

        '''
        pass

    def get_cpu_usage(self, instance): 
        ''' get the route table from DUT
            instance: Telnet/SSH/Serial connection instance 

        '''
        pass
    
    def get_mem_usage(self, instance): 
        ''' get the memory usage from DUT
            instance: Telnet/SSH/Serial connection instance 

        '''
        #step: get memory status 
        basic_airlink.slog("Step:  get memory status")
        
        ret = instance.command("free -m")
        ret_str = ''.join(ret)                             
        basic_airlink.slog(ret_str)
        
        ret = instance.command("top -n3")
        ret_str = ''.join(ret)                             
        basic_airlink.slog(ret_str)

        ret = instance.command("\n")

        ret = instance.command("cat /proc/meminfo")
        ret_str = ''.join(ret)                             
        basic_airlink.slog(ret_str)