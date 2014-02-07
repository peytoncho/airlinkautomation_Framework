import yaml
import io
import wx

class FwupdateController():
    
    def __init__(self):
        pass
       
    def loadGuiYmlFile(self):
        with open('fwupdate_GUI.yml','r') as stream:
            fwupdate_map = yaml.load(stream)
        return fwupdate_map
    
    def loadInfoYmlFile(self):
        with open('fwupdate_info.yml','r') as stream:
            fwupdate_info_map = yaml.load(stream)
        return fwupdate_info_map
    
    def dumpYmlFile(self, fwupdate_map):    
        stream = open('fwupdate_GUI.yml','w')
        yaml.dump(fwupdate_map, stream, default_flow_style=False)
        stream.close()
    
    def getMapData(self, fwupdate_map, key):
        value = fwupdate_map[key]
        return value
    
    def setMapData(self, fwupdate_map, key, value):
        fwupdate_map[key] = value
        
    
# if __name__ == '__main__':
#     obj = FwupdateController()
#     obj.setDeviceName()   
    