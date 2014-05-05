import json
from sets import Set
sourceA = open('link_imdb_filmaps.json')
filmaps = json.load(sourceA)
sourceB = open('link_ml_imdb.json')
ml = json.load(sourceB)
sourceC = open('all_link.json')
all = json.load(sourceC)
sourceD = open('imdb_data.json')
imdb = json.load(sourceD)
ids = set()
count = 0
for entry in filmaps:
    ids.add(entry["imdb_id"])
    count += 1
for entry in ml:
    ids.add(entry["imdb_id"])
    count += 1
for entry in all:
    ids.add(entry["imdb_id"])
    count += 1
for entry in imdb:
    ids.add(entry["imdb_id"])
    count += 1
print len(ids)
print count