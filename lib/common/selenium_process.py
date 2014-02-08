import time
import os, sys, getpass
import multiprocessing
import threading

sys.path.append(os.environ['AIRLINKAUTOMATION_HOME'] + "/lib/common")
sys.path.append(os.environ['AIRLINKAUTOMATION_HOME'] + "/lib/site-packages")

import selenium_utilities
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import yaml
import msciids
import proxy_airlink
import basic_airlink

class SeleniumProcess(multiprocessing.Process):
    # queue used to pass logging information from child process to main process
    log_queue = multiprocessing.Queue() 
    stop_logging_thread = False

    # strings that designate which task is to be done
    WAIT_NETWORK_READY = "WAIT_NETWORK_READY"
    REBOOT = "REBOOT"

    def __init__(self, test_config, task, timeout, conn, proxy_ip = None):
        # This method runs in the main process when the object is created
        multiprocessing.Process.__init__(self) # init function of parent class

        self.conn = conn 
        self.task = task
        self.timeout = timeout
        self.test_config = test_config
        self.proxy_ip = proxy_ip

        # save reference to log_queue, when new process forks with the call the start() the class variable in the new process gets over-written
        # we restore it when the new process starts (at the beginning of run())
        self.temp = self.__class__.log_queue 

        # maps the task that is passed in to the actual function - to add more tasks you will have to subclass this class (SeleniumProcess). 
        # see selenium_vpn.py as example
        self.available_tasks = {self.WAIT_NETWORK_READY:self.wait_network_ready,
                                self.REBOOT:self.reboot}

        if self.task in self.available_tasks.keys():
            self.f = self.available_tasks[self.task]

    @classmethod # This method runs in the main process
    def create_and_execute(cls, task, config, timeout, retries, proxy_ip = None):
        # Create a thread within the main process handle logging done in the child process 
        # as there's no way to log to the same file from multiple proccess in python
        cls.stop_logging_thread = False
        logging_thread = threading.Thread(target = cls.log_handler)
        logging_thread.start()

        for attempt in range(retries):
            conn, child_conn = multiprocessing.Pipe(duplex = False) # pipe so child process can send back results
            se_process = cls(config, task, timeout, child_conn, proxy_ip) # create child process object - process is not created in system yet
            #se_process.daemon = 1
            se_process.start() # fork new process in OS, the spawned process's entry point is se_process.run()

            if conn.poll(2*timeout):
                # Child process responded with results before time out
                result = conn.recv() # get results
            else:
                # Child process did not respond with results before time out
                se_process.os_kill_browser(config["BROWSER"]) # force kill all browsers
                result = {}
                result["EXCEPTION"] = True
                result["RESULT"] = False # set result to False so we won't break out of the FOR-loop if there are retries remaining
                basic_airlink.cslog("Child process timed out after %d seconds" %(2*timeout))

            if se_process.is_alive(): # kill child process if it's still alive
                try:
                    se_process.terminate()
                except WindowsError:
                    basic_airlink.slog("WindowsError excepted when terminating child process, try to terminate child process with os.system()...")
                    os.system("taskkill /pid %s /t /f >nul 2>&1" %str(se_process.pid))

                se_process.join(10)

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

    def run(self): # This method is the entry point in the new process. do not call this directly, call start() to spawn the new process
        # restore class variable so it points to the same queue as the one in the main process
        self.__class__.log_queue = self.temp

        # suppress console output - if we want to print, call self.mp_log()
        f = open(os.devnull, 'w')
        sys.stdout = f

        try:
            self.login() # log into acemanager
            self.t = threading.Timer(self.timeout, self.timeout_handler) # generate selenium except by closing the driver if timeout
            self.t.start()
            result = self.f() # do the task 
            self.t.cancel() # stop timer
        except Exception as error:
            self.close_driver()
            self.mp_log("Selenium Error while performing %s: %s" %(self.task, str(error)), "s")
            self.conn.send({"EXCEPTION":True, "RESULT":False})
            return

        self.close_driver()
        self.conn.send({"EXCEPTION":False, "RESULT":result})

    def timeout_handler(self):
        self.close_driver()
        self.mp_log("Selenium timed out after %d seconds" %self.timeout, "cs")
        self.conn.send({"EXCEPTION":True, "RESULT":False})

    def close_driver(self):
        try:
            self.driver.quit()
        except Exception as e:
            self.os_kill_browser(self.test_config["BROWSER"])

        time.sleep(1)

    @staticmethod
    def os_kill_browser(browser):
        # Kill browser through OS
        if browser == "FF":
            os.system("taskkill /im firefox.exe /t /f >nul 2>&1")
        elif browser == "IE":
            os.system("taskkill /im IEDriverServer.exe /t /f >nul 2>&1")
            os.system("taskkill /im iexplore.exe /t /f >nul 2>&1")

        # clean up temp dir on pc because selenium FF webdriver creates ~100 MB of temp 
        # files and only deletes them if driver.quit() is called and is successful
        temp_dir = "C:\\Users\\%s\\AppData\\Local\\Temp\\" % getpass.getuser()
        for each in os.listdir(temp_dir):
            os.system("rmdir %s%s /S /Q >nul 2>&1" %(temp_dir,each))

    def mp_log(self, msg, level="cs"):
        # send logging information back to main process to be logged
        # level can be any of "cs", "c", "s" which corresponds to the basic_airlink.cslog, clog, slog
        self.__class__.log_queue.put({"msg": msg, "level": level})
        
    def login(self):
        if self.proxy_ip is not None:
            self.proxy = proxy_airlink.ProxyAirlink(self.proxy_ip)
            self.proxy_conn = self.proxy.connect()
            self.local_se_ins = selenium_utilities.SeleniumAcemanager()
            self.se_ins = self.proxy.deliver(self.local_se_ins)
        else:
            self.se_ins = selenium_utilities.SeleniumAcemanager()
        
        self.driver = self.se_ins.login(self.test_config["ACEMANAGER_URL"], self.test_config["ACEMANAGER_USER"], self.test_config["ACEMANAGER_PASSWORD"])
        time.sleep(2)

    def wait_network_ready(self):

        time.sleep(1)
        network_state = self.driver.find_element_by_id(str(msciids.MSCIID_STS_NETWORK_STATE)).text
        self.mp_log("Waiting for network ready on ACEmanager -> network_state = %s" %network_state, "s")

        return network_state == "Network Ready"

    def reboot(self):
        time.sleep(1)
        ret = self.se_ins.reboot(self.driver)
        time.sleep(1)
        return ret
