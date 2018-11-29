# requiere pyshark-legacy

import pyshark
cap = pyshark.FileCapture('archivo.pcap', only_summaries=True, keep_packets="True", display_filter="http")

pkts = []
try: 
  for pkt in cap:  
    print pkt
    pkts.append(pkt)
        
except pyshark.capture.capture.TSharkCrashException as e:
  pass

print len(pkts)
