import fwupdate_airlink as fa
import lan_airlink as la
import telnet_airlink as ta
import at_utilities
import time


fa_ins = fa.FwupdateAirlink()
lan_ins = la.LanAirlink()
ta_ins = ta.TelnetAirlink()
at_ins = at_utilities.AtCommands()

#ta_ins.read_until_safe(expected_key)

ftp_ip = "192.168.13.101"
ftp_username = "user1"
ftp_pwd = "12345"
rm_filename = "MC8705_ATT001_3553.bin"

while not ta_ins.connect():
    print "connection fail"

ret = at_ins.rm_update(ta_ins, ftp_ip, ftp_username, ftp_pwd, rm_filename)
print ret


#fa_ins._verify_rm("MC8705_ATT001_3553")

# url = "HTTP://192.168.13.31:9191"
# username = "user"
# password = "12345"
# change_ip = "192.168.13.1"
# change_ip_url = "HTTP://"+change_ip+":9191"
# driver = lan_ins.login(url, username, password)
# lan_ins.set_ethernet_device_ip(driver, change_ip)
# lan_ins.apply_reboot(driver)
# time.sleep(150)
# driver.close()
# driver = lan_ins.login(change_ip_url, username, password)


