This tool is for testing Enable/Disable DMNR feature in ACEManager.
This tool is self contained

The tool counts Enable and then Disable as ONE round(time)

Usage: 
1, Open cmd, go to the folder of this tool

2, Example: python launcher.py -n 3    (If you don't pass any argument here, the default is 5 times)

3, The tool will dump the information from linux after doing 3 times Enable/Disable
And it will keep dumping the file every 3 times.

4, You can stop the script anytime you want. Ctrl+c

5, The info will be dumped to logs/ folder under this tool's directory.



  