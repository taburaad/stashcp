#!/usr/bin/env python
import subprocess, threading, os, sys, time
import urllib2
import datetime
import math

try: import simplejson as json
except ImportError: import json


import socket

debug=1
if len(sys.argv)>1:
	try:
		debug=int(sys.argv[1])
	except ValueError:
		print '# unknown argument. The only accepted argument is an integer number representing debug level.'
		sys.exit(-1)

if debug: print "# getting client coordinates..."

worked=0
try:
    req = urllib2.Request("http://geoip.mwt2.org:4288/json/", None)
    opener = urllib2.build_opener()
    f = opener.open(req,timeout=5)
    res=json.load(f)
    lon=res['longitude']
    lat=res['latitude']
    ip=res['ip']
    worked=1
except:
    if debug:
        print "# Can't determine client coordinates using geoip.mwt2.org ", sys.exc_info()[0]

if not worked:
    try:
        req = urllib2.Request("http://freegeoip.net/json/", None)
        opener = urllib2.build_opener()
        f = opener.open(req,timeout=5)
        res=json.load(f)
        lon=res['longitude']
        lat=res['latitude']
    except:
        print "# Can't determine client coordinates using freegeoip.net ", sys.exc_info()[0]
        sys.exit(1)



n = datetime.datetime.utcnow()
one_day = datetime.timedelta(days=1)
n = n + one_day
t = n + one_day
today = datetime.datetime.date(n)
tomorrow = datetime.datetime.date(t)

class site:
    def __init__(self,na):
        self.name=na
        self.status=0
        self.longitude=0
        self.latitude=0
    def coo(self, lo, la):
	self.longitude=lo
	self.latitude=la
    def prn(self):
        print "#", self.name, "\tlong:",self.longitude,"\t lat:",self.latitude,"\tstatus:",self.status

Sites=dict()
worked=0
try:
    url="https://raw.githubusercontent.com/opensciencegrid/StashCache/master/bin/caches.json"
    if debug: print "# getting StashCache endpoints coordinates and statuses from GitHub ..."
    response=urllib2.Request(url,None)
    opener = urllib2.build_opener()
    f = opener.open(response, timeout=40)
    data = json.load(f)
    for si in data:
        n=si['name']
        s=site(n)
        s.status=si['status']
        s.coo(si['longitude'],si['latitude'])
        #s.prn()
        Sites[n]=s
    worked=1
except urllib2.HTTPError:
	if debug: print "# Can't connect to GitHub."
except:
    if debug: print "# Can't connect to GitHub.", sys.exc_info()[0]


# calculating distances to "green" endpoints
mindist=40000
minsite=''

for s in Sites:
    if not Sites[s].status==1: continue
    dlon = math.radians(lon - Sites[s].longitude)
    dlat = math.radians(lat - Sites[s].latitude)
    a = pow(math.sin(dlat/2),2) + math.cos(math.radians(Sites[s].latitude)) * math.cos(math.radians(lat)) * pow(math.sin(dlon/2),2)
    c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a) )
    d = 6373 * c # 6373 is the radius of the Earth in km
    if debug>1:
        Sites[s].prn()
        print "#",d,"km"
    if d<mindist:
        mindist=d
        minsite=Sites[s].name


if debug:
    print "#",minsite, mindist,"km"

print minsite[:-1]
