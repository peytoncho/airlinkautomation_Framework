When setting up IPsec VPN test cases, make sure the following
fields in common_testbed_conf.yml are set according to the
testbed set up.

VPN:
    AIRLINK_WAN_IP:       "0.0.0.0"
    AIRLINK_SIM_STATIC:   "NO" # "YES" or "NO"
       
    CISCO_SUBNET:         "10.11.12.0"
    CISCO_SUBNET_MASK:    "255.255.255.0"
    CISCO_HOST:           "10.11.12.13"    
        
    AIRLINK_SUBNET:       "192.168.0.0"
    AIRLINK_SUBNET_MASK:  "255.255.0.0"
    AIRLINK_HOST:         "192.168.13.100"


MANAGEMENT_IP: 
    CONTROLLER : 192.168.14.100
    HOST1      : 192.168.13.100
    HOST2      : 10.11.12.13

PUBLIC_IP: 
    VPN_CISCO_ROUTER : 208.81.123.54
