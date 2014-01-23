################################################################################
#
# This file includes Connectivity class, and implementation
# Company: Sierra Wireless
# Time   : Jun  24, 2013
# Author: Airlink
#
################################################################################

import logging
import os
import sys
import datetime
import time

airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")
sys.path.append(".")

import basic_airlink
import proxy_airlink

basic_airlink.append_sys_path()

tbd_config_map = basic_airlink.get_tbd_config_data()
import telnet_airlink, ssh_airlink, ping_airlink, serial_airlink
import linux_airlink


class Connectivity:
    
    def __init__(self, device_name, username="user", password="12345", debug_level = "0", verbose = False):
        
        ''' check all related items in testbed for testing '''
                
        self.device_name = device_name
        self.username = username
        self.password = password
        self.debug_level = debug_level
        self.verbose = verbose
        self.error_flag = 0
        
    def get_url(self):
        addr = self.address()
        return "http://"+addr +":9191"
    
       
    def address(self):
        '''
        Return the IP address based on the DUT  and connection interface 
        
        Args: 
            device:  DUT name 
            interface: 4 physical connection ways (OTA/USB/ETH/WIFI) between PC and device
        Returns: 
            IP address which PC can ping to device
        Others: 
            The connection is not serial 
            
        '''
        print "\ndevice_name:"+ self.device_name
        if   tbd_config_map[self.device_name]["INTERFACE"]  == "ETHERNET": 
            return tbd_config_map[self.device_name]["ETH_DEVICE_IP"]  
        elif tbd_config_map[self.device_name]["INTERFACE"]  == "OTA":
            return tbd_config_map[self.device_name]["WAN_IP"]  
        elif tbd_config_map[self.device_name]["INTERFACE"]  == "USB":
            return tbd_config_map[self.device_name]["USB_DEVICE_IP"]                      
        elif tbd_config_map[self.device_name]["INTERFACE"]  == "WIFI":
            return tbd_config_map[self.device_name]["WIFI_DEVICE_IP"]  
        else:
            return "0.0.0.0"
        
        
    def telnet_interface(self):
        '''
         Telnet to device by different connections ETHERNET/USB/OTA/WIFI
        
        '''
        tn_timeout = tbd_config_map[self.device_name]["TELNET_TIMEOUT"]
        
        if    tbd_config_map[self.device_name]["INTERFACE"] == "ETHERNET":
            connect_instance = telnet_airlink.TelnetAirlink(tbd_config_map[self.device_name]["ETH_DEVICE_IP"], "2332", self.username,self.password,self.verbose, tn_timeout)
        elif  tbd_config_map[self.device_name]["INTERFACE"] == "USB":
            connect_instance = telnet_airlink.TelnetAirlink(tbd_config_map[self.device_name]["USB_DEVICE_IP"], "2332", self.username,self.password,self.verbose, tn_timeout)
        elif  tbd_config_map[self.device_name]["INTERFACE"] == "OTA":
            connect_instance = telnet_airlink.TelnetAirlink(tbd_config_map[self.device_name]["WAN_IP"],        "2332", self.username,self.password,self.verbose, tn_timeout)
        elif  tbd_config_map[self.device_name]["INTERFACE"] == "WIFI":
            connect_instance = telnet_airlink.TelnetAirlink(tbd_config_map[self.device_name]["WIFI_DEVICE_IP"],"2332", self.username,self.password,self.verbose, tn_timeout)
        else: 
            logging.debug("\n Wrong interface type")
            
        return connect_instance


    def ssh_interface(self):
        '''
         SSH to device by different connections ETHERNET/USB/OTA/WIFI
         
         TODO: why there is no timeout in ssh_airlink.SshAirlink() ? problem?
        
        '''
        ssh_timeout =tbd_config_map[self.device_name]["SSH_TIMEOUT"]

        if    tbd_config_map[self.device_name]["INTERFACE"] == "ETHERNET":
            ssh_instance = ssh_airlink.SshAirlink( hostname=tbd_config_map[self.device_name]["ETH_DEVICE_IP"], port = "22", username = self.username, password = self.password)
        elif  tbd_config_map[self.device_name]["INTERFACE"] == "USB":
            print "\n USB IP = " + tbd_config_map[self.device_name]["USB_IP"]
            ssh_instance = ssh_airlink.SshAirlink( hostname=tbd_config_map[self.device_name]["USB_DEVICE_IP"], port = "22", username = self.username, password = self.password)
        elif  tbd_config_map[self.device_name]["INTERFACE"] == "OTA":
            ssh_instance = ssh_airlink.SshAirlink( hostname=tbd_config_map[self.device_name]["WAN_IP"], port = "22", username = self.username, password = self.password)
        elif  tbd_config_map[self.device_name]["INTERFACE"] == "WIFI":
            ssh_instance = ssh_airlink.SshAirlink( hostname=tbd_config_map[self.device_name]["WIFI_DEVICE_IP"], port = "22", username = self.username, password = self.password)
        else: 
            logging.debug("\n Wrong interface type")
            
        return ssh_instance
 
 
    def serial_interface(self):
        '''
         Connect to device by Serial cable from PC
        
        '''
        serial_timeout =tbd_config_map[self.device_name]["SERIAL_TIMEOUT"]

        logging.debug("\n Make sure the serial cable connected before testing")
       
        if   tbd_config_map[self.device_name]["INTERFACE"] == "SERIAL":
            print "\n COM_PORT=======" + tbd_config_map[self.device_name]["COM_PORT"]
            serial_instance = serial_airlink.SerialAirlink(tbd_config_map[self.device_name]["COM_PORT"], 115200, serial_timeout)
        else:       
            logging.debug("\n Wrong interface type")
        
        return serial_instance
    
    

    def telnet_ssh(self):
        '''
        connect to device by telnet or ssh 
        
        '''
        connect_type      = tbd_config_map[self.device_name]["CONNECTION_TYPE"]
        connect_interface = tbd_config_map[self.device_name]["INTERFACE"]
        if    connect_type == "TELNET":
            return self.telnet_interface(connect_interface)
        elif  connect_type == "SSH":
            return self.ssh_interface(connect_interface)
        else: 
            logging.debug("\n Wrong connection type")
            
    
    def connection_types(self):
        '''
        
        '''
        if    tbd_config_map[self.device_name]["CONNECTION_TYPE"] == "TELNET":
            return self.telnet_interface()
        elif  tbd_config_map[self.device_name]["CONNECTION_TYPE"] == "SSH":
            return self.ssh_interface()
        elif  tbd_config_map[self.device_name]["CONNECTION_TYPE"] == "SERIAL":
            return self.serial_interface()
   
 
    def testbed_ready(self):
        ''' check if testbed ready 
        '''
#         if not self.controller_ready(testbed_name):
#             return False
        
#         if testbed_name in ["WAN","VPN","GPS","LPM", "LAN"]:
#             if not self.host_ready(1, testbed_name) or \
#                not self.host_ready(2, testbed_name):
#                 return False
        dut_ip=self.address()    
        if not self.dut_ready(dut_ip): 
            return False
        
        return True    
            
    def dut_ready(self,dut_ip):
        ''' check if DUT is ready 
        '''
               
        ret = True  
        if  tbd_config_map[self.device_name]["INTERFACE"] == "SERIAL":
            logging.debug("please make sure the serial line connected!\n")  
            return ret
        else:               
            pp=ping_airlink.PingAirlink()         # shall not be Serial cable connection
            for i in range(1,5):
                if  pp.ping_test(dut_ip):            
                    logging.debug("DUT ready\n")  
                else: 
                    logging.debug("DUT not ready yet\n")  
                    self.error_flag +=1
                    ret = False
            
        return ret    

    def host_ready(self, host_no=1, testbed_name="WAN"):
        ''' check if host1/host2 ready
        TODO
        '''
            
        pp=ping_airlink.PingAirlink()     
        
        if host_no == 1: 
            if  pp.ping_test(tbd_config_map["MANAGEMENT_IP"]["HOST1"]):            
                basic_airlink.slog("HOST1 ready\n")  
                return True
            else: 
                basic_airlink.slog("HOST1 not ready yet\n")  
                return False
                
        elif host_no == 2: 

            if  pp.ping_test(tbd_config_map["MANAGEMENT_IP"]["HOST2"]):            
                basic_airlink.slog("HOST2 ready\n") 
                return True 
            else: 
                basic_airlink.slog("HOST2 not ready yet\n")  
                return False
        else: 
                basic_airlink.slog("HOST number wrong\n")              
                return False      
 
    def controller_ready(self, testbed_name = "WAN"):
        
        return True
            
    def add_route(self, network_destination, netmask, gateway, metric=30):
        ''' Add route by administrator  (IPV4), for example in Windows OS
        route ADD 
        Args:    
            network_destination_ip    network_destination_ip
            local_eth_ip              gateway address
            metric                    interface METRIC
        TODO: for Linux
        Returns: True/False
        '''
        cmd ='route ADD'
        arg_string = '-p '+ network_destination +' MASK '+netmask+' '+gateway+\
        ' METRIC ' +str(metric)
        current_date_time = datetime.datetime.now()
        basic_airlink.cslog(str(current_date_time)+" Executing " + cmd)
        ret=basic_airlink.cmd_stdout(cmd, arg_string, 30)
        
        if ret.find("failed",0)>=0:
            return False
        else:
            return True
                
    def delete_route(self, network_destination):
        ''' Delete route by administrator (IPV4)
        TODO: for Linux
        
        Args:    None
        Returns: True/False
        '''
        current_date_time = datetime.datetime.now()
        cmd = 'route DELETE '
        arg_string = network_destination 
        basic_airlink.cslog(str(current_date_time)+ " Executing " + cmd)
        ret=basic_airlink.cmd_stdout(cmd, arg_string, 30)
        if ret.find("failed",0)>=0:
            return False
        else:
            return True
            
    def change_route(self, network_destination, netmask, gateway,metric=30):
        '''  change route table by administrator (IPV4)
        route CHANGE 0.0.0.0 MASK 0.0.0.0 10.1.12.41 METRIC 4
        TODO: for Linux
        Args:    
            network_destination_ip    network_destination_ip
            local_eth_ip              gateway address
            metric                    METRIC
            
        Returns: True/False
        '''
        current_date_time = datetime.datetime.now()
        cmd = 'route CHANGE '
        arg_string = network_destination +' MASK '+netmask+' '+gateway+\
        ' METRIC ' +str(metric)
        basic_airlink.cslog(str(current_date_time)+ " Executing " + cmd)
        ret=basic_airlink.cmd_stdout(cmd, arg_string, 30)
        if ret.find("failed",0)>=0:
            return False
        else:
            return True
    
    def get_route_table(self):
        '''  print out route table by administrator and command route PRINT 
         TODO: for Linux
       Args: None
        Returns: string, route table info
        '''
        current_date_time = datetime.datetime.now()
        cmd = 'route PRINT '
        
        basic_airlink.cslog(str(current_date_time)+ " Executing " + cmd)
        return basic_airlink.cmd_stdout(cmd, "", 30)
                            
    def update_controller_rt(self, 
                             host2_private_ip="172.20.20.2", 
                             controller_private_ip="192.168.13.201"):
        ''' update controller route table: change one and add one
        
        Args: 
            host2_private_ip       HOST2 Private IP
            controller_private_ip  Controller PC's private IP
        Returns: TODO
        
        '''
        # DUT to everywhere,  shall be there once plgin eth cables, just change METRIC
        self.change_route("0.0.0.0","0.0.0.0", "10.1.12.254", 3)
            
        #  from controller to DUT ... host 2
        self.delete_route(host2_private_ip)
        self.add_route(host2_private_ip,"255.255.255.255",controller_private_ip, 30)    
        
    def resource_monitor(self, flag):
        ''' need to do first
             #self.connectivity_obj = connectivity.Connectivity(username="root", password="v3r1fym3", debug_level = tbd_config_map["LOG_LEVEL"], verbose = True) 
       
        '''
        if flag == "YES":
            connectivity_ins = self.connection_types()
            if connectivity_ins.connect():
    #                self.at_radio_ins = at_utilities_radio.AtCommandsRadio()
    #                ret = self.at_radio_ins.get_gstatus(self.connectivity_ins)
                self.linux_ins = linux_airlink.LinuxAirlink()
                ret = self.linux_ins.get_mem_usage(connectivity_ins)                
                print ret  
                #time.sleep(60)
                connectivity_ins.close() 