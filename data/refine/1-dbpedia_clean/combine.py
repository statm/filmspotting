# -*- coding: utf-8 -*-

import json

def dump(file, data):
    f = open(file, "w+")
    f.write(json.dumps(data))
    f.close()
    
data_cleaned = []
data_deleted = []

if __name__ == '__main__':
    for i in range(1, 7):
        f = open("cleaned_" + str(i) + ".json")
        data = json.load(f)
        data_cleaned.extend(data)
        f.close()
        
        f = open("deleted_" + str(i) + ".json")
        data = json.load(f)
        data_deleted.extend(data)
        f.close()
        
    dump("cleaned.json", data_cleaned)
    dump("deleted.json", data_deleted)