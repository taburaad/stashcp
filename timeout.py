import argparse
import os
import time
import subprocess
import sys


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-t', dest='timeout', type=int)
parser.add_argument('-f', dest='filename')
parser.add_argument('-d', dest='diff', type=int)
parser.add_argument('-s', dest='expSize', type=int)
results = parser.parse_args()

def start_watchdog(xrdpid,timeout=results.timeout,filename=results.filename,diff=results.diff,expSize=results.expSize):
    prevSize=0
    newSize=0
    while (newSize<expSize):
        time.sleep(timeout)
        if os.path.isfile(filename):
            newSize=os.stat(filename).st_size
            nextSize=prevSize+diff
            if nextSize<expSize:
                wantSize=nextSize
            else:
                wantSize=expSize
            if newSize > wantSize:
                print 'kill'
                os.killpg(os.getpgid(xrdcp.pid), signal.SIGTERM)
            else:
                prevSize=os.stat(filename).st_size
        else:
            print "did not start"
            xrdcp.terminate()

xrdcp=subprocess.Popen(['./2.sh &'],stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

start_watchdog(xrdpid=xrdcp.pid)
print "done"
