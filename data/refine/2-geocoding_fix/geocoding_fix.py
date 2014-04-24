import json
import urllib2
import sys

data = []

def dump():
    f = open("geocoding_fixed.json", "w+")
    f.write(json.dumps(data))
    f.close()

if __name__ == '__main__':
    f = open("geocoding_fixed.json")
    data = json.load(f)
    f.close()
    
    counter = 0
    status_table = {}
    
    for entry in data:
        for location in entry["locations"]:
            if location["source"] != "imdb" \
            and (location["geocoding"] == "" or location["geocoding"]["status"] == "OVER_QUERY_LIMIT"):
                counter += 1
                
                sys.stdout.write(str(counter) + ") geocoding address: " + location["actual_location"].encode("utf8") + " ...")
                
                gcdata = json.load(urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address=" + urllib2.quote(location["actual_location"].encode("utf8")).replace("%20", "+") + "&sensor=false", timeout=10))
                
                location["geocoding"] = gcdata
                print gcdata["status"]
                
                if gcdata["status"] == "OVER_QUERY_LIMIT":
                    print status_table
                    dump()
                    sys.exit(1)
                
                if gcdata["status"] not in status_table.keys():
                    status_table[gcdata["status"]] = 1
                else:
                    status_table[gcdata["status"]] += 1
    
    print status_table
    dump()