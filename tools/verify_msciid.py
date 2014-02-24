import basic_airlink
import selenium_utilities
import time
import sys

se_ins = selenium_utilities.SeleniumAcemanager()
ace_page_data = basic_airlink.get_ace_config_data()
tbd_config_data = basic_airlink.get_tbd_config_data()
ace_element_data = basic_airlink.get_ele_config_data('4.3.5')

def get_element_common(driver,page,subtab,element_id):
    result = True
    element_txt = ""
    try:
        element_txt = se_ins.get_by_id(driver, page, subtab, element_id) 
    except:
        result = False
    return element_txt, result

def run(target_id):
    driver = se_ins.login(tbd_config_data[se_ins.device_name]['ACE_URL'], \
                          tbd_config_data[se_ins.device_name]['USERNAME'], \
                          tbd_config_data[se_ins.device_name]['PASSWORD'])
    element_value = ""
    result = True
    msg = ""
    for page,v1 in ace_element_data.iteritems():
        for subtab,v2 in ace_element_data[page].iteritems():
            for element,v3 in ace_element_data[page][subtab].iteritems():
#                sys.stdout.write("Checking===> Page: \'"+page+"\' | Subtab: \'"+subtab+"\' | Element: \'"+element+"\' ...")
#                element_value, result = get_element_common(driver,page,subtab,v3[0])
                if target_id == v3[0]:
                    print page
                    print subtab
                if result == True:
                    msg = "Pass"
                else:
                    msg = "Fail"
                sys.stdout.write(msg+'\n')
                
                #print k3+' : '+v3[0]

if __name__ == '__main__':
    run()
