import os
import demjson
import json
import subprocess
#WHATWEB_CMD = "whatweb -a 1 --log-json=/home/azureuser/collect/out.json {}"

def whatweb(domain):
    url = domain
    try:
        subprocess.run(["whatweb", "-a", "1", "--log-json=/home/azureuser/collect/out.json", url], check = True, stdout=None)
    except:
        return 0
    with open('/home/azureuser/collect/out.json', 'r') as fh:
        atext = fh.read().replace('[\n',' ')
        atext = atext.replace(']\n',' ')
    if (atext.find(',\n') != -1):
        atext = atext.split(',\n')
        result = atext[1].replace('\n',' ')
    else:
        result = atext.replace('\n',' ')
    ##output_file = open("output/" + domain +".txt", "a+")
    os.remove('/home/azureuser/collect/out.json')
    return result
