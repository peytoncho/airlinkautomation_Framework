################################################################################
#
# This file includes Connectivity class, and implementation
# Company: Sierra Wireless
# Time   : Jun  24, 2013
# Author : Airlink
#
################################################################################

import logging
import datetime
import basic_airlink

basic_airlink.append_sys_path()

tbd_config_map = basic_airlink.get_tbd_config_data()
import telnet_airlink, ssh_airlink, ping_airlink, serial_airlink
import linux_airlink
import at_utilities
import sys
import time
import selenium_utilities
import proxy_airlink

class Connectivity:
    
    def __init__(self, device_name=tbd_config_map["DUTS"][0], username="user", password="12345", debug_level = "0", verbose = False):
        
        ''' check all related items in testbed for testing '''
                
        self.device_name  = device_name
        self.username = username
        self.password = password
        self.debug_level = debug_level
        self.verbose = verbose
        self.device_model = tbd_config_map[self.device_name]["MODEL"]
        self.aleos_sw_ver = tbd_config_map[self.device_name]["ALEOS_FW_VER"][:-4]  #long -> short        
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

        basic_airlink.cslog(" Make sure the serial cable connected before testing")
       
#        if   tbd_config_map[self.device_name]["INTERFACE"] == "SERIAL":
#            print "\n COM_PORT=======" + tbd_config_map[self.device_name]["COM_PORT"]
        serial_instance = serial_airlink.SerialAirlink(tbd_config_map[self.device_name]["COM_PORT"], 115200, serial_timeout)
#        else:       
#            logging.debug("\n Wrong interface type")
        
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
   
 
    def testbed_ready(self, proxy_ip=None, testbed_name="WAN", retry_count = 3):
        ''' check if testbed ready 
        '''
        if not self.controller_ready(testbed_name):
            return False
        
        if testbed_name in ["WAN","VPN","GPS","LPM", "LAN"]:
            if not self.host_ready(1, testbed_name) or \
               not self.host_ready(2, testbed_name):
                return False
            
        if not self.dut_ready(proxy_ip, retry_count): 
            return False
        
        return True    
            
    def dut_ready(self, proxy_ip=None, device_name=tbd_config_map["DUTS"][0],retry_count=3):
        ''' check if DUT is ready 
        TODO
        '''
        adr = self.address()
        ready = False

        if proxy_ip is not None:
            self.proxy = proxy_airlink.ProxyAirlink(proxy_ip)
            self.proxy_conn = self.proxy.connect()    
            for ii in range(retry_count):
                pp = ping_airlink.PingAirlink()
                remote_ping = self.proxy.deliver(pp)
                
                if remote_ping.ping_test(adr):
                    basic_airlink.cslog(device_name+" ready " + " at Try out "+str(ii+1)) 
                    ready = True
                    break                       
                else:
                    basic_airlink.cslog(device_name+" not ready yet "+ " at Try out "+str(ii+1)) 
                                   
        else:
            for ii in range(retry_count):       
    #            if  tbd_config_map[self.device_name]["INTERFACE"] == "SERIAL":
    #                basic_airlink.cslog("please make sure the serial line connected!\n")  
    #                return True
                           
                pp=ping_airlink.PingAirlink()         # shall not be Serial cable connection
                if  not pp.ping_test(adr):            
                    basic_airlink.cslog(device_name+" not ready yet "+ " at Try out "+str(ii+1))  
                else:
                    basic_airlink.cslog(device_name+" ready "+ " at Try out "+str(ii+1)) 
                    ready = True
                    break
        return ready       

    def host_ready(self, host_no=1, testbed_name="WAN", retry_count = 3):
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
        
    def resource_monitor(self, flag=tbd_config_map["RESOURCE_MONITOR"]):
        ''' need to do first
             #self.connectivity_obj = connectivity.Connectivity(device_name=tbd_config_map["DUTS"][0], username="root", password="v3r1fym3", debug_level = tbd_config_map["LOG_LEVEL"], verbose = True) 
       
        '''
        if flag == "YES":
            connectivity_ins = self.connection_types()
            if connectivity_ins.connect():
                self.linux_ins = linux_airlink.LinuxAirlink()
                ret = self.linux_ins.get_mem_usage(connectivity_ins)                
                connectivity_ins.close() 

    def get_at_instance(self, proxy_ip = None):
        ''' if proxy_ip is not None then will generate remote at instance.
        '''
        local_at_ins   = at_utilities.AtCommands() 
        
        if proxy_ip is not None:
            
            self.proxy = proxy_airlink.ProxyAirlink(proxy_ip)
            self.proxy_conn = self.proxy.connect()
        
            at_ins = self.proxy.deliver(local_at_ins)
            
        else:
            at_ins = local_at_ins 
            
        return at_ins

    def get_se_instance(self, proxy_ip = None):
        ''' if proxy_ip is not None then will generate remote Selenium UI instance.
        '''
        local_se_ins = selenium_utilities.SeleniumAcemanager(self.device_name)
        
        if proxy_ip is not None:
            self.proxy = proxy_airlink.ProxyAirlink(proxy_ip)
            self.proxy_conn = self.proxy.connect()
            
            se_ins = self.proxy.deliver(local_se_ins)
        else:
            se_ins = local_se_ins
        
        return se_ins        
                            
    def global_init(self, proxy_ip=None, how_init ="AT"):
        '''  THhis method will do the global initialization (factory reset) on
         all DUTs defined in comm_testbed_conf.yml.
         Args: 
             proxy_ip    None - DUT connects to controller, 
                         host  IP address - DUT connects to host
            how_init     AT - by AT coomand do factort reset 
                        UI - factory reset by ACEmanger UI -> Admin -> Advanced  -> Factory resset button
         Returns:  True/False 
         Globals:  
             self.device_name 
             tbd_config_map["GLOBAl_INIT"] ON/OFF
             tbd_config_map[self.device_name]["USERNAME"],
             tbd_config_map[self.device_name]["PASSWORD"],
        '''
        
        ret_init = True
       
        if tbd_config_map["GLOBAl_INIT"] == "ON":
            
            basic_airlink.cslog("On "+ self.devcie_name+", Global initialization "+'begins from testsuite launcher, parameters: proxy_ip = '+str(proxy_ip)+", how_init ="+how_init)
            
                        
            if how_init == "AT":
                
                at_ins = self.get_at_instance(proxy_ip)
                
                basic_airlink.cslog("Try out: serial interface")
                connect_instance = self.serial_interface()
                if not connect_instance.connect(): 
                    basic_airlink.cslog("Problem: serial connection")
                    
                    basic_airlink.cslog("Try out: SSH interface")           
                    connect_instance = self.ssh_interface()
                    if not connect_instance.connect(): 
                        basic_airlink.cslog("Problem: ssh connection")

                        basic_airlink.cslog("Try out: Telnet interface")           
                        connect_instance = self.telnet_interface()
                        if not connect_instance.connect(): 
                            basic_airlink.cslog("Problem: telnet connection")
                            return False                                             
                                
                ret = at_ins.factory_reset(connect_instance)
                if not ret:
                    ret_init =  False  
                
                time.sleep(tbd_config_map[self.device_name]["REBOOT_TIMEOUT"])   # TO Enhance                 
                
            elif how_init == "UI":
                
                se_ins = self.get_se_instance(proxy_ip)
           
                basic_airlink.cslog("step: login to ACEmanager")
                ace_manager_url = self.get_url()
                driver = se_ins.login(ace_manager_url, 
                                                tbd_config_map[self.device_name]["USERNAME"], 
                                                tbd_config_map[self.device_name]["PASSWORD"])
                time.sleep(tbd_config_map[self.device_name]["ACE_LOGIN_WAIT"])  
                     
                se_ins.admin_advanced_page(driver)
                
                if not se_ins.factory_reset(driver): 
                    ret_init =  False   
                else: 
                    
                    time.sleep(tbd_config_map[self.device_name]["REBOOT_TIMEOUT"])  #  TO Enhance      
                    
                se_ins.quit(driver)                       
        
        return ret_init       
