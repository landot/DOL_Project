__author__ = 'timl'

from lxml import html
import requests
import time
import pymongo
from datetime import datetime, timedelta

start_time = time.time()

# Connection to Mongo DB
try:
    conn = pymongo.MongoClient('localhost', 27017)
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e
   conn


db = conn['test-database4']



officeName = ['Bellevue/Bel-Red', 'Bellingham', 'Bremerton', 'Kennewick', 'Lacey', 'Lynnwood',
    'Mount Vernon', 'Parkland', 'Puyallup', 'Renton', 'Seattle: Downtown',
    'Seattle: West Seattle', 'Smokey Point', 'Spokane', 'Tacoma', 'Union Gap', 'Vancouver-North', 'Wenatchee']

officeWebAddress = ['https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=45&oid=23',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=46&oid=8',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=66&oid=9',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=315&oid=49',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=333&oid=5',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=371&oid=20',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=431&oid=12',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=495&oid=6',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=529&oid=34',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=542&oid=29',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=583&oid=24',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=583&oid=30',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=735&oid=21',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=619&oid=70',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=638&oid=36',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=668&oid=51',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=677&oid=40',
                    'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=703&oid=63'
                    ]

officeNameAll = ['Hoquiam','Kelso','Moses Lake','Port Angeles']

officeWebAddressAll = ['https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=289&oid=38',
                      'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=312&oid=42',
                      'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=428&oid=57',
                      'https://fortress.wa.gov/dol/dolprod/dsdoffices/OfficeInfo.aspx?cid=510&oid=14']


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


def go(name, address):
    try:
        page = requests.get(address)
        tree = html.fromstring(page.text)

    except:
        print("http connection failed, trying https now")
        page = requests.get(address)
        print('{} ({})'.format(page.url, page.status_code))


    newWait = findNewTimes(tree)
    renewWait = findRenewTimes(tree)

    print name

    newLicense = {
        "DateTime": datetime.utcnow() + timedelta(hours=-7),
        "Location": name,
        "Wait Time": newWait
    }
    print('new license data:')
    print newLicense
    print('')

    renewLicense = {
        "DateTime": datetime.utcnow() + timedelta(hours=-7),
        "Location": name,
        "Wait Time": renewWait
    }


    print('renew license data:')
    print renewLicense

    db.test.alldol.insert({
        "Location:": name,
        "New License Wait Time:": newWait,
        "License Renewal Wait Time:": renewWait,
        "Timestamp": datetime.utcnow() + timedelta(hours=-7)
    })
    print '________________________________'
    print('')

#general function that finds times of new license and renewal
def findTimes(nameList, webList):
    count = 0
    while count < len(nameList):
        name = nameList[count]
        address = webList[count]
        #do stuff
        go(name, address)
        count += 1

#special case for offices that have all services (different xpath)
def findTimesAll(nameList, webList):
    count = 0

    while count < len(nameList):
        name = nameList[count]
        address = webList[count]

        try:
            page = requests.get(address)
        except:
            print("http connection failed, trying https now")
            page = requests.get(address)
            print('{} ({})'.format(page.url, page.status_code))


        tree = html.fromstring(page.text)

        print name
        print('All Services data:')

        allWait = findNewTimes(tree)

        newLicense = {
            "DateTime": datetime.utcnow() + timedelta(hours=-7),
            "Location": name,
            "Wait Time": allWait
        }

        print newLicense

        db.test.alldol.insert({
            "Location:": name,
            "All Services Wait Time:": allWait,
            "Timestamp": datetime.utcnow() + timedelta(hours=-7)
        })
        print '________________________________'
        print('')
        count += 1


min = datetime.now().replace(hour=8, minute=00, second=0, microsecond=0)
max = datetime.now().replace(hour=17, minute=00, second=0, microsecond=0)


while True:
    curr = datetime.utcnow() + timedelta(hours=-7)
    while True and min < curr < max:
        runTime = time.time()
        findTimes(officeName, officeWebAddress)
        findTimesAll(officeNameAll, officeWebAddressAll)
        print("Run Time:")
        print("--- %s seconds ---" % (time.time() - runTime))
        print('')
        print("--- %s seconds ---" % (time.time() - start_time))
        time.sleep(50)
        curr = datetime.utcnow() + timedelta(hours=-7)
        print curr

    time.sleep(60)





