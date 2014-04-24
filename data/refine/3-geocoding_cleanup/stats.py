import json

if __name__ == '__main__':
    f = open("geocoding_cleaned.json")
    data = json.load(f)
    f.close()
    
    print "movie count: " + str(len(data))
    
    status_table = {}
    
    l = 0
    
    for entry in data:
        for location in entry["locations"]:
            l += 1
            gc = location["geocoding"]
            if not gc["status"] in status_table.keys():
                status_table[gc["status"]] = 1
            else:
                status_table[gc["status"]] += 1
                
                
    print "location count: " + str(l)
    print status_table