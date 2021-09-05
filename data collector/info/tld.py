import tldextract

class TLD_info:
    def tld_extr(self,domain):
        extra = tldextract.extract(domain)
        self.tld = extra.suffix
        self.subdomain = extra.subdomain
        if self.subdomain=='www' or self.subdomain=='':
            self.lvl=2
        else:
            self.lvl = 3 + self.subdomain.count('.') - self.subdomain.count('www')
