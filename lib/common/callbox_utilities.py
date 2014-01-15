###############################################################################
#
# This module provides Callbox (Anritsu and Rohde Schwarz) operations. 
# Company: Sierra Wireless
# Time: Apr 2nd, 2013
# Author: Airlink
# 
################################################################################

import os, time,logging,datetime
import basic_airlink
import pyvisa.visa

class AnritsuMD8475A(object):
    '''  This class provides a few methods for callbox Anritsu operations: launch/close application, load parameters, 
         start/stop simulation, and get the DUT status.
    '''

    def __init__(self):
        ''' Inits date, time, airlinkautomation_home
        Args: None
        Returns: None
        '''
        self.airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME']
        current_date_time = datetime.datetime.now()

        basic_airlink.slog(str(current_date_time)+ " Please launch WnsProxy and change NAT!")
        
    def launch_smart_studio(self):
        ''' launch callbox application 
        Args: None
        Returns: 
        '''
        os.chdir(self.airlinkautomation_home_dirname+'/tools/WnsRemoteExe')
        cmd ='WnsRemote.exe 0 1.1.0.1 1.1.0.1 >ttt_launch.txt'
        current_date_time = datetime.datetime.now()
        basic_airlink.slog(str(current_date_time)+ " launch callbox application which will take about 2 mins ...")
        ret=os.system(cmd)
        logging.debug(ret)
        time.sleep(90)

        if os.path.getsize("ttt_launch.txt") == 0: 
            return ""
        
        fh=open('ttt_launch.txt','r')
        for line in fh: 
            basic_airlink.slog(line)
            #words = line.split(" = ")
            return line   
                
    def close_smart_studio(self):
        ''' close application 
        Args: None
        Returns: close result
        '''
        os.chdir(self.airlinkautomation_home_dirname+'/tools/WnsRemoteExe')
        cmd ='WnsRemote.exe 5 1.1.0.1 >ttt_close.txt '
        current_date_time = datetime.datetime.now()
        basic_airlink.slog(str(current_date_time)+ " Close callbox application ...")
        ret=os.system(cmd)
        time.sleep(30)
        logging.debug(ret)

        if os.path.getsize("ttt_close.txt") == 0: 
            return ""
        
        fh=open('ttt_close.txt','r')
        for line in fh: 
            basic_airlink.slog(line)
            #words = line.split(" = ")
            return line       
        
    def load_sim_param_file(self, filename):
        ''' Load SIM parameter file  
        Args: 
            filename: string, SIM parameter file name
        Returns: None
        ''' 

        current_date_time = datetime.datetime.now()
        basic_airlink.slog(str(current_date_time)+ " Take 30s to load SIM Parameters file: "+filename)

        os.chdir(self.airlinkautomation_home_dirname+'/tools/WnsRemoteExe')
        cmd ='WnsRemote.exe 1 1.1.0.1 '+filename +"  >ttt_load_sim.txt"
        os.system(cmd) 
        time.sleep(30)
       
 
    def load_cell_param_file(self, filename):
        ''' Load Cell Parameters file 
        Args: 
            filename: string, cell parameter file name
        Returns: None
        ''' 
        current_date_time = datetime.datetime.now()
        basic_airlink.slog(str(current_date_time)+ " Take 5s to load cell Parameters file: " + filename)
        os.chdir(self.airlinkautomation_home_dirname+'/tools/WnsRemoteExe')
        cmd ='WnsRemote.exe 2 1.1.0.1 '+filename+"  >ttt_load_cell.txt"
        os.system(cmd)              
        time.sleep(5)
               
    def start_simulator(self):
        ''' Start Simulation
        Args: None
        Returns: None
        '''         
        os.chdir(self.airlinkautomation_home_dirname+'/tools/WnsRemoteExe')
        current_date_time = datetime.datetime.now()
        basic_airlink.slog(str(current_date_time)+ " Start simulation, wait about 3 mins")
        cmd = 'WnsRemote.exe 3 1.1.0.1 >ttt_start.txt'
        os.system(cmd)    
        time.sleep(180)

        if os.path.getsize("ttt_start.txt") == 0: 
            return ""
        
        fh=open('ttt_start.txt','r')
        for line in fh: 
            basic_airlink.slog(line) 

            if line.find("FAIL",0) >= 0:
                return "FAIL"  
            
        return ""
   
    def stop_simulator(self):
        ''' Stop Simulation  
        Args: None
        Returns: None
        ''' 

        current_date_time = datetime.datetime.now()
        basic_airlink.slog(str(current_date_time)+ " Stop Simulation ")
      
        os.chdir(self.airlinkautomation_home_dirname+'/tools/WnsRemoteExe')
        cmd = 'WnsRemote.exe 4 1.1.0.1  >ttt_stop.txt'
        os.system(cmd)  
        time.sleep(30)
        
        
    def get_ue_status(self):
        '''To get UE status (not network's) 
        Args: None
        Returns: UE status, e.g. "POWEROFF","DETACH", "REGISTRATION","PACKET TERMINATION","PACKET COMMUNICATION","FAIL".
        '''

        current_date_time = datetime.datetime.now()
        basic_airlink.slog(str(current_date_time)+ " Getting UE status ...")
 
        os.chdir(self.airlinkautomation_home_dirname+'/tools/WnsRemoteExe')
        cmd = 'WnsRemote.exe 6 1.1.0.1 >ue_status.txt '
        os.system(cmd) 
        time.sleep(30)

        if os.path.getsize("ue_status.txt") == 0: 
            return ""
        
        fh=open('ue_status.txt','r')
        for line in fh: 
            print line + "\n"
            #words = line.split(" = ")
            basic_airlink.slog(line)
            if line.find("PACKET COMMUNICATION",0) >= 0:
                return "PACKET COMMUNICATION"  
            elif line.find("PACKET TERMINATION",0) >= 0:
                return "PACKET TERMINATION"  
            elif line.find("FAIL",0) >= 0:
                return "FAIL"  
            elif line.find("POWEROFF",0) >= 0:
                return "POWEROFF"  
            elif line.find("Ok",0) >= 0:
                return "Ok"                          
            elif line.find("IDLE",0) >= 0:
                return "IDLE" 
            
            return ""
            
#        
#    def get_network_status(self):
#        '''To get network status (not UE's) 
#        Args: None
#        Returns: string, network status,e.g. "WIN RUN","WNS EXIT","WNS IDLE","WNS SIMULATION","FAIL", "OK"
#        '''
#        
#        current_date_time = datetime.datetime.now()
#        basic_airlink.slog(str(current_date_time)+ " To get network status")
#        os.chdir(self.airlinkautomation_home_dirname+'/tools/WnsRemoteExe')
#        cmd = 'WnsRemote.exe 7 1.1.0.1 >net_status.txt '
#        os.system(cmd) 
#        time.sleep(30)
#
#        if os.path.getsize("net_status.txt") == 0: 
#            return ""
#        
#        fh=open('net_status.txt','r')
#        for line in fh: 
#            basic_airlink.slog(line)
#            #words = line.split(" = ")
#            #print words
#            if line.find("WNS SIMULATION",0) >= 0:
#                return "WNS SIMULATION"  
#
#            elif line.find("WNS IDLE",0) >= 0:
#                return "WNS IDLE"  
#        
#                             
#        return ""
   
   
    def get_simulator_status(self):
        '''To get simulation status (not UE's) to check if it is in started/stopped/error
        Args: None
        Returns: (TBD)string, simulator status,e.g. "WIN RUN","WNS EXIT","WNS IDLE","FAIL", "WNS SIMULATION"
        '''
        
        current_date_time = datetime.datetime.now()
        basic_airlink.slog(str(current_date_time)+ " To get Simulation status (ERROR/STARTED/STOPEED)")
        os.chdir(self.airlinkautomation_home_dirname+'/tools/WnsRemoteExe')
        cmd = 'WnsRemote.exe 7 1.1.0.1 >simulation_status.txt '
        os.system(cmd) 
        time.sleep(30)

        if os.path.getsize("simulation_status.txt") == 0: 
            return ""
        
        fh=open('simulation_status.txt','r')
        for line in fh: 
            basic_airlink.slog(line)
            #words = line.split(" = ")
            #print words
            if line.find("WNS SIMULATION",0) >= 0:
                return "WNS SIMULATION"  

            elif line.find("WNS IDLE",0) >= 0:
                return "STOPPED"  

            elif line.find("FAIL",0) >= 0:
                return "FAIL"          
                             
        return ""
    
    def start_ims(self):
        ''' Start IMS
        Args: None
        Returns: None
        '''         
        os.chdir(self.airlinkautomation_home_dirname+'/tools/WnsRemoteExe')
        current_date_time = datetime.datetime.now()
        basic_airlink.slog(str(current_date_time)+ " Start IMS, wait about 3 secs")
        cmd = 'WnsRemote.exe 8 1.1.0.1 >ttt_start_ims.txt'
        os.system(cmd)    
        time.sleep(3)       

    def udp_iperf(self, server_ip, wan_ip, dl_datarate,  ul_datarate, duration,  packet_size, port_no):
        '''
        Execute UDP iperf commands, and get the throughput rate
        Args: 
            dl_daterate:   Downlink Date rate unit kbps
            ul_daterate:   Uplink Date rate unit kbps
            duration:      Iperf duration seconds 
            packet_length: packet length bytes
        Returns: 
            Output UDP iperf results to a file udp_throughput_iperf.txt
            
        '''
        os.chdir(self.airlinkautomation_home_dirname+'/tools/WnsRemoteExe')
        
        current_date_time = datetime.datetime.now()
        
        cmd = 'WnsRemote.exe 100 127.0.0.1 '+\
             server_ip+' '+ \
             wan_ip+' 0 ' + \
             str(dl_datarate) + ' ' +\
             str(ul_datarate) + ' ' +\
             str(duration)    + ' ' +\
             str(packet_size) +'  ' +\
             str(port_no) +'  ' +\
             '>>udp_throughput_iperf.txt'
             
        basic_airlink.slog(str(current_date_time)+ " Executing iperf command: " + cmd)
        
        os.system(cmd) 
                   
    def wns_proxy(self):
        ''' Launch wnsProxy.exe as administrator
        Args:    None
        Returns: None
        '''
        os.chdir(self.airlinkautomation_home_dirname+'/tools/WnsProxy')
        current_date_time = datetime.datetime.now()
        cmd = 'WnsProxy.exe &'
        basic_airlink.slog(str(current_date_time)+ " Executing " + cmd)
        os.system(cmd) 
        time.sleep(30)
        basic_airlink.slog(str(current_date_time)+ " Done " + cmd)

    def route_add(self, server_ip, local_ip):
        ''' Add route as administrator
        Args:    None
        Returns: None
        '''
        current_date_time = datetime.datetime.now()
        cmd = 'route ADD '+server_ip +' MASK 255.255.255.255 '+local_ip+' METRIC 30 '
        basic_airlink.slog(str(current_date_time)+ " Executing " + cmd)
        os.system(cmd) 
        time.sleep(30)
        basic_airlink.slog(str(current_date_time)+ " Done " + cmd)
        
    def route_delete(self, server_ip, local_ip):
        ''' Add route as administrator
        Args:    None
        Returns: None
        '''
        current_date_time = datetime.datetime.now()
        cmd = 'route DELETE '+server_ip 
        basic_airlink.slog(str(current_date_time)+ " Executing " + cmd)
        os.system(cmd) 
        time.sleep(30)
        basic_airlink.slog(str(current_date_time)+ " Done " + cmd)
                      
    def tcp_iperf(self, server_ip, wan_ip, dl_flag, ul_flag, duration, window_size, port_no):
        ''' Execute TCP iperf commands, and get the throughput rate
        
        Args: 
            dl_flag:   0 - don't, 1 - do Downlink transfer
            ul_flag:   0 - don't, 1 - do Uplink transfer
            duration:    iperf duration seconds 
            window_size: TCP ipser window size
            port_no:  number of port used fro transfer
            
        Returns: 
            Output TCP iperf results to a file tcp_throughput_iperf.txt
            
        '''
        os.chdir(self.airlinkautomation_home_dirname+'/tools/WnsRemoteExe')
        
        current_date_time = datetime.datetime.now()
        
        cmd = 'WnsRemote.exe 101 127.0.0.1 '+server_ip+' '+ wan_ip +' 0 '+ \
           str(dl_flag) + '  ' +str(ul_flag) + ' ' + str(duration) + ' ' + \
           str(window_size) +' '+ str(port_no)+' >>tcp_throughput_iperf.txt'
           
        basic_airlink.slog(str(current_date_time)+ " Executing TCP iperf command: \n" + cmd)
        
        os.system(cmd)
                

    def handover(self):
        ''' TODO '''
        
        pass  
    

    def callbox_ready(self,tbd_config_map, throughput_config_map):
        ''' make callbox is in ready for test 
        
        Args: 
            tbd_config_map : a list, test bed configuration
            throughput_config_map: a list, throughput test configuration
            
        Returns:
            True/False
        '''
        device_name = tbd_config_map["DUTS"][0]
        
        if  tbd_config_map[device_name]["RM_TYPE"] == "MC7750":
            
            if   tbd_config_map[device_name]["NET_SERVICE_TYPE"].find("LTE",0) >=0:
                sim_param_filename  = throughput_config_map["SIM_PARAM_FILE"]["VZW_LTE"]
                cell_param_filename = throughput_config_map["CELL_PARAM_FILE"]["VZW_LTE"]  
                
            elif   tbd_config_map[device_name]["NET_SERVICE_TYPE"].find("EV-DO",0) >=0:
                sim_param_filename  = throughput_config_map["SIM_PARAM_FILE"]["VZW_EVDO"]
                cell_param_filename = throughput_config_map["CELL_PARAM_FILE"]["VZW_EVDO"]   
                          
        elif tbd_config_map[device_name]["RM_TYPE"] == "MC7700":
            
            if  tbd_config_map[device_name]["NET_SERVICE_TYPE"].find("LTE",0) >=0:

                sim_param_filename  = throughput_config_map["SIM_PARAM_FILE"]["ATT_LTE"]
                cell_param_filename = throughput_config_map["CELL_PARAM_FILE"]["ATT_LTE"]  
                  
            elif  tbd_config_map[device_name]["NET_SERVICE_TYPE"].find("3G",0) >=0:
                sim_param_filename  = throughput_config_map["SIM_PARAM_FILE"]["ATT_HSPA"]
                cell_param_filename = throughput_config_map["CELL_PARAM_FILE"]["ATT_HSPA"] 
                
        simu_status   = self.get_simulator_status()
        
        if simu_status == "WNS SIMULATION": 
            return True
                
        ue_status   = self.get_ue_status()
        
        if ue_status == "FAIL":
 
            #self.wns_proxy()   
            self.stop_simulator()        
            self.close_smart_studio()        
            
            self.launch_smart_studio()
            basic_airlink.slog("SIM parameter filename = "  + sim_param_filename)    
            basic_airlink.slog("Cell parameter filename = " + cell_param_filename)             
            self.load_sim_param_file(sim_param_filename)
            self.load_cell_param_file(cell_param_filename)
            #if tbd_config_map[self.device_name]["RM_TYPE"] == "MC7750":
            #    self.start_ims()

            if self.start_simulator() == "FAIL": 
                self.fail_flag += 1
                basic_airlink.slog("SIMULATION failed to start up, you can restart callbox") 
                return False
            else:
                return True
   
 
        elif ue_status == "POWEROFF" or ue_status == "PACKET TERMINATION":
            
            basic_airlink.slog("Wait 3 minutes")
            time.sleep(180)   
                
            simu_status = self.get_simulator_status()

            if simu_status == "FAIL":
                self.fail_flag +=1
                return False
            else:
                return True       
    
class RsCMW500(object):
    '''  To provide callbox R&S CMW500 operations  '''
 
    def __init__(self):
        ''' Inits date,time, and airlinkautomation_home variable  '''
        
        self.airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME']
        
        current_date_time = datetime.datetime.now()

        basic_airlink.slog(str(current_date_time))
        
        
    def cell_net(self,cell_network):
        '''  format the cell network technology name to suite for SCPI command 
        LTE -> LTE
        WCDMA -> WCDMa
        EVDO -> EVDO
        CDMA -> CDMA
        GSM | EDGE -> GSM
        Args: 
            cell_network: string, "LTE","WCDMA", "CDMA","GSM","EDGE"
        Return: 
            string, "LTE","WCDMa", "CDMA","GSM","EDGE"
            -1: invalid 
        '''
        if cell_network == "LTE":
            return "LTE"
            
        elif cell_network == "WCDMA":
            return "WCDMa"
            
        elif cell_network == "EVDO":
            return "EVDO"
            
        elif cell_network == "CDMA":
            return "CDMA"
            
        elif cell_network == "GSM" or cell_network == "EDGE":
            return "GSM"
            
        else: 
            basic_airlink.slog("Cell network parameter is incorrect")
            return -1


    def connect(self, VISA_address):
        ''' connect test controller to CMW500 tester via Ethernet (TCPIP), GPIB
        
        Args: 
           VISA_address:  VISA address, refer to "CBX_CMW500" section in configuration file testbed2conf.yml
        Returns: 
            True   connect successfully
            False  connection failed  
        '''       
        try:
            self.visa_instance = pyvisa.visa.instrument(VISA_address) 
            
        except Exception as e:
            
            print type(e)
            basic_airlink.slog(" VISA connection failed" + type(e))
            return False
            
        finally:
            return True
    
    
    def close(self):
        ''' Disconnect controller and CMW500 tester
        '''
        self.visa_instance.close()
        

    def clear(self):
        ''' Execute Clear command 
        Args: None
        Returns: 
            True Execute successfully 
            False execution failed 
        '''
        
        try:
            self.visa_instance.ask("*CLS;*OPC?")
        except Exception as e:
            basic_airlink.slog(" clear command failed: " + type(e))
            return False
            
        finally:
            return True  
  
            
    def reset(self):
        ''' reset command '''
        
        try:
            self.visa_instance.ask("*RST;*OPC?")
        except Exception as e:
            basic_airlink.slog(" reset command failed: " + type(e))
            return False
            
        finally:
            return True            
        

    def  get_opt(self):
        ''' run the command "*OPT?" to query 
        '''
                
        try:
            self.visa_instance.ask("*OPT?")
        except Exception as e:
            basic_airlink.slog(" OPT command failed: " + type(e))
            return False
            
        finally:
            return True  
        
 
    def  get_idn(self):
        ''' run the command "*IDN?" to query the ID''' 
               
        try:
            self.visa_instance.ask("*IDN?")
        except Exception as e:
            basic_airlink.slog(" IDN command failed: " + type(e))
            return False
            
        finally:
            return True
               
 
    def  get_system_error(self):
        ''' run the command "SYSTemERRor?" to get the system error
        '''
        self.visa_instance.ask("SYSTEMERROR?")
        basic_airlink.slog(" Done")      

       
    def set_main_rf_ports(self,cell_network,ul_connector, ul_convertor,dl_connector,dl_convertor):
        ''' Select the port to use for measurements.
               cell_network   LTE/CDMA/GSM/EDGE/EVDO/WCDMA
        TODO:  check the CDMA  and GSM command format       
        Args: 
             ulport  UL port 
             dlport  DL port 
        Returns:
            True  - OK
            False - failed 
        '''

        basic_airlink.slog("Select RF port")   
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
         
        try:
            
            self.visa_instance.ask("ROUTe:"+netcell+":SIGN:SCENario:SCELl "+ul_connector+","+ ul_convertor+","+dl_connector+","+dl_convertor+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting RF port (DL/UL) failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True    
        
    def set_fading(self,cell_network,ul_connector, ul_convertor,dl_connector,dl_convertor,iq_level):
        ''' Select the port to use for measurements.
               cell_network   LTE/CDMA/GSM/EDGE/EVDO/WCDMA
        TODO:  check the CDMA  and GSM command format       
        ARGs: 
             ulport  UL port 
             dlport  DL port 
        Returns:
            True  - OK
            False - failed 
        '''

        basic_airlink.slog("Select RF Fading")   
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
         
        try:
            
            self.visa_instance.ask("ROUTe:"+netcell+":SIGN:SCENario:SCFading "+ul_connector+","+ ul_convertor+","+dl_connector+","+dl_convertor+","+iq_level+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting RF fading (DL/UL) failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True    
                                 
        
    def set_input_pathloss(self, cell_network, passloss):
        ''' Set input passloss for LTE,  WCDMA  and GSM, e.g. CONFigure:LTE:SIGN:RFSettings:EATTenuation:INPut 2 '''
        
        basic_airlink.slog("set input passloss ")
        
#        DL_PL = 26.870000

        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
        
        try:
            
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:RFSettings:EATTenuation:INPut "+str(passloss)+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting pathloss DL failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True     

    def set_output(self, cell_network, output_val):
        ''' Set output for LTE, WCDMA and GSM, e.g. CONFigure:LTE:SIGN:RFSettings:EATTenuation:OUTPut 2 '''
        
        basic_airlink.slog("set output")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
        
        try:
            
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:RFSettings:EATTenuation:OUTPut "+output_val+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" set output failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
                   
    def set_input(self, cell_network, input_val):
        ''' Set output for LTE, WCDMA and GSM, e.g. CONFigure:LTE:SIGN:RFSettings:EATTenuation:INPut 2 '''
        
        basic_airlink.slog("set input")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
        
        try:
            
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:RFSettings:EATTenuation:INPut "+input_val+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" set input failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
        
        
    def set_output_pathloss(self, cell_network, passloss):
        ''' Set output passloss for LTE, WCDMA and GSM, e.g. CONFigure:LTE:SIGN:RFSettings:EATTenuation:OUTPut 2 '''
        
        basic_airlink.slog("set output passloss")
        
#        UL_PL = 30.730000

        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
        
        try:
            
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:RFSettings:EATTenuation:OUTPut "+str(passloss)+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" set pathloss UL failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
               
 
    def set_band(self, cell_network, band):
        ''' Set band 
        ARGs:
              cell_network   LTE/CDMA/GSM/EDGE/EVDO/WCDMA
              band            band  used, eg. OB17
            
        '''
        basic_airlink.slog("set band")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:BAND "+band+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting band failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True   
    

    def set_ul_channel(self, cell_network, ul_chan):
        
        basic_airlink.slog("set UL channel")
 
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:RFSettings:CHANnel:UL "+ul_chan +";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting UL channel failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True   
               
 
    def set_dl_channel(self, cell_network, dl_chan):
        
        basic_airlink.slog("set DL channel")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:RFSettings:CHANnel:DL "+dl_chan +";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" setting DL channel failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 

 
    def get_dl_frequency(self, cell_network):
        
        basic_airlink.slog("Get DL frequency")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:RFSettings:CHANnel:DL? Hz "+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Getting DL frequency failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
        

    def get_ul_frequency(self, cell_network):
        
        basic_airlink.slog("Get UL frequency")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:RFSettings:CHANnel:UL? Hz "+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Getting UL frequency failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
                        

    def set_dl_foffset(self, cell_network, dl_foffset):
        
        basic_airlink.slog("set DL frequency offset")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:RFSettings:FOFFset:DL "+dl_foffset +";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" setting DL frequency offset failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
 
 
    def set_ul_foffset(self, cell_network, ul_foffset):
        
        basic_airlink.slog("set UL frequency offset ")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:RFSettings:FOFFset:DL "+ul_foffset +";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" setting UL frequency offset failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
        
  
    def set_enp_mode(self, cell_network, enp_mode):
        
        basic_airlink.slog("set UL frequency offset ")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:RFSettings:ENPMode "+enp_mode +";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" setting exp nomial powermode failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
                      
    def set_dl_rsepre_level(self, cell_network, dl_epre_level):
        
        basic_airlink.slog("set DL EPRE level")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:RFSettings:DL:RSEPre:LEVel "+str(dl_epre_level) +";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting DL EPRE level failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 


    def set_ul_open_loop_nominal_power(self, cell_network, ul_open_loop_nominal_power):
        
        basic_airlink.slog("set UL open loop nominal power")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:UL:PUSCH:LEVel "+str(ul_open_loop_nominal_power) +";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting UL open loop nominal power failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True
        
        
    def set_ul_close_loop_target_power(self, cell_network, ul_close_loop_target_power):
        
        basic_airlink.slog("set UL close loop target power")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:UPLink:TPC:CLTPower "+str(ul_close_loop_target_power) +";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting UL close loop target power failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True
        
        
    def set_ul_max_allowed_power(self, cell_network, ul_max_allowed_power):
        
        basic_airlink.slog("set UL max allowed power")
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:UL:PMAX "+str(ul_max_allowed_power) +";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting UL max allowed power failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True
        
        
    def set_ul_tpc_closed_loop(self, cell_network):
        
        basic_airlink.slog("set UL TPC to Closed Loop")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:UL:TPC:SET CLoop;*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting UL TPC to Closed Loop failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True
        
        
    def set_dl_cell_bandwidth(self, cell_network,band_width):
        ''' Configure Signalling  cell bandwidth DL,e.g. CONFigure:LTE:Signaling:CELL:BANDwidth:DL B100;*OPC? '''
        
        basic_airlink.slog("Configure Signalling  cell bandwidth DL")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":Signaling:CELL:BANDwidth:DL "+band_width+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting DL cell bandwidth failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True

        
    def set_cell_pcid(self, cell_network,pcid):
        ''' Configure cell PCID,e.g. CONFigure:LTE:SIGN:CELL:PCID 0;*OPC? '''
        
        basic_airlink.slog("Configure cell PCID")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CELL:PCID "+pcid+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting cell PCID failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True
         
 
    def set_cell_phic(self, cell_network,phic):
        ''' Configure cell PHIC,e.g. CONFigure:LTE:SIGN:CELL:PHIC Half;*OPC? '''
        
        basic_airlink.slog("Configure cell PHIC")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CELL:PHIC "+phic+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting cell PHIC failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True
 
 
    def set_dl_sss_poffset(self, cell_network, dl_sss_poffset):
        ''' Configure DL SSS POFFSET,e.g. CONFigure:LTE:SIGN:DL:SSS:POFFset 0;*OPC? '''
        
        basic_airlink.slog("Configure DL SSS POFFSET")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:DL:SSS:POFFset "+dl_sss_poffset+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting DL SSS POFFSET failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True
                     

    def set_dl_pbch_poffset(self, cell_network, dl_pbch_poffset):
        ''' Configure DL PBCH POFFSET,e.g. CONFigure:LTE:SIGN:DL:PBCH:POFFset 0;*OPC? '''
        
        basic_airlink.slog("Configure DL PBCH POFFSET")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:DL:PBCH:POFFset "+dl_pbch_poffset+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting DL PBCH POFFSET failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True
 
 
    def set_dl_pss_poffset(self, cell_network, dl_pss_poffset):
        ''' Configure DL PSS POFFSET,e.g. CONFigure:LTE:SIGN:DL:PSS:POFFset 0;*OPC? '''
        
        basic_airlink.slog("Configure DL PSS POFFSET")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:DL:PSS:POFFset "+dl_pss_poffset+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting DL PSS POFFSET failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True

 
    def set_dl_pcfich_poffset(self, cell_network, dl_pcfich_poffset):
        ''' Configure DL PCFICH POFFSET,e.g. CONFigure:LTE:SIGN:DL:PCFich:POFFset 0;*OPC? '''
        
        basic_airlink.slog("Configure DL PCFICH POFFSET")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:DL:PCFICH:POFFset "+dl_pcfich_poffset+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting DL PCFICH POFFSET failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True
 
 
    def set_dl_phich_poffset(self, cell_network, dl_phich_poffset):
        ''' Configure DL PHICH POFFSET,e.g. CONFigure:LTE:SIGN:DL:PHICh:POFFset -12;*OPC? '''
        
        basic_airlink.slog("Configure DL PHICH POFFSET")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:DL:PHICh:POFFset "+dl_phich_poffset+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting DL PHICH POFFSET failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True

 
    def set_dl_pdcch_poffset(self, cell_network, dl_pdcch_poffset):
        ''' Configure DL PDCCH POFFSET,e.g. CONFigure:LTE:SIGN:DL:PDCCh:POFFset 0;*OPC? '''
        
        basic_airlink.slog("Configure DL PDCCH POFFSET")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:DL:PDCCh:POFFset "+dl_pdcch_poffset+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting DL PDCCH POFFSET failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True
 
  
    def set_dl_ocng(self, cell_network, dl_ocng):
        ''' Configure DL OCNG,e.g. CONFigure:LTE:SIGN:DL:OCNG OFF;*OPC? '''
        
        basic_airlink.slog("Configure DL OCNG to ON or OFF")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:DL:OCNG "+dl_ocng+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting DL OCNG failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True

  
    def set_dl_pdsch_rindex(self, cell_network, dl_pdsch_rindex):
        ''' Configure DL PDSCH RINDEX,e.g. CONFigure:LTE:SIGN:DL:PDSCh:RINDex 0;*OPC? '''
        
        basic_airlink.slog("Configure DL PDSCH RINDEX")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:DL:PDSCh:RINDex "+dl_pdsch_rindex+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting DL PDSCH RINDEX failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True


  
    def set_dl_pdsch_pa(self, cell_network, dl_pdsch_pa):
        ''' Configure DL PDSCH PA,e.g. CONFigure:LTE:SIGN:DL:PDSCh:PA ZERO;*OPC? '''
        
        basic_airlink.slog("Configure DL PDSCH PA")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:DL:PDSCh:PA "+dl_pdsch_pa+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting DL PDSCH PA failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True

  
    def set_dl_awgn(self, cell_network, dl_awgn):
        ''' Configure DL AWGN,e.g. CONFigure:LTE:SIGN:DL:AWGN OFF;*OPC? '''
        
        basic_airlink.slog("Configure DL AWGN to ON or OFF")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:DL:AWGN "+dl_awgn+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting DL AWGN failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True
 
   
    def set_cell_security_authenticate(self, cell_network, cell_security_authenticate):
        ''' Configure security authenticate,e.g. CONFigure:LTE:SIGN:CELL:SECurity:AUTHenticat OFF;*OPC? '''
        
        basic_airlink.slog("Configure CELL security authenticate")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CELL:SECurity:AUTHenticat "+cell_security_authenticate+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting CELL security authenticate failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True


    def set_cell_security_nas(self, cell_network, cell_security_nas):
        ''' Configure security authenticate,e.g. CONFigure:LTE:SIGN:CELL:SECurity:NAS OFF;*OPC? '''
        
        basic_airlink.slog("Configure cell security NAS to ON or OFF")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CELL:SECurity:NAS "+cell_security_nas+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting cell security NAS failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True
 
 
    def set_cell_security_as(self, cell_network, cell_security_as):
        ''' Configure security authenticate,e.g. CONFigure:LTE:SIGN:CELL:SECurity:AS OFF;*OPC?'''
        
        basic_airlink.slog("Configure cell security AS to ON or OFF")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CELL:SECurity:AS "+cell_security_as+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting cell security AS failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True       
        

    def set_cell_security_ialgorithm(self, cell_network, cell_security_ialgorithm):
        ''' Configure security IALGORITHM,e.g. CONFigure:LTE:SIGN:CELL:SECurity:IALGorithm NULL;*OPC?'''
        
        basic_airlink.slog("Configure cell security IALGORITHM")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CELL:SECurity:IALGorithm "+cell_security_ialgorithm+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting cell security IALGORITHM failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 


    def set_cell_security_milenage(self, cell_network, cell_security_milenage):
        ''' Configure security IALGORITHM,e.g. CONFigure:LTE:SIGN:CELL:SECurity:MILenage OFF;*OPC?'''
        
        basic_airlink.slog("Configure cell security MILenage")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CELL:SECurity:MILenage "+cell_security_milenage+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting cell security MILenage failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 


    def set_cell_security_skey(self, cell_network, cell_security_skey):
        ''' Configure security SKEY,e.g. CONFigure:LTE:SIGN:CELL:SECurity:SKEY #H000102030405060708090A0B0C0D0E0F;*OPC?'''
        
        basic_airlink.slog("Configure cell security SKEY")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CELL:SECurity:SKEY "+cell_security_skey+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting cell security SKEY failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 


    def set_cell_security_opc(self, cell_network, cell_security_opc):
        ''' Configure security SKEY,e.g. CONFigure:LTE:SIGN:CELL:SECurity:OPC #H00000000000000000000000000000000;*OPC?'''
        
        basic_airlink.slog("Configure cell security OPC")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CELL:SECurity:OPC "+cell_security_opc+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting cell security OPC failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
 
 
    def set_cell_ueid_imsi(self, cell_network, cell_ueid_imsi):
        ''' Configure UE IDentity IMSI,e.g. CONFigure:LTE:SIGN:CELL:UEIDentity:IMSI "001010123456789";*OPC?'''
        
        basic_airlink.slog("Configure cell UE IDentity IMSI")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CELL:UEIDentity:IMSI "+cell_ueid_imsi+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting cell UE IDentity IMSI failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 

 
    def set_cell_mcc(self, cell_network, cell_mcc):
        ''' Configure cell MCC,e.g. CONFigure:LTE:SIGN:CELL:MCC 1;*OPC?'''
        
        basic_airlink.slog("Configure cell MCC")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CELL:MCC "+cell_mcc+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting cell MCC failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
        
 
    def set_cell_mnc_digits(self, cell_network, cell_mnc_digits):
        ''' Configure CELL MNC digits,e.g. CONFigure:LTE:SIGN:CELL:MNC:DIGits TWO;*OPC?'''
        
        basic_airlink.slog("Configure cell MNC digits")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CELL:MNC:DIGits "+cell_mnc_digits+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting cell MNC digits failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 

 
    def set_cell_mnc(self, cell_network, cell_mnc):
        ''' Configure cell MNC,e.g. CONFigure:LTE:SIGN:CELL:MNC 1;*OPC?'''
        
        basic_airlink.slog("Configure cell MNC")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CELL:MNC "+cell_mnc+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting cell MNC failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 

 
    def set_cell_tac(self, cell_network, cell_tac):
        ''' Configure cell TAC,e.g. CONFigure:LTE:SIGN:CELL:TAC 1;*OPC?'''
        
        basic_airlink.slog("Configure cell TAC")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CELL:TAC "+cell_tac+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting cell TAC failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
        
  
    def set_cell_cid_eutran(self, cell_network, cell_cid_entran):
        ''' Configure cell CID EUTRAN,e.g. CONFigure:LTE:SIGN:CELL:CID:EUTRan #B0000000000000010000000000000;*OPC?'''
        
        basic_airlink.slog("Configure cell CID EUTRAN")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CELL:CID:EUTRan "+cell_cid_entran+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting cell CID EUTRAN failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
 
 
    def set_connection_tmode(self, cell_network, connection_tmode):
        ''' Configure connection tmode,e.g. CONFigure:LTE:SIGN:CONNection:TMODe OFF;*OPC?'''
        
        basic_airlink.slog("Configure connection tmode to ON or OFF")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CONNection:TMODe "+connection_tmode+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting connection tmode failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
        
        
    def set_connection_dlpadding(self, cell_network, connection_dlpadding):
        ''' Configure connection DL Padding,e.g. CONFigure:LTE:SIGN:CONNection:DLPadding ON;*OPC?'''
        
        basic_airlink.slog("Configure connection DL Padding")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CONNection:DLPadding "+connection_dlpadding+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting connection DL Padding failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
 
         
    def set_connection_dleinsertion(self, cell_network, connection_dleinsertion):
        ''' Configure connection DLEinsertion,e.g. CONFigure:LTE:SIGN:CONNection:DLEinsertion 0;*OPC?'''
        
        basic_airlink.slog("Configure connection DLEinsertion")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CONNection:DLEinsertion "+connection_dleinsertion+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting connection DLEinsertion failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
               
         
    def set_connection_asemission(self, cell_network, connection_asemission):
        ''' Configure connection ASEMission,e.g. CONFigure:LTE:SIGN:CONNection:ASEMission NS06;*OPC?'''
        
        basic_airlink.slog("Configure connection ASEMission")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CONNection:ASEMission "+connection_asemission+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting connection ASEMission failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
        

    def set_connection_ueterminate(self, cell_network, connection_ueterminate):
        ''' Configure connection UE terminate,e.g. CONFigure:LTE:SIGN:CONNection:UETerminate RMC;*OPC?'''
        
        basic_airlink.slog("Configure connection UETerminate")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CONNection:UETerminate "+connection_ueterminate+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting connection UETerminate failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
 
 
    def set_dl_connection_rmc(self, cell_network, dl_connection_rmc):
        ''' Configure connection RMC DL,e.g. CONFigure:LTE:SIGN:CONNection:RMC:DL N50,QPSK,KEEP;*OPC?'''
        
        basic_airlink.slog("Configure connection RMC DL")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CONNection:RMC:DL "+dl_connection_rmc+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting connection RMC DL failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 

 
    def set_ul_connection_rmc(self, cell_network, ul_connection_rmc):
        ''' Configure connection RMC UL,e.g. CONFigure:LTE:SIGN:CONNection:RMC:UL N50,QPSK,KEEP;*OPC?'''
        
        basic_airlink.slog("Configure connection RMC UL")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CONNection:RMC:UL "+ul_connection_rmc+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting connection RMC UL failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True 
        
 
    def set_connection_fcoefficient(self, cell_network, connection_fcoefficient):
        ''' Configure connection FCOefficient,e.g. CONFigure:LTE:SIGN:CONNection:FCOefficient FC4;*OPC?'''
        
        basic_airlink.slog("Configure connection FCOefficient")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CONNection:FCOefficient "+connection_fcoefficient+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting connection FCOefficient failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True

 
    def set_dl_connection_rmc_rbposition(self, cell_network, dl_connection_rmc_rbposition):
        ''' Configure connection RMC RBPosition DL,e.g. CONFigure:LTE:SIGN:CONNection:RMC:RBPosition:DL LOW;*OPC?'''
        
        basic_airlink.slog("Configure connection RMC RBPosition DL")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CONNection:RMC:RBPosition:DL "+dl_connection_rmc_rbposition+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting connection RMC RBPosition DL failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True
 
  
    def set_ul_connection_rmc_rbposition(self, cell_network, ul_connection_rmc_rbposition):
        ''' Configure connection RMC RBPosition UL,e.g. CONFigure:LTE:SIGN:CONNection:RMC:RBPosition:UL LOW;*OPC?'''
        
        basic_airlink.slog("Configure connection RMC RBPosition UL")
        
        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("CONFigure:"+netcell+":SIGN:CONNection:RMC:RBPosition:UL "+ul_connection_rmc_rbposition+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting connection RMC RBPosition UL failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True
                
                                                                                                                                                                                                                                 
    def set_signal(self, cell_network, signal_state): 
        ''' Set Signal to ON or OFF 
        
        TODO: need to debug for non-LTE command format '''
        
        basic_airlink.slog("set signal " + signal_state)
        

        netcell=self.cell_net(cell_network)  
        if netcell == -1:
            return False
 
        try:          
            self.visa_instance.ask("SOURce:"+netcell+":SIGNaling:CELL:STATe "+signal_state+";*OPC?")
            
        except Exception as e:
            basic_airlink.slog(" Setting signal state failed, and got the exception: " + type(e))
            return False
            
        finally:
            return True
        
        signal = ""
        time.sleep(10)
        
        while signal != signal_state:
            tt=self.visa_instance.ask("SOURce:LTE:SIGNaling:CELL:STATe? ")
            if tt.find(signal_state,0) >= 0:
                signal = signal_state
        
  
        basic_airlink.slog("signal is " + signal_state)

                                                                                                                              
    def call_setup_LTE(self): 
        ''' call setup LTE 
        
        TODO: to be updated'''
            
        basic_airlink.slog("call setup LTE configuration")
        
        self.set_dl_cell_bandwidth("LTE","B100")
        self.set_cell_pcid("LTE","0")
        self.set_cell_phic("LTE","Half")
        self.set_dl_sss_poffset("LTE","0")
        self.set_dl_pbch_poffset("LTE","0")
        self.set_dl_pss_poffset("LTE","0")
        self.set_dl_pcfich_poffset("LTE","0")
        self.set_dl_phich_poffset("LTE","-12")
        self.set_dl_pdcch_poffset("LTE","0")
        self.set_dl_ocng("LTE","OFF")
        self.set_dl_pdsch_rindex("LTE","0")
        self.set_dl_pdsch_pa("LTE","ZERO")
        self.set_dl_awgn("LTE","OFF")
        self.set_cell_security_authenticate("LTE","OFF")
        self.set_cell_security_nas("LTE","OFF")
        self.set_cell_security_as("LTE","OFF")
        self.set_cell_security_ialgorithm("LTE","NULL")
        self.set_cell_security_milenage("LTE","OFF")
        self.set_cell_security_skey("LTE","#H000102030405060708090A0B0C0D0E0F")
        self.set_cell_security_opc("LTE","#H00000000000000000000000000000000")
        self.set_cell_ueid_imsi("LTE","001010123456789")
        self.set_cell_mcc("LTE","1")
        self.set_cell_mnc_digits("LTE","TWO")
        self.set_cell_mnc("LTE","1")
        self.set_cell_tac("LTE","1")
        self.set_cell_cid_eutran("LTE","#B0000000000000010000000000000")
        self.set_connection_tmode("LTE","OFF")
        self.set_connection_dlpadding("LTE","ON")
        self.set_connection_dleinsertion("LTE","0")
        self.set_connection_asemission("LTE","NS06")
        self.set_connection_ueterminate("LTE","RMC")
        self.set_dl_connection_rmc("LTE","N50,QPSK,KEEP")
        self.set_ul_connection_rmc("LTE","N50,QPSK,KEEP")
        self.set_connection_fcoefficient("LTE","FC4")  
        self.set_dl_connection_rmc_rbposition("LTE","LOW")
        self.set_ul_connection_rmc_rbposition("LTE","LOW")
 
 
    def call_setup_CDMA2000(self): 
        ''' TODO: call setup CDMA2000 '''
         
        pass

 
    def call_setup_1xEVDO(self): 
        ''' TODO: call setup CDMA '''
         
        pass
    
     
    def call_setup_WCDMA(self): 
        ''' TODO: call setup WCDMA '''
         
        pass                

    def call_setup_GSM(self): 
        ''' TODO: call setup GSM '''
         
        pass
    
    
    def udp_iperf(self, dl_datarate,  ul_datarate, duration,  packet_size):
        ''' TODO '''
        
        pass


    def tcp_iperf(self, dl_datarate,  ul_datarate, duration,  packet_size):
        ''' TODO: '''
        
        pass


    def handover(self):
        ''' TODO: '''
        
        pass       
         
               
    def call_setup_config_file(self, filename='call_setup.cfg'): 
        ''' TODO: to be removed '''
            
        basic_airlink.slog("call setup configuration")

        fh=open(filename,'r')
        
        for line in fh: 
            self.visa_instance.ask(line)           
        fh.close()
                