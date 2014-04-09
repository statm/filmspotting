import json
import urllib2
from bs4 import BeautifulSoup
import re
from urllib2 import URLError, urlopen, HTTPError
import gc
import os

data = []
counter = 0
def dump():
    f = open("movie_location_detail.json", "w+")
    f.write(json.dumps(data))
    f.close()

def char_range(c1, c2):
    for c in xrange(ord(c1), ord(c2)+1):
        yield chr(c)
        
def dlfile(url):
    try:
        f = urlopen(url)
        print "downloading " + url
        with open(os.path.basename(url), "wb") as local_file:
            local_file.write(f.read())
    except HTTPError, e:
        print "HTTP Error: ", e.code, url
    except URLError, e:
        print "URL Error: ", e.reason, url

def clean(url):
    if url.find("../../") != -1 or url.find("../") != -1:
        url = url[url.rfind("/")+1:]
    return url

def get_movie_list():
    result = []
    
    for i in char_range('a', 'z'):
        print "visiting movies starting with character " + i + "..."
        url = "http://www.movie-locations.com/movies/" + i + "/" + i + "movies.html"
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        entries = soup.select("b a")
        for entry in entries:
            temp = clean(entry.attrs["href"])
            temp = temp[0].lower() + "/" + temp
            result.append(temp)
    print "all movie ids from a to z collected."
    return result
    

    
def get_movie_info(movie_id):
    # basic info
    imdb_movie_url = "http://www.movie-locations.com/movies/" + movie_id
    page = urllib2.urlopen(url=imdb_movie_url, timeout=10)
    soup = BeautifulSoup(page)
      
    temp = soup.select("#details h1")[0].contents[0].strip()
    pos = temp.rfind(',')
    movie_name = temp[:pos+1]
    movie_year = temp[pos+1:]
            
    #image info
    location_images = []
    for detail in soup.select("#maintext #illust"):
        location = detail.find("img")
        temp = clean(location.attrs["src"])
        location_img_url = "http://www.movie-locations.com/movies/" + temp[0] +"/"+ temp
        location_img_desc = detail.find("p").text
        location_images.append({"location_img_url" : location_img_url,
        "location_img_desc" : location_img_desc})
    
    #text info
    locations = []
    for location in soup.select("#maintext .name"):
        locations.append(location.contents[0].strip())
    
    # return an object containing all data above
    return {
            "id":counter,
            "name":movie_name,
            "year":movie_year,
            "location_images":location_images,
            "locations": locations}
    

if __name__ == '__main__':
    #temp = open("movieLocation_data.json");
    movie_list = get_movie_list()
    #movie_list = json.load(temp)
    error_id = []
        
    for movie_id in movie_list:
        counter += 1
        print "visiting movie  " + str(counter)+ ": " + movie_id
        try:
            data.append(get_movie_info(movie_id))
        except IndexError, URLError:
            print "error occured at " + movie_id
            error_id.append(movie_id)
        except:
            print "error occured at "+ movie_id
            error_id.append(movie_id)
    dump()
    print error_id
