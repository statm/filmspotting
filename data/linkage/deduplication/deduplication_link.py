import csv
import json
from sets import Set

def dump(file, data):
    f = open(file, "w+")
    f.write(json.dumps(data))
    f.close()
            
if __name__ == '__main__':
    sourceA = open('../link_new.json')
    fm = json.load(sourceA)
    to_remove_ids = []
    to_remove_objs = []
    to_insert_objs = []
    keep_ids = []
    ids = []
    idxs = []
    data = []
    with open('duplicate_link.csv') as sourceB:
        reader = csv.DictReader(sourceB, delimiter=',')
        temp = []
        name = ''
        for line in reader:
            id = line["id"]
            idxs.append(str(id))
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
    print len(fm)
    print len(idxs)
    counter = 0
    for list in ids:
        locations = []
        for entry in fm:
            if entry["id"] in list:
                for location in entry["locations"]:
                    if location not in locations:
                        locations.append(location)
        item = {}
        for entry in fm:
            if str(entry["id"]) == str(list[0]):
                item = entry
                break
        new_obj = {  "id": item["id"],
                     "name": item["name"],
                     "year": item["year"],
                     "genres": item["genres"],
                     "rate": item["rate"],
                     "desc": item["desc"],
                     "director": item["director"],
                     "cast": item["cast"],
                     "location_images": item["location_images"],
                     "locations": locations}
        to_insert_objs.append(new_obj)
        counter += 1
    fm = [entry for entry in fm if str(entry["id"]) not in idxs]
    print len(fm)
    for entry in to_insert_objs:
        fm.append(entry)
    print len(fm)
    dump("link_clean.json", fm)
    dump("insert.json", to_insert_objs)
    