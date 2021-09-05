from pysafebrowsing import SafeBrowsing

result = {}
def check_domain_sb(url):
    domain = "http://"+url
    s = SafeBrowsing('SAFEBROWSING KEY')
    try:
        a =  s.lookup_urls([domain])
    except:
        return 0
    binary = a[domain]['malicious']
    if str(binary)=="False":
        return binary
    else:
        return a[domain]['threats']
def sf(url, subdomain_resolver):
    result['domain'] = check_domain_sb(url)
    if subdomain_resolver:
        result['subdomain'] = check_domain_sb("dontworryitsresearch."+url)
    else:
        result['subdomain'] = 0
    return result
