import argparse
import sys
import subprocess
import datetime
import time
import re
import os
import json
import requests
import multiprocessing


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

TIMEOUT = 60
DIFF = TIMEOUT * 10
#load=subprocess.Popen(['module load xrootd/4.2.1'],stdout=subprocess.PIPE,shell=True)


def doStashCpSingle(sourceFile=args.source, destination=args.destination):
    xrdfs = subprocess.Popen(["xrdfs", "root://data.ci-connect.net", "stat", sourceFile], stdout=subprocess.PIPE).communicate()[0]
    fileSize=re.findall(r"Size:   \d+",xrdfs)[0].split(":   ")[1]
    fileSize=int(fileSize)
    cache=find_closest()
    command = "python ./timeout.py -t "+str(TIMEOUT)+ " -f "+sourceFile + " -d "+str(DIFF)+" -s "+str(fileSize)+" -x "+str(xrdargs)+" -c "+cache+" -z "+destination
    date=datetime.datetime.now()
    start1=int(time.mktime(date.timetuple()))
    copy=subprocess.Popen([command],stdout=subprocess.PIPE,shell=True)
    xrd_exit=copy.communicate()[0].split()[-1]
    date=datetime.datetime.now()
    end1=int(time.mktime(date.timetuple()))
    filename=destination+'/'+sourceFile.split('/')[-1]
    dlSz=os.stat(filename).st_size
    destSpace=1000
    sitename='inProgress'
    xrdcp_version="4.2.1"
    start2=0
    start3=0
    end2=0
    xrdexit2=-1
    xrdexit3=-1
    if xrd_exit=='0': #worked first try
        dltime=end1-start1
        status = 'Success'
        tries=1
        payload="{ \"timestamp\" : %d, \"host\" : '%s', \"filename\" : '%s', \"filesize\" : %d, \"download_size\" : %d, \"download_time\" : %d,  \"sitename\" : '%s', \"destination_space\" : %d, \"status\" : '%s', \"xrdexit1\" : %s, \"xrdexit2\" : %d, \"xrdexit3\" : %d, \"tries\" : %d, \"xrdcp_version\" : '%s', \"start1\" : %d, \"end1\" : %d, \"start2\" : %d, \"end2\" : %d, \"start3\" : %d, \"cache\" : '%s'}" % (end1, cache, sourceFile, fileSize, dlSz, dltime, sitename, destSpace, status, xrd_exit, xrdexit2, xrdexit3, tries, xrdcp_version, start1, end1, start2, end2, start3, cache)
        payload=payload.replace("'", '"')
        payload=payload.replace('"{', "'{")
        payload=payload.replace('}"', "}'")
        p = multiprocessing.Process(target=es_send, name="es_send", args=(payload,))
        p.start()
        time.sleep(5)
        p.terminate()
        p.join()
    else: #copy again using same cache
        print "1st try failed on %s, trying again" % cache
        date=datetime.datetime.now()
        start2=int(time.mktime(date.timetuple()))    
        copy=subprocess.Popen([command],stdout=subprocess.PIPE,shell=True)
        xrd_exit=copy.communicate()[0].split()[-1]
        date=datetime.datetime.now()
        end2=int(time.mktime(date.timetuple()))
        dlSz=os.stat(filename).st_size
        if xrd_exit=='0': #worked second try
            status = 'Success'
            tries=2
            dltime=end2-start2
            payload="{ \"timestamp\" : %d, \"host\" : '%s', \"filename\" : '%s', \"filesize\" : %d, \"download_size\" : %d, \"download_time\" : %d,  \"sitename\" : '%s', \"destination_space\" : %d, \"status\" : '%s', \"xrdexit1\" : %s, \"xrdexit2\" : %d, \"xrdexit3\" : %d, \"tries\" : %d, \"xrdcp_version\" : '%s', \"start1\" : %d, \"end1\" : %d, \"start2\" : %d, \"end2\" : %d, \"start3\" : %d, \"cache\" : '%s'}" % (end2, cache, sourceFile, fileSize, dlSz, dltime, sitename, destSpace, status, xrd_exit, xrdexit2, xrdexit3, tries, xrdcp_version, start1, end1, start2, end2, start3, cache)
            payload=payload.replace("'", '"')
            payload=payload.replace('"{', "'{")
            payload=payload.replace('}"', "}'")
            p = multiprocessing.Process(target=es_send, name="es_send", args=(payload,))
            p.start()
            time.sleep(5)
            p.terminate()
            p.join()
        else: #pull from origin
            print "2nd try failed on %s, pulling from origin" % cache
            cache="root://data.ci-connect.net"
            command = "python ./timeout.py -t "+str(TIMEOUT)+ " -f "+sourceFile + " -d "+str(DIFF)+" -s "+str(fileSize)+" -x "+str(xrdargs)+" -c "+cache+" -z "+destination
            date=datetime.datetime.now()
            start3=int(time.mktime(date.timetuple()))    
            copy=subprocess.Popen([command],stdout=subprocess.PIPE,shell=True)
            xrd_exit=copy.communicate()[0].split()[-1]
            date=datetime.datetime.now()
            end3=int(time.mktime(date.timetuple()))
            dlSz=os.stat(filename).st_size
            dltime=end3-start3
            if xrd_exit=='0':
                print "Trunk Success"
                status = 'Trunk Sucess'
                tries=3
            else:
                print "stashcp failed"
                status = 'Timeout'
                tries = 3
            payload="{ \"timestamp\" : %d, \"host\" : '%s', \"filename\" : '%s', \"filesize\" : %d, \"download_size\" : %d, \"download_time\" : %d,  \"sitename\" : '%s', \"destination_space\" : %d, \"status\" : '%s', \"xrdexit1\" : %s, \"xrdexit2\" : %d, \"xrdexit3\" : %d, \"tries\" : %d, \"xrdcp_version\" : '%s', \"start1\" : %d, \"end1\" : %d, \"start2\" : %d, \"end2\" : %d, \"start3\" : %d, \"cache\" : '%s'}" % (end3, cache, sourceFile, fileSize, dlSz, dltime, sitename, destSpace, status, xrd_exit, xrdexit2, xrdexit3, tries, xrdcp_version, start1, end1, start2, end2, start3, cache)
            payload=payload.replace("'", '"')
            payload=payload.replace('"{', "'{")
            payload=payload.replace('}"', "}'")
            p = multiprocessing.Process(target=es_send, name="es_send", args=(payload,))
            p.start()
            time.sleep(5)
            p.terminate()
            p.join()





def es_send(payload):
        url = "http://uct2-int.mwt2.org:9951"
        payload = payload
        res = requests.post(url, data=payload)

doStashCpSingle()
