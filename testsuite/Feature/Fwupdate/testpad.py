import fwupdate_airlink as fa
import lan_airlink as la
import time


fa_ins = fa.FwupdateAirlink()
lan_ins = la.LanAirlink()
#fa_ins._verify_rm("MC8705_ATT001_3553")

url = "HTTP://192.168.13.31:9191"
username = "user"
password = "12345"
change_ip = "192.168.13.1"
change_ip_url = "HTTP://"+change_ip+":9191"
driver = lan_ins.login(url, username, password)
lan_ins.set_ethernet_device_ip(driver, change_ip)
lan_ins.apply_reboot(driver)
time.sleep(150)
driver.close()
driver = lan_ins.login(change_ip_url, username, password)


