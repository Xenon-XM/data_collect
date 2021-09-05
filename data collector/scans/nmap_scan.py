import nmap
class NmapScanner:
    def __init__(self):
        pass
    def scan(self, target):
        try:
            nm = nmap.PortScanner()
            #TCP/IP fingerprinting (for OS scan)
            machine = nm.scan(target, arguments=' --host-timeout=30 -O')
            self.os = machine['scan'][target]['osmatch'][0]['osclass'][0]['osfamily']
        except:
            self.os = "Unknown"
        
