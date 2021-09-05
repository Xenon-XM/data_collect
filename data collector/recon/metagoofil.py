import os

METAGOOFIL_CMD = "metagoofil -d {} -t doc,pdf"

url = "http://salaryforall.com"

cmd = METAGOOFIL_CMD.format(url)

os.system(cmd)