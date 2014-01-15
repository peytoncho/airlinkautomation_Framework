import telnetlib

# The following procedures are for configuring the Cisco Router/Concentrator for VPN/IpSec

# Additional features to add
# show crypto isakmp policy
# show crypto map
# show crypto isakmp sa
# show crypto ipsec sa
# 
# show debug

# handle the following when going Dynamic to Call Box static
#no ip route 0.0.0.0 0.0.0.0 192.168.1.1
#no ip nat pool nat 64.163.70.155 64.163.70.155 netmask 255.255.255.252
#ip route 0.0.0.0 0.0.0.0 192.168.1.11
#no ip default-gateway 64.163.70.1
#ip default-gateway 192.168.1.11
#no crypto isakmp key sierra123 address 0.0.0.0 0.0.0.0 no-xauth

# convert Aleos AT Command values to Cisco IOS command values

import logging

class CiscoConfig:
    # 
    def __init__(self, ip = "172.22.1.254", port = "23", username = "", password = "enable", debug_level = True, verbose = False):
        
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.debug_level = debug_level
        self.verbose = verbose

        self.connect()

        
        # load cisco config file 
        # TODO: no need to implement it which need start from erase:
    def load_cisco_config(self):
        fo = open("/airlinkautomation/testsuite/GX440/VPN/1811_live_lte.conf","r")
        cmd = fo.read()
        print cmd
        fo.close()
        cmd_list = "config t" + "\r\n" 
        self.tn.write(cmd_list)
        self.tn.read_until('(config)#')       
        self.tn.write(cmd)
        self.tn.read_until('SM5#')      
         

        # CISCO IOS Command "show conf"
    def show_cisco_config(self):
        print "show cisco config\n"

        cmd_list = "show conf" +"\r\n"
        print self.tn.write(cmd_list)
        
        keep_entering = True
        
        while keep_entering:
            idx, obj, response = self.tn.expect(['--More--', '-end'],3)
            if idx == 0:
                self.tn.write(" ")                      
            elif idx == 1:
                keep_entering = False
                #self.tn.write("\n")                      
            print response
 
        keep_entering2 = True
        while keep_entering2:
            idx, obj, response = self.tn.expect(['--More--', 'end'],3)
            if idx == 0:
                self.tn.write(" ")                      
            elif idx == 1:
                keep_entering2 = False
                self.tn.write("\n")                      

            print response
               
    def verbose_print(self, msg):
        if self.verbose:
            print msg
            

    def connect(self):

        self.verbose_print("Initiating Telnet connection ...")
        
        self.tn = telnetlib.Telnet(self.ip, self.port)
        if self.debug_level:
            self.tn.set_debuglevel(1)
            self.tn.msg(0)
        
        #self.tn.read_until("login: ")
        #self.tn.write(self.username + "\n")
        
        self.tn.read_until("Password: ")
        self.tn.write(self.password + "\n")

     
        # TODO: 
    def check_connection(self):
        
        self.verbose_print("Checking connection ...")
        print("Checking connection ...")
        
        self.tn.write("\n")
        output = self.tn.expect(["SM5#", "ERROR"])
        if output[0] == 0:
            self.verbose_print("Connection stablished ...")
            self.tn.write("\n")
            output = self.tn.expect(["SM5#", "ERROR"])
        else:
            self.verbose_print("Retry ...")
            self.initiate_connection()

    
    def set_aleos_vpn_translation(self):
      
        return
        
    def set_transform_set(self):
    
    
        return
    
    def set_crypto_dynamic_map(self):
  
    
        return
    
    def set_crypto_map(self):
     
    
        return
    
        # cisco IOS CLI command to setup isakmp policy
    def set_isakmp_policy(self):
        cmd_list = ["config t" + "\r\n"]
        cmd_list.append("crypto isakmp policy 100"+"\r\n")
        cmd_list.append(" encr aes"+"\r\n")
        cmd_list.append(" authentication pre-share"+"\r\n")
        cmd_list.append(" group 2"+"\r\n")
        cmd_list.append(" lifetime 7200"+"\r\n")
        cmd_list.append("exit" + "\r\n")
        self.tn.write(cmd_list)
        self.tn.read_until('SM5#') 
        
    
        # cisco IOS CLI command "interface"
        #@param interface_name interface name 
        #@param children       interface children 
    def set_interface0(self, interface_name, children):
        print "update cisco interface\n"
        prompt = 'SM5' +'(config)#'
        self.tn.write("config t" + "\r\n")
        self.tn.read_until(prompt)  
        
        if_prompt = 'SM5' +'(config-if)#'
        cmd_list=["interface FastEthernet0" +"\n"]
        cmd_list.append =("duplex auto" +"\n")
        cmd_list.append =("duplex auto"+"\n")
        cmd_list.append =("speed auto"+"\n")
        cmd_list.append =("no cdp enable"+"\n")
        cmd_list.append =("crypto map IPSEC"+"\n")
        cmd_list.append =("!"+"\n")
        self. ios_commands(cmd_list, if_prompt)
        
        self.tn.write("end" + "\r\n")
        prompt = 'SM5#'
        self.tn.read_until(prompt)   
        print "pass"
    
    # execute cisco IOS command list 
    def ios_commands(self,cmd_list,prompt):
        print "ios_commands \n"
        for cmd in cmd_list:
            self.tn.write(cmd +'\n')
            self.tn.read_until(prompt)     
                  
        print "ios_commands done \n"

    # execute cisco IOS command to update ip route
    def get_ip_route(self):
  
        print "pass"
        
     # execute cisco IOS command to update ip route
    def set_ip_route(self):
        prompt = 'SM5' +'(config)#'

        print "update cisco ip route\n"
        self.tn.write("config t" + "\r\n")
        self.tn.read_until('(config)#')   

        cmd_list = ["ip route 0.0.0.0 0.0.0.0 FastEthernet0"]
        cmd_list.append("ip route 0.0.0.0 0.0.0.0 208.81.123.254") 
        self. ios_commands(cmd_list, prompt)
        
        self.tn.write("end" + "\r\n")
        self.tn.read_until('SM5#')   
        print "pass"

       # Read Access List
    def get_access_list(self):
        print "read cisco access list\n"
 
        print "pass"
        
        # Cisco IOS CLI command to update Access List
        #access-list 102 permit ip 10.11.12.0 0.0.0.255 any
        #access-list 102 permit ip any 10.11.12.0 0.0.0.255
        #access-list 102 permit ip 192.168.13.0 0.0.0.255 any
        #access-list 102 permit ip any 192.168.13.0 0.0.0.255
    def set_access_list(self):
        print "update cisco access list\n"
        prompt = 'SM5' +'(config)#'
        self.tn.write("config t" + "\r\n")
        self.tn.read_until(prompt)   

        cmd_list = ["access-list 102 permit ip 10.11.12.0 0.0.0.255 any"]
        cmd_list.append("access-list 102 permit ip any 10.11.12.0 0.0.0.255")
        cmd_list.append("access-list 102 permit ip 192.168.13.0 0.0.0.255 any")
        cmd_list.append("access-list 102 permit ip any 192.168.13.0 0.0.0.255")    
        self. ios_commands(cmd_list, prompt)
        
        self.tn.write("end" + "\r\n")
        self.tn.read_until('SM5#')   
        print "pass"
          
    
    # Cisco IOS CLI command "config terminal"
    def CiscoConfigCmd(self, cmd):
        self.tn.write("config t" + "\r\n")
        self.tn.read_until('SM5(config)#') 
        self.tn.write(cmd)
        self.tn.read_until('SM5#')     
   
        return
        
        # cisco IOS CLI command "enable"
    def enable(self):

        self.tn.write("enable" + "\r\n")
        self.tn.read_until("SM5#")
    
        return
        
        # To read Cisco aggressive Isakmp Policy
    def get_aggressive_isakmp_policy(self):

    
        return

        # To setup Cisco aggressive Isakmp Policy
    def set_aggressive_isakmp_policy(self):
        cmd_list = ["config t" + "\r\n"]
        cmd_list.append("crypto isakmp peer address 0.0.0.0" + "\r\n")
        cmd_list.append("set aggressive-mode client-endpoint ipv4-address 0.0.0.0" + "\r\n")
        cmd_list.append("exit" + "\r\n")
        self.tn.write(cmd_list)
        self.tn.read_until('SM5#')
    
        return
            
    def ConcentratorVpnSetup(self):
  
    
        return
    
    # To save the cisco router configuration
    def save_config(self):
        self.tn.write("write memory")
        self.tn.read_until('SM5#')  
        return
    