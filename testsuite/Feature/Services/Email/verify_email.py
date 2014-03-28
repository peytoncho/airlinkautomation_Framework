from selenium import webdriver   
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import selenium.webdriver.remote.webdriver
import os
import sys
import time


class VerifyEmail(object):
    def __init__(self,des_email_svr = "gmail",username="airlinksierra@gmail.com",password="v3r1fym3"):
        self.des_email_svr = des_email_svr
        self.username = username
        self.password = password
        
        if self.des_email_svr == "gmail":
            self.url = "HTTP://mail.google.com" 
    
    def access_email_client(self):
        driver = webdriver.Firefox()
        driver.get(self.url)
        
        if self.des_email_svr == "gmail":
            driver.find_element_by_id("Email").clear()
            driver.find_element_by_id("Email").send_keys(self.username)
            driver.find_element_by_id("Passwd").clear()
            driver.find_element_by_id("Passwd").send_keys(self.password)
            driver.find_element_by_id("signIn").click()
            
        
        #for other email service provider, please add the login page implementation code below    
        return driver
    
    def verify_email_subject(self, driver, expect_str):
        subj_str = ""
        try:
            WebDriverWait(driver, timeout=60).until(EC.visibility_of_element_located((\
                                            By.XPATH, "//div[@class='y6']/span[contains(.,\'"+expect_str+"\')]")))
            subj_ele = driver.find_element_by_xpath(\
                                            "//div[@class='y6']/span[contains(.,\'"+expect_str+"\')]")
            subj_str = subj_ele.text
        
        except:
            print "ERROR!"
     
        return subj_str


if __name__ == "__main__":
    email_ins = VerifyEmail()
    driver = email_ins.access_email_client()
    
    print email_ins.verify_email_subject(driver, "This")
    print "DONE!"

