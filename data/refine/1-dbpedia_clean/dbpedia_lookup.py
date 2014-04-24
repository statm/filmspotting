# -*- coding: utf-8 -*-
import _socket
import json
import re
import urllib2
from urllib2 import URLError, urlopen, HTTPError

BATCH_SIZE = 300

def dump(file, data):
    f = open(file, "w+")
    f.write(json.dumps(data))
    f.close()

if __name__ == '__main__':
    file = open("../../linkage/link.json")
    data = json.load(file)
    delete = []
    counter = 0
    batch_count = 0
    
    result_data = []
    
    for entry in data:
        try:
            counter += 1
            print str(counter) + ". " + entry["name"]
            print "   > total location entries: " + str(len(entry["locations"]))
            
            del_index = []
            for idx in xrange(len(entry["locations"])):
                if entry["locations"][idx]["source"] == "movie_location":
                    location = re.sub('[\s|,]+', '_', entry["locations"][idx]["actual_location"])
                    query = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryString="+urllib2.quote(location.encode('utf8'))
                    page = urllib2.urlopen(url=query, timeout=10).read()
                    if page.count('<Label>person</Label>') > 0 or page.count('<Label>country</Label>') > 0:
                        print "     > " + entry["locations"][idx]["actual_location"]
                        del_index.append(idx)
 
            print "   > " + str(len(del_index)) + " locations are deleted"
            print ""
            
            for idx in reversed(del_index):
                delete.append(entry["locations"][idx]["actual_location"])
                entry["locations"].pop(idx)
            
            result_data.append(entry)
            
            if counter >= BATCH_SIZE:
                counter = 0
                batch_count += 1
                dump("deleted_" + str(batch_count) + ".json", delete)
                dump("cleaned_" + str(batch_count) + ".json", result_data)
                delete = []
                result_data = []
            
                
        except (IndexError, URLError, _socket.error) as e:
            print "*** error occured for movie: " + entry["name"]
    
    dump("deleted_" + str(batch_count) + ".json", delete)
    dump("cleaned_" + str(batch_count) + ".json", result_data)