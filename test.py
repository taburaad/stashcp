import subprocess
import multiprocessing
import time

def testing(input1):
    for i in range(5):
        print i
    time.sleep(5)
    print input1


xrdcp=subprocess.Popen(['./2.sh'],shell=True)
background=multiprocessing.Process(target=testing,args=['hello'])
background.start()

print "hi"
stream=xrdcp.communicate()[0]
print xrdcp.returncode
print background, background.is_alive()
background.terminate()
time.sleep(2)
print background, background.is_alive()
