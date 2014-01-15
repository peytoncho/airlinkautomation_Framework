################################################################################
#
# This module has common methods for SNMP test automation. It uses SNMP tool 
# from snmpsoft.com.
# Company: Sierra Wireless
# Time: Feb 19, 2013
# Author: Airlink
# 
################################################################################
from msciids import *
import os
import sys
import datetime
import time
from types import *

test_area = "Services"
test_sub_area="SNMP"
airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME'] 
sys.path.append(airlinkautomation_home_dirname+"/lib/common")

import basic_airlink
basic_airlink.append_sys_path()
tbd_config_map, snmp_config_map = basic_airlink.get_config_data(test_area,test_sub_area)

OIDSTRING = 'STRING'
OIDINTEGER ='INTEGER'
OIDIPADDRESS = 'IPADDRESS'

snmp_oid_map = [
                
    [".1.3.6.1.4.1.20542.9.1.1.1.4.0", OIDSTRING, "aleosSWVer",   0,  MSCIID_INF_ALEOS_SW_VER],
    [".1.3.6.1.4.1.20542.9.1.1.1.17.0", OIDSTRING, "phoneMumber",   0,  MSCIID_INF_PHONE_NUM],
    [".1.3.6.1.4.1.20542.9.1.1.1.259.0", OIDSTRING, "networkState",   0,  MSCIID_STS_NETWORK_STATE],
    [".1.3.6.1.4.1.20542.9.1.1.1.260.0", OIDINTEGER, "netChannel",   0,  MSCIID_STS_NETWORK_CHANNEL],
    [".1.3.6.1.4.1.20542.9.1.1.1.261.0", OIDINTEGER, "RSSI",   0,  MSCIID_STS_NETWORK_RSSI],
    [".1.3.6.1.4.1.20542.9.1.1.1.264.0", OIDSTRING, "networkServiceType",   0,  MSCIID_STS_NETWORK_SERVICE],
    [".1.3.6.1.4.1.20542.9.1.1.1.266.0", OIDSTRING, "powerIn",   0,  MSCIID_STS_POWERIN],
    [".1.3.6.1.4.1.20542.9.1.1.1.267.0", OIDINTEGER, "boardTemp",   0,  MSCIID_STS_BOARDTEMP],
    [".1.3.6.1.4.1.20542.9.1.1.1.283.0", OIDINTEGER, "cellularBytesSent",   0,  MSCIID_STS_MODEM_SENT],
    [".1.3.6.1.4.1.20542.9.1.1.1.284.0", OIDINTEGER, "cellularBytesRecvd",   0,  MSCIID_STS_MODEM_RECV],
    [".1.3.6.1.4.1.20542.9.1.1.1.301.0", OIDIPADDRESS, "ipAddress",   0,  MSCIID_STS_NETWORK_IP],
    [".1.3.6.1.4.1.20542.9.1.1.1.643.0", OIDSTRING, "CDMAECIO",   0,  MSCIID_STS_CDMA_ECIO],
    [".1.3.6.1.4.1.20542.9.1.1.1.644.0", OIDSTRING, "CDMAOperator",   0,  MSCIID_STS_CDMA_OPERATOR],
    [".1.3.6.1.4.1.20542.9.1.1.1.770.0", OIDSTRING, "gprsnetworkOperator",   0,  MSCIID_STS_GPRS_OPERATOR],
    [".1.3.6.1.4.1.20542.9.1.1.1.772.0", OIDSTRING, "gprsECIO",   0,  MSCIID_STS_GPRS_ECIO],
    [".1.3.6.1.4.1.20542.9.1.1.1.1154.0", OIDSTRING, "deviceName",   0,  MSCIID_CFG_CMN_MDM_NAME],

    #cellular
    [".1.3.6.1.4.1.20542.9.1.1.2.10.0", OIDSTRING, "electronicID",   0,  MSCIID_INF_MODEM_ID],
    [".1.3.6.1.4.1.20542.9.1.1.2.263.0", OIDINTEGER, "errorRate",   0,  MSCIID_STS_NETWORK_ER],
    [".1.3.6.1.4.1.20542.9.1.1.2.281.0", OIDINTEGER, "packetsSent",   0,  MSCIID_STS_MODEM_IP_SENT],
    [".1.3.6.1.4.1.20542.9.1.1.2.282.0", OIDINTEGER, "packetsRecvd",   0,  MSCIID_STS_MODEM_IP_RECV],
    [".1.3.6.1.4.1.20542.9.1.1.2.283.0", OIDINTEGER, "bytesSent",   0,  MSCIID_STS_MODEM_SENT],
    [".1.3.6.1.4.1.20542.9.1.1.2.284.0", OIDINTEGER, "bytesRecvd",   0,  MSCIID_STS_MODEM_RECV],
    [".1.3.6.1.4.1.20542.9.1.1.2.301.0", OIDIPADDRESS, "wanIP",   0,  MSCIID_STS_NETWORK_IP],
    [".1.3.6.1.4.1.20542.9.1.1.2.642.0", OIDINTEGER, "prlVersion",   0,  MSCIID_STS_CDMA_PRL_VERSION],
    [".1.3.6.1.4.1.20542.9.1.1.2.646.0", OIDSTRING, "prlUpdateStatus",   0,  MSCIID_STS_CDMA_PRL_UPD_STS],
    [".1.3.6.1.4.1.20542.9.1.1.2.648.0", OIDINTEGER, "SID",   0,  MSCIID_STS_CDMA_SID],
    [".1.3.6.1.4.1.20542.9.1.1.2.649.0", OIDINTEGER, "NID",   0,  MSCIID_STS_CDMA_NID],
    [".1.3.6.1.4.1.20542.9.1.1.2.650.0", OIDSTRING, "pnOffset",   0,  MSCIID_STS_CDMA_PN_OFFSET],
    [".1.3.6.1.4.1.20542.9.1.1.2.651.0", OIDSTRING, "baseClass",   0,  MSCIID_STS_CDMA_LTE_BASE_CLASS],
    [".1.3.6.1.4.1.20542.9.1.1.2.771.0", OIDSTRING, "iccid",   0,  MSCIID_STS_GPRS_SIMID],
    [".1.3.6.1.4.1.20542.9.1.1.2.773.0", OIDSTRING, "cellid",   0,  MSCIID_STS_GPRS_LTE_CELL_ID],
    [".1.3.6.1.4.1.20542.9.1.1.2.774.0", OIDSTRING, "lac",   0,  MSCIID_STS_GPRS_LTE_LAC],
    [".1.3.6.1.4.1.20542.9.1.1.2.785.0", OIDSTRING, "imsi",   0,  MSCIID_STS_GPRS_IMSI],
    [".1.3.6.1.4.1.20542.9.1.1.2.1082.0", OIDSTRING, "dnsServer1",   0,  MSCIID_CFG_CMN_MDM_DNS_IP1],
    [".1.3.6.1.4.1.20542.9.1.1.2.1083.0", OIDSTRING, "dnsServer2",   0,  MSCIID_CFG_CMN_MDM_DNS_IP2],
    [".1.3.6.1.4.1.20542.9.1.1.2.1104.0", OIDINTEGER, "keepAlivePingTime",   0, MSCIID_CFG_CMN_IPPING_PERIOD],
    [".1.3.6.1.4.1.20542.9.1.1.2.1105.0", OIDIPADDRESS, "keepAliveIPAddress",   0,  MSCIID_CFG_CMN_IPPING_ADDR],
    [".1.3.6.1.4.1.20542.9.1.1.2.2056.0", OIDSTRING, "cellBand",   0,  MSCIID_CFG_GPRS_RADIO_BAND],
    [".1.3.6.1.4.1.20542.9.1.1.2.11202.0", OIDSTRING, "apn",   0,  MSCIID_STS_CMN_APN_CURRENT],
    [".1.3.6.1.4.1.20542.9.1.1.2.5046.0", OIDINTEGER, "wanUseTime",   0,  STS_TIME_IN_USE],
    [".1.3.6.1.4.1.20542.9.1.1.2.10249.0", OIDSTRING, "rscp",   0,  MSCIID_STS_GPRS_RSCP],

    #lan
    [".1.3.6.1.4.1.20542.9.1.1.3.279.0", OIDINTEGER, "lanpacketSent",   0,  MSCIID_STS_HOST_IP_SENT],
    [".1.3.6.1.4.1.20542.9.1.1.3.280.0", OIDINTEGER, "lanpacketRecvd",   0,  MSCIID_STS_HOST_IP_RECV],
    [".1.3.6.1.4.1.20542.9.1.1.3.1130.0", OIDSTRING, "usbMode",   0, MSCIID_CFG_CMN_USB_DEVICE],
    [".1.3.6.1.4.1.20542.9.1.1.3.4506.0", OIDSTRING, "wifiAPStatus",   0, MSCIID_WIFI_ENABLE],
    [".1.3.6.1.4.1.20542.9.1.1.3.4507.0", OIDSTRING, "wifiSSID",   0, MSCIID_WIFI_SSID],
    [".1.3.6.1.4.1.20542.9.1.1.3.4508.0", OIDINTEGER, "wifiChannel",   0,  MSCIID_WIFI_CHANNEL],
    [".1.3.6.1.4.1.20542.9.1.1.3.4509.0", OIDSTRING, "wifiSecurityType",   0, MSCIID_WIFI_SECURITY_TYPE],
    [".1.3.6.1.4.1.20542.9.1.1.3.9001.0", OIDSTRING, "vrrpEnabled",   0, MSCIID_VRRP_ENABLED],
    [".1.3.6.1.4.1.20542.9.1.1.3.10401.0", OIDSTRING, "wifiBridgeEnabled",   0, MSCIID_CFG_WIFI_BRIDGE_EN],
    [".1.3.6.1.4.1.20542.9.1.1.3.10405.0", OIDINTEGER, "wifipacketSent",   0,  MSCIID_STS_WIFI_TX_PKT_COUNT],
    [".1.3.6.1.4.1.20542.9.1.1.3.10406.0", OIDINTEGER, "wifipacketRecvd",   0,  MSCIID_STS_WIFI_RX_PKT_COUNT],

    # vpn
    [".1.3.6.1.4.1.20542.9.1.1.4.3176.0", OIDSTRING, "vpn1Status",   0, MSCIID_STS_IPSEC_STATE],
    [".1.3.6.1.4.1.20542.9.1.1.4.3177.0", OIDSTRING, "incomingOOB",   0, MSCIID_CFG_IPSEC_INBOUND],
    [".1.3.6.1.4.1.20542.9.1.1.4.3178.0", OIDSTRING, "outgoingOOB",   0, MSCIID_CFG_IPSEC_OB_ALEOS],
    [".1.3.6.1.4.1.20542.9.1.1.4.3179.0", OIDSTRING, "outgoingHostOOB",   0, MSCIID_CFG_IPSEC_OB_HOST],
    [".1.3.6.1.4.1.20542.9.1.1.4.3205.0", OIDSTRING, "vpn2Status",   0, MSCIID_STS_IPSEC2_STATE],
    [".1.3.6.1.4.1.20542.9.1.1.4.3231.0", OIDSTRING, "vpn3Status",   0, MSCIID_STS_IPSEC3_STATE],
    [".1.3.6.1.4.1.20542.9.1.1.4.3257.0", OIDSTRING, "vpn4Status",   0, MSCIID_STS_IPSEC4_STATE],
    [".1.3.6.1.4.1.20542.9.1.1.4.3283.0", OIDSTRING, "vpn5Status",   0, MSCIID_STS_IPSEC5_STATE],

    #security
     #DEPRECATED   [".1.3.6.1.4.1.20542.9.1.1.5.385.0", OIDINTEGER, "badPasswdCount",   0,  MSCIID_STS_BAD_PW_CNT],
    [".1.3.6.1.4.1.20542.9.1.1.5.386.0", OIDINTEGER, "ipRejectCount",   0,  MSCIID_STS_IP_REJECT_CNT],
    #DEPRECATED     [".1.3.6.1.4.1.20542.9.1.1.5.387.0", OIDSTRING, "ipRejectLog",   0, MSCIID_STS_IP_REJECT_LIST],
    [".1.3.6.1.4.1.20542.9.1.1.5.1062.0", OIDSTRING, "trustedHosts",   0, MSCIID_CFG_CMN_FRIEND_MODE],
    [".1.3.6.1.4.1.20542.9.1.1.5.3505.0", OIDSTRING, "portFilteringIn",   0, MSCIID_FW_PORTS_WOB],
    [".1.3.6.1.4.1.20542.9.1.1.5.3506.0", OIDSTRING, "portFilteringOut",   0, MSCIID_FW_O_PORTS_WOB],
    [".1.3.6.1.4.1.20542.9.1.1.5.3509.0", OIDSTRING, "macFiltering",   0, MSCIID_NET_MAC_FILTER_ENABLE],
    [".1.3.6.1.4.1.20542.9.1.1.5.5112.0", OIDSTRING, "portForwarding",   0, PF_ENABLED],
    [".1.3.6.1.4.1.20542.9.1.1.5.5113.0", OIDSTRING, "dmz",   0, DMZ_ENABLED],

    # services
    [".1.3.6.1.4.1.20542.9.1.1.6.1149.0", OIDSTRING, "aceManager",   0, MSCIID_CFG_CMN_ACEWEB_ACCESS],
    [".1.3.6.1.4.1.20542.9.1.1.6.5007.0", OIDSTRING, "fullDomainName",   0, DDNS_FQDN],
    [".1.3.6.1.4.1.20542.9.1.1.6.5011.0", OIDSTRING, "dynamicDnsService",   0, DDNS_SERVICE],
    [".1.3.6.1.4.1.20542.9.1.1.6.5026.0", OIDSTRING, "aceNet",   0, FC_STATUS],

    # gps
    [".1.3.6.1.4.1.20542.9.1.1.7.900.0", OIDINTEGER, "gpsFix",   0, MSCIID_STS_PP_GPS_QUAL],
    [".1.3.6.1.4.1.20542.9.1.1.7.901.0", OIDINTEGER, "satelliteCount",   0, MSCIID_STS_PP_GPS_SAT_CNT],
    [".1.3.6.1.4.1.20542.9.1.1.7.902.0", OIDSTRING, "lattitude",   0, MSCIID_STS_PP_GPS_LAT],
    [".1.3.6.1.4.1.20542.9.1.1.7.903.0", OIDSTRING, "longitude",   0, MSCIID_STS_PP_GPS_LONG],
    [".1.3.6.1.4.1.20542.9.1.1.7.904.0", OIDSTRING, "heading",   0, MSCIID_STS_PP_GPS_HEADING],
    [".1.3.6.1.4.1.20542.9.1.1.7.905.0", OIDINTEGER, "speed",   0, MSCIID_STS_PP_GPS_SPEED],
    [".1.3.6.1.4.1.20542.9.1.1.7.906.0", OIDINTEGER, "engineHours",   0, MSCIID_STS_PP_ENGINE_HRS],

    # serial
    [".1.3.6.1.4.1.20542.9.1.1.8.273.0", OIDINTEGER, "serialPacketSent",   0, MSCIID_STS_HOST_SENT],
    [".1.3.6.1.4.1.20542.9.1.1.8.274.0", OIDINTEGER, "serialPacketRecvd",   0, MSCIID_STS_HOST_RECV],
    [".1.3.6.1.4.1.20542.9.1.1.8.1043.0", OIDSTRING, "serialPortMode",   0, MSCIID_CFG_CMN_DEFAULT_MODE],
    [".1.3.6.1.4.1.20542.9.1.1.8.1048.0", OIDSTRING, "tcpAutoAnswer",   0, MSCIID_CFG_CMN_TCP_AUTO_ANS],
    [".1.3.6.1.4.1.20542.9.1.1.8.1054.0", OIDSTRING, "udpAutoAnswer",   0, MSCIID_CFG_CMN_UDP_AUTO_ANS],

    # about
    [".1.3.6.1.4.1.20542.9.1.1.9.3.0", OIDSTRING, "msciVersion",   0, MSCIID_INF_VERSION],
    [".1.3.6.1.4.1.20542.9.1.1.9.4.0", OIDSTRING, "aleosSWVersion",   0, MSCIID_INF_ALEOS_SW_VER],
    [".1.3.6.1.4.1.20542.9.1.1.9.5.0", OIDSTRING, "deviceHWConfiguration",   0, MSCIID_INF_ALEOS_HW_VER],
    [".1.3.6.1.4.1.20542.9.1.1.9.7.0", OIDSTRING, "deviceModel",   0, MSCIID_INF_PRODUCT_STR],
    [".1.3.6.1.4.1.20542.9.1.1.9.8.0", OIDSTRING, "radioFirmwareVersion",   0, MSCIID_INF_MODEM_SW_VER],
    [".1.3.6.1.4.1.20542.9.1.1.9.9.0", OIDSTRING, "radioModelType",   0, MSCIID_INF_MODEM_HW_VER],
    [".1.3.6.1.4.1.20542.9.1.1.9.25.0", OIDSTRING, "deviceID",   0, MSCIID_INF_DEVICE_ID],
    [".1.3.6.1.4.1.20542.9.1.1.9.66.0", OIDSTRING, "macAddress",   0, MSCIID_INF_MAC_ADDR],

    # digital/analog inputs/outputs
    [".1.3.6.1.4.1.20542.9.1.10.1.851.0", OIDINTEGER, "digitalInput1",   0, MSCIID_STS_IO_DIGITAL_IN1],
    [".1.3.6.1.4.1.20542.9.1.10.1.852.0", OIDINTEGER, "digitalInput2",   0, MSCIID_STS_IO_DIGITAL_IN2],
    [".1.3.6.1.4.1.20542.9.1.10.1.853.0", OIDINTEGER, "digitalInput3",   0, MSCIID_STS_IO_DIGITAL_IN3],
    [".1.3.6.1.4.1.20542.9.1.10.1.854.0", OIDINTEGER, "digitalInput4",   0, MSCIID_STS_IO_DIGITAL_IN4],
    [".1.3.6.1.4.1.20542.9.1.10.1.855.0", OIDINTEGER, "analogInput1",   0, MSCIID_STS_IO_ANALOG_IN1],
    [".1.3.6.1.4.1.20542.9.1.10.1.856.0", OIDINTEGER, "analogInput2",   0, MSCIID_STS_IO_ANALOG_IN2],
    [".1.3.6.1.4.1.20542.9.1.10.1.857.0", OIDINTEGER, "analogInput3",   0, MSCIID_STS_IO_ANALOG_IN3],
    [".1.3.6.1.4.1.20542.9.1.10.1.858.0", OIDINTEGER, "analogInput4",   0, MSCIID_STS_IO_ANALOG_IN4],
    [".1.3.6.1.4.1.20542.9.1.10.1.859.0", OIDINTEGER, "digitalOutput1",  0, MSCIID_STS_IO_DIGITAL_OUT1],
    [".1.3.6.1.4.1.20542.9.1.10.1.860.0", OIDINTEGER, "digitalOutput2",  0, MSCIID_STS_IO_DIGITAL_OUT2],
    [".1.3.6.1.4.1.20542.9.1.10.2.861.0", OIDINTEGER, "digitalConfig1",  0, MSCIID_STS_IO_DIGITAL_CFG1],
    [".1.3.6.1.4.1.20542.9.1.10.2.862.0", OIDINTEGER, "digitalConfig2",  0, MSCIID_STS_IO_DIGITAL_CFG2],
    [".1.3.6.1.4.1.20542.9.1.10.1.863.0", OIDINTEGER, "digitalOutput3",  0, MSCIID_STS_IO_DIGITAL_OUT3],
    [".1.3.6.1.4.1.20542.9.1.10.1.864.0", OIDINTEGER, "digitalOutput4",  0, MSCIID_STS_IO_DIGITAL_OUT4],
    [".1.3.6.1.4.1.20542.9.1.10.1.865.0", OIDINTEGER, "digitalOutput5",  0, MSCIID_STS_IO_DIGITAL_OUT5],
    [".1.3.6.1.4.1.20542.9.1.10.1.866.0", OIDINTEGER, "digitalOutput6",  0, MSCIID_STS_IO_DIGITAL_OUT6],
    [".1.3.6.1.4.1.20542.9.1.10.1.867.0", OIDINTEGER, "digitalInput5",   0, MSCIID_STS_IO_DIGITAL_IN5],
    [".1.3.6.1.4.1.20542.9.1.10.1.868.0", OIDINTEGER, "digitalInput6",   0, MSCIID_STS_IO_DIGITAL_IN6],
    [".1.3.6.1.4.1.20542.9.1.10.2.869.0", OIDINTEGER, "digitalConfig3",  0, MSCIID_STS_IO_DIGITAL_CFG3],
    [".1.3.6.1.4.1.20542.9.1.10.2.870.0", OIDINTEGER, "digitalConfig4",  0, MSCIID_STS_IO_DIGITAL_CFG4],
    [".1.3.6.1.4.1.20542.9.1.10.2.871.0", OIDINTEGER, "digitalConfig5",  0, MSCIID_STS_IO_DIGITAL_CFG5],
    [".1.3.6.1.4.1.20542.9.1.10.2.872.0", OIDINTEGER, "digitalConfig6",  0, MSCIID_STS_IO_DIGITAL_CFG6],
    [".1.3.6.1.4.1.20542.9.1.10.1.873.0", OIDINTEGER, "analogInput5",   0, MSCIID_STS_IO_ANALOG_IN5],
    [".1.3.6.1.4.1.20542.9.1.10.1.874.0", OIDINTEGER, "analogInput6",   0, MSCIID_STS_IO_ANALOG_IN6],
    [".1.3.6.1.4.1.20542.9.1.10.1.875.0", OIDINTEGER, "analogInput7",   0, MSCIID_STS_IO_ANALOG_IN7],
    [".1.3.6.1.4.1.20542.9.1.10.1.876.0", OIDINTEGER, "analogInput8",   0, MSCIID_STS_IO_ANALOG_IN8],
    [".1.3.6.1.4.1.20542.9.1.10.1.4002.0", OIDINTEGER, "pulseAccumulator1",   0, MSCIID_PULSE_CNT_01],
    [".1.3.6.1.4.1.20542.9.1.10.1.4003.0", OIDINTEGER, "pulseAccumulator2",   0, MSCIID_PULSE_CNT_01 + 1],
    [".1.3.6.1.4.1.20542.9.1.10.1.4004.0", OIDINTEGER, "pulseAccumulator3",   0, MSCIID_PULSE_CNT_01 + 2],
    [".1.3.6.1.4.1.20542.9.1.10.1.4005.0", OIDINTEGER, "pulseAccumulator4",   0, MSCIID_PULSE_CNT_01 + 3],
    [".1.3.6.1.4.1.20542.9.1.10.1.4006.0", OIDINTEGER, "pulseAccumulator5",   0, MSCIID_PULSE_CNT_01 + 4],
    [".1.3.6.1.4.1.20542.9.1.10.1.4007.0", OIDINTEGER, "pulseAccumulator6",   0, MSCIID_PULSE_CNT_01 + 5],
    [".1.3.6.1.4.1.20542.9.1.10.1.4011.0", OIDINTEGER, "coefficientAnalogInput1",   0, MSCIID_IO_A_COEF_01],
    [".1.3.6.1.4.1.20542.9.1.10.1.4012.0", OIDINTEGER, "coefficientAnalogInput2",   0, MSCIID_IO_A_COEF_01 + 1],
    [".1.3.6.1.4.1.20542.9.1.10.1.4013.0", OIDINTEGER, "coefficientAnalogInput3",   0, MSCIID_IO_A_COEF_01 + 2],
    [".1.3.6.1.4.1.20542.9.1.10.1.4014.0", OIDINTEGER, "coefficientAnalogInput4",   0, MSCIID_IO_A_COEF_01 + 3],
    [".1.3.6.1.4.1.20542.9.1.10.1.4015.0", OIDINTEGER, "coefficientAnalogInput5",   0, MSCIID_IO_A_COEF_01 + 4],
    [".1.3.6.1.4.1.20542.9.1.10.1.4016.0", OIDINTEGER, "coefficientAnalogInput6",   0, MSCIID_IO_A_COEF_01 + 5],
    [".1.3.6.1.4.1.20542.9.1.10.1.4017.0", OIDINTEGER, "coefficientAnalogInput7",   0, MSCIID_IO_A_COEF_01 + 6],
    [".1.3.6.1.4.1.20542.9.1.10.1.4018.0", OIDINTEGER, "coefficientAnalogInput8",   0, MSCIID_IO_A_COEF_01 + 7],
    [".1.3.6.1.4.1.20542.9.1.10.1.4021.0", OIDINTEGER, "offsetAnalogInput1",   0, MSCIID_IO_A_OFFSET_01],
    [".1.3.6.1.4.1.20542.9.1.10.1.4022.0", OIDINTEGER, "offsetAnalogInput2",   0, MSCIID_IO_A_OFFSET_01 + 1],
    [".1.3.6.1.4.1.20542.9.1.10.1.4023.0", OIDINTEGER, "offsetAnalogInput3",   0, MSCIID_IO_A_OFFSET_01 + 2],
    [".1.3.6.1.4.1.20542.9.1.10.1.4024.0", OIDINTEGER, "offsetAnalogInput4",   0, MSCIID_IO_A_OFFSET_01 + 3],
    [".1.3.6.1.4.1.20542.9.1.10.1.4025.0", OIDINTEGER, "offsetAnalogInput5",   0, MSCIID_IO_A_OFFSET_01 + 4],
    [".1.3.6.1.4.1.20542.9.1.10.1.4026.0", OIDINTEGER, "offsetAnalogInput6",   0, MSCIID_IO_A_OFFSET_01 + 5],
    [".1.3.6.1.4.1.20542.9.1.10.1.4027.0", OIDINTEGER, "offsetAnalogInput7",   0, MSCIID_IO_A_OFFSET_01 + 6],
    [".1.3.6.1.4.1.20542.9.1.10.1.4028.0", OIDINTEGER, "offsetAnalogInput8",   0, MSCIID_IO_A_OFFSET_01 + 7],
    [".1.3.6.1.4.1.20542.9.1.10.1.4031.0", OIDINTEGER, "unitsAnalogInput1",   0, MSCIID_IO_A_UNITS_01],
    [".1.3.6.1.4.1.20542.9.1.10.1.4032.0", OIDINTEGER, "unitsAnalogInput2",   0, MSCIID_IO_A_UNITS_01 + 1],
    [".1.3.6.1.4.1.20542.9.1.10.1.4033.0", OIDINTEGER, "unitsAnalogInput3",   0, MSCIID_IO_A_UNITS_01 + 2],
    [".1.3.6.1.4.1.20542.9.1.10.1.4034.0", OIDINTEGER, "unitsAnalogInput4",   0, MSCIID_IO_A_UNITS_01 + 3],
    [".1.3.6.1.4.1.20542.9.1.10.1.4035.0", OIDINTEGER, "unitsAnalogInput5",   0, MSCIID_IO_A_UNITS_01 + 4],
    [".1.3.6.1.4.1.20542.9.1.10.1.4036.0", OIDINTEGER, "unitsAnalogInput6",   0, MSCIID_IO_A_UNITS_01 + 5],
    [".1.3.6.1.4.1.20542.9.1.10.1.4037.0", OIDINTEGER, "unitsAnalogInput7",   0, MSCIID_IO_A_UNITS_01 + 6],
    [".1.3.6.1.4.1.20542.9.1.10.1.4038.0", OIDINTEGER, "unitsAnalogInput8",   0, MSCIID_IO_A_UNITS_01 + 7],
    [".1.3.6.1.4.1.20542.9.1.10.1.4041.0", OIDINTEGER, "scaledAnalogInput1",  0, MSCIID_SCALED_ANALOG_01],
    [".1.3.6.1.4.1.20542.9.1.10.1.4042.0", OIDINTEGER, "scaledAnalogInput2",  0, MSCIID_SCALED_ANALOG_01 + 1],
    [".1.3.6.1.4.1.20542.9.1.10.1.4043.0", OIDINTEGER, "scaledAnalogInput3",  0, MSCIID_SCALED_ANALOG_01 + 2],
    [".1.3.6.1.4.1.20542.9.1.10.1.4044.0", OIDINTEGER, "scaledAnalogInput4",  0, MSCIID_SCALED_ANALOG_01 + 3],
    [".1.3.6.1.4.1.20542.9.1.10.1.4045.0", OIDINTEGER, "scaledAnalogInput5",  0, MSCIID_SCALED_ANALOG_01 + 4],
    [".1.3.6.1.4.1.20542.9.1.10.1.4046.0", OIDINTEGER, "scaledAnalogInput6",  0, MSCIID_SCALED_ANALOG_01 + 5],
    [".1.3.6.1.4.1.20542.9.1.10.1.4047.0", OIDINTEGER, "scaledAnalogInput7",  0, MSCIID_SCALED_ANALOG_01 + 6],
    [".1.3.6.1.4.1.20542.9.1.10.1.4048.0", OIDINTEGER, "scaledAnalogInput8",  0, MSCIID_SCALED_ANALOG_01 + 7],

    # snmpconfig
    [".1.3.6.1.4.1.20542.9.1.12.1166.0", OIDIPADDRESS, "trapipAddress",   1, MSCIID_CFG_CMN_SNMP_TRAPDEST],
    [".1.3.6.1.4.1.20542.9.1.12.2730.0", OIDSTRING, "snmpContact",   1, MSCIID_CFG_SNMP_CONTACT],
    [".1.3.6.1.4.1.20542.9.1.12.2731.0", OIDSTRING, "snmpName",   1, MSCIID_CFG_SNMP_NAME],
    [".1.3.6.1.4.1.20542.9.1.12.2732.0", OIDSTRING, "snmpLocation",   1, MSCIID_CFG_SNMP_LOCATION],
    [".1.3.6.1.4.1.20542.9.1.12.10040.0", OIDINTEGER, "snmpEnable",   1, MSCIID_CFG_SNMP_ENABLE],
    [".1.3.6.1.4.1.20542.9.1.12.10041.0", OIDINTEGER, "snmpVersion",   1, MSCIID_CFG_SNMP_VERSION ],
    [".1.3.6.1.4.1.20542.9.1.12.10042.0", OIDINTEGER, "snmpport",   1, MSCIID_CFG_SNMP_PORT],
    [".1.3.6.1.4.1.20542.9.1.12.10043.0", OIDINTEGER, "trapport",   1, MSCIID_CFG_SNMP_TRAPPORT ],
    [".1.3.6.1.4.1.20542.9.1.12.10044.0", OIDSTRING, "engineid",   1, MSCIID_CFG_SNMP_ENGINEID],
    [".1.3.6.1.4.1.20542.9.1.12.10045.0", OIDSTRING, "rouser",   1, MSCIID_CFG_SNMP_ROUSER],
    [".1.3.6.1.4.1.20542.9.1.12.10046.0", OIDINTEGER, "rosecuritylvl",   1, MSCIID_CFG_SNMP_ROUSER_SECLVL],
    [".1.3.6.1.4.1.20542.9.1.12.10047.0", OIDINTEGER, "roauthtype",   1, MSCIID_CFG_SNMP_ROUSER_AUTHTYPE],
    [".1.3.6.1.4.1.20542.9.1.12.10048.0", OIDSTRING, "roauthkey",   1, MSCIID_CFG_SNMP_ROUSER_AUTHKEY],
    [".1.3.6.1.4.1.20542.9.1.12.10049.0", OIDINTEGER, "roprivtype",   1, MSCIID_CFG_SNMP_ROUSER_PRIVTYPE],
    [".1.3.6.1.4.1.20542.9.1.12.10050.0", OIDSTRING, "roprivkey",   1, MSCIID_CFG_SNMP_ROUSER_PRIVKEY],
    [".1.3.6.1.4.1.20542.9.1.12.10051.0", OIDSTRING, "rwuser",   1, MSCIID_CFG_SNMP_RWUSER],
    [".1.3.6.1.4.1.20542.9.1.12.10052.0", OIDINTEGER, "rwsecuritylvl",   1, MSCIID_CFG_SNMP_RWUSER_SECLVL],
    [".1.3.6.1.4.1.20542.9.1.12.10053.0", OIDINTEGER, "rwauthtype",   1, MSCIID_CFG_SNMP_RWUSER_AUTHTYPE],
    [".1.3.6.1.4.1.20542.9.1.12.10054.0", OIDSTRING, "rwauthkey",   1, MSCIID_CFG_SNMP_RWUSER_AUTHKEY],
    [".1.3.6.1.4.1.20542.9.1.12.10055.0", OIDINTEGER, "rwprivtype",   1, MSCIID_CFG_SNMP_RWUSER_PRIVTYPE],
    [".1.3.6.1.4.1.20542.9.1.12.10056.0", OIDSTRING, "rwprivkey",   1, MSCIID_CFG_SNMP_RWUSER_PRIVKEY],
    [".1.3.6.1.4.1.20542.9.1.12.10057.0", OIDSTRING, "trapuser",   1, MSCIID_CFG_SNMP_TRAP_USER],
    [".1.3.6.1.4.1.20542.9.1.12.10058.0", OIDINTEGER, "trapsecuritylvl",   1, MSCIID_CFG_SNMP_TRAP_SECLVL],
    [".1.3.6.1.4.1.20542.9.1.12.10059.0", OIDINTEGER, "trapauthtype",   1, MSCIID_CFG_SNMP_TRAP_AUTHTYPE],
    [".1.3.6.1.4.1.20542.9.1.12.10060.0", OIDSTRING, "trapauthkey",   1, MSCIID_CFG_SNMP_TRAP_AUTHKEY],
    [".1.3.6.1.4.1.20542.9.1.12.10061.0", OIDINTEGER, "trapprivtype",   1, MSCIID_CFG_SNMP_TRAP_PRIVTYPE],
    [".1.3.6.1.4.1.20542.9.1.12.10062.0", OIDSTRING, "trapprivkey",   1, MSCIID_CFG_SNMP_TRAP_PRIVKEY],
    [".1.3.6.1.4.1.20542.9.1.12.10063.0", OIDSTRING, "rocommunity",   1, MSCIID_CFG_SNMP_ROCOMMUNITY],
    [".1.3.6.1.4.1.20542.9.1.12.10064.0", OIDSTRING, "rwcommunity",   1, MSCIID_CFG_SNMP_RWCOMMUNITY],
    [".1.3.6.1.4.1.20542.9.1.12.10065.0", OIDSTRING, "trapcommunity",   1,MSCIID_CFG_SNMP_TRAP_COMMUNITY],
    
    #reset modem
    [".1.3.6.1.4.1.20542.9.1.12.65001.0", OIDINTEGER, "rebootmodem",   1, MSCIID_RESET_MODEM],
]

class SnmpAirlink(object): 

    def __init__(self):
        ''' Inits date, time. 
        Precondition: The SNMP shall have been enabled before start this class.
        Args: None
        Returns: None
        '''
        current_date_time = datetime.datetime.now()

        basic_airlink.cslog(str(current_date_time))
        
        self.error_flag = 0
        
        self.init_snmp_config()

    def init_snmp_config(self):
        ''' Inits SNMP Read/Write variables.
        ''' 
        
        self.snmp_enable = snmp_config_map["SNMP_CONFIG"]["SNMP_ENABLE"]
        self.snmp_ver    = snmp_config_map["SNMP_CONFIG"]["SNMP_VERSION"]
        self.snmp_port   = snmp_config_map["SNMP_CONFIG"]["SNMP_PORT"]
        self.trap_addr   = snmp_config_map["SNMP_CONFIG"]["SNMP_TRAPDEST"]
        self.trap_port   = snmp_config_map["SNMP_CONFIG"]["SNMP_TRAPPORT"]
        self.ro_community=snmp_config_map["SNMP_CONFIG"]["SNMP_ROCOMMUNITY"]
        self.rw_community=snmp_config_map["SNMP_CONFIG"]["SNMP_RWCOMMUNITY"]
        self.trap_community=snmp_config_map["SNMP_CONFIG"]["SNMP_TRAP_COMMUNITY"]
        self.ro_username        =snmp_config_map["SNMP_CONFIG"]["SNMP_ROUSER"]
        self.ro_security_level  =snmp_config_map["SNMP_CONFIG"]["SNMP_ROUSER_SECLVL"]
        self.ro_auth_type=snmp_config_map["SNMP_CONFIG"]["SNMP_ROUSER_AUTHTYPE"]
        self.ro_auth_key =snmp_config_map["SNMP_CONFIG"]["SNMP_ROUSER_AUTHKEY"]
        self.ro_priv_type=snmp_config_map["SNMP_CONFIG"]["SNMP_ROUSER_PRIVTYPE"]
        self.ro_priv_key =snmp_config_map["SNMP_CONFIG"]["SNMP_ROUSER_PRIVKEY"]
        self.rw_username=snmp_config_map["SNMP_CONFIG"]["SNMP_RWUSER"]
        self.rw_security_level=snmp_config_map["SNMP_CONFIG"]["SNMP_RWUSER_SECLVL"]    
        self.rw_auth_type=snmp_config_map["SNMP_CONFIG"]["SNMP_RWUSER_AUTHTYPE"]
        self.rw_auth_key=snmp_config_map["SNMP_CONFIG"]["SNMP_RWUSER_AUTHKEY"]
        self.rw_priv_type=snmp_config_map["SNMP_CONFIG"]["SNMP_RWUSER_PRIVTYPE"]
        self.rw_priv_key=snmp_config_map["SNMP_CONFIG"]["SNMP_ROUSER_PRIVKEY"]
        self.trap_engine_id=snmp_config_map["SNMP_CONFIG"]["SNMP_ENGINEID"]
        self.trap_username=snmp_config_map["SNMP_CONFIG"]["SNMP_TRAP_USER"]
        self.trap_security_level=snmp_config_map["SNMP_CONFIG"]["SNMP_TRAP_SECLVL"]
        self.trap_auth_type=snmp_config_map["SNMP_CONFIG"]["SNMP_TRAP_AUTHTYPE"]
        self.trap_auth_key=snmp_config_map["SNMP_CONFIG"]["SNMP_TRAP_AUTHKEY"]
        self.trap_priv_type=snmp_config_map["SNMP_CONFIG"]["SNMP_TRAP_PRIVTYPE"]
        self.trap_priv_key=snmp_config_map["SNMP_CONFIG"]["SNMP_TRAP_PRIVKEY"]     
        
    def cmd_stdout(self, command, argument, timeout=3):
        ''' TODO
        '''

        cmd = command +' ' + argument +'>ttt.txt'
        basic_airlink.cslog(command +' ' + argument, "BLUE","WHITE")

        os.system(cmd)
        
        time.sleep(timeout)
        
        if os.path.getsize("ttt.txt") == 0: 
            return ""
        
        fh=open('ttt.txt','r')
        input_file = fh.read()
        fh.close()
        basic_airlink.cslog(input_file, "BLUE","WHITE")

        return input_file

    def cmd_stdout_last_line(self, command, argument, timeout=3):
        ''' TODO
        '''

        cmd = command +' ' + argument +'>ttt.txt'
        basic_airlink.cslog(command +' ' + argument, "BLUE","WHITE")

        os.system(cmd)
        
        time.sleep(timeout)
        
        if os.path.getsize("ttt.txt") == 0: 
            return ""
        
        fh=open('ttt.txt','r')
        for line in fh:
            pass
        fh.close()
        
        basic_airlink.cslog(line, "BLUE","WHITE")

        return line

    def cmd_stdout_value(self, command, argument, timeout=3):
        ''' TODO
        '''

        cmd = command +' ' + argument +'>ttt.txt'
        basic_airlink.cslog(command +' ' + argument, "BLUE","WHITE")

        os.system(cmd)
        
        time.sleep(timeout)
        
        if os.path.getsize("ttt.txt") == 0: 
            return ""
        
        fh=open('ttt.txt','r')
        for line in fh:
            pass
        fh.close()
        
        if line.find("Failed",0)>=0 or line.find("Timeout",0)>=0: 
            return "Failed"
        
        value = line[6:]
        basic_airlink.cslog(line, "BLUE","WHITE")
        basic_airlink.cslog(value, "BLUE","WHITE")

        return value
    
    def msciid_map_oid(self, msci_id):
        
        lll= len(snmp_oid_map)
        
        for i in range(0,lll+1):
            if snmp_oid_map[i][4] == msci_id:
                return snmp_oid_map[i][0]
        return ""        
        
    def snmpget(self, agent_host, oid):
        ''' agent_host: device IP
        '''
        if self.snmp_ver == 2: 
            return self.snmpget_v2c(self.ro_community, agent_host, oid, self.snmp_port, 10)
        elif self.snmp_ver == 3: 
            return self.snmpget_v3(self.ro_username, self.ro_auth_type, self.ro_auth_key, self.ro_priv_type, self.ro_priv_key, self.ro_security_level,agent_host, oid, timeout=30)
          
    def snmpset(self, agent_host, oid, value):
        ''' TODO
        '''
        if self.snmp_ver == 2: 
            return self.snmpset_v2c(self.rw_community, agent_host, oid, value, self.snmp_port, 10)
        elif self.snmp_ver == 3: 
            return self.snmpset_v3(self.rw_username, self.rw_auth_type, self.rw_auth_key, self.rw_priv_type, self.rw_priv_key, self.rw_security_level,agent_host, oid, value, timeout=30)

    def snmpwalk(self, agent_host):
        if self.snmp_ver == 2: 
            return self.snmpwalk_v2c(self.rw_community, agent_host, self.snmp_port, 90)
        elif self.snmp_ver == 3: 
            return self.snmpwalk_v3(self.rw_username, self.rw_auth_type, self.rw_auth_key, self.rw_priv_type, self.rw_priv_key, self.rw_security_level,agent_host, self.snmp_port, timeout=30)

    def snmpget_v2c(self, 
                    community, 
                    agent_host, 
                    oid, 
                    snmp_port=161, 
                    timeout=5):
        '''
        To perform SNMP v2 GET operation
        Args:
        
            community : SNMP v2c community name 
            agent_host: agent hosy IP address 
            oid       : object id specified 
        Returns: 
            the value of oid 
        '''
        os.chdir(airlinkautomation_home_dirname+'/tools/snmpsoft')
        cmd ="snmpget.exe"
        arg =" -c:"+community+" -v:2c " +"-r:"+agent_host +\
        " -p:"+str(snmp_port)+" -o:"+ oid
        ret=self.cmd_stdout_value(cmd, arg, timeout)
        if ret.find("Failed",0)>=0:
            return "Failed"
        else:
            return ret
                
    def snmpset_v2c(self, 
                    community, 
                    agent_host, 
                    oid, 
                    value, 
                    snmp_port=161, 
                    timeout=30):  
        '''
        Perform SNMP v2c SET operation
        '''
        os.chdir(airlinkautomation_home_dirname+'/tools/snmpsoft')
        cmd ="snmpset.exe"
        
        if  type(value) is IntType:
            arg =" -c:"+community+" -v:2c -t:"+str(timeout)+" -r:" +\
            agent_host +" -o:"+ oid +" -val:" + str(value)+ " -tp:int " 
        elif  type(value) is StringType:
            arg =" -c:"+community+" -v:2c -t:"+str(timeout)+\
            " -r:" +agent_host +" -o:"+ oid +" -val:" + value + " -tp:str " 
                
        ret=self.cmd_stdout_last_line(cmd, arg, timeout) 
        if ret.find("OK",0)>=0:
            return True
        else:
            return False      
      
    def snmpwalk_v2c(self, community, agent_host, snmp_port=161, timeout=180):
        '''
        '''
        os.chdir(airlinkautomation_home_dirname+'/tools/snmpsoft')
        cmd ="snmpwalk.exe"
        arg =" -t:"+str(timeout)+" -c:"+community+" -v:2c -r:" +\
        agent_host +" -p:"+str(snmp_port)
            
        return self.cmd_stdout(cmd, arg, timeout)


    def snmptrap_v2c(self, community, agent_host, trap_oid, timeout=10):
        ''' TODO with event report periodically
        '''
        os.chdir(airlinkautomation_home_dirname+'/tools/snmpsoft')

        cmd ="snmptrapgen.exe"
        arg =" -t:"+str(timeout)+" -c:"+community+" -v:2c " +\
        " -r:"+agent_host +" -to:"+ trap_oid
            
        return self.cmd_stdout(cmd, arg, timeout)
                                    
 
    def snmpget_v3(self, username, auth_type, auth_key, priv_type, priv_key, security_level,agent_host, oid, timeout=30):
        '''
        To Perform SNMP v2 GET operation
        Args:
        
            community : SNMP v2c community name 
            agent_host: agent hosy IP address 
            oid       : object id specified 
        Returns: 
            the value of oid 
        '''

        os.chdir(airlinkautomation_home_dirname+'/tools/snmpsoft')
        cmd ="snmpget.exe"
        
        if   security_level == 2: 
            arg =" -v:3 " +" -r:"+agent_host +" -sn:"+username+\
            " -ap:"+auth_type+" -aw:"+auth_key+\
            " -pp:"+priv_type+" -pw:"+priv_key+\
            " -o:"+ oid

        elif security_level == 1: 
            arg =" -v:3 " +" -r:"+agent_host +" -sn:"+username+\
            " -ap:"+auth_type+" -aw:"+auth_key+" -o:"+ oid
            
        elif security_level == 0: 
            arg =" -v:3 " +" -r:"+agent_host +" -sn:"+username+" -o:"+ oid         
               
        return self.cmd_stdout(cmd, arg, timeout)


    def snmpset_v3(self, username, auth_type, auth_key, priv_type, priv_key, security_level,agent_host, oid, value, timeout=30):
        
        os.chdir(airlinkautomation_home_dirname+'/tools/snmpsoft')
        cmd ="snmpset.exe"
        
        if security_level == 2: 
            if type(value) is IntType: 
                arg =" -v:3 " +" -r:"+agent_host +" -sn:"+username+\
                " -ap:"+auth_type+" -aw:"+auth_key+\
                " -pp:"+priv_type+" -pw:"+priv_key+\
                " -o:"+ oid +\
                " -val:"+str(value) +" -tp:int"

            elif type(value) is StringType: 
                arg =" -v:3 " +" -r:"+agent_host +" -sn:"+username+\
                " -ap:"+auth_type+" -aw:"+auth_key+\
                " -pp:"+priv_type+" -pw:"+priv_key+\
                " -o:"+ oid +\
                " -val:"+value +" -tp:str"
                
        elif security_level == 1: 
            
            if type(value) is IntType: 
                arg =" -v:3 " +" -r:"+agent_host +" -sn:"+username+\
                " -ap:"+auth_type+" -aw:"+auth_key+\
                " -o:"+ oid +\
                " -val:"+str(value) +" -tp:int"
            elif type(value) is StringType: 
                arg =" -v:3 " +"-r:"+agent_host +" -sn:"+username+\
                " -ap:"+auth_type+" -aw:"+auth_key+\
                " -o:"+ oid +\
                " -val:"+value +" -tp:str"
                                                
        elif security_level == 0: 
            if type(value) is IntType: 
                arg =" -v:3 " +" -r:"+agent_host +" -sn:"+username+" -o:"+ oid+\
                " -val:"+ str(value) +" -tp:int"
  
            elif type(value) is StringType: 
                arg =" -v:3 " +" -r:"+agent_host +" -sn:"+username+" -o:"+ oid+\
                " -val:"+value +" -tp:str"

        ret=self.cmd_stdout(cmd, arg, timeout)
        
        if ret.find("Failed",0)>=0: 
            return False 
        else:
            return True

                 
    def snmpwalk_v3(self, username, auth_type, auth_key, priv_type, priv_key, security_level,agent_host, port=161, timeout=30):
       
        os.chdir(airlinkautomation_home_dirname+'/tools/snmpsoft')
        cmd ="snmpwalk.exe"
        
        if security_level == 2: 
            arg =" -v:3 " +" -r:"+agent_host +" -sn:"+username+\
            " -ap:"+auth_type+" -aw:"+auth_key+\
            " -pp:"+priv_type+" -pw:"+priv_key+\
            " -p:"+str(port)

        elif security_level == 1: 
            
            arg =" -v:3 " +" -r:"+agent_host +" -sn:"+username+\
            " -ap:"+auth_type+" -aw:"+auth_key +\
            " -p:"+str(port)
                                                
        elif security_level == 0: 
            arg =" -v:3 " +" -r:"+agent_host +" -sn:"+username +\
            " -p:"+str(port)
            
        return self.cmd_stdout(cmd, arg, timeout)  
  
    def snmptrap_v3(self,community,agent_host,snmp_port,trap_oid,timeout=30): 
        ''' TODO with event report periodically
        '''
        
        os.chdir(airlinkautomation_home_dirname+'/tools/snmpsoft')

        cmd ="snmptrapgen.exe"
        arg =" -t:"+str(timeout)+" -c:"+community+" -v:3 " +\
        " -r:"+agent_host +" -to:"+ trap_oid
            
        return self.cmd_stdout(cmd, arg, timeout)    

    def snmpget_ecio_v2c(self, agent_host, cell_net):
        ''' get GPRS/CDMA Ecio by SNMP v2c
        
        Returns: string ecio value 
        '''
        if cell_net =="GPRS" or cell_net=="GSM" or cell_net=="WCDMA":
            ecio_oid = self.msciid_map_oid(MSCIID_STS_GPRS_ECIO)
            
        elif cell_net =="CDMA" or cell_net=="EVDO":
            ecio_oid = self.msciid_map_oid(MSCIID_STS_CDMA_ECIO)
            
        return self.snmpget_v2c( self.rw_community, agent_host, ecio_oid, self.snmp_port, timeout=30)


    def snmpget_ecio_v3(self, agent_host, cell_net):
        ''' read GPRS/CDMA Ecio by SNMP v3, it is READ ONLY.
        Returns: string ecio value 
        '''
        if cell_net =="GPRS" or cell_net=="GSM" or cell_net=="WCDMA":
            ecio_oid = self.msciid_map_oid(MSCIID_STS_GPRS_ECIO)
            
        elif cell_net =="CDMA" or cell_net=="EVDO":
            ecio_oid = self.msciid_map_oid(MSCIID_STS_CDMA_ECIO)
            
        return self.snmpget_v3(self.rw_username, self.rw_auth_type, self.rw_auth_key, self.rw_priv_type, self.rw_priv_key, self.rw_security_level,agent_host, ecio_oid, timeout=30)


    def snmpget_trap_ip_v3(self, agent_host):
        ''' get trap IP by SNMP v3
        Returns: True/False 
        '''
        trap_ip_oid = self.msciid_map_oid(MSCIID_CFG_CMN_SNMP_TRAPDEST)
        return self.snmpget_v3(self.rw_username, self.rw_auth_type, self.rw_auth_key, self.rw_priv_type, self.rw_priv_key, self.rw_security_level,agent_host, trap_ip_oid, timeout=30)

    def snmpset_trap_ip_v3(self, agent_host, trap_ip):
        ''' set trap IP by SNMP v3
        Returns: True/False 
        '''
        trap_ip_oid = self.msciid_map_oid(MSCIID_CFG_CMN_SNMP_TRAPDEST)
        return self.snmpset_v3(self.rw_username, self.rw_auth_type, self.rw_auth_key, self.rw_priv_type, self.rw_priv_key, self.rw_security_level,agent_host, trap_ip_oid, trap_ip, timeout=30)
      
