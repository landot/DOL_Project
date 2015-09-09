__author__ = 'timl'

from lxml import html
import requests
import time
import pymongo
from datetime import datetime, timedelta


min = datetime.now().replace(hour=10, minute=50, second=0, microsecond=0)
max = datetime.now().replace(hour=10, minute=52, second=0, microsecond=0)

min2 = datetime.now().replace(hour=10, minute=57, second=0, microsecond=0)
max2 = datetime.now().replace(hour=10, minute=59, second=0, microsecond=0)

curr = datetime.utcnow() + timedelta(hours=-7)

while True:
    curr = datetime.utcnow() + timedelta(hours=-7)
    while True and min < curr < max or min2 < curr < max2:
        print('it worked')
        curr = datetime.utcnow() + timedelta(hours=-7)
        print curr
        time.sleep(1)
    print '________________________________'
    time.sleep(5)
    print curr

