import urllib.request, urllib.error, urllib.parse
import os

class Download:
    def __init__(self, address, subdomain_resolver):
        self.address = address
        self.domain = "researchdns." + address
        self.subdomain_resolver = subdomain_resolver

    
    def write(self, filename, url):
        try:
            response = urllib.request.urlopen(url)
            webContent = response.read()
            f = open(filename, 'wb')
            f.write(webContent)
            f.close
        except:
            pass

    def copy(self):
        filename = "/home/azureuser/collect/webpages/" + self.address + "/"+self.address + ".html"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        domain = "http://"+self.address
        self.write(filename, domain)
        if self.subdomain_resolver:
            filename = "/home/azureuser/collect/webpages/" +self.address + "/" +self.domain + ".html"
            domain = "http://"+self.domain
            self.write(filename, domain)

