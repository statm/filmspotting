import csv
import json

def dump(file, data):
    f = open(file, "w+")
    f.write(json.dumps(data))
    f.close()
    
def find_index(attr, id, obj):
    for i, j in enumerate(obj):
        if str(j[attr]) == id:
            return i
            
if __name__ == '__main__':
    sourceA = open('../../crawlers/movie_location/movie_location.json')
    ml = json.load(sourceA)
    sourceB = open('duplicate_ml.csv')
    to_remove_ids = []
    to_remove_objs = []
    keep_ids = []
    ids = []
    idxs = []
    with open('duplicate_ml.csv') as sourceB:
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
       
    print ids
    print idxs
    for list in ids:
        counter = 0
        for entry in list:
            if counter == 0:
                keep_ids.append(entry)
                counter += 1
    print keep_ids
    to_remove_ids = [item for item in idxs if item not in keep_ids]
    print to_remove_ids
    for entry in ml:
        if str(entry["id"]) in to_remove_ids:
            to_remove_objs.append(entry)
            ml.remove(entry)
    dump("test.json", to_remove_objs)
    dump("movie_location.json", ml)
    