# get the id list of movies in movie_location website
import json
import urllib2
from bs4 import BeautifulSoup
import re
from urllib2 import URLError, urlopen, HTTPError
from collections import OrderedDict

def dump(data):
    f = open("movie_ids.json", "w+")
    f.write(json.dumps(data))
    f.close()
    
def clean(url, special):
    if special and url.find("../../") == -1 and url.find("../") == -1:
        url = "movies/0/" + url
    elif url.find("../../") == -1 and url.find("../") == -1:
        url = "movies/" + url[0].lower() + "/" + url
    elif url.find("../../") != -1:
        url = url[url.find("../../")+5:]
    elif url.find("../") != -1:
        url = "movies/" + url[url.find("../")+3:]
    return url
    
if __name__ == '__main__':
    result = []
    catgr_url = "http://www.movie-locations.com/films.html"
    page = urllib2.urlopen(url=catgr_url, timeout=10)
    soup = BeautifulSoup(page)
    entries = soup.select("#maintext table p2 a")
    for entry in entries:
        url = "http://www.movie-locations.com/" + entry.attrs['href']
        print "visiting movies in " + entry.attrs['href'] + "..."
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        if entry.attrs['href'] == "movies/0/0movies.html":
            items = soup.select("td font strong a")
            special = True
        else:
            items = soup.select("b a")
            special = False
        for item in items:
            temp = clean(item.attrs["href"], special)
            result.append(temp)
    result = list(OrderedDict.fromkeys(result))
    print "all movie ids from a to z collected."
    dump(result)