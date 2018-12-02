from pysnmp.hlapi import *

def consultaSNMP(comunidad, host, oid):
  errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))
  
  resultado = "0"

  if errorIndication:
    pass
    # print(errorIndication)    
  elif errorStatus:
    pass
    # print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
  else:
    for varBind in varBinds:
      varB = (' = '.join([x.prettyPrint() for x in varBind]))
      resultado = varB.split()[2]
  
  return resultado
