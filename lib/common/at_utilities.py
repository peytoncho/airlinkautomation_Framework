################################################################################
#
# This file includes AT command class, and implementation of AT commands
# Company: Sierra Wireless
# Time: Jun  24, 2013
# Author: Airlink
#
################################################################################

import basic_airlink

class AtCommands(object):
    ''' This class includes AT commands implementation
    '''
    
    def __init__(self): 
        '''
        '''
        pass
    

    def query(self, instance, cmd):
        ''' common method to execute AT command, and return result
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            cmd:  AT command string
            
        Returns: 
            string, the results of executing AT query command
        '''
        #len_cmd = len(cmd)
        ret = instance.command(cmd)
        ret_str = ''.join(ret)
        basic_airlink.slog(ret_str)
        if ret_str.find("OK",0) == -1: 
            return basic_airlink.ERR
        else:
            #ret_str = ret_str[len_cmd:]
            ret_str = ret_str.replace(cmd,"")
            ret_str = ret_str.replace("OK","")
            ret_str = ret_str.replace("\n","")
            ret_str = ret_str.replace("\r","")
            return ret_str
    def query_new(self, instance, cmd):
        ''' common method to execute AT command, and return result
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            cmd:  AT command string
            
        Returns: 
            string, the results of executing AT query command
        '''
        #len_cmd = len(cmd)
        ret = instance.command(cmd)
        ret_str = ''.join(ret)
        basic_airlink.slog(ret_str)
        if not "OK" in ret_str: 
            return basic_airlink.ERR
        else:
            #ret_str = ret_str[len_cmd:]
            ret_str = ret_str.replace(cmd,"")
            ret_str = ret_str.replace("OK","")
            ret_str = ret_str.replace("\r","")
            return ret_str   
 
    def assign(self, instance, cmd):
        ''' common method to execute AT assignment command
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            cmd: string, AT assignment command
            
        Return: 
            True/False
        '''
        ret = instance.command(cmd)
        ret_str = ''.join(ret)
        basic_airlink.slog(ret_str)
        if not "OK" in ret_str:
            return False
        else:
            return True 
 
    def execute(self, instance, cmd):
        ''' common method to execute AT command without '?','='
        no OK return
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            cmd: string, AT assignment command
            
        Return: 
            True/False
        '''
        ret = instance.command(cmd)
        ret_str = ''.join(ret)
        basic_airlink.slog(ret_str)
        if ret_str.find("ERROR",0) >= 0:
            return False
        else:
            return True 
           
    def factory_reset(self, instance): 
        '''  Factory reset by AT command
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            True/False 
        '''
        cmd = "at*resetcfg"
        basic_airlink.slog("Step:  factory reset by AT command")
        return self.assign(instance,cmd)

    def atz_reboot(self, instance): 
        ''' Device reboot by AT command ATZ
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            True/False 
        '''
        cmd = "atz"
        basic_airlink.slog("Step:  reboot by AT command")
        return self.assign(instance,cmd)

    def get_block_reset_config(self, instance): 
        '''  Block reset config by AT command
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            block reset flag  0/1
        '''
        cmd = "at*block_reset_config?"
        basic_airlink.slog("Step:  get block reset by AT command")
        return self.query(instance,cmd)

    def set_block_reset_config(self, instance, flag): 
        '''  enable/disable Block reset config by AT command
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            True/False 
        '''
        cmd = "at*block_reset_config="+flag
        basic_airlink.slog("Step:  set block reset by AT command")
        return self.assign(instance,cmd)

    def get_board_temp(self, instance): 
        '''  get board temperature by AT command
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            block reset flag  0/1
        '''
        cmd = "at*boardtemp?"
        basic_airlink.slog("Step:  get board temperature by AT command")
        return self.query(instance,cmd)

    def get_power_input_voltage(self, instance): 
        '''  get power input voltage by AT command
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            power input voltage
        '''
        cmd = "at*powerin?"
        basic_airlink.slog("Step:  get power input voltage by AT command")
        return self.query(instance,cmd)

    def get_power_state(self, instance): 
        '''  get power state by AT command *POWERMODE?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            power state
        '''
        cmd = "at*powermode?"
        basic_airlink.slog("Step:  get power state by AT command *POWERMODE?")
        return self.query(instance,cmd)
    
    def at_ping(self, instance, address): 
        '''  at ping by AT command
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            True/False
        '''
        cmd = "ATPING"+address
        basic_airlink.slog("Step:  ping by AT command")
        return self.execute(instance,cmd)
                           
    def gstatus(self, instance): 
        ''' use modem_util to get the status, this is radio AT command
        TODO
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            status 
        '''
        basic_airlink.slog("Step:  get status by AT command for root user")
        ret = instance.command("modem_util $ALEOS_ATDEV 115200 \'at!gstatus?\'")
        ret_str = ''.join(ret)                
        basic_airlink.clog(ret_str)         
        if ret_str.find("OK",0) == -1 : 
            basic_airlink.slog(' device reboot not OK   \n')
            return basic_airlink.ERR
        else:    
            return ret_str
    
    def get_ecio(self, instance): 
        ''' use modem_util to get the Ec/Io value, this is radio AT command
        TODO
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            status 
        '''
        basic_airlink.slog("Step: Status using AT command for root user")
        ret = instance.command("modem_util $ALEOS_ATDEV 115200 \'at+ecio?\'")
        ret_str = ''.join(ret)               
        basic_airlink.clog(ret_str)         
        if ret_str.find("OK",0) == -1 : 
            basic_airlink.slog(' get ECIO not OK   \n')
            return basic_airlink.ERR
        else:    
            return ret_str
    
    def get_system_reset_number(self, instance):
        ''' To get the number of system reset 
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            system reset number 
        '''
        cmd = "at*sysresets?"
        basic_airlink.slog("Step:  get the number of system reset")            
        return self.query(instance,cmd)
 
    def get_analog_input_value(self, instance, analog_pin):
        '''Query current value of Analog input 1/2/3/4/5 by AT commands
            AT*ANALOGIN1?
            AT*ANALOGIN2?
            AT*ANALOGIN3?
            AT*ANALOGIN4?
            AT*ANALOGIN5? (new)
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            current value of Analog1/2/3/4/5
        '''
        cmd = "AT*ANALOGIN"+analog_pin+"?"
        basic_airlink.slog("Step:  get current value of Analog input 1/2/3/4/5 by AT command")
        return self.query(instance,cmd)
 
    def get_cell_info(self, instance, more_flag):
        '''Query cell info by AT command 
            AT*CELLINFO?
            AT*CELLINFO2?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            more_flag: empty string ""/"2"
            
        Returns:
            current cell info
        '''
        cmd = "AT*CELLINFO"+more_flag+"?"
        basic_airlink.slog("Step:  get current cell info by AT command")
        return self.query(instance,cmd)

    def get_wan_auth_mode(self, instance):
        '''Query cell info by AT command 
            AT*CLIENT_PPP_AUTH?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            current WAN authentication mode
        '''
        cmd = "AT*CLIENT_PPP_AUTH?"
        basic_airlink.slog("Step:  get current WAN authentication mode by AT command AT*CLIENT_PPP_AUTH?")
        return self.query(instance,cmd)

    def set_wan_auth_mode(self, instance, mode):
        '''Set cell info by AT command 
            AT*CLIENT_PPP_AUTH=0/1/2
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            True/False
        '''
        cmd = "AT*CLIENT_PPP_AUTH="+mode
        basic_airlink.slog("Step:  set current WAN authentication mode by AT command AT*CLIENT_PPP_AUTH="+mode)
        return self.assign(instance,cmd)

    def get_cts_assert(self, instance):
        '''Query assert CTS by AT command AT*CTSE?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            current assert CTS
        '''
        cmd = "AT*CTSE?"
        basic_airlink.slog("Step:  get assert CTS by AT command AT*CTSE?")
        return self.query(instance,cmd)
 
    def set_cts_assert(self, instance, flag):
        '''enable/disable assert CTS by AT command AT*CTSE=0/1
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            True/False
        '''
        cmd = "AT*CTSE="+flag
        basic_airlink.slog("Step:  set assert CTS by AT command AT*CTSE="+flag)
        return self.assign(instance,cmd)
                                     
    def get_current_day_data_usage(self, instance):
        '''Query current day data usage by AT command AT*DATACURDAY?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            current day data usage
        '''

        cmd = "AT*DATACURDAY?"        
        basic_airlink.slog("Step:  get current day data usage by AT command " +cmd)
        return self.query(instance,cmd)
              
    def get_previous_day_data_usage(self, instance):
        '''Query previous day data usage by AT command AT*DATAPREDAY?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Previous day data usage
        '''
        cmd ="AT*DATAPREDAY?"
        basic_airlink.slog("Step:  get previous day data usage by AT command " + cmd)
        return self.query(instance,cmd)
               
    def get_data_plan_units(self, instance):
        '''Query data plan units by AT command AT*DATAPLANUNITS?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Data plan units
        '''
        cmd ="AT*DATAPLANUNITS?"
        basic_airlink.slog("Step:  get data plan units by AT command")
        return self.query(instance,cmd)
        
    def set_data_plan_units(self, instance, unit_flag ):
        '''Set data plan units by AT command AT*DATAPLANUNITS=[1|2]
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            unit_flag: "1" for MB, "2" for KB
            
        Returns:
            True/False
        '''
        cmd = "AT*DATAPLANUNITS="+unit_flag
        basic_airlink.slog("Step:  get data plan units by AT command")
        return self.assign(instance,cmd)  
            
    def get_data_usage_enable(self, instance):
        '''Query data usage enable by AT command AT*DATUSAGEENABLE?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Data plan units
        '''
        cmd = "AT*DATUSAGEENABLE?"
        basic_airlink.slog("Step:  get data usage enable by AT command")
        return self.query(instance,cmd)
    
    def set_data_usage_enable(self, instance, flag):
        '''Set data usage enable by AT command AT*DATAUSAGEENABLE=[1|0]
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            flag: "1" for enable, "0" for disable
            
        Returns:
            True/False
        '''
        cmd = "AT*DATAUSAGEENABLE="+flag
        basic_airlink.slog("Step:  set data usage enable by AT command")
        return self.assign(instance, cmd)  

    def get_date(self, instance):
        '''Query current date/time by AT command AT*DATE?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            current date/time
        '''
        cmd = "AT*DATE?"
        basic_airlink.slog("Step:  get current date/time by AT command")
        return self.query(instance,cmd)

    def get_datz(self, instance):
        '''Query the flag (enable/disable) to allow reset with "atz" by 
           AT command AT*DATZ?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            flag (enable/disable) to allow reset with "atz"
        '''
        cmd = "AT*DATZ?"
        basic_airlink.slog("Step:  get current date/time by AT command")
        return self.query(instance,cmd)

    def set_datz(self, instance, flag ):
        '''enable/disable atz reset by AT command AT*DATZ=[1|0]
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            flag: [1|0]   1= enable, 0 = disable
            
        Returns:
            True/False
        '''
        cmd = "AT*DATZ="+flag
        basic_airlink.slog("Step:  enable/disable atz reset AT command")
        return self.assign(instance,cmd)
 
    def get_device_id(self, instance):
        '''get device ID by AT command AT*DEVICEID?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Device ID
        '''
        cmd = "AT*DEVICEID?"
        basic_airlink.slog("Step:  get device ID by AT command")
        return self.query(instance,cmd)       
   
    def get_digital_input_value(self, instance, digital_pin):
        '''Query current value of digital input 1/2/3/4 by AT command 
            AT*DIGITALIN1?
            AT*DIGITALIN2?
            AT*DIGITALIN3?
            AT*DIGITALIN4?
            AT*DIGITALIN5?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            current value of digital input 1/2/3/4/5
        '''
        cmd = "AT*DIGITALIN"+digital_pin+"?"
        basic_airlink.slog("Step:  get current value of digital input 1/2/3/4/5 by AT command")
        return self.query(instance,cmd)


    def get_disable_dvt(self, instance):
        '''Query current value of disable DVT by AT command AT*DISABLEDVT?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            current value of disable DVT
        '''
        cmd = "AT*DISABLEDVT?"
        basic_airlink.slog("Step:  get current value of disable DVT by AT command")
        return self.query(instance,cmd)

    def get_domain(self, instance):
        '''Query domain by AT command AT*DOMAIN?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            domain
        '''
        cmd = "AT*DOMAIN?"
        basic_airlink.slog("Step:  get domain by AT command")
        return self.query(instance,cmd)   
    
    def set_domain(self, instance, fqdn_domain):
        '''set domain by AT command AT*DOMAIN=[FQDN of domain]
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            fqdn_domain: FQDN of domain
            
        Returns:
            True/False
        '''
        cmd = "AT*DOMAIN="+fqdn_domain
        basic_airlink.slog("Step:  set domain AT command")
        return self.query(instance,cmd)
    
    def get_device_port(self, instance):
        '''Query device port for inbound PAD by AT command AT*DPORT?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            device port 
        '''
        cmd = "AT*DPORT?"
        basic_airlink.slog("Step:  get device port by AT command")
        return self.query(instance,cmd)
      
    def set_device_port(self, instance, port):
        '''set device port by AT command AT*DPORT=[port]
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            port: device port
            
        Returns:
            True/False
        '''
        cmd = "AT*DPORT="+port
        basic_airlink.slog("Step:  set device port AT command")
        return self.query(instance,cmd)   
 
    def get_dial_udp(self, instance):
        '''Query flag to force to dial to UDP only by AT command AT*DU?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            flag to force to dial to UDP only
        '''
        cmd = "AT*DU?"
        basic_airlink.slog("Step:  get flag to force to dial to UDP only by AT command")
        return self.query(instance,cmd)   
    
    def enable_dial_udp(self, instance, flag):
        '''set flag (force to dial to UDP only) by AT command AT*DU=[0|1]
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            flag: "0" for disable, "1" for enable
            
        Returns:
            True/False
        '''
        cmd="AT*DU="+flag
        basic_airlink.slog("Step:  enable/disable to force to dial UDP only by AT command")
        return self.assign(instance,cmd)   
 
    def get_dynamic_dns(self, instance):
        '''Query dynamic DNS by AT command AT*DYNDNS?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            value to map the dynamic DNS
        '''
        cmd = "AT*DYDNS?"
        basic_airlink.slog("Step:  Query dynamic DNS by AT command AT*DYNDNS?")
        return self.query(instance,cmd)   
    
    def set_dynamic_dns(self, instance, flag):
        '''Set dynamic DNS by AT command AT*DYNDNS=0/2/5/6/8/9/10
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            flag: 0/2/5/6/8/9/10
            
        Returns:
            True/False
        '''
        cmd="AT*DYNDNS="+flag
        basic_airlink.slog("Step:  Set dynamic DNS by AT command AT*DYNDNS=0/2/5/6/8/9/10")
        return self.assign(instance,cmd) 
 
    def get_engine_hours(self, instance):
        '''Query engine hours by AT command AT*ENGHRS? in Low Power mode
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            value to map the dynamic DNS
        '''
        cmd = "AT*ENGHRS?"
        basic_airlink.slog("Step:  Query engine hours by AT command AT*ENGHRS?")
        return self.query(instance,cmd)   
    
    def set_engine_hours(self, instance, hrs):
        '''Set engine hours starting value by AT command AT*ENGHRS=[hrs] in Low Power mode
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            hrs:  engine hours starting value
            
        Returns:
            True/False
        '''
        cmd="AT*ENGHRS="+hrs
        basic_airlink.slog("Step:  Set engine hours starting value by AT command AT*ENGHRS=[hrs]")
        return self.assign(instance,cmd) 

    def get_flag_enq_out(self, instance):
        '''Query flag to output ENQ by AT command AT*ENQ?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            flag to output ENQ
        '''
        cmd = "AT*ENQ?"
        basic_airlink.slog("Step:  Query flag to output ENQ by AT command AT*ENQ?")
        return self.query(instance,cmd)   
    
    def enable_enq_out(self, instance, flag):
        '''set flag (to putput ENQ) by AT command AT*ENQ=[0|1]
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            flag: "0" for disable, "1" for enable
            
        Returns:
            True/False
        '''
        cmd="AT*ENQ="+flag
        basic_airlink.slog("Step:  enable/disable to output ENQ by AT command")
        return self.assign(instance,cmd) 
                                          
    def get_ethernet_device_ip(self, instance):
        '''get HOST PEER IP/Device IP by AT command AT*HOSTPEERIP?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Device IP
        '''
        cmd="AT*HOSTPEERIP?"
        basic_airlink.slog("Step:  get device IP by AT command")
        return self.query(instance,cmd)   
            
    def set_ethernet_device_ip(self, instance, device_ip):
        ''' Set Ethernet device IP by AT command AT*HOSTPEERIP=<device_ip>
        
        Args:
            instance: connection (Telnet/SSH/Serial) instance 
            device_ip:  device IP address
            
        Returns:
            True/False 
        '''
        cmd="AT*HOSTPEERIP="+device_ip
        basic_airlink.slog("Step:  set HOST PEER IP by AT command")
        return self.assign(instance,cmd)
     
    def get_ethernet_starting_ip(self, instance):
        '''get starting IP by AT command AT*HOSTPRIVIP?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            starting IP
        '''
        cmd="AT*HOSTPRIVIP?"
        basic_airlink.slog("Step:  get starting IP by AT command")
        return self.query(instance,cmd)
                
    def set_ethernet_starting_ip(self, instance, staring_ip):
        ''' Set starting IP by AT command
        
        Args:
            instance: connection (Telnet/SSH/Serial) instance 
            starting_ip: starting IP address
            
        Returns: True/False
        
        '''
        cmd="AT*HOSTPRIVIP="+staring_ip
        basic_airlink.slog("Step:  set starting IP by AT command")
        return self.assign(instance,cmd) 

    def get_ethernet_ending_ip(self, instance):
        '''get ending IP by AT command AT*DHCPHOSTEND?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            ending IP
        '''
        cmd="AT*DHCPHOSTEND?"
        basic_airlink.slog("Step:  get ending IP by AT command")
        return self.query(instance,cmd)
                
    def set_ethernet_ending_ip(self, instance, ending_ip):
        ''' Set ending IP by AT command
        Args:
            instance: connection (Telnet/SSH/Serial) instance 
            sending_ip: Ethernet ending IP address
        Returns:
            True/False 
        '''
        cmd="AT*DHCPHOSTEND="+ending_ip
        basic_airlink.slog("Step:  set ending IP by AT command")
        return self.assign(instance,cmd)
                              
    def get_ethernet_dhcp_network_mask(self, instance):
        '''get DHCP network mask by AT command AT*DHCPNETMASK?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            DHCP network mask 
        '''
        cmd="AT*DHCPNETMASK?"
        basic_airlink.slog("Step:  get DHCP network mask by AT command")
        return self.query(instance,cmd)                         
 
    def set_ethernet_dhcp_network_mask(self, instance,dhcp_network_mask):
        '''set DHCP network mask by AT command        
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            dhcp_network_mask: Ethernet network mask
            
        Returns:
            True/False
        '''
        cmd="AT*DHCPNETMASK="+dhcp_network_mask
        basic_airlink.slog("Step:  set DHCP network mask by AT command")
        return self.assign(instance,cmd)
                             
    def get_ethernet_dhcp_server_mode(self, instance):
        '''get DHCP  server mode by AT command AT*DHCPSERVER?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            DHCP server mode 
        '''
        cmd="AT*DHCPSERVER?"
        basic_airlink.slog("Step:  get DHCP server mode by AT command")
        return self.query(instance,cmd)                           
 
    def set_ethernet_dhcp_server_mode(self, instance,dhcp_server_mode):
        '''set DHCP server mode by AT command    
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            dhcp_server_mode: DHCP server mode, "1 -Enable, "0" - disable
            
        Returns:
            True/False 
        '''
        cmd="AT*DHCPSERVER="+dhcp_server_mode
        basic_airlink.slog("Step:  set DHCP server mode by AT command")
        return self.assign(instance,cmd)
                        
    def get_ethernet_mac(self, instance, eth_port):
        '''get Ethernet Mac address by AT command 
            AT*ETHMAC?
            AT*ETHMAC?1
            AT*ETHMAC?2
            AT*ETHMAC?3
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            eth_port: empty/1 Ethernet port on device, 2/3 Ethernet port on the x-card
            
        Returns:
            Ethernet MAC address
        '''
        cmd="AT*ETHMAC?"+eth_port
        basic_airlink.slog("Step:  get Ethernet Mac address by AT command")
        return self.query(instance,cmd)           
                       
    def get_ethernet_state(self, instance, eth_port):
        '''Query Ethernet state by AT command 
            AT*ETHSTATE?
            AT*ETHSTATE?1
            AT*ETHSTATE?2
            AT*ETHSTATE?3
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            eth_port: empty/1 Ethernet port on device, 2/3 Ethernet port on the x-card
        Returns:
            Ethernet State
        '''
        cmd="AT*ETHSTATE?"+eth_port
        basic_airlink.slog("Step:  get Ethernet State by AT command")
        return self.query(instance,cmd)               
    
    def get_dns_state(self, instance, dns_no):
        '''Query DNS state by AT command 
            AT*DNS1?
            AT*DNS2?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            dns_no : "1" - primary DNS, "2" - secondary DNS
            
        Returns:
            DNS State
        '''
        cmd="AT*DNS"+dns_no+"?"
        basic_airlink.slog("Step:  get DNS State by AT command")
        return self.query(instance,cmd)                                  

    def get_dns_user(self, instance):
        '''Get DNS user IP by AT command AT*DNSUSER?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            DNS user IP
        '''
        cmd="AT*DNSUSER?"
        basic_airlink.slog("Step:  get DNS user by AT command")
        return self.query(instance,cmd)              

    def set_dns_user(self, instance,dns_user_ip):
        '''set DNS user IP mode by AT command        
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            dns_user_ip:  DNS user IP
            
        Returns:
            True/False 
        '''
        cmd="AT*DNSUSER="+dns_user_ip
        basic_airlink.slog("Step:  set DNS user IP by AT command")
        return self.assign(instance,cmd)    
    
    def get_host_auth(self, instance):
        '''Query host authentication for PPPeE by AT command AT*HOSTAUTH?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            host authentication
        '''
        cmd="AT*HOSTAUTH?"
        basic_airlink.slog("Step:  Query host authentication by AT command")
        return self.query(instance,cmd)            
    
    def set_host_auth(self, instance,host_auth):
        '''set host authentication by AT command     
           
        Args: 
            instance : Telnet/SSH/Serial connection instance 
            host_auth: authentication for PPoE, 0/1/2
            
        Returns:
            True/False 
        '''
        cmd="AT*HOSTAUTH="+host_auth
        basic_airlink.slog("Step:  set DNS user IP by AT command")
        return self.assign(instance,cmd)
    
    def get_host_password(self, instance):
        '''Get host password by AT command AT*HOSTPW?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            HOST password
        '''
        cmd="AT*HOSTPW?"
        basic_airlink.slog("Step:  get host password by AT command")
        return self.query(instance,cmd)            

    def set_host_passsord(self, instance,host_password):
        '''set host password mode by AT command AT*HOSTPW=[password]    
          
        Args: 
            instance     : Telnet/SSH/Serial connection instance 
            host_password: password 
            
        Returns:
            True/False 
        '''
        cmd="AT*HOSTPW="+host_password
        basic_airlink.slog("Step:  set host password by AT command")
        return self.assign(instance,cmd)  
    
    def get_host_username(self, instance):
        '''get host username by AT command AT*HOSTPUID?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            HOST UID
        '''
        cmd="AT*HOSTUID?"
        basic_airlink.slog("Step:  get host username by AT command")
        return self.query(instance,cmd)           
    
    def set_host_username(self, instance,host_username):
        '''set host username by AT command AT*HOSTUID=[username]    
         
        Args: 
            instance     : Telnet/SSH/Serial connection instance 
            host_username: host username 
            
        Returns:
            True/False 
        '''
        basic_airlink.slog("Step:  set host username by AT command")
        cmd="AT*HOSTUID="+host_username
        return self.assign(instance,cmd)    
 
    
    def get_usb_device_mode(self, instance):
        '''get USB device mode by AT command AT*USBDEVICE?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            USB device mode
        ''' 
        cmd = "AT*USBDEVICE?"
        basic_airlink.slog("Step:  get USB device mode by AT command")
        return self.query(instance,cmd)

    def get_wifi_mac(self, instance):
        '''Query WIFI MAC address by AT command AT*WIFIMAC?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            WIFI MAC Address
        ''' 
        cmd = "AT*WIFIMAC?"
        basic_airlink.slog("Step:  get WIFI MAC address by AT command")
        return self.query(instance,cmd)       
   
    def get_wifi_mode(self, instance):
        '''get Wifi mode by AT command AT*WIFIMODE?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi mode (0/1/2/3)
        ''' 
        cmd = "AT*WIFIMODE?"
        basic_airlink.slog("Step:  get Wifi mode by AT command")
        return self.query(instance,cmd)
       
    def set_wifi_mode(self, instance,flag):
        '''set Wifi mode by AT command AT*WIFIMODE=[0/1/2/3]    
         
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            flag:  
                "3" - access point and client mode, 
                "2" - client mode, 
                "1" - access point, 
                "0" - WIFI OFF 
            
        Returns:
            True/False 
        '''
        basic_airlink.slog("Step:  set Wifi mode by AT command")
        cmd="AT*WIFIMODE="+flag
        return self.assign(instance,cmd)   
     
    def get_wifi_ap_bridged(self, instance):
        '''get Wifi AP bridged by AT command AT*APBRIDGED?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi bridged
        ''' 
 
        cmd = "AT*APBRIDGED?"
        basic_airlink.slog("Step:  get Wifi bridged by AT command")
        return self.query(instance,cmd)
       
    def set_wifi_ap_bridged(self, instance,flag):
        '''set Wifi bridged by AT command AT*APBRIDGED=[0/1]    
         
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            flag:  "1" - enable, "0" - disable 
            
        Returns:
            True/False 
        '''
        basic_airlink.slog("Step:  set Wifi bridged by AT command")
        cmd="AT*APBRIDGED="+flag
        return self.assign(instance,cmd)    
    
    def get_wifi_ap_channel(self, instance):
        '''get Wifi AP channel by AT command AT*APCHANNEL?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi AP channel
        '''
        
        cmd = "AT*APCHANNEL?"
        basic_airlink.slog("Step:  get Wifi AP channel by AT command")
        return self.query(instance,cmd)    

    def set_wifi_ap_channel(self, instance,channel_num):
        '''set Wifi AP channel by AT command AT*APCHANNEL=[0-11]   
          
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            channel_num: channel number (range 0-11)
            
        Returns:
            True/False 
        '''
        basic_airlink.slog("Step:  set Wifi AP channel by AT command")
        cmd="AT*APCHANNEL="+channel_num
        return self.assign(instance,cmd)    
    
    def get_wifi_ap_enable(self, instance):
        '''Query Wifi AP enable by AT command AT*APEN?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi AP enable
        '''
        
        cmd = "AT*APEN?"
        basic_airlink.slog("Step:  get Wifi AP enable AT command")
        return self.query(instance,cmd)     
    
    def set_wifi_ap_enable(self, instance,ap_enable):
        '''set Wifi AP enable by AT command AT*APEN=[2|3]    
         
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            ap_enable  : 2 for b/g enabled, 3 for b/g/n enabled 
            
        Returns:
            True/False 
        '''
        basic_airlink.slog("Step:  set Wifi AP enable by AT command")
        cmd="AT*APEN="+ap_enable
        return self.assign(instance,cmd)       
        
    def get_wifi_ap_max_client(self, instance):
        '''Query Wifi AP max client by AT command AT*APMAXCLIENT?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi AP max client
        '''
        
        basic_airlink.slog("Step:  get Wifi AP max client AT command")
        cmd="AT*APMAXCLIENT?"
        return self.query(instance,cmd)           
  
    def set_wifi_ap_max_client(self, instance,ap_max_client):
        '''set Wifi AP max client by AT command AT*APMAXCLIENT=[1-8]  
           
        Args: 
            instance     : Telnet/SSH/Serial connection instance 
            ap_max_client: 1-8
            
        Returns:
            True/False 
        '''    
        cmd = "AT*APMAXCLIENT="+ap_max_client
        basic_airlink.slog("Step:  set Wifi AP max client by AT command")
        return self.assign(instance,cmd)      
          
    def get_wifi_ap_security_type(self, instance):
        '''Query Wifi AP security type by AT command AT*APSECURITYTYPE?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi AP security type
        '''   
        cmd = "AT*APSECURITYTYPE?"
        basic_airlink.slog("Step:  get Wifi AP security type AT command")
        return self.query(instance,cmd)      

    def set_wifi_ap_security_type(self, instance, ap_security_type):
        '''set Wifi AP security type by AT command AT*APSECURITYTYPE=[0/3/5] 
           ALLX-2440 
           
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            ap_security_type: 0 - open, 3 = WPA Personal  5 = WPA2 Personal
            
        Returns:
            True/False 
        '''
        basic_airlink.slog("Step:  set Wifi AP security type by AT command")
        cmd="AT*APSECURITYTYPE="+ap_security_type
        return self.assign(instance,cmd)    
    
    def get_wifi_ap_tx_power(self, instance):
        '''Query Wifi AP trasnmit power by AT command AT*APTXPWR?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi AP trasnmit power
        '''   
        cmd = "AT*APTXPWR?"
        basic_airlink.slog("Step:  get Wifi AP trasnmit power AT command")
        return self.query(instance,cmd)       

    def set_wifi_ap_tx_power(self, instance, ap_tx_power):
        '''set Wifi AP trasnmit power by AT command AT*APTXPWR=[0,1]    
         
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            ap_tx_power: 0 - low, 1 = normal
            
        Returns:
            True/False 
        '''
        basic_airlink.slog("Step:  set Wifi AP trasnmit power by AT command")
        cmd="AT*APTXPWR="+ap_tx_power
        return self.assign(instance,cmd)       
    
    def get_wifi_ap_host_ip(self, instance):
        '''Query Wifi AP host IP by AT command AT*APHOSTIP?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi AP AP host IP
        '''     
        basic_airlink.slog("Step:  get Wifi AP AP host IP AT command")
        cmd="AT*APHOSTIP?"
        return self.query(instance,cmd)    
    
    def set_wifi_ap_host_ip(self, instance, ap_host_ip):
        '''set Wifi AP host IP by AT command AT*APHOSTIP=<ip address>  
          
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            ap_host_ip: AP host IP
            
        Returns:
            True/False 
        '''
        basic_airlink.slog("Step:  set Wifi AP host IP by AT command")
        cmd="AT*APHOSTIP="+ap_host_ip
        return self.assign(instance,cmd)      
        
    def get_wifi_ap_starting_ip(self, instance):
        '''Query Wifi AP starting IP by AT command AT*APSTARTIP?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi AP starting IP
        '''    
        basic_airlink.slog("Step:  get Wifi AP starting IP AT command")
        cmd="AT*APSTARTIP?"
        return self.query(instance,cmd)    
    
    def set_wifi_ap_starting_ip(self, instance, ap_starting_ip):
        '''set Wifi AP starting IP by AT command AT*APSTARTIP=[0,1]  
           
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            ap_tx_power: starting IP
            
        Returns:
            True/False 
        '''
        basic_airlink.slog("Step:  set Wifi AP starting IP by AT command")
        cmd="AT*APSTARTIP="+ap_starting_ip
        return self.assign(instance,cmd)    
        
    def get_wifi_ap_ending_ip(self, instance):
        '''Query Wifi AP ending IP by AT command AT*APENDIP?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi AP ending IP
        '''
        
        basic_airlink.slog("Step:  get Wifi AP ending IP AT command")
        cmd="AT*APENDIP?"
        return self.query(instance,cmd)    

    def set_wifi_ap_ending_ip(self, instance, ap_ending_ip):
        '''set Wifi AP ending IP by AT command AT*APENDIP=<ip address> 
            
        Args: 
            instance : Telnet/SSH/Serial connection instance 
            ap_end_ip: ending IP address
            
        Returns:
            True/False 
        '''
        basic_airlink.slog("Step:  set Wifi AP ending IP by AT command")
        cmd="AT*APENDIP="+ap_ending_ip
        return self.assign(instance,cmd)      
    
    def get_wifi_ap_net_mask(self, instance):
        '''Query Wifi AP network mask by AT command AT*APNETMASK?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi AP network mask
        '''    
        basic_airlink.slog("Step:  get Wifi AP network mask AT command")
        cmd="AT*APNETMASK?"
        return self.query(instance,cmd)    
    
    def set_wifi_ap_net_mask(self, instance,ap_net_mask):
        '''set Wifi AP network mask by AT command AT*APNETMASK=[ip address] 
            
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            ap_net_mask: IP address
            
        Returns:
            True/False 
        '''
        basic_airlink.slog("Step:  set Wifi AP network mask by AT command")
        cmd="AT*APNETMASK="+ap_net_mask
        return self.assign(instance,cmd)    
    
    def get_wifi_ap_ssid_broadcast(self, instance):
        '''Query Wifi AP SSID broadcast by AT command AT*APSSIDBCAST?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi AP SSID broadcast 
        '''   
        basic_airlink.slog("Step:  get Wifi AP SSID broadcast  AT command")
        cmd="AT*APSSIDBCAST?"
        return self.query(instance,cmd)    
    
    def set_wifi_ap_ssid_broadcast(self, instance, ap_ssid_bcast):
        '''set Wifi AP SSID broadcast  by AT command AT*APSSIDBCAST=[ip address] 
            
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            ap_net_mask: SSID broadcast 1 or 0
            
        Returns:
            True/False 
        '''
        basic_airlink.slog("Step:  set Wifi AP SSID broadcast  by AT command")
        cmd="AT*APSSIDBCAST="+ap_ssid_bcast
        return self.assign(instance,cmd)    
           
    def get_wifi_ap_ssid_val(self, instance):
        '''Query Wifi AP SSID value by AT command AT*APSSIDVAL?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi AP SSID value 
        '''
        
        basic_airlink.slog("Step:  get Wifi AP SSID value  AT command")
        cmd="AT*APSSIDVAL?"
        return self.query(instance,cmd)    
    
    def set_wifi_ap_ssid_val(self, instance,ap_ssid_val):
        '''set Wifi AP SSID value by AT command AT*APSSIDVAL=[SSID value]    
         
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            ap_ssid_val: SSID value 
            
        Returns:
            True/False 
        '''
        basic_airlink.slog("Step:  set Wifi AP SSID value by AT command")
        cmd="AT*APSSIDVAL="+ap_ssid_val
        return self.assign(instance,cmd)    
    
    def get_wifi_ap_wep_enc_type(self, instance):
        '''Query Wifi AP WEP Encrypt type by AT command AT*APWEPENCTYPE?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi AP WEP Encrypt type 
        '''
        basic_airlink.slog("Step:  get Wifi AP WEP Encrypt type by AT command")
        cmd="AT*APWEPENCTYPE?"
        return self.query(instance,cmd)          

    def set_wifi_ap_wep_enc_type(self, instance, ap_wep_enc_type):
        '''set Wifi AP WEP Encrypt type by AT command AT*APWEPENCTYPE=[0/1]     
        
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            ap_wep_enc_type: WEP Encrypt type 
                            0 - disables WEP
                            1 - enables WEP
                            
        Returns:
            True/False 
        '''
        basic_airlink.slog("Step:  set Wifi AP WEP Encrypt type by AT command")
        cmd="AT*APWEPENCTYPE="+ap_wep_enc_type
        return self.assign(instance,cmd)    
         
    def get_wifi_ap_wep_key(self, instance):
        '''Query Wifi AP WEP key by AT command AT*APWEPKEY?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi AP WEP key
        '''
        basic_airlink.slog("Step:  get Wifi AP WEP key by AT command")
        cmd="AT*APWEPKEY?"
        return self.query(instance,cmd)          
          
    def get_wifi_ap_wep_key_len(self, instance):
        '''Query Wifi AP WEP key length by AT command AT*APWEPKEYLEN?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi AP WEP key length
        '''
        
        basic_airlink.slog("Step:  get Wifi AP WEP key length by AT command")
        cmd="AT*APWEPKEYLEN?"
        return self.query(instance,cmd)          

    def set_wifi_ap_wep_key_len(self, instance,ap_wep_key_len):
        '''set Wifi AP WEP key length by AT command AT*APWEPKEYLEN=[0/1/2]
             
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            ap_wep_key_len: WEP key length, 
                            0 for 64 bit encryption
                            1 for 128 bit encryption
                            2 for custom key
                            
        Returns:
            True/False 
        '''
        basic_airlink.slog("Step:  set Wifi AP WEP key length by AT command")
        cmd="AT*APWEPKEYLEN="+ap_wep_key_len
        return self.assign(instance,cmd)    
        
    def get_wifi_ap_wpa_crypt(self, instance):
        '''Query Wifi AP WPA/WPA2 Encryption type by AT command AT*APWPACRYPT?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Wifi AP WPA/WPA2 Encryption type
        '''
        
        basic_airlink.slog("Step:  get Wifi AP WPA/WPA2 Encryption type by AT command")
        cmd="AT*APWPACRYPT?"
        return self.query(instance,cmd)              

    def set_wifi_ap_wpa_crypt(self, instance,ap_wpa_crypt):
        '''set Wifi AP WPA/WPA2 encryption type by AT command AT*APWPACRYPT=[0/1]  
           
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            ap_wpa_crypt: WPA Crypt. 0 for TKIP, 1 for AES
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set Wifi AP WPA/WPA2 Encryption type by AT command")
        cmd="AT*APWPACRYPT="+ap_wpa_crypt
        return self.assign(instance,cmd)    
 
    def get_auto_prl_flag(self, instance):
        '''Query Auto update flag for CDMA PRL by AT command AT*AUTOPRL?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            0/1
        '''
        
        basic_airlink.slog("Step:  get Auto update flag for CDMA PRL by AT command AT*AUTOPRL?")
        cmd="AT*AUTOPRL?"
        return self.query(instance,cmd)              

    def set_auto_prl_flag(self, instance,flag):
        '''set Auto update flag for CDMA PRL by AT command AT*AUTOPRL=[0/1]  
           
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            flag: 0 -disable 1 - enable
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set  Auto update flag for CDMA PRL by AT command")
        cmd="AT*AUTOPRL="+flag
        return self.assign(instance,cmd) 
     
    def get_auto_prl_frequency(self, instance):
        '''Query Auto update frequency for CDMA PRL by AT command AT*AUTOPRLFREQ?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            PRL auto update frequency (# of days)
        '''
        
        basic_airlink.slog("Step:  get Auto update frequency for CDMA PRL by AT command")
        cmd="AT*AUTOPRLFREQ?"
        return self.query(instance,cmd)              

    def set_auto_prl_frequency(self, instance,frequency):
        '''set Auto update frequency for CDMA PRL by AT command AT*AUTOPRLFREQ=[0/1]  
           
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            frequency  :  how often the PRL shall be auto updated (#of days)
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set  Auto update frequency for CDMA PRL by AT command")
        cmd="AT*AUTOPRLFREQ="+frequency
        return self.assign(instance,cmd)  

    def get_avms_account(self, instance):
        '''Query AVMS account by AT command AT*AVMS_ACCOUNT?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            AVMS account
        '''
        basic_airlink.slog("Step:  get AVMS account by AT command")
        cmd="AT*AVMS_ACCOUNT?"
        return self.query(instance,cmd)              

    def set_avms_account(self, instance,account):
        '''set  AVMS account by AT command AT*AVMS_ACCOUNT=[account]  
           
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            account:  AVMS account
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set AVMS account by AT command")
        cmd="AT*AVMS_ACCOUNT="+account
        return self.assign(instance,cmd) 
     
    def get_avms_enable_flag(self, instance):
        '''Query AVMS enable flag by AT command AT*AVMS_ENABLE?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            0/1
        '''
        
        basic_airlink.slog("Step:  get Auto update flag for CDMA PRL by AT command")
        cmd="AT*AVMS_ENABLE?"
        return self.query(instance,cmd)              

    def set_avms_enable_flag(self, instance,flag):
        '''set AVMS enable flag by AT command AT*AVMS_ENABLE=[0/1]  
           
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            flag: 0 -disable 1 - enable
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set  AVMS enable flag by AT command")
        cmd="AT*AVMS_ENABLE="+flag
        return self.assign(instance,cmd) 
 
    def get_avms_interval(self, instance):
        '''Query AVMS heardbeat interval by AT command AT*AVMS_INTERVAL?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            AVMS interval
        '''
        basic_airlink.slog("Step:  get AVMS heardbeat interval by AT command")
        cmd="AT*AVMS_INTERVAL?"
        return self.query(instance,cmd)              

    def set_avms_interval(self, instance, interval):
        '''set  AVMS heardbeat interval by AT command AT*AVMS_INTERVAL=[#of s]  
           
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            flag: 0 -disable 1 - enable
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set AVMS heardbeat interval by AT command")
        cmd="AT*AVMS_INTERVAL="+interval
        return self.assign(instance,cmd) 

    def get_avms_name(self, instance):
        '''Query AVMS name by AT command AT*AVMS_NAME?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            AVMS name
        '''
        
        basic_airlink.slog("Step:  get AVMS name by AT command")
        cmd="AT*AVMS_NAME?"
        return self.query(instance,cmd)              

    def set_avms_name(self, instance,name):
        '''set  AVMS name by AT command AT*AVMS_NAME=[name]  
           
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            name:  AVMS name
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set AVMS name by AT command")
        cmd="AT*AVMS_NAME="+name
        return self.assign(instance,cmd) 

    def get_avms_server(self, instance):
        '''Query AVMS server by AT command AT*AVMS_SERVER?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            AVMS server URL
        '''
        
        basic_airlink.slog("Step:  get AVMS server by AT command")
        cmd="AT*AVMS_SERVER?"
        return self.query(instance,cmd)              

    def set_avms_server(self, instance,server_url):
        '''set  AVMS server by AT command AT*AVMS_SERVER=[url]  
           
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            ipaddress:  AVMS server URL
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set AVMS server URL by AT command")
        cmd="AT*AVMS_SERVER="+server_url
        return self.assign(instance,cmd)            

    def get_avms_status(self, instance):
        '''Query AVMS status by AT command AT*AVMS_STATUS?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            AVMS status
        '''
        basic_airlink.slog("Step:  get AVMS status by AT command")
        cmd="AT*AVMS_STATUS?"
        return self.query(instance,cmd)
 
    def get_avms_id(self, instance):
        '''Query AVMS ID by AT command AT*AVMSID?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            AVMS ID
        '''
        basic_airlink.slog("Step:  get AVMS ID by AT command")
        cmd="AT*AVMSID?"
        return self.query(instance,cmd)              

    def set_avms_id(self, instance, identity):
        '''set  AVMS ID by AT command AT*AVMSID=[identity]  
           
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            identity:  AVMS ID
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set AVMS identity by AT command")
        cmd="AT*AVMSID="+identity
        return self.assign(instance,cmd)  

    def get_avms_identity(self, instance):
        '''Query AVMS ID by AT command AT*AVMS_IDENTITY?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            AVMS ID
        '''
        basic_airlink.slog("Step:  get AVMS ID by AT command")
        cmd="AT*AVMS_IDENTITY?"
        return self.query(instance,cmd)              

    def set_avms_identity(self, instance, identity):
        '''set  AVMS ID by AT command AT*AVMSID=[identity]  
           
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            identity:  AVMS ID
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set AVMS identity by AT command")
        cmd="AT*AVMS_IDENTITY="+identity
        return self.assign(instance,cmd)  
 
    def get_band(self, instance):
        '''Query cuurent band by AT command AT*BAND?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            BAND number in use
        '''
        basic_airlink.slog("Step:  get current BAND by AT command")
        cmd="AT*BAND?"
        return self.query(instance,cmd)              

    def get_for_band(self, instance):
        '''Query band by AT command AT!BAND?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            BAND number
        '''
        basic_airlink.slog("Step:  get for BAND by AT command")
        cmd="AT!BAND?"
        return self.query(instance,cmd)    
    
    def set_for_band(self, instance, band_no):
        '''set BAND by AT command AT!BAND=[band#]  
           
        Args: 
            instance   : Telnet/SSH/Serial connection instance 
            band_no:  band number
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set for BAND by AT command")
        cmd="AT!BAND="+band_no
        return self.assign(instance,cmd) 
                         
    def get_ppdevid(self, instance):
        '''Query the PP device ID by AT command AT*PPDEVID?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            flag to enable for device ID to use with GPS reports (or UDP PAD) 
        '''
        basic_airlink.slog("Step:  get device ID enable by AT command")
        cmd="AT*PPDEVID?"
        return self.query(instance,cmd)          

    def set_ppdevid(self, instance, flag):
        '''enable/disable for device ID to use with GPS reports by AT command AT*PPDEVID=[2|1|0]
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            flag: 
                2- ESN or IMSI,  1= phone number, 0 = none/not set
                
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  enable for device ID to use with GPS reports AT command")
        cmd="AT*PPDEVID="+flag
        return self.assign(instance,cmd)    
    
    def get_evdo_data_service(self, instance):
        '''Query EVDO data service by AT command AT*EVDODATASERV?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            EVDO data service 
        '''
        
        basic_airlink.slog("Step:  get EVDO data service by AT command AT*EVDODATASERV?")
        cmd="AT*EVDODATASERV?"
        return self.query(instance,cmd)          
    
    def set_evdo_data_service(self, instance, flag ):
        ''' set EVDO data service by AT command AT*EVDODATASERV=[4|3|2|1|0]
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            flag: [4|3|2|1|0]   
                4 - LTE only (GX440)
                3 - CDMA only (GX400)
                2 - 1x only (GX400/LS300)
                1 - EV-DO only (GX400/LS300)
                0 -
                
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set EVDO data service AT command")
        cmd="AT*EVDODATASERV="+flag
        return self.assign(instance,cmd)    
 
    def get_evdo_diversity(self, instance):
        '''Query EVDO diversity by AT command AT*EVDODIVERSITY?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            EVDO diversity antenna
        '''
        
        basic_airlink.slog("Step:  get EVDO diversity antenna by AT command")
        cmd="AT*EVDODIVERSITY?"
        return self.query(instance,cmd)          
    
    def set_evdo_diversity(self, instance, flag ):
        ''' set EVDO diversity by AT command AT*EVDODIVERSITY=[1|0]
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            flag:
                1 - Enable support for diversity anntenna (default)
                0 - Disable
                
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set EVDO diversity  AT command")
        cmd="AT*EVDODIVERSITY="+flag
        return self.assign(instance,cmd)    

    def get_evdo_roam_perf(self, instance):
        '''Query CDMA/LTE roaming perference by AT command AT*EVDOROAMPERF?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Network roaming perferences: Automatic, Home only
        '''
        
        basic_airlink.slog("Step:  get EVDO diversity by AT command")
        cmd="AT*EVDODIVERSITY?"
        return self.query(instance,cmd)          
    
    def set_evdo_roam_perf(self, instance, flag ):
        ''' set CDMA/LTE roaming perference by AT command AT*EVDODIVERSITY=[1|0]
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            flag:
                1 - Home Only
                0 - Automatic
                
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set CDMA/LTE roaming perference by AT command")
        cmd="AT*EVDODIVERSITY="+flag
        return self.assign(instance,cmd)    

    def fw_update(self, instance, ftp_server_ip, username, password, fw_filename=""):
        ''' FW update by internal AT command AT*FWUPDATA=<server_ip>,<username>,<password>
        need to rename build *.bin file to fw.bin in FTP server shared folder
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            ftp_server_ip: FTP server IP address (local or remote)
            username: user name to login to FTP server
            password: password to login to FTP server
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  Update FW by AT command")
        cmd="AT*FWUPDATE= "+ftp_server_ip +","+username+","+password+","+fw_filename
        ret = instance.command(cmd)
        ret_str = ''.join(ret)
        basic_airlink.slog(ret_str)
        return ret_str   
 
    def fw_rm_update(self, instance, ftp_server_ip, username, password, fw_filename="", rm_filename=""):
        ''' Update FW and RM by internal new AT command 
            AT*FWRMUPDATA=<server_ip>,<username>,<password>,<fw_filename>,<rm_filename>
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            ftp_server_ip: FTP server IP address
            username: user name to login to FTP server
            password: password to login to FTP server
            fw_filename: FW file name 
            rm_filename: RM file name
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  Update FW and RM by AT command")
        cmd="AT*FWRMUPDATE="+ftp_server_ip +","+username+","+password +"," +fw_filename+","+rm_filename
        ret = instance.command(cmd)
        ret_str = ''.join(ret)
        basic_airlink.slog(ret_str)
        return ret_str      
    
    def rm_update(self, instance, ftp_server_ip, username, password, rm_filename):
        ''' RM update by internal new AT command 
            AT*RMUPDATE=<server_ip>,<username>,<password>,<rm_filename>
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            server IP: FTP server IP address
            username: user name to login to FTP server
            password: password to login to FTP server
            rm_filename: RM file name (FTP server shared folder)
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  Update RM by AT command")
        cmd="AT*RMUPDATE="+ftp_server_ip +","+username+","+password +"," +rm_filename       
        ret = instance.command(cmd)
        ret_str = ''.join(ret)
        basic_airlink.slog(ret_str)
        
        return ret_str

    def template_upload(self, instance, ftp_server_ip, username, password, template_filename):
        ''' RM update by internal new AT command 
            AT*TPLUPDATE=<server_ip>,<username>,<password>,<template_filename>
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            server IP: FTP server IP address
            username: user name to login to FTP server
            password: password to login to FTP server
            template_filename: template file name (xml file in FTP server shared folder)
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  Upload template by AT command")
        cmd="AT*TPLUPDATE="+ftp_server_ip +","+username+","+password +"," +template_filename
        return self.assign(instance,cmd)   
        
    def get_global_id(self, instance):
        '''Query global ID by AT command AT*GLOBALID?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Global ID for AVMS and others
        '''
        
        basic_airlink.slog("Step:  get global ID by AT command")
        cmd="AT*GLOBALID?"
        return self.assign(instance,cmd)       
        
    def get_gps_data(self, instance):
        ''' Get GPS data by AT command  AT*GPSDATA?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            GPS data
        '''
        
        basic_airlink.slog("Step:  get GPS data by AT command")
        cmd="AT*GPSDATA?"
        return self.query(instance,cmd)       
    
    def get_gsm_hangup_to_reset(self, instance):
        '''GSM related, forces the RM to reset when it disconnects by AT command AT*HANGUPTORESET?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            flag to forces the RM to reset when it disconnects 
        '''
        basic_airlink.slog("Step:  get flag to forces the RM to reset when it disconnects by AT command")
        cmd="AT*HANGUPTORESET?"
        return self.query(instance,cmd)           
    
    def set_gsm_hangup_to_reset(self, instance, flag):
        '''Set flag to forces the RM to reset when it disconnects by AT command AT*HANGUPTORESET=[0|1]
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            flag:
                1 - Enable
                0 - Disable      
                  
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set flag to forces the RM to reset when it disconnects by AT command")
        cmd="AT*HANGUPTORESET="+flag
        return self.assign(instance,cmd)
    
    def get_ip_manager_server_address(self, instance, ip_manager_server_num):
        ''' Query IP manager server IP or FQDN by AT command 
            AT*IPMANAGER1?
            AT*IPMANAGER2?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IP manager server address
        '''
        
        basic_airlink.slog("Step:  get IP manager server address when it disconnects by AT command")
        cmd="AT*IPMANAGER"+ip_manager_server_num+"?"
        return self.query(instance,cmd)          
    
    def set_ip_manager_server_address(self, instance, ip_manager_server_num, ip_manager_server_address):
        '''Set IP manager server IP or FQDN by AT command 
            AT*IPMANAGER1=<ip address or FQDN>
            AT*IPMANAGER2=<ip address or FQDN>    
             
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            ip_manager_server_num:
                1 - 1st IP manager server 
                2 - 2nd IP manager server 
            ip_manager_server:    IP address or FQDN   
                     
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IP manager server IP or FQDN by AT command")
        cmd="AT*IPMANAGER"+ip_manager_server_num+"="+ip_manager_server_address
        return self.assign(instance,cmd)    
    
    def get_ip_manager_server_key(self, instance, ip_manager_server_num):
        ''' Query IP manager server key by AT command 
            AT*IPMGRKEY1?
            AT*IPMGRKEY2?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IP manager server address
        '''
        
        basic_airlink.slog("Step:  get IP manager server address when it disconnects by AT command")
        cmd="AT*IPMGRKEY"+ip_manager_server_num+"?"
        return self.query(instance,cmd)       
    
    def set_ip_manager_server_key(self, instance, ip_manager_server_num, ip_manager_server_key):
        '''Set IP manager server KEY by AT command 
            AT*IPMGRKEY1=<password or key>
            AT*IPMGRKEY2=<password or key>  
               
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            ip_manager_server_num:
                1 - 1st IP manager server 
                2 - 2nd IP manager server 
            ip_manager_server_key:    password or key     
                   
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IP manager server key by AT command")
        cmd="AT*IPMGRKEY"+ip_manager_server_num+"="+ip_manager_server_key
        return self.assign(instance,cmd)    
    
    def get_ip_manager_update_interval(self, instance, ip_manager_server_num):
        ''' Query IP manager update interval by AT command 
            AT*IPMGRUPDATE1?
            AT*IPMGRUPDATE2?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IP manager update interval
        '''
        
        basic_airlink.slog("Step:  get IP manager update interval by AT command")
        cmd="AT*IPMGRUPDATE"+ip_manager_server_num+"?"
        return self.assign(instance,cmd)       
    
    def set_ip_manager_update_interval(self, instance, ip_manager_server_num, ip_manager_update_interval):
        '''Set IP manager update interval by AT command 
            AT*IPMGRUPDATE1=<update interval 0 - 255>
            AT*IPMGRUPDATE2=<update interval 0 - 255>   
              
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            ip_manager_server_num:
                1 - 1st IP manager server 
                2 - 2nd IP manager server 
            ip_manager_update_interval:    update interval    
                   
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IP manager update interval by AT command")
        cmd="AT*IPMGRKEY"+ip_manager_server_num+"="+ip_manager_update_interval
        return self.assign(instance,cmd)    

    def get_ip_ping_interval(self, instance):
        ''' Query IP ping interval by AT command AT*IPPING?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IP ping interval
        '''
        
        basic_airlink.slog("Step:  get IP ping interval by AT command")
        cmd="AT*IPPING?"
        return self.query(instance,cmd)       

    def set_ip_ping_interval(self, instance, keep_alive_interval):
        '''Set IP ping interval by AT command AT*IPPING=0|15-255 
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            keep_alive_interval:
                0 - disable 
                15- 255 (minutes) keep alive interval
                
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IP ping interval by AT command")
        cmd="AT*IPPING="+keep_alive_interval
        return self.assign(instance,cmd)    
    
    def get_ip_ping_address(self, instance):
        ''' Query IP ping address by AT command AT*IPPINGADDR?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IP ping address
        '''
        
        basic_airlink.slog("Step:  get IP ping address by AT command")
        cmd="AT*IPPINGADDR?"
        return self.query(instance,cmd)           
    
    def set_ip_ping_address(self, instance, keep_alive_address):
        '''Set IP ping IP or FQDN by AT command AT*IPPING=0|15-255 
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            keep_alive_address: IP address or FQDN
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IP ping IP or FQDN by AT command")
        cmd="AT*IPPINGADDR="+keep_alive_address
        return self.assign(instance,cmd)    
        
    def get_ip_ping_force(self, instance):
        ''' Query IP ping force by AT command AT*IPPINGFORCE?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IP ping force enable/disable
        '''
        
        basic_airlink.slog("Step:  get IP ping force enable or disable by AT command")
        cmd="AT*IPPINGFORCE?"
        return self.query(instance,cmd)          
    
    def set_ip_ping_force(self, instance, flag):
        '''Set IP ping force by AT command AT*IPPINGFROCE=[0|1]
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            flag: 0 - disable, 1 - enable
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IP ping force by AT command")
        cmd="AT*IPPINGFORCE="+flag
        return self.assign(instance,cmd)    
    
    def get_ipsec_auth(self, instance, vpn_no):
        ''' Query IPsec authentication by AT command 
            AT*IPSEC1_AUTH?
            AT*IPSEC2_AUTH?
            AT*IPSEC3_AUTH?
            AT*IPSEC4_AUTH?
            AT*IPSEC5_AUTH?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC authentication
        '''
        basic_airlink.slog("Step:  get IPsec authentication by AT command")
        cmd="AT*IPSEC"+vpn_no+"_AUTH?"
        return self.query(instance,cmd)             
    
    def set_ipsec_auth(self, instance, vpn_no, ipsec_auth):
        '''Set IP ping force by AT command 
            AT*IPSEC1_AUTH=[number]
            AT*IPSEC2_AUTH=[number]
            AT*IPSEC3_AUTH=[number]
            AT*IPSEC4_AUTH=[number]        
            AT*IPSEC5_AUTH=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_auth:  authentication mode
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set IPSEC auth by AT command")
        cmd="AT*IPSEC"+vpn_no+"_AUTH="+ipsec_auth
        return self.assign(instance,cmd)    
    
    def get_ipsec_dh(self, instance, vpn_no):
        ''' Query IPsec authentication by AT command 
            AT*IPSEC1_DH?
            AT*IPSEC2_DH?
            AT*IPSEC3_DH?
            AT*IPSEC4_DH?
            AT*IPSEC5_DH?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC dh
        '''
        basic_airlink.slog("Step:  get IPsec DH by AT command")
        cmd="AT*IPSEC"+vpn_no+"_DH?"
        return self.query(instance,cmd)          
    
    def set_ipsec_dh(self, instance, vpn_no, ipsec_dh):
        '''Set IPSEC DU by AT command 
            AT*IPSEC1_DH=[number]
            AT*IPSEC2_DH=[number]
            AT*IPSEC3_DH=[number]
            AT*IPSEC4_DH=[number]
            AT*IPSEC5_DH=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_dh:  
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IPSEC DU by AT command")
        cmd="AT*IPSEC"+vpn_no+"_DH="+ipsec_dh
        return self.assign(instance,cmd)          
    
    def get_ipsec_encrypt(self, instance, vpn_no):
        ''' Query IPSEC encryption by AT command 
            AT*IPSEC1_ENCRYPT?
            AT*IPSEC2_ENCRYPT?
            AT*IPSEC3_ENCRYPT?
            AT*IPSEC4_ENCRYPT?
            AT*IPSEC5_ENCRYPT?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC encryption
        '''
        basic_airlink.slog("Step:  get IPSEC encryption by AT command")
        cmd="AT*IPSEC"+vpn_no+"_ENCRYPT?"
        return self.query(instance,cmd)          
    
    def set_ipsec_encrypt(self, instance, vpn_no, ipsec_encrypt):
        '''Set IPSEC encryption by AT command 
            AT*IPSEC1_ENCRYPT=[number]
            AT*IPSEC2_ENCRYPT=[number]
            AT*IPSEC3_ENCRYPT=[number]
            AT*IPSEC4_ENCRYPT=[number]
            AT*IPSEC5_ENCRYPT=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_encrypt:  IPSEC encryption
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set IPSEC encryption by AT command")
        cmd="AT*IPSEC"+vpn_no+"_ENCRYPT="+ipsec_encrypt
        return self.assign(instance,cmd)          
        
    def get_ipsec_gateway(self, instance, vpn_no):
        ''' Query IPSEC gateway by AT command 
            AT*IPSEC1_GATEWAY?
            AT*IPSEC2_GATEWAY?
            AT*IPSEC3_GATEWAY?
            AT*IPSEC4_GATEWAY?
            AT*IPSEC5_GATEWAY?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC gateway address
        '''
        basic_airlink.slog("Step:  get IPSEC gateway by AT command")
        cmd="AT*IPSEC"+vpn_no+"_GATEWAY?"
        return self.query(instance,cmd)          
    
    def set_ipsec_gateway(self, instance, vpn_no, ipsec_gateway):
        '''Set IPSEC gateway by AT command 
            AT*IPSEC1_GATEWAY=[ address]
            AT*IPSEC2_GATEWAY=[ address]
            AT*IPSEC3_GATEWAY=[ address]
            AT*IPSEC4_GATEWAY=[ address]
            AT*IPSEC5_GATEWAY=[ address]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_gateway:  IPSEC gateway IP address
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set IPSEC gateway address by AT command")
        cmd="AT*IPSEC"+vpn_no+"_GATEWAY="+ipsec_gateway
        return self.assign(instance,cmd)          
        
    def get_ipsec_ike_auth(self, instance, vpn_no):
        ''' Query IPSEC IKE authentication by AT command 
            AT*IPSEC1_IKE_AUTH?
            AT*IPSEC2_IKE_AUTH?
            AT*IPSEC3_IKE_AUTH?
            AT*IPSEC4_IKE_AUTH?
            AT*IPSEC5_IKE_AUTH?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC IKE authentication
        '''
        
        basic_airlink.slog("Step:  get IPSEC IKE authentication by AT command")
        cmd="AT*IPSEC"+vpn_no+"_IKE_AUTH?"
        return self.query(instance,cmd)           
    
    def set_ipsec_ike_auth(self, instance, vpn_no, ipsec_ike_auth):
        '''Set IPSEC IKE authentication by AT command 
            AT*IPSEC1_IKE_AUTH=[number]
            AT*IPSEC2_IKE_AUTH=[number]
            AT*IPSEC3_IKE_AUTH=[number]
            AT*IPSEC4_IKE_AUTH=[number]
            AT*IPSEC5_IKE_AUTH=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_auth:  authentication mode
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set IPSEC IKE authentication by AT command")
        cmd="AT*IPSEC"+vpn_no+"_IKE_AUTH="+ipsec_ike_auth
        return self.assign(instance,cmd)          

    def get_ipsec_ike_dh(self, instance, vpn_no):
        ''' Query IPSEC IKE DH by AT command 
            AT*IPSEC1_IKE_DH?
            AT*IPSEC2_IKE_DH?
            AT*IPSEC3_IKE_DH?
            AT*IPSEC4_IKE_DH?
            AT*IPSEC5_IKE_DH?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC IKE DH
        '''
        
        basic_airlink.slog("Step:  get IPSEC IKE DU by AT command")
        cmd="AT*IPSEC"+vpn_no+"_IKE_DH?"
        return self.query(instance,cmd)    
    
    def set_ipsec_ike_dh(self, instance, vpn_no, ipsec_ike_dh):
        '''Set IPSEC IKE DU by AT command 
            AT*IPSEC1_IKE_DH=[number]
            AT*IPSEC2_IKE_DH=[number]
            AT*IPSEC3_IKE_DH=[number]
            AT*IPSEC4_IKE_DH=[number]
            AT*IPSEC5_IKE_DH=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_ike_dh:  
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IPSEC IKE DH by AT command")
        cmd="AT*IPSEC"+vpn_no+"_IKE_DH="+ipsec_ike_dh
        return self.assign(instance,cmd)    

    def get_ipsec_ike_encrypt(self, instance, vpn_no):
        ''' Query IPSEC IKE encryption by AT command 
            AT*IPSEC1_IKE_ENCRYPT?
            AT*IPSEC2_IKE_ENCRYPT?
            AT*IPSEC3_IKE_ENCRYPT?
            AT*IPSEC4_IKE_ENCRYPT?
            AT*IPSEC5_IKE_ENCRYPT?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC IKE encryption
        '''
        basic_airlink.slog("Step:  get IPSEC IKE encryption by AT command")
        cmd="AT*IPSEC"+vpn_no+"_IKE_ENCRYPT?"
        return self.query(instance,cmd)        
    
    def set_ipsec_ike_encrypt(self, instance, vpn_no, ipsec_ike_encrypt):
        '''Set IPSEC IKE encryption by AT command 
            AT*IPSEC1_IKE_ENCRYPT=[number]
            AT*IPSEC2_IKE_ENCRYPT=[number]
            AT*IPSEC3_IKE_ENCRYPT=[number]
            AT*IPSEC4_IKE_ENCRYPT=[number]
            AT*IPSEC5_IKE_ENCRYPT=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_ike_encrypt:  IPSEC IKE encryption
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set IPSEC IKE encryption by AT command")
        cmd="AT*IPSEC"+vpn_no+"_IKE_ENCRYPT="+ipsec_ike_encrypt
        return self.assign(instance,cmd)
       
    def get_ipsec_ike_lifetime(self, instance, vpn_no):
        ''' Query IPSEC IKE life time by AT command 
            AT*IPSEC1_IKE_LIFETIME?
            AT*IPSEC2_IKE_LIFETIME?
            AT*IPSEC3_IKE_LIFETIME?
            AT*IPSEC4_IKE_LIFETIME?
            AT*IPSEC5_IKE_LIFETIME?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC IKE life time
        '''
        
        basic_airlink.slog("Step:  get IPSEC IKE life time by AT command")
        cmd="AT*IPSEC"+vpn_no+"_IKE_LIFETIME?"
        return self.query(instance,cmd)    
    
    def set_ipsec_ike_lifetime(self, instance, vpn_no, ipsec_ike_life_time):
        '''Set IPSEC IKE life time by AT command 
            AT*IPSEC1_IKE_LIFETIME=[number]
            AT*IPSEC2_IKE_LIFETIME=[number]
            AT*IPSEC3_IKE_LIFETIME=[number]
            AT*IPSEC4_IKE_LIFETIME=[number]
            AT*IPSEC5_IKE_LIFETIME=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_ike_life_time:  IPSEC IKE life time
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IPSEC IKE life time by AT command")
        cmd="AT*IPSEC"+vpn_no+"_IKE_LIFETIME="+ipsec_ike_life_time
        return self.assign(instance,cmd)
   
    def get_ipsec_lifetime(self, instance, vpn_no):
        ''' Query IPSEC life time by AT command 
            AT*IPSEC1_LIFETIME?
            AT*IPSEC2_LIFETIME?
            AT*IPSEC3_LIFETIME?
            AT*IPSEC4_LIFETIME?
            AT*IPSEC5_LIFETIME?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC life time
        '''
        
        basic_airlink.slog("Step:  get IPSEC life time by AT command")
        cmd="AT*IPSEC"+vpn_no+"_LIFETIME?"
        return self.query(instance,cmd)    
    
    def set_ipsec_lifetime(self, instance, vpn_no, ipsec_life_time):
        '''Set IPSEC life time by AT command 
            AT*IPSEC1_LIFETIME=[number]
            AT*IPSEC2_LIFETIME=[number]
            AT*IPSEC3_LIFETIME=[number]
            AT*IPSEC4_LIFETIME=[number]
            AT*IPSEC5_LIFETIME=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_life_time:  IPSEC life time
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IPSEC life time by AT command")
        cmd="AT*IPSEC"+vpn_no+"_LIFETIME="+ipsec_life_time
        return self.assign(instance,cmd)
               
    def get_ipsec_local_addr(self, instance, vpn_no):
        ''' Query IPSEC local address by AT command 
            AT*IPSEC1_LOCAL_ADDR?
            AT*IPSEC2_LOCAL_ADDR?
            AT*IPSEC3_LOCAL_ADDR?
            AT*IPSEC4_LOCAL_ADDR?
            AT*IPSEC5_LOCAL_ADDR?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC local address
        '''
        
        basic_airlink.slog("Step:  get IPSEC local address by AT command")
        cmd="AT*IPSEC"+vpn_no+"_LOCAL_ADDR?"
        return self.query(instance,cmd)    

    def set_ipsec_local_addr(self, instance, vpn_no, ipsec_local_addr):
        '''Set IPSEC local address by AT command 
            AT*IPSEC1_LOCAL_ADDR=[address]
            AT*IPSEC2_LOCAL_ADDR=[address]
            AT*IPSEC3_LOCAL_ADDR=[address]
            AT*IPSEC4_LOCAL_ADDR=[address]
            AT*IPSEC5_LOCAL_ADDR=[address]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_local_addr:  IPSEC local address
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IPSEC local address by AT command")
        cmd="AT*IPSEC"+vpn_no+"_LOCAL_ADDR="+ipsec_local_addr
        return self.assign(instance,cmd)
              
    def get_ipsec_local_addr_mask(self, instance, vpn_no):
        ''' Query IPSEC local address mask by AT command 
            AT*IPSEC1_LOCAL_ADDR_MASK?
            AT*IPSEC2_LOCAL_ADDR_MASK?
            AT*IPSEC3_LOCAL_ADDR_MASK?
            AT*IPSEC4_LOCAL_ADDR_MASK?
            AT*IPSEC5_LOCAL_ADDR_MASK?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC local address mask
        '''
        
        basic_airlink.slog("Step:  get IPSEC local address mask by AT command")
        cmd="AT*IPSEC"+vpn_no+"_LOCAL_ADDR_MASK?"
        return self.query(instance,cmd)    

    def set_ipsec_local_addr_mask(self, instance, vpn_no, ipsec_local_addr_mask):
        '''Set IPSEC local address mask by AT command 
            AT*IPSEC1_LOCAL_ADDR_MASK=[address]
            AT*IPSEC2_LOCAL_ADDR_MASK=[address]
            AT*IPSEC3_LOCAL_ADDR_MASK=[address]
            AT*IPSEC4_LOCAL_ADDR_MASK=[address]
            AT*IPSEC5_LOCAL_ADDR_MASK=[address]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_local_addr:  IPSEC local address mask
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IPSEC local address mask by AT command")
        cmd="AT*IPSEC"+vpn_no+"_LOCAL_ADDR_MASK="+ipsec_local_addr_mask
        return self.assign(instance,cmd)

    def get_ipsec_local_addr_type(self, instance, vpn_no):
        ''' Query IPSEC local address type by AT command 
            AT*IPSEC1_LOCAL_ADDR_TYPE?
            AT*IPSEC2_LOCAL_ADDR_TYPE?
            AT*IPSEC3_LOCAL_ADDR_TYPE?
            AT*IPSEC4_LOCAL_ADDR_TYPE?
            AT*IPSEC5_LOCAL_ADDR_TYPE?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC local address type
        '''
        
        basic_airlink.slog("Step:  get IPSEC local address type by AT command")
        cmd="AT*IPSEC"+vpn_no+"_LOCAL_ADDR_TYPE?"
        return self.query(instance,cmd)    
    
    def set_ipsec_local_addr_type(self, instance, vpn_no, ipsec_local_addr_type):
        '''Set IPSEC local address type by AT command 
            AT*IPSEC1_LOCAL_ADDR_TYPE=[number]
            AT*IPSEC2_LOCAL_ADDR_TYPE=[number]
            AT*IPSEC3_LOCAL_ADDR_TYPE=[number]
            AT*IPSEC4_LOCAL_ADDR_TYPE=[number]
            AT*IPSEC5_LOCAL_ADDR_TYPE=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_local_addr:  IPSEC local address type
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IPSEC local address type by AT command")
        cmd="AT*IPSEC"+vpn_no+"_LOCAL_ADDR_TYPE="+ipsec_local_addr_type
        return self.assign(instance,cmd)

    def get_ipsec_local_id(self, instance, vpn_no):
        ''' Query IPSEC local ID by AT command  (ALLX-4110)
            AT*IPSEC1_LOCAL_ID?
            AT*IPSEC2_LOCAL_ID?
            AT*IPSEC3_LOCAL_ID?
            AT*IPSEC4_LOCAL_ID?
            AT*IPSEC5_LOCAL_ID?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC local ID
        '''
        
        basic_airlink.slog("Step:  get IPSEC local ID by AT command")
        cmd="AT*IPSEC"+vpn_no+"_LOCAL_ID?"
        return self.query(instance,cmd)    
    
    def set_ipsec_local_id(self, instance, vpn_no, ipsec_local_id):
        '''Set IPSEC local ID by AT command 
            AT*IPSEC1_LOCAL_ID=[number]
            AT*IPSEC2_LOCAL_ID=[number]
            AT*IPSEC3_LOCAL_ID=[number]
            AT*IPSEC4_LOCAL_ID=[number]
            AT*IPSEC5_LOCAL_ID=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_local_id:  IPSEC local ID
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IPSEC local ID by AT command")
        cmd="AT*IPSEC"+vpn_no+"_LOCAL_ID="+ipsec_local_id
        return self.assign(instance,cmd)

    def get_ipsec_local_id_type(self, instance, vpn_no):
        ''' Query IPSEC local ID type by AT command 
            AT*IPSEC1_LOCAL_ID_TYPE?
            AT*IPSEC2_LOCAL_ID_TYPE?
            AT*IPSEC3_LOCAL_ID_TYPE?
            AT*IPSEC4_LOCAL_ID_TYPE?
            AT*IPSEC5_LOCAL_ID_TYPE?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC local ID type
        '''
        
        basic_airlink.slog("Step:  get IPSEC local ID type by AT command")
        cmd="AT*IPSEC"+vpn_no+"_LOCAL_ID_TYPE?"
        return self.query(instance,cmd)    
    
    def set_ipsec_local_id_type(self, instance, vpn_no, ipsec_local_id_type):
        '''Set IPSEC local ID type by AT command 
            AT*IPSEC1_LOCAL_ID_TYPE=[number]
            AT*IPSEC2_LOCAL_ID_TYPE=[number]
            AT*IPSEC3_LOCAL_ID_TYPE=[number]
            AT*IPSEC4_LOCAL_ID_TYPE=[number]
            AT*IPSEC5_LOCAL_ID_TYPE=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_local_id:  IPSEC local ID type
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IPSEC local ID type by AT command")
        cmd="AT*IPSEC"+vpn_no+"_LOCAL_ID_TYPE="+ipsec_local_id_type
        return self.assign(instance,cmd)

    def get_ipsec_neg_mode(self, instance, vpn_no):
        ''' Query IPSEC neg mode by AT command 
            AT*IPSEC1_NEG_MDOE?
            AT*IPSEC2_NEG_MDOE?
            AT*IPSEC3_NEG_MDOE?
            AT*IPSEC4_NEG_MDOE?
            AT*IPSEC5_NEG_MDOE?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC neg mode
        '''
        
        basic_airlink.slog("Step:  get IPSEC neg mode by AT command")
        cmd="AT*IPSEC"+vpn_no+"_NEG_MODE?"
        return self.query(instance,cmd)    

    def set_ipsec_neg_mode(self, instance, vpn_no, ipsec_neg_mode):
        '''Set IPSEC neg mode by AT command 
            AT*IPSEC1_NEG_MODE=[number]
            AT*IPSEC2_NEG_MODE=[number]
            AT*IPSEC3_NEG_MODE=[number]
            AT*IPSEC4_NEG_MODE=[number]
            AT*IPSEC5_NEG_MODE=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_neg_mode:  IPSEC neg mode
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IPSEC neg mode by AT command")
        cmd="AT*IPSEC"+vpn_no+"_NEG_MODE="+ipsec_neg_mode
        return self.assign(instance,cmd)
    
    def get_ipsec_pfs(self, instance, vpn_no):
        ''' Query IPSEC PFS by AT command 
            AT*IPSEC1_PFS?
            AT*IPSEC2_PFS?
            AT*IPSEC3_PFS?
            AT*IPSEC4_PFS?
            AT*IPSEC5_PFS?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Perfect Forward Secrecy
        '''
        
        basic_airlink.slog("Step:  get IPSEC PFS by AT command")
        cmd="AT*IPSEC"+vpn_no+"_PFS?"
        return self.query(instance,cmd)      
    
    def set_ipsec_pfs(self, instance, vpn_no, pfs_value):
        '''Set IPSEC PFS by AT command 
            AT*IPSEC1_PFS=[number]
            AT*IPSEC2_PFS=[number]
            AT*IPSEC3_PFS=[number]
            AT*IPSEC4_PFS=[number]
            AT*IPSEC5_PFS=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_pfs:  IPSEC local ID type
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IPSEC Perfect Forward Secrecy by AT command")
        cmd="AT*IPSEC"+vpn_no+"_PFS="+pfs_value
        return self.assign(instance,cmd)
             
    def get_ipsec_remote_addr(self, instance, vpn_no):
        ''' Query IPSEC remote address by AT command 
            AT*IPSEC1_REMOTE_ADDR?
            AT*IPSEC2_REMOTE_ADDR?
            AT*IPSEC3_REMOTE_ADDR?
            AT*IPSEC4_REMOTE_ADDR?
            AT*IPSEC5_REMOTE_ADDR?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC remote address
        '''
        
        basic_airlink.slog("Step:  get IPSEC remote address by AT command")
        cmd="AT*IPSEC"+vpn_no+"_REMOTE_ADDR?"
        return self.query(instance,cmd)    

    def set_ipsec_remote_addr(self, instance, vpn_no, ipsec_remote_addr):
        '''Set IPSEC remote address by AT command 
            AT*IPSEC1_REMOTE_ADDR=[address]
            AT*IPSEC2_REMOTE_ADDR=[address]
            AT*IPSEC3_REMOTE_ADDR=[address]
            AT*IPSEC4_REMOTE_ADDR=[address]
            AT*IPSEC5_REMOTE_ADDR=[address]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_remote_addr:  IPSEC remote address
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IPSEC remote address by AT command")
        cmd="AT*IPSEC"+vpn_no+"_REMOTE_ADDR="+ipsec_remote_addr
        return self.assign(instance,cmd)
  
    def get_ipsec_remote_addr_mask(self, instance, vpn_no):
        ''' Query IPSEC remote address mask by AT command 
            AT*IPSEC1_REMOTE_ADDR_MASK?
            AT*IPSEC2_REMOTE_ADDR_MASK?
            AT*IPSEC3_REMOTE_ADDR_MASK?
            AT*IPSEC4_REMOTE_ADDR_MASK?
            AT*IPSEC5_REMOTE_ADDR_MASK?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC remote address mask
        '''
        
        basic_airlink.slog("Step:  get IPSEC remote address mask by AT command")
        cmd="AT*IPSEC"+vpn_no+"_REMOTE_ADDR_MASK?"
        return self.query(instance,cmd)     
    
    def set_ipsec_remote_addr_mask(self, instance, vpn_no, ipsec_remote_addr_mask):
        '''Set IPSEC remote address mask by AT command 
            AT*IPSEC1_REMOTE_ADDR_MASK=[address]
            AT*IPSEC2_REMOTE_ADDR_MASK=[address]
            AT*IPSEC3_REMOTE_ADDR_MASK=[address]
            AT*IPSEC4_REMOTE_ADDR_MASK=[address]
            AT*IPSEC5_REMOTE_ADDR_MASK=[address]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_remote_addr_mask:  IPSEC remote address mask
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IPSEC remote address mask by AT command")
        cmd="AT*IPSEC"+vpn_no+"_REMOTE_ADDR_MASK="+ipsec_remote_addr_mask
        return self.assign(instance,cmd)
     
    def get_ipsec_remote_addr_type(self, instance, vpn_no):
        ''' Query IPSEC remote address type by AT command 
            AT*IPSEC1_REMOTE_ADDR_TYPE?
            AT*IPSEC2_REMOTE_ADDR_TYPE?
            AT*IPSEC3_REMOTE_ADDR_TYPE?
            AT*IPSEC4_REMOTE_ADDR_TYPE?
            AT*IPSEC5_REMOTE_ADDR_TYPE?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC remote address type
        '''
        
        basic_airlink.slog("Step:  get IPSEC remote address type by AT command")
        cmd="AT*IPSEC"+vpn_no+"_REMOTE_ADDR_TYPE?"
        return self.query(instance,cmd)    
    
    def set_ipsec_remote_addr_type(self, instance, vpn_no, ipsec_remote_addr_type):
        '''Set IPSEC remote address type by AT command 
            AT*IPSEC1_REMOTE_ADDR_TYPE=[number]
            AT*IPSEC2_REMOTE_ADDR_TYPE=[number]
            AT*IPSEC3_REMOTE_ADDR_TYPE=[number]
            AT*IPSEC4_REMOTE_ADDR_TYPE=[number]
            AT*IPSEC5_REMOTE_ADDR_TYPE=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_remote_addr_type:  IPSEC remote address type
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IPSEC remote address type by AT command")
        cmd="AT*IPSEC"+vpn_no+"_REMOTE_ADDR_TYPE="+ipsec_remote_addr_type
        return self.assign(instance,cmd)
    
    def get_ipsec_remote_id(self, instance, vpn_no):
        ''' Query IPSEC remote ID by AT command 
            AT*IPSEC1_REMOTE_ID?
            AT*IPSEC2_REMOTE_ID?
            AT*IPSEC3_REMOTE_ID?
            AT*IPSEC4_REMOTE_ID?
            AT*IPSEC5_REMOTE_ID?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC remote ID
        '''
        
        basic_airlink.slog("Step:  get IPSEC remote ID by AT command")
        cmd="AT*IPSEC"+vpn_no+"_REMOTE_ID?"
        return self.query(instance,cmd)
    
    
    def set_ipsec_remote_id(self, instance, vpn_no, ipsec_remote_id):
        '''Set IPSEC remote ID by AT command 
            AT*IPSEC1_REMOTE_ID=[number]
            AT*IPSEC2_REMOTE_ID=[number]
            AT*IPSEC3_REMOTE_ID=[number]
            AT*IPSEC4_REMOTE_ID=[number]
            AT*IPSEC5_REMOTE_ID=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_remote_id:  IPSEC remote ID
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IPSEC remote ID by AT command")
        cmd="AT*IPSEC"+vpn_no+"_REMOTE_ID="+ipsec_remote_id
        return self.assign(instance,cmd)


    def get_ipsec_remote_id_type(self, instance, vpn_no):
        ''' Query IPSEC remote ID type by AT command 
            AT*IPSEC1_REMOTE_ID_TYPE?
            AT*IPSEC2_REMOTE_ID_TYPE?
            AT*IPSEC3_REMOTE_ID_TYPE?
            AT*IPSEC4_REMOTE_ID_TYPE?
            AT*IPSEC5_REMOTE_ID_TYPE?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC remote ID type
        '''
        
        basic_airlink.slog("Step:  get IPSEC remote ID type by AT command")
        cmd="AT*IPSEC"+vpn_no+"_REMOTE_ID_TYPE?"
        return self.query(instance,cmd)
    
    
    def set_ipsec_remote_id_type(self, instance, vpn_no, ipsec_remote_id_type):
        '''Set IPSEC remote ID type by AT command 
            AT*IPSEC1_REMOTE_ID_TYPE=[number]
            AT*IPSEC2_REMOTE_ID_TYPE=[number]
            AT*IPSEC3_REMOTE_ID_TYPE=[number]
            AT*IPSEC4_REMOTE_ID_TYPE=[number]
            AT*IPSEC5_REMOTE_ID_TYPE=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_remote_id_type:  IPSEC remote ID type
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set IPSEC remote ID type by AT command")
        cmd="AT*IPSEC"+vpn_no+"_REMOTE_ID_TYPE="+ipsec_remote_id_type
        return self.assign(instance,cmd)
 
    def get_ipsec_shared_key1(self, instance, vpn_no):
        ''' Query IPSEC shared key1 by AT command 
            AT*IPSEC1_SHARED_KEY1?
            AT*IPSEC2_SHARED_KEY1?
            AT*IPSEC3_SHARED_KEY1?
            AT*IPSEC4_SHARED_KEY1?
            AT*IPSEC5_SHARED_KEY1?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC shared key1
        '''
        basic_airlink.slog("Step:  get IPSEC shared key1 by AT command")
        cmd="AT*IPSEC"+vpn_no+"_SHARED_KEY1?"
        return self.query(instance,cmd)
    
    def set_ipsec_shared_key1(self, instance, vpn_no, ipsec_shared_key1):
        '''Set IPSEC shared key1 by AT command 
            AT*IPSEC1_SHARED_KEY1=[number]
            AT*IPSEC2_SHARED_KEY1=[number]
            AT*IPSEC3_SHARED_KEY1=[number]
            AT*IPSEC4_SHARED_KEY1=[number]
            AT*IPSEC5_SHARED_KEY1=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_shared_key1:  IPSEC shared key1
            
        Returns:
            True/False
        '''
        basic_airlink.slog("Step:  set IPSEC shared key1 by AT command")
        cmd="AT*IPSEC"+vpn_no+"_SHARED_KEY1="+ipsec_shared_key1
        return self.assign(instance,cmd)
    
    def get_ipsec_status(self, instance, vpn_no):
        ''' Query IPSEC status by AT command 
            AT*IPSEC1_STATUS?
            AT*IPSEC2_STATUS?
            AT*IPSEC3_STATUS?
            AT*IPSEC4_STATUS?
            AT*IPSEC5_STATUS?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC status
        '''
        basic_airlink.slog("Step:  get IPSEC status by AT command")
        cmd="AT*IPSEC"+vpn_no+"_STATUS?"
        return self.query(instance,cmd)
        
    def get_ipsec_tunnel_type(self, instance, vpn_no):
        ''' Query IPSEC tunnel type by AT command 
            AT*IPSEC1_TUNNEL_TYPE?
            AT*IPSEC2_TUNNEL_TYPE?
            AT*IPSEC3_TUNNEL_TYPE?
            AT*IPSEC4_TUNNEL_TYPE?
            AT*IPSEC5_TUNNEL_TYPE?
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            IPSEC tunnel type
        '''
        basic_airlink.slog("Step:  get IPSEC tunnel type by AT command")
        cmd="AT*IPSEC"+vpn_no+"_TUNNEL_TYPE?"
        return self.query(instance,cmd)

    def set_ipsec_tunnel_type(self, instance, vpn_no, ipsec_tunnel_type):
        '''Set IPSEC tunnel type by AT command 
            AT*IPSEC1_TUNNEL_TYPE=[number]
            AT*IPSEC2_TUNNEL_TYPE=[number]
            AT*IPSEC3_TUNNEL_TYPE=[number]
            AT*IPSEC4_TUNNEL_TYPE=[number]
            AT*IPSEC5_TUNNEL_TYPE=[number]
            
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            vpn_no: VPN number 
            ipsec_tunnel_type:  IPSEC tunnel type
            
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set IPSEC tunnel type by AT command")
        cmd="AT*IPSEC"+vpn_no+"_TUNNEL_TYPE="+ipsec_tunnel_type
        return self.assign(instance,cmd)
    
    def get_rsrp(self, instance):
        '''Query LTE RSRP by AT commands  AT*LTERSRP?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            LTE RSRP
        '''
        cmd = "AT*LTERSRP?"
        basic_airlink.slog("Step:  get LTE RSRP by AT command")
        return self.query(instance,cmd)
 
    def get_rsrq(self, instance):
        '''Query LTE RSRQ by AT commands  AT*LTERSRP?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            LTE RSRQ
        '''
        cmd = "AT*LTERSRP?"
        basic_airlink.slog("Step:  get LTE RSRQ by AT command")
        return self.query(instance,cmd)   
           
    def get_modem_name(self, instance):
        '''Query modem name by AT commands  AT*MODEMNAME?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            modem name
        '''
        cmd = "AT*MODEMNAME?"
        basic_airlink.slog("Step:  get modem name by AT command")
        return self.query(instance,cmd)
    
    def set_modem_name(self, instance,modem_name):
        '''Set modem name by AT commands  AT*MODEMNAME=[name]

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            True/False
        '''
        cmd = "AT*MODEMNAME="+modem_name
        basic_airlink.slog("Step:  set modem name by AT command")
        return self.assign(instance,cmd)
 
    def get_status_update_address(self, instance):
        '''Query status update address by AT commands  AT*MSCIUPDADDR?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            status update address
        '''
        cmd = "AT*MSCIUPDADDR?"
        basic_airlink.slog("Step:  get status update address by AT command")
        return self.query(instance,cmd)
    
    def set_status_update_address(self, instance,address, port):
        '''Set status update address and port by AT commands  
           AT*MSCIUPDADDR=[ipaddress/port]

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            True/False
        '''
        cmd = "AT*MSCIUPDADDR="+address+"/"+port
        basic_airlink.slog("Step: set status update address/port by AT command")
        return self.assign(instance,cmd)
       
    def get_status_update_interval(self, instance):
        '''Query status update interval by AT commands  AT*MSCIUPDPERIOD?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            status update interval
        '''
        cmd = "AT*MSCIUPDPERIOD?"
        basic_airlink.slog("Step:  get status update interval by AT command")
        return self.query(instance,cmd)
    
    def set_status_update_interval(self, instance, interval):
        '''Set status update interval by AT commands  AT*MSCIUPDPERIOD=[0-255]

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            True/False
        '''
        cmd = "AT*MSCIUPDPERIOD="+interval
        basic_airlink.slog("Step: set status update interval by AT command")
        return self.assign(instance,cmd)

    def get_net_allow_zero_ip(self, instance):
        '''Query net allow zero IP by AT commands  AT*NETALLOWZEROIP?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            flag (1/0)
                1  Allow or not the device to get an IP from cellular network 
                   with last octet as 0
                0  not allow the device to get an IP from cellular network 
                   with last octet as 0
        '''
        cmd = "AT*NETALLOWZEROIP?"
        basic_airlink.slog("Step:  get net allow zero IP by AT command")
        return self.query(instance,cmd)
 
    def set_net_allow_zero_ip(self, instance, flag):
        '''Allow or not the device to get an IP from cellular network with last
           octet as 0 by AT commands  AT*NETALLOWZEROIP=[1/0]

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            True/False
        '''
        cmd = "AT*NETALLOWZEROIP="+flag
        basic_airlink.slog("Step: set net allow zero IP  by AT command")
        return self.assign(instance,cmd)    
    
    def get_apn(self, instance):
        '''Query APN AT commands  AT*APN?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            APN
        '''
        cmd = "AT*NETAPN?"
        basic_airlink.slog("Step:  get APN by AT command")
        return self.query(instance,cmd)
 
    def set_apn(self, instance, apn):
        '''Set APN  by AT commands  AT*APN=[apn]

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            True/False
        '''
        cmd = "AT*NETAPN="+apn
        basic_airlink.slog("Step: set APN  by AT command")
        return self.assign(instance,cmd)  

    def get_net_channel(self, instance):
        '''Query net channel AT commands  AT*NETCHAN?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            network channel
        '''
        cmd = "AT*NETCHAN?"
        basic_airlink.slog("Step:  get network channel by AT command")
        return self.query(instance,cmd)
                       
    def get_phone_num(self, instance):
        '''Query phone number by AT commands  AT*NETPHONE?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            phone number
        '''
        cmd = "AT*NETPHONE?"
        basic_airlink.slog("Step:  get phone number by AT command")
        return self.query(instance,cmd)
    
    def get_net_ip(self, instance):
        '''Query NET IP  by AT commands  AT*NETIP?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Net IP
        '''
        cmd = "AT*NETIP?"
        basic_airlink.slog("Step:  get NET IP by AT command")
        return self.query(instance,cmd)
    
    def get_net_op(self, instance):
        '''Query NET operator  by AT commands  AT*NETOP?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Network operator
        '''
        cmd = "AT*NETOP?"
        basic_airlink.slog("Step:  get NET Operator by AT command")
        return self.query(instance,cmd)
    
    def get_net_password(self, instance):
        '''Query celluar network password if one required by AT commands  
           AT*NETPW?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Network passoword
        '''
        cmd = "AT*NETPW?"
        basic_airlink.slog("Step:  get NET password by AT command")
        return self.query(instance,cmd)
 
    def set_net_password(self, instance, password):
        '''Assign celluar network password if one required by AT commands  
           AT*NETPW=[password]

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            True/False
        '''
        cmd = "AT*NETPW="+password
        basic_airlink.slog("Step:  set network password by AT command")
        return self.assign(instance,cmd)
       
    def get_net_rssi(self, instance):
        '''Query network RSSI by AT commands  AT*NETRSSI?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Network RSSI
        '''
        cmd = "AT*NETRSSI?"
        basic_airlink.slog("Step:  get network RSSI by AT command")
        return self.query(instance,cmd)
    
    def get_net_service_type(self, instance):
        '''Query network service type by AT commands  AT*NETSERV?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Network service type (EV-DO, LTE, HSPA+, etc)
        '''
        cmd = "AT*NETSERV?"
        basic_airlink.slog("Step:  get network service type by AT command")
        return self.query(instance,cmd)
    
    def get_net_service_raw(self, instance):
        '''Query network service raw by AT commands  AT*NETSERVICE_RAW?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Network service RAW
        '''
        cmd = "AT*NETSERVICE_RAW?"
        basic_airlink.slog("Step:  get network servcie raw by AT command")
        return self.query(instance,cmd)
    
    def get_net_state(self, instance):
        '''Query network state by AT commands  AT*NETSTATE?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Network state
        '''
        cmd = "AT*NETSTATE?"
        basic_airlink.slog("Step:  get network state by AT command")
        return self.query(instance,cmd)
    
    def get_net_state_raw(self, instance):
        '''Query network state raw by AT commands AT*NETSTATE_RAW?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Network state RAW
        '''
        cmd = "AT*NETSTATE_RAW?"
        basic_airlink.slog("Step:  get network state raw by AT command")
        return self.query(instance,cmd)
    
    def get_net_uid(self, instance):
        '''Query celluar network username by AT commands  AT*NETUID?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Network username
        '''
        cmd = "AT*NETUID?"
        basic_airlink.slog("Step:  get network username by AT command")
        return self.query(instance,cmd)
 
    def set_net_username(self, instance, username):
        '''Assign celluar network username if one required by AT commands  
           AT*NETUID=[username]

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            True/False
        '''
        cmd = "AT*NETUID="+username
        basic_airlink.slog("Step:  set network username by AT command")
        return self.assign(instance,cmd)
 
    def get_net_connection_minutes(self, instance):
        '''Query minutes to wait for a network conenction (default 120) by 
            AT commands  AT*NETWDOG?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            minutes to wait for a network conenction (default 120)
        '''
        cmd = "AT*NETWDOG?"
        basic_airlink.slog("Step:  get minutes to wait for a network conenction \
         (default 120) by AT command")
        return self.query(instance,cmd)
    
    def set_net_connection_minutes(self, instance, minutes):
        '''Assign minutes to wait for a network conenction by AT commands  
           AT*NETWDOG=[0-255]

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            True/False
        '''
        cmd = "AT*NETWDOG="+minutes
        basic_airlink.slog("Step:  set minutes to wait for a network conenction by AT command")
        return self.assign(instance,cmd)   
    
    def get_numtoip(self, instance):
        '''Query flag to convert 12 digit number to an IP for use in PAD dialing
          (enable/disable) by AT command  AT*NETNUMTOIP?

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            1/0
        '''
        cmd = "AT*NETWDOG?"
        basic_airlink.slog("Step:  get flag to convert 12 digit number to an IP \
                            for use in PAD dialing (enable/disable) by AT command ")
        return self.query(instance,cmd)
 
    def set_numtoip(self, instance, flag):
        '''Enable/disable to convert 12 digit number to an IP for use in PAD dialing
          (enable/disable) by AT command  AT*NETNUMTOIP=0/1

        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            True/False
        '''
        cmd = "AT*NETNUMTOIP="+flag
        basic_airlink.slog("Step:  Enable/disable to convert 12 digit number to \
                            an IP for use in PAD dialing (enable/disable) by AT command")
        return self.assign(instance,cmd) 


    def get_gps_serial_port(self, instance):
        '''Query Serial streaming interface port by AT commands AT*PGPS?

        Args: 
            instance: Serial connection instance 
            
        Returns:
            Serial streaming interface port(s): 0-7 
            disable streaming (0), 
            RS232/DB9 port on the device (1), 
            USB serial (2), 
            RS232/DB9 + USB (3), 
            x-card serial (4), 
            x-card serial + 
        '''     
        cmd = "AT*PGPS?"
        basic_airlink.slog("Step:  get Serial streaming interface port by AT command")
        return self.query(instance,cmd)
    
    def set_gps_serial_port(self, instance, serial_port_no):
        '''set Serial streaming interface port by AT commands AT*PGPS=[0-7]

        Args: 
            instance: Serial connection instance 
            
        Returns:
            True/False
        '''
        cmd = "AT*PGPS="+serial_port_no
        basic_airlink.slog("Step:  set Serial streaming interface port by AT command")
        return self.assign(instance,cmd)    
    
    def get_gps_serial_streaming_flag(self, instance):
        '''Query Serial streaming flag by AT commands AT*PGPSC?

        Args: 
            instance: Serial connection instance 
            
        Returns:
            Serial streaming flag: 0/1
        '''
        cmd = "AT*PGPSC?"
        basic_airlink.slog("Step:  get Serial streaming flag by AT command")
        return self.query(instance,cmd)
    
    def set_gps_serial_streaming_flag(self, instance, stream_flag):
        '''set Serial streaming flag by AT commands AT*PGPSC=[0/1]
        
        Args: 
            instance: Serial connection instance 
            flag: Serial streaming only when the Netstate is not Network Ready: 
                  Always stream (0), 
                  only stream with out of coverage (1)
            
        Returns:
            True/False
        '''
        cmd = "AT*PGPSC="+stream_flag
        basic_airlink.slog("Step:  set Serial streaming flag by AT command")
        return self.assign(instance,cmd) 
    
    def get_gps_serial_stream_no_coverage_delay(self, instance):
        '''Query Serial streaming only with no coverage delay by AT commands AT*PGPSD?

        Args: 
            instance: Serial connection instance 
            
        Returns:
            Serial streaming Stream only with no coverage delay
        '''
        cmd = "AT*PGPSD?"
        basic_airlink.slog("Step:  get Serial streaming only with no coverage \
                            delay by AT command")
        return self.query(instance,cmd)
    
    def set_gps_serial_stream_no_coverage_delay(self, instance, seconds):
        '''set Serial streaming only with no coverage delay by AT commands AT*PGPSD=[seconds]

        Args: 
            instance: Serial connection instance 
            seconds:  Serial Stream only with no coverage delay
            
        Returns:
            True/False
        '''
        cmd = "AT*PGPSD="+seconds
        basic_airlink.slog("Step:  set Serial Stream only with no coverage delay by AT command")
        return self.assign(instance,cmd)    
    
    def get_gps_serial_stream_frequency(self, instance):
        '''Query Serial streaming frequency by AT commands AT*PGPSF?

        Args: 
            instance: Serial connection instance 
            
        Returns:
            Serial streaming Stream frequency
        '''
        cmd = "AT*PGPSF?"
        basic_airlink.slog("Step:  get Serial streaming frequency by AT command")
        return self.query(instance,cmd)
    
    def set_gps_serial_stream_frequency(self, instance, seconds):
        '''set Serial streaming frequency by AT commands AT*PGPSF=[seconds]
           How frequently to send GPS reports to the serial stream. 
           Default (0) = 1 second.

        Args: 
            instance: Serial connection instance 
            seconds:  Serial streaming frequency to send GPS reports to the s
                      erial stream. Default (0) = 1 second
        Returns:
            True/False
        '''
        cmd = "AT*PGPSF="+seconds
        basic_airlink.slog("Step:  set Serial streaming frequency by AT command")
        return self.assign(instance,cmd) 
     
    def get_gps_serial_stream_report_type(self, instance):
        '''Query Serial streaming report type by AT commands AT*PGPSR?

        Args: 
            instance: Serial connection instance 
            
        Returns:
            Serial streaming Stream report type E0|E1|E2|F0|F1|F2|F3|F4
        '''
        cmd = "AT*PGPSR?"
        basic_airlink.slog("Step:  get serial streaming report type by AT command")
        return self.query(instance,cmd)
    
    def set_gps_serial_stream_report_type(self, instance, report_type):
        '''set Serial streaming report type by AT commands AT*PGPSR=[seconds]

        Args: 
            instance: Serial connection instance 
            report_type : E0|E1|E2|F0|F1|F2|F3|F4
            
        Returns:
            True/False
        '''
        cmd = "AT*PGPSR="+report_type
        basic_airlink.slog("Step:  set serial streaming report type by AT command")
        
    def get_gps_report_interval_distance(self, instance, server_no, distance_unit):
        '''Query report interval distance in kilometers/meters by AT commands 
            AT*PPDIST?            
            AT*PP2DIST?
            AT*PP3DIST?
            AT*PP4DIST?
            AT*PPDISTM?            
            AT*PP2DISTM?
            AT*PP3DISTM?
            AT*PP4DISTM?
            
        Args: 
            instance : SSH/Telnet connection instance 
            gps_server_no: "1"/"2"/"3"/"4"
            distance_unit: "KM" - in kilometers, "M" - in meters
            
        Returns:
            Report interval distance in kilometer
        '''
        if server_no=="1":
            server_no=""
        if distance_unit=="KM":
            distance_unit=""
        cmd = "AT*PP"+server_no+"DIST"+distance_unit+"?"
        basic_airlink.slog("Step:  get GPS report interval distance in \
                            kilometer/meters by AT command")
        return self.query(instance,cmd)
    
    def set_gps_report_interval_distance(self, 
                                         instance, 
                                         server_no, 
                                         distance_unit, 
                                         interval_distance):
        '''set Serial streaming report interval distance in kilometers/meters 
           by AT commands
        
                    AT*PPDIST=[0-65535]   
                    AT*PP2DIST=[0-65535]   
                    AT*PP3DIST=[0-65535]   
                    AT*PP4DIST=[0-65535]   

                    AT*PPDISTM=[0-65535]   
                    AT*PP2DISTM=[0-65535]   
                    AT*PP3DISTM=[0-65535]   
                    AT*PP4DISTM=[0-65535] 
                    
        Args: 
            instance : SSH/Telnet connection instance 
            server_no: GPS server number
            interval_distance: report interval distance
            distance_unit: "KM" - in kilometers, "M" - in meters
            
        Returns:
            True/False
       '''
        if server_no == "1":
            server_no=""    
        if distance_unit =="KM":
            distance_unit=""    
        cmd = "AT*PPD="+server_no+"DIST"+distance_unit+"="+interval_distance
        basic_airlink.slog("Step:  set GPS report interval distance by AT command")
        return self.assign(instance,cmd)  
  
    def get_gps_report_type(self, instance, server_no):
        '''Query GPS report type by AT commands 
            AT*PPGPSR?
            AT*PP2GPSR?
            AT*PP3GPSR?
            AT*PP4GPSR?

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            The report type: 
                RAP (11, 12, 13, 14), 
                NMEA (E0, E1, E2), 
                TAIP (F0, F1, F2, F3, F4) , 
                Xora (D0)
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"GPSR?"
        basic_airlink.slog("Step:  get GPS report type by AT command")
        return self.query(instance,cmd)
    
    def set_gps_report_type(self, instance, server_no, report_type):
        '''set Serial streaming report type by AT commands 
                *PPGPSR=11|12|13|14|E0|E1|E2|F0|F1|F2|F3|F4|D0
                *PP2GPSR=11|12|13|14|E0|E1|E2|F0|F1|F2|F3|F4|D0
                *PP3GPSR=11|12|13|14|E0|E1|E2|F0|F1|F2|F3|F4|D0
                *PP4GPSR=11|12|13|14|E0|E1|E2|F0|F1|F2|F3|F4|D0

        Args: 
            instance: Serial connection instance 
            The report type: 
                RAP (11, 12, 13, 14), 
                NMEA (E0, E1, E2), 
                TAIP (F0, F1, F2, F3, F4) , 
                Xora (D0)            
        Returns:
            True/False
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"GPSR="+report_type
        basic_airlink.slog("Step:  set GPS report type by AT command")
        return self.assign(instance,cmd)  
        
    def get_gps_report_dest_ip(self, instance, server_no):
        '''Query GPS report destination by AT commands 
            AT*PPIP?
            AT*PP2IP?
            AT*PP3IP?
            AT*PP4IP?

        Args: 
            instance: SSH/Telnet connection instance 
            server_no: GPS server numvber (1-4)
            
        Returns:
            The report destination address
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"IP?"
        basic_airlink.slog("Step:  get GPS report destination IP by AT command")
        return self.query(instance,cmd)
    
    def set_gps_report_dest_ip(self, instance, server_no, dest_ip):
        '''set GPS report destination address by AT commands 

        Args: 
            instance: SSH/Telnet connection instance 
            server_no: GPS server number 
            dest_address: The report desitination IP       
                 
        Returns:
            True/False
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"IP="+dest_ip
        basic_airlink.slog("Step:  set GPS report destination IP by AT command")
        return self.assign(instance,cmd)  
        
    def get_gps_max_retries(self, instance, server_no):
        '''Query GPS Maximum number of retries for Simple Reliable, UDP Sequence 
           mode, and the TCP transports. Default = 10 by AT commands 
               AT*PPMAXRETRIES?
               AT*PP2MAXRETRIES?
               AT*PP3MAXRETRIES?
               AT*PP4MAXRETRIES?

        Args: 
            instance: SSH/Telnet connection instance 
            server_no: GPS server numvber (1-4)
            
        Returns:
            The Maximum number of retries for Simple Reliable, UDP Sequence 
           mode, and the TCP transports

        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"MAXRETRIES?"
        basic_airlink.slog("Step:  get GPS Maximum number of retries by AT command")
        return self.query(instance,cmd)
        
    def set_gps_max_retries(self, instance, server_no, max_retries):
        '''set GPS Maximum number of retries by AT commands 
                AT*PPMAXRETRIES=0-255
                AT*PP2MAXRETRIES=0-255
                AT*PP3MAXRETRIES=0-255
                AT*PP4MAXRETRIES=0-255
        Args: 
            instance: SSH/Telnet connection instance 
            server_no: GPS server number 
            max_retries: The Maximum number of retries     
                 
        Returns:
            True/False
        '''       
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"MAXRETRIES="+max_retries
        basic_airlink.slog("Step:  set GPS Maximum number of retries by AT command")
        return self.assign(instance,cmd)  
  
    def get_gps_min_time_between_packets(self, instance, server_no):
        '''Query GPS Minimum amount of time between report packets. Multiple 
           reports can be in each packet by AT commands 
               AT*PPMINTIME??
               AT*PP2MINTIME?
               AT*PP3MINTIME?
               AT*PP4MINTIME?

        Args: 
            instance: SSH/Telnet connection instance 
            server_no: GPS server number (1-4)
            
        Returns:
            Minimum amount of time between report packets
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"MINTIME?"
        basic_airlink.slog("Step:  get GPS Minimum amount of time between report packets by AT command")
        return self.query(instance,cmd)
    
    def set_gps_min_time_between_packets(self, instance, server_no, min_time):
        '''set GPS Minimum amount of time between report packets by AT commands 
                AT*PPMINTIME=0-65535
                AT*PP2MINTIME=0-65535
                AT*PP3MINTIME=0-65535
                AT*PP4MINTIME=0-65535
        Args: 
            instance: SSH/Telnet connection instance 
            server_no: GPS server number 
            min_time: Minimum amount of time between report packets    
                 
        Returns:
            True/False
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"MINTIME="+min_time
        basic_airlink.slog("Step:  set GPS Minimum amount of time between report packets by AT command")
        return self.assign(instance,cmd)  
        
    def get_gps_include_odo_flag(self, instance, server_no):
        '''Query flag to include the current Odometer with RAP reports by AT commands 
               AT**PPODOM?
               AT**PP2ODOM?
               AT**PP3ODOM?
               AT**PP4ODOM?

        Args: 
            instance: SSH/Telnet connection instance 
            server_no: GPS server number (1-4)
            
        Returns:
            flag to include the current Odometer with RAP reports
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"ODOM?"
        basic_airlink.slog("Step:  get flag to include the current Odometer with RAP report by AT command")
        return self.query(instance,cmd)
        
    def set_gps_include_odo_flag(self, instance, server_no, flag):
        '''enable/disable flag to include the current Odometer with RAP report by AT commands 
                AT*PPODOM=0/1
                AT*PP2ODOM=0/1
                AT*PP3ODOM=0/1
                AT*PP4ODOM=0/1

        Args: 
            instance: SSH/Telnet connection instance 
            server_no: GPS server number 
            flag: 1 - include the current Odometer with RAP report or 0 not
                 
        Returns:
            True/False
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"ODOM="+flag
        basic_airlink.slog("Step:  set flag to include the current Odometer with RAP report by AT command")
        return self.assign(instance,cmd)  

    def get_gps_report_dest_port(self, instance, server_no):
        '''Query GPS report destination port by AT commands 
            AT*PPPORT?
            AT*PP2PORT?
            AT*PP3PORT?
            AT*PP4PORT?

        Args: 
            instance: SSH/Telnet connection instance 
            server_no: GPS server numvber (1-4)
            
        Returns:
            The report destination port
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"PORT?"
        basic_airlink.slog("Step:  get GPS report destination port by AT command")
        return self.query(instance,cmd)
        
    def set_gps_report_dest_port(self, instance, server_no, dest_port):
        '''set GPS report destination port by AT commands 
                AT*PPPORT=0-65535
                AT*PP2PORT=0-65535
                AT*PP3PORT=0-65535
                AT*PP4PORT=0-65535

        Args: 
            instance : SSH/Telnet connection instance 
            server_no: GPS server number 1-4
            dest_port: The report desitination port       
                 
        Returns:
            True/False
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+str(server_no)+"PORT="+str(dest_port)
        basic_airlink.slog("Step:  set GPS report destination port by AT command") 
        return self.assign(instance,cmd) 
    
    
    def get_gps_include_input_in_rap(self, instance, server_no):
        '''By AT commands query falg of including the current digital input values 
           in RAP reports
            AT*PPREPORTINPUTS?
            AT*PP2REPORTINPUTS?
            AT*PP3REPORTINPUTS?
            AT*PP4REPORTINPUTS?

        Args: 
            instance: SSH/Telnet connection instance 
            server_no: GPS server numvber (1-4)
            
        Returns:
            flag to include the current digital input values in RAP reports (0/1)
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"REPORTINPUTS?"
        basic_airlink.slog("Step:  by AT command query falg to include the current \
                            digital input values in RAP reports ")
        return self.query(instance,cmd)
        
    def enable_gps_include_input_in_rap(self, instance, server_no, flag):
        '''by AT commands mark if include the current digital input values in RAP reports 
                AT*PPREPORTINPUTS=0/1
                AT*PP2REPORTINPUTS=0/1
                AT*PP3REPORTINPUTS=0/1
                AT*PP4REPORTINPUTS=0/1

        Args: 
            instance : SSH/Telnet connection instance 
            server_no: GPS server number 1-4
            flag: 
                1: include the current digital input values in RAP reports, 0: not 
                 
        Returns:
            True/False
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"REPORTINPUTS="+flag
        basic_airlink.slog("Step:  by AT command mark if include the current \
                            digital input values in RAP reports ") 
        return self.assign(instance,cmd) 

    def get_gps_first_retry_interval(self, instance, server_no):
        '''By AT commands query the first retry interval for Simple Reliable, 
           UDP Sequence mode, and the TCP transports. Default = 10
            AT*PPSIMPLETO?
            AT*PP2SIMPLETO?
            AT*PP3SIMPLETO?
            AT*PP4SIMPLETO?

        Args: 
            instance: SSH/Telnet connection instance 
            server_no: GPS server numvber (1-4)
            
        Returns:
            the first retry interval for Simple Reliable, 
            UDP Sequence mode, and the TCP transports. Default = 10
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"SIMPLETO?"
        basic_airlink.slog("Step:  by AT command querythe first retry interval \
                            for Simple Reliable, UDP Sequence mode, and the TCP transports. ")
        return self.query(instance,cmd)
        
    def set_gps_first_retry_interval(self, instance, server_no, interval):
        '''by AT commands set the first retry interval for Simple Reliable, 
           UDP Sequence mode, and the TCP transports.
                AT*PPSIMPLETO=0-255
                AT*PP2SIMPLETO=0-255
                AT*PP3SIMPLETO=0-255
                AT*PP4SIMPLETO=0-255

        Args: 
            instance : SSH/Telnet connection instance 
            server_no: string, GPS server number 1-4
            interval:  string,
                the first retry interval for Simple Reliable, 
                UDP Sequence mode, and the TCP transports.
                 
        Returns:
            True/False
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"SIMPLETO="+interval
        basic_airlink.slog("Step:  by AT command set the first retry interval for Simple Reliable, \
                            UDP Sequence mode, and the TCP transports. ") 
        return self.assign(instance,cmd) 
        
    def get_gps_unreliable_snf(self, instance, server_no):
        '''By AT commands query Unreliable SNF
            AT*PPSNF?
            AT*PP2SNF?
            AT*PP3SNF?
            AT*PP4SNF?

        Args: 
            instance: SSH/Telnet connection instance 
            server_no: GPS server numvber (1-4)
            
        Returns:
            Unreliable SNF enable/disable
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"SNF?"
        basic_airlink.slog("Step:  by AT command query Unreliable SNF enable/disable ")
        return self.query(instance,cmd)
        
    def enable_gps_unreliable_snf(self, instance, server_no, flag):
        '''by AT commands mark Unreliable SNF 
                AT*PPSNF=0/1
                AT*PP2SNF=0/1
                AT*PP3SNF=0/1
                AT*PP4SNF=0/1

        Args: 
            instance : SSH/Telnet connection instance 
            server_no: GPS server number 1-4
            flag: 
                1: Unreliable SNF enable, 0: disable 
                 
        Returns:
            True/False
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"SNF="+flag
        basic_airlink.slog("Step:  by AT command mark Unreliable SNF ") 
        return self.assign(instance,cmd) 
        
    def get_gps_tranport_snf_mode(self, instance, server_no):
        '''By AT commands get transport SNF mode
            disabled (0), 
            Reliable mode (1), 
            Simple Reliable (2), 
            UDP Sequence (3), 
            TCP Listen (4), 
            TCP (5)      

        Args: 
            instance: SSH/Telnet connection instance 
            server_no: GPS server numvber (1-4)
            
        Returns:
            transport SNF mode
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"SNFR?"
        basic_airlink.slog("Step:  by AT command query transport SNF mode ")
        return self.query(instance,cmd)
        
    def set_gps_tranport_snf_mode(self, instance, server_no, mode):
        '''by AT commands set tranport snf mode
                AT*PPSNFR=0/1/2/3/4/5
                AT*PP2SNFR=0/1/2/3/4/5
                AT*PP3SNFR=0/1/2/3/4/5
                AT*PP4SNFR=0/1/2/3/4/5

        Args: 
            instance : SSH/Telnet connection instance 
            server_no: GPS server number 1-4
            mode: transport snf mode
            
        Returns:
            True/False
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"SNFR="+mode
        basic_airlink.slog("Step:  by AT command set transport SNF mode") 
        return self.assign(instance,cmd) 
        
    def get_gps_report_interval(self, instance, server_no):
        '''By AT commands get GPS Report Time Interval (seconds)
         *PPTIME?    
         *PP2TIME?    
         *PP3TIME?    
         *PP4TIME?    

        Args: 
            instance: SSH/Telnet connection instance 
            server_no: GPS server numvber (1-4)
            
        Returns:
            GPS report time interval (seconds)
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"TIME?"
        basic_airlink.slog("Step:  by AT command query GPS report time interval (s) ")
        return self.query(instance,cmd)
        
    def set_gps_report_interval(self, instance, server_no, interval):
        '''by AT commands set GPS Report Time Interval (seconds)
                AT*PPTIME=0-65535
                AT*PP2TIME=0-65535
                AT*PP3TIME=0-65535
                AT*PP4TIME=0-65535

        Args: 
            instance : SSH/Telnet connection instance 
            server_no: GPS server number 1-4
            interval: GPS report time interval(s)
            
        Returns:
            True/False
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"TIME="+interval
        basic_airlink.slog("Step:  by AT command set GPS report time interval (s)") 
        return self.assign(instance,cmd) 

                
    def get_gps_tsv(self, instance, server_no):
        '''By AT commands get GPS Stationary Vehicle Timer (minutes)
         *PPTSV?    
         *PP2TSV?    
         *PP3TSV?    
         *PP4TSV?    

        Args: 
            instance: SSH/Telnet connection instance 
            server_no: GPS server numvber (1-4)
            
        Returns:
            GPS Stationary Vehicle Timer (minutes)
        '''
        if server_no == "1":
            server_no="" 
        cmd = "AT*PP"+server_no+"TSV?"
        basic_airlink.slog("Step:  by AT command query GPS Stationary Vehicle Timer (minutes)")
        return self.query(instance,cmd)
 
    def get_prl_status(self, instance):
        '''By AT commands get PRL update status: *PRLSTATUS?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            PRL update status  (ACEmanager UI -> status -> WAN)
        '''
        cmd = "AT*PRLSTATUS?"
        basic_airlink.slog("Step:  by AT command query PRL status")
        return self.query(instance,cmd) 

    def get_pulse_count(self, instance, digital_in_no):
        '''By AT commands get current pulse count for digital in #: 
            *PULSECNT1?      
            *PULSECNT2?      
            *PULSECNT3?      
            *PULSECNT4?      
            *PULSECNT5?      
            *PULSECNT6?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            Pulse count  (ACEmanager UI -> IO)
        '''
        cmd = "AT*PULSTCNT"+digital_in_no+"?"
        basic_airlink.slog("Step:  by AT command query current pulse count for digital in 1-6")
        return self.query(instance,cmd) 

    def enable_radio_connect(self, instance, flag):
        '''By AT command enable/disable activate PDP context: *RADIO_CONNECT=[0/1]  

        Args: 
            instance: SSH/Telnet connection instance 
            flag: 0 - disable, 1 - enable
            
        Returns:
            True/False
        '''
        cmd = "AT*RADIO_CONNECT="+flag
        basic_airlink.slog("Step:  by AT command enable/disable radio connection")
        return self.assign(instance,cmd) 

    def enable_radio_connect_startup(self, instance, flag):
        '''By AT command enable/disable activate PDP contex during nect boot: 
          *RADIO_CONNECT_STARTUP=[0/1]  

        Args: 
            instance: SSH/Telnet connection instance 
            flag: 0 - disable, 1 - enable
            
        Returns:
            True/False
        '''
        cmd = "AT*RADIO_CONNECT_STARTUP="+flag
        basic_airlink.slog("Step:  by AT command enable/disable radio connection during next boot")
        return self.assign(instance,cmd)
 
    def get_relay_out(self, instance, relay_no):
        '''By AT commands get relay out: 
            *RELAYOUT1?      
            *RELAYOUT2?      
            *RELAYOUT3?      
            *RELAYOUT4?      
            *RELAYOUT5?      
            *RELAYOUT6?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            relay out  (ACEmanager UI -> IO)
        '''
        cmd = "AT*PULSTCNT"+relay_no+"?"
        basic_airlink.slog("Step:  by AT command query relay out")
        return self.query(instance,cmd) 

    def set_relay_out(self, instance, relay_no):
        '''By AT commands set relay out: 
            *RELAYOUT1=[0/1]      
            *RELAYOUT2=[0/1]   
            *RELAYOUT3=[0/1]     
            *RELAYOUT4=[0/1]     
            *RELAYOUT5=[0/1]     
            *RELAYOUT6=[0/1]      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            True/False
        '''
        cmd = "AT*RELAYOUT="+relay_no
        basic_airlink.slog("Step:  by AT command set relay out")
        return self.assign(instance,cmd) 

    def set_remote_log_server(self, instance, ip_address, port_no):
        '''By AT commands set the remote sys log server ip and port: 
            *REMOTELOG=<sys log server ip>,<port #>    
            ACEmanager -> Admin 

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            True/False
        '''
        cmd = "AT*REMOTELOG="+ip_address+","+port_no
        basic_airlink.slog("Step:  by AT command set remote log server")
        return self.assign(instance,cmd) 
                             
    def get_snmp_version(self, instance):
        '''By AT command get SNMP version: *SNMPVERSION?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP version
        '''
        cmd = "AT*SNMPVERSION?"
        basic_airlink.slog("Step:  by AT command query SNMP version")
        return self.query(instance,cmd) 

    def set_snmp_version(self, instance,ver):
        '''By AT command set SNMP version: *SNMPVERSION=[ver]  

        Args: 
            instance: SSH/Telnet connection instance 
            ver: SNMP version [2/3]
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPVERSION="+ver
        basic_airlink.slog("Step:  by AT command set SNMP version")
        return self.assign(instance,cmd) 
    
    def get_snmp_enable(self, instance):
        '''By AT commands get SNMP enable flag: *SNMP?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP enable
        '''
        cmd = "AT*SNMP?"
        basic_airlink.slog("Step:  by AT command query SNMP enable")
        return self.query(instance,cmd) 

    def set_snmp_enable(self, instance,flag):
        '''By AT commands enable or disable SNMP feature: *SNMP=[0/1]      

        Args: 
            instance: SSH/Telnet connection instance 
            flag: 0/1
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMP="+flag
        basic_airlink.slog("Step:  by AT command enable or disable SNMP feature")
        return self.assign(instance,cmd) 
    
    def get_snmp_contact(self, instance):
        '''By AT command get SNMP contact: *SNMPCONTACT?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP contact
        '''
        cmd = "AT*SNMPCONTACT?"
        basic_airlink.slog("Step:  by AT command query SNMP contact")
        return self.query(instance,cmd) 

    def set_snmp_contact(self, instance,contact_name):
        '''By AT command set SNMP contact: *SNMPCONTACT=[string]      

        Args: 
            instance: SSH/Telnet connection instance 
            contact_name: string, contact name
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPCONTACT="+contact_name
        basic_airlink.slog("Step:  by AT command set SNMP contact")
        return self.assign(instance,cmd) 
    
 
    
    def get_snmp_location(self, instance):
        '''By AT command get SNMP location: *SNMPLOCATION?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP location
        '''
        cmd = "AT*SNMPLOCATION?"
        basic_airlink.slog("Step:  by AT command query SNMP location")
        return self.query(instance,cmd) 

    def set_snmp_location(self, instance,location):
        '''By AT command set SNMP location: *SNMPLOCATION=[location]      

        Args: 
            instance: SSH/Telnet connection instance 
            location: string, location
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPLOCATION="+location
        basic_airlink.slog("Step:  by AT command set SNMP location")
        return self.assign(instance,cmd) 

    def get_snmp_name(self, instance):
        '''By AT command get SNMP name: *SNMPNAME?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP name
        '''
        cmd = "AT*SNMPNAME?"
        basic_airlink.slog("Step:  by AT command query SNMP name")
        return self.query(instance,cmd) 

    def set_snmp_name(self, instance, name):
        '''By AT command set SNMP name: *SNMPNAME=[name]      

        Args: 
            instance: SSH/Telnet connection instance 
            name: string, SNMP name
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPNAME="+name
        basic_airlink.slog("Step:  by AT command set SNMP name")
        return self.assign(instance,cmd)
    
    def get_snmp_port(self, instance):
        '''By AT command get SNMP port: *SNMPPORT?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP port
        '''
        cmd = "AT*SNMPPORT?"
        basic_airlink.slog("Step:  by AT command query SNMP port")
        return self.query(instance,cmd) 

    def set_snmp_port(self, instance, port):
        '''By AT command set SNMP port: *SNMPPORT=[port]      

        Args: 
            instance: SSH/Telnet connection instance 
            port: string, SNMP port
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPPORT="+port
        basic_airlink.slog("Step:  by AT command set SNMP port")
        return self.assign(instance,cmd)
    
    def get_snmp_ro_community(self, instance):
        '''By AT command get SNMP Read Only community: *SNMPROCOMMUNITY?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP Read Only community
        '''
        cmd = "AT*SNMPROCOMMUNITY?"
        basic_airlink.slog("Step:  by AT command query SNMP Read Only community")
        return self.query(instance,cmd) 

    def set_snmp_ro_community(self, instance, community):
        '''By AT command set SNMP Read Only community: *SNMPROCOMMUNITY=[community]      

        Args: 
            instance: SSH/Telnet connection instance 
            community: string, SNMP Read Only community
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPROCOMMUNITY="+community
        basic_airlink.slog("Step:  by AT command set SNMP Read Only community")
        return self.assign(instance,cmd)
    
    def get_snmp_ro_username(self, instance):
        '''By AT command get SNMP Read Only user: *SNMPROUSER?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP Read Only user
        '''
        cmd = "AT*SNMPROUSER?"
        basic_airlink.slog("Step:  by AT command query SNMP Read Only user")
        return self.query(instance,cmd) 

    def set_snmp_ro_username(self, instance, username):
        '''By AT command set SNMP Read Only user: *SNMPUSER=[username]      

        Args: 
            instance: SSH/Telnet connection instance 
            username: string, SNMP user name
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPROUSER="+username
        basic_airlink.slog("Step:  by AT command set SNMP Read Only user")
        return self.assign(instance,cmd)
    
    def get_snmp_ro_auth_type(self, instance):
        '''By AT command get SNMP Read Only authentication type: *SNMPROAUTHTYPE?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP Read Only authentication type
        '''
        cmd = "AT*SNMPROUSERAUTHTYPE?"
        basic_airlink.slog("Step:  by AT command query SNMP Read Only authentication type")
        return self.query(instance,cmd) 

    def set_snmp_ro_auth_type(self, instance, auth_type):
        '''By AT command set SNMP Read Only authentication type: *SNMPUSERAUTHTYPE=[username]      

        Args: 
            instance: SSH/Telnet connection instance 
            username: string, SNMP authentication type
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPROUSERAUTHTYPE="+auth_type
        basic_airlink.slog("Step:  by AT command set SNMP Read Only authentication type")
        return self.assign(instance,cmd)
    
    def get_snmp_ro_privacy_type(self, instance):
        '''By AT command get SNMP Read Only priv type: *SNMPROPRIVTYPE?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP Read Only authentication type
        '''
        cmd = "AT*SNMPROUSERPRIVTYPE?"
        basic_airlink.slog("Step:  by AT command query SNMP Read Only priv type")
        return self.query(instance,cmd) 

    def set_snmp_ro_privacy_type(self, instance, priv_type):
        '''By AT command set SNMP Read Only priv type: *SNMPUSERPRIVTYPE=[type]      

        Args: 
            instance: SSH/Telnet connection instance 
            type: string, SNMP priv type
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPROUSERPRIVTYPE="+priv_type
        basic_airlink.slog("Step:  by AT command set SNMP Read Only priv type")
        return self.assign(instance,cmd)
    
    def get_snmp_ro_security_level(self, instance):
        '''By AT command get SNMP Read Only user security level: *SNMPROUSERSECLVL?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP Read Only user securoty level
        '''
        cmd = "AT*SNMPROUSERSECLVL?"
        basic_airlink.slog("Step:  by AT command query SNMP Read Only user security level")
        return self.query(instance,cmd) 

    def set_snmp_ro_security_level(self, instance, sec_lvl):
        '''By AT command set SNMP Read Only user security level: *SNMPUSERSECLVL=[level]      

        Args: 
            instance: SSH/Telnet connection instance 
            level: string, SNMP RO user security level
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPROUSERSECLVL="+sec_lvl
        basic_airlink.slog("Step:  by AT command set SNMP Read Only user security level")
        return self.assign(instance,cmd)
    
    def get_snmp_rw_community(self, instance):
        '''By AT command get SNMP Read Write community: *SNMPRWCOMMUNITY?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP Read Write community
        '''
        cmd = "AT*SNMPRWCOMMUNITY?"
        basic_airlink.slog("Step:  by AT command query SNMP Read Write community")
        return self.query(instance,cmd) 

    def set_snmp_rw_community(self, instance, community):
        '''By AT command set SNMP Read/Write community: *SNMPRWCOMMUNITY=[community]      

        Args: 
            instance: SSH/Telnet connection instance 
            community: string, SNMP Read/Write community
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPRWCOMMUNITY="+community
        basic_airlink.slog("Step:  by AT command set SNMP Read Only community")
        return self.assign(instance,cmd)
    
    def get_snmp_rw_username(self, instance):
        '''By AT command get SNMP Read/Write user: *SNMPRWUSER?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP Read/Write user
        '''
        cmd = "AT*SNMPRWUSER?"
        basic_airlink.slog("Step:  by AT command query SNMP Read/Write user")
        return self.query(instance,cmd) 

    def set_snmp_rw_username(self, instance, username):
        '''By AT command set SNMP Read/Write user: *SNMPRWUSER=[username]      

        Args: 
            instance: SSH/Telnet connection instance 
            username: string, SNMP user name
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPRWUSER="+username
        basic_airlink.slog("Step:  by AT command set SNMP Read/Write user")
        return self.assign(instance,cmd)
    
    def get_snmp_rw_auth_type(self, instance):
        '''By AT command get SNMP Read/Write user authentication type: *SNMPRWUSERAUTHTYPE?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP Read/Write user authentication type
        '''
        cmd = "AT*SNMPRWUSERAUTHTYPE?"
        basic_airlink.slog("Step:  by AT command query SNMP Read Only authentication type")
        return self.query(instance,cmd) 

    def set_snmp_rw_auth_type(self, instance, auth_type):
        '''By AT command set SNMP Read/Write user authentication type: *SNMPRWUSERAUTHTYPE=[username]      

        Args: 
            instance: SSH/Telnet connection instance 
            username: string, SNMP authentication type
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPRWUSERAUTHTYPE="+auth_type
        basic_airlink.slog("Step:  by AT command set SNMP Read/Write user authentication type")
        return self.assign(instance,cmd)
    
    def get_snmp_rw_privacy_type(self, instance):
        '''By AT command get SNMP Read/Write user priv type: *SNMPRWUSERPRIVTYPE?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP Read/Write user authentication type
        '''
        cmd = "AT*SNMPRWUSERPRIVTYPE?"
        basic_airlink.slog("Step:  by AT command query SNMP Read/Write user priv type")
        return self.query(instance,cmd) 

    def set_snmp_rw_privacy_type(self, instance, priv_type):
        '''By AT command set SNMP Read/Write user priv type: *SNMPRWUSERPRIVTYPE=[type]      

        Args: 
            instance: SSH/Telnet connection instance 
            type: string, SNMP priv type
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPRWUSERPRIVTYPE="+priv_type
        basic_airlink.slog("Step:  by AT command set SNMP Read/Write user priv type")
        return self.assign(instance,cmd)
    
    def get_snmp_rw_security_level(self, instance):
        '''By AT command get SNMP Read/Write user security level: *SNMPRWUSERSECLVL?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP Read/Write user securoty level
        '''
        cmd = "AT*SNMPRWUSERSECLVL?"
        basic_airlink.slog("Step:  by AT command query SNMP Read/Write user security level")
        return self.query(instance,cmd) 

    def set_snmp_rw_security_level(self, instance, sec_lvl):
        '''By AT command set SNMP Read/Write user security level: *SNMPRWUSERSECLVL=[level]      

        Args: 
            instance: SSH/Telnet connection instance 
            sec_lvl: string, SNMP Read/Write user security level
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPRWUSERSECLVL="+sec_lvl
        basic_airlink.slog("Step:  by AT command set SNMP Read/Write user security level")
        return self.assign(instance,cmd)

    def get_snmp_trap_community(self, instance):
        '''By AT command get SNMP trap community: *SNMPTRAPCOMMUNITY?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP trap community
        '''
        cmd = "AT*SNMPTRAPCOMMUNITY?"
        basic_airlink.slog("Step:  by AT command query SNMP trap community")
        return self.query(instance,cmd) 

    def set_snmp_trap_community(self, instance, community):
        '''By AT command set SNMP trap community: *SNMPTRAPCOMMUNITY=[community]      

        Args: 
            instance: SSH/Telnet connection instance 
            community: string, SNMP Read/Write community
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPTRAPCOMMUNITY="+community
        basic_airlink.slog("Step:  by AT command set SNMP trap community")
        return self.assign(instance,cmd)
 
    def get_snmp_trap_engine_id(self, instance):
        '''By AT command get SNMP engine ID: *SNMPENGINEID?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP engine ID
        '''
        cmd = "AT*SNMPENGINEID?"
        basic_airlink.slog("Step:  by AT command query SNMP engine ID")
        return self.query(instance,cmd) 

    def set_snmp_trap_engine_id(self, instance,engine_id):
        '''By AT command set SNMP engine ID: *SNMPENGINEID=[engine id]      

        Args: 
            instance: SSH/Telnet connection instance 
            engine_id: string, engine ID
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPENGINEID="+engine_id
        basic_airlink.slog("Step:  by AT command set SNMP engine ID")
        return self.assign(instance,cmd) 
       
    def get_snmp_trap_username(self, instance):
        '''By AT command get SNMP trap user: *SNMPTRAPUSER?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP trap user
        '''
        cmd = "AT*SNMPTRAPUSER?"
        basic_airlink.slog("Step:  by AT command query SNMP trap user")
        return self.query(instance,cmd) 

    def set_snmp_trap_username(self, instance, username):
        '''By AT command set SNMP trap user: *SNMPTRAPUSER=[username]      

        Args: 
            instance: SSH/Telnet connection instance 
            username: string, SNMP trap user name
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPTRAPUSER="+username
        basic_airlink.slog("Step:  by AT command set SNMP trap user")
        return self.assign(instance,cmd)
    
    def get_snmp_trap_auth_type(self, instance):
        '''By AT command get SNMP trap user authentication type: 
        *SNMPTRAPAUTHTYPE?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP trap user authentication type
        '''
        cmd = "AT*SNMPTRAPAUTHTYPE?"
        basic_airlink.slog("Step:  by AT command query SNMP trap authentication type")
        return self.query(instance,cmd) 

    def set_snmp_trap_auth_type(self, instance, auth_type):
        '''By AT command set SNMP trap user authentication type: 
        *SNMPTRAPAUTHTYPE=[auth_type]      

        Args: 
            instance: SSH/Telnet connection instance 
            username: string, SNMP authentication type
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPTRAPAUTHTYPE="+auth_type
        basic_airlink.slog("Step:  by AT command set SNMP trap user authentication type")
        return self.assign(instance,cmd)
    
    def get_snmp_trap_privacy_type(self, instance):
        '''By AT command get SNMP trap user priv type: *SNMPTRAPPRIVTYPE?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP trap user authentication type
        '''
        cmd = "AT*SNMPTRAPPRIVTYPE?"
        basic_airlink.slog("Step:  by AT command query SNMP trap user priv type")
        return self.query(instance,cmd) 

    def set_snmp_trap_privacy_type(self, instance, priv_type):
        '''By AT command set SNMP trap user priv type: *SNMPTRAPPRIVTYPE=[type]      

        Args: 
            instance: SSH/Telnet connection instance 
            type: string, SNMP priv type
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPTRAPPRIVTYPE="+priv_type
        basic_airlink.slog("Step:  by AT command set SNMP trap user priv type")
        return self.assign(instance,cmd)
    
    def get_snmp_trap_security_level(self, instance):
        '''By AT command get SNMP trap user security level: *SNMPTRAPSECLVL?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP trap user securoty level
        '''
        cmd = "AT*SNMPTRAPSECLVL?"
        basic_airlink.slog("Step:  by AT command query SNMP trap user security level")
        return self.query(instance,cmd) 

    def set_snmp_trap_security_level(self, instance, sec_lvl):
        '''By AT command set SNMP trap user security level: *SNMPTRAPSECLVL=[level]      

        Args: 
            instance: SSH/Telnet connection instance 
            sec_lvl: string, SNMP trap user security level
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPTRAPSECLVL="+sec_lvl
        basic_airlink.slog("Step:  by AT command set SNMP trap user security level")
        return self.assign(instance,cmd)
    
    def get_snmp_trap_dest(self, instance):
        '''By AT command get SNMP trap destination level: *SNMPTRAPDEST?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP trap destination
        '''
        cmd = "AT*SNMPTRAPDEST?"
        basic_airlink.slog("Step:  by AT command query SNMP trap destination")
        return self.query(instance,cmd) 

    def set_snmp_trap_dest(self, instance, dest):
        '''By AT command set SNMP trap user security level: *SNMPTRAPDEST=[level]      

        Args: 
            instance: SSH/Telnet connection instance 
            dest: string, SNMP trap destination
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPTRAPDEST="+dest
        basic_airlink.slog("Step:  by AT command set SNMP trap destination")
        return self.assign(instance,cmd)
    
    def get_snmp_trap_port(self, instance):
        '''By AT command get SNMP trap portl: *SNMPTRAPPORT?      

        Args: 
            instance: SSH/Telnet connection instance 
            
        Returns:
            SNMP trap port
        '''
        cmd = "AT*SNMPTRAPPORT?"
        basic_airlink.slog("Step:  by AT command query SNMP trap port")
        return self.query(instance,cmd) 

    def set_snmp_trap_port(self, instance, port):
        '''By AT command set SNMP trap port: *SNMPTRAPPORT=[port]      

        Args: 
            instance: SSH/Telnet connection instance 
            sec_lvl: string, SNMP trap port
            
        Returns:
            True/False
        '''
        cmd = "AT*SNMPTRAPPORT="+port
        basic_airlink.slog("Step:  by AT command set SNMP trap port")
        return self.assign(instance,cmd)
    
    def get_variable_list(self, instance): 
        '''  list most variables'values by AT command  AT&V
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            list of variables
        '''
        cmd = "AT&V"
        basic_airlink.slog("Step:  list most set by AT command")
        return self.query(instance,cmd)
    
    def write_non_volatile_memory(self, instance): 
        '''  Write to non volatile memory by AT command  AT&W
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            True/False
        '''
        cmd = "AT&W"
        basic_airlink.slog("Step:  Write to non volatile memory by AT command  AT&W")
        return self.execute(instance,cmd)
    
    def get_device_model(self, instance): 
        '''  get device mode by AT command  ATI[0]
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            device model 
        '''
        cmd = "ATI"
        basic_airlink.slog("Step:  Write to non volatile memory by AT command  AT&W")
        ret_lst = self.query_new(instance,cmd).split("\n")
        lst = []
        for i in ret_lst:
            if i!="":
                lst.append(i)
        return lst[0]
    
    def get_device_model_i0(self, instance): 
        '''  get device mode by AT command  ATI0
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            device model 
        '''
        cmd = "ATI0"
        basic_airlink.slog("Step:  get device mode by AT command  ATI0")
        return self.query(instance,cmd)
 
    def get_fw_version(self, instance): 
        '''  get ALEOS FW version by AT command  ATI1
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            ALEOS FW version
        '''
        cmd = "ATI1"
        basic_airlink.slog("Step:  get ALEOS FW version by AT command  ATI1")
        ret_lst = self.query_new(instance,cmd).split("\n")
        lst = []
        for i in ret_lst:
            if i!="":
                lst.append(i)
        return lst[0]        

    def get_rm_version(self, instance): 
        '''  get radio version by AT command  ATI2
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Radio Module Version
        '''
        cmd = "ATI2"
        basic_airlink.slog("Step:  get radio version by AT command  ATI2")
        ret_lst = self.query_new(instance,cmd).split("\n")
        lst = []
        for i in ret_lst:
            if i!="":
                lst.append(i)
        return lst[0]        
    
    def get_rm_name(self, instance):
        '''  get radio module by AT command  ATI2
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            Radio Module Name 
        '''
        cmd = "ATI2"
        basic_airlink.slog("Step:  get radio version by AT command  ATI2")
        ret_lst = self.query_new(instance,cmd).split("\n")        
        lst = []
        for i in ret_lst:
            if i!="":
                lst.append(i)
        return lst[1]
        
    
    def get_esn_imei_eid(self, instance): 
        '''  get ESN/IMEI/EID by AT command  ATI3
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            ESN/IMEI/EID
        '''
        cmd = "ATI3"
        basic_airlink.slog("Step:  get ESN/IMEI/EID by AT command  ATI3")
        return self.query(instance,cmd) 
 
    def get_hspa_diversity(self, instance):
        '''Query GSM/HSPA diversity by AT command AT*RXDIVERSITY?
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            
        Returns:
            GSM/HSPA diversity 
        '''
        
        basic_airlink.slog("Step:  Query GSM/HSPA diversity antenna by AT command")
        cmd="AT*RXDIVERSITY?"
        return self.query(instance,cmd)          
    
    def set_hspa_diversity(self, instance, flag ):
        ''' set GSM/HSPA diversity by AT command AT*RXDIVERSITY=[1|0]
        
        Args: 
            instance: Telnet/SSH/Serial connection instance 
            flag:
                1 - Enable support for diversity anntenna (default)
                0 - Disable
                
        Returns:
            True/False
        '''
        
        basic_airlink.slog("Step:  set GSM/HSPA  diversity  AT command")
        cmd="AT*RXDIVERSITY="+flag
        return self.assign(instance,cmd)       
