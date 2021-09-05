import os
import json
import demjson
ZDNS_CMD = "echo '{}' | /home/azureuser/collect/recon/zdns/zdns/zdns {} -name-servers={} -result-verbosity short -output-file /home/azureuser/collect/temp.out"

def jsonhandle(type, dns_records):
    
    input_file  = open('/home/azureuser/collect/temp.out',"r")
    ##output_file = open("output/" + domain +".txt", "a+")
    for line in input_file:
        try:
            js = demjson.decode(line)
            #domain = js['name']
            #ip = 'NULL'
            if js['status'] == 'NOERROR':
                try:
                    answers = js['data']['answers']
                    for answer in answers:
                        key = answer['type']
                        value = answer['answer']
                        if key not in dns_records:
                            dns_records[key] = list()
                        dns_records[key].append(value)
                except KeyError as ke:
                    print('No DNS record found:', type)
                    dns_records[type] = 'None'
            else:
                dns_records[type] = 'None'
        except:
            dns_records[type] = 'None'
                    #print(name + " " + ip + "\n")
            #answers2 = js['data']['additionals']
            #for answer in answers2:
            #    if answer['type'] == 'A':
            #        name = answer['name']
            #        ip = answer['answer']
            #        output_file.write(name + " " + ip + "\n")
    input_file.close()
    #output_file.close()            

def zdns_cmd(domain, ip):
    dns_records=dict()
    dns_records['AAAA']=None
    dns_records['CNAME']=None
    dns_records['DNSKEY']=None
    dns_records['DS']=None
    dns_records['KEY']=None
    dns_records['MX']=None
    dns_records['NS']=None
    dns_records['RRSIG']=None
    dns_records['TXT']=None
    dns_records['AXFR']=None
    print("DNS lookup:")
    cmd_A = ZDNS_CMD.format(domain, 'A',  ip)
    cmd_AAAA = ZDNS_CMD.format(domain, 'AAAA',  ip)
    cmd_CNAME = ZDNS_CMD.format(domain, 'CNAME',  ip)
    cmd_DNSKEY = ZDNS_CMD.format(domain, 'DNSKEY',  ip)
    cmd_DS = ZDNS_CMD.format(domain, 'DS',  ip)
    cmd_KEY = ZDNS_CMD.format(domain, 'KEY',  ip)
    cmd_MX = ZDNS_CMD.format(domain, 'MX',  ip)
    cmd_NS = ZDNS_CMD.format(domain, 'NS',  ip)
    cmd_RRSIG = ZDNS_CMD.format(domain, 'RRSIG',  ip)
    cmd_TXT = ZDNS_CMD.format(domain, 'TXT',  ip)
    cmd_AXFR = ZDNS_CMD.format(domain, 'AXFR',  ip)

    os.system(cmd_A)
    jsonhandle('A',dns_records)
    os.system(cmd_AAAA)
    jsonhandle('AAAA',dns_records)
    os.system(cmd_CNAME)
    jsonhandle('CNAME',dns_records)
    os.system(cmd_DNSKEY)
    jsonhandle('DNSKEY',dns_records)
    os.system(cmd_DS)
    jsonhandle('DS',dns_records)
    os.system(cmd_KEY)
    jsonhandle('KEY',dns_records)
    os.system(cmd_MX)
    jsonhandle('MX',dns_records)
    os.system(cmd_NS)
    jsonhandle('NS',dns_records)
    os.system(cmd_RRSIG)
    jsonhandle('RRSIG',dns_records)
    os.system(cmd_TXT)
    jsonhandle('TXT',dns_records)
    os.system(cmd_AXFR)
    jsonhandle('AXFR',dns_records)
    os.remove('/home/azureuser/collect/temp.out')
    return dns_records
