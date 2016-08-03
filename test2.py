import subprocess
import re

file1="user/taburaad/public/2gb_file.tar"

output = subprocess.Popen(["xrdfs", "root://data.ci-connect.net", "stat", file1], stdout=subprocess.PIPE).communicate()[0]
#output=subprocess.Popen(["echo", "hi"],stdout=subprocess.PIPE).communicate()[0]
line=re.findall(r"Size:   \d+",output)[0].split(":   ")[1]
#line=line.split(":   ")[1]



xrdargs="-d 2 --nopbar -f"
cache="root://data.ci-connect.net"
filename="user/taburaad/public/2gb_file.tar"
destination ="."
filepath=cache+":1094//"+ filename
print filepath

xrdcp=subprocess.Popen(['xrdcp ' + xrdargs + " " + filepath+' '+ destination ],shell=True)


