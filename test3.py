import subprocess

xrdargs="-d 2 --nopbar -f"
fileSize=100
cache="root://data.ci-connect.net"

cp=subprocess.Popen(['python ./timeout.py -t 2 -f user/taburaad/public/2gb_file.tar -d 5 -s fileSize'],stdout=subprocess.PIPE,shell=True)

