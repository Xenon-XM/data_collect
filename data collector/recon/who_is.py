import whois

class whois_info:
    def __init__(self, domain):
        self.domain = domain
        try:
            self.w = whois.whois(domain)
            self.registrar = self.w.registrar
            self.country = self.w.country
            self.email = self.w.emails
            self.city = self.w.city
            self.org = self.w.org
            self.creation = self.w.creation_date
            self.exporation = self.w.expiration_date
        except:
            self.registrar = None
            self.country = None
            self.email = None
            self.city = None
            self.org = None
            self.creation = None
            self.exporation = None
        
