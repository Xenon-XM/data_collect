import os 
from subprocess import check_output
#amass takes longer than the whole program
def amass_run(domain):
    out = check_output(["amass","intel","-whois","-d",domain])
    sout= out.decode("utf-8")
    sout = sout.replace(" ","")
    sout = sout.replace("\n",",")
    return sout