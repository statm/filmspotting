import json
import urllib2
from bs4 import BeautifulSoup
import re
from urllib2 import URLError
import gc

data = []

def dump():
    f = open("imdb_data.json", "w+")
    f.write(json.dumps(data))
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

def get_movie_info(movie_id):
    # basic info
    imdb_movie_url = "http://www.imdb.com/title/" + movie_id + "/"
    page = urllib2.urlopen(url=imdb_movie_url, timeout=10)
    soup = BeautifulSoup(page)
      
    movie_name = soup.select(".header .itemprop")[0].contents[0].strip()
    movie_year = soup.select(".header .nobr a")[0].contents[0].strip()
    movie_rate = soup.select(".star-box-giga-star")[0].contents[0].strip()
      
    movie_genres = []
    for prop in soup.select(".itemprop"):
        if (prop.attrs["itemprop"] == "genre"):
            movie_genres.append(prop.contents[0].strip())
            
    # location info
    imdb_movie_loc_url = "http://www.imdb.com/title/" + movie_id + "/locations"
    page = urllib2.urlopen(url=imdb_movie_loc_url, timeout=10)
    soup = BeautifulSoup(page)
    
    movie_locations = []
    for location in soup.select(".soda"):
        actual_location = location.select("dt a")[0].contents[0].strip()
        movie_location = location.select("dd")[0].contents[0].strip()
        movie_locations.append({"actual_location":actual_location, "movie_location":movie_location})
    
    
    # return an object containing all data above
    return {"id":movie_id,
            "name":movie_name,
            "year":movie_year,
            "rate":movie_rate,
            "genres":movie_genres,
            "locations":movie_locations}

if __name__ == '__main__':
    top1000_list = get_top1000_list()
    error_id = []
    
    counter = 0
    for movie_id in top1000_list:
        counter += 1
        print "visiting movie page " + str(counter)+ "/1000: " + movie_id
        try:
            data.append(get_movie_info(movie_id))
        except IndexError, URLError:
            print "error occured at " + movie_id
            error_id.append(movie_id)
    
    dump()
    print error_id
    
    
#[u'tt0245429', u'tt0986264', u'tt0110357', u'tt0910970', u'tt0095327', u'tt0435761', u'tt0119698', u'tt1049413', u'tt0114709', u'tt0096283', u'tt0347149', u'tt0892769', u'tt0118843', u'tt0087544', u'tt0338564', u'tt0266543', u'tt0353969', u'tt1220719', u'tt0092067', u'tt0423866', u'tt0374546', u'tt0094625', u'tt0198781', u'tt1562872', u'tt0808417', u'tt0382932', u'tt0113568', u'tt0317705', u'tt0103639', u'tt0120363', u'tt2294629', u'tt0129167', u'tt0126029', u'tt1527788', u'tt0398286', u'tt0097814', u'tt1772341', u'tt0286244', u'tt0104652', u'tt1588170', u'tt0158983', u'tt0310775', u'tt0029583', u'tt0876563', u'tt0851578', u'tt1323594', u'tt0451094', u'tt1568921', u'tt1410063', u'tt0111512', u'tt0441773', u'tt1436045', u'tt0070608', u'tt0986233', u'tt0097757', u'tt1386932', u'tt0312004', u'tt0268380', u'tt0032910', u'tt1690953', u'tt1453405', u'tt0120762', u'tt0462538', u'tt0929632', u'tt0385700', u'tt0048280', u'tt0328832', u'tt0046183', u'tt1302011', u'tt0178868', u'tt0120917']