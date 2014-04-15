import json

csv_str = ''
def dump():
    f = open("../linkage/movie_location.csv", "w+")
    f.write(csv_str.encode('utf8'))
    f.close()

if __name__ == '__main__':
    location = open('../crawlers/movie_location/movie_location.json')
    data = json.load(location)
    csv_str = '"id","name","year"\n'
    for movie in data:
        csv_str += '"' + str(movie["id"]) + '","' + movie["name"] + '","' + str(movie["year"]).strip() + '"\n'
    dump()