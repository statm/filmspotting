import json

if __name__ == '__main__':
    f = open("geocoding_cleaned.json")
    data = json.load(f)
    f.close()
    
    loc_parts = []
    
    for entry in data:
        for location in entry["locations"]:
            gc = location["geocoding"]
            if gc["status"] == "OK":
                for addr_comp in gc["results"][0]["address_components"]:
                    if addr_comp["long_name"] not in loc_parts:
                        loc_parts.append(addr_comp["long_name"])
                        
    print len(loc_parts)
                