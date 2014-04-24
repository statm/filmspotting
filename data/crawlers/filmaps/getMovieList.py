# -*- coding: utf-8 -*-

import json
import urllib2
from bs4 import BeautifulSoup
import re
from urllib2 import URLError, urlopen, HTTPError
from collections import OrderedDict

counter = 0
def dump(data):
    f = open("movie_ids.json", "w+")
    f.write(json.dumps(data))
    f.close()
    
if __name__ == '__main__':
    result = []
    catgr_url = "http://www.filmaps.com/results.php?r=&c=f&lang=en"
    page = urllib2.urlopen(url=catgr_url, timeout=10)
    soup = BeautifulSoup(page)
    entries = soup.select("#itemresults #details a")
    for index in xrange(0, len(entries), 2):
        url = entries[index].attrs['href'].encode('utf8')
        result.append(url)
        print url
        counter += 1
    print "all movie ids from a to z collected."
    print counter
    dump(result)