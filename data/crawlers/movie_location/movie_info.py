import json

info = []
def dump():
    f = open("movie_info_csv.json", "w+")
    f.write(json.dumps(data))
    f.close()

if __name__ == '__main__':
    location = open('movie_location_detail.json')
    data = load(location)
    for movie in data:
        temp = {"id": movie["id"],
                "year": movie["year"],
                "name": movie["name"]}
        info.append(temp)
    dump(info)