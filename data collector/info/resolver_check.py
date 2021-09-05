import dns.resolver

def resolve_check(domain):
    subdomain = 'researchdns.' + domain
    try:
        dns.resolver.resolve(subdomain, 'A')
        return True
    except:
        return False
def resolve_check_domain(domain):
    try:
        dns.resolver.resolve(domain, 'A')
        return True
    except:
        return False

