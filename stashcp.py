import argparse
import sys
import subprocess
import datetime
import time
import re
import os



parser = argparse.ArgumentParser(description = 'stashcp')
parser.add_argument('--debug', action='store_true', help='debug')
parser.add_argument('-r', action='store_true', help='recursively copy')
parser.add_argument('-s', dest='source', help='source')
parser.add_argument('-d', dest='destination', help='destination')
parser.add_argument('--closest', action='store_true')
args=parser.parse_args()

def find_closest():
    closest=subprocess.Popen(['./get_best_stashcache.py', '0'], stdout=subprocess.PIPE)
    cache=closest.communicate()[0].split()[0]
    return cache

if not args.closest:
    if args.source is None or args.destination is None:
        parser.error('without --closest, *both* -s source *and* -d destination are required')
else:
    print find_closest()
    sys.exit()

if not args.debug:
    xrdargs=0
else:
    xrdargs=1

TIMEOUT = 1
DIFF = TIMEOUT * 10
load=subprocess.Popen(['module load xrootd/4.2.1'],stdout=subprocess.PIPE,shell=True)





def doStashCpSingle(sourceFile=args.source, destination=args.destination):
    output = subprocess.Popen(["xrdfs", "root://data.ci-connect.net", "stat", sourceFile], stdout=subprocess.PIPE).communicate()[0]
    fileSize=re.findall(r"Size:   \d+",output)[0].split(":   ")[1]
    cache=find_closest()
    command = "python ./timeout.py -t "+str(TIMEOUT)+ " -f "+sourceFile + " -d "+str(DIFF)+" -s "+fileSize+" -x "+str(xrdargs)+" -c "+cache+" -z "+destination
    date=datetime.datetime.now()
    start1=int(time.mktime(date.timetuple()))
    copy=subprocess.Popen([command],stdout=subprocess.PIPE,shell=True)
    xrd_exit=copy.communicate()[0].split()[-1]
    date=datetime.datetime.now()
    end1=int(time.mktime(date.timetuple()))
    dltime=end1-start1
    filename=destination+'/'+sourceFile.split('/')[-1]
    print filename
    dlSz=os.stat(filename).st_size
    print dlSz
    #payload="{ \"timestamp\" : ${timestamp}, \"host\" : \"${hn}\"

    print "xrdcp exit code: ",xrd_exit
    print cache
    print fileSize
    print 'start: ',start1
    print 'end: ',end1


doStashCpSingle()

