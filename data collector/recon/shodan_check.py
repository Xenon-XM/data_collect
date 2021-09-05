import shodan

SHODAN_API_KEY = "SHODAN KEY"

class Shodan_checker():
        def __init__(self):
                self.api = shodan.Shodan(SHODAN_API_KEY)
                self.banners=list()
        def check(self, ip):
                try:
                        host = self.api.host(ip)
                        #self.org=host.get('org', 'n/a')
                        #self.os=host.get('os', 'n/a')
                        for item in host['data']:        
                                string = str(item['port']) + ":" + item['data'].replace("\n",", ")
                                string=string.replace('\r', '')
                                #string.replace("\n","")
                                self.banners.append(string)
                except:
                        self.basnners = 0
