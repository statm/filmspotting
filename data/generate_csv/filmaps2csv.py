import json

csv_str = ''
def dump():
    f = open("../linkage/filmaps.csv", "w+")
    f.write(csv_str.encode('utf8'))
    f.close()

if __name__ == '__main__':
    location = open('../crawlers/filmaps/filmaps.json')
    data = json.load(location)
    csv_str = '"id","name"\n'
    for movie in data:
        if movie["name"].find('(') != -1:
            name = movie["name"][:movie["name"].index('(')]
            csv_str += '"' + str(movie["id"]) + '","' + name.strip() + '"\n'
        else:
            csv_str += '"' + str(movie["id"]) + '","' + movie["name"].strip() + '"\n'
    dump()