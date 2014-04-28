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
    sourceA = open('../crawlers/imdb/imdb_data.json')
    imdb = json.load(sourceA)
    
    sourceB = open('../crawlers/movie_location/movie_location.json')
    movie_location = json.load(sourceB)
    
    imdb_linked_index = []
    movie_location_linked_index = []
    
    with open('linkage_result_ml_imdb.csv') as linkage:
        reader = csv.DictReader(linkage, delimiter=',')
        for line in reader:
            index_loc = find_index("id", line["id@sourceB"], movie_location)
            index_imdb = find_index("imdb_id", line["id@sourceA"], imdb)
            print line["id@sourceB"]
            imdb_linked_index.append(index_imdb)
            movie_location_linked_index.append(index_loc)
            locations = []
            for location in movie_location[index_loc]["locations"]:
                temp = {"movie_location": "",
                        "actual_location": location["actual_location"],
                        "source": location["source"],
                        "geocoding": ""}
                locations.append(temp)
            for location in imdb[index_imdb]["locations"]:
                locations.append(location)
            movie = {"id": line["id@sourceA"],
                     "name": line["name@sourceA"], 
                     "year": line["year@sourceA"],
                     "genres": imdb[index_imdb]["genres"],
                     "rate": imdb[index_imdb]["rate"],
                     "desc": imdb[index_imdb]["desc"],
                     "director": movie_location[index_loc]["director"],
                     "cast": movie_location[index_loc]["cast"],
                     "location_images": movie_location[index_loc]["location_images"],
                     "locations": locations}
            #print movie
            data.append(movie) 
    
    for index, entry in enumerate(imdb):
        if index not in imdb_linked_index:
            movie = {"id": entry["imdb_id"],
                     "name": entry["name"],
                     "year": entry["year"],
                     "genres": entry["genres"],
                     "rate": entry["rate"],
                     "desc": entry["desc"],
                     "director": None,
                     "cast": None,
                     "location_images": None,
                     "locations": entry["locations"]}
            data.append(movie)
    
    for index, entry in enumerate(movie_location):
        if index not in movie_location_linked_index:
            locations = []
            for location in entry["locations"]:
                loc = {"movie_location": "",
                        "actual_location": location["actual_location"],
                        "source": location["source"],
                        "geocoding": ""}
                locations.append(loc)
            movie = {"id": entry["id"],
                     "name": entry["name"],
                     "year": entry["year"],
                     "genres": None,
                     "rate": None,
                     "desc": None,
                     "director": entry["director"],
                     "cast": entry["cast"],
                     "location_images": entry["location_images"],
                     "locations": locations
                    }
            data.append(movie)
    
    dump('link_ml_imdb.json')