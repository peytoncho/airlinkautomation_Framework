################################################################################
# This class provides basic methods for FTP operation.
# Company: Sierra Wireless
# Time   : Jun 11, 2013
# Author : Airlink 
#
################################################################################

import time
import os
import glob
import logging
import ftplib  
import basic_airlink 
        
class FtpAirlink(object):
    '''  This class provides basic methods to do FTP
    
    '''
                     
    def __init__(self):
        ''' check all related items in testbed'''
        
        self.airlinkautomation_home_dirname = os.environ['AIRLINKAUTOMATION_HOME']
         
         
    def login(self,ftp_server_address, username, password, ftp_timeout=600):
        '''  login to FTP server 
        
        Args:
            ftp_server_address: FTP server IP address
            username : user name 
            password : password 
            ftp_timeout: FTP timeout, the default is 600s
        Returns:
            True/False
        '''

        basic_airlink.slog("login to FTP server: "+ftp_server_address +";" + username+";" + password)
        
        try:
        
            self.ftpp = ftplib.FTP(ftp_server_address, username, password,ftp_timeout)
        
            self.ftpp.login(username, password)
        
            self.ftpp.set_debuglevel(2)
            
        except Exception, e:
            
            logging.debug("\n FTP server login failed, the exception is "  + str(e))
            return False        
 
        basic_airlink.slog("FTP server login succeed")
       
        return True
    
    
    def quit(self):
        ''' Disconnect FTP server '''
        
        self.ftpp.quit()
        basic_airlink.slog("Disconnect FTP server")

        
    def get_dir_list(self):
        '''  get the file list from the server directory '''

        data = []

        self.ftpp.dir(data.append)

        for line in data:
            print "-", line


    def download_file(self, pathname, filename):
        ''' Download a file by FTP, and get the download time 
        Args: 
            pathname: local folder name 
            filename: name of file to download
            
        Returns: 
            True/False
        ''' 

        starttime = time.time()
        self.download_time=0
        local_filename = pathname+"/"+ filename
        
        try: 

            fh = open(local_filename, "wb")
            self.ftpp.retrbinary("RETR " + filename, fh.write, 1024)
            fh.close()
            
        except Exception, e:
            basic_airlink.slog("Download file failed, the exception is "  + str(e))
            return False
        
        endtime = time.time()  
        
        self.download_time = endtime - starttime
        basic_airlink.slog("Download file done. This download time(s) is: " +  str(self.download_time) )
        return True

        
    def upload_file(self,pathname, filename):
        '''
         Using the ftplib module to upload file, and get the upload time
         
        Args: 
            pathname: local folder name 
            filename: name of file to upload
            
        Returns: 
            True/False

        '''  

        starttime = time.time()
        self.upload_time = 0
      
#        try: 
#            ftp.delete(filename)
#            
#        except Exception, e:
#            logging.debug(" file delete problem found "  + str(e))
                
        try: 
            local_filename = pathname + "/"+ filename

            ext = os.path.splitext(filename)[1]
            
            if ext in (".txt", ".htm", ".html"):
                self.ftpp.storlines("STOR " + filename, open(local_filename))
            else:
                self.ftpp.storbinary("STOR " + filename, open(local_filename, "rb"), 1024)
             
        except Exception, e:
            basic_airlink.slog("Upload file failed, the exception is "  + str(e))
            return False
                   
        endtime = time.time()  
        
        self.upload_time = endtime - starttime
        basic_airlink.slog("upload file done. This upload time (s) is: " +  str(self.upload_time) )
             
        return True     
    
    def generate_mb_file(self, pathname, filename, number_mb):
        ''' generate a file whose isze is n*MB 
        
        Args: 
            pathname: local folder name 
            filename: name of file
            number_mb: file size, unit MB
            
        Returns: 
            True/False

        '''
        
        try: 
            local_filename = pathname+"/"+ filename
            
            with open(local_filename, 'wb') as bigfile:
                bigfile.seek(1048576*number_mb)
                bigfile.write('0')
                
        except Exception, e:
                basic_airlink.slog("Generating file failed "  + str(e))
                return False 

        basic_airlink.slog("Generating file OK ")

        return True
         

    def upload_file_scheduler(self, interval, repeat_times, size_flag):
        ''' upload file for times, and get the average upload time 
        
        Args:
             interval:  interval time
             repeat_times: FTP repeat times
             size_flag: 
                 L - large of file 100MB, 
                 M - middle size of file 10MB, 
                 S - small size of 1MB file
             
        Returns: 
            avg_upload_time average upload time 
        '''

        avg_upload_time   =0
           
        for xxx in range(1,repeat_times+1):
            
            basic_airlink.slog(" the loop:" + str(xxx))
            
            pathname = self.airlinkautomation_home_dirname+'/data/testfiles'
            
            if   size_flag =="L": 
                if not os.path.exists(pathname+"/"+"data_100MB.bin"):
                    self.generate_mb_file(pathname, "data_100MB.bin", 100)
            
                if not self.upload_file(pathname, 'data_100MB.bin'):
                    basic_airlink.slog("\n Upload large size file failed.")
                    return 0
                                     
            elif size_flag =="M": 
                if not os.path.exists(pathname+"/"+"data_10MB.bin"):
                    self.generate_mb_file(pathname, "data_10MB.bin", 10)

                if not self.upload_file(self.airlinkautomation_home_dirname+'/data/testfiles', 'data_10MB.bin'):
                    basic_airlink.slog("\n Upload medium size file failed.")
                    return 0  
                
            elif size_flag =="S": 
                if not os.path.exists(pathname+"/"+"data_1MB.bin"):
                    self.generate_mb_file(pathname, "data_1MB.bin", 1)
                if not self.upload_file(self.airlinkautomation_home_dirname+'/data/testfiles', 'data_1MB.bin'):
                    basic_airlink.slog("\n Upload small size file failed.")
                    return 0  
        
            avg_upload_time += self.upload_time/repeat_times

            if interval > self.upload_time: 
                time.sleep(interval-self.upload_time)
    
                         
        basic_airlink.slog("Upload and download completed successfully.")
        return avg_upload_time
 
 
    def download_file_scheduler(self, interval, repeat_times, size_flag):
        ''' download file for times, and get the average download time 
        
        Args:
             interval  interval time
             repeat_times FTP repeat times
             size_flag: 
                 L - Large of file 100MB, 
                 M -  middle size of file 10MB, 
                 S - small size of 1MB file
             
        Returns: 
            avg_download_time average download time 
        '''

        avg_download_time =0     
           
        for xxx in range(1,repeat_times+1):
             
            basic_airlink.slog(" the loop:" + str(xxx))
 
            if   size_flag =="L": 
                if not self.download_file(self.airlinkautomation_home_dirname+'/logs', 'data_100MB.bin'): 
                    basic_airlink.slog("\n Download large size file failed.")
                    return 0
                                     
            elif size_flag =="M": 
                if   not self.download_file(self.airlinkautomation_home_dirname+'/logs', 'data_10MB.bin'):
                    basic_airlink.slog("\n Download medium size file failed.")
                    return 0  
                
            elif size_flag =="S": 
                if  not self.download_file(self.airlinkautomation_home_dirname+'/logs', 'data_1MB.bin'):
                    basic_airlink.slog("\n Download small size file failed.")
                    return 0  
        
            avg_download_time += self.download_time/repeat_times   
            if interval > self.download_time: 
                time.sleep(interval-self.download_time)

        basic_airlink.slog("Download completed successfully.")
        return avg_download_time
                                      

    def transfer_file(self, repeat_times, size_flag):
        ''' upload and download file for times, and get the average upload and download time 
        
        Args:
             repeat_times FTP repeat times
             size_flag: 
                 L - large of file 100MB, 
                 M - midile size of file 10MB, 
                 S - small size of 1MB file
             
        Returns: 
            avg_upload_time   average upload time 
            avg_download_time average download time 
        '''

        avg_upload_time   =0
        avg_download_time =0     
           
        for xxx in range(1,repeat_times+1):
            
            basic_airlink.slog(" the loop:" + str(xxx))

            if   size_flag =="L": 
                filelist = glob.glob(os.path.join(self.airlinkautomation_home_dirname+'/data/testfiles', 'data_100MB.bin'))
                if not filelist:
                    self.generate_mb_file(self.airlinkautomation_home_dirname+'/data/testfiles', 'data_100MB.bin', 100)
                if not self.upload_file(self.airlinkautomation_home_dirname+'/data/testfiles', 'data_100MB.bin') or  \
                   not self.download_file(self.airlinkautomation_home_dirname+'/logs', 'data_100MB.bin'): 
                    basic_airlink.slog("\n Upload or download large size file failed.")
                    return 0,0
                                     
            elif size_flag =="M": 
                filelist = glob.glob(os.path.join(self.airlinkautomation_home_dirname+'/data/testfiles', 'data_10MB.bin'))
                if not filelist:
                    self.generate_mb_file(self.airlinkautomation_home_dirname+'/data/testfiles', 'data_10MB.bin', 10)
                if not self.upload_file(self.airlinkautomation_home_dirname+'/data/testfiles', 'data_10MB.bin') or  \
                   not self.download_file(self.airlinkautomation_home_dirname+'/logs', 'data_10MB.bin'):
                    basic_airlink.slog("\n Upload or download medium size file failed.")
                    return 0,0  
                
            elif size_flag =="S": 
                filelist = glob.glob(os.path.join(self.airlinkautomation_home_dirname+'/data/testfiles', 'data_1MB.bin'))
                if not filelist:
                    self.generate_mb_file(self.airlinkautomation_home_dirname+'/data/testfiles', 'data_1MB.bin', 1)
                if not self.upload_file(self.airlinkautomation_home_dirname+'/data/testfiles', 'data_1MB.bin') or  \
                   not self.download_file(self.airlinkautomation_home_dirname+'/logs', 'data_1MB.bin'):
                    basic_airlink.slog("\n Upload or download small size file failed.")
                    return 0,0  
        
            avg_upload_time += self.upload_time/repeat_times
            avg_download_time += self.download_time/repeat_times   
                         
        basic_airlink.slog("\n Upload and download completed successfully.")
        return avg_upload_time, avg_download_time               