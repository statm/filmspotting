import json

data = []

def dump():
    f = open("imdb_data.json", "w+")
    f.write(json.dumps(data))
    f.close()

if __name__ == '__main__':
    f = open("imdb_data.json", "r")
    data = json.loads(f.read())
    f.close()
    
    count = 0
    for entry in data:
        entry['id'] = count
        count += 1
    
    dump()