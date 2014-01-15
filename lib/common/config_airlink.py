import yaml, datetime,logging
import basic_airlink

class ConfigParser:
    ''' this class provides method to handle the test bed yaml configuratiom file 
    '''
    
    def __init__(self, config_file = "config/testbed2Conf.yml"):

        stream = open(config_file, 'r')
        self.map = yaml.load(stream)
        stream.close()


    def processing_config(self, feature_name):
        ''' to transfer info from yaml config files to list
            
        '''
        
        current_date_str = str(datetime.datetime.now().date())
        current_time_str = str(datetime.datetime.now().time()).replace(":","-")
        
        self.device_name  = self.map["DUTS"][0]


        log_filename = \
        self.map["LOG_FILE_FOLDER"]+current_date_str+"_"+current_time_str+"_"+ \
        self.map[self.device_name]["MODEL"]  +"_" + \
        self.map[self.device_name]["RM_TYPE"]+ "_"+ \
        self.map[self.device_name]["ALEOS_FW_VER"]+ "_"+ \
        feature_name+"_testsuite.log"
        FORMAT ='%(asctime)-15s => %(levelname)-8s => %(message)s'
        LEVEL=basic_airlink.log_level[self.map["PYTHON_LOGGING_LEVEL"]]
        basic_airlink.slog(self.map["PYTHON_LOGGING_LEVEL"])
        logging.basicConfig(filename = log_filename, format=FORMAT, level = LEVEL)  
        