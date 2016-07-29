import argparse
import os
import time
import subprocess
import multiprocessing


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-t', dest='timeout', type=int)
parser.add_argument('-f', dest='filename')
parser.add_argument('-d', dest='diff', type=int)
parser.add_argument('-s', dest='expSize', type=int)
parser.add_argument('-x', dest='xrdebug')
parser.add_argument('-c', dest='cache')
parser.add_argument('-z', dest='destination')
results = parser.parse_args()

def start_watchdog(xrdcp,timeout=results.timeout,filename=results.filename,diff=results.diff,expSize=results.expSize):
    prevSize=0
    newSize=0
    filename="./"+filename.split("/")[-1]
    print "filename is: "+filename
    while (newSize<expSize):
        print "sleep"
        time.sleep(timeout)
        if os.path.isfile(filename):
            newSize=os.stat(filename).st_size
            print "size: "+str(newSize)
            nextSize=prevSize+diff
            if nextSize<expSize:
                wantSize=nextSize
            else:
                wantSize=expSize
            if newSize < wantSize:
                xrdcp.kill()
                newSize=expSize
                print "killed"
            else:
                prevSize=os.stat(filename).st_size
                print "prev size: ",prevSize
        else:
            xrdcp.kill()
            newSize=expSize
            print "did not start"
print results.xrdebug
filepath=results.cache+":1094//"+ results.filename
if results.xrdebug=="1":
    command="xrdcp -d 2 --nopbar -f " + filepath + " " + results.destination
else:
    command="xrdcp -s -f " + filepath + " " + results.destination

print command
filename="./"+results.filename.split("/")[-1]
print filename
if os.path.isfile(filename):
    os.remove(filename)
xrdcp=subprocess.Popen([command ],shell=True,stdout=subprocess.PIPE)
time.sleep(1)
watchdog=multiprocessing.Process(target=start_watchdog,args=[xrdcp])
watchdog.start()

#print "watchdog started, stream now"
streamdata=xrdcp.communicate()[0]

xrd_exit=xrdcp.returncode
print "xrdcp exit code: ", xrd_exit

#print watchdog, watchdog.is_alive()
watchdog.terminate()
#time.sleep(1)
#print watchdog, watchdog.is_alive()
#print "done"
