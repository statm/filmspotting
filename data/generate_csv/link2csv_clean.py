import json

csv_str = ''
def dump():
    f = open("../linkage/link_new.csv", "w+")
    f.write(csv_str.encode('utf8'))
    f.close()

if __name__ == '__main__':
    location = open('../linkage/deduplication/link_clean.json')
    data = json.load(location)
    csv_str = '"id","name"\n'
    for movie in data:
        csv_str += '"' + str(movie["id"]) + '","' + movie["name"].strip() + '"\n'
    dump()