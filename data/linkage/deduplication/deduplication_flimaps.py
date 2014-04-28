import csv
import json
from sets import Set

def dump(file, data):
    f = open(file, "w+")
    f.write(json.dumps(data))
    f.close()
            
if __name__ == '__main__':
    sourceA = open('../../crawlers/filmaps/movie_location_c.json')
    fm = json.load(sourceA)
    to_remove_ids = []
    to_remove_objs = []
    to_insert_objs = []
    keep_ids = []
    ids = []
    idxs = []
    data = []
    with open('duplicate_fimaps.csv') as sourceB:
        reader = csv.DictReader(sourceB, delimiter=',')
        temp = []
        name = ''
        for line in reader:
            id = line["id"]
            idxs.append(id)
            if name == line["name"]:
                temp.append(id)
            elif name == '':
                name = line["name"]
                temp.append(id)
            else:
                ids.append(temp)
                temp = []
                temp.append(id)
                name = line["name"]
        ids.append(temp)
    for list in ids:
        locations = []
        id = 0
        name = ""
        for entry in fm:
            if str(entry["id"]) in list:
                id = entry["id"]
                name = entry["name"]
                for location in entry["locations"]:
                    if location not in locations:
                        locations.append(location)
        new_obj = {
                   "id": id,
                   "name": name,
                   "locations": locations}
        to_insert_objs.append(new_obj)
    fm = [entry for entry in fm if str(entry["id"]) not in idxs]
    print len(fm)
    for entry in to_insert_objs:
        fm.append(entry)
    dump("filmaps.json", fm)
    dump("insert.json", to_insert_objs)
    