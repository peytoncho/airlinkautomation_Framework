from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp import debug

#debug.setLogger(debug.Debug('all'))
cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData('public'),
    cmdgen.UdpTransportTarget(('demo.snmplabs.com', 161)),
    cmdgen.MibVariable('SNMPv2-MIB', 'sysName', 0)
)

# Check for errors and print out results
if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex)-1] or '?'
            )
        )
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))