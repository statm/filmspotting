# -*- coding: utf-8 -*-
import json
import re
import urllib2
from urllib2 import URLError, urlopen, HTTPError

def dump(file, data):
    f = open(file, "w+")
    f.write(json.dumps(data))
    f.close()

if __name__ == '__main__':
    file = open("split/link_5.json")
    data = json.load(file)
    delete = []
    try:
        for entry in data:
            del_index = []
            for idx in xrange(len(entry["locations"])):
                location = re.sub('[\s|,]+', '_', entry["locations"][idx]["actual_location"])
                query = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryString="+urllib2.quote(location.encode('utf8'))
                page = urllib2.urlopen(url=query, timeout=10).read()
                if page.count('Person') > 0 or page.count('Country') > 0:
                    del_index.append(idx)
            print del_index
            for idx in reversed(del_index):
                delete.append(entry["locations"][idx])
                entry["locations"].pop(idx)
    except (urllib2.HTTPError):
        print location
    
    dump("a.json", delete)
    dump("link_5_new.json", data)