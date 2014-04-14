import json
import urllib2

if __name__ == '__main__':
    f = open("imdb_data.json")
    data = json.load(f)
    f.close()
    
    counter = 0
    
    for entry in data:
        for location in entry["locations"]:
            gcdata = location["geocoding"]
            if gcdata["status"] == "INVALID_REQUEST":
                counter += 1
                location["geocoding"] = json.load(urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address=" + urllib2.quote(location["actual_location"].encode("utf8")).replace("%20", "+") + "&sensor=false", timeout=10))
                print str(counter) + " => " + location["geocoding"]["status"]
    
    f = open("imdb_data_fix.json", "w+")
    f.write(json.dumps(data))
    f.close()
