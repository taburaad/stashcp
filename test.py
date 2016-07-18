import subprocess
import threading
import time

def testing(input1):
    for i in range(5):
        print i
    time.sleep(5)
    print input1


xrdcp=subprocess.Popen(['./2.sh'],shell=True)
background=threading.Thread(target=testing,args=['hello'])
background.start()

print "hi"
stream=xrdcp.communicate()[0]
print xrdcp.returncode
