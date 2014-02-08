import time
import os, sys
import multiprocessing
import threading
import socket
import urllib2
import basic_airlink

sys.path.append(os.environ['AIRLINKAUTOMATION_HOME'] + "/lib/common")
sys.path.append(os.environ['AIRLINKAUTOMATION_HOME'] + "/lib/site-packages")

import cisco_config
import cisco_asa_config
import yaml

class VpnCiscoProcess(multiprocessing.Process):
    # queue used to pass logging information from child process to main process
    log_queue = multiprocessing.Queue() 
    stop_logging_thread = False
    
    # strings that designate which task is to be done
    CONFIG_GATEWAY = "CONFIG_GATEWAY"
    CLEANUP_GATEWAY = "CLEANUP_GATEWAY"
    VERIFY_GATEWAY = "VERIFY_GATEWAY"
    CHECK_SA = "CHECK_SA"
    CHECK_GRE_TUNNEL = "CHECK_GRE_TUNNEL"
    CONFIG_AND_VERIFY_GRE_GATEWAY = "CONFIG_AND_VERIFY_GRE_GATEWAY"
    CLEAR_GRE_GATEWAY = "CLEAR_GRE_GATEWAY"
    WATCH_ERROR_MESSAGE = "WATCH_ERROR_MESSAGE"
    DUMMY = "DUMMY"

    def __init__(self, test_config, task, timeout, conn):
        multiprocessing.Process.__init__(self)

        self.conn = conn 
        self.task = task
        self.timeout = timeout
        self.test_config = test_config

        # save reference to log_queue, when new process forks with the call the start() the class variable in the new process gets over-written
        # we restore it when the new process starts (at the beginning of run())
        self.temp = self.__class__.log_queue 

        self.f = {self.CONFIG_GATEWAY: self.config_gateway,
                  self.CLEANUP_GATEWAY: self.cleanup_gateway,
                  self.VERIFY_GATEWAY: self.verify_gateway,
                  self.CHECK_SA: self.check_sa,
                  self.CHECK_GRE_TUNNEL: self.check_gre_tunnel,
                  self.CLEAR_GRE_GATEWAY: self.clear_gre_gateway,
                  self.CONFIG_AND_VERIFY_GRE_GATEWAY: self.config_and_verify_gre_gateway,
                  self.WATCH_ERROR_MESSAGE:self.watch_error_message,
                  self.DUMMY:self.dummy}[self.task]

    @classmethod # This method runs in the main process
    def create_and_execute(cls, task, config, timeout, retries):
        # Create a thread within the main process handle logging done in the child process 
        # as there's no way to log to the same file from multiple proccess in python
        cls.stop_logging_thread = False
        logging_thread = threading.Thread(target = cls.log_handler)
        logging_thread.start()

        for attempt in range(retries):
            conn, child_conn = multiprocessing.Pipe(duplex = False) # pipe so child process can send back results
            cisco_process = cls(config, task, timeout, child_conn) # create child process object - process is not created in system yet
            cisco_process.daemon = 1
            cisco_process.start() # fork new process in OS, the spawned process's entry point is cisco_process.run()

            if conn.poll(2*timeout):
                # Child process responded with results before time out
                result = conn.recv() # get results
            else:
                # Child process did not respond with results before time out
                result = {}
                result["EXCEPTION"] = True
                result["RESULT"] = False # set result to False so we won't break out of the FOR-loop if there are retries remaining
                basic_airlink.cslog("Child process timed out after %d seconds" %(2*timeout))

            if cisco_process.is_alive(): # kill child process if it's still alive
                try:
                    cisco_process.terminate()
                except WindowsError:
                    basic_airlink.slog("WindowsError excepted when terminating child process, try to terminate child process with os.system()...")
                    os.system("taskkill /pid %s /t /f >nul 2>&1" %str(cisco_process.pid))

                cisco_process.join(10)

            if not result["EXCEPTION"] and result["RESULT"]:
                # If no exception and result is positive, exit function and return the result
                break

        # stop the log handler thread
        cls.stop_logging_thread = True 
        logging_thread.join()

        # If the FOR-loop ends with result being False, then the test has failed and the False is returned
        return result["RESULT"]

    @classmethod
    def log_handler(cls): # This is a thread that runs in the main process to handle logging
        log_function = {"cs": basic_airlink.cslog,
                        "s": basic_airlink.slog,
                        "c": basic_airlink.clog}
        while not cls.stop_logging_thread:
            if not cls.log_queue.empty():
                log_obj = cls.log_queue.get()
                log_function[log_obj["level"]](log_obj["msg"])
            else:
                time.sleep(0.001)

    def mp_log(self, msg, level="cs"):
        # send logging information back to main process to be logged
        # level can be any of "cs", "c", "s" which corresponds to the basic_airlink.cslog, clog, slog
        self.__class__.log_queue.put({"msg": msg, "level": level})

    def run(self): # This method is the entry point in the new process. do not call this directly, call start() to spawn the new process
        # restore class variable so it points to the same queue as the one in the main process
        self.__class__.log_queue = self.temp

        # suppress console output - if we want to print, call self.mp_log()
        #f = open(os.devnull, 'w')
        #sys.stdout = f

#        try:
#            self.login() # log into the router 
#            self.t = threading.Timer(self.timeout, self.timeout_handler) # generate selenium except by closing the driver if timeout
#            self.t.start()
#            result = self.f() # do the task 
#            self.t.cancel() # stop timer
#        except Exception as error:
#            self.mp_log("Cisco Error while performing %s: %s" %(self.task, str(error)), "cs")
#            self.conn.send({"EXCEPTION":True, "RESULT":False})
#            return

        self.login() # log into the router 
        self.t = threading.Timer(self.timeout, self.timeout_handler) # generate selenium except by closing the driver if timeout
        self.t.start()
        result = self.f() # do the task 
        self.t.cancel() # stop timer

        self.conn.send({"EXCEPTION":False, "RESULT":result})

    def timeout_handler(self):
        self.conn.send({"EXCEPTION":True, "RESULT":False, "REASON": "Timed out"})

    def login(self):
        if self.test_config["CISCO_TYPE"] == "IOS":
            self.cisco = cisco_config.CiscoConfig(ip = self.test_config["GATEWAY_ADDRESS"],
                                             port = self.test_config["TELNET_PORT"],
                                             username = self.test_config["TELNET_USER"],
                                             password = self.test_config["TELNET_PASSWORD"],
                                             hostname = self.test_config["TELNET_HOSTNAME"],
                                             enable_password = self.test_config["CISCO_ENABLE_PASSWORD"],
                                             verbose = self.test_config["TELNET_VERBOSE"],
                                             debug_level = self.test_config["TELNET_DEBUG"])
        else: # "ASA"
            logged_in = False
            while not logged_in:
                self.cisco = cisco_asa_config.CiscoAsaConfig(hostname = self.test_config["GATEWAY_ADDRESS"],
                                                             port = self.test_config["SSH_PORT"],
                                                             username = self.test_config["SSH_USER"],
                                                             password = self.test_config["SSH_PASSWORD"],
                                                             router_name = self.test_config["ASA_NAME"],
                                                             enable_password = self.test_config["ASA_ENABLE_PASSWORD"])
                logged_in = self.cisco.connected

    def config_gateway(self):
        if self.test_config["CISCO_TYPE"] == "IOS":
            return self.config_ios_gateway()
        else: # ASA
            return self.config_asa_gateway()

    def config_asa_gateway(self):
        # configure host subnet
        if not self.cisco.config_dhcp_and_host_subnet(network = self.test_config["REMOTE_ADDRESS"], mask_len = self.test_config["REMOTE_ADDRESS_MASK_LENGTH"]):
            self.mp_log("Unsuccessful call to %s" %self.cisco.config_dhcp_and_host_subnet.__name__, 's')
            return False

        if not self.cisco.config_routing_policies(cisco_subnet = self.test_config["REMOTE_ADDRESS"],
                                              cisco_subnet_mask = self.test_config["REMOTE_ADDRESS_MASK"],
                                              airlink_subnet = self.test_config["LOCAL_ADDRESS"], 
                                              airlink_subnet_mask = self.test_config["LOCAL_ADDRESS_MASK"],
                                              negotiation_mode = self.test_config["NEGOTIATION_MODE"]):
            self.mp_log("Unsuccessful call to %s" %self.cisco.config_routing_policies.__name__, 's')
            return False

        if not self.cisco.config_isakmp(encryption = self.test_config["IKE_ENCRYPTION"], 
                                        authentication = self.test_config["IKE_AUTHENTICATION"], 
                                        dh = self.test_config["IKE_DH_GROUP"], 
                                        lifetime = self.test_config["IKE_SA_LIFETIME"]):
            self.mp_log("Unsuccessful call to %s" %self.cisco.config_isakmp.__name__, 's')
            return False

        if not self.cisco.config_ipsec(encryption = self.test_config["IPSEC_ENCRYPTION"], 
                            authentication = self.test_config["IPSEC_AUTHENTICATION"],
                            pfs = self.test_config["PFS"],
                            dh = self.test_config["IPSEC_DH_GROUP"], 
                            lifetime = self.test_config["IPSEC_SA_LIFETIME"]):
            self.mp_log("Unsuccessful call to %s" %self.cisco.config_ipsec.__name__, 's')
            return False

        return True

    def config_ios_gateway(self):
        # configure host subnet
        if not self.cisco.config_dhcp_and_host_subnet(network = self.test_config["REMOTE_ADDRESS"], mask_len = self.test_config["REMOTE_ADDRESS_MASK_LENGTH"]):
            self.mp_log("Unsuccessful call to %s" %self.cisco.config_dhcp_and_host_subnet.__name__, 's')
            return False


        # Configure IKE policy
        if not self.cisco.set_isakmp_policy(priority = "100", 
                                     encryption = self.test_config["IKE_ENCRYPTION"], 
                                     dh = self.test_config["IKE_DH_GROUP"], 
                                     hashing = self.test_config["IKE_AUTHENTICATION"], 
                                     lifetime = self.test_config["IKE_SA_LIFETIME"]):
            self.mp_log("Unsuccessful call to %s" %self.cisco.set_isakmp_policy.__name__, 's')
            return False

        # Configure preshared key
        if not self.cisco.set_isakmp_key(self.test_config["PRESHARED_KEY"]):
            self.mp_log("Unsuccessful call to %s" %self.cisco.set_isakmp_key.__name__, 's')
            return False

        # configure ipsec crypto map
        if not self.cisco.configure_ipsec_crypto_map(esp =  self.test_config["IPSEC_ENCRYPTION"], 
                                                     ah = self.test_config["IPSEC_AUTHENTICATION"], 
                                                     dh = self.test_config["IPSEC_DH_GROUP"], 
                                                     lifetime = self.test_config["IPSEC_SA_LIFETIME"], 
                                                     pfs = self.test_config["PFS"],
                                                     device_subnet = self.test_config["LOCAL_ADDRESS"], 
                                                     device_subnet_wildcards = self.wildcard(self.test_config["LOCAL_ADDRESS_MASK"]), 
                                                     gateway_subnet = self.test_config["REMOTE_ADDRESS"], 
                                                     gateway_subnet_wildcards = self.wildcard(self.test_config["REMOTE_ADDRESS_MASK"])):
            self.mp_log("Unsuccessful call to %s" %self.cisco.configure_ipsec_crypto_map.__name__, 's')
            return False

        # Assign crypto map to interface FastEthernet 0
        if not self.cisco.assign_crypto_map_to_interface(interface="FastEthernet 0"):
            self.mp_log("Unsuccessful call to %s" %self.cisco.assign_crypto_map_to_interface.__name__, 's')
            return False
            
        return True

    def cleanup_gateway(self):
        if self.test_config["CISCO_TYPE"] == "IOS":
            tasks = [self.cisco.remove_all_isakmp_policies,
                     self.cisco.remove_all_isakmp_key,
                     self.cisco.clear_all_crypto_map,
                     self.cisco.clear_all_access_list,
                     self.cisco.clear_all_transform_sets,
                     self.cisco.clear_vpn_session,
                     self.cisco.clear_tunnel_interface,
                     self.cisco.clear_dhcp_and_host_subnet]
        else: # ASA
            tasks = [self.cisco.clear_routing_policies,
                     self.cisco.clear_crypto,
                     self.cisco.clear_dhcp_and_host_subnet]

        for task in tasks:
            if not task():
                self.mp_log("Could not clean up Cisco router. Failed in %s()" %task.__name__)
                return False
        return True

    def verify_gateway(self):
        if self.test_config["CISCO_TYPE"] == "IOS":
            return self.verify_ios_gateway()
        else:
            return self.verify_asa_gateway()

    def verify_asa_gateway(self):
        if not self.cisco.verify_routing_policies(cisco_subnet = self.test_config["REMOTE_ADDRESS"],
                                              cisco_subnet_mask = self.test_config["REMOTE_ADDRESS_MASK"],
                                              airlink_subnet = self.test_config["LOCAL_ADDRESS"], 
                                              airlink_subnet_mask = self.test_config["LOCAL_ADDRESS_MASK"],
                                              negotiation_mode = self.test_config["NEGOTIATION_MODE"]):
            self.mp_log("Unsuccessful call to %s" %self.cisco.verify_routing_policies.__name__, 's')
            print("Unsuccessful call to %s" %self.cisco.verify_routing_policies.__name__, 's')
            return False

        if not self.cisco.verify_isakmp(encryption = self.test_config["IKE_ENCRYPTION"], 
                                        authentication = self.test_config["IKE_AUTHENTICATION"], 
                                        dh = self.test_config["IKE_DH_GROUP"], 
                                        lifetime = self.test_config["IKE_SA_LIFETIME"]):
            self.mp_log("Unsuccessful call to %s" %self.cisco.verify_isakmp.__name__, 's')
            print("Unsuccessful call to %s" %self.cisco.verify_isakmp.__name__, 's')
            return False

        if not self.cisco.verify_ipsec(encryption = self.test_config["IPSEC_ENCRYPTION"], 
                            authentication = self.test_config["IPSEC_AUTHENTICATION"],
                            pfs = self.test_config["PFS"],
                            dh = self.test_config["IPSEC_DH_GROUP"], 
                            lifetime = self.test_config["IPSEC_SA_LIFETIME"]):
            self.mp_log("Unsuccessful call to %s" %self.cisco.verify_ipsec.__name__, 's')
            print("Unsuccessful call to %s" %self.cisco.verify_ipsec.__name__, 's')
            return False

        return True

    def verify_ios_gateway(self):
        # Verify IKE policy
        if not self.cisco.confirm_IKE_policy(priority = "100", 
                                        encryption = self.test_config["IKE_ENCRYPTION"], 
                                        dh = self.test_config["IKE_DH_GROUP"], 
                                        hashing = self.test_config["IKE_AUTHENTICATION"], 
                                        lifetime = self.test_config["IKE_SA_LIFETIME"]):
            return False

        # Verify IKE PSK
        if not self.cisco.verify_isakmp_key(key = self.test_config["PRESHARED_KEY"]):
            return False

        # Verify ipsec crypto map and that it has been assigned to FastEthernet 0
        if not self.cisco.verify_ipsec_crypto_map(esp = self.test_config["IPSEC_ENCRYPTION"], 
                                             ah =  self.test_config["IPSEC_AUTHENTICATION"], 
                                             dh = self.test_config["IPSEC_DH_GROUP"], 
                                             lifetime = self.test_config["IPSEC_SA_LIFETIME"], 
                                             pfs = self.test_config["PFS"], 
                                             interface = "FastEthernet0",
                                             local_address = self.test_config["LOCAL_ADDRESS"], 
                                             local_address_wildcard = self.wildcard(self.test_config["LOCAL_ADDRESS_MASK"]), 
                                             remote_address = self.test_config["REMOTE_ADDRESS"], 
                                             remote_address_wildcard = self.wildcard(self.test_config["REMOTE_ADDRESS_MASK"])):
            return False
        return True

    def check_sa(self):
        return self.cisco.check_crypto_ipsec_sa(self.test_config["AIRLINK_WAN_IP"] if self.test_config["AIRLINK_SIM_STATIC"] == "YES" else None)

#    def get_wan_ip(self): # This function is not very reliable because if window's routing table often ends up using the incorrect interface on the testbed
#        if self.test_config["AIRLINK_SIM_STATIC"] == "YES":
#            return self.test_config["AIRLINK_WAN_IP"]
#        else:
#            wan_ip_sites = ["http://ipecho.net/plain","http://myip.dnsdynamic.com/","http://icanhazip.com/","http://wtfismyip.com/text"]
#            attempts = 10
#            for attempt in range(attempts):
#                for site in wan_ip_sites:
#                    try:
#                        wan_ip = urllib2.urlopen(site).read()
#                    except Exception as exception:
#                        print str(exception)
#                        continue
#    
#                    try:
#                        socket.inet_aton(wan_ip)
#                    except socket.error:
#                        # the site gave us stuff that's not an ipv4 ip address
#                        continue
#
#                    return wan_ip
            
    def wildcard(self, mask):
        ret = ""
        for octet in mask.split("."):
            ret += str(int(octet) ^ 0xFF) + "."
        return ret[:-1]

    def config_and_verify_gre_gateway(self):
        ret = self.cisco.configure_and_verify_tunnel_interface(self.test_config["AIRLINK_WAN_IP"], self.test_config["LOCAL_ADDRESS"], self.test_config["LOCAL_ADDRESS_MASK"])

        ret = ret and self.cisco.config_dhcp_and_host_subnet("172.20.20.0", 24)

        return ret
    def clear_gre_gateway(self):
        return self.cisco.clear_tunnel_interface()

    def check_gre_tunnel(self):
        return self.cisco.check_tunnel(self.test_config["AIRLINK_WAN_IP"])

    def watch_error_message(self):
        return self.cisco.watch_error_message(self.test_config["CISCO_WAIT_MESSAGE"], self.test_config["CISCO_WAIT_MESSAGE_TIMEOUT"])

    def dummy(self):
        return self.cisco.watch_error_message(self.test_config["CISCO_WAIT_MESSAGE"], self.test_config["CISCO_WAIT_MESSAGE_TIMEOUT"])

