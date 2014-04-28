import csv
import json

data = []
def dump(file):
    f = open(file, "w+")
    f.write(json.dumps(data))
    f.close()
    
def find_index(attr, id, obj):
    for i, j in enumerate(obj):
        if str(j[attr]) == id:
            return i
            
if __name__ == '__main__':
    sourceA = open('link_ml_imdb.json')
    link = json.load(sourceA)
    
    sourceB = open('../crawlers/filmaps/filmaps.json')
    filmaps = json.load(sourceB)
    
    link_linked_index = []
    filmaps_linked_index = []
    
    with open('linkage_result_fimaps_imdb.csv') as linkage:
        reader = csv.DictReader(linkage, delimiter=',')
        for line in reader:
            index_loc = find_index("id", line["id@sourceB"], filmaps)
            index_link = find_index("id", line["id@sourceA"], link)
            print line["id@sourceB"]
            link_linked_index.append(index_link)
            filmaps_linked_index.append(index_loc)
            locations = []
            for location in filmaps[index_loc]["locations"]:
                temp = {"movie_location": location["description"],
                        "actual_location": location["location"],
                        "source": "filmaps",
                        "geocoding": location["geocoding"]}
                locations.append(temp)
            for location in link[index_link]["locations"]:
                locations.append(location)
            movie = {"id": link[index_link]["id"],
                     "name": link[index_link]["name"], 
                     "year": link[index_link]["year"],
                     "genres": link[index_link]["genres"],
                     "rate": link[index_link]["rate"],
                     "desc": link[index_link]["desc"],
                     "director": link[index_link]["director"],
                     "cast": link[index_link]["cast"],
                     "location_images": link[index_link]["location_images"],
                     "locations": locations}
            #print movie
            data.append(movie) 
    
    for index, entry in enumerate(link):
        if index not in link_linked_index:
            movie = {"id": entry["id"],
                     "name": entry["name"],
                     "year": entry["year"],
                     "genres": entry["genres"],
                     "rate": entry["rate"],
                     "desc": entry["desc"],
                     "director": entry["director"],
                     "cast": entry["cast"],
                     "location_images": entry["location_images"],
                     "locations": entry["locations"]}
            data.append(movie)
    
    for index, entry in enumerate(filmaps):
        if index not in filmaps_linked_index:
            locations = []
            for location in entry["locations"]:
                loc = {"movie_location": location["description"],
                        "actual_location": location["location"],
                        "source": "filmaps",
                        "geocoding": location["geocoding"]}
                locations.append(loc)
            movie = {"id": entry["id"],
                     "name": entry["name"],
                     "year": None,
                     "genres": None,
                     "rate": None,
                     "desc": None,
                     "director": None,
                     "cast": None,
                     "location_images": None,
                     "locations": locations
                    }
            data.append(movie)
    
    dump('link_new.json')