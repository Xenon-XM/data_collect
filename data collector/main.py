#!/usr/bin/python3.9
import argparse
import csv
import asyncio
import os
from saving.save import Download
import saving.screenshot as ss
import recon.fpdns_os as fp
from recon.who_is import whois_info
from recon.zdns import zdns_cmd
from scans.nmap_scan import NmapScanner
from scans.sslyze_scan import SSlyzeScanner
from web.wapp import wapp_analyze
from web.whatweb import whatweb
#from web.drupal import droop
from info.ranks import Ranking
from info.resolver_check import resolve_check
from info.ranks_glob import alexa_rank
from info.tld import TLD_info
from recon.metadata import keyword_search
from recon.shodan_check import Shodan_checker
from recon.maxmind import maxmind_info
from scans.safebrowsing import sf
from scans.virustotal import vt_api
from info.theharvester import harvest, harvest_emails, harvest_ips, harvest_people, harvest_hosts
from recon.sublister import search_subdomain_sli
from web.whatweb import whatweb
import logging

def collect(domain, ip_ns, ns, ranks_daily):
    logging.basicConfig(filename='/home/azureuser/domain_log', encoding='utf-8',  
        format='%(asctime)s %(levelname)s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('started testing: ' + str(domain) + ', ' + str(ns) + ', ' + str(ip_ns))
    #CHECK IF CORRECT SUBDOMAIN EXISTS
    subdomain_resolver=resolve_check(domain)
    #PART OF THE SCRIPT NEEDED TO RUN ON NEW SUBDOMAIN
    logging.info('getting screenshots')
#    task = Download(domain, subdomain_resolver)
 #   task.copy()
#    ss.shot(domain, subdomain_resolver)
    #INFO
    logging.info('info gathering')
    ranks=ranks_daily.check_domain_all(domain)
    alexa_global = alexa_rank(domain)
    logging.info('ranks - done')
    tld = TLD_info()
    tld.tld_extr(domain)
    logging.info('tld - done')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(harvest(domain))
    harv_emails = harvest_emails()
    harv_people = harvest_people()
    harv_hosts = harvest_hosts()
    harv_ips = harvest_ips()
    logging.info('theHarvester - done')
    #tld.lvl
    #tld.tld
    #RECON
    logging.info('recon')
    whois_information = whois_info(domain)
    logging.info('whois - done')
    server = fp.server_type(ip_ns)
    auth = fp.a_s(domain)
    logging.info('fpdns - done')
    records = zdns_cmd(domain, ip_ns)
    logging.info('zdns - done')
    metadata = keyword_search(domain)
    maxmind_i =maxmind_info(ip_ns) 
    maxmind_domain = list()
    try:
        if (len(records['A'])!=0):
            for ip_web in records['A']:
                maxmind_res = maxmind_info(ip_web)
                maxmind_res['asn'] = str(ip_web) +":" + str(maxmind_res['asn'])
                maxmind_domain.append(maxmind_res['asn'])
    except:
        records['A']=None
    logging.info('maxmind - done')
    sublis = search_subdomain_sli(domain)
    logging.info('sublist3r - done')
    shod = Shodan_checker()
    shod.check(ip_ns)
    logging.info('shodan - done')
    #SCANS
    logging.info('scanning')
    scanners = [NmapScanner()]#ZapScanner(), NexposeScanner(), OpenVASScanner()]
    for scanner in scanners:
        scanner.scan(ip_ns)
    logging.info('nmap - done')
    https_info = SSlyzeScanner()
    https_info.test(domain)
    logging.info('sslyze - done')
    safe_br=sf(domain, subdomain_resolver)
    logging.info('SafeBrowsing - done')
    virus=vt_api(domain)
    logging.info('VirusTotal - done')
    #WEB INFO
    logging.info('collecting web info')
    web_categories = wapp_analyze(domain)
    logging.info('wappalazer - done')
    web_info = whatweb(domain)
    logging.info('whatweb - done')
    with open('/home/azureuser/collect/results.csv', 'a', newline='',encoding='UTF8') as file:
        writer = csv.writer(file)
        data=[domain, ns, ip_ns, records['A'], records['AAAA'], tld.tld, tld.lvl, subdomain_resolver, whois_information.country, whois_information.city, auth,  maxmind_i['country'], maxmind_i['asn'],maxmind_domain, scanners[0].os,server, https_info.cert, https_info.num_certificates, https_info.issuer, whois_information.registrar, whois_information.email, whois_information.org, whois_information.creation, whois_information.exporation, ranks['alexa'], alexa_global, ranks['majestic'], ranks['umbrella'], ranks['tranco'], metadata, web_categories, web_info, records['MX'], records['NS'], records['DNSKEY'], records['DS'], records['KEY'], records['RRSIG'], records['TXT'], records['CNAME'], records['AXFR'], safe_br['domain'], safe_br['subdomain'], sublis, harv_emails, harv_people, harv_hosts, harv_ips, shod.banners, virus]
        writer.writerow(data)
    if ns=='None':
        ns=''
    with open('/home/azureuser/collect/domains_tested.txt', 'a') as outf:
        outf.write(domain+',' + ns + ','+ip_ns+'\n')
    logging.info('finished collecting for ' + domain+', ' + ns + ', '+ip_ns)
def main(config):
    ranks_daily = Ranking()
    csv_check = os.path.exists('/home/azureuser/collect/results.csv')
    if not csv_check:
        with open('/home/azureuser/collect/results.csv', 'w', newline='',encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow(["Domain","NS", "IP of NS", "IPv4(WEB)", "IPv6", "TLD", "Level of domain", "research.", "Country(WEB)", "City(WEB)", "IP address(NS)", "Country(NS)", "ASN(NS)", "ASN(WEB)", "OS", "Server", "SSL/TLS", "Num of cert-s", "CA",  "REG", "Whois email","Whois org", "Creation date", "Expiration date", "ALexa daily", "Alexa global", "Majestic", "Umbrella", "TRANCO", "Metadata", "Wappalazer", "WhatWeb", "MX", "NS", "DNSKEY", "DS", "KEY", "RRSIG", "TXT", "CNAME", "AXFR", "SafeBrowsing(domain)", "SafeBrowsing(subdomain)", "Sublist3r", "theharvester-emails", "theharvester-people", "theharvester-hosts", "theharvester-ips","Banners","VirustotalAPI"])
    if config['fname']:
        # Using readline()
        file1 = open(config['fname'], 'r')
        count = 0
        while True:
            count += 1
            # Get next line from file
            line = file1.readline().strip()
            # if line is empty
            # end of file is reached
            if not line:
                break
            if count%2==0:
                collect(prev_line, line, ranks_daily)
            prev_line = line
        file1.close()
    else:
        collect(config['domain'],config['address'], config["ns"], ranks_daily)
    return True
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', help='Specify a domain name')
    parser.add_argument('-i', '--ip',  help='Specify IP address of the name server')
    parser.add_argument('-f', '--file', help='Specify the name of the file with data')
    parser.add_argument('-ns', '--ns', help='Specify the name server', nargs='?', const='None')
    args = parser.parse_args()
    config = {
        'domain': args.domain,
        'address': args.ip,
        'ns': args.ns,
        'fname': args.file
    }
    
    main(config)

    exit(0)
