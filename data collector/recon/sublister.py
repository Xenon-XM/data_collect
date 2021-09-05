import sublist3r 

def search_subdomain_sli(domain):
    try:
        subdomains = sublist3r.main(domain, 10, savefile=None, ports= None, silent=False, verbose= False, enable_bruteforce= False, engines=None)
    except:
        subdomains = 0
    return subdomains