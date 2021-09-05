import os 
from subprocess import check_output

def server_type(server_ip):
    try:
        out = check_output(["fpdns", "-s", server_ip])
        sout= out.decode("utf-8")
        sout = sout.replace(server_ip,"")
        sout = sout.replace(" ","")
    except:
        sout = 0
    return sout
def a_s(domain):
    servers=list()
    try:
        out = check_output(["fpdns", "-D", domain])
        sout= out.decode("utf-8")
        i = sout.find("(")
        while i!=-1:
            start = i + 1
            end = sout.find(")")
            substring = sout[start:end]
            sout = sout[end+1::]
            substring = substring.replace(domain,"")
            substring = substring.replace(" ","")
            substring = substring.replace(",","")
            servers.append(substring)
            i = sout.find("(", i+1)
    except:
        pass    
    return servers