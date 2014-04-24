import json

data = []

def dump():
    f = open("geocoding_cleaned.json", "w+")
    f.write(json.dumps(data))
    f.close()

if __name__ == '__main__':
    f = open("../2-geocoding_fix/geocoding_fixed.json")
    data = json.load(f)
    f.close()
    
    for entry in data:
        to_remove = []
    
        for idx in xrange(len(entry["locations"])):
            location = entry["locations"][idx]
            gc = location["geocoding"]
            if gc["status"] != "OK":
                to_remove.append(idx)
            else:
                gc["results"] = gc["results"][:1]
                
        for idx in reversed(to_remove):
            entry["locations"].pop(idx)
            
    dump()