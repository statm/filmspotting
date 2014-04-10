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
    sourceA = open('imdb_data.json')
    imdb = json.load(sourceA)
    
    sourceB = open('movie_location_detail.json')
    movie_location = json.load(sourceB)
    
    with open('linkage_result.csv') as linkage:
        reader = csv.DictReader(linkage, delimiter=',')
        for line in reader:
            index_loc = find_index("id", line["id@sourceB"], movie_location)
            index_imdb = find_index("imdb_id", line["id@sourceA"], imdb)
            #print index_loc
            #print index_imdb
            locations = []
            for location in movie_location[index_loc]["locations"]:
                temp = {"movie_location": "",
                        "actual_location": location}
                locations.append(temp)
            for location in imdb[index_imdb]["locations"]:
                locations.append(location)
            movie = {"id": line["id@sourceA"],
                     "name": line["name@sourceA"], 
                     "year": line["year@sourceA"],
                     "genres": imdb[index_imdb]["genres"],
                     "rate": imdb[index_imdb]["rate"],
                     "desc": imdb[index_imdb]["desc"],
                     "location_images": movie_location[index_loc]["location_images"],
                     "locations": locations}
            #print movie
            data.append(movie)
    dump('link.json')