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

z=dict()
class Ranking:
    def  __init__(self):
        alexa_file = open("/home/azureuser/collect/top-1m-alexa.csv").readlines()
        self.alexa_ranking = dict([(a,b) for b,a in re.findall(r"^(\d+),(\S+)", "".join(alexa_file), re.MULTILINE)])
        umbrella_file = open("/home/azureuser/collect/top-1m-umb.csv").readlines()
        self.umbrella_ranking = dict([(a,b) for b,a in re.findall(r"^(\d+),(\S+)", "".join(umbrella_file), re.MULTILINE)])
        tranco_file = open("/home/azureuser/collect/top-1m-tr.csv").readlines()
        self.tranco_ranking = dict([(a,b) for b,a in re.findall(r"^(\d+),(\S+)", "".join(tranco_file), re.MULTILINE)])
        maj_file = open("/home/azureuser/collect/top-1m-maj.csv").readlines()
        self.maj_ranking = dict([(a,b) for b,a in re.findall(r"^(\d+),(\S+)", "".join(maj_file), re.MULTILINE)])

#This helper function will strip the domain to the root and return that piece.
    def split_domain(self):
        parts = tldextract.extract(self.domain)
        self.domain = parts.domain + "." + parts.suffix

    def check_domain_all(self, domain):
        self.domain = domain
        self.split_domain
        domain = self.domain
        try:
            z['umbrella'] = self.umbrella_ranking.get(domain, -1)
            z['tranco']=self.tranco_ranking.get(domain, -1)
            z['majestic']=self.maj_ranking.get(domain, -1)
            z['alexa'] =  self.alexa_ranking.get(domain, -1)

        except:
            z['umbrella'] = -1
            z['alexa'] = -1
            z['tranco'] = -1
            z['majestic'] = -1
        return z

    
