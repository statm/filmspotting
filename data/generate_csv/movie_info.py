import json

info = []
def dump():
    f = open("imdb_data_detail.json", "w+")
    f.write(json.dumps(info))
    f.close()

if __name__ == '__main__':
    location = open('imdb_data.json')
    data = json.load(location)
    for movie in data:
        temp = {"id": movie["id"],
                "year": movie["year"],
                "name": movie["name"]}
        info.append(temp)
    dump()