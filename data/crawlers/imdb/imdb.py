import _socket
import json
import os
import re
import sys
from urllib2 import URLError, urlopen, HTTPError
import urllib2

from bs4 import BeautifulSoup


counter = 0
data = []

def dump_data():
    f = open("imdb_data.json", "w+")
    f.write(json.dumps(data))
    f.close()
    
def log_error(errorData):
    f = open("error.txt", "w+")
    f.write(errorData)
    f.close()
    
def get_top1000_list():
    result = []
    
    for i in xrange(0, 10):
        print "visiting top1000 page " + str(i) + "..."
        index = i * 100 + 1
        url = "http://www.imdb.com/search/title?at=0&groups=top_1000&sort=user_rating,desc&start=" + str(index) + "&view=simple"
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        entries = soup.select(".title a")
        for entry in entries:
            movie_id = re.search("\/title\/(tt\d{7})\/", entry.attrs["href"]).group(1)
            result.append(movie_id)
            
    print "top 1000 movie ids collected."
    return result

def save_movie_img(movie_id, img_url):
    try:
        f = urlopen(img_url)
        with open(os.path.dirname(__file__) + "\\images\\" + movie_id + ".jpg", "wb") as local_file:
            local_file.write(f.read())
    except HTTPError, e:
        print "HTTP Error: ", e.code, img_url
    except URLError, e:
        print "URL Error: ", e.reason, img_url

def get_movie_info(movie_id):
    # basic info
    imdb_movie_url = "http://www.imdb.com/title/" + movie_id + "/"
    page = urllib2.urlopen(url=imdb_movie_url, timeout=10)
    soup = BeautifulSoup(page)
    
    movie_img_url = soup.select(".image img")[0].attrs["src"].strip()
    save_movie_img(movie_id, movie_img_url)
    
    movie_name = soup.select(".header .itemprop")[0].contents[0].strip()
    movie_year = soup.select(".header .nobr a")[0].contents[0].strip()
    movie_rate = soup.select(".star-box-giga-star")[0].contents[0].strip()
      
    movie_genres = []
    
    for genre in soup.findAll("span", attrs={"itemprop" : "genre"}):
        movie_genres.append(genre.contents[0].strip())
            
    movie_description = soup.findAll(attrs={"itemprop" : "description"})[0].contents[0].strip()
            
    # location info
    imdb_movie_loc_url = "http://www.imdb.com/title/" + movie_id + "/locations"
    page = urllib2.urlopen(url=imdb_movie_loc_url, timeout=10)
    soup = BeautifulSoup(page)
    
    movie_locations = []
    for location in soup.select(".soda"):
        actual_location = location.select("dt a")[0].contents[0].strip()
        movie_location = location.select("dd")[0].contents[0].strip()
        geocoding = json.load(urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address=" + urllib2.quote(location["actual_location"].encode("utf8")).replace("%20", "+") + "&sensor=false"))
        movie_locations.append({"actual_location":actual_location, "movie_location":movie_location, "geocoding": geocoding, "source": "imdb"})

    # return an object containing all data above
    return {"index":counter,
            "imdb_id":movie_id,
            "name":movie_name,
            "year":movie_year,
            "desc":movie_description,
            "rate":movie_rate,
            "genres":movie_genres,
            "locations":movie_locations}

if __name__ == '__main__':
    top1000_list = get_top1000_list()
    error_ids = []
    
    for movie_id in top1000_list:
        counter += 1
        sys.stdout.write("visiting movie page " + str(counter)+ "/" + str(len(top1000_list)) + ": " + movie_id + "...")
        try:
            data.append(get_movie_info(movie_id))
            print "done"
        except (IndexError, URLError, _socket.error) as e:
            print "error"
            error_ids.append(movie_id)
    
    dump_data()
    log_error("\n".join(error_ids))
    
    print "done"
