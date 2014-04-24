# -*- coding: utf-8 -*-

import json, sys

l = ""
m = ""
r = ""

def dump():
    f = open('movies.sql', 'w+')
    f.write(m.encode('utf-8'))
    f.close()
    
    f = open('locations.sql', 'w+')
    f.write(l.encode('utf-8'))
    f.close()
    
    f = open('rel.sql', 'w+')
    f.write(r.encode('utf-8'))
    f.close()
    
def clean(v):
    if v:
        return v.replace("'", "\\'").replace("\n", " ")
    else:
        return ""

if __name__ == '__main__':
    f = open('../refine/3-geocoding_cleanup/geocoding_cleaned.json')
    data = json.load(f)
    f.close()
    
    movieCount = 0
    locationCount = 0
    
    for entry in data:
        movieCount += 1
        
        m += "INSERT INTO movie VALUES (" + str(movieCount) + ",'" \
            + clean(json.dumps(entry["cast"])) + "', '" \
            + clean(entry["desc"]) + "', '" \
            + clean(json.dumps(entry["director"])) + "', '" \
            + clean(json.dumps(entry["genres"])) + "', '" \
            + clean(entry["rate"]) + "', '" \
            + clean(entry["name"]) + "', '" \
            + clean(entry["year"]) + "', '" \
            + clean(str(entry["id"])) + "');\n"
            
        if entry["locations"]:
            for location in entry["locations"]:
                locationCount += 1
                
                print "l => " + str(locationCount) + "                    m => " + str(movieCount)
            
                l += "INSERT INTO location VALUES (" + str(locationCount) + ", '" \
                    + clean(location["actual_location"]) + "', '"
                    
                if location["geocoding"] and (location["geocoding"]["status"] == "OK"):
                    gc = location["geocoding"]["results"][0]
                    address_fragments = ""
                    for fragment in gc["address_components"]:
                        address_fragments += fragment["long_name"] + "|" + fragment["short_name"] + "|"
                    l += clean(address_fragments) + "', '"
                    l += clean(gc["formatted_address"]) + "', "
                    l += str(gc["geometry"]["location"]["lat"]) + ", "
                    l += str(gc["geometry"]["location"]["lng"]) + ", "
                else:
                    l += "', NULL, NULL, NULL, "
                
                l += str(movieCount) + ", '"
                l += clean(location["movie_location"]) + "', '" \
                    + clean(location["source"]) + "');\n"
                    
                r += "INSERT INTO movie_location VALUES (" + str(movieCount) + ", " + str(locationCount) + ");\n"
    dump()