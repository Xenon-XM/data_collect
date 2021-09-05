from sanic import Sanic
from sanic.response import json, text
from sanic.exceptions import NotFound
from sanic.exceptions import ServerError
import re
import tldextract

from collections import OrderedDict
from urllib.request import urlopen

import os
import urllib
import zipfile


#ALEXA
# download the file
f = open('/home/azureuser/collect/top-1m.zip', 'wb')
try:
    file = urlopen('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip').read()
    f.write(file)

# unzip it
    zip = zipfile.ZipFile(r'/home/azureuser/collect/top-1m.zip')
    zip.extractall('/home/azureuser/collect/')
    os.rename('/home/azureuser/collect/top-1m.csv','/home/azureuser/collect/top-1m-alexa.csv') 
except:
    pass
f.close()
#UMBRELLA
f = open('/home/azureuser/collect/top-1m-umb.zip', 'wb')
try:
    file = urlopen('http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip').read()
    f.write(file)
# unzip it
    zip = zipfile.ZipFile(r'/home/azureuser/collect/top-1m-umb.zip')
    zip.extractall('/home/azureuser/collect/')
    os.rename('/home/azureuser/collect/top-1m.csv','/home/azureuser/collect/top-1m-umb.csv') 
except:
    pass
f.close()

#TRANCO
f = open('/home/azureuser/collect/top-1m-tr.csv', 'wb')
try:
    file = urlopen('https://tranco-list.eu/download/ZLVG/1000000').read()
    f.write(file)
except:
    pass
f.close()

#MAJESTIC
f = open('/home/azureuser/collect/top-1m-maj.csv', 'wb')
try:
    file = urlopen('https://downloads.majestic.com/majestic_million.csv').read()
    f.write(file)
except:
    pass
f.close()

if os.path.exists('/home/azureuser/collect/top-1m-umb.zip'):
    os.remove('/home/azureuser/collect/top-1m-umb.zip') 
if os.path.exists('/home/azureuser/collect/top-1m.zip'):
    os.remove('/home/azureuser/collect/top-1m.zip') 

