__author__ = 'timl'

from lxml import html
import requests
import time
import pymongo
from datetime import datetime, timedelta


# Connection to Mongo DB
try:
    conn = pymongo.MongoClient('localhost', 27017)
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e
   conn

#test
db = conn['test-database3']


start_time = time.time()

#gets new license times
def findNewTimes(tree):
    license = tree.xpath("string(//*[@id=\"ctl00_Main_waittime\"]/text()[2])")
    times = license.split(" ")
    hour = float(times[0])
    minute = float(times[2])
    time = hour * 60 + minute
    return time


#gets renewal times, current time
def findRenewTimes(tree):
    renew = tree.xpath("string(//*[@id=\"ctl00_Main_waittime\"])")
    times = renew.split(" ")



    #Finds the hour wait (RENEWALS)
    hour = times[17][18:]
    if hour.isdigit():
        realHour = float(times[17][18:])
    else:
        realHour = '0'

    realMinute = float(times[19])


    if realHour == '0':
        time = realMinute
    elif realHour == '1':
        time = 60 + realMinute
    elif realHour == '2':
        time = 120 + realMinute
    else:
        time = realMinute
    return time


def go():
    try:
        page = requests.get('https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=583&oid=24')
    except:
        print("http connection failed, trying https now")
        page = requests.get('https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=583&oid=24')
        print('{} ({})'.format(page.url, page.status_code))


    tree = html.fromstring(page.text)

    newWait = findNewTimes(tree)
    renewWait = findRenewTimes(tree)


    newLicense = {
        "DateTime": datetime.utcnow() + timedelta(hours=-7),
        "Location": "Seattle Downtown",
        "Wait Time": newWait
    }
    print('new license data:')
    print newLicense
    print('')

    renewLicense = {
        "DateTime": datetime.utcnow() + timedelta(hours=-7),
        "Location": "Seattle Downtown",
        "Wait Time": renewWait
    }
    print('renew license data:')
    print renewLicense
    print '________________________________'
    print '________________________________'
    print '________________________________'


    print("--- %s seconds ---" % (time.time() - start_time))
    time.sleep(60)

    db.timtext.today.insert({
        "New License Wait Time:": newWait,
        "License Renewal Wait Time:": renewWait,
        "Timestamp": datetime.utcnow() + timedelta(hours=-7)
    })


min = datetime.now().replace(hour=8, minute=30, second=0, microsecond=0)
max = datetime.now().replace(hour=16, minute=30, second=0, microsecond=0)


while True:
    curr = datetime.utcnow() + timedelta(hours=-7)
    while min < curr < max:
        go()
        curr = datetime.utcnow() + timedelta(hours=-7)
        print curr

    print curr
    print '________________________________'
    print("--- %s seconds ---" % (time.time() - start_time))
    time.sleep(60)
    min = datetime.now().replace(hour=8, minute=00, second=0, microsecond=0)
    max = datetime.now().replace(hour=17, minute=00, second=0, microsecond=0)