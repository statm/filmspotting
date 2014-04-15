import json

csv_str = ''
def dump():
    f = open("../linkage/imdb.csv", "w+")
    f.write(csv_str.encode('utf8'))
    f.close()

if __name__ == '__main__':
    location = open('../crawlers/imdb/imdb_data.json')
    data = json.load(location)
    csv_str = '"id","name","year"\n'
    for movie in data:
        csv_str += '"' + movie["imdb_id"] + '","' + movie["name"] + '","' + str(movie["year"]) + '"\n'
    dump()