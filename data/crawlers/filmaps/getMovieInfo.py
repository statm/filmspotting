# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import re
from urllib2 import URLError, urlopen, HTTPError
import gc
import os
import json
from collections import OrderedDict

data = []
counter = 0
def dump():
    f = open("movie_location.json", "w+")
    f.write(json.dumps(data))
    f.close()

def get_movie_info(movie_url):
    # basic info
    
    page = urllib2.urlopen(url=movie_url, timeout=10)
    soup = BeautifulSoup(page)

    movie_name = soup.select("#citypromo div h2")[0].text
    geocoding = []
    locations = []
    scriptResults = soup('script', {'type': 'text/javascript'})
    for script in scriptResults:
        for block in script:
            pos = block.find("var map = new google.maps.Map")
            if pos != -1:
                blob = block[pos:]
                for str in blob.split(";"):
                    if str.find("title:") != -1:
                        locations.append(str[str.index('title:')+6:str.rfind('}')].encode('utf8').strip())
                    if str.find("var coordenadas = new google.maps.LatLng") != -1:
                        geocoding.append(str[str.index('('):str.find('}')]+')')
    desc = []
    for item in soup.select("#moviecities2 .item ul li"):
        desc.append(item.text)
    if len(locations) > 0:
        info = []
        for idx in xrange(len(geocoding)):
            info.append({
                        "location": locations[idx],
                        "description": desc[idx],
                        "geocoding": geocoding[idx]})
        print info
        # return an object containing all data above
        return {
                "id":counter,
                "name":movie_name,
                "locations": info}
    else:
        return
if __name__ == '__main__':
    movie_list = json.load(open("movie_ids.json"))
    error_id = []
        
    for movie_url in movie_list:
        counter += 1
        print "---->visiting" + str(counter) + " : " + movie_url.encode('utf8')
        try:
            data.append(get_movie_info(movie_url.replace("\t", "")))
        except IndexError, URLError:
            print "error occured at " + movie_url.encode('utf8')
            error_id.append(movie_url)
        except:
            print "error occured at "+ movie_url.encode('utf8')
            error_id.append(movie_url)
    dump()
    print error_id