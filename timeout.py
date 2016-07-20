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
results = parser.parse_args()

def start_watchdog(xrdcp,timeout=results.timeout,filename=results.filename,diff=results.diff,expSize=results.expSize):
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
            if newSize < wantSize:
                xrdcp.kill()
                newSize=expSize
                return "killed"
            else:
                prevSize=os.stat(filename).st_size
        else:
            xrdcp.kill()
            newSize=expSize
            return "did not start"

xrdcp=subprocess.Popen(['./2.sh'],shell=True)

watchdog=multiprocessing.Process(target=start_watchdog,args=[xrdcp])
watchdog.start()

print "watchdog started, stream now"
streamdata=xrdcp.communicate()[0]

xrd_exit=xrdcp.returncode
print "xrdcp exit code: ", xrd_exit

print watchdog, watchdog.is_alive()
watchdog.terminate()
time.sleep(1)
print watchdog, watchdog.is_alive()
print "done"
