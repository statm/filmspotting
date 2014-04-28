import csv
import json

def dump(file, data):
    f = open(file, "w+")
    f.write(json.dumps(data))
    f.close()
            
if __name__ == '__main__':
    sourceA = open('filmaps.json')
    films = json.load(sourceA)
    for entry in films:
        entry["id"] = "fm" + str(entry["id"])
        entry["name"] = entry["name"].strip()
    dump("filmaps_new.json", films)