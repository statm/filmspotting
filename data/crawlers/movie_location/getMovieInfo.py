#get all the info of a movie page
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

def findContent(tag):
    name = tag.find('a').text
    temp = clean(tag.find('a').attrs['href'])
    link = "http://www.movie-locations.com/people/"+temp[0].lower()+"/"+temp 
    return {"name": name, "link": link}

def clean(url):
    if url.find("../../") != -1 or url.find("../") != -1:
        url = url[url.rfind("/")+1:]
    return url
    
def get_movie_info(movie_id):
    # basic info
    movie_url = "http://www.movie-locations.com/" + movie_id
    page = urllib2.urlopen(url=movie_url, timeout=10)
    soup = BeautifulSoup(page)
    
    #movie name and year info    
    temp = soup.select("#details h1")[0].contents[0].strip()
    if temp.endswith(')'):
        pos = temp.rfind('(')
        movie_name = temp[:pos]
        movie_year = temp[pos+1:-1]
    else:
        pos = temp.rfind(',')
        movie_name = temp[:pos]
        movie_year = temp[pos+1:]
    

    #movie director info
    director = []
    foundtext = soup.find('h3', text="Director")
    if foundtext.findNext().name == "ul":
        lis = foundtext.findNext().findAll('li')
        for li in lis:
            director.append(findContent(li))
    elif foundtext.findNext().name == "p":
        director.append(findContent(foundtext.findNext()))

    #movie cast info
    cast = []
    foundtext = soup.find('h3', text="Cast")
    if (foundtext != None) and len(foundtext) != 0:
        lis = foundtext.findNext().findAll('li')
        for li in lis:
            cast.append(findContent(li))

    #image info
    location_images = []
    locations = []
    loop = False
    while not loop:
        tlocations = []
        #location and location images info
        details = soup.select("#maintext #illust") + soup.select("#maintext #illustvert")
        for detail in details:
            location = detail.find("img")
            location_img_url = movie_url[:movie_url.rfind('/')+1] + clean(location.attrs["src"])
            location_img_desc = detail.find("p").text
            location_images.append({"location_img_url" : location_img_url,
            "location_img_desc" : location_img_desc})
            node = detail.nextSibling
            while (node.nextSibling is not None) and node.nextSibling.name == "p" :
                para = node.nextSibling
                for link in para.findAll("a"):
                    if link.text != "":
                        tlocations.append(link.text)
                node = para.nextSibling
        for location in soup.select("#maintext .name"):
            if location.text != "":
                tlocations.append(location.text)
        tlocations = list(OrderedDict.fromkeys(tlocations))
        for location in tlocations:
            locations.append({"movie_location": "", "actual_location": location, "source": "movie_location"})
        
        #location info
        # paras = soup.select("#maintext p")
        # tlocations = []
        # for para in paras:
            # if para.findNext()
            # links = para.findAll("a")
            # for link in links:
                # print link.text
                # tlocations.append(link.text)
        # for location in soup.select("#maintext .name"):
            # tlocations.append(location.contents[0].strip())
        # tlocations = list(OrderedDict.fromkeys(tlocations))
        # print tlocations
        # for location in tlocations:
            # locations.append({"movie_location": "", "actual_location": location, "source": "movie_location"})
        # print "OK"    
        #check if there is a second or third page
        hasLoop = False
        for link in soup.select("#maintext p a"):
            if (link.text == "Page 3" and movie_url.find('2') != -1) or (link.text == "Page 2" and movie_url.find('1') != -1):
                movie_url = movie_url[0:movie_url.rfind('/')+1] + link.attrs['href']
                print movie_url
                page = urllib2.urlopen(url=movie_url, timeout=10)
                soup = BeautifulSoup(page)
                hasLoop = True
                break
        if not hasLoop:
            loop = True
                
    # return an object containing all data above
    return {
            "id":counter,
            "name":movie_name,
            "year":movie_year,
            "director": director,
            "cast": cast,
            "location_images":location_images,
            "locations": locations}
    

if __name__ == '__main__':
    movie_list = json.load(open("movie_ids.json"))
    error_id = []
        
    for movie_id in movie_list:
        counter += 1
        # if counter < 20:
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